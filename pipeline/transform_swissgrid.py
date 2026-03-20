#!/usr/bin/env python3
"""
transform_swissgrid_v2.py
=========================
Transformiert Swissgrid EnergieUebersichtCH XLSX → JSON für energy-viz.

Basiert auf der tatsächlichen XLSX-Struktur (verifiziert 2023 + 2024):
  - Alle Daten im Sheet "Zeitreihen0h15" (65 Spalten)
  - Zeile 0 = Einheiten (kWh), Zeile 1+ = Daten
  - Timestamps in Spalte "Unnamed: 0" als "DD.MM.YYYY HH:MM"
  - Alle Wert-Spalten als object (string) → müssen numerisch konvertiert werden

Outputs:
  1) swissgrid-national-15min-{year}.json
  2) swissgrid-kanton-15min-{year}.json  (oder aggregiert)
  3) swissgrid-cross-border-15min-{year}.json

Verwendung:
    python transform_swissgrid_v2.py
    python transform_swissgrid_v2.py --year 2024 --out-dir src/data
    python transform_swissgrid_v2.py --years 2020,2021,2022,2023,2024
    python transform_swissgrid_v2.py --year 2024 --kanton-agg 1h
"""

import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd
import numpy as np
import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE_URL = "https://www.swissgrid.ch/dam/dataimport/energy-statistic"
DATA_SHEET = "Zeitreihen0h15"

# Spalten-Mapping: Kurzname → Substring im Original-Spaltennamen
# (Swissgrid-Spalten haben DE\nEN Format, wir matchen auf den DE-Teil)
NATIONAL_COLS = {
    "prod": "Summe produzierte Energie",
    "cons": "Summe verbrauchte Energie",
    "end_cons": "Summe endverbrauchte Energie",
    "net_out": "Netto Ausspeisung",
    "grid_in": "Vertikale Einspeisung",
}

CROSS_BORDER_COLS = {
    "ch_to_at": "CH->AT",
    "at_to_ch": "AT->CH",
    "ch_to_de": "CH->DE",
    "de_to_ch": "DE->CH",
    "ch_to_fr": "CH->FR",
    "fr_to_ch": "FR->CH",
    "ch_to_it": "CH->IT",
    "it_to_ch": "IT->CH",
}

# Kanton-Kürzel → BFS-ID
KANTON_BFS = {
    "ZH": 1, "BE": 2, "LU": 3, "UR": 4, "SZ": 5, "OW": 6, "NW": 7,
    "GL": 8, "ZG": 9, "FR": 10, "SO": 11, "BS": 12, "BL": 13, "SH": 14,
    "AR": 15, "AI": 16, "SG": 17, "GR": 18, "AG": 19, "TG": 20,
    "TI": 21, "VD": 22, "VS": 23, "NE": 24, "GE": 25, "JU": 26
}

KANTON_NAMES = {
    "ZH": "Zürich", "BE": "Bern", "LU": "Luzern", "UR": "Uri",
    "SZ": "Schwyz", "OW": "Obwalden", "NW": "Nidwalden", "GL": "Glarus",
    "ZG": "Zug", "FR": "Fribourg", "SO": "Solothurn", "BS": "Basel-Stadt",
    "BL": "Basel-Landschaft", "SH": "Schaffhausen", "AR": "Appenzell A.Rh.",
    "AI": "Appenzell I.Rh.", "SG": "St. Gallen", "GR": "Graubünden",
    "AG": "Aargau", "TG": "Thurgau", "TI": "Ticino", "VD": "Vaud",
    "VS": "Valais", "NE": "Neuchâtel", "GE": "Genève", "JU": "Jura"
}


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------

