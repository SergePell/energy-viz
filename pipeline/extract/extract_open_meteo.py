"""
Extract-Skript für Open-Meteo Historical Weather API.

Funktionsweise:
1. Liest Stations-Konfiguration aus pipeline/config/weather_stations.py
2. Pro Station ein API-Call mit allen 6 Variablen, stündlich
3. Speichert pro Station eine CSV in pipeline/raw/snapshots/<datum>/open_meteo/
4. Aktualisiert das gemeinsame _manifest.json

API-Doku: https://open-meteo.com/en/docs/historical-weather-api
- Kostenlos, keine Authentifizierung
- Rate-Limit: 10'000 Requests/Tag, 5'000/Stunde, 600/Minute
- Wir machen 18 Calls (einer pro Station) — weit unter dem Limit

Aufruf:
    python pipeline/extract/extract_open_meteo.py
        Lädt alle 18 Stationen, Zeitraum 2017-01-01 bis heute

    python pipeline/extract/extract_open_meteo.py --from 2017-01-01 --to 2026-05-01
        Lädt alle 18 Stationen für den angegebenen Zeitraum

    python pipeline/extract/extract_open_meteo.py --station CH-ZH
        Lädt nur eine Station

    python pipeline/extract/extract_open_meteo.py --force
        Überschreibt bestehende Files

Idempotent: zweifaches Ausführen ohne --force überspringt vorhandene Files.

Variablen pro Stunde:
- temperature_2m (°C)
- shortwave_radiation (W/m²)
- direct_radiation (W/m²)
- wind_speed_10m (m/s)
- cloud_cover (%)
- precipitation (mm)

Datenmenge:
- 9 Jahre × 8'760 Stunden × 6 Variablen = ~470'000 Zeilen pro Station
- Pro Station ca. 8-12 MB CSV
- Total ca. 150-200 MB
"""

import argparse
import sys
import time
from datetime import date
from pathlib import Path
from typing import Optional

import requests
import pandas as pd

# Pfad-Setup
PIPELINE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PIPELINE_ROOT.parent))

from pipeline.config.weather_stations import WEATHER_STATIONS, WEATHER_VARIABLES
from pipeline.utils.manifest import (
    init_manifest,
    add_file_to_manifest,
    write_manifest,
    load_manifest,
)


SNAPSHOT_ROOT = PIPELINE_ROOT / "raw" / "snapshots"
SOURCE_FAMILY = "open_meteo"
HTTP_TIMEOUT = 120

API_BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

DEFAULT_START_DATE = "2017-01-01"

HTTP_HEADERS = {
    "User-Agent": "energy-viz-pipeline/0.1 (Masterthesis FHGR; serge.pellegrini@stud.fhgr.ch)",
}

# Pause zwischen Requests, damit wir die API nicht überlasten
SLEEP_BETWEEN_REQUESTS_SEC = 1.0


