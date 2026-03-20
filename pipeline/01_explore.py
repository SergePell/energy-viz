"""
01_explore.py - BFE Gesamtenergiestatistik erkunden

Zweck: Aufbau des CSV verstehen, vor der Verarbeitung.
Quelle:
    opendata.swiss — Bundesamt für Energie (BFE)
    OGD115: Energiebilanz der Schweiz
    OGD32:  Elektrizitätsbilanz Jahreswerte
    OGD123: Energiebilanz der erneuerbaren Energien
"""
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent / "raw"

FILES = {
    "Energiebilanz (OGD115)": RAW_DIR / "ogd115_energiebilanz.csv",
    "Elektrizitätsbilanz (OGD32)": RAW_DIR / "ogd32_elektrizitaetsbilanz.csv",
    "Erneuerbare Energien (OGD123)": RAW_DIR / "ogd123_erneuerbare.csv",
}

def detect_separator(filepath):
    """
    Automatische Erkennung von CSV Trennzeichen
    """
    with open(filepath, "r", encoding="utf-8") as f:
        first_line = f.readline()

    counts = {
        ",": first_line.count(","),
        ";": first_line.count(";"),
        "\t": first_line.count("\t"),
    }
    # Das Trennzeichen das am häufigsten vorkommt
    return max(counts, key=counts.get)

def explore_file(name, filepath):
    """
    Struktur CSV
    """
    print(f"\n {'=' * 70}")
    print(f"\n {name}")
    print(f"\n {filepath}")
    print(f"\n {'=' * 70}")

    if not filepath.exists():
        print(f"\n {filepath} nicht gefund!")
        return None

    sep = detect_separator(filepath)
    sep_name = {",": "Komma", ";": "Semikolon", "\t": "Tab"}[sep]
    print(f"\n Trennzeichen: {sep_name}")

    try:
        df = pd.read_csv(filepath, sep=sep, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, sep=sep, encoding="latin-1")
        print("Encoding: latin-1 (statt utf-8)")

    print(f"Zeilen: {df.shape[0]}")
    print(f"Zeilen: {df.shape[1]}")

    print(f"\n {df.head()}")
    print(f"\n {df.tail()}")

    for col in df.columns:
        dtype = str(df[col].dtype)
        nunique = df[col].nunique()

        sample_values = df[col].dropna()
        if len(sample_values) > 0:
            sample = str(sample_values.iloc[0])[:30]
        else:
            sample = "(alles leer)"

        print(f"  {col:<40} {dtype:<10} {nunique:>7}   {sample}")


    for col in df.columns:
        col_lower = col.lower().strip()
        if col_lower in ["jahr", "year", "date", "jahr / année"]:
            print(f"\n Zeitraum: {df[col].min()} bis {df[col].max()}")

    print(f"\n  Vorschau (erste 5 Zeilen):")
    print(f"  {'-' * 70}")
    preview = df.head(5).to_string(index=False)
    for line in preview.split("\n"):
        print(f"  {line}")

    print(f"\n  Letzte 3 Zeilen:")
    print(f"  {'-' * 70}")
    preview_tail = df.tail(3).to_string(index=False)
    for line in preview_tail.split("\n"):
        print(f"  {line}")

    return df

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("BFE Daten-Exploration")
    print("Suche Dateien in:", RAW_DIR)
    print("=" * 70)

    results = {}
    for name, filepath in FILES.items():
        df = explore_file(name, filepath)
        if df is not None:
            results[name] = df

    print(f"\n\n{'=' * 70}")
    print("Zusammenfassung")
    print(f"{'=' * 70}")
    print(f"Gefundene Dateien: {len(results)} von {len(FILES)}")
    for name, df in results.items():
        print(f"    ✓ {name}: {df.shape[0]} Zeilen × {df.shape[1]} Spalten")

    if len(results) < len(FILES):
        missing = set(FILES.keys()) - set(results.keys())
        for name in missing:
            print(f"    ✗ {name}: nicht gefunden")

    print(f"{'=' * 70}\n")