def download_xlsx(year: int, target_dir: Path = Path("raw")) -> Path:
    """
    Lade EnergieUebersichtCH-{year} herunter.
    - Ab 2020: .xlsx
    - 2009–2019: .xls (altes Excel-Format)
    Prüft zuerst ob eine lokale Datei existiert (.xlsx oder .xls).
    """
    target_dir.mkdir(parents=True, exist_ok=True)

    # Prüfe ob lokal bereits vorhanden (beide Formate)
    for ext in [".xlsx", ".xls"]:
        filepath = target_dir / f"EnergieUebersichtCH-{year}{ext}"
        if filepath.exists():
            print(f"  ✓ Datei existiert bereits: {filepath}")
            return filepath

    # Download: passendes Format wählen
    extensions = [".xlsx", ".xls"] if year >= 2020 else [".xls", ".xlsx"]

    for ext in extensions:
        filename = f"EnergieUebersichtCH-{year}{ext}"
        url = f"{BASE_URL}/{filename}"
        print(f"  ⬇ Versuche {url} ...")

        try:
            resp = requests.get(url, timeout=120)
            if resp.status_code == 404:
                print(f"    → 404, versuche alternatives Format ...")
                continue
            resp.raise_for_status()

            filepath = target_dir / filename
            filepath.write_bytes(resp.content)
            size_mb = len(resp.content) / (1024 * 1024)
            print(f"  ✓ Gespeichert: {filepath} ({size_mb:.1f} MB)")
            return filepath

        except requests.exceptions.HTTPError as e:
            print(f"    → HTTP-Fehler: {e}")
            continue
        except requests.exceptions.RequestException as e:
            print(f"    → Netzwerk-Fehler: {e}")
            continue

    raise FileNotFoundError(f"Konnte EnergieUebersichtCH-{year} weder als .xlsx noch .xls herunterladen")


# ---------------------------------------------------------------------------
# Core: Sheet lesen und aufbereiten
# ---------------------------------------------------------------------------

def read_zeitreihen(filepath: Path) -> pd.DataFrame:
    """
    Lese das Zeitreihen-Sheet und bereite es auf:
    - Findet das Sheet dynamisch (Zeitreihen0h15 oder ähnlich)
    - Überspringe Zeile 0 (Einheiten-Zeile)
    - Parse Timestamps
    - Konvertiere alle Wert-Spalten zu float

    Unterstützt .xlsx (openpyxl) und .xls (xlrd).
    """
    ext = filepath.suffix.lower()
    engine = "xlrd" if ext == ".xls" else "openpyxl"

    # Sheet-Namen lesen
    xl = pd.ExcelFile(filepath, engine=engine)
    print(f"  Sheets: {xl.sheet_names}")

    # Daten-Sheet finden (verschiedene mögliche Namen)
    data_sheet = None
    for name in xl.sheet_names:
        if any(kw in name.lower() for kw in ["zeitreihen", "timeseries", "data", "0h15"]):
            data_sheet = name
            break

    if not data_sheet:
        # Fallback: Sheet mit den meisten Spalten
        max_cols = 0
        for name in xl.sheet_names:
            try:
                test_df = pd.read_excel(filepath, sheet_name=name, header=0, nrows=3, engine=engine)
                if test_df.shape[1] > max_cols:
                    max_cols = test_df.shape[1]
                    data_sheet = name
            except Exception:
                pass

    if not data_sheet:
        raise ValueError(f"Kein Daten-Sheet gefunden in {filepath.name}. Sheets: {xl.sheet_names}")

    print(f"  Lese Sheet '{data_sheet}' (engine={engine}) ...")

    df = pd.read_excel(filepath, sheet_name=data_sheet, header=0, engine=engine)

    # Erste Datenzeile enthält Einheiten ("kWh", "MW") → entfernen
    ts_col = df.columns[0]
    unit_mask = df[ts_col].astype(str).str.contains(
        "Zeitstempel|kWh|MW|Einheit|Timestamp", case=False, na=False
    )
    df = df[~unit_mask].copy()

    # Timestamps parsen (Format: "DD.MM.YYYY HH:MM" oder "YYYY-MM-DD HH:MM:SS")
    df["timestamp"] = pd.to_datetime(df[ts_col], dayfirst=True, format="mixed")
    df = df.drop(columns=[ts_col])

    # Alle anderen Spalten zu numerisch konvertieren
    for col in df.columns:
        if col != "timestamp":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Nach Timestamp sortieren
    df = df.sort_values("timestamp").reset_index(drop=True)

    print(f"  ✓ {len(df)} Zeilen, {len(df.columns)} Spalten")
    print(f"  ✓ Zeitraum: {df['timestamp'].min()} → {df['timestamp'].max()}")

    return df


def find_col(df: pd.DataFrame, substring: str) -> str | None:
    """Finde Spaltenname der den Substring enthält (case-insensitive)."""
    for col in df.columns:
        if substring.lower() in col.lower():
            return col
    return None


