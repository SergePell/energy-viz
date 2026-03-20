#!/usr/bin/env python3
"""
explore_swissgrid.py
====================
Explorative Analyse der Swissgrid EnergieUebersichtCH XLSX-Dateien.
Gibt für jedes Sheet: Shape, Columns, Dtypes, Head, Nulls, Statistiken aus.

Verwendung:
    python explore_swissgrid.py                          # Default: 2024
    python explore_swissgrid.py --year 2023
    python explore_swissgrid.py --file path/to/local.xlsx
"""

import argparse
import sys
from pathlib import Path

import pandas as pd
import requests

# ---------------------------------------------------------------------------
# 1) Download
# ---------------------------------------------------------------------------

BASE_URL = "https://www.swissgrid.ch/dam/dataimport/energy-statistic"


def download_xlsx(year: int, target_dir: Path = Path("raw")) -> Path:
    """Lade EnergieUebersichtCH-{year}.xlsx herunter."""
    target_dir.mkdir(parents=True, exist_ok=True)
    filename = f"EnergieUebersichtCH-{year}.xlsx"
    filepath = target_dir / filename

    if filepath.exists():
        print(f"✓ Datei existiert bereits: {filepath}")
        return filepath

    url = f"{BASE_URL}/{filename}"
    print(f"⬇ Downloading {url} ...")

    resp = requests.get(url, timeout=60)
    resp.raise_for_status()

    filepath.write_bytes(resp.content)
    size_mb = len(resp.content) / (1024 * 1024)
    print(f"✓ Gespeichert: {filepath} ({size_mb:.1f} MB)")
    return filepath


# ---------------------------------------------------------------------------
# 2) Explore
# ---------------------------------------------------------------------------

