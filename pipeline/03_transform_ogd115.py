"""
03_transform_ogd115.py — BFE Gesamtenergiestatistik (OGD115) aufbereiten

Zweck:
    Die Energiebilanz der Schweiz (Long-Format) in mehrere saubere
    JSON-Dateien umwandeln — eine pro Perspektive.

Quelle:
    opendata.swiss OGD115 — Energiebilanz der Schweiz
    9405 Zeilen, 4 Spalten (Jahr, Rubrik, Energietraeger, TJ)
    Zeitraum: 1980–2024

Was das Script erzeugt:
    1. energy_mix.json       — Inlandproduktion nach Energieträger pro Jahr
    2. consumption.json      — Endverbrauch nach Sektor pro Jahr
    3. trade.json            — Import/Export nach Energieträger pro Jahr
    4. overview.json         — Bruttoverbrauch nach Energieträger pro Jahr

Ausführen:
    cd energy-viz
    .venv\\Scripts\\Activate.ps1
    python pipeline/03_transform_ogd115.py
"""

import pandas as pd
import json
from pathlib import Path

# ── Pfade ──────────────────────────────────────────────────
PIPELINE_DIR = Path(__file__).parent
RAW_FILE = PIPELINE_DIR / "raw" / "ogd115_energiebilanz.csv"
OUTPUT_DIR = PIPELINE_DIR / "output"
SRC_DATA_DIR = PIPELINE_DIR.parent / "src" / "data"


def save_json(data, filename):
    """Speichert JSON in pipeline/output/ und src/data/."""
    for target_dir in [OUTPUT_DIR, SRC_DATA_DIR]:
        target_dir.mkdir(parents=True, exist_ok=True)
        filepath = target_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"   ✓ {filename} ({len(data)} Datensätze)")


def pivot_rubrik(df, rubrik_name, short_name):
    """
    Filtert eine Rubrik und pivotiert von Long zu Wide Format.

    Long (Rohdaten):
        Jahr | Rubrik          | Energietraeger | TJ
        2024 | Inlandproduktion| Wasserkraft    | 131000

    Wide (Ergebnis):
        year | wasserkraft | solar | wind | ...
        2024 | 131000      | 21460 | 616  | ...

    Parameter:
        df:           DataFrame mit allen Daten
        rubrik_name:  Exakter Name der Rubrik (z.B. "Inlandproduktion")
        short_name:   Kurzname für Logging
    """
    print(f"\n── {short_name} ({rubrik_name}) ──")

    # Filtern
    subset = df[df["Rubrik"] == rubrik_name].copy()
    if subset.empty:
        print(f"   ⚠ Keine Daten für Rubrik '{rubrik_name}'")
        return None

    print(f"   {len(subset)} Zeilen gefiltert")

    # Pivotieren: Zeilen (Energieträger) → Spalten
    # aggfunc="first" weil es pro Jahr+Energieträger nur einen Wert gibt
    pivot = subset.pivot_table(
        index="Jahr",
        columns="Energietraeger",
        values="TJ",
        aggfunc="first"
    )

    # Spalten umbenennen: Deutsch → kurze englische Keys
    rename_map = {
        "Elektrizität": "electricity",
        "Erdölprodukte": "oil_products",
        "Fernwärme": "district_heat",
        "Gas": "gas",
        "Holzenergie": "wood",
        "Kernbrennstoffe": "nuclear_fuel",
        "Kohle": "coal",
        "Müll und Industrieabfälle": "waste",
        "Rohöl": "crude_oil",
        "Uebrige erneuerbare Energien": "other_renewable",
        "Wasserkraft": "hydro",
    }
    pivot = pivot.rename(columns=rename_map)

    # NaN → 0, runden
    pivot = pivot.fillna(0).round(1)

    # Index (Jahr) als Spalte
    pivot = pivot.reset_index().rename(columns={"Jahr": "year"})
    pivot["year"] = pivot["year"].astype(int)

    print(f"   {len(pivot)} Jahre, {len(pivot.columns)-1} Energieträger")

    return pivot


