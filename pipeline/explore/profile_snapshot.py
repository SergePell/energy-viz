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
    """
    Profiliert eine CSV-Datei mit Robustheit gegen Header-Zeilen.

    BFE-Datensätze haben oft mehrzeilige Metadaten-Header (Titel, Lizenz,
    Beschreibung) vor der eigentlichen Datentabelle. pd.read_csv scheitert
    daran. Wir probieren mehrere skiprows-Werte und nehmen das Ergebnis
    mit den meisten gefundenen Spalten.
    """
    encoding, separator = detect_csv_format(filepath)

    # Strategie: skiprows=0..20 probieren, behalte das Ergebnis mit der
    # höchsten "Qualität" (= meiste Spalten × meiste Zeilen)
    best_result = None
    best_score = 0
    best_skiprows = 0
    last_error = None

    for skip in range(0, 21):
        try:
            df_try = pd.read_csv(
                filepath,
                encoding=encoding,
                sep=separator,
                skiprows=skip,
                low_memory=False,
                on_bad_lines="skip",  # Fallback: tolerante Mode
            )
            if len(df_try) == 0 or len(df_try.columns) == 0:
                continue
            score = len(df_try) * len(df_try.columns)
            if score > best_score:
                best_score = score
                best_result = df_try
                best_skiprows = skip
        except Exception as e:
            last_error = str(e)
            continue

    if best_result is None:
        # Komplette Niederlage — wenigstens Raw-Auszug zur Diagnose
        return {
            "format": "csv",
            "encoding": encoding,
            "separator": separator,
            "error": f"Konnte CSV nicht parsen. Letzter Fehler: {last_error}",
            "raw_preview": _read_raw_lines(filepath, encoding, n_lines=30),
        }

    profile = {
        "format": "csv",
        "encoding": encoding,
        "separator": separator,
        "skipped_header_rows": best_skiprows,
        **profile_dataframe(best_result),
    }

    if best_skiprows > 0:
        profile["note"] = (
            f"Datei hat {best_skiprows} Header-/Metadaten-Zeilen vor den "
            f"eigentlichen Daten. Diese wurden für die Tabellen-Erkennung "
            f"übersprungen, aber im raw_header dokumentiert."
        )
        profile["raw_header"] = _read_raw_lines(filepath, encoding, n_lines=best_skiprows)

    return profile


def _read_raw_lines(filepath: Path, encoding: str, n_lines: int) -> list:
    """Liest die ersten n Zeilen als Raw-Text — für Diagnose und Header-Doku."""
    try:
        with open(filepath, "r", encoding=encoding, errors="replace") as f:
            return [next(f).rstrip("\n\r") for _ in range(n_lines)]
    except StopIteration:
        return []
    except Exception:
        return []


def detect_csv_format(filepath: Path) -> tuple:
    """
    Versucht Encoding und Separator robust zu erkennen.
    BFE-CSVs sind oft UTF-8 mit Semikolon, manchmal Latin-1.

    Strategie für Separator: Mehrere Zeilen lesen (auch tief im File), die
    Spalten-Anzahl pro Separator zählen, und den Separator wählen, dessen
    Zählung am stabilsten und höchsten ist. Damit funktioniert es auch bei
    Files mit Metadaten-Header, in denen die ersten Zeilen anders aussehen
    als die eigentliche Tabelle.
    """
    # Encoding probieren
    encoding = None
    for enc in ["utf-8", "utf-8-sig", "latin-1", "cp1252"]:
        try:
            with open(filepath, "r", encoding=enc) as f:
                f.read(4096)  # nur ein Stück zum Test
            encoding = enc
            break
        except UnicodeDecodeError:
            continue
    if encoding is None:
        encoding = "utf-8"

    # Mehrere Zeilen lesen für Separator-Statistik
    lines = []
    try:
        with open(filepath, "r", encoding=encoding, errors="replace") as f:
            for i, line in enumerate(f):
                if i >= 50:  # nur erste 50 Zeilen ansehen, reicht
                    break
                lines.append(line)
    except Exception:
        pass

    # Pro Separator-Kandidat: wie konsistent ist die Spalten-Anzahl?
    candidates = [";", "\t", ","]
    best_sep = ","
    best_score = -1

    for sep in candidates:
        # Nur Zeilen mit mindestens einem Vorkommen des Separators zählen —
        # Header-Zeilen ohne Trennzeichen verfälschen sonst die Statistik
        counts = [line.count(sep) for line in lines if line.strip() and sep in line]
        if not counts:
            continue
        # Häufigste Spalten-Anzahl
        from collections import Counter
        counter = Counter(counts)
        most_common_count, frequency = counter.most_common(1)[0]
        # Score = (# Trennzeichen pro Zeile) × (Anzahl Zeilen mit dieser Anzahl)
        # Bevorzugt Separatoren, die in vielen Zeilen ähnlich oft vorkommen
        score = most_common_count * frequency
        if score > best_score:
            best_score = score
            best_sep = sep

    return encoding, best_sep


