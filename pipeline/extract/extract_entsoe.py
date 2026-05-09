"""
Extract-Skript für ENTSO-E Transparency Platform.

Holt Day-Ahead-Spotpreise für CH (Bidding Zone 10YCH-SWISSGRIDZ).
Pro API-Call ein Jahr (API-Limit). Ergebnisse werden in eine zusammengefasste
CSV pro Snapshot geschrieben.

API-Doku: https://documenter.getpostman.com/view/7009892/2s93JtP3F6
- Authentifizierung: Token via Header oder Query-Parameter
- Token muss in .env als ENTSOE_API_TOKEN hinterlegt sein
- Rate-Limit: 400 Requests pro Minute (wir machen ~10, weit drunter)

Aufruf:
    python pipeline/extract/extract_entsoe.py
        Zieht Day-Ahead-Spotpreise CH ab 2017 bis heute

    python pipeline/extract/extract_entsoe.py --from-year 2020
        Zieht ab spezifischem Jahr

    python pipeline/extract/extract_entsoe.py --year 2024
        Nur ein spezifisches Jahr

    python pipeline/extract/extract_entsoe.py --force
        Überschreibt bestehende Files

Datenmenge:
- 9 Jahre × 8'760 Stunden ≈ 79'000 Zeilen
- ~3 MB CSV total

Output-Format (UTF-8):
    zeitstempel_utc, gebiet_code, preis_eur_mwh
"""

import argparse
import os
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Optional
from xml.etree import ElementTree as ET

import requests
import pandas as pd

# Pfad-Setup
PIPELINE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PIPELINE_ROOT.parent))

from pipeline.config.entsoe_sources import (
    ENTSOE_BIDDING_ZONE_CH,
    DOCUMENT_TYPE_PRICE,
    ENTSOE_API_BASE,
    DEFAULT_START_YEAR,
)
from pipeline.utils.manifest import (
    init_manifest,
    add_file_to_manifest,
    write_manifest,
    load_manifest,
)


SNAPSHOT_ROOT = PIPELINE_ROOT / "raw" / "snapshots"
SOURCE_FAMILY = "entsoe"
HTTP_TIMEOUT = 120

# ENTSO-E XML-Namespace (in den Antwort-Tags eingebettet)
ENTSOE_NS = {"ns": "urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:3"}


def load_api_token() -> str:
    """
    Lädt das API-Token aus .env oder Umgebungsvariable.
    Priorität: 1) Umgebungsvariable, 2) .env-Datei im Repo-Root.
    """
    token = os.environ.get("ENTSOE_API_TOKEN")
    if token:
        return token

    # .env aus Repo-Root lesen (manuell, ohne python-dotenv-Dependency)
    env_path = PIPELINE_ROOT.parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("ENTSOE_API_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")

    raise RuntimeError(
        "ENTSO-E API-Token nicht gefunden. "
        "Bitte ENTSOE_API_TOKEN in .env hinterlegen oder als Umgebungsvariable setzen."
    )


def format_period(year: int, is_start: bool) -> str:
    """
    Erzeugt Periode im ENTSO-E-Format YYYYMMDDHHmm.
    Start: 1. Januar 00:00 UTC
    Ende: 1. Januar 00:00 UTC des Folgejahres
    """
    if is_start:
        return f"{year}01010000"
    else:
        # Ende = 1.1. des Folgejahres
        return f"{year + 1}01010000"


def fetch_year_prices(year: int, token: str, end_year_partial: bool = False) -> pd.DataFrame:
    """
    Holt Day-Ahead-Spotpreise für ein einzelnes Jahr.
    Returns: DataFrame mit Spalten [zeitstempel_utc, gebiet_code, preis_eur_mwh]

    Wenn end_year_partial=True, wird statt 1.1. des Folgejahres das heutige
    Datum als Ende verwendet (für das laufende Jahr).
    """
    period_start = format_period(year, is_start=True)

    if end_year_partial:
        # Heute 00:00 UTC als Ende für das laufende Jahr
        today = date.today()
        period_end = f"{today.year}{today.month:02d}{today.day:02d}0000"
    else:
        period_end = format_period(year, is_start=False)

    params = {
        "documentType": DOCUMENT_TYPE_PRICE,
        "in_Domain": ENTSOE_BIDDING_ZONE_CH,
        "out_Domain": ENTSOE_BIDDING_ZONE_CH,
        "periodStart": period_start,
        "periodEnd": period_end,
        "securityToken": token,
    }

    response = requests.get(ENTSOE_API_BASE, params=params, timeout=HTTP_TIMEOUT)

    if response.status_code == 401:
        raise RuntimeError("ENTSO-E API: Authentifizierung fehlgeschlagen. Token prüfen.")
    if response.status_code != 200:
        raise RuntimeError(
            f"ENTSO-E API-Fehler {response.status_code}: {response.text[:300]}"
        )

    return parse_price_xml(response.text)


