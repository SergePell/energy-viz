"""
04_transform_ogd123.py — BFE Erneuerbare Energien (OGD123) aufbereiten

Zweck:
    Die Erneuerbare-Energien-Bilanz in saubere JSONs umwandeln.
    OGD123 hat mehr Detail als OGD115: Hier sind Solar, Wind, Wasserkraft-Subtypen,
    Biogas-Subtypen und Umweltwärme einzeln aufgeschlüsselt.

Quelle:
    opendata.swiss OGD123 — Energiebilanz der erneuerbaren Energien
    8855 Zeilen, 4 Spalten (Jahr, Rubrik, Energietraeger, TJ)
    Zeitraum: 1990–2024

Was das Script erzeugt:
    1. renewable_production.json  — Erneuerbare Inlandproduktion nach Technologie
    2. renewable_detail.json      — Detail: Umwandlung nach Technologie (PV, Wind, Laufwerke etc.)

Ausführen:
    cd energy-viz
    .venv\Scripts\Activate.ps1
    python pipeline/04_transform_ogd123.py
"""

import pandas as pd
import json
from pathlib import Path

# ── Pfade ──────────────────────────────────────────────────
PIPELINE_DIR = Path(__file__).parent
RAW_FILE = PIPELINE_DIR / "raw" / "ogd123_erneuerbare.csv"
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


