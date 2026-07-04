"""
Extract-Skript für historische WASTA-Snapshots (Wasserkraft-Anlagen).

Funktionsweise:
1. Liest die URL-Konfiguration aus pipeline/config/wasta_historical_sources.py
2. Lädt pro Jahr ein ZIP-Archiv herunter (2014-2026)
3. Extrahiert NUR die XLSX-Datei aus dem ZIP, ignoriert PDFs/EXE/Dokumentation
4. Speichert sie in pipeline/raw/snapshots/<datum>/wasta_historical/wasta_<jahr>.xlsx
5. Aktualisiert das gemeinsame _manifest.json

Aufruf:
    python pipeline/extract/extract_bfe_wasta_historical.py
        Lädt alle Jahres-Snapshots (2014-2026)

    python pipeline/extract/extract_bfe_wasta_historical.py --year 2024
        Lädt nur ein spezifisches Jahr

    python pipeline/extract/extract_bfe_wasta_historical.py --force
        Überschreibt bestehende Files

Hintergrund: Die BFE-Publikationen sind eigentlich CD-ROM-Distributionen mit
~180 Files (Zentralenblätter als PDF, Dokumentation, Autorun-Programm).
Wir extrahieren nur die XLSX-Datei mit den eigentlichen Daten und werfen
den Rest weg. Pro Jahr ist die XLSX ca. 200-300 KB.

Idempotent: zweifaches Ausführen ohne --force überspringt vorhandene Files.

Hinweis: Die Jahres-Zuordnung basiert auf der Annahme "neueste Publikations-ID
= neuestes Jahr". Falls beim ersten Profilieren auffällt, dass ein Jahr
falsch zugeordnet ist, in wasta_historical_sources.py korrigieren.
"""

import argparse
import sys
import zipfile
from datetime import date
from pathlib import Path
from typing import Optional

import requests

# Pfad-Setup
PIPELINE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PIPELINE_ROOT.parent))

from pipeline.config.wasta_historical_sources import WASTA_HISTORICAL_FILES
from pipeline.utils.manifest import (
    init_manifest,
    add_file_to_manifest,
    write_manifest,
    load_manifest,
)


SNAPSHOT_ROOT = PIPELINE_ROOT / "raw" / "snapshots"
SOURCE_FAMILY = "wasta_historical"
HTTP_TIMEOUT = 120

HTTP_HEADERS = {
    "User-Agent": "energy-viz-pipeline/0.1 (Masterthesis FHGR; serge.pellegrini@stud.fhgr.ch)",
}


def download_file(url: str, target_path: Path) -> None:
    """Lädt eine Datei via HTTP runter, streamt in Chunks."""
    response = requests.get(
        url, timeout=HTTP_TIMEOUT, stream=True, headers=HTTP_HEADERS,
        allow_redirects=True,  # BFE-Publication-DB nutzt Redirects
    )
    response.raise_for_status()

    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


def is_zip_file(filepath: Path) -> bool:
    """Prüft via Magic-Number, ob die Datei ein ZIP-Archiv ist."""
    try:
        with open(filepath, "rb") as f:
            magic = f.read(4)
        return magic[:2] == b"PK"
    except Exception:
        return False


def extract_xlsx_from_zip(zip_path: Path, target_xlsx: Path) -> Optional[str]:
    """
    Extrahiert die einzige relevante XLSX-Datei aus dem ZIP.
    Ignoriert PDFs, EXE, Lock-Files und andere CD-ROM-Artefakte.

    Returns: Original-Filename in der ZIP, oder None bei Fehler.
    """
    target_xlsx.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zf:
        members = zf.namelist()

        # Nur XLSX-Files, ohne Excel-Lock-Files (~$)
        xlsx_candidates = [
            m for m in members
            if m.lower().endswith(".xlsx")
            and not Path(m).name.startswith("~$")
        ]

        if not xlsx_candidates:
            return None

        if len(xlsx_candidates) > 1:
            # Falls mehrere XLSX vorhanden sind: nimm die grösste
            # (ist dann die Datentabelle, nicht ein Index)
            xlsx_candidates.sort(
                key=lambda m: zf.getinfo(m).file_size,
                reverse=True,
            )

        chosen = xlsx_candidates[0]
        with zf.open(chosen) as src, open(target_xlsx, "wb") as dst:
            dst.write(src.read())

        return chosen


