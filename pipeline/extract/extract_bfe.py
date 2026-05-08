"""
Extract-Skript für BFE-Quellen via opendata.swiss CKAN-API.

Funktionsweise:
1. Liest die Quellen-Konfiguration aus pipeline/config/sources.py
2. Pro Quelle: ruft die CKAN-API auf, um aktuelle Resource-URLs zu bekommen
3. Lädt die gewünschten Formate (CSV, GeoPackage, ...) herunter
4. Speichert sie in pipeline/raw/snapshots/<datum>/bfe/
5. Schreibt _manifest.json mit Provenance-Informationen (SHA-256 etc.)

Aufruf:
    python pipeline/extract/extract_bfe.py
        Zieht alle Priorität-A-Quellen, Snapshot-Datum = heute

    python pipeline/extract/extract_bfe.py --date 2026-05-03
        Zieht in spezifisches Snapshot-Datum (für Tests / Reproduzierbarkeit)

    python pipeline/extract/extract_bfe.py --force
        Überschreibt bestehenden Snapshot

    python pipeline/extract/extract_bfe.py --dataset pv_grossanlagen
        Zieht nur eine spezifische Quelle (auch mehrfach möglich)

    python pipeline/extract/extract_bfe.py --list
        Zeigt verfügbare Quellen ohne Download

Idempotent: Zweifaches Ausführen ohne --force überspringt vorhandene Files.
"""

import argparse
import sys
from datetime import date
from pathlib import Path
from typing import Optional

import requests

# Pfad-Setup, damit die Imports funktionieren, egal von wo aufgerufen
PIPELINE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PIPELINE_ROOT.parent))

from pipeline.config.sources import SOURCES, get_priority_a_sources
from pipeline.utils.manifest import (
    init_manifest,
    add_file_to_manifest,
    write_manifest,
    load_manifest,
)


# === Konstanten ===

CKAN_API_BASE = "https://opendata.swiss/api/3/action"
SNAPSHOT_ROOT = PIPELINE_ROOT / "raw" / "snapshots"
SOURCE_FAMILY = "bfe"
HTTP_TIMEOUT = 60  # Sekunden

# Höflicher User-Agent — manche Server lehnen leere/Standard-UAs ab
HTTP_HEADERS = {
    "User-Agent": "energy-viz-pipeline/0.1 (Masterthesis FHGR; serge.pellegrini@stud.fhgr.ch)",
    "Accept": "application/json, */*",
}

# Mapping von CKAN-Format-Strings auf interne format_keys + Dateierweiterungen
# CKAN ist nicht 100% konsistent (mal "CSV", mal "csv", mal "text/csv")
FORMAT_MAPPING = {
    "CSV": ("csv", ".csv"),
    "TEXT/CSV": ("csv", ".csv"),
    "XLSX": ("xlsx", ".xlsx"),
    "GEOPACKAGE": ("gpkg", ".gpkg"),
    "GPKG": ("gpkg", ".gpkg"),
    "GEOJSON": ("geojson", ".geojson"),
    "JSON": ("json", ".json"),
    "XML": ("xml", ".xml"),
    "ZIP": ("zip", ".zip"),
}


# === CKAN-API-Funktionen ===

def fetch_dataset_metadata(slug: str) -> dict:
    """
    Holt die vollständigen Metadaten eines Datensatzes via CKAN-API.
    Returns das 'result'-Dict aus der API-Antwort.
    """
    url = f"{CKAN_API_BASE}/package_show?id={slug}"
    response = requests.get(url, timeout=HTTP_TIMEOUT, headers=HTTP_HEADERS)
    response.raise_for_status()

    data = response.json()
    if not data.get("success"):
        raise RuntimeError(f"CKAN-API gab Fehler zurück für Slug '{slug}': {data}")

    return data["result"]


def select_resources(
    metadata: dict, preferred_formats: list
) -> list:
    """
    Wählt aus den verfügbaren Resources jene aus, die einem der gewünschten
    Formate entsprechen. Pro Format wird die jeweils erste passende Resource genommen.

    Args:
        metadata: Ergebnis von fetch_dataset_metadata()
        preferred_formats: z.B. ["CSV", "GeoPackage"]

    Returns:
        Liste von Tuples (format_key, file_extension, url, resource_id)
    """
    resources = metadata.get("resources", [])
    selected = []
    seen_format_keys = set()

    # Normalisierte Wunschliste
    preferred_normalized = [f.upper() for f in preferred_formats]

    for resource in resources:
        ckan_format = (resource.get("format") or "").strip().upper()
        if not ckan_format or ckan_format not in FORMAT_MAPPING:
            continue

        format_key, file_ext = FORMAT_MAPPING[ckan_format]

        # Schon ein File für dieses Format ausgewählt? → skip
        if format_key in seen_format_keys:
            continue

        # Gehört das Format zu den Wunschformaten?
        if not any(
            FORMAT_MAPPING.get(p, (None, None))[0] == format_key
            for p in preferred_normalized
        ):
            continue

        url = resource.get("download_url") or resource.get("url")
        if not url:
            continue

        selected.append(
            (format_key, file_ext, url, resource.get("id"))
        )
        seen_format_keys.add(format_key)

    return selected


# === Download-Funktionen ===