def transform():
    """Hauptfunktion: Liest OGD123 ein und erzeugt JSON-Dateien."""

    print("=" * 60)
    print("  OGD123 — Erneuerbare Energien transformieren")
    print("=" * 60)

    # ── 1. Einlesen ────────────────────────────────────────
    print("\n1. CSV einlesen...")
    df = pd.read_csv(RAW_FILE, sep=",")
    print(f"   {df.shape[0]} Zeilen, Zeitraum {df['Jahr'].min()}–{df['Jahr'].max()}")

    # ── 2. Inlandproduktion nach Energieträger ─────────────
    # Zeigt die erneuerbaren Energiequellen der Schweiz:
    # Wasserkraft, Holz, Sonne, Wind, Biogas, Umweltwärme etc.
    print("\n── Erneuerbare Inlandproduktion ──")

    prod = df[df["Rubrik"] == "Inlandproduktion"].copy()
    print(f"   {len(prod)} Zeilen gefiltert")

    # Pivotieren: Energieträger → Spalten
    pivot = prod.pivot_table(
        index="Jahr",
        columns="Energietraeger",
        values="TJ",
        aggfunc="first"
    )

    # Spalten umbenennen
    rename_prod = {
        "Biogas": "biogas",
        "Biogene Treibstoffe": "biofuel",
        "Erneuerbare Elektrizität": "renewable_electricity",
        "Erneuerbare Fernwärme": "renewable_district_heat",
        "Erneuerbarer Müll und Industrieabfälle": "waste_renewable",
        "Erneuerbares Gas": "renewable_gas",
        "Holzenergie": "wood",
        "Sonne": "solar",
        "Umweltwärme": "ambient_heat",
        "Wasserkraft": "hydro",
        "Wind": "wind",
    }
    pivot = pivot.rename(columns=rename_prod)
    pivot = pivot.fillna(0).round(1)
    pivot = pivot.reset_index().rename(columns={"Jahr": "year"})
    pivot["year"] = pivot["year"].astype(int)

    print(f"   {len(pivot)} Jahre, {len(pivot.columns)-1} Energieträger")
    save_json(pivot.to_dict(orient="records"), "renewable_production.json")

    # ── 3. Erzeugung nach Technologie (Detail) ─────────────
    # Die interessantesten Umwandlungs-Rubriken einzeln extrahieren.
    # Diese zeigen die spezifischen Technologien: PV, Wind, Laufwerke etc.
    print("\n── Erzeugung nach Technologie (Detail) ──")

    # Nur Energieumwandlungs-Rubriken
    tech_rubriks = {
        "Energieumwandlung - Laufwerke": "hydro_run",
        "Energieumwandlung - Speicherwerke (ohne Pumpspeicherung)": "hydro_storage",
        "Energieumwandlung - Photovoltaikanlagen": "solar_pv",
        "Energieumwandlung - Windenergieanlagen": "wind",
        "Energieumwandlung - Kehrichtverbrennungsanlagen": "waste_incineration",
        "Energieumwandlung - Umweltwärmenutzung": "ambient_heat",
        "Energieumwandlung - Automatische Feuerungen mit Holz (Elektrizitäts-Produktion)": "wood_electricity",
        "Energieumwandlung - Automatische Feuerungen mit Holz (Fernwärme-Produktion)": "wood_district_heat",
        "Energieumwandlung - Biogasanlagen Landwirtschaft": "biogas_agriculture",
        "Energieumwandlung - Biogasanlagen Gewerbe/Industrie": "biogas_industry",
        "Energieumwandlung - Klärgasanlagen": "biogas_sewage",
        "Energieumwandlung - Deponiegasanlagen": "biogas_landfill",
        "Energieumwandlung - Feuerungen für erneuerbare Abfälle": "waste_renewable_fire",
    }

    # Für jede Technologie: Summe aller Energieträger pro Jahr (= Gesamt-Output)
    tech_frames = []
    for rubrik, key in tech_rubriks.items():
        subset = df[df["Rubrik"] == rubrik]
        if subset.empty:
            continue
        yearly = subset.groupby("Jahr")["TJ"].sum().reset_index()
        yearly.columns = ["year", key]
        yearly[key] = yearly[key].round(1)
        tech_frames.append(yearly)

    if tech_frames:
        # Alle Technologien zusammenführen
        tech_data = tech_frames[0]
        for frame in tech_frames[1:]:
            tech_data = pd.merge(tech_data, frame, on="year", how="outer")

        tech_data = tech_data.fillna(0)
        tech_data["year"] = tech_data["year"].astype(int)
        tech_data = tech_data.sort_values("year").reset_index(drop=True)

        print(f"   {len(tech_data)} Jahre, {len(tech_data.columns)-1} Technologien")
        save_json(tech_data.to_dict(orient="records"), "renewable_detail.json")
    else:
        print("   ⚠ Keine Technologie-Daten gefunden")

    # ── 4. Endverbrauch Erneuerbare ────────────────────────
    print("\n── Endverbrauch Erneuerbare ──")

    end = df[df["Rubrik"] == "Endverbrauch - Total"].copy()
    if not end.empty:
        pivot_end = end.pivot_table(
            index="Jahr",
            columns="Energietraeger",
            values="TJ",
            aggfunc="first"
        )
        pivot_end = pivot_end.rename(columns=rename_prod)
        pivot_end = pivot_end.fillna(0).round(1)
        pivot_end = pivot_end.reset_index().rename(columns={"Jahr": "year"})
        pivot_end["year"] = pivot_end["year"].astype(int)

        # Total berechnen
        numeric_cols = [c for c in pivot_end.columns if c != "year"]
        pivot_end["total"] = pivot_end[numeric_cols].sum(axis=1).round(1)

        print(f"   {len(pivot_end)} Jahre, {len(numeric_cols)} Energieträger")
        save_json(pivot_end.to_dict(orient="records"), "renewable_consumption.json")

    # ── Zusammenfassung ────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  ✓ OGD123 Transformation abgeschlossen")
    print(f"{'='*60}")
    print(f"  Erzeugte Dateien:")
    print(f"    renewable_production.json   Inlandproduktion nach Energieträger")
    print(f"    renewable_detail.json       Erzeugung nach Technologie (PV, Wind etc.)")
    print(f"    renewable_consumption.json  Endverbrauch erneuerbare Energien")
    print(f"{'='*60}")


if __name__ == "__main__":
    if not RAW_FILE.exists():
        print(f"⚠ Datei nicht gefunden: {RAW_FILE}")
        print(f"→ Bitte von opendata.swiss herunterladen (OGD123)")
    else:
        transform()