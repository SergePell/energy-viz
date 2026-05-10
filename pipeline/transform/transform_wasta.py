"""
Transform-Skript für WASTA Wasserkraftwerke.

Funktionsweise:
1. Liest WASTA-CSVs aus pipeline/raw/snapshots/<datum>/bfe/wasta_wasserkraft/
   - HydropowerPlant.csv (723 Stammdaten)
   - TechnicalSpecification.csv (723 technische Daten)
   - HydropowerPlantTypeCatalogue.csv (4 Typ-Codes)
   - HydropowerPlantOperationalStatusCatalogue.csv (5 Status-Codes)
2. Joint Stammdaten + TechnicalSpec über WASTANumber/hydropowerPlantR
3. Löst TypeCode (t1-t4) und OperationalStatusCode (os1-os5) via Catalogues auf
4. Reprojiziert Koordinaten LV95 (EPSG:2056) → WGS84 (EPSG:4326)
5. Mappt Kanton-Kürzel (GR) auf ISO 3166-2 (CH-GR)
6. Schreibt zwei Output-Files:
   - dim/wasserkraftwerk.json: alle Stammdaten (~250-300 KB)
   - dim/wasserkraftwerk_geometry.geojson: Punkte für Karten-Visualisierung

Aufruf:
    python pipeline/transform/transform_wasta.py
        Nimmt automatisch den neuesten Snapshot

    python pipeline/transform/transform_wasta.py --snapshot 2026-05-05
        Nimmt einen spezifischen Snapshot

    python pipeline/transform/transform_wasta.py --force
        Überschreibt bestehende Outputs

Output-Schema dim/wasserkraftwerk.json:
    [
      {
        "wasta_nummer": 100100,
        "name": "Val Giuv",
        "standort": "Rueras",
        "kanton_code": "CH-GR",                     # ISO 3166-2, oder null
        "typ_code": "t1",                           # Original-Code
        "typ_label_de": "Laufkraftwerk",            # Klartext deutsch
        "status_code": "os1",                       # Original-Code
        "status_label_de": "im Normalbetrieb",      # Klartext deutsch
        "inbetriebnahme_jahr": 1968,
        "fallhoehe_m": 247.0,
        "leistung_turbine_max_mw": 8.5,             # aus TechnicalSpec
        "leistung_generator_max_mw": 8.0,           # aus TechnicalSpec
        "produktion_erwartet_gwh": 35.2,            # aus TechnicalSpec
        "leistung_pumpe_max_mw": 0.0,               # aus TechnicalSpec
        "leistung_motor_mw": 0.0,                   # aus TechnicalSpec
        "stichtag_spec": "2024-12-31",              # aus TechnicalSpec
        "longitude": 8.7234,                        # WGS84
        "latitude": 46.6712                         # WGS84
      }, ...
    ]

Output-Schema dim/wasserkraftwerk_geometry.geojson:
    Standard FeatureCollection (Point-Geometrien) mit Properties:
    wasta_nummer, name, kanton_code, typ_code, status_code

Hinweis: 16 von 723 Anlagen haben keinen Kanton-Eintrag. Das sind typischerweise
internationale Grenzkraftwerke (Rheinau, Reckingen) oder stillgelegte Anlagen
mit unklarer historischer Zuordnung. Diese behalten kanton_code = null.
"""

import argparse
import json
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


# Mapping CH-Kanton-Kürzel → ISO 3166-2 Code
# Manche Quellen nutzen "GR", "ZH", "VS", manche "Graubünden" — hier mappen wir
# das BFE-WASTA-Format (zwei-Buchstaben-Kürzel) auf ISO 3166-2.
KANTON_KURZEL_TO_ISO = {
    "ZH": "CH-ZH", "BE": "CH-BE", "LU": "CH-LU", "UR": "CH-UR", "SZ": "CH-SZ",
    "OW": "CH-OW", "NW": "CH-NW", "GL": "CH-GL", "ZG": "CH-ZG", "FR": "CH-FR",
    "SO": "CH-SO", "BS": "CH-BS", "BL": "CH-BL", "SH": "CH-SH", "AR": "CH-AR",
    "AI": "CH-AI", "SG": "CH-SG", "GR": "CH-GR", "AG": "CH-AG", "TG": "CH-TG",
    "TI": "CH-TI", "VD": "CH-VD", "VS": "CH-VS", "NE": "CH-NE", "GE": "CH-GE",
    "JU": "CH-JU",
}