def parse_price_xml(xml_text: str) -> pd.DataFrame:
    """
    Parst die ENTSO-E Publication-XML-Antwort und extrahiert Day-Ahead-Preise.

    Struktur der Antwort:
    <Publication_MarketDocument>
      <TimeSeries>
        <Period>
          <timeInterval>
            <start>2024-01-01T00:00Z</start>
            <end>2024-01-02T00:00Z</end>
          </timeInterval>
          <resolution>PT60M</resolution>
          <Point>
            <position>1</position>
            <price.amount>45.32</price.amount>
          </Point>
          <Point>
            <position>2</position>
            <price.amount>38.71</price.amount>
          </Point>
          ...
        </Period>
      </TimeSeries>
      ...
    </Publication_MarketDocument>

    Pro Period gibt es typischerweise 24 Points (eine pro Stunde).
    Mehrere Periods für unterschiedliche Tage.
    """
    rows = []
    root = ET.fromstring(xml_text)

    # Falls Antwort eine Acknowledgement (kein Daten-Doc) ist: leerer DataFrame
    if "Acknowledgement" in root.tag:
        # Tag-Inhalt ausgeben für Diagnose
        reason = root.find(".//{*}Reason/{*}text")
        msg = reason.text if reason is not None else "unbekannt"
        print(f"    Hinweis von ENTSO-E: {msg}")
        return pd.DataFrame(columns=["zeitstempel_utc", "gebiet_code", "preis_eur_mwh"])

    # TimeSeries-Elemente durchgehen
    for ts in root.findall(".//{*}TimeSeries"):
        for period in ts.findall(".//{*}Period"):
            time_interval = period.find("{*}timeInterval")
            if time_interval is None:
                continue
            start_elem = time_interval.find("{*}start")
            if start_elem is None:
                continue
            start_str = start_elem.text  # z.B. "2024-01-01T00:00Z"
            start_dt = pd.Timestamp(start_str)

            resolution_elem = period.find("{*}resolution")
            resolution = resolution_elem.text if resolution_elem is not None else "PT60M"

            # Resolution parsen — typisch PT60M (60 Min) oder PT15M (15 Min)
            if resolution == "PT60M":
                interval_minutes = 60
            elif resolution == "PT15M":
                interval_minutes = 15
            elif resolution == "PT30M":
                interval_minutes = 30
            else:
                # Fallback: 60 Min annehmen
                interval_minutes = 60

            for point in period.findall("{*}Point"):
                position_elem = point.find("{*}position")
                price_elem = point.find("{*}price.amount")
                if position_elem is None or price_elem is None:
                    continue

                position = int(position_elem.text)
                price = float(price_elem.text)

                # Zeitstempel = start + (position - 1) * interval
                ts_utc = start_dt + pd.Timedelta(minutes=(position - 1) * interval_minutes)
                rows.append({
                    "zeitstempel_utc": ts_utc.isoformat(),
                    "gebiet_code": "CH",
                    "preis_eur_mwh": price,
                })

    return pd.DataFrame(rows)


