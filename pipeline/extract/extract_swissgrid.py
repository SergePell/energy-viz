"""
Extract-Skript für Swissgrid Energieübersicht (15-Min-Daten 2009–heute).

Funktionsweise:
1. Liest die URL-Konfiguration aus pipeline/config/swissgrid_sources.py
2. Lädt pro Jahr eine Excel-Datei herunter (.xls 2009-2019, .xlsx ab 2020)
3. Speichert sie in pipeline/raw/snapshots/<datum>/swissgrid/
4. Aktualisiert das gemeinsame _manifest.json

Aufruf:
    python pipeline/extract/extract_swissgrid.py
        Lädt alle Jahres-Files (2009 bis aktuelles Jahr)

    python pipeline/extract/extract_swissgrid.py --year 2024
        Lädt nur ein spezifisches Jahr (mehrfach möglich: --year 2024 --year 2025)

    python pipeline/extract/extract_swissgrid.py --from 2018
        Lädt ab dem angegebenen Jahr bis zum Ende der Konfiguration

    python pipeline/extract/extract_swissgrid.py --force
        Überschreibt bestehende Files

Idempotent: zweifaches Ausführen ohne --force überspringt vorhandene Files.

Hinweis: Swissgrid-Files können einige MB pro Jahr sein. Der gesamte
Bestand 2009-2026 ist ca. 100-200 MB. Snapshot-Verzeichnis sollte in
.gitignore stehen (siehe README).
"""

import argparse
import sys
from datetime import date
from pathlib import Path
from typing import Optional

import requests

# Pfad-Setup
PIPELINE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PIPELINE_ROOT.parent))

from pipeline.config.swissgrid_sources import SWISSGRID_FILES
from pipeline.utils.manifest import (
    init_manifest,
    add_file_to_manifest,
    write_manifest,
    load_manifest,
)


SNAPSHOT_ROOT = PIPELINE_ROOT / "raw" / "snapshots"
SOURCE_FAMILY = "swissgrid"
HTTP_TIMEOUT = 120  # Sekunden — Swissgrid-Server kann lahm sein

HTTP_HEADERS = {
    "User-Agent": "energy-viz-pipeline/0.1 (Masterthesis FHGR; serge.pellegatta@stud.fhgr.ch)",
}


def download_file(url: str, target_path: Path) -> None:
    """Lädt eine Datei via HTTP runter, streamt in Chunks."""
    response = requests.get(
        url, timeout=HTTP_TIMEOUT, stream=True, headers=HTTP_HEADERS
    )
    response.raise_for_status()

    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


def extract_year(
    year: int,
    config: dict,
    snapshot_dir: Path,
    manifest: dict,
    force: bool = False,
) -> bool:
    """Extrahiert die Datei für ein einzelnes Jahr."""
    url = config["url"]
    extension = config["extension"]

    target_dir = snapshot_dir / SOURCE_FAMILY
    target_dir.mkdir(parents=True, exist_ok=True)

    target_filename = f"energieuebersicht_ch_{year}{extension}"
    target_path = target_dir / target_filename

    print(f"\n→ Swissgrid {year}")

    # Idempotenz-Check
    if target_path.exists() and not force:
        print(f"  ✓ {target_filename} existiert bereits — übersprungen")

        existing = (
            manifest["sources"]
            .get(SOURCE_FAMILY, {})
            .get(f"energieuebersicht_{year}", {})
            .get("file")
        )
        if not existing:
            add_file_to_manifest(
                manifest,
                SOURCE_FAMILY,
                f"energieuebersicht_{year}",
                "file",
                target_path,
                url,
            )
        return True

    # Download
    try:
        print(f"  ↓ {target_filename}", end=" ", flush=True)
        download_file(url, target_path)
        size_mb = target_path.stat().st_size / (1024 * 1024)
        print(f"({size_mb:.2f} MB)")

        add_file_to_manifest(
            manifest,
            SOURCE_FAMILY,
            f"energieuebersicht_{year}",
            "file",
            target_path,
            url,
        )
        return True
    except Exception as e:
        print(f"\n  ! Fehler beim Download: {e}")
        if target_path.exists():
            target_path.unlink()
        return False


