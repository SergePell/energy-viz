"""
Profile-Skript für Snapshots.

Geht durch einen Snapshot-Ordner und erstellt pro Datendatei zwei Profile:
- <quelle>.profile.json — strukturiert, maschinenlesbar (für Snapshot-Vergleiche)
- <quelle>.profile.md   — formatiert, für Menschen (Obsidian, Thesis-Material)

Funktioniert für: CSV, XLSX, GeoPackage, JSON.

Aufruf:
    python pipeline/explore/profile_snapshot.py
        Profiliert den neuesten Snapshot

    python pipeline/explore/profile_snapshot.py --date 2026-05-03
        Profiliert spezifischen Snapshot

    python pipeline/explore/profile_snapshot.py --file pv_grossanlagen.csv
        Profiliert nur eine bestimmte Datei

    python pipeline/explore/profile_snapshot.py --diff
        Vergleicht den aktuellen Snapshot mit dem vorigen und zeigt Änderungen

Outputs gehen nach: pipeline/profiles/<snapshot_date>/
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd

# Pfad-Setup
PIPELINE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PIPELINE_ROOT.parent))

from pipeline.utils.manifest import load_manifest


SNAPSHOT_ROOT = PIPELINE_ROOT / "raw" / "snapshots"
PROFILES_ROOT = PIPELINE_ROOT / "profiles"


# === Profil-Erstellung pro Dateityp ===

def profile_csv(filepath: Path) -> dict:
    """Profiliert eine CSV-Datei."""
    # Erst encoding und separator robust erkennen
    encoding, separator = detect_csv_format(filepath)

    df = pd.read_csv(filepath, encoding=encoding, sep=separator, low_memory=False)

    return {
        "format": "csv",
        "encoding": encoding,
        "separator": separator,
        **profile_dataframe(df),
    }


def detect_csv_format(filepath: Path) -> tuple:
    """
    Versucht Encoding und Separator robust zu erkennen.
    BFE-CSVs sind oft UTF-8 mit Semikolon, manchmal Latin-1.
    """
    # Encoding probieren
    for enc in ["utf-8", "utf-8-sig", "latin-1", "cp1252"]:
        try:
            with open(filepath, "r", encoding=enc) as f:
                first_line = f.readline()
            encoding = enc
            break
        except UnicodeDecodeError:
            continue
    else:
        encoding = "utf-8"
        first_line = ""

    # Separator: Semikolon-Heuristik
    if first_line.count(";") > first_line.count(","):
        separator = ";"
    elif first_line.count("\t") > first_line.count(","):
        separator = "\t"
    else:
        separator = ","

    return encoding, separator


def profile_xlsx(filepath: Path) -> dict:
    """Profiliert eine XLSX-Datei (erstes Sheet)."""
    xl = pd.ExcelFile(filepath)
    sheet_names = xl.sheet_names

    # Erstes Sheet profilieren
    df = pd.read_excel(filepath, sheet_name=sheet_names[0])

    profile = {
        "format": "xlsx",
        "all_sheets": sheet_names,
        "profiled_sheet": sheet_names[0],
        **profile_dataframe(df),
    }

    if len(sheet_names) > 1:
        profile["note"] = (
            f"Datei hat {len(sheet_names)} Sheets. Profiliert wurde nur das erste "
            f"('{sheet_names[0]}'). Andere Sheets ggf. separat prüfen."
        )

    return profile


def profile_geopackage(filepath: Path) -> dict:
    """Profiliert ein GeoPackage."""
    try:
        import geopandas as gpd
    except ImportError:
        return {
            "format": "gpkg",
            "error": "geopandas nicht installiert. "
                     "Installiere mit: pip install geopandas",
        }

    # Layer auflisten
    layers = gpd.list_layers(filepath)
    layer_names = layers["name"].tolist() if hasattr(layers, "tolist") else list(layers)

    # Ersten Layer profilieren
    gdf = gpd.read_file(filepath, layer=layer_names[0])

    profile = {
        "format": "gpkg",
        "all_layers": layer_names,
        "profiled_layer": layer_names[0],
        "crs": str(gdf.crs) if gdf.crs else None,
        "geometry_type": str(gdf.geom_type.value_counts().to_dict())
                         if not gdf.empty else None,
        "bbox": list(gdf.total_bounds) if not gdf.empty else None,
        **profile_dataframe(pd.DataFrame(gdf.drop(columns="geometry", errors="ignore"))),
    }

    if len(layer_names) > 1:
        profile["note"] = (
            f"GeoPackage hat {len(layer_names)} Layer. Profiliert wurde nur "
            f"der erste ('{layer_names[0]}')."
        )

    return profile


def profile_json(filepath: Path) -> dict:
    """Profiliert eine JSON-Datei."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list) and data and isinstance(data[0], dict):
        # Array of records — als DataFrame profilieren
        df = pd.DataFrame(data)
        return {
            "format": "json",
            "structure": "array_of_records",
            **profile_dataframe(df),
        }
    elif isinstance(data, dict):
        return {
            "format": "json",
            "structure": "object",
            "top_level_keys": list(data.keys()),
        }
    else:
        return {
            "format": "json",
            "structure": "other",
            "type": type(data).__name__,
        }


