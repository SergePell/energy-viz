"""
Transform-Skript für Open-Meteo Wetterdaten.

Funktionsweise:
1. Liest alle 18 Station-CSVs aus pipeline/raw/snapshots/<datum>/open_meteo/
2. Konsolidiert die Stationen in eine einzige Tabelle
3. Bereinigt Duplikate
4. Sortiert nach Zeitstempel und Station
5. Speichert als Parquet in pipeline/intermediate/<datum>/fact/

Aufruf:
    python pipeline/transform/transform_wetter.py
        Konsolidiert alle Stationen

    python pipeline/transform/transform_wetter.py --force
        Überschreibt bestehenden Output

Output-Schema fact/wetter_stuendlich.parquet:
    zeitstempel_utc          datetime64[us, UTC]
    wetterstation_code       str (CH-AG, CH-AI_AR, ...)
    temperature_2m           float64    Temperatur in 2m Höhe (°C)
    shortwave_radiation      float64    Globalstrahlung (W/m²)
    direct_radiation         float64    Direkte Strahlung (W/m²)
    wind_speed_10m           float64    Windgeschwindigkeit in 10m Höhe (m/s)
    cloud_cover              int64      Bewölkung (%)
    precipitation            float64    Niederschlag (mm)

Hinweise:
- Format ist "Wide-Long-Mix": eine Zeile pro (Zeitstempel × Station),
  die 6 Wetter-Variablen als Spalten. Diese Struktur ist üblich für
  multivariate Sensordaten und joinbar mit Energie-Faktentabellen.

- Die Spalte "station_id" aus dem Extract heisst hier "wetterstation_code"
  für Konsistenz mit der allgemeinen Pipeline-Konvention (alle Code-Spalten
  enden auf _code).

Datenmenge:
- 18 Stationen × ~82'000 Stunden = ~1.48 Mio Zeilen
- Geschätzt 30-50 MB Parquet (komprimiert)
"""

import argparse
import sys
from datetime import date
from pathlib import Path
from typing import Optional

import pandas as pd

# Pfad-Setup
PIPELINE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PIPELINE_ROOT.parent))

from pipeline.utils.manifest import (
    init_manifest,
    add_file_to_manifest,
    write_manifest,
    load_manifest,
)


SNAPSHOT_ROOT = PIPELINE_ROOT / "raw" / "snapshots"
INTERMEDIATE_ROOT = PIPELINE_ROOT / "intermediate"


def find_latest_snapshot() -> Optional[str]:
    """Findet das neueste Snapshot-Datum mit Open-Meteo-Daten."""
    if not SNAPSHOT_ROOT.exists():
        return None

    candidates = []
    for entry in SNAPSHOT_ROOT.iterdir():
        if not entry.is_dir():
            continue
        if (entry / "open_meteo").exists():
            candidates.append(entry.name)

    if not candidates:
        return None

    return sorted(candidates)[-1]


def load_and_consolidate(open_meteo_dir: Path) -> pd.DataFrame:
    """
    Liest alle 18 Stations-CSVs ein und konsolidiert sie in eine Tabelle.
    """
    csv_files = sorted(open_meteo_dir.glob("CH-*.csv"))
    if not csv_files:
        return pd.DataFrame()

    dfs = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        dfs.append(df)
        print(f"    {csv_file.stem:15s}: {len(df):,} Zeilen")

    combined = pd.concat(dfs, ignore_index=True)
    return combined