def parse_year_args(
    args_year: Optional[list],
    args_from: Optional[int],
    args_to: Optional[int],
) -> list:
    """
    Bestimmt aus den CLI-Argumenten, welche Jahre zu extrahieren sind.
    """
    available_years = sorted(SWISSGRID_FILES.keys())

    if args_year:
        # Spezifische Jahre angefragt
        for y in args_year:
            if y not in SWISSGRID_FILES:
                print(f"FEHLER: Jahr {y} nicht in Konfiguration. "
                      f"Verfügbar: {available_years[0]}-{available_years[-1]}")
                sys.exit(1)
        return args_year

    # --from / --to als Bereich
    start = args_from if args_from else available_years[0]
    end = args_to if args_to else available_years[-1]

    return [y for y in available_years if start <= y <= end]


def main():
    parser = argparse.ArgumentParser(
        description="Extract Swissgrid Energieübersicht (15-Min-Daten)"
    )
    parser.add_argument(
        "--date", default=None,
        help="Snapshot-Datum YYYY-MM-DD (default: heute)",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Bestehende Files überschreiben",
    )
    parser.add_argument(
        "--year", action="append", type=int, default=None,
        help="Nur ein spezifisches Jahr ziehen (mehrfach möglich)",
    )
    parser.add_argument(
        "--from", dest="from_year", type=int, default=None,
        help="Ab welchem Jahr (default: ältestes verfügbares)",
    )
    parser.add_argument(
        "--to", dest="to_year", type=int, default=None,
        help="Bis welches Jahr (default: neuestes verfügbares)",
    )
    parser.add_argument(
        "--list", action="store_true",
        help="Verfügbare Jahre listen, kein Download",
    )
    args = parser.parse_args()

    # === --list Mode ===
    if args.list:
        print("Verfügbare Swissgrid-Jahres-Files:")
        print()
        for year in sorted(SWISSGRID_FILES.keys()):
            cfg = SWISSGRID_FILES[year]
            print(f"  {year}  {cfg['extension']}  {cfg['url']}")
        return

    # === Setup ===
    snapshot_date = args.date or date.today().isoformat()
    snapshot_dir = SNAPSHOT_ROOT / snapshot_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    years_to_extract = parse_year_args(args.year, args.from_year, args.to_year)

    print(f"Snapshot-Datum: {snapshot_date}")
    print(f"Snapshot-Verzeichnis: {snapshot_dir}")
    print(f"Jahre zu extrahieren: {len(years_to_extract)}")
    print(f"  Bereich: {years_to_extract[0]} – {years_to_extract[-1]}")
    if args.force:
        print("Modus: FORCE (bestehende Files werden überschrieben)")

    # === Manifest laden oder neu anlegen ===
    existing_manifest = load_manifest(snapshot_dir)
    if existing_manifest and not args.force:
        manifest = existing_manifest
        # extracted_by ergänzen falls neu
        if "swissgrid" not in manifest.get("sources", {}):
            print("→ Bestehendes Manifest geladen, wird ergänzt um Swissgrid.")
        else:
            print("→ Bestehendes Manifest geladen, wird aktualisiert.")
    else:
        manifest = init_manifest(snapshot_date, "extract_swissgrid.py")

    # === Extraction ===
    success_count = 0
    fail_count = 0

    for year in years_to_extract:
        ok = extract_year(
            year, SWISSGRID_FILES[year], snapshot_dir, manifest, force=args.force,
        )
        if ok:
            success_count += 1
        else:
            fail_count += 1

    # === Manifest schreiben ===
    manifest_path = write_manifest(manifest, snapshot_dir)

    # === Zusammenfassung ===
    print()
    print("=" * 60)
    print(f"Erfolgreich:  {success_count} / {len(years_to_extract)}")
    if fail_count:
        print(f"Fehlgeschlagen: {fail_count}")
    print(f"Manifest:     {manifest_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