def extract_year(
    year: int,
    config: dict,
    snapshot_dir: Path,
    manifest: dict,
    force: bool = False,
) -> bool:
    """Extrahiert die Daten-XLSX für ein einzelnes Jahr."""
    url = config["url"]

    target_dir = snapshot_dir / SOURCE_FAMILY
    target_dir.mkdir(parents=True, exist_ok=True)

    target_xlsx = target_dir / f"wasta_{year}.xlsx"
    tmp_zip = target_dir / f"wasta_{year}.zip_tmp"

    print(f"\n→ WASTA {year}")

    # Idempotenz-Check
    if target_xlsx.exists() and not force:
        print(f"  ✓ wasta_{year}.xlsx existiert bereits — übersprungen")

        existing = (
            manifest["sources"]
            .get(SOURCE_FAMILY, {})
            .get(f"wasta_{year}", {})
        )
        if not existing:
            add_file_to_manifest(
                manifest,
                SOURCE_FAMILY,
                f"wasta_{year}",
                "xlsx",
                target_xlsx,
                url,
            )
        return True

    # Download
    try:
        print(f"  ↓ ZIP herunterladen", end=" ", flush=True)
        download_file(url, tmp_zip)
        size_mb = tmp_zip.stat().st_size / (1024 * 1024)
        print(f"({size_mb:.1f} MB)")

        # Prüfen, ob es wirklich ein ZIP ist
        if not is_zip_file(tmp_zip):
            print(f"  ! Datei ist kein ZIP-Archiv — übersprungen")
            tmp_zip.unlink()
            return False

        # XLSX extrahieren, Rest wegwerfen
        print(f"  ↓ XLSX extrahieren", end=" ", flush=True)
        original_name = extract_xlsx_from_zip(tmp_zip, target_xlsx)

        if original_name is None:
            print("\n  ! Keine XLSX im ZIP gefunden")
            tmp_zip.unlink()
            return False

        xlsx_size_kb = target_xlsx.stat().st_size / 1024
        print(f"({xlsx_size_kb:.1f} KB)")
        print(f"    Original: {Path(original_name).name}")

        # ZIP wegwerfen
        tmp_zip.unlink()

        # Manifest-Eintrag
        add_file_to_manifest(
            manifest,
            SOURCE_FAMILY,
            f"wasta_{year}",
            "xlsx",
            target_xlsx,
            url,
        )
        return True
    except Exception as e:
        print(f"\n  ! Fehler beim Download/Extrahieren: {e}")
        if tmp_zip.exists():
            tmp_zip.unlink()
        if target_xlsx.exists():
            target_xlsx.unlink()
        return False


def parse_year_args(
    args_year: Optional[list],
    args_from: Optional[int],
    args_to: Optional[int],
) -> list:
    """Bestimmt aus den CLI-Argumenten, welche Jahre zu extrahieren sind."""
    available_years = sorted(WASTA_HISTORICAL_FILES.keys())

    if args_year:
        for y in args_year:
            if y not in WASTA_HISTORICAL_FILES:
                print(f"FEHLER: Jahr {y} nicht in Konfiguration. "
                      f"Verfügbar: {available_years[0]}-{available_years[-1]}")
                sys.exit(1)
        return args_year

    start = args_from if args_from else available_years[0]
    end = args_to if args_to else available_years[-1]

    return [y for y in available_years if start <= y <= end]


def main():
    parser = argparse.ArgumentParser(
        description="Extract historische WASTA-Snapshots (2014-2026), nur XLSX-Daten"
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
        print("Verfügbare WASTA-Jahres-Snapshots:")
        print()
        for year in sorted(WASTA_HISTORICAL_FILES.keys(), reverse=True):
            cfg = WASTA_HISTORICAL_FILES[year]
            print(f"  {year}  {cfg['url']}")
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
        if SOURCE_FAMILY not in manifest.get("sources", {}):
            print(f"→ Bestehendes Manifest geladen, wird ergänzt um {SOURCE_FAMILY}.")
        else:
            print("→ Bestehendes Manifest geladen, wird aktualisiert.")
    else:
        manifest = init_manifest(snapshot_date, "extract_bfe_wasta_historical.py")

    # === Extraction ===
    success_count = 0
    fail_count = 0

    for year in years_to_extract:
        ok = extract_year(
            year, WASTA_HISTORICAL_FILES[year],
            snapshot_dir, manifest, force=args.force,
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