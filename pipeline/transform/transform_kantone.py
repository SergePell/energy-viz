"""
Transform-Skript für Kantons-Stammdaten und -Geometrie.

Funktionsweise:
1. Liest swisstopo-GeoJSON aus pipeline/raw/snapshots/<datum>/swisstopo/
2. Mappt BFS-Kantonsnummern auf ISO 3166-2 Codes (CH-ZH, CH-AG, etc.)
3. Aggregiert Mehrteil-Kantone (Exklaven) zu einem Eintrag
4. Erstellt zwei Output-Files:
   - dim/kanton.json: Lookup-Tabelle (26 Einträge, ~5 KB)
   - dim/kanton_geometry.geojson: vereinfachte GeoJSON für Frontend-Karten

Aufruf:
    python pipeline/transform/transform_kantone.py
        Nimmt automatisch den neuesten Snapshot

    python pipeline/transform/transform_kantone.py --snapshot 2026-05-10
        Nimmt einen spezifischen Snapshot

    python pipeline/transform/transform_kantone.py --force
        Überschreibt bestehende Outputs

Output-Schema dim/kanton.json:
    [
      {
        "kanton_code": "CH-GR",            # ISO 3166-2
        "kanton_bfs_nr": 18,               # offizielle BFS-Nummer
        "kanton_name_de": "Graubünden",
        "flaeche_ha": 710530,
        "see_flaeche_ha": null,
        "einwohner": 198379
      }, ...
    ]

Output-Schema dim/kanton_geometry.geojson:
    Standard FeatureCollection mit Properties:
    kanton_code, kanton_bfs_nr, kanton_name_de
"""

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Optional

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
SOURCE_FAMILY = "kanton"


# Mapping BFS-Nummer → ISO 3166-2 Code
# Quelle: https://www.bfs.admin.ch/bfs/de/home/grundlagen/nomenklaturen.html
BFS_TO_ISO = {
    1:  "CH-ZH", 2:  "CH-BE", 3:  "CH-LU", 4:  "CH-UR", 5:  "CH-SZ",
    6:  "CH-OW", 7:  "CH-NW", 8:  "CH-GL", 9:  "CH-ZG", 10: "CH-FR",
    11: "CH-SO", 12: "CH-BS", 13: "CH-BL", 14: "CH-SH", 15: "CH-AR",
    16: "CH-AI", 17: "CH-SG", 18: "CH-GR", 19: "CH-AG", 20: "CH-TG",
    21: "CH-TI", 22: "CH-VD", 23: "CH-VS", 24: "CH-NE", 25: "CH-GE",
    26: "CH-JU",
}


def find_latest_snapshot() -> Optional[str]:
    """Findet das neueste Snapshot-Datum mit swisstopo-Daten."""
    if not SNAPSHOT_ROOT.exists():
        return None

    candidates = []
    for entry in SNAPSHOT_ROOT.iterdir():
        if entry.is_dir() and (entry / "swisstopo").exists():
            candidates.append(entry.name)

    if not candidates:
        return None

    return sorted(candidates)[-1]