def profile_xlsx(filepath: Path) -> dict:
    """
    Profiliert eine Excel-Datei (XLSX oder XLS, ALLE Sheets).
    Bei Swissgrid und ähnlichen Files sind Multi-Sheet üblich (Einstellungen,
    Daten, Übersichten). Wir profilieren jedes Sheet einzeln, damit du die
    Struktur jedes Sheets siehst.
    """
    try:
        xl = pd.ExcelFile(filepath)
    except Exception as e:
        return {
            "format": filepath.suffix.lstrip(".").lower(),
            "error": f"Konnte Datei nicht öffnen: {e}",
            "hint": "Für .xls: pip install xlrd. Für .xlsx: pip install openpyxl",
        }

    sheet_names = xl.sheet_names
    sheets_profiled = {}
    sheet_errors = {}

    for sheet in sheet_names:
        try:
            df = pd.read_excel(filepath, sheet_name=sheet)
            if df.empty:
                sheets_profiled[sheet] = {
                    "rows": 0,
                    "n_columns": 0,
                    "note": "Sheet ist leer",
                }
            else:
                sheets_profiled[sheet] = profile_dataframe(df)
        except Exception as e:
            sheet_errors[sheet] = str(e)

    profile = {
        "format": filepath.suffix.lstrip(".").lower(),
        "all_sheets": sheet_names,
        "sheets": sheets_profiled,
    }

    if sheet_errors:
        profile["sheet_errors"] = sheet_errors

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

    # Layer auflisten — gpd.list_layers gibt ein DataFrame mit Spalte 'name' zurück
    try:
        layers_df = gpd.list_layers(filepath)
        if hasattr(layers_df, "columns") and "name" in layers_df.columns:
            layer_names = layers_df["name"].tolist()
        else:
            # Fallback: pyogrio direkt verwenden
            import pyogrio
            layer_info = pyogrio.list_layers(str(filepath))
            layer_names = [row[0] for row in layer_info]
    except Exception as e:
        return {
            "format": "gpkg",
            "error": f"Konnte Layer nicht auflisten: {e}",
        }

    if not layer_names:
        return {
            "format": "gpkg",
            "error": "Keine Layer im GeoPackage gefunden",
        }

    # Ersten Layer profilieren
    try:
        gdf = gpd.read_file(filepath, layer=layer_names[0])
    except Exception as e:
        return {
            "format": "gpkg",
            "all_layers": layer_names,
            "error": f"Konnte Layer '{layer_names[0]}' nicht lesen: {e}",
        }

    profile = {
        "format": "gpkg",
        "all_layers": layer_names,
        "profiled_layer": layer_names[0],
        "crs": str(gdf.crs) if gdf.crs else None,
        "geometry_type": str(gdf.geom_type.value_counts().to_dict())
                         if not gdf.empty else None,
        "bbox": [float(x) for x in gdf.total_bounds] if not gdf.empty else None,
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

def _render_columns_table(columns: list) -> str:
    """Erzeugt aus einer Spalten-Liste die Markdown-Tabelle."""
    lines = []
    lines.append("| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |")
    lines.append("|------|-----|-------|--------|--------------------------|")

    for col in columns:
        # Spaltennamen: Newlines entfernen für saubere Tabelle
        name = str(col["name"]).replace("\n", " | ")
        dtype = col["dtype"]
        nulls = f"{col['null_count']} ({col['null_pct']}%)"
        unique = col["unique_count"]

        if "min" in col and col["min"] is not None:
            mean_str = f"{col['mean']:.2f}" if col.get("mean") is not None else "—"
            value_info = f"{col['min']} … {col['max']} (mean {mean_str})"
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

    return "\n".join(lines)


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
        if profile.get("skipped_header_rows", 0) > 0:
            lines.append(f"**Übersprungene Header-Zeilen:** "
                         f"{profile['skipped_header_rows']}")
        lines.append("")

        # Bei Diagnose-Bedarf: rohe Header-Zeilen zeigen
        if "raw_header" in profile:
            lines.append("### Übersprungene Header-Zeilen (zur Doku)")
            lines.append("```")
            for line in profile["raw_header"]:
                lines.append(line)
            lines.append("```")
            lines.append("")

        if "raw_preview" in profile:
            lines.append("### Raw-Vorschau (CSV konnte nicht geparst werden)")
            lines.append("```")
            for line in profile["raw_preview"]:
                lines.append(line)
            lines.append("```")
            lines.append("")

    elif profile.get("format") == "xlsx" or profile.get("format") == "xls":
        lines.append(f"**Sheets:** {', '.join(profile.get('all_sheets', []))}")
        lines.append("")

        # Bei Multi-Sheet-Profilen: pro Sheet einen eigenen Block rendern
        if "sheets" in profile:
            for sheet_name, sheet_profile in profile["sheets"].items():
                lines.append(f"## Sheet: `{sheet_name}`")
                lines.append("")
                if "note" in sheet_profile:
                    lines.append(f"> {sheet_profile['note']}")
                    lines.append("")
                if "rows" in sheet_profile:
                    lines.append(f"**Zeilen:** {sheet_profile['rows']:,}")
                    lines.append(f"**Spalten:** {sheet_profile['n_columns']}")
                    lines.append("")
                if "columns" in sheet_profile and sheet_profile["columns"]:
                    lines.append(_render_columns_table(sheet_profile["columns"]))
                    lines.append("")
            # Sheet-Errors falls vorhanden
            if "sheet_errors" in profile:
                lines.append("## Fehler beim Lesen einzelner Sheets")
                for sheet, err in profile["sheet_errors"].items():
                    lines.append(f"- `{sheet}`: {err}")
                lines.append("")
            return "\n".join(lines)
        # Fallback (alte Struktur falls vorhanden)
        if "note" in profile:
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

    # Spalten-Tabelle (für CSV / JSON-Records)
    if "columns" in profile:
        lines.append("## Spalten")
        lines.append("")
        lines.append(_render_columns_table(profile["columns"]))
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
    ".xls": profile_xlsx,  # älteres Excel-Format, gleicher Profiler
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

    # Alle Datendateien rekursiv durchgehen
    profiled_count = 0
    for source_family_dir in snapshot_dir.iterdir():
        if not source_family_dir.is_dir():
            continue

        # rglob statt iterdir: damit auch entpackte ZIP-Bundles in Unterordnern
        # (z.B. snapshot/bfe/wasta_wasserkraft/HydropowerPlant.csv) profiliert werden
        all_files = sorted(source_family_dir.rglob("*"))

        for filepath in all_files:
            if not filepath.is_file():
                continue
            if filepath.suffix.lower() not in PROFILER_BY_EXTENSION:
                continue
            if args.file and filepath.name != args.file:
                continue
            # _manifest.json ausschliessen
            if filepath.name == "_manifest.json":
                continue

            # Output-Pfad: behalte die relative Struktur unter snapshot_dir bei,
            # aber flatten zu eindeutigen Namen für die Profile
            rel_path = filepath.relative_to(snapshot_dir)
            # rel_path z.B. 'bfe/wasta_wasserkraft/HydropowerPlant.csv'
            # Profil-Name: 'bfe__wasta_wasserkraft__HydropowerPlant'
            profile_stem = "__".join(rel_path.with_suffix("").parts)

            print(f"→ {rel_path}")
            profile = profile_file(filepath)
            if profile is None:
                continue

            # JSON schreiben
            json_path = profiles_dir / f"{profile_stem}.profile.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(profile, f, indent=2, ensure_ascii=False, default=str)

            # Markdown schreiben
            manifest_entry = find_manifest_entry(manifest, filepath)
            md = render_markdown(profile, filepath, manifest_entry)
            md_path = profiles_dir / f"{profile_stem}.profile.md"
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md)

            print(f"  ✓ {json_path.name}")
            profiled_count += 1

    print()
    print("=" * 60)
    print(f"Profiliert: {profiled_count} Dateien")
    print(f"Outputs:    {profiles_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