def find_kanton_cols(df: pd.DataFrame) -> dict:
    """
    Erkennt Kantons-Spalten für Produktion und Verbrauch.

    Swissgrid hat zwei Formate:
      Einzeln:  "Produktion Kanton AG\nProduction Canton AG"
      Gruppe:   "Produktion Kantone AI, AR\nProduction Cantons AI, AR"
                "Produktion Kantone OW, NW, UR\nProduction Cantons OW, NW, UR"

    Returns:
      {
        "single": {
          "prod": { "AG": <col_name>, "FR": <col_name>, ... },
          "cons": { "AG": <col_name>, "FR": <col_name>, ... }
        },
        "grouped": {
          "prod": { ("AI","AR"): <col_name>, ("BL","BS"): <col_name>, ... },
          "cons": { ("AI","AR"): <col_name>, ("BL","BS"): <col_name>, ... }
        }
      }
    """
    single_prod = {}
    single_cons = {}
    grouped_prod = {}
    grouped_cons = {}

    for col in df.columns:
        col_str = str(col)

        # --- Einzelkanton: "Produktion Kanton AG" ---
        m = re.search(r"Produktion Kanton\s+([A-Z]{2})", col_str)
        if m:
            single_prod[m.group(1)] = col
            continue
        m = re.search(r"Verbrauch Kanton\s+([A-Z]{2})", col_str)
        if m:
            single_cons[m.group(1)] = col
            continue

        # --- Kantonsgruppe: "Produktion Kantone AI, AR" oder "...OW, NW, UR" ---
        m = re.search(r"Produktion Kantone\s+((?:[A-Z]{2},?\s*)+)", col_str)
        if m:
            abbrs = tuple(a.strip() for a in m.group(1).split(",") if a.strip())
            grouped_prod[abbrs] = col
            continue
        m = re.search(r"Verbrauch Kantone\s+((?:[A-Z]{2},?\s*)+)", col_str)
        if m:
            abbrs = tuple(a.strip() for a in m.group(1).split(",") if a.strip())
            grouped_cons[abbrs] = col
            continue

    return {
        "single": {"prod": single_prod, "cons": single_cons},
        "grouped": {"prod": grouped_prod, "cons": grouped_cons}
    }


# ---------------------------------------------------------------------------
# Transform 1: National
# ---------------------------------------------------------------------------

def transform_national(df: pd.DataFrame, year: int) -> dict:
    """
    Nationale Zeitreihe: Produktion, Verbrauch, Endverbrauch, Netz.

    Output-Schema:
    {
      "meta": { ... },
      "data": [
        {
          "t": "2024-01-01T00:15:00",
          "prod": 1296448,
          "cons": 1939192,
          "end_cons": 1443841,
          "net_out": ...,
          "grid_in": ...
        }
      ]
    }
    """
    print("\n  [National] Spalten-Matching ...")

    col_map = {}
    for key, substring in NATIONAL_COLS.items():
        matched = find_col(df, substring)
        if matched:
            col_map[key] = matched
            print(f"    ✓ {key:10s} → '{matched[:60]}...'")
        else:
            print(f"    ✗ {key:10s} → NICHT GEFUNDEN (Substring: '{substring}')")

    if not col_map:
        raise ValueError("Keine nationalen Spalten gefunden")

    data = []
    for _, row in df.iterrows():
        entry = {"t": row["timestamp"].isoformat()}
        for key, orig_col in col_map.items():
            val = row[orig_col]
            entry[key] = round(float(val)) if pd.notna(val) else None
        data.append(entry)

    output = {
        "meta": {
            "dataset": "swissgrid-national",
            "resolution": "15min",
            "unit": "kWh",
            "year": year,
            "records": len(data),
            "fields": list(col_map.keys()),
            "source": "Swissgrid EnergieUebersichtCH",
            "source_url": "https://www.swissgrid.ch/de/home/customers/topics/energy-data-ch.html",
            "note": "Regelblock CH (inkl. FL, Teile Elsass; exkl. Laufenburg). Abweichung <2%."
        },
        "data": data
    }

    print(f"    → {len(data)} Records")
    return output


# ---------------------------------------------------------------------------
# Transform 2: Kanton
# ---------------------------------------------------------------------------