def find_latest_snapshot() -> Optional[str]:
    """Findet das neueste Snapshot-Datum mit WASTA-Daten."""
    if not SNAPSHOT_ROOT.exists():
        return None

    candidates = []
    for entry in SNAPSHOT_ROOT.iterdir():
        if not entry.is_dir():
            continue
        wasta_dir = entry / "bfe" / "wasta_wasserkraft"
        if not wasta_dir.exists():
            continue
        if (wasta_dir / "HydropowerPlant.csv").exists():
            candidates.append(entry.name)

    if not candidates:
        return None

    return sorted(candidates)[-1]


def load_catalogue(path: Path, code_column: str = "ID",
                   label_column: str = "DE") -> dict:
    """
    Liest ein BFE-Catalogue-CSV und gibt ein Dict {code: label_de} zurück.
    """
    df = pd.read_csv(path)
    return dict(zip(df[code_column], df[label_column]))


def reproject_lv95_to_wgs84(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reprojiziert LV95 (EPSG:2056) → WGS84 (EPSG:4326).
    Erweitert den DataFrame um longitude und latitude.

    LV95 nutzt _x = Ostkoordinate, _y = Nordkoordinate (in Metern).
    WGS84 nutzt longitude (Längengrad) und latitude (Breitengrad) in Grad.
    """
    try:
        from pyproj import Transformer
    except ImportError:
        print("FEHLER: pyproj nicht installiert. Bitte installieren mit:")
        print("  pip install pyproj")
        sys.exit(1)

    # always_xy=True garantiert: Input ist (lon/east, lat/north),
    # Output ist (longitude, latitude) — vermeidet Achsen-Verwechslung.
    transformer = Transformer.from_crs("EPSG:2056", "EPSG:4326", always_xy=True)

    # Vektorisierte Umrechnung (schnell)
    lon, lat = transformer.transform(df["_x"].values, df["_y"].values)

    df = df.copy()
    df["longitude"] = lon
    df["latitude"] = lat
    return df


def transform_wasta(
    plants_df: pd.DataFrame,
    specs_df: pd.DataFrame,
    type_lookup: dict,
    status_lookup: dict,
) -> pd.DataFrame:
    """
    Joint Stammdaten + TechnicalSpec, löst Catalogues auf, reprojiziert.
    Returns: ein DataFrame mit allen sauberen Spalten in Pipeline-Konvention.
    """
    # Reprojektion zuerst auf den plants_df
    plants_df = reproject_lv95_to_wgs84(plants_df)

    # Join über WASTANumber = hydropowerPlantR
    merged = plants_df.merge(
        specs_df,
        left_on="WASTANumber",
        right_on="hydropowerPlantR",
        how="left",
        suffixes=("", "_spec"),
    )

    # Anzahl prüfen — wir erwarten 1:1
    if len(merged) != len(plants_df):
        print(f"  ! WARNUNG: Join hat {len(merged)} Zeilen, erwartet {len(plants_df)}.")
        print(f"    Vermutlich Mehrfach-Treffer in TechnicalSpecification.")

    # Catalogue-Auflösung
    merged["typ_label_de"] = merged["TypeCode"].map(type_lookup)
    merged["status_label_de"] = merged["OperationalStatusCode"].map(status_lookup)

    # Kanton-Mapping zu ISO 3166-2
    # Manche Anlagen haben keinen Canton (NaN) — bleibt NaN
    merged["kanton_code"] = merged["Canton"].map(KANTON_KURZEL_TO_ISO)

    # Validierung: Codes ohne Mapping?
    unmapped_types = merged[merged["typ_label_de"].isna() & merged["TypeCode"].notna()]
    if len(unmapped_types) > 0:
        print(f"  ! WARNUNG: {len(unmapped_types)} Anlagen mit nicht-gemapptem TypeCode.")
        print(f"    Codes: {unmapped_types['TypeCode'].unique()}")

    unmapped_status = merged[merged["status_label_de"].isna() & merged["OperationalStatusCode"].notna()]
    if len(unmapped_status) > 0:
        print(f"  ! WARNUNG: {len(unmapped_status)} Anlagen mit nicht-gemapptem StatusCode.")
        print(f"    Codes: {unmapped_status['OperationalStatusCode'].unique()}")

    unmapped_kantone = merged[merged["kanton_code"].isna() & merged["Canton"].notna()]
    if len(unmapped_kantone) > 0:
        print(f"  ! WARNUNG: {len(unmapped_kantone)} Anlagen mit nicht-gemapptem Kanton-Kürzel.")
        print(f"    Kürzel: {unmapped_kantone['Canton'].unique()}")

    # Spalten-Renaming und -Auswahl in Pipeline-Konvention
    result = pd.DataFrame()
    result["wasta_nummer"] = merged["WASTANumber"].astype(int)
    result["name"] = merged["Name"]
    result["standort"] = merged["Location"]
    result["kanton_code"] = merged["kanton_code"]
    result["typ_code"] = merged["TypeCode"]
    result["typ_label_de"] = merged["typ_label_de"]
    result["status_code"] = merged["OperationalStatusCode"]
    result["status_label_de"] = merged["status_label_de"]
    result["inbetriebnahme_jahr"] = merged["BeginningOfOperation"].astype(int)
    result["fallhoehe_m"] = merged["FallHeight"]

    # TechnicalSpec-Spalten (können null sein, falls eine Anlage keine Spec hat)
    result["leistung_turbine_max_mw"] = merged["PerformanceTurbineMaximum"]
    result["leistung_generator_max_mw"] = merged["PerformanceGeneratorMaximum"]
    result["produktion_erwartet_gwh"] = merged["ProductionExpected"]
    result["leistung_pumpe_max_mw"] = merged["PumpsPowerInputMaximum"]
    result["leistung_motor_mw"] = merged["EnginePowerDemand"]
    result["stichtag_spec"] = merged["DateOfStatistic"]

    # Geometrie
    result["longitude"] = merged["longitude"]
    result["latitude"] = merged["latitude"]

    # Sortieren nach wasta_nummer für Konsistenz
    result = result.sort_values("wasta_nummer").reset_index(drop=True)

    return result


def build_geometry_geojson(df: pd.DataFrame) -> dict:
    """
    Baut eine GeoJSON-FeatureCollection mit Punkt-Geometrien für das Frontend.
    Nur die wichtigsten Properties (für Visualisierung), nicht alle Stammdaten.
    """
    features = []
    for _, row in df.iterrows():
        if pd.isna(row["longitude"]) or pd.isna(row["latitude"]):
            continue

        # Properties bewusst minimal halten — Detail-Daten kommen aus dim_wasserkraftwerk.json
        features.append({
            "type": "Feature",
            "properties": {
                "wasta_nummer": int(row["wasta_nummer"]),
                "name": row["name"],
                "kanton_code": row["kanton_code"] if pd.notna(row["kanton_code"]) else None,
                "typ_code": row["typ_code"],
                "status_code": row["status_code"],
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    round(float(row["longitude"]), 6),
                    round(float(row["latitude"]), 6),
                ],
            },
        })

    return {
        "type": "FeatureCollection",
        "features": features,
    }


def write_outputs(
    dim_df: pd.DataFrame,
    geometry_geojson: dict,
    intermediate_dir: Path,
) -> tuple:
    """Schreibt die zwei Output-Files."""
    dim_dir = intermediate_dir / "dim"
    dim_dir.mkdir(parents=True, exist_ok=True)

    dim_path = dim_dir / "wasserkraftwerk.json"
    geom_path = dim_dir / "wasserkraftwerk_geometry.geojson"

    # JSON-Output: konvertiere NaN zu None
    records = dim_df.where(pd.notna(dim_df), None).to_dict(orient="records")
    with open(dim_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    with open(geom_path, "w", encoding="utf-8") as f:
        json.dump(geometry_geojson, f, ensure_ascii=False)

    return dim_path, geom_path


def main():
    parser = argparse.ArgumentParser(
        description="Transform WASTA Wasserkraftwerke in dim_wasserkraftwerk + Geometry"
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
            print("FEHLER: Kein Snapshot mit WASTA-Daten gefunden.")
            sys.exit(1)

    snapshot_dir = SNAPSHOT_ROOT / snapshot_date
    wasta_dir = snapshot_dir / "bfe" / "wasta_wasserkraft"

    plants_csv = wasta_dir / "HydropowerPlant.csv"
    specs_csv = wasta_dir / "TechnicalSpecification.csv"
    type_csv = wasta_dir / "HydropowerPlantTypeCatalogue.csv"
    status_csv = wasta_dir / "HydropowerPlantOperationalStatusCatalogue.csv"

    for f in [plants_csv, specs_csv, type_csv, status_csv]:
        if not f.exists():
            print(f"FEHLER: {f} existiert nicht.")
            sys.exit(1)

    # === Output-Datum ===
    intermediate_date = args.intermediate_date or date.today().isoformat()
    intermediate_dir = INTERMEDIATE_ROOT / intermediate_date
    intermediate_dir.mkdir(parents=True, exist_ok=True)

    dim_path = intermediate_dir / "dim" / "wasserkraftwerk.json"
    geom_path = intermediate_dir / "dim" / "wasserkraftwerk_geometry.geojson"

    print(f"Snapshot-Datum:       {snapshot_date}")
    print(f"Snapshot-Verzeichnis: {snapshot_dir}")
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
    print("→ CSVs einlesen", end=" ", flush=True)
    plants_df = pd.read_csv(plants_csv)
    specs_df = pd.read_csv(specs_csv)
    print(f"(Plants: {len(plants_df)}, Specs: {len(specs_df)})")

    print("→ Catalogues einlesen", end=" ", flush=True)
    type_lookup = load_catalogue(type_csv)
    status_lookup = load_catalogue(status_csv)
    print(f"(Typen: {len(type_lookup)}, Status: {len(status_lookup)})")

    print("→ Transformieren (Join + Catalogue-Auflösung + Reprojektion)")
    dim_df = transform_wasta(plants_df, specs_df, type_lookup, status_lookup)
    print(f"  ✓ {len(dim_df)} Anlagen verarbeitet")

    print("→ Geometry-GeoJSON aufbauen", end=" ", flush=True)
    geometry_geojson = build_geometry_geojson(dim_df)
    print(f"({len(geometry_geojson['features'])} Punkt-Features)")

    print("→ Output schreiben")
    dim_path, geom_path = write_outputs(dim_df, geometry_geojson, intermediate_dir)
    dim_size_kb = dim_path.stat().st_size / 1024
    geom_size_kb = geom_path.stat().st_size / 1024
    print(f"  ✓ {dim_path.name:42s} ({dim_size_kb:7.1f} KB)")
    print(f"  ✓ {geom_path.name:42s} ({geom_size_kb:7.1f} KB)")

    # === Manifest ===
    existing_manifest = load_manifest(intermediate_dir)
    if existing_manifest:
        manifest = existing_manifest
    else:
        manifest = init_manifest(intermediate_date, "transform_wasta.py")

    add_file_to_manifest(
        manifest, "dim", "wasserkraftwerk", "json", dim_path,
        f"transform_wasta.py from {wasta_dir.relative_to(PIPELINE_ROOT.parent)}",
    )
    add_file_to_manifest(
        manifest, "dim", "wasserkraftwerk_geometry", "geojson", geom_path,
        f"transform_wasta.py from {wasta_dir.relative_to(PIPELINE_ROOT.parent)}",
    )

    manifest_path = write_manifest(manifest, intermediate_dir)

    print()
    print("=" * 60)
    print(f"Erfolgreich abgeschlossen.")
    print(f"Manifest: {manifest_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()