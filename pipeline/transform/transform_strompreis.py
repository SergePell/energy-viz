"""
Transform-Skript für ENTSO-E Day-Ahead-Spotpreise CH.

Funktionsweise:
1. Liest alle CSV-Files aus pipeline/raw/snapshots/<datum>/entsoe/
2. Konsolidiert die Jahre in eine einzige Tabelle
3. Bereinigt Duplikate (z.B. DST-Übergänge können doppelte Zeitstempel erzeugen)
4. Sortiert nach Zeitstempel
5. Speichert als Parquet in pipeline/intermediate/<datum>/fact/

Aufruf:
    python pipeline/transform/transform_strompreis.py
        Konsolidiert alle verfügbaren Jahre

    python pipeline/transform/transform_strompreis.py --force
        Überschreibt bestehenden Output

Output-Schema fact/strompreis_stuendlich.parquet:
    zeitstempel_utc      datetime64[us, UTC]
    gebiet_code          str ("CH")
    preis_eur_mwh        float64

Datenmenge:
- 9 Jahre × 8'760 Stunden + 1 Schaltjahr = ~79'000 Zeilen
- ~1.5 MB Parquet
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
    """Findet das neueste Snapshot-Datum mit ENTSO-E-Daten."""
    if not SNAPSHOT_ROOT.exists():
        return None

    candidates = []
    for entry in SNAPSHOT_ROOT.iterdir():
        if not entry.is_dir():
            continue
        if (entry / "entsoe").exists():
            candidates.append(entry.name)

    if not candidates:
        return None

    return sorted(candidates)[-1]


def load_and_consolidate(entsoe_dir: Path) -> pd.DataFrame:
    """
    Liest alle ENTSO-E CSV-Files ein und konsolidiert sie in eine Tabelle.
    """
    csv_files = sorted(entsoe_dir.glob("day_ahead_prices_ch_*.csv"))
    if not csv_files:
        return pd.DataFrame()

    dfs = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        dfs.append(df)
        print(f"    {csv_file.name}: {len(df):,} Zeilen")

    combined = pd.concat(dfs, ignore_index=True)
    return combined


def transform_strompreis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bereinigt und sortiert die konsolidierten Strompreis-Daten.
    """
    if df.empty:
        return df

    # Zeitstempel zu Pandas-Datetime parsen (ist bereits ISO-8601 UTC aus Extract)
    df["zeitstempel_utc"] = pd.to_datetime(df["zeitstempel_utc"], utc=True)

    # Duplikate droppen (z.B. DST-Übergänge oder Überlappungen zwischen Jahres-Files)
    n_before = len(df)
    df = df.drop_duplicates(subset=["zeitstempel_utc", "gebiet_code"])
    n_dropped = n_before - len(df)
    if n_dropped > 0:
        print(f"  → {n_dropped} Duplikat(e) entfernt")

    # Sortieren
    df = df.sort_values("zeitstempel_utc").reset_index(drop=True)

    return df


def main():
    parser = argparse.ArgumentParser(
        description="Transform ENTSO-E Strompreise in eine konsolidierte Faktentabelle"
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
            print("FEHLER: Kein Snapshot mit ENTSO-E-Daten gefunden.")
            sys.exit(1)

    snapshot_dir = SNAPSHOT_ROOT / snapshot_date
    entsoe_dir = snapshot_dir / "entsoe"

    if not entsoe_dir.exists():
        print(f"FEHLER: {entsoe_dir} existiert nicht.")
        sys.exit(1)

    # === Output-Datum ===
    intermediate_date = args.intermediate_date or date.today().isoformat()
    intermediate_dir = INTERMEDIATE_ROOT / intermediate_date
    fact_dir = intermediate_dir / "fact"
    fact_dir.mkdir(parents=True, exist_ok=True)

    output_path = fact_dir / "strompreis_stuendlich.parquet"

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
    print("→ CSV-Files einlesen")
    df = load_and_consolidate(entsoe_dir)

    if df.empty:
        print("FEHLER: Keine ENTSO-E CSV-Files gefunden.")
        sys.exit(1)

    print(f"  Konsolidiert: {len(df):,} Zeilen total")

    print("→ Bereinigen und sortieren")
    df = transform_strompreis(df)
    print(f"  Final: {len(df):,} Zeilen")

    # Statistik
    min_ts = df["zeitstempel_utc"].min()
    max_ts = df["zeitstempel_utc"].max()
    min_preis = df["preis_eur_mwh"].min()
    max_preis = df["preis_eur_mwh"].max()
    mean_preis = df["preis_eur_mwh"].mean()

    print()
    print(f"  Zeitraum: {min_ts} bis {max_ts}")
    print(f"  Preise:   {min_preis:.2f} bis {max_preis:.2f} EUR/MWh (Mittel: {mean_preis:.2f})")

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
        manifest = init_manifest(intermediate_date, "transform_strompreis.py")

    add_file_to_manifest(
        manifest, "fact", "strompreis_stuendlich", "parquet", output_path,
        f"transform_strompreis.py from {entsoe_dir.relative_to(PIPELINE_ROOT.parent)}",
    )

    manifest_path = write_manifest(manifest, intermediate_dir)

    print()
    print("=" * 60)
    print(f"Erfolgreich abgeschlossen.")
    print(f"Manifest: {manifest_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()