"""
Transform-Skript für BFE-Bilanz (Jahres- und Monatsbilanz).

Funktionsweise:
1. Liest BFE-Bilanz-CSVs aus pipeline/raw/snapshots/<datum>/bfe/
2. Trennt Erzeugungs-Daten (long, pro Energieform) von Bilanz-Aggregaten (wide)
3. Konvertiert Einheiten: GWh → MWh (Pipeline-Konvention)
4. Erstellt vier Output-Files in pipeline/intermediate/<datum>/fact/:
   - bilanz_erzeugung_jahr.json     (long, ~300 Zeilen)
   - bilanz_erzeugung_monat.json    (long, ~2'500 Zeilen)
   - bilanz_aggregat_jahr.json      (wide, 65 Zeilen)
   - bilanz_aggregat_monat.json     (wide, 314 Zeilen)

Aufruf:
    python pipeline/transform/transform_bilanz.py
        Nimmt automatisch den neuesten Snapshot

    python pipeline/transform/transform_bilanz.py --snapshot 2026-05-05
        Nimmt einen spezifischen Snapshot

    python pipeline/transform/transform_bilanz.py --force
        Überschreibt bestehende Outputs

Output-Schema bilanz_erzeugung_jahr.json (Long-Format):
    [
      {
        "jahr": 2020,
        "energieform_code": "wasserkraft_laufwerk",
        "erzeugung_mwh": 17500000.0
      }, ...
    ]

Output-Schema bilanz_erzeugung_monat.json (Long-Format):
    [
      {
        "jahr": 2024,
        "monat": 3,
        "energieform_code": "kernkraft",
        "erzeugung_mwh": 2100000.0,
        "ist_definitiv": true
      }, ...
    ]

Output-Schema bilanz_aggregat_jahr.json (Wide-Format):
    [
      {
        "jahr": 2024,
        "erzeugung_netto_mwh": 65000000,
        "einfuhr_mwh": 22000000,
        "ausfuhr_mwh": 25000000,
        "landesverbrauch_mwh": 60000000,
        "verluste_mwh": 4000000,
        "endverbrauch_mwh": 56000000,
        "verbrauch_speicherpumpen_mwh": 2500000
      }, ...
    ]

Output-Schema bilanz_aggregat_monat.json (Wide-Format):
    Wie Jahres-Aggregat, plus monat und ist_definitiv.

Energieform-Codes:
    wasserkraft_laufwerk         Laufwasserkraftwerke
    wasserkraft_speicherwerk     Speicherkraftwerke
    kernkraft                    Kernkraftwerke
    thermisch_fossil             Thermisch fossil
    thermisch_abfaelle           Thermisch erneuerbare Abfälle
    holz                         Holz
    biogas                       Biogas
    photovoltaik                 Photovoltaik
    wind                         Wind
    thermisch_aggregiert         Thermisch (Monatsbilanz, aggregiert)
    andere_aggregiert            Andere (vor 1995 oder Monatsbilanz)

Hinweis: Die Granularität der BFE-Bilanz folgt der historisch-politischen
Entwicklung der CH-Stromerzeugung:
  - 1960-1968: nur andere_aggregiert (vor Aufschlüsselung)
  - 1969: Kernkraft separat (Beznau 1 in Betrieb)
  - 1970-1989: + Wasserkraft Lauf-/Speicherwerk (BFE-Aufschlüsselung)
  - 1990-2024: + 6 Subkategorien (fossil, abfaelle, holz, biogas, PV, wind)

Für die Jahre 1960-1969 ist die Wasserkraft NICHT in dieser Long-Tabelle
enthalten. Die Gesamterzeugung jener Jahre ist nur in der Aggregat-Tabelle
(erzeugung_netto_mwh) verfügbar — eine Datenlücke der BFE-Quelle, keine
Verarbeitungs-Limitation.

In der Monatsbilanz vor ca. 2006 sind Wind, PV und Thermisch nicht separat
ausgewiesen. Für diese Monate gibts nur "andere_aggregiert".
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Optional

import pandas as pd

# Pfad-Setup
PIPELINE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PIPELINE_ROOT.parent))

from pipeline.utils.manifest import (
    init_manifest,
    add_file_to_manifest,
    write_manifest,
    load_manifest,
)

SNAPSHOT_ROOT = PIPELINE_ROOT / "raw" / "snapshots"
INTERMEDIATE_ROOT = PIPELINE_ROOT / "intermediate"

GWH_TO_MWH = 1000  # Faktor zur Einheiten-Umrechnung

# Mapping: Roh-Spalte → Energieform-Code (Jahresbilanz)
ENERGIEFORMEN_JAHR = {
    "Erzeugung_laufwerk_GWh": "wasserkraft_laufwerk",
    "Erzeugung_speicherwerk_GWh": "wasserkraft_speicherwerk",
    "Erzeugung_kernkraftwerk_GWh": "kernkraft",
    "Erzeugung_andere_fossil_GWh": "thermisch_fossil",
    "Erzeugung_andere_erneuerbare_abfaelle_GWh": "thermisch_abfaelle",
    "Erzeugung_holz_GWh": "holz",
    "Erzeugung_biogas_GWh": "biogas",
    "Erzeugung_photovoltaik_GWh": "photovoltaik",
    "Erzeugung_wind_GWh": "wind",
}

# Spalte für aggregiertes "andere" vor Aufschlüsselung (vor 1995)
ENERGIEFORM_JAHR_AGG = "Erzeugung_andere_total_GWh"

# Mapping: Roh-Spalte → Energieform-Code (Monatsbilanz)
ENERGIEFORMEN_MONAT = {
    "Erzeugung_Laufwerk_GWh": "wasserkraft_laufwerk",
    "Erzeugung_Speicherwerk_GWh": "wasserkraft_speicherwerk",
    "Erzeugung_Kernkraftwerk_GWh": "kernkraft",
    "Erzeugung_Thermische_GWh": "thermisch_aggregiert",
    "Erzeugung_Windkraft_GWh": "wind",
    "Erzeugung_Photovoltaik_GWh": "photovoltaik",
}

# Spalte für aggregiertes "andere" (in Monatsbilanz vor Aufschlüsselung)
ENERGIEFORM_MONAT_AGG = "Erzeugung_andere_GWh"

# Mapping: Roh-Spalte → Aggregat-Spalte (Jahres- und Monatsbilanz)
# Beide Bilanz-Files haben die gleichen Aggregat-Spalten.
AGGREGAT_SPALTEN = {
    "Verbrauch_speicherpumpen_GWh": "verbrauch_speicherpumpen_mwh",
    "Verbrauch_Speicherpumpen_GWh": "verbrauch_speicherpumpen_mwh",  # Monat (Gross)
    "Erzeugung_netto_GWh": "erzeugung_netto_mwh",
    "Landeserzeugung_GWh": "landeserzeugung_mwh",  # nur in Monatsbilanz
    "Einfuhr_GWh": "einfuhr_mwh",
    "Ausfuhr_GWh": "ausfuhr_mwh",
    "Landesverbrauch_GWh": "landesverbrauch_mwh",
    "Verluste_GWh": "verluste_mwh",
    "Endverbrauch_GWh": "endverbrauch_mwh",
}


def find_latest_snapshot() -> Optional[str]:
    """Findet das neueste Snapshot-Datum mit BFE-Bilanz-Daten."""
    if not SNAPSHOT_ROOT.exists():
        return None

    candidates = []
    for entry in SNAPSHOT_ROOT.iterdir():
        if not entry.is_dir():
            continue
        bfe_dir = entry / "bfe"
        if not bfe_dir.exists():
            continue
        if (bfe_dir / "bilanz_jahreswerte.csv").exists() and \
                (bfe_dir / "bilanz_monatswerte.csv").exists():
            candidates.append(entry.name)

    if not candidates:
        return None

    return sorted(candidates)[-1]


def transform_jahr_erzeugung(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transformiert die Jahresbilanz in Long-Format pro Energieform.

    Für Jahre mit aufgeschlüsselten Subkategorien (ab 1990) werden
    fossil, abfaelle, holz, biogas, photovoltaik und wind einzeln eingetragen.

    Für Jahre ohne Aufschlüsselung (vor 1990) wird stattdessen ein einzelner
    Eintrag "andere_aggregiert" mit dem Wert aus Erzeugung_andere_total_GWh
    erzeugt.

    Hauptkategorien (Wasserkraft Lauf/Speicher, Kernkraft) werden nur dann
    eingetragen, wenn der Wert nicht NaN ist — Wasserkraft erst ab 1970,
    Kernkraft erst ab 1969 (Beznau 1).
    """
    rows = []

    for _, row in df.iterrows():
        jahr = int(row["Jahr"])

        # 1. Hauptkategorien (immer vorhanden seit 1960): Wasserkraft + Kernkraft
        main_cats = [
            "Erzeugung_laufwerk_GWh",
            "Erzeugung_speicherwerk_GWh",
            "Erzeugung_kernkraftwerk_GWh",
        ]
        for col in main_cats:
            if col in row and pd.notna(row[col]):
                rows.append({
                    "jahr": jahr,
                    "energieform_code": ENERGIEFORMEN_JAHR[col],
                    "erzeugung_mwh": float(row[col]) * GWH_TO_MWH,
                })

        # 2. Subkategorien für "andere" (ab 1995): fossil, abfaelle, holz, biogas, PV, wind
        subcat_cols = [
            "Erzeugung_andere_fossil_GWh",
            "Erzeugung_andere_erneuerbare_abfaelle_GWh",
            "Erzeugung_holz_GWh",
            "Erzeugung_biogas_GWh",
            "Erzeugung_photovoltaik_GWh",
            "Erzeugung_wind_GWh",
        ]
        # Sind die Subkategorien für dieses Jahr verfügbar?
        # Wenn alle Null sind → vor 1995, nutze andere_total
        # Wenn mindestens eine nicht-Null → ab 1995, nutze die Subkategorien
        subcat_values = [row[col] for col in subcat_cols if col in row]
        has_subcategories = any(pd.notna(v) for v in subcat_values)

        if has_subcategories:
            for col in subcat_cols:
                if col in row and pd.notna(row[col]):
                    rows.append({
                        "jahr": jahr,
                        "energieform_code": ENERGIEFORMEN_JAHR[col],
                        "erzeugung_mwh": float(row[col]) * GWH_TO_MWH,
                    })
        else:
            # Vor 1995: nutze die aggregierte Spalte
            if ENERGIEFORM_JAHR_AGG in row and pd.notna(row[ENERGIEFORM_JAHR_AGG]):
                rows.append({
                    "jahr": jahr,
                    "energieform_code": "andere_aggregiert",
                    "erzeugung_mwh": float(row[ENERGIEFORM_JAHR_AGG]) * GWH_TO_MWH,
                })

    return pd.DataFrame(rows)


