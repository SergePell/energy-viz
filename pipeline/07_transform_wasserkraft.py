#!/usr/bin/env python3
"""
07_transform_wasserkraft.py
===========================
Transformiert BFE Wasserkraftanlagen-Statistik (ZIP) → JSON mit Geodaten.

Extrahiert die CSV aus dem ZIP, konvertiert Swiss LV95 → WGS84 Koordinaten,
und erzeugt ein kompaktes JSON für Kartenvisualisierung.

Input:  pipeline/raw/wasserkraftanlagen_2025.zip
Output: src/data/hydropower-plants.json

Verwendung:
    python pipeline/07_transform_wasserkraft.py
"""

import json
import math
import zipfile
import io
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Pfade
# ---------------------------------------------------------------------------
PIPELINE_DIR = Path(__file__).parent
RAW_ZIP = PIPELINE_DIR / "raw" / "wasserkraftanlagen_2025.zip"
OUT = PIPELINE_DIR.parent / "src" / "data" / "hydropower-plants.json"

# ---------------------------------------------------------------------------
# WKA-Typ Mapping
# ---------------------------------------------------------------------------
TYPE_MAP = {
    "L": "run_of_river",       # Laufwasserkraftwerk
    "S": "storage",            # Speicherkraftwerk
    "PS": "pumped_storage",    # Pumpspeicherkraftwerk
    "P": "pump",               # Reine Pumpanlage
    "U": "refurbishment",      # Umbau/Erneuerung
    "D": "pressure_reduction", # Druckreduzieranlage
}

TYPE_LABELS = {
    "run_of_river": "Laufwasserkraftwerk",
    "storage": "Speicherkraftwerk",
    "pumped_storage": "Pumpspeicherkraftwerk",
    "pump": "Pumpanlage",
    "refurbishment": "Umbau/Erneuerung",
    "pressure_reduction": "Druckreduzieranlage",
}

# ---------------------------------------------------------------------------
# Kanton-Mapping (deutsch → Kürzel)
# ---------------------------------------------------------------------------
KANTON_MAP = {
    "Aargau": "AG", "Appenzell A.Rh.": "AR", "Appenzell I.Rh.": "AI",
    "Basel-Landschaft": "BL", "Bern": "BE", "Freiburg": "FR",
    "Genf": "GE", "Glarus": "GL", "Graubuenden": "GR", "Jura": "JU",
    "Luzern": "LU", "Neuenburg": "NE", "Nidwalden": "NW",
    "Obwalden": "OW", "Schaffhausen": "SH", "Schwyz": "SZ",
    "Solothurn": "SO", "St.Gallen": "SG", "Tessin": "TI",
    "Thurgau": "TG", "Uri": "UR", "Waadt": "VD", "Wallis": "VS",
    "Zuerich": "ZH", "Zug": "ZG",
    # Grenzüberschreitende Anlagen
    "Austria": "AT", "Deutschland": "DE", "France": "FR_int",
}


# ---------------------------------------------------------------------------
# LV95 → WGS84 Koordinaten-Konvertierung
# ---------------------------------------------------------------------------
def lv95_to_wgs84(east: float, north: float) -> tuple[float, float]:
    """
    Konvertiert Swiss LV95 (CH1903+) Koordinaten nach WGS84.

    Basiert auf der Näherungsformel des Bundesamts für Landestopografie.
    Genauigkeit: ca. 1 Meter — ausreichend für Kartenvisualisierung.

    Parameter:
        east:  LV95 Ost-Koordinate  (z.B. 2700400)
        north: LV95 Nord-Koordinate (z.B. 1169740)

    Returns:
        (latitude, longitude) in WGS84 Dezimalgrad
    """
    # Hilfsgrössen (in 1000 km)
    y_aux = (east - 2600000) / 1000000
    x_aux = (north - 1200000) / 1000000

    # Breitengrad
    lat = (16.9023892
           + 3.238272 * x_aux
           - 0.270978 * y_aux ** 2
           - 0.002528 * x_aux ** 2
           - 0.0447 * y_aux ** 2 * x_aux
           - 0.0140 * x_aux ** 3)

    # Längengrad
    lon = (2.6779094
           + 4.728982 * y_aux
           + 0.791484 * y_aux * x_aux
           + 0.1306 * y_aux * x_aux ** 2
           - 0.0436 * y_aux ** 3)

    # Umrechnung: Sexagesimalsekunden → Dezimalgrad
    lat = lat * 100 / 36
    lon = lon * 100 / 36

    return round(lat, 6), round(lon, 6)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("  DS-10 — Wasserkraftanlagen der Schweiz")
    print("=" * 60)

    # CSV aus ZIP lesen
    z = zipfile.ZipFile(RAW_ZIP)
    csv_files = [f for f in z.namelist() if f.endswith('.csv')]
    if not csv_files:
        print("  ✗ Keine CSV-Datei im ZIP gefunden")
        return

    csv_file = csv_files[0]
    print(f"\n  CSV: {csv_file}")

    df = pd.read_csv(
        io.BytesIO(z.read(csv_file)),
        sep=';',
        encoding='latin-1'
    )
    print(f"  {len(df)} Anlagen, {df.shape[1]} Spalten")

    # Relevante Spalten extrahieren und umbenennen
    plants = []
    skipped = 0

    for _, row in df.iterrows():
        # Koordinaten
        east = row.get("ZE-Koordinaten (Ost)")
        north = row.get("ZE-Koordinaten (Nord)")

        if pd.isna(east) or pd.isna(north) or east == 0 or north == 0:
            skipped += 1
            continue

        # LV95 → WGS84
        lat, lon = lv95_to_wgs84(float(east), float(north))

        # Kanton
        kanton_raw = str(row.get("ZE-Kanton (Land)", ""))
        kanton = KANTON_MAP.get(kanton_raw, kanton_raw)

        # Typ
        typ_raw = str(row.get("WKA-Typ", "")).strip()
        typ = TYPE_MAP.get(typ_raw, typ_raw)

        # Status
        status = str(row.get("ZE-Status - beachten!", "")).strip()

        # Produktion und Leistung
        prod_year = row.get("Prod. ohne Umwaelzb. - Jahr [GWh]")
        prod_winter = row.get("Prod. ohne Umwaelzb. - Winter [GWh]")
        prod_summer = row.get("Prod. ohne Umwaelzb. - Sommer [MW]")  # Spaltenname sagt MW, ist aber GWh
        capacity_turbine = row.get("Inst. Turbinenleistung [MW]")
        capacity_generator = row.get("Max. Leistung ab Generator [MW]")
        capacity_pump = row.get("Inst. Pumpenleistung [MW]")

        # Inbetriebnahme
        year_first = row.get("ZE-Erste Inbetriebnahme")
        year_last = row.get("ZE-Letzte Inbetriebnahme")

        # Höhe
        elevation = row.get("ZE-Kote [m.ue.M.]")

        # Gewässer
        water = str(row.get("Genutzte Gewaesser - Name (1)", "")).strip()
        if water == "nan":
            water = None

        plant = {
            "id": int(row["ZE-Nr"]),
            "name": str(row["ZE-Name"]).strip(),
            "plant_name": str(row["WKA-Name"]).strip(),
            "type": typ,
            "canton": kanton,
            "location": str(row.get("ZE-Standort", "")).strip(),
            "status": status,
            "lat": lat,
            "lon": lon,
            "elevation_m": round(float(elevation)) if pd.notna(elevation) else None,
            "capacity_mw": round(float(capacity_turbine), 1) if pd.notna(capacity_turbine) else None,
            "capacity_generator_mw": round(float(capacity_generator), 1) if pd.notna(capacity_generator) else None,
            "capacity_pump_mw": round(float(capacity_pump), 1) if pd.notna(capacity_pump) and float(capacity_pump) > 0 else None,
            "production_gwh": round(float(prod_year), 1) if pd.notna(prod_year) else None,
            "production_winter_gwh": round(float(prod_winter), 1) if pd.notna(prod_winter) else None,
            "production_summer_gwh": round(float(prod_summer), 1) if pd.notna(prod_summer) else None,
            "year_commissioned": int(year_first) if pd.notna(year_first) else None,
            "year_last_update": int(year_last) if pd.notna(year_last) else None,
            "water_body": water,
        }
        plants.append(plant)

    print(f"  ✓ {len(plants)} Anlagen mit Koordinaten")
    if skipped:
        print(f"  ⚠ {skipped} Anlagen ohne Koordinaten übersprungen")

    # Statistiken
    types = {}
    cantons = {}
    total_capacity = 0
    total_production = 0
    for p in plants:
        t = p["type"]
        types[t] = types.get(t, 0) + 1
        c = p["canton"]
        cantons[c] = cantons.get(c, 0) + 1
        if p["capacity_mw"]:
            total_capacity += p["capacity_mw"]
        if p["production_gwh"]:
            total_production += p["production_gwh"]

    print(f"\n  Typen:")
    for t, count in sorted(types.items(), key=lambda x: -x[1]):
        label = TYPE_LABELS.get(t, t)
        print(f"    {label:30s} {count:>4}")

    print(f"\n  Top-10 Kantone:")
    for c, count in sorted(cantons.items(), key=lambda x: -x[1])[:10]:
        print(f"    {c:5s} {count:>4}")

    print(f"\n  Gesamtleistung: {total_capacity:,.0f} MW")
    print(f"  Gesamtproduktion: {total_production:,.0f} GWh/Jahr")

    # JSON bauen
    output = {
        "meta": {
            "dataset": "bfe-hydropower-plants",
            "source": "BFE Statistik der Wasserkraftanlagen der Schweiz",
            "source_url": "https://www.bfe.admin.ch/bfe/de/home/versorgung/statistik-und-geodaten/energiestatistiken/teilstatistiken.html",
            "reference_date": "2025-01-01",
            "records": len(plants),
            "coordinate_system": "WGS84 (konvertiert aus LV95/CH1903+)",
            "types": TYPE_LABELS,
            "total_capacity_mw": round(total_capacity, 1),
            "total_production_gwh": round(total_production, 1),
        },
        "data": plants,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False)

    size_kb = OUT.stat().st_size / 1024
    print(f"\n  ✓ {OUT} ({size_kb:.0f} KB)")
    print("=" * 60)


if __name__ == "__main__":
    main()