def extract_year(
    year: int,
    token: str,
    snapshot_dir: Path,
    manifest: dict,
    force: bool = False,
    end_year_partial: bool = False,
) -> bool:
    """Extrahiert die Day-Ahead-Preise für ein Jahr in eine Jahres-CSV."""
    target_dir = snapshot_dir / SOURCE_FAMILY
    target_dir.mkdir(parents=True, exist_ok=True)

    target_file = target_dir / f"day_ahead_prices_ch_{year}.csv"

    print(f"\n→ ENTSO-E Day-Ahead CH {year}")

    # Idempotenz-Check (ausser für laufendes Jahr — das ändert sich täglich)
    if target_file.exists() and not force and not end_year_partial:
        print(f"  ✓ {target_file.name} existiert bereits — übersprungen")

        existing = (
            manifest["sources"]
            .get(SOURCE_FAMILY, {})
            .get(f"day_ahead_prices_ch_{year}", {})
        )
        if not existing:
            add_file_to_manifest(
                manifest, SOURCE_FAMILY,
                f"day_ahead_prices_ch_{year}",
                "csv", target_file,
                f"{ENTSOE_API_BASE}?...year={year}",
            )
        return True

    # API-Call
    try:
        print(f"  ↓ API-Call", end=" ", flush=True)
        df = fetch_year_prices(year, token, end_year_partial=end_year_partial)
        print(f"({len(df):,} Zeilen)")

        if df.empty:
            print(f"  ! Keine Daten für {year} erhalten — Datei wird nicht geschrieben")
            return False

        # Sortieren und speichern
        df = df.sort_values("zeitstempel_utc").reset_index(drop=True)
        df.to_csv(target_file, index=False, encoding="utf-8")
        size_kb = target_file.stat().st_size / 1024
        print(f"  ✓ {target_file.name} ({size_kb:.1f} KB)")

        # Manifest-Eintrag (Token wird aus URL für Sicherheit entfernt)
        url_for_manifest = (
            f"{ENTSOE_API_BASE}?documentType={DOCUMENT_TYPE_PRICE}"
            f"&in_Domain={ENTSOE_BIDDING_ZONE_CH}"
            f"&out_Domain={ENTSOE_BIDDING_ZONE_CH}"
            f"&periodStart={format_period(year, is_start=True)}"
            f"&periodEnd={format_period(year, is_start=False)}"
        )
        add_file_to_manifest(
            manifest, SOURCE_FAMILY,
            f"day_ahead_prices_ch_{year}",
            "csv", target_file, url_for_manifest,
        )
        return True
    except Exception as e:
        print(f"\n  ! Fehler: {e}")
        if target_file.exists():
            target_file.unlink()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Extract Day-Ahead-Spotpreise CH von ENTSO-E"
    )
    parser.add_argument(
        "--date", default=None,
        help="Snapshot-Datum YYYY-MM-DD (default: heute)",
    )
    parser.add_argument(
        "--from-year", type=int, default=DEFAULT_START_YEAR,
        help=f"Ab welchem Jahr (default: {DEFAULT_START_YEAR})",
    )
    parser.add_argument(
        "--year", action="append", type=int, default=None,
        help="Nur ein spezifisches Jahr ziehen (mehrfach möglich)",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Bestehende Files überschreiben",
    )
    args = parser.parse_args()

    # Token laden
    try:
        token = load_api_token()
    except RuntimeError as e:
        print(f"FEHLER: {e}")
        sys.exit(1)

    # Setup
    snapshot_date = args.date or date.today().isoformat()
    snapshot_dir = SNAPSHOT_ROOT / snapshot_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    # Jahre bestimmen
    current_year = date.today().year
    if args.year:
        years_to_extract = sorted(args.year)
    else:
        years_to_extract = list(range(args.from_year, current_year + 1))

    print(f"Snapshot-Datum: {snapshot_date}")
    print(f"Snapshot-Verzeichnis: {snapshot_dir}")
    print(f"Jahre zu extrahieren: {years_to_extract}")
    if args.force:
        print("Modus: FORCE (bestehende Files werden überschrieben)")

    # Manifest laden oder neu anlegen
    existing_manifest = load_manifest(snapshot_dir)
    if existing_manifest and not args.force:
        manifest = existing_manifest
        if SOURCE_FAMILY not in manifest.get("sources", {}):
            print(f"→ Bestehendes Manifest geladen, wird ergänzt um {SOURCE_FAMILY}.")
        else:
            print("→ Bestehendes Manifest geladen, wird aktualisiert.")
    else:
        manifest = init_manifest(snapshot_date, "extract_entsoe.py")

    # Extraction
    success_count = 0
    fail_count = 0

    for year in years_to_extract:
        # Laufendes Jahr nur bis heute, nicht bis 1.1. nächstes Jahr
        is_partial = (year == current_year)
        ok = extract_year(
            year, token, snapshot_dir, manifest,
            force=args.force, end_year_partial=is_partial,
        )
        if ok:
            success_count += 1
        else:
            fail_count += 1

    # Manifest schreiben
    manifest_path = write_manifest(manifest, snapshot_dir)

    # Zusammenfassung
    print()
    print("=" * 60)
    print(f"Erfolgreich:  {success_count} / {len(years_to_extract)}")
    if fail_count:
        print(f"Fehlgeschlagen: {fail_count}")
    print(f"Manifest:     {manifest_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()