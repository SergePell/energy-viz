#!/usr/bin/env python3
"""
08_transform_ogd124.py
======================
Transformiert OGD124 (Erdölbilanz) von Long → Wide JSON.

Input:  pipeline/raw/ogd124_erdölbilanz.csv
Output: src/data/oil-balance.json

Verwendung:
    python pipeline/08_transform_ogd124.py
"""

import json
from pathlib import Path

import pandas as pd

PIPELINE_DIR = Path(__file__).parent
RAW = PIPELINE_DIR / "raw" / "ogd124_erdölbilanz.csv"
OUT = PIPELINE_DIR.parent / "src" / "data" / "oil-balance.json"

# Energieträger → kurze englische Keys
CARRIER_MAP = {
    "Benzin bleifrei": "petrol_unleaded",
    "Benzin verbleit": "petrol_leaded",
    "Diesel": "diesel",
    "Flugbenzin": "avgas",
    "Flugpetrol": "jet_fuel",
    "Heizöl extra-leicht": "heating_oil_light",
    "Heizöl mittel und schwer": "heating_oil_heavy",
    "Petrolkoks": "petcoke",
    "Rohöl": "crude_oil",
    "Übrige Erdölprodukte": "other_oil",
    "Uebrige Erdölprodukte": "other_oil",
    "Heizöl extraleicht": "heating_oil_light",
    "Nicht-energetische Produkte": "non_energy_products",
}

# Rubriken → kurze Keys
RUBRIK_MAP = {
    "Absatz Grosshandel": "wholesale",
    "Einkauf Konsumenten": "consumer_purchase",
    "Endverbrauch": "final_consumption",
    "Export": "export",
    "Import": "import",
    "Lagerbewegung Grosshandel": "stock_wholesale",
    "Lagerbewegung Konsumenten": "stock_consumer",
    "Nicht-energetischer Verbrauch": "non_energy_use",
    "Raffinerieproduktion": "refinery_production",
    "Statistische Differenz": "statistical_diff",
    "Umbuchungen": "reclassification",
    "Endverbrauch - Total": "final_consumption",
    "Eigenverbrauch der Raffinerien": "refinery_own_use",
    "Lagerveränderung Grosshandel": "stock_wholesale",
    "Lagerveränderung Konsumenten": "stock_consumer",
    "Produkteumbuchungen": "reclassification",
    "Produktion Inlandraffinerien (exkl. Verluste)": "refinery_production",
    "Energieumwandlung - konventionell-thermische Kraft-, Fernheiz- und Fernheizkraftwerke": "conversion_thermal",
}


def main():
    print("=" * 60)
    print("  DS-11 — Erdölbilanz der Schweiz (OGD124)")
    print("=" * 60)

    df = pd.read_csv(RAW)
    print(f"\n  Input: {len(df)} Zeilen (Long-Format)")
    print(f"  Zeitraum: {df['Jahr'].min()}–{df['Jahr'].max()}")
    print(f"  Rubriken: {sorted(df['Rubrik'].dropna().unique())}")
    print(f"  Energieträger: {sorted(df['Energietraeger'].dropna().unique())}")

    # --- Endverbrauch pivotieren (Hauptinteresse) ---
    end = df[df["Rubrik"] == "Endverbrauch - Total"].copy()
    print(f"\n  Endverbrauch: {len(end)} Zeilen")

    pv_end = end.pivot_table(
        index="Jahr",
        columns="Energietraeger",
        values="Tonnen",
        aggfunc="first"
    ).reset_index()
    pv_end.columns.name = None
    pv_end = pv_end.rename(columns={"Jahr": "year"})
    pv_end = pv_end.rename(columns=CARRIER_MAP)
    pv_end = pv_end.fillna(0).round(0)
    pv_end["year"] = pv_end["year"].astype(int)

    # Total berechnen
    num_cols = [c for c in pv_end.columns if c != "year"]
    pv_end["total"] = pv_end[num_cols].sum(axis=1).round(0)

    # --- Import/Export pivotieren ---
    imp = df[df["Rubrik"] == "Import"].copy()
    exp = df[df["Rubrik"] == "Export"].copy()

    pv_imp = imp.pivot_table(index="Jahr", columns="Energietraeger", values="Tonnen", aggfunc="first").reset_index()
    pv_imp.columns.name = None
    pv_imp = pv_imp.rename(columns={"Jahr": "year"}).rename(columns=CARRIER_MAP).fillna(0).round(0)

    pv_exp = exp.pivot_table(index="Jahr", columns="Energietraeger", values="Tonnen", aggfunc="first").reset_index()
    pv_exp.columns.name = None
    pv_exp = pv_exp.rename(columns={"Jahr": "year"}).rename(columns=CARRIER_MAP).fillna(0).round(0)

    # --- Alle Rubriken als kompakte Zeitreihe ---
    all_rubriks = {}
    for rubrik in df["Rubrik"].unique():
        subset = df[df["Rubrik"] == rubrik]
        yearly_total = subset.groupby("Jahr")["Tonnen"].sum().reset_index()
        yearly_total.columns = ["year", "total_tonnes"]
        yearly_total["total_tonnes"] = yearly_total["total_tonnes"].round(0)
        key = RUBRIK_MAP.get(rubrik, rubrik)
        all_rubriks[key] = yearly_total.to_dict(orient="records")

    # JSON bauen
    output = {
        "meta": {
            "dataset": "ogd124-oil-balance",
            "source": "BFE Gesamtenergiestatistik — Erdölbilanz (opendata.swiss)",
            "source_id": "ogd124@bundesamt-fur-energie-bfe",
            "resolution": "yearly",
            "unit": "Tonnen",
            "time_range": f"{df['Jahr'].min()} to {df['Jahr'].max()}",
            "records_raw": len(df),
            "carriers": {v: k for k, v in CARRIER_MAP.items() if k in df["Energietraeger"].values},
            "rubriks": {v: k for k, v in RUBRIK_MAP.items() if k in df["Rubrik"].values},
            "note": (
                "Einheit: Tonnen. Umrechnung zu TJ: produktspezifische Heizwerte nötig. "
                "OGD115 enthält dieselben Daten in TJ aggregiert als 'Erdölprodukte'."
            ),
        },
        "final_consumption": json.loads(pv_end.to_json(orient="records")),
        "import": json.loads(pv_imp.to_json(orient="records")),
        "export": json.loads(pv_exp.to_json(orient="records")),
        "rubrik_totals": all_rubriks,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False)

    size_kb = OUT.stat().st_size / 1024
    print(f"\n  Endverbrauch: {len(pv_end)} Jahre × {len(num_cols)} Produkte")
    print(f"  Import: {len(pv_imp)} Jahre")
    print(f"  Export: {len(pv_exp)} Jahre")
    print(f"  Rubrik-Summen: {len(all_rubriks)} Rubriken")
    print(f"\n  ✓ {OUT} ({size_kb:.0f} KB)")
    print("=" * 60)


if __name__ == "__main__":
    main()
