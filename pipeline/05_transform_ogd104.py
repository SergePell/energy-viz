#!/usr/bin/env python3
"""
05_transform_ogd104.py
===================
Transformiert OGD104 (Energiedashboard Stromproduktion Swissgrid)
von Long-Format → Wide-Format JSON.

Input:  pipeline/raw/ogd104_stromproduktion_swissgrid.csv
Output: src/data/electricity-daily.json

Verwendung:
    python pipeline/05_transform_ogd104.py
"""

import json
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Pfade
# ---------------------------------------------------------------------------
PIPELINE_DIR = Path(__file__).parent
RAW = PIPELINE_DIR / "raw" / "ogd104_stromproduktion_swissgrid.csv"
OUT_DIR = PIPELINE_DIR.parent / "src" / "data"
OUT_FILE = OUT_DIR / "electricity-daily.json"
# ---------------------------------------------------------------------------
# Spalten-Mapping
# ---------------------------------------------------------------------------
RENAME = {
    "Datum": "date",
    "Flusskraft": "hydro_run",
    "Speicherkraft": "hydro_storage",
    "Kernkraft": "nuclear",
    "Photovoltaik": "solar",
    "Thermische": "thermal",
    "Wind": "wind",
}


def main():
    print("=" * 60)
    print("  OGD104 — Tägliche Stromproduktion nach Energieträger")
    print("=" * 60)

    # Einlesen
    df = pd.read_csv(RAW)
    print(f"\n  Input: {len(df)} Zeilen (Long-Format)")
    print(f"  Energieträger: {sorted(df['Energietraeger'].unique())}")

    # Pivotieren: Long → Wide
    pv = df.pivot_table(
        index="Datum",
        columns="Energietraeger",
        values="Produktion_GWh"
    ).reset_index()
    pv.columns.name = None

    # Umbenennen
    pv = pv.rename(columns=RENAME)

    # Berechnete Felder
    pv["hydro_total"] = (pv["hydro_run"].fillna(0) + pv["hydro_storage"].fillna(0)).round(1)
    pv["renewable_total"] = (
        pv["hydro_run"].fillna(0)
        + pv["hydro_storage"].fillna(0)
        + pv["solar"].fillna(0)
        + pv["wind"].fillna(0)
    ).round(1)
    pv["total"] = (
        pv["hydro_run"].fillna(0)
        + pv["hydro_storage"].fillna(0)
        + pv["nuclear"].fillna(0)
        + pv["solar"].fillna(0)
        + pv["thermal"].fillna(0)
        + pv["wind"].fillna(0)
    ).round(1)

    # NaN → null (bleibt in JSON als null)
    pv = pv.where(pd.notna(pv), None)

    print(f"  Output: {len(pv)} Tage (Wide-Format)")
    print(f"  Zeitraum: {pv['date'].iloc[0]} → {pv['date'].iloc[-1]}")
    print(f"  Spalten: {list(pv.columns)}")

    # JSON bauen
    output = {
        "meta": {
            "dataset": "ogd104-electricity-daily",
            "source": "BFE / Energiedashboard (opendata.swiss)",
            "source_id": "104@bundesamt-fur-energie-bfe",
            "resolution": "daily",
            "unit": "GWh",
            "time_range": f"{pv['date'].iloc[0]} to {pv['date'].iloc[-1]}",
            "records": len(pv),
            "fields": {
                "hydro_run": "Flusskraft (Laufwasserkraftwerke)",
                "hydro_storage": "Speicherkraft (Speicher- und Pumpspeicherkraftwerke)",
                "nuclear": "Kernkraftwerke",
                "solar": "Photovoltaik",
                "thermal": "Thermische Kraftwerke (konventionell-thermisch)",
                "wind": "Windenergie",
                "hydro_total": "Wasserkraft total (hydro_run + hydro_storage)",
                "renewable_total": "Erneuerbare total (hydro + solar + wind)",
                "total": "Gesamtproduktion (alle Träger)",
            },
            "note": (
                "Daten teilweise modelliert (v.a. PV, kleine Wasserkraft). "
                "Nachkorrekturen bei neuesten Tagen möglich."
            ),
        },
        "data": json.loads(pv.to_json(orient="records")),
    }

    # Speichern
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False)

    size_mb = OUT_FILE.stat().st_size / (1024 * 1024)
    print(f"\n  ✓ {OUT_FILE} ({size_mb:.1f} MB)")
    print("=" * 60)


if __name__ == "__main__":
    main()