def load_geojson(path: Path) -> dict:
    """Liest die swisstopo-GeoJSON ein."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_kanton_attribute(features: list) -> dict:
    """
    Extrahiert pro Kanton (BFS-Nr) die Stammdaten.
    Mehrere Features pro Kanton (z.B. Exklaven) werden zusammengefasst.
    Returns: dict[bfs_nr → dict mit Stammdaten]
    """
    kantone = {}

    for feat in features:
        props = feat.get("properties", {})
        objektart = props.get("OBJEKTART")

        # Sicherheits-Check: nur Kanton-Features
        if objektart != "Kanton":
            continue

        bfs_nr = props.get("KANTONSNUM")
        if bfs_nr is None:
            continue

        if bfs_nr not in kantone:
            kantone[bfs_nr] = {
                "kanton_bfs_nr": bfs_nr,
                "kanton_name_de": props.get("NAME"),
                "flaeche_ha": props.get("KANTONSFLA"),
                "see_flaeche_ha": props.get("SEE_FLAECH"),
                "einwohner": props.get("EINWOHNERZ"),
            }
        else:
            # Bei Mehrteil-Kantonen: Flächen addieren
            existing = kantone[bfs_nr]
            for fld in ("flaeche_ha", "see_flaeche_ha", "einwohner"):
                new_val = props.get(fld)
                if new_val is None:
                    continue
                if existing.get(fld) is None:
                    existing[fld] = new_val
                else:
                    existing[fld] += new_val

    return kantone


def build_dim_kanton(kantone_attrs: dict) -> list:
    """
    Baut die dim_kanton-Liste in einheitlichem Format.
    Sortiert nach BFS-Nummer für Konsistenz.
    """
    result = []
    for bfs_nr in sorted(kantone_attrs.keys()):
        attrs = kantone_attrs[bfs_nr]
        if bfs_nr not in BFS_TO_ISO:
            print(f"  ! WARNUNG: BFS-Nummer {bfs_nr} nicht im ISO-Mapping. Übersprungen.")
            continue

        result.append({
            "kanton_code": BFS_TO_ISO[bfs_nr],
            "kanton_bfs_nr": bfs_nr,
            "kanton_name_de": attrs["kanton_name_de"],
            "flaeche_ha": attrs["flaeche_ha"],
            "see_flaeche_ha": attrs["see_flaeche_ha"],
            "einwohner": attrs["einwohner"],
        })

    return result


def build_geometry_geojson(features: list) -> dict:
    """
    Baut eine vereinfachte GeoJSON-FeatureCollection für das Frontend.
    Behält die Original-Geometrien, ersetzt aber die Properties durch
    nur die für uns relevanten Felder.
    """
    new_features = []
    for feat in features:
        props = feat.get("properties", {})

        if props.get("OBJEKTART") != "Kanton":
            continue

        bfs_nr = props.get("KANTONSNUM")
        if bfs_nr not in BFS_TO_ISO:
            continue

        new_features.append({
            "type": "Feature",
            "properties": {
                "kanton_code": BFS_TO_ISO[bfs_nr],
                "kanton_bfs_nr": bfs_nr,
                "kanton_name_de": props.get("NAME"),
            },
            "geometry": feat.get("geometry"),
        })

    return {
        "type": "FeatureCollection",
        "features": new_features,
    }


def write_outputs(
    dim_kanton: list,
    geometry_geojson: dict,
    intermediate_dir: Path,
) -> tuple:
    """Schreibt die zwei Output-Files."""
    dim_dir = intermediate_dir / "dim"
    dim_dir.mkdir(parents=True, exist_ok=True)

    # dim/kanton.json
    dim_path = dim_dir / "kanton.json"
    with open(dim_path, "w", encoding="utf-8") as f:
        json.dump(dim_kanton, f, ensure_ascii=False, indent=2)

    # dim/kanton_geometry.geojson
    geom_path = dim_dir / "kanton_geometry.geojson"
    with open(geom_path, "w", encoding="utf-8") as f:
        json.dump(geometry_geojson, f, ensure_ascii=False)

    return dim_path, geom_path


def main():
    parser = argparse.ArgumentParser(
        description="Transform swisstopo Kantons-GeoJSON in dim_kanton + Geometry-File"
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

    # === Snapshot-Datum bestimmen ===
    if args.snapshot:
        snapshot_date = args.snapshot
    else:
        snapshot_date = find_latest_snapshot()
        if not snapshot_date:
            print("FEHLER: Kein Snapshot mit swisstopo-Daten gefunden.")
            sys.exit(1)

    snapshot_dir = SNAPSHOT_ROOT / snapshot_date
    swisstopo_dir = snapshot_dir / "swisstopo"

    if not swisstopo_dir.exists():
        print(f"FEHLER: {swisstopo_dir} existiert nicht.")
        sys.exit(1)

    # Kantons-GeoJSON finden
    geojson_files = list(swisstopo_dir.glob("*.geojson"))
    if not geojson_files:
        print(f"FEHLER: Keine .geojson-Datei in {swisstopo_dir}.")
        sys.exit(1)

    if len(geojson_files) > 1:
        # Heuristik: Datei mit "kanton" im Namen bevorzugen
        kanton_files = [f for f in geojson_files if "kanton" in f.name.lower()]
        if kanton_files:
            input_file = kanton_files[0]
        else:
            input_file = geojson_files[0]
    else:
        input_file = geojson_files[0]

    # === Output-Datum bestimmen ===
    intermediate_date = args.intermediate_date or date.today().isoformat()
    intermediate_dir = INTERMEDIATE_ROOT / intermediate_date
    intermediate_dir.mkdir(parents=True, exist_ok=True)

    # Output-Pfade
    dim_path = intermediate_dir / "dim" / "kanton.json"
    geom_path = intermediate_dir / "dim" / "kanton_geometry.geojson"

    print(f"Snapshot-Datum:       {snapshot_date}")
    print(f"Snapshot-Verzeichnis: {snapshot_dir}")
    print(f"Input-File:           {input_file.name}")
    print(f"Output-Datum:         {intermediate_date}")
    print(f"Output-Verzeichnis:   {intermediate_dir}")

    # Idempotenz-Check
    if dim_path.exists() and geom_path.exists() and not args.force:
        print()
        print("✓ Beide Output-Files existieren bereits — übersprungen.")
        print(f"  Mit --force überschreiben.")
        return

    # === Verarbeitung ===
    print()
    print("→ GeoJSON einlesen", end=" ", flush=True)
    geojson = load_geojson(input_file)
    n_features = len(geojson.get("features", []))
    print(f"({n_features} Features)")

    print(f"→ Kantons-Attribute extrahieren", end=" ", flush=True)
    kantone_attrs = extract_kanton_attribute(geojson["features"])
    print(f"({len(kantone_attrs)} unique Kantone)")

    if len(kantone_attrs) != 26:
        print(f"  ! WARNUNG: Erwartete 26 Kantone, gefunden {len(kantone_attrs)}.")

    print(f"→ dim_kanton aufbauen", end=" ", flush=True)
    dim_kanton = build_dim_kanton(kantone_attrs)
    print(f"({len(dim_kanton)} Einträge)")

    print(f"→ Geometry-GeoJSON aufbauen", end=" ", flush=True)
    geometry_geojson = build_geometry_geojson(geojson["features"])
    print(f"({len(geometry_geojson['features'])} Features)")

    print(f"→ Output schreiben")
    dim_path, geom_path = write_outputs(
        dim_kanton, geometry_geojson, intermediate_dir,
    )
    dim_size_kb = dim_path.stat().st_size / 1024
    geom_size_mb = geom_path.stat().st_size / (1024 * 1024)
    print(f"  ✓ {dim_path.name}            ({dim_size_kb:.1f} KB)")
    print(f"  ✓ {geom_path.name} ({geom_size_mb:.1f} MB)")

    # === Manifest-Update ===
    existing_manifest = load_manifest(intermediate_dir)
    if existing_manifest:
        manifest = existing_manifest
    else:
        manifest = init_manifest(intermediate_date, "transform_kantone.py")

    add_file_to_manifest(
        manifest, "dim", "kanton", "json", dim_path,
        f"transform_kantone.py from {input_file.relative_to(PIPELINE_ROOT.parent)}",
    )
    add_file_to_manifest(
        manifest, "dim", "kanton_geometry", "geojson", geom_path,
        f"transform_kantone.py from {input_file.relative_to(PIPELINE_ROOT.parent)}",
    )
    manifest_path = write_manifest(manifest, intermediate_dir)

    print()
    print("=" * 60)
    print(f"Erfolgreich abgeschlossen.")
    print(f"Manifest: {manifest_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()