def download_file(url: str, target_path: Path) -> None:
    """
    Lädt eine Datei via HTTP runter und schreibt sie auf Disk.
    Streamt in Chunks, damit auch grosse Dateien funktionieren.
    """
    response = requests.get(url, timeout=HTTP_TIMEOUT, stream=True, headers=HTTP_HEADERS)
    response.raise_for_status()

    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


# === Hauptlogik ===

def extract_source(
    source_id: str,
    source_config: dict,
    snapshot_dir: Path,
    manifest: dict,
    force: bool = False,
) -> bool:
    """
    Extrahiert eine einzelne Quelle.
    Returns True bei Erfolg, False wenn übersprungen.
    """
    slug = source_config["slug"]
    preferred_formats = source_config["preferred_formats"]

    target_dir = snapshot_dir / SOURCE_FAMILY
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n→ {source_id} (slug: {slug})")

    # CKAN-API abfragen
    try:
        metadata = fetch_dataset_metadata(slug)
    except Exception as e:
        print(f"  ! Fehler beim API-Call: {e}")
        return False

    # Verfügbare Resources auswählen
    selected = select_resources(metadata, preferred_formats)
    if not selected:
        print(f"  ! Keine Resources im gewünschten Format gefunden.")
        print(f"    Gewünscht: {preferred_formats}")
        available = [r.get("format") for r in metadata.get("resources", [])]
        print(f"    Verfügbar: {available}")
        return False

    success_count = 0

    for format_key, file_ext, url, resource_id in selected:
        target_filename = f"{source_id}{file_ext}"
        target_path = target_dir / target_filename

        # Idempotenz-Check
        if target_path.exists() and not force:
            print(f"  ✓ {target_filename} existiert bereits — übersprungen "
                  f"(--force zum Überschreiben)")
            # Trotzdem ins Manifest, falls noch nicht drin
            existing = manifest["sources"].get(SOURCE_FAMILY, {}).get(
                source_id, {}
            ).get(format_key)
            if not existing:
                add_file_to_manifest(
                    manifest, SOURCE_FAMILY, source_id, format_key,
                    target_path, url, resource_id,
                )
            success_count += 1
            continue

        # Download
        try:
            print(f"  ↓ {format_key} → {target_filename}", end=" ", flush=True)
            download_file(url, target_path)
            size_kb = target_path.stat().st_size / 1024
            print(f"({size_kb:.1f} KB)")

            add_file_to_manifest(
                manifest, SOURCE_FAMILY, source_id, format_key,
                target_path, url, resource_id,
            )
            success_count += 1
        except Exception as e:
            print(f"\n  ! Fehler beim Download: {e}")
            if target_path.exists():
                target_path.unlink()  # unvollständiges File löschen

    return success_count > 0


def main():
    parser = argparse.ArgumentParser(
        description="Extract-Skript für BFE-Quellen via opendata.swiss"
    )
    parser.add_argument(
        "--date",
        default=None,
        help="Snapshot-Datum YYYY-MM-DD (default: heute)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Bestehende Files überschreiben",
    )
    parser.add_argument(
        "--dataset",
        action="append",
        default=None,
        help="Nur eine spezifische Quelle ziehen (mehrfach möglich)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Verfügbare Quellen listen, kein Download",
    )
    args = parser.parse_args()

    # === --list Mode ===
    if args.list:
        print("Verfügbare Quellen in pipeline/config/sources.py:")
        print()
        for source_id, config in SOURCES.items():
            print(f"  {source_id}")
            print(f"    Priorität: {config['priority']}  |  "
                  f"RQ-Bezug: {config['rq_bezug']}")
            print(f"    Formate: {', '.join(config['preferred_formats'])}")
            print(f"    Slug: {config['slug']}")
            print(f"    Notiz: {config['notes']}")
            print()
        return

    # === Setup ===
    snapshot_date = args.date or date.today().isoformat()
    snapshot_dir = SNAPSHOT_ROOT / snapshot_date

    # Quellen-Auswahl
    if args.dataset:
        sources_to_extract = {}
        for ds in args.dataset:
            if ds not in SOURCES:
                print(f"FEHLER: Quelle '{ds}' nicht in Konfiguration.")
                print(f"Verfügbar: {list(SOURCES.keys())}")
                sys.exit(1)
            sources_to_extract[ds] = SOURCES[ds]
    else:
        sources_to_extract = get_priority_a_sources()

    print(f"Snapshot-Datum: {snapshot_date}")
    print(f"Snapshot-Verzeichnis: {snapshot_dir}")
    print(f"Quellen zu extrahieren: {len(sources_to_extract)}")
    if args.force:
        print("Modus: FORCE (bestehende Files werden überschrieben)")

    # === Manifest laden oder neu anlegen ===
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    existing_manifest = load_manifest(snapshot_dir)
    if existing_manifest and not args.force:
        manifest = existing_manifest
        print("→ Bestehendes Manifest geladen, wird ergänzt.")
    else:
        manifest = init_manifest(snapshot_date, "extract_bfe.py")

    # === Extraction ===
    success_count = 0
    fail_count = 0

    for source_id, source_config in sources_to_extract.items():
        ok = extract_source(
            source_id, source_config, snapshot_dir, manifest, force=args.force,
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
    print(f"Erfolgreich:  {success_count} / {len(sources_to_extract)}")
    if fail_count:
        print(f"Fehlgeschlagen: {fail_count}")
    print(f"Manifest:     {manifest_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