def fetch_station_data(
    station_id: str,
    station_config: dict,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """
    Holt die Wetterdaten für eine Station vom Open-Meteo Archive-API.
    Returns: DataFrame mit Spalten [time, temperature_2m, ...]
    """
    params = {
        "latitude": station_config["latitude"],
        "longitude": station_config["longitude"],
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ",".join(WEATHER_VARIABLES),
        "timezone": "UTC",  # explizit UTC, konsistent mit Pipeline-Konvention
    }

    response = requests.get(
        API_BASE_URL,
        params=params,
        headers=HTTP_HEADERS,
        timeout=HTTP_TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()

    # API-Antwort hat die Struktur:
    # { "hourly": {"time": [...], "temperature_2m": [...], ...}, ... }
    if "hourly" not in data:
        raise ValueError(f"Keine 'hourly'-Daten in API-Antwort: {data}")

    df = pd.DataFrame(data["hourly"])

    # Zeitstempel als ISO-8601 UTC
    df["time"] = pd.to_datetime(df["time"], utc=True)

    # Spalten umbenennen: zeitstempel_utc statt time
    df = df.rename(columns={"time": "zeitstempel_utc"})

    # Station-ID als Spalte hinzufügen
    df["station_id"] = station_id

    # Spalten-Reihenfolge: zeitstempel_utc, station_id, dann Variablen
    cols = ["zeitstempel_utc", "station_id"] + WEATHER_VARIABLES
    df = df[cols]

    return df


def extract_station(
    station_id: str,
    station_config: dict,
    start_date: str,
    end_date: str,
    snapshot_dir: Path,
    manifest: dict,
    force: bool = False,
) -> bool:
    """Extrahiert die Daten für eine einzelne Station."""
    target_dir = snapshot_dir / SOURCE_FAMILY
    target_dir.mkdir(parents=True, exist_ok=True)

    target_file = target_dir / f"{station_id}.csv"

    print(f"\n→ {station_id} ({station_config['name']})")

    # Idempotenz-Check
    if target_file.exists() and not force:
        print(f"  ✓ {station_id}.csv existiert bereits — übersprungen")

        existing = (
            manifest["sources"]
            .get(SOURCE_FAMILY, {})
            .get(station_id, {})
        )
        if not existing:
            add_file_to_manifest(
                manifest,
                SOURCE_FAMILY,
                station_id,
                "csv",
                target_file,
                f"{API_BASE_URL}?lat={station_config['latitude']}&lon={station_config['longitude']}",
            )
        return True

    # API-Call
    try:
        print(f"  ↓ API-Call für {start_date} bis {end_date}", end=" ", flush=True)
        df = fetch_station_data(station_id, station_config, start_date, end_date)
        print(f"({len(df):,} Zeilen)")

        # Speichern
        df.to_csv(target_file, index=False, encoding="utf-8")
        size_mb = target_file.stat().st_size / (1024 * 1024)
        print(f"  ✓ {station_id}.csv ({size_mb:.1f} MB)")

        # Manifest-Eintrag
        url_with_params = (
            f"{API_BASE_URL}?lat={station_config['latitude']}"
            f"&lon={station_config['longitude']}"
            f"&start_date={start_date}&end_date={end_date}"
        )
        add_file_to_manifest(
            manifest,
            SOURCE_FAMILY,
            station_id,
            "csv",
            target_file,
            url_with_params,
        )
        return True
    except requests.exceptions.HTTPError as e:
        print(f"\n  ! HTTP-Fehler: {e}")
        if hasattr(e.response, "text"):
            print(f"    Response: {e.response.text[:200]}")
        return False
    except Exception as e:
        print(f"\n  ! Fehler: {e}")
        if target_file.exists():
            target_file.unlink()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Extract historische Wetterdaten via Open-Meteo Archive-API"
    )
    parser.add_argument(
        "--date", default=None,
        help="Snapshot-Datum YYYY-MM-DD (default: heute)",
    )
    parser.add_argument(
        "--from", dest="from_date", default=DEFAULT_START_DATE,
        help=f"Start-Datum YYYY-MM-DD (default: {DEFAULT_START_DATE})",
    )
    parser.add_argument(
        "--to", dest="to_date", default=None,
        help="End-Datum YYYY-MM-DD (default: gestern, weil heute oft nicht komplett)",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Bestehende Files überschreiben",
    )
    parser.add_argument(
        "--station", action="append", default=None,
        help="Nur eine spezifische Station ziehen (mehrfach möglich)",
    )
    parser.add_argument(
        "--list", action="store_true",
        help="Verfügbare Stationen listen, kein Download",
    )
    args = parser.parse_args()

    # === --list Mode ===
    if args.list:
        print("Verfügbare Wetterstationen:")
        print()
        for sid, cfg in WEATHER_STATIONS.items():
            print(f"  {sid:15s}  {cfg['name']:18s}  ({cfg['latitude']:.3f}, "
                  f"{cfg['longitude']:.3f}, {cfg['altitude_m']}m)")
        return

    # === Setup ===
    snapshot_date = args.date or date.today().isoformat()
    snapshot_dir = SNAPSHOT_ROOT / snapshot_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    # Default end_date = gestern
    if args.to_date:
        end_date = args.to_date
    else:
        from datetime import timedelta
        yesterday = date.today() - timedelta(days=1)
        end_date = yesterday.isoformat()

    start_date = args.from_date

    # Stations-Auswahl
    if args.station:
        stations_to_extract = {}
        for sid in args.station:
            if sid not in WEATHER_STATIONS:
                print(f"FEHLER: Station '{sid}' nicht in Konfiguration. "
                      f"Verfügbar: {list(WEATHER_STATIONS.keys())}")
                sys.exit(1)
            stations_to_extract[sid] = WEATHER_STATIONS[sid]
    else:
        stations_to_extract = WEATHER_STATIONS

    print(f"Snapshot-Datum: {snapshot_date}")
    print(f"Snapshot-Verzeichnis: {snapshot_dir}")
    print(f"Zeitraum: {start_date} bis {end_date}")
    print(f"Stationen: {len(stations_to_extract)}")
    if args.force:
        print("Modus: FORCE (bestehende Files werden überschrieben)")

    # === Manifest laden oder neu anlegen ===
    existing_manifest = load_manifest(snapshot_dir)
    if existing_manifest and not args.force:
        manifest = existing_manifest
        if SOURCE_FAMILY not in manifest.get("sources", {}):
            print(f"→ Bestehendes Manifest geladen, wird ergänzt um {SOURCE_FAMILY}.")
        else:
            print("→ Bestehendes Manifest geladen, wird aktualisiert.")
    else:
        manifest = init_manifest(snapshot_date, "extract_open_meteo.py")

    # === Extraction ===
    success_count = 0
    fail_count = 0

    for i, (station_id, station_config) in enumerate(stations_to_extract.items()):
        ok = extract_station(
            station_id, station_config,
            start_date, end_date,
            snapshot_dir, manifest, force=args.force,
        )
        if ok:
            success_count += 1
        else:
            fail_count += 1

        # Pause zwischen Requests, ausser nach dem letzten
        if i < len(stations_to_extract) - 1:
            time.sleep(SLEEP_BETWEEN_REQUESTS_SEC)

    # === Manifest schreiben ===
    manifest_path = write_manifest(manifest, snapshot_dir)

    # === Zusammenfassung ===
    print()
    print("=" * 60)
    print(f"Erfolgreich:  {success_count} / {len(stations_to_extract)}")
    if fail_count:
        print(f"Fehlgeschlagen: {fail_count}")
    print(f"Manifest:     {manifest_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()