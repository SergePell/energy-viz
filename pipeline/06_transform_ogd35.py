#!/usr/bin/env python3
"""
transform_ogd35.py
==================
Transformiert OGD35 (Monatliche Elektrizitätsbilanz) → JSON.

Behandelt den Strukturbruch:
  - Vor ~2022: Thermische+Wind+PV zusammengefasst als "Erzeugung_andere_GWh"
  - Ab ~2022:  Einzeln aufgeschlüsselt, "andere" = NaN

Output: src/data/electricity-monthly.json

Verwendung:
    python pipeline/transform_ogd35.py
"""

import json
from pathlib import Path

import pandas as pd

PIPELINE_DIR = Path(__file__).parent
RAW = PIPELINE_DIR / "raw" / "ogd35_schweizerische_elektrizitaetsbilanz_monatswerte.csv"
OUT = PIPELINE_DIR.parent / "src" / "data" / "electricity-monthly.json"

RENAME = {
    "Jahr": "year",
    "Monat": "month",
    "Definitiv": "definitive",
    "Erzeugung_Laufwerk_GWh": "hydro_run",
    "Erzeugung_Speicherwerk_GWh": "hydro_storage",
    "Erzeugung_Kernkraftwerk_GWh": "nuclear",
    "Erzeugung_andere_GWh": "other_combined",
    "Erzeugung_Thermische_GWh": "thermal",
    "Erzeugung_Windkraft_GWh": "wind",
    "Erzeugung_Photovoltaik_GWh": "solar",
    "Landeserzeugung_GWh": "production_total",
    "Verbrauch_Speicherpumpen_GWh": "pump_consumption",
    "Erzeugung_netto_GWh": "production_net",
    "Einfuhr_GWh": "import",
    "Ausfuhr_GWh": "export",
    "Landesverbrauch_GWh": "consumption_national",
    "Verluste_GWh": "losses",
    "Endverbrauch_GWh": "consumption_final",
}


def main():
    print("=" * 60)
    print("  OGD35 — Monatliche Elektrizitätsbilanz")
    print("=" * 60)

    df = pd.read_csv(RAW)
    df = df.rename(columns=RENAME)
    print(f"\n  Input: {len(df)} Monate ({df['year'].min()}–{df['year'].max()})")

    # Datumsfeld erzeugen (YYYY-MM-01)
    df["date"] = pd.to_datetime(
        df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2) + "-01"
    ).dt.strftime("%Y-%m-%d")

    # Berechnete Felder
    df["hydro_total"] = df["hydro_run"].fillna(0) + df["hydro_storage"].fillna(0)
    df["trade_balance"] = df["import"].fillna(0) - df["export"].fillna(0)

    # Spaltenreihenfolge
    cols = [
        "date", "year", "month", "definitive",
        "hydro_run", "hydro_storage", "hydro_total",
        "nuclear",
        "solar", "wind", "thermal", "other_combined",
        "production_total", "pump_consumption", "production_net",
        "import", "export", "trade_balance",
        "consumption_national", "losses", "consumption_final",
    ]
    df = df[cols]

    # NaN → None für JSON
    df = df.where(pd.notna(df), None)

    # Strukturbruch dokumentieren
    has_detail = df[df["solar"].notna()]
    has_combined = df[df["other_combined"].notna()]
    print(f"  Einzelaufschlüsselung (Solar/Wind/Therm): {has_detail['date'].min()} → {has_detail['date'].max()}")
    print(f"  Zusammengefasst (other_combined):         {has_combined['date'].min()} → {has_combined['date'].max()}")

    # JSON bauen
    output = {
        "meta": {
            "dataset": "ogd35-electricity-monthly",
            "source": "BFE Elektrizitätsstatistik (opendata.swiss)",
            "source_id": "ogd35@bundesamt-fur-energie-bfe",
            "resolution": "monthly",
            "unit": "GWh",
            "time_range": f"{df['date'].iloc[0]} to {df['date'].iloc[-1]}",
            "records": len(df),
            "fields": {
                "hydro_run": "Laufwasserkraftwerke",
                "hydro_storage": "Speicherwasserkraftwerke",
                "hydro_total": "Wasserkraft total (berechnet)",
                "nuclear": "Kernkraftwerke",
                "solar": "Photovoltaik (ab ~2022, vorher in other_combined)",
                "wind": "Windenergie (ab ~2022, vorher in other_combined)",
                "thermal": "Thermische KW (ab ~2022, vorher in other_combined)",
                "other_combined": "Thermische+Wind+PV zusammengefasst (vor ~2022)",
                "production_total": "Landeserzeugung (brutto)",
                "pump_consumption": "Verbrauch Speicherpumpen",
                "production_net": "Nettoerzeugung (brutto - Pumpen)",
                "import": "Einfuhr",
                "export": "Ausfuhr",
                "trade_balance": "Import - Export (positiv = Netto-Import)",
                "consumption_national": "Landesverbrauch",
                "losses": "Übertragungs- und Verteilungsverluste",
                "consumption_final": "Endverbrauch",
                "definitive": "1 = definitiv, 0 = provisorisch",
            },
            "note": (
                "Strukturbruch: Vor ~2022 sind Thermische, Wind und PV in 'other_combined' "
                "zusammengefasst. Ab ~2022 einzeln aufgeschlüsselt. "
                "Provisorische Werte (definitive=0) können sich noch ändern."
            ),
        },
        "data": json.loads(df.to_json(orient="records")),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False)

    size_kb = OUT.stat().st_size / 1024
    print(f"\n  ✓ {OUT} ({size_kb:.0f} KB)")
    print("=" * 60)


if __name__ == "__main__":
    main()