def transform_kanton(df: pd.DataFrame, year: int, aggregate: str = "15min") -> dict:
    """
    Kantonale Produktion + Verbrauch.

    Swissgrid liefert 11 Einzelkantone + 7 Gruppen (15 weitere Kantone).
    Gruppen werden als solche beibehalten (z.B. "SH+ZH"), da eine Aufteilung
    auf Einzelkantone Annahmen erfordern würde.

    Output-Schema:
    {
      "meta": { ... },
      "regions": {
        "AG":      { "cantons": ["AG"],           "bfs_ids": [19] },
        "SH+ZH":   { "cantons": ["SH", "ZH"],     "bfs_ids": [14, 1] },
        "OW+NW+UR": { "cantons": ["OW","NW","UR"], "bfs_ids": [6, 7, 4] },
        ...
      },
      "data": [
        {
          "t": "2024-01-01T01:00:00",
          "prod": { "AG": 12345, "SH+ZH": 99999, ... },
          "cons": { "AG": 23456, "SH+ZH": 88888, ... }
        }
      ]
    }
    """
    print("\n  [Kanton] Spalten-Matching ...")

    kanton_cols = find_kanton_cols(df)
    n_single_prod = len(kanton_cols["single"]["prod"])
    n_single_cons = len(kanton_cols["single"]["cons"])
    n_group_prod = len(kanton_cols["grouped"]["prod"])
    n_group_cons = len(kanton_cols["grouped"]["cons"])

    print(f"    Einzelkantone:  {n_single_prod} Prod, {n_single_cons} Cons")
    print(f"    Kantonsgruppen: {n_group_prod} Prod, {n_group_cons} Cons")

    for abbr, col in sorted(kanton_cols["single"]["prod"].items()):
        print(f"      ✓ {abbr}")
    for group, col in kanton_cols["grouped"]["prod"].items():
        print(f"      ✓ {'+'.join(group)} (Gruppe)")

    total = n_single_prod + n_group_prod + n_single_cons + n_group_cons
    if total == 0:
        print("    ⚠ Keine Kantons-Spalten erkannt")
        return {}

    # --- Build unified region mapping ---
    # Key = region_id (e.g. "AG" or "SH+ZH"), Value = column name
    regions_meta = {}
    prod_region_cols = {}  # region_id → orig column
    cons_region_cols = {}

    # Singles
    for abbr, col in kanton_cols["single"]["prod"].items():
        rid = abbr
        prod_region_cols[rid] = col
        regions_meta[rid] = {
            "cantons": [abbr],
            "bfs_ids": [KANTON_BFS[abbr]],
            "names": [KANTON_NAMES[abbr]]
        }
    for abbr, col in kanton_cols["single"]["cons"].items():
        rid = abbr
        cons_region_cols[rid] = col
        if rid not in regions_meta:
            regions_meta[rid] = {
                "cantons": [abbr],
                "bfs_ids": [KANTON_BFS[abbr]],
                "names": [KANTON_NAMES[abbr]]
            }

    # Groups
    for group_tuple, col in kanton_cols["grouped"]["prod"].items():
        rid = "+".join(group_tuple)
        prod_region_cols[rid] = col
        regions_meta[rid] = {
            "cantons": list(group_tuple),
            "bfs_ids": [KANTON_BFS[a] for a in group_tuple if a in KANTON_BFS],
            "names": [KANTON_NAMES[a] for a in group_tuple if a in KANTON_NAMES]
        }
    for group_tuple, col in kanton_cols["grouped"]["cons"].items():
        rid = "+".join(group_tuple)
        cons_region_cols[rid] = col
        if rid not in regions_meta:
            regions_meta[rid] = {
                "cantons": list(group_tuple),
                "bfs_ids": [KANTON_BFS[a] for a in group_tuple if a in KANTON_BFS],
                "names": [KANTON_NAMES[a] for a in group_tuple if a in KANTON_NAMES]
            }

    all_region_ids = sorted(regions_meta.keys())
    print(f"    → {len(all_region_ids)} Regionen total")

    # --- Aggregieren ---
    work_df = df[["timestamp"]].copy()
    for rid, col in prod_region_cols.items():
        work_df[f"prod_{rid}"] = df[col]
    for rid, col in cons_region_cols.items():
        work_df[f"cons_{rid}"] = df[col]

    if aggregate != "15min":
        print(f"    Aggregiere auf {aggregate} ...")
        work_df = work_df.set_index("timestamp").resample(aggregate).sum().reset_index()
        print(f"    → {len(work_df)} aggregierte Zeilen")

    # --- JSON bauen ---
    data = []
    for _, row in work_df.iterrows():
        entry = {"t": row["timestamp"].isoformat()}

        prod_entry = {}
        for rid in all_region_ids:
            key = f"prod_{rid}"
            if key in work_df.columns:
                val = row[key]
                prod_entry[rid] = round(float(val)) if pd.notna(val) else None
        if prod_entry:
            entry["prod"] = prod_entry

        cons_entry = {}
        for rid in all_region_ids:
            key = f"cons_{rid}"
            if key in work_df.columns:
                val = row[key]
                cons_entry[rid] = round(float(val)) if pd.notna(val) else None
        if cons_entry:
            entry["cons"] = cons_entry

        data.append(entry)

    # Abdeckung prüfen: welche Kantone sind vertreten?
    covered_cantons = set()
    for meta in regions_meta.values():
        covered_cantons.update(meta["cantons"])
    missing = set(KANTON_BFS.keys()) - covered_cantons

    output = {
        "meta": {
            "dataset": "swissgrid-kanton",
            "resolution": aggregate,
            "source_resolution": "15min",
            "unit": "kWh",
            "year": year,
            "records": len(data),
            "regions_count": len(all_region_ids),
            "cantons_covered": len(covered_cantons),
            "cantons_missing": sorted(missing) if missing else [],
            "source": "Swissgrid EnergieUebersichtCH",
            "note": (
                "Swissgrid gruppiert einige Kantone (z.B. SH+ZH, BE+JU). "
                "Gruppen-Keys verwenden '+' als Separator. "
                "Für Choropleth-Mapping: alle Kantone einer Gruppe erhalten den gleichen Wert, "
                "oder proportionale Aufteilung nach BFE-Jahresverbrauch."
            )
        },
        "regions": regions_meta,
        "data": data
    }

    print(f"    → {len(data)} Records, {len(covered_cantons)}/26 Kantone abgedeckt")
    if missing:
        print(f"    ⚠ Nicht abgedeckt: {sorted(missing)}")
    return output


# ---------------------------------------------------------------------------
# Transform 3: Cross-Border
# ---------------------------------------------------------------------------

def transform_cross_border(df: pd.DataFrame, year: int) -> dict:
    """
    Grenzüberschreitende Stromflüsse.

    Output-Schema:
    {
      "meta": { ... },
      "data": [
        {
          "t": "2024-01-01T00:15:00",
          "AT": { "import": 12345, "export": 6789 },
          "DE": { ... },
          "FR": { ... },
          "IT": { ... },
          "total_import": ...,
          "total_export": ...,
          "net": ...
        }
      ]
    }
    """
    print("\n  [Cross-Border] Spalten-Matching ...")

    col_map = {}
    for key, substring in CROSS_BORDER_COLS.items():
        matched = find_col(df, substring)
        if matched:
            col_map[key] = matched
            print(f"    ✓ {key:12s} → gefunden")
        else:
            print(f"    ✗ {key:12s} → NICHT GEFUNDEN")

    if not col_map:
        print("    ⚠ Keine Cross-Border-Spalten gefunden")
        return {}

    # Gruppiere nach Land
    neighbors = {}
    for key, orig_col in col_map.items():
        # key format: "ch_to_at" oder "at_to_ch"
        parts = key.split("_to_")
        if len(parts) == 2:
            src, dst = parts
            country = dst.upper() if src == "ch" else src.upper()
            direction = "export" if src == "ch" else "import"
            neighbors.setdefault(country, {})[direction] = orig_col

    data = []
    for _, row in df.iterrows():
        entry = {"t": row["timestamp"].isoformat()}
        total_imp = 0
        total_exp = 0

        for country in sorted(neighbors.keys()):
            cols = neighbors[country]
            imp_val = float(row[cols["import"]]) if "import" in cols and pd.notna(row[cols["import"]]) else 0
            exp_val = float(row[cols["export"]]) if "export" in cols and pd.notna(row[cols["export"]]) else 0

            entry[country] = {
                "import": round(imp_val),
                "export": round(exp_val)
            }
            total_imp += imp_val
            total_exp += exp_val

        entry["total_import"] = round(total_imp)
        entry["total_export"] = round(total_exp)
        entry["net"] = round(total_exp - total_imp)  # positiv = Netto-Export

        data.append(entry)

    output = {
        "meta": {
            "dataset": "swissgrid-cross-border",
            "resolution": "15min",
            "unit": "kWh",
            "year": year,
            "records": len(data),
            "neighbors": sorted(neighbors.keys()),
            "source": "Swissgrid EnergieUebersichtCH",
            "note": "Verbundaustausch über alle Übertragungsleitungen pro Grenze."
        },
        "data": data
    }

    print(f"    → {len(data)} Records, Länder: {sorted(neighbors.keys())}")
    return output