def transform_wetter(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bereinigt und transformiert die Wetterdaten.
    """
    if df.empty:
        return df

    # Zeitstempel parsen (kommt als String aus CSV)
    df["zeitstempel_utc"] = pd.to_datetime(df["zeitstempel_utc"], utc=True)

    # Spalte umbenennen für Pipeline-Konvention
    df = df.rename(columns={"station_id": "wetterstation_code"})

    # Duplikate droppen (sollten keine sein, aber Sicherheits-Check)
    n_before = len(df)
    df = df.drop_duplicates(subset=["zeitstempel_utc", "wetterstation_code"])
    n_dropped = n_before - len(df)
    if n_dropped > 0:
        print(f"  → {n_dropped} Duplikat(e) entfernt")

    # Sortieren
    df = df.sort_values(["zeitstempel_utc", "wetterstation_code"]).reset_index(drop=True)

    # Spalten-Reihenfolge sicherstellen
    columns_order = [
        "zeitstempel_utc",
        "wetterstation_code",
        "temperature_2m",
        "shortwave_radiation",
        "direct_radiation",
        "wind_speed_10m",
        "cloud_cover",
        "precipitation",
    ]
    df = df[columns_order]

    return df


def main():
    parser = argparse.ArgumentParser(
        description="Transform Open-Meteo Wetterdaten in eine konsolidierte Faktentabelle"
    )
    parser.add_argument(
        "--snapshot", default=None,
        help="Snapshot-Datum YYYY-MM-DD (default: neuester verfügbarer)",
    )
    parser.add_argument(
        "--intermediate-date", default=None,
        help="Output-Datum YYYY-MM-DD (default: heute)",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Bestehende Output-Files überschreiben",
    )
    args = parser.parse_args()

    # === Snapshot bestimmen ===
    if args.snapshot:
        snapshot_date = args.snapshot
    else:
        snapshot_date = find_latest_snapshot()
        if not snapshot_date:
            print("FEHLER: Kein Snapshot mit Open-Meteo-Daten gefunden.")
            sys.exit(1)

    snapshot_dir = SNAPSHOT_ROOT / snapshot_date
    open_meteo_dir = snapshot_dir / "open_meteo"

    if not open_meteo_dir.exists():
        print(f"FEHLER: {open_meteo_dir} existiert nicht.")
        sys.exit(1)

    # === Output-Datum ===
    intermediate_date = args.intermediate_date or date.today().isoformat()
    intermediate_dir = INTERMEDIATE_ROOT / intermediate_date
    fact_dir = intermediate_dir / "fact"
    fact_dir.mkdir(parents=True, exist_ok=True)

    output_path = fact_dir / "wetter_stuendlich.parquet"

    print(f"Snapshot-Datum:       {snapshot_date}")
    print(f"Snapshot-Verzeichnis: {snapshot_dir}")
    print(f"Output-Datum:         {intermediate_date}")
    print(f"Output-Pfad:          {output_path}")

    # Idempotenz-Check
    if output_path.exists() and not args.force:
        print()
        print("✓ Output-File existiert bereits — übersprungen.")
        print(f"  Mit --force überschreiben.")
        return

    # === Verarbeitung ===
    print()
    print("→ CSV-Files einlesen (18 Stationen)")
    df = load_and_consolidate(open_meteo_dir)

    if df.empty:
        print("FEHLER: Keine Open-Meteo CSV-Files gefunden.")
        sys.exit(1)

    print(f"  Konsolidiert: {len(df):,} Zeilen total")

    print("→ Bereinigen und transformieren")
    df = transform_wetter(df)
    print(f"  Final: {len(df):,} Zeilen")

    # Statistik
    min_ts = df["zeitstempel_utc"].min()
    max_ts = df["zeitstempel_utc"].max()
    n_stations = df["wetterstation_code"].nunique()
    min_temp = df["temperature_2m"].min()
    max_temp = df["temperature_2m"].max()
    mean_temp = df["temperature_2m"].mean()

    print()
    print(f"  Zeitraum:    {min_ts} bis {max_ts}")
    print(f"  Stationen:   {n_stations}")
    print(f"  Temperatur:  {min_temp:.1f}°C bis {max_temp:.1f}°C (Mittel: {mean_temp:.1f}°C)")

    # === Output schreiben ===
    print()
    print("→ Output schreiben")
    df.to_parquet(output_path, index=False)
    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"  ✓ {output_path.name} ({size_mb:.1f} MB, {len(df):,} Zeilen)")

    # === Manifest ===
    existing_manifest = load_manifest(intermediate_dir)
    if existing_manifest:
        manifest = existing_manifest
    else:
        manifest = init_manifest(intermediate_date, "transform_wetter.py")

    add_file_to_manifest(
        manifest, "fact", "wetter_stuendlich", "parquet", output_path,
        f"transform_wetter.py from {open_meteo_dir.relative_to(PIPELINE_ROOT.parent)}",
    )

    manifest_path = write_manifest(manifest, intermediate_dir)

    print()
    print("=" * 60)
    print(f"Erfolgreich abgeschlossen.")
    print(f"Manifest: {manifest_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()