def profile_dataframe(df: pd.DataFrame) -> dict:
    """Erstellt das eigentliche Spalten-Profil eines DataFrames."""
    columns_info = []

    for col in df.columns:
        series = df[col]
        col_info = {
            "name": col,
            "dtype": str(series.dtype),
            "null_count": int(series.isnull().sum()),
            "null_pct": round(float(series.isnull().mean() * 100), 2),
            "unique_count": int(series.nunique(dropna=True)),
        }

        non_null = series.dropna()

        # Numerische Spalten
        if pd.api.types.is_numeric_dtype(series) and not non_null.empty:
            col_info.update({
                "min": _safe_value(non_null.min()),
                "max": _safe_value(non_null.max()),
                "mean": _safe_value(non_null.mean()),
                "median": _safe_value(non_null.median()),
            })

        # Datums-Spalten (heuristisch erkennen)
        elif pd.api.types.is_datetime64_any_dtype(series) and not non_null.empty:
            col_info.update({
                "min_date": str(non_null.min()),
                "max_date": str(non_null.max()),
            })

        # Kategoriale / String-Spalten — Beispiele zeigen
        else:
            sample = non_null.head(5).astype(str).tolist()
            col_info["examples"] = sample

            # Falls wenige unique values: alle zeigen (ist kategorial)
            if col_info["unique_count"] <= 20 and not non_null.empty:
                col_info["all_values"] = sorted(
                    non_null.unique().astype(str).tolist()
                )

        columns_info.append(col_info)

    return {
        "rows": len(df),
        "n_columns": len(df.columns),
        "columns": columns_info,
    }


def _safe_value(val):
    """Konvertiert numpy-Typen in Python-Native für JSON-Serialisierung."""
    if pd.isna(val):
        return None
    if hasattr(val, "item"):
        return val.item()
    return val


# === Renderer ===

