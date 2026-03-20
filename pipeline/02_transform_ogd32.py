"""
02_transform_ogd32.py — BFE Elektrizitätsbilanz (OGD32) aufbereiten

Zweck:
    Die Elektrizitätsbilanz CSV in ein sauberes JSON umwandeln,
    das React direkt importieren kann.

Quelle:
    opendata.swiss OGD32 — Schweizerische Elektrizitätsbilanz Jahreswerte
    65 Zeilen (1960–2024), 18 Spalten, Werte in GWh

Was das Script macht:
    1. CSV einlesen
    2. Spalten umbenennen (kurze, englische Keys für JavaScript)
    3. NaN-Werte durch 0 ersetzen (fehlende Daten = nicht erhoben)
    4. Berechnete Felder ergänzen (Hydro total, Erneuerbare total, etc.)
    5. Als JSON in pipeline/output/ und src/data/ speichern

Ausführen:
    cd energy-viz
    .venv\Scripts\Activate.ps1
    python pipeline/02_transform_ogd32.py
"""

import pandas as pd
import json
from pathlib import Path

# ── Pfade ──────────────────────────────────────────────────
PIPELINE_DIR = Path(__file__).parent
RAW_FILE = PIPELINE_DIR / "raw" / "ogd32_elektrizitaetsbilanz.csv"
OUTPUT_JSON = PIPELINE_DIR / "output" / "electricity.json"

# Auch direkt in src/data/ speichern, damit React es importieren kann
SRC_DATA_DIR = PIPELINE_DIR.parent / "src" / "data"