def transform():
    """Hauptfunktion: Liest OGD115 ein und erzeugt 4 JSON-Dateien."""

    print("=" * 60)
    print("  OGD115 — Gesamtenergiestatistik transformieren")
    print("=" * 60)

    # ── 1. Einlesen ────────────────────────────────────────
    print("\n1. CSV einlesen...")
    df = pd.read_csv(RAW_FILE, sep=",")
    print(f"   {df.shape[0]} Zeilen, Zeitraum {df['Jahr'].min()}–{df['Jahr'].max()}")

    # ── 2. Inlandproduktion (Energiemix) ───────────────────
    # Zeigt woher die Energie in der Schweiz kommt:
    # Wasserkraft, Kernbrennstoffe, Holz, Solar/Wind (in "Übrige erneuerbare")
    mix = pivot_rubrik(df, "Inlandproduktion", "Energiemix")
    if mix is not None:
        save_json(mix.to_dict(orient="records"), "energy_mix.json")

    # ── 3. Endverbrauch nach Sektor ────────────────────────
    # Zeigt wer die Energie verbraucht:
    # Haushalte, Industrie, Dienstleistungen, Verkehr
    print("\n── Endverbrauch nach Sektor ──")

    # Alle Endverbrauchs-Rubriken sammeln
    sector_rubriks = {
        "Endverbrauch - Haushalte": "households",
        "Endverbrauch - Industrie": "industry",
        "Endverbrauch - Dienstleistungen": "services",
        "Endverbrauch - Verkehr": "transport",
        "Endverbrauch - Statistische Differenz inkl. Landwirtschaft": "other",
        "Endverbrauch - Total": "total",
    }

    # Für jeden Sektor: Summe aller Energieträger pro Jahr
    sector_data = None
    for rubrik, key in sector_rubriks.items():
        subset = df[df["Rubrik"] == rubrik]
        # Summiere alle Energieträger pro Jahr
        yearly = subset.groupby("Jahr")["TJ"].sum().reset_index()
        yearly.columns = ["year", key]
        yearly[key] = yearly[key].round(1)

        if isinstance(sector_data, pd.DataFrame):
            sector_data = pd.merge(sector_data, yearly, on="year", how="outer")
        else:
            sector_data = yearly

    sector_data = sector_data.fillna(0)
    sector_data["year"] = sector_data["year"].astype(int)
    print(f"   {len(sector_data)} Jahre, {len(sector_rubriks)} Sektoren")
    save_json(sector_data.to_dict(orient="records"), "consumption_sectors.json")

    # ── 4. Import/Export ───────────────────────────────────
    # Zeigt den Energiehandel mit dem Ausland
    imp = pivot_rubrik(df, "Import", "Import")
    exp = pivot_rubrik(df, "Export", "Export")

    if imp is not None and exp is not None:
        # Zusammenführen: Import und Export pro Energieträger
        trade_records = []
        for year in sorted(set(imp["year"]) | set(exp["year"])):
            row = {"year": int(year)}

            imp_row = imp[imp["year"] == year]
            exp_row = exp[exp["year"] == year]

            for col in imp.columns:
                if col == "year":
                    continue
                imp_val = float(imp_row[col].values[0]) if len(imp_row) > 0 and col in imp_row.columns else 0
                exp_val = float(exp_row[col].values[0]) if len(exp_row) > 0 and col in exp_row.columns else 0
                row[f"{col}_import"] = round(imp_val, 1)
                row[f"{col}_export"] = round(exp_val, 1)
                row[f"{col}_balance"] = round(imp_val - exp_val, 1)

            trade_records.append(row)

        save_json(trade_records, "trade.json")

    # ── 5. Bruttoverbrauch (Überblick) ─────────────────────
    # Gesamtbild: Wie viel Energie wird insgesamt verbraucht?
    overview = pivot_rubrik(df, "Bruttoverbrauch", "Bruttoverbrauch")
    if overview is not None:
        save_json(overview.to_dict(orient="records"), "overview.json")

    # ── Zusammenfassung ────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  ✓ OGD115 Transformation abgeschlossen")
    print(f"{'='*60}")
    print(f"  Erzeugte Dateien:")
    print(f"    energy_mix.json          Inlandproduktion nach Energieträger")
    print(f"    consumption_sectors.json  Endverbrauch nach Sektor")
    print(f"    trade.json               Import/Export nach Energieträger")
    print(f"    overview.json            Bruttoverbrauch nach Energieträger")
    print(f"{'='*60}")


if __name__ == "__main__":
    if not RAW_FILE.exists():
        print(f"⚠ Datei nicht gefunden: {RAW_FILE}")
        print(f"→ Bitte von opendata.swiss herunterladen (OGD115)")
    else:
        transform()