# ---------------------------------------------------------------------------
# Dateigrössen-Report
# ---------------------------------------------------------------------------

def report_size(filepath: Path) -> str:
    size = filepath.stat().st_size
    if size > 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MB"
    return f"{size / 1024:.0f} KB"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Transform Swissgrid XLSX → JSON (v2)")
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument("--years", type=str, help="Komma-separiert: 2020,2021,2022")
    parser.add_argument("--file", type=str, help="Lokale XLSX statt Download")
    parser.add_argument("--out-dir", type=str, default="src/data")
    parser.add_argument("--kanton-agg", type=str, default="1h",
                        help="Kanton-Aggregation: 15min, 1h, 1D (default: 1h)")
    parser.add_argument("--skip-national", action="store_true")
    parser.add_argument("--skip-kanton", action="store_true")
    parser.add_argument("--skip-border", action="store_true")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    years = [args.year]
    if args.years:
        years = [int(y.strip()) for y in args.years.split(",")]

    all_outputs = []

    for year in years:
        print(f"\n{'#' * 70}")
        print(f"# YEAR: {year}")
        print(f"{'#' * 70}")

        # Download
        if args.file:
            filepath = Path(args.file)
        else:
            try:
                filepath = download_xlsx(year)
            except (FileNotFoundError, Exception) as e:
                print(f"  ✗ Download fehlgeschlagen: {e}")
                print(f"  → Überspringe {year}")
                continue

        # Sheet einlesen (einmal für alle Transforms)
        try:
            df = read_zeitreihen(filepath)
        except Exception as e:
            print(f"  ✗ Fehler beim Lesen: {e}")
            continue

        # --- 1) National ---
        if not args.skip_national:
            print(f"\n{'─' * 40}")
            print(f"[1/3] National")
            print(f"{'─' * 40}")
            try:
                result = transform_national(df, year)
                outfile = out_dir / f"swissgrid-national-15min-{year}.json"
                with open(outfile, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False)
                print(f"  ✓ {outfile} ({report_size(outfile)})")
                all_outputs.append(outfile)
            except Exception as e:
                print(f"  ✗ Fehler: {e}")

        # --- 2) Kanton ---
        if not args.skip_kanton:
            print(f"\n{'─' * 40}")
            print(f"[2/3] Kanton ({args.kanton_agg})")
            print(f"{'─' * 40}")
            try:
                result = transform_kanton(df, year, aggregate=args.kanton_agg)
                if result:
                    suffix = args.kanton_agg.replace("min", "min")
                    outfile = out_dir / f"swissgrid-kanton-{suffix}-{year}.json"
                    with open(outfile, "w", encoding="utf-8") as f:
                        json.dump(result, f, ensure_ascii=False)
                    print(f"  ✓ {outfile} ({report_size(outfile)})")
                    all_outputs.append(outfile)
            except Exception as e:
                print(f"  ✗ Fehler: {e}")

        # --- 3) Cross-Border ---
        if not args.skip_border:
            print(f"\n{'─' * 40}")
            print(f"[3/3] Cross-Border")
            print(f"{'─' * 40}")
            try:
                result = transform_cross_border(df, year)
                if result:
                    outfile = out_dir / f"swissgrid-cross-border-15min-{year}.json"
                    with open(outfile, "w", encoding="utf-8") as f:
                        json.dump(result, f, ensure_ascii=False)
                    print(f"  ✓ {outfile} ({report_size(outfile)})")
                    all_outputs.append(outfile)
            except Exception as e:
                print(f"  ✗ Fehler: {e}")

    # Final Report
    print(f"\n{'=' * 70}")
    print(f"FERTIG — {len(all_outputs)} Dateien erzeugt:")
    print(f"{'=' * 70}")
    for f in all_outputs:
        print(f"  {f}  ({report_size(f)})")


if __name__ == "__main__":
    main()