def explore_sheet(df: pd.DataFrame, sheet_name: str) -> dict:
    """Analysiere ein einzelnes Sheet und gib Summary zurück."""
    summary = {
        "sheet": sheet_name,
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "nulls": df.isnull().sum().to_dict(),
        "null_pct": (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
    }

    # Zeitstempel-Spalte erkennen
    time_cols = [c for c in df.columns if any(
        kw in str(c).lower() for kw in ["datum", "date", "time", "zeit", "timestamp"]
    )]

    if time_cols:
        tc = time_cols[0]
        summary["time_col"] = tc
        summary["time_min"] = str(df[tc].min())
        summary["time_max"] = str(df[tc].max())

        # Zeitintervall prüfen
        if pd.api.types.is_datetime64_any_dtype(df[tc]):
            diffs = df[tc].diff().dropna()
            if len(diffs) > 0:
                summary["interval_median"] = str(diffs.median())
                summary["interval_unique"] = diffs.nunique()

    # Numerische Spalten: Statistiken
    num_cols = df.select_dtypes(include="number").columns.tolist()
    if num_cols:
        summary["numeric_stats"] = df[num_cols].describe().round(2).to_dict()

    return summary


def explore_xlsx(filepath: Path) -> list[dict]:
    """Alle Sheets einer XLSX-Datei explorieren."""
    print(f"\n{'=' * 70}")
    print(f"EXPLORING: {filepath.name}")
    print(f"{'=' * 70}")

    # Alle Sheet-Namen lesen
    xl = pd.ExcelFile(filepath)
    print(f"\nSheets gefunden: {len(xl.sheet_names)}")
    for i, name in enumerate(xl.sheet_names):
        print(f"  [{i}] {name}")

    results = []

    for sheet_name in xl.sheet_names:
        print(f"\n{'─' * 50}")
        print(f"Sheet: {sheet_name}")
        print(f"{'─' * 50}")

        try:
            # Erste Zeilen inspizieren um Header-Zeile zu finden
            df_raw = pd.read_excel(filepath, sheet_name=sheet_name, header=None, nrows=10)

            # Heuristik: Header-Zeile finden (erste Zeile mit vielen String-Werten)
            header_row = 0
            for idx, row in df_raw.iterrows():
                str_count = sum(1 for v in row if isinstance(v, str) and len(str(v)) > 2)
                if str_count >= 3:
                    header_row = idx
                    break

            # Nochmal lesen mit korrektem Header
            df = pd.read_excel(
                filepath,
                sheet_name=sheet_name,
                header=header_row
            )

            # Leere Zeilen/Spalten entfernen
            df = df.dropna(how="all").dropna(axis=1, how="all")

            if df.empty:
                print(f"  ⚠ Sheet ist leer oder enthält nur Metadaten")
                results.append({"sheet": sheet_name, "shape": (0, 0), "note": "empty"})
                continue

            # Datetime-Konvertierung versuchen
            for col in df.columns:
                if any(kw in str(col).lower() for kw in ["datum", "date", "time", "zeit"]):
                    try:
                        df[col] = pd.to_datetime(df[col])
                    except Exception:
                        pass

            summary = explore_sheet(df, sheet_name)
            results.append(summary)

            # Ausgabe
            print(f"  Shape: {summary['shape']}")
            print(f"  Columns ({len(summary['columns'])}):")
            for c in summary['columns'][:15]:  # Max 15 anzeigen
                dtype = summary['dtypes'].get(c, '?')
                nulls = summary['nulls'].get(c, 0)
                null_pct = summary['null_pct'].get(c, 0)
                print(f"    · {c:40s}  {str(dtype):15s}  nulls={nulls} ({null_pct}%)")
            if len(summary['columns']) > 15:
                print(f"    ... und {len(summary['columns']) - 15} weitere Spalten")

            if "time_col" in summary:
                print(f"  Zeitraum: {summary['time_min']} → {summary['time_max']}")
                if "interval_median" in summary:
                    print(f"  Intervall (Median): {summary['interval_median']}")

            print(f"\n  Head (3 Zeilen):")
            print(df.head(3).to_string(max_cols=8))

        except Exception as e:
            print(f"  ✗ Fehler: {e}")
            results.append({"sheet": sheet_name, "error": str(e)})

    return results


# ---------------------------------------------------------------------------
# 3) Kanton-Sheet spezifische Analyse
# ---------------------------------------------------------------------------

def explore_kanton_sheet(filepath: Path):
    """Tiefenanalyse des Kantons-Sheets (wichtigste Datenquelle für Thesis)."""
    print(f"\n{'=' * 70}")
    print(f"KANTON-TIEFENANALYSE")
    print(f"{'=' * 70}")

    # Sheet-Name kann variieren
    xl = pd.ExcelFile(filepath)
    kanton_sheets = [s for s in xl.sheet_names if "kanton" in s.lower() or "canton" in s.lower()]

    if not kanton_sheets:
        # Fallback: Sheet mit vielen Spalten (26 Kantone + Timestamp)
        kanton_sheets = [s for s in xl.sheet_names if "verbrauch" in s.lower()]
        print(f"  ⚠ Kein explizites Kanton-Sheet gefunden, teste: {kanton_sheets}")

    for sheet_name in kanton_sheets:
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        df = df.dropna(how="all").dropna(axis=1, how="all")

        if df.shape[1] < 20:
            continue

        print(f"\n  Sheet: {sheet_name}")
        print(f"  Shape: {df.shape}")
        print(f"  → {df.shape[0]} Viertelstunden = ca. {df.shape[0] / 96:.0f} Tage")
        print(f"  → {df.shape[1]} Spalten (erwartet: 1 Timestamp + 26 Kantone + Aggregat)")

        # Kanton-Spalten identifizieren
        kanton_abbrevs = [
            "AG", "AI", "AR", "BE", "BL", "BS", "FR", "GE", "GL", "GR",
            "JU", "LU", "NE", "NW", "OW", "SG", "SH", "SO", "SZ", "TG",
            "TI", "UR", "VD", "VS", "ZG", "ZH"
        ]

        found_cantons = []
        for col in df.columns:
            col_str = str(col).upper().strip()
            for abbr in kanton_abbrevs:
                if abbr in col_str:
                    found_cantons.append((col, abbr))
                    break

        print(f"  Erkannte Kantons-Spalten: {len(found_cantons)}")
        for col, abbr in found_cantons:
            print(f"    · {abbr}: '{col}'")

        # Wertebereiche pro Kanton
        print(f"\n  Wertebereiche (kWh pro 15 Min):")
        for col, abbr in found_cantons[:5]:
            vals = pd.to_numeric(df[col], errors="coerce")
            print(f"    {abbr}: min={vals.min():,.0f}  max={vals.max():,.0f}  "
                  f"mean={vals.mean():,.0f}  nulls={vals.isnull().sum()}")
        if len(found_cantons) > 5:
            print(f"    ... ({len(found_cantons) - 5} weitere)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Explore Swissgrid XLSX")
    parser.add_argument("--year", type=int, default=2024, help="Jahr (default: 2024)")
    parser.add_argument("--file", type=str, help="Lokale XLSX-Datei statt Download")
    parser.add_argument("--kanton-deep", action="store_true", help="Kanton-Tiefenanalyse")
    args = parser.parse_args()

    if args.file:
        filepath = Path(args.file)
    else:
        filepath = download_xlsx(args.year)

    results = explore_xlsx(filepath)

    if args.kanton_deep:
        explore_kanton_sheet(filepath)

    # Summary
    print(f"\n{'=' * 70}")
    print(f"SUMMARY")
    print(f"{'=' * 70}")
    for r in results:
        status = "✓" if "error" not in r else "✗"
        shape = r.get("shape", "?")
        print(f"  {status} {r['sheet']:30s}  {str(shape)}")


if __name__ == "__main__":
    main()