def render_markdown(profile: dict, filepath: Path, manifest_entry: Optional[dict]) -> str:
    """Erzeugt aus dem Profil eine Markdown-Übersicht."""
    lines = []
    lines.append(f"# Profil: {filepath.name}")
    lines.append("")
    lines.append(f"**Erstellt:** {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"**Pfad:** `{filepath}`")
    lines.append(f"**Format:** {profile.get('format', '?').upper()}")

    if manifest_entry:
        lines.append(f"**SHA-256:** `{manifest_entry.get('sha256', '?')}`")
        lines.append(f"**Quelle:** {manifest_entry.get('url', '?')}")
        lines.append(f"**Grösse:** {manifest_entry.get('size_bytes', 0) / 1024:.1f} KB")

    lines.append("")

    # Format-spezifische Hinweise
    if profile.get("format") == "csv":
        lines.append(f"**Encoding:** {profile.get('encoding')}")
        lines.append(f"**Separator:** `{profile.get('separator')}`")
        lines.append("")
    elif profile.get("format") == "xlsx":
        lines.append(f"**Sheets:** {', '.join(profile.get('all_sheets', []))}")
        lines.append(f"**Profiliertes Sheet:** {profile.get('profiled_sheet')}")
        if "note" in profile:
            lines.append("")
            lines.append(f"> {profile['note']}")
        lines.append("")
    elif profile.get("format") == "gpkg":
        lines.append(f"**Layer:** {', '.join(profile.get('all_layers', []))}")
        lines.append(f"**CRS:** {profile.get('crs')}")
        lines.append(f"**Geometrie-Typ:** {profile.get('geometry_type')}")
        if profile.get("bbox"):
            bbox = profile["bbox"]
            lines.append(f"**BBox:** [{bbox[0]:.4f}, {bbox[1]:.4f}, "
                         f"{bbox[2]:.4f}, {bbox[3]:.4f}]")
        lines.append("")

    # Allgemeine Stats
    if "rows" in profile:
        lines.append(f"**Zeilen:** {profile['rows']:,}")
        lines.append(f"**Spalten:** {profile['n_columns']}")
        lines.append("")

    # Spalten-Tabelle
    if "columns" in profile:
        lines.append("## Spalten")
        lines.append("")
        lines.append("| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |")
        lines.append("|------|-----|-------|--------|--------------------------|")

        for col in profile["columns"]:
            name = col["name"]
            dtype = col["dtype"]
            nulls = f"{col['null_count']} ({col['null_pct']}%)"
            unique = col["unique_count"]

            # Wertebereich kompakt
            if "min" in col:
                value_info = f"{col['min']} … {col['max']} (mean {col['mean']:.2f})"
            elif "min_date" in col:
                value_info = f"{col['min_date']} … {col['max_date']}"
            elif "all_values" in col:
                vals = col["all_values"]
                if len(vals) <= 8:
                    value_info = ", ".join(f"`{v}`" for v in vals)
                else:
                    value_info = ", ".join(f"`{v}`" for v in vals[:5]) + f", … (+{len(vals)-5})"
            elif "examples" in col:
                value_info = ", ".join(f"`{v}`" for v in col["examples"][:3])
            else:
                value_info = "—"

            lines.append(f"| `{name}` | {dtype} | {nulls} | {unique} | {value_info} |")

        lines.append("")

    # JSON-Spezifika
    if profile.get("structure") == "object":
        lines.append("## Top-Level-Keys")
        for key in profile.get("top_level_keys", []):
            lines.append(f"- `{key}`")
        lines.append("")

    return "\n".join(lines)


# === Hauptlogik ===

PROFILER_BY_EXTENSION = {
    ".csv": profile_csv,
    ".xlsx": profile_xlsx,
    ".gpkg": profile_geopackage,
    ".json": profile_json,
}


def profile_file(filepath: Path) -> Optional[dict]:
    """Profiliert eine einzelne Datei je nach Endung."""
    ext = filepath.suffix.lower()
    profiler = PROFILER_BY_EXTENSION.get(ext)
    if not profiler:
        print(f"  ! Kein Profiler für {ext}, übersprungen.")
        return None

    try:
        return profiler(filepath)
    except Exception as e:
        print(f"  ! Fehler beim Profilieren: {e}")
        return {"format": ext.lstrip("."), "error": str(e)}


def find_manifest_entry(manifest: dict, filepath: Path) -> Optional[dict]:
    """Sucht den Manifest-Eintrag zur gegebenen Datei."""
    if not manifest:
        return None
    for source_family, datasets in manifest.get("sources", {}).items():
        for dataset_id, formats in datasets.items():
            for format_key, entry in formats.items():
                if entry.get("filename") == filepath.name:
                    return entry
    return None


def get_latest_snapshot() -> Optional[Path]:
    """Findet den neuesten Snapshot-Ordner."""
    if not SNAPSHOT_ROOT.exists():
        return None
    snapshots = sorted([p for p in SNAPSHOT_ROOT.iterdir() if p.is_dir()])
    return snapshots[-1] if snapshots else None


def main():
    parser = argparse.ArgumentParser(
        description="Erzeugt Profile pro Datei in einem Snapshot."
    )
    parser.add_argument(
        "--date", default=None,
        help="Snapshot-Datum YYYY-MM-DD (default: neuester Snapshot)",
    )
    parser.add_argument(
        "--file", default=None,
        help="Nur eine spezifische Datei profilieren (Dateiname)",
    )
    args = parser.parse_args()

    # Snapshot bestimmen
    if args.date:
        snapshot_dir = SNAPSHOT_ROOT / args.date
    else:
        snapshot_dir = get_latest_snapshot()
        if snapshot_dir is None:
            print(f"FEHLER: Keine Snapshots in {SNAPSHOT_ROOT} gefunden.")
            sys.exit(1)

    if not snapshot_dir.exists():
        print(f"FEHLER: Snapshot {snapshot_dir} existiert nicht.")
        sys.exit(1)

    snapshot_date = snapshot_dir.name
    profiles_dir = PROFILES_ROOT / snapshot_date
    profiles_dir.mkdir(parents=True, exist_ok=True)

    # Manifest laden (für Provenance-Infos in Profilen)
    manifest = load_manifest(snapshot_dir)

    print(f"Snapshot:      {snapshot_dir}")
    print(f"Profile gehen nach: {profiles_dir}")
    print()

    # Alle Datendateien durchgehen
    profiled_count = 0
    for source_family_dir in snapshot_dir.iterdir():
        if not source_family_dir.is_dir():
            continue

        for filepath in sorted(source_family_dir.iterdir()):
            if filepath.suffix.lower() not in PROFILER_BY_EXTENSION:
                continue
            if args.file and filepath.name != args.file:
                continue

            print(f"→ {filepath.name}")
            profile = profile_file(filepath)
            if profile is None:
                continue

            # JSON schreiben
            json_path = profiles_dir / f"{filepath.stem}.profile.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(profile, f, indent=2, ensure_ascii=False, default=str)

            # Markdown schreiben
            manifest_entry = find_manifest_entry(manifest, filepath)
            md = render_markdown(profile, filepath, manifest_entry)
            md_path = profiles_dir / f"{filepath.stem}.profile.md"
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md)

            print(f"  ✓ {json_path.name}")
            print(f"  ✓ {md_path.name}")
            profiled_count += 1

    print()
    print("=" * 60)
    print(f"Profiliert: {profiled_count} Dateien")
    print(f"Outputs:    {profiles_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