def transform():
    """
    Liest die BFE Elektrizitätsbilanz CSV ein und erzeugt ein
    sauberes JSON für die Visualisierung.
    """

    # ── 1. CSV einlesen ────────────────────────────────────
    print("1. Lese CSV ein...")
    df = pd.read_csv(RAW_FILE, sep=",")
    print(f"   {df.shape[0]} Zeilen × {df.shape[1]} Spalten geladen")

    # ── 2. Spalten umbenennen ──────────────────────────────
    # Kurze, englische Keys — einfacher in JavaScript zu nutzen
    # Originalnamen sind lang und auf Deutsch
    print("2. Spalten umbenennen...")

    rename_map = {
        "Jahr": "year",
        "Erzeugung_laufwerk_GWh": "hydro_run",        # Laufwasserkraftwerke
        "Erzeugung_speicherwerk_GWh": "hydro_storage", # Speicherwasserkraftwerke
        "Erzeugung_kernkraftwerk_GWh": "nuclear",      # Kernkraftwerke
        "Erzeugung_andere_total_GWh": "other_total",   # Andere Erzeugung total
        "Erzeugung_andere_fossil_GWh": "other_fossil",  # Fossile Kraftwerke
        "Erzeugung_andere_erneuerbare_abfaelle_GWh": "waste_renewable",  # Erneuerbare Abfälle
        "Erzeugung_holz_GWh": "wood",                  # Holzenergie
        "Erzeugung_biogas_GWh": "biogas",              # Biogas
        "Erzeugung_photovoltaik_GWh": "solar",         # Photovoltaik
        "Erzeugung_wind_GWh": "wind",                  # Windenergie
        "Verbrauch_speicherpumpen_GWh": "pump_consumption",  # Pumpspeicher-Verbrauch
        "Erzeugung_netto_GWh": "production_net",       # Netto-Erzeugung
        "Einfuhr_GWh": "import",                       # Strom-Import
        "Ausfuhr_GWh": "export",                       # Strom-Export
        "Landesverbrauch_GWh": "consumption_gross",     # Landesverbrauch
        "Verluste_GWh": "losses",                       # Netz-Verluste
        "Endverbrauch_GWh": "consumption_final",        # Endverbrauch
    }

    df = df.rename(columns=rename_map)

    # Prüfen ob alle Spalten umbenannt wurden
    unknown = [c for c in df.columns if c not in rename_map.values()]
    if unknown:
        print(f"   ⚠ Unbekannte Spalten: {unknown}")
    else:
        print(f"   ✓ Alle {len(rename_map)} Spalten umbenannt")

    # ── 3. NaN durch 0 ersetzen ────────────────────────────
    # Vor ~1970 gibt es keine Daten für Solar, Wind, Kernkraft etc.
    # Das bedeutet nicht 0 Produktion, sondern "nicht erhoben".
    # Für die Visualisierung setzen wir es auf 0 — in den Tooltips
    # kann man das als "keine Daten" kennzeichnen.
    print("3. Fehlende Werte (NaN) durch 0 ersetzen...")
    nan_count = df.isna().sum().sum()
    df = df.fillna(0)
    print(f"   ✓ {nan_count} NaN-Werte ersetzt")

    # ── 4. Berechnete Felder ergänzen ──────────────────────
    print("4. Berechnete Felder ergänzen...")

    # Wasserkraft total = Laufwerke + Speicherwerke
    df["hydro_total"] = df["hydro_run"] + df["hydro_storage"]

    # Erneuerbare total = Hydro + Solar + Wind + Holz + Biogas + Abfälle
    df["renewable_total"] = (
        df["hydro_total"]
        + df["solar"]
        + df["wind"]
        + df["wood"]
        + df["biogas"]
        + df["waste_renewable"]
    )

    # Anteil Erneuerbare am Endverbrauch (%)
    df["renewable_pct"] = (
        (df["renewable_total"] / df["consumption_final"] * 100)
        .round(1)
        .clip(lower=0)  # Keine negativen Prozente
    )

    # Import-Export-Saldo (positiv = Netto-Import, negativ = Netto-Export)
    df["trade_balance"] = df["import"] - df["export"]

    print(f"4 Felder ergänzt: hydro_total, renewable_total, renewable_pct, trade_balance")

    # ── 5. Datentypen bereinigen ───────────────────────────
    # year als int, alles andere als float mit max 1 Dezimalstelle
    print("5. Datentypen bereinigen...")
    df["year"] = df["year"].astype(int)

    # Alle numerischen Spalten auf 1 Dezimalstelle runden
    numeric_cols = [c for c in df.columns if c != "year"]
    df[numeric_cols] = df[numeric_cols].round(1)

    print(f"   ✓ {len(numeric_cols)} Spalten gerundet")

    # ── 6. Als JSON speichern ──────────────────────────────
    print("6. JSON exportieren...")

    # In eine Liste von Dictionaries umwandeln
    # orient="records" → [{year: 1960, solar: 0, ...}, {year: 1961, ...}]
    records = df.to_dict(orient="records")

    # pipeline/output/ — Archiv-Kopie
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"   ✓ {OUTPUT_JSON}")
    print(f"     {len(records)} Datensätze, {OUTPUT_JSON.stat().st_size:,} Bytes")

    # src/data/ — für React-Import
    SRC_DATA_DIR.mkdir(parents=True, exist_ok=True)
    src_file = SRC_DATA_DIR / "electricity.json"
    with open(src_file, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"   ✓ {src_file}")

    # ── 7. Zusammenfassung ─────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  ✓ Transformation abgeschlossen")
    print(f"{'='*60}")
    print(f"Zeitraum:        {df['year'].min()} – {df['year'].max()}")
    print(f"Datensätze:      {len(records)}")
    print(f"Spalten:         {len(df.columns)}")
    print(f"Spalten-Liste:")
    for col in df.columns:
        # Letzten Wert (2024) als Beispiel zeigen
        val = df[df["year"] == df["year"].max()][col].values[0]
        print(f"    {col:<25} 2024: {val}")

    print(f"\nJSON gespeichert in:")
    print(f"pipeline/output/electricity.json (Archiv)")
    print(f"src/data/electricity.json (React-Import)")
    print(f"\n In React nutzen:")
    print(f"import data from'./data/electricity.json'")
    print(f"{'='*60}")


# ── Hauptprogramm ──────────────────────────────────────────
if __name__ == "__main__":
    if not RAW_FILE.exists():
        print(f"Datei nicht gefunden: {RAW_FILE}")
        print(f"Bitte zuerst von opendata.swiss herunterladen")
    else:
        transform()