def transform_monat_erzeugung(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transformiert die Monatsbilanz in Long-Format pro Energieform.

    Für Monate mit aufgeschlüsselten Daten (ab ca. 2006): einzelne Subkategorien.
    Für Monate ohne Aufschlüsselung: nur "andere_aggregiert".

    Hauptkategorien (Wasserkraft + Kernkraft) sind in allen Monaten verfügbar.
    """
    rows = []

    for _, row in df.iterrows():
        jahr = int(row["Jahr"])
        monat = int(row["Monat"])
        ist_definitiv = bool(int(row["Definitiv"]))

        # 1. Hauptkategorien (immer)
        main_cats = [
            "Erzeugung_Laufwerk_GWh",
            "Erzeugung_Speicherwerk_GWh",
            "Erzeugung_Kernkraftwerk_GWh",
        ]
        for col in main_cats:
            if col in row and pd.notna(row[col]):
                rows.append({
                    "jahr": jahr,
                    "monat": monat,
                    "energieform_code": ENERGIEFORMEN_MONAT[col],
                    "erzeugung_mwh": float(row[col]) * GWH_TO_MWH,
                    "ist_definitiv": ist_definitiv,
                })

        # 2. Aufgeschlüsselte: Thermisch, Wind, PV (typischerweise ab 2006)
        subcat_cols = [
            "Erzeugung_Thermische_GWh",
            "Erzeugung_Windkraft_GWh",
            "Erzeugung_Photovoltaik_GWh",
        ]
        subcat_values = [row[col] for col in subcat_cols if col in row]
        has_subcategories = any(pd.notna(v) for v in subcat_values)

        if has_subcategories:
            for col in subcat_cols:
                if col in row and pd.notna(row[col]):
                    rows.append({
                        "jahr": jahr,
                        "monat": monat,
                        "energieform_code": ENERGIEFORMEN_MONAT[col],
                        "erzeugung_mwh": float(row[col]) * GWH_TO_MWH,
                        "ist_definitiv": ist_definitiv,
                    })
        else:
            # Vor 2006: nur aggregiertes "andere"
            if ENERGIEFORM_MONAT_AGG in row and pd.notna(row[ENERGIEFORM_MONAT_AGG]):
                rows.append({
                    "jahr": jahr,
                    "monat": monat,
                    "energieform_code": "andere_aggregiert",
                    "erzeugung_mwh": float(row[ENERGIEFORM_MONAT_AGG]) * GWH_TO_MWH,
                    "ist_definitiv": ist_definitiv,
                })

    return pd.DataFrame(rows)


def transform_jahr_aggregat(df: pd.DataFrame) -> pd.DataFrame:
    """Extrahiert die Bilanz-Aggregate aus der Jahresbilanz (Wide-Format)."""
    result = pd.DataFrame()
    result["jahr"] = df["Jahr"].astype(int)

    aggregat_cols_jahr = {
        "Verbrauch_speicherpumpen_GWh": "verbrauch_speicherpumpen_mwh",
        "Erzeugung_netto_GWh": "erzeugung_netto_mwh",
        "Einfuhr_GWh": "einfuhr_mwh",
        "Ausfuhr_GWh": "ausfuhr_mwh",
        "Landesverbrauch_GWh": "landesverbrauch_mwh",
        "Verluste_GWh": "verluste_mwh",
        "Endverbrauch_GWh": "endverbrauch_mwh",
    }

    for source_col, target_col in aggregat_cols_jahr.items():
        if source_col in df.columns:
            result[target_col] = df[source_col] * GWH_TO_MWH

    return result


def transform_monat_aggregat(df: pd.DataFrame) -> pd.DataFrame:
    """Extrahiert die Bilanz-Aggregate aus der Monatsbilanz (Wide-Format)."""
    result = pd.DataFrame()
    result["jahr"] = df["Jahr"].astype(int)
    result["monat"] = df["Monat"].astype(int)
    result["ist_definitiv"] = df["Definitiv"].astype(int).astype(bool)

    aggregat_cols_monat = {
        "Verbrauch_Speicherpumpen_GWh": "verbrauch_speicherpumpen_mwh",
        "Landeserzeugung_GWh": "landeserzeugung_mwh",
        "Erzeugung_netto_GWh": "erzeugung_netto_mwh",
        "Einfuhr_GWh": "einfuhr_mwh",
        "Ausfuhr_GWh": "ausfuhr_mwh",
        "Landesverbrauch_GWh": "landesverbrauch_mwh",
        "Verluste_GWh": "verluste_mwh",
        "Endverbrauch_GWh": "endverbrauch_mwh",
    }

    for source_col, target_col in aggregat_cols_monat.items():
        if source_col in df.columns:
            result[target_col] = df[source_col] * GWH_TO_MWH

    return result


def write_json(df: pd.DataFrame, path: Path) -> None:
    """Schreibt einen DataFrame als JSON (Liste von Records)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    records = df.to_dict(orient="records")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Transform BFE-Bilanz (Jahr + Monat) in Long+Wide-Faktentabellen"
    )
    parser.add_argument(
        "--snapshot", default=None,
        help="Snapshot-Datum YYYY-MM-DD (default: neuester verfügbarer)",
    )
    parser.add_argument(
        "--intermediate-date", default=None,
        help="Output-Datum YYYY-MM-DD (default: heute)",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Bestehende Output-Files überschreiben",
    )
    args = parser.parse_args()

    # === Snapshot bestimmen ===
    if args.snapshot:
        snapshot_date = args.snapshot
    else:
        snapshot_date = find_latest_snapshot()
        if not snapshot_date:
            print("FEHLER: Kein Snapshot mit BFE-Bilanz-Daten gefunden.")
            sys.exit(1)

    snapshot_dir = SNAPSHOT_ROOT / snapshot_date
    bfe_dir = snapshot_dir / "bfe"

    jahr_csv = bfe_dir / "bilanz_jahreswerte.csv"
    monat_csv = bfe_dir / "bilanz_monatswerte.csv"

    if not jahr_csv.exists():
        print(f"FEHLER: {jahr_csv} existiert nicht.")
        sys.exit(1)
    if not monat_csv.exists():
        print(f"FEHLER: {monat_csv} existiert nicht.")
        sys.exit(1)

    # === Output-Datum ===
    intermediate_date = args.intermediate_date or date.today().isoformat()
    intermediate_dir = INTERMEDIATE_ROOT / intermediate_date
    fact_dir = intermediate_dir / "fact"

    output_files = {
        "bilanz_erzeugung_jahr": fact_dir / "bilanz_erzeugung_jahr.json",
        "bilanz_erzeugung_monat": fact_dir / "bilanz_erzeugung_monat.json",
        "bilanz_aggregat_jahr": fact_dir / "bilanz_aggregat_jahr.json",
        "bilanz_aggregat_monat": fact_dir / "bilanz_aggregat_monat.json",
    }

    print(f"Snapshot-Datum:       {snapshot_date}")
    print(f"Snapshot-Verzeichnis: {snapshot_dir}")
    print(f"Output-Datum:         {intermediate_date}")
    print(f"Output-Verzeichnis:   {intermediate_dir}")

    # Idempotenz-Check
    all_exist = all(p.exists() for p in output_files.values())
    if all_exist and not args.force:
        print()
        print("✓ Alle vier Output-Files existieren bereits — übersprungen.")
        print(f"  Mit --force überschreiben.")
        return

    # === Verarbeitung ===
    print()
    print("→ CSVs einlesen", end=" ", flush=True)
    df_jahr = pd.read_csv(jahr_csv)
    df_monat = pd.read_csv(monat_csv)
    print(f"(Jahr: {len(df_jahr)} Zeilen, Monat: {len(df_monat)} Zeilen)")

    # === 1. Erzeugung Jahr (long) ===
    print("→ Jahr-Erzeugung transformieren (long)", end=" ", flush=True)
    erzeugung_jahr = transform_jahr_erzeugung(df_jahr)
    print(f"({len(erzeugung_jahr)} Zeilen)")

    # === 2. Erzeugung Monat (long) ===
    print("→ Monat-Erzeugung transformieren (long)", end=" ", flush=True)
    erzeugung_monat = transform_monat_erzeugung(df_monat)
    print(f"({len(erzeugung_monat)} Zeilen)")

    # === 3. Aggregat Jahr (wide) ===
    print("→ Jahr-Aggregate transformieren (wide)", end=" ", flush=True)
    aggregat_jahr = transform_jahr_aggregat(df_jahr)
    print(f"({len(aggregat_jahr)} Zeilen)")

    # === 4. Aggregat Monat (wide) ===
    print("→ Monat-Aggregate transformieren (wide)", end=" ", flush=True)
    aggregat_monat = transform_monat_aggregat(df_monat)
    print(f"({len(aggregat_monat)} Zeilen)")

    # === Output schreiben ===
    print("→ Output schreiben")
    write_json(erzeugung_jahr, output_files["bilanz_erzeugung_jahr"])
    write_json(erzeugung_monat, output_files["bilanz_erzeugung_monat"])
    write_json(aggregat_jahr, output_files["bilanz_aggregat_jahr"])
    write_json(aggregat_monat, output_files["bilanz_aggregat_monat"])

    for key, path in output_files.items():
        size_kb = path.stat().st_size / 1024
        print(f"  ✓ {path.name:38s} ({size_kb:6.1f} KB)")

    # === Manifest ===
    existing_manifest = load_manifest(intermediate_dir)
    if existing_manifest:
        manifest = existing_manifest
    else:
        manifest = init_manifest(intermediate_date, "transform_bilanz.py")

    for key, path in output_files.items():
        add_file_to_manifest(
            manifest, "fact", key, "json", path,
            f"transform_bilanz.py from {jahr_csv.relative_to(PIPELINE_ROOT.parent)} "
            f"+ {monat_csv.relative_to(PIPELINE_ROOT.parent)}",
        )

    manifest_path = write_manifest(manifest, intermediate_dir)

    print()
    print("=" * 60)
    print(f"Erfolgreich abgeschlossen.")
    print(f"Manifest: {manifest_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()