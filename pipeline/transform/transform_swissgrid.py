"""
Transform-Skript für Swissgrid Energieübersicht (15-Min-Daten).

Funktionsweise:
1. Liest Swissgrid-XLSX/XLS aus pipeline/raw/snapshots/<datum>/swissgrid/
2. Parst das Sheet "Zeitreihen0h15" mit den 15-Min-Werten
3. Konvertiert Zeitstempel von Europe/Zurich → UTC
4. Konvertiert Energie-Werte von kWh → MWh
5. Mappt 18 Swissgrid-Einheiten auf ISO 3166-2 Codes
6. Schreibt vier Output-Files in pipeline/intermediate/<datum>/fact/:
   - swissgrid_erzeugung_15min_<jahr>.parquet     (long, ~630'000 Zeilen)
   - swissgrid_verbrauch_15min_<jahr>.parquet     (long, ~630'000 Zeilen)
   - swissgrid_grenzkupplung_15min_<jahr>.parquet (long, ~280'000 Zeilen)
   - swissgrid_ch_aggregat_15min_<jahr>.parquet   (wide, ~35'000 Zeilen)

Aufruf:
    python pipeline/transform/transform_swissgrid.py --year 2024
        Transformiert ein einzelnes Jahr (Test-Modus)

    python pipeline/transform/transform_swissgrid.py
        Transformiert alle verfügbaren Jahre

    python pipeline/transform/transform_swissgrid.py --force
        Überschreibt bestehende Outputs

Output-Schema swissgrid_erzeugung_15min:
    [
      {
        "zeitstempel_utc": "2024-01-01T00:15:00+00:00",
        "swissgrid_einheit": "CH-AG",
        "erzeugung_mwh": 512.108
      }, ...
    ]

Output-Schema swissgrid_verbrauch_15min:
    Wie Erzeugung, mit verbrauch_mwh.

Output-Schema swissgrid_grenzkupplung_15min:
    [
      {
        "zeitstempel_utc": "2024-01-01T00:15:00+00:00",
        "richtung_code": "CH_AT",        # vom-zum
        "energie_mwh": 48.1
      }, ...
    ]

Output-Schema swissgrid_ch_aggregat_15min (wide):
    [
      {
        "zeitstempel_utc": "...",
        "produktion_total_mwh": 1296.448,
        "verbrauch_total_mwh": 1939.192,
        "endverbrauch_total_mwh": 1443.842,
        "vertikale_einspeisung_mwh": 854.345,
        "netto_ausspeisung_mwh": 604.677,
        "import_mwh": 1089.017,
        "export_mwh": 445.459,
        "transit_mwh": 445.459
      }, ...
    ]

Hinweise:
- Regelenergie (Sekundär/Tertiär) wird bewusst weggelassen — nicht zentral für
  die Forschungsfragen. Kann später ergänzt werden.
- Zeitstempel im Roh-Sheet sind lokale CH-Zeit (Europe/Zurich) und werden
  nach UTC konvertiert. Sommerzeit-Übergänge werden via pandas tz_localize
  mit ambiguous='infer' behandelt.
"""

import argparse
import re
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

KWH_TO_MWH = 1 / 1000  # Faktor zur Einheiten-Umrechnung

ZEITREIHEN_SHEET = "Zeitreihen0h15"

# Mapping: Swissgrid-Spaltenname → ISO-Code
# Die Spalten heissen z.B. "Produktion Kanton AG | Production Canton AG"
# Wir matchen via Regex auf die Kanton-Codes.
EINHEIT_REGEX_PATTERNS = [
    # Einzelkantone
    (r"Kanton AG\b", "CH-AG"),
    (r"Kanton FR\b", "CH-FR"),
    (r"Kanton GL\b", "CH-GL"),
    (r"Kanton GR\b", "CH-GR"),
    (r"Kanton LU\b", "CH-LU"),
    (r"Kanton NE\b", "CH-NE"),
    (r"Kanton SO\b", "CH-SO"),
    (r"Kanton SG\b", "CH-SG"),
    (r"Kanton TI\b", "CH-TI"),
    (r"Kanton TG\b", "CH-TG"),
    (r"Kanton VS\b", "CH-VS"),
    # Gruppen
    (r"Kantone AI,\s*AR\b", "CH-AI_AR"),
    (r"Kantone BL,\s*BS\b", "CH-BL_BS"),
    (r"Kantone BE,\s*JU\b", "CH-BE_JU"),
    (r"Kantone SZ,\s*ZG\b", "CH-SZ_ZG"),
    (r"Kantone OW,\s*NW,\s*UR\b", "CH-OW_NW_UR"),
    (r"Kantone GE,\s*VD\b", "CH-GE_VD"),
    (r"Kantone SH,\s*ZH\b", "CH-SH_ZH"),
]

# Mapping: Swissgrid-Spaltenname → Aggregat-Spalte (CH-weit)
CH_AGGREGAT_SPALTEN = {
    "Summe produzierte Energie Regelblock Schweiz": "produktion_total_mwh",
    "Summe verbrauchte Energie Regelblock Schweiz": "verbrauch_total_mwh",
    "Summe endverbrauchte Energie Regelblock Schweiz": "endverbrauch_total_mwh",
    "Vertikale Einspeisung ins Übertragungsnetz Schweiz": "vertikale_einspeisung_mwh",
    "Netto Ausspeisung aus dem Übertragungsnetz Schweiz": "netto_ausspeisung_mwh",
    "Import": "import_mwh",
    "Export": "export_mwh",
    "Transit": "transit_mwh",
}

# Mapping: Swissgrid-Spaltenname → Grenzkupplung-Richtung
GRENZKUPPLUNG_SPALTEN = {
    "Verbundaustausch CH->AT": "CH_AT",
    "Verbundaustausch AT->CH": "AT_CH",
    "Verbundaustausch CH->DE": "CH_DE",
    "Verbundaustausch DE->CH": "DE_CH",
    "Verbundaustausch CH->FR": "CH_FR",
    "Verbundaustausch FR->CH": "FR_CH",
    "Verbundaustausch CH->IT": "CH_IT",
    "Verbundaustausch IT->CH": "IT_CH",
}


def find_swissgrid_files(snapshot_dir: Path) -> dict:
    """
    Findet alle Swissgrid-Files im Snapshot-Verzeichnis.
    Returns: dict[jahr → Path]
    """
    swissgrid_dir = snapshot_dir / "swissgrid"
    if not swissgrid_dir.exists():
        return {}

    files = {}
    # Pattern: energieuebersicht_ch_<jahr>.xlsx oder .xls
    pattern = re.compile(r"energieuebersicht_ch_(\d{4})\.xlsx?$", re.IGNORECASE)
    for f in swissgrid_dir.iterdir():
        if not f.is_file():
            continue
        m = pattern.match(f.name)
        if m:
            jahr = int(m.group(1))
            files[jahr] = f

    return files


def find_latest_snapshot() -> Optional[str]:
    """Findet das neueste Snapshot-Datum mit Swissgrid-Daten."""
    if not SNAPSHOT_ROOT.exists():
        return None

    candidates = []
    for entry in SNAPSHOT_ROOT.iterdir():
        if not entry.is_dir():
            continue
        if (entry / "swissgrid").exists():
            candidates.append(entry.name)

    if not candidates:
        return None

    return sorted(candidates)[-1]


def map_einheit_from_column(column_name: str) -> Optional[str]:
    """
    Mappt einen Swissgrid-Spaltennamen auf einen Einheit-Code.
    Returns: ISO-Code (CH-AG, CH-AI_AR, ...) oder None wenn keine Einheit.
    """
    for pattern, code in EINHEIT_REGEX_PATTERNS:
        if re.search(pattern, column_name):
            return code
    return None


def load_swissgrid_sheet(file_path: Path) -> pd.DataFrame:
    """
    Liest das Sheet 'Zeitreihen0h15' aus einem Swissgrid-File ein.

    Die erste Datenzeile enthält Einheiten-Header (kWh) statt Werte.
    Wir lesen sie ein, droppen sie aber sofort.
    """
    # XLS/XLSX automatisch erkannt
    df = pd.read_excel(file_path, sheet_name=ZEITREIHEN_SHEET)

    # Erste Spalte ist "Unnamed: 0" mit dem Zeitstempel
    # Erste Zeile in dieser Spalte ist "Zeitstempel" (oder "Zeitstempel 0h15")
    # → wir droppen alle Zeilen wo Spalte 0 keinen parsbaren Zeitstempel hat
    timestamp_col = df.columns[0]

    # Zeitstempel parsen — Format ist "DD.MM.YYYY HH:MM"
    df["_parsed_timestamp"] = pd.to_datetime(
        df[timestamp_col],
        format="%d.%m.%Y %H:%M",
        errors="coerce",
    )

    # Zeilen ohne validen Zeitstempel droppen (Header-Zeile, Footer, etc.)
    n_before = len(df)
    df = df[df["_parsed_timestamp"].notna()].copy()
    n_dropped = n_before - len(df)
    if n_dropped > 0:
        print(f"    {n_dropped} Zeile(n) ohne validen Zeitstempel gedroppt")

    return df


def convert_to_utc(df: pd.DataFrame, timestamp_col: str = "_parsed_timestamp") -> pd.Series:
    """
    Konvertiert lokale Schweizer Zeitstempel (Europe/Zurich) nach UTC.
    Sommerzeit-Übergänge werden via ambiguous='infer' behandelt.
    """
    ts = df[timestamp_col]

    # Lokalisiere als Europe/Zurich, dann nach UTC konvertieren
    # ambiguous='infer' versucht, doppelte Stunden bei DST-Ende zu unterscheiden
    # nonexistent='shift_forward' verschiebt fehlende Stunde bei DST-Anfang
    try:
        ts_local = ts.dt.tz_localize(
            "Europe/Zurich",
            ambiguous="infer",
            nonexistent="shift_forward",
        )
    except Exception as e:
        # Falls infer nicht klappt: fallback auf False (= Winterzeit)
        print(f"    DST-Inferenz fehlgeschlagen ({e}), verwende ambiguous=False")
        ts_local = ts.dt.tz_localize(
            "Europe/Zurich",
            ambiguous=False,
            nonexistent="shift_forward",
        )

    return ts_local.dt.tz_convert("UTC")


def column_to_numeric(series: pd.Series) -> pd.Series:
    """
    Konvertiert eine Swissgrid-Spalte zu numerischen Werten.
    Werte können als String oder Zahl kommen, Header-Zeile mit "kWh" wird Null.
    """
    return pd.to_numeric(series, errors="coerce")


def transform_einheiten_long(
        df: pd.DataFrame,
        timestamp_utc: pd.Series,
        spalten_filter: str,  # "Produktion" oder "Verbrauch"
) -> pd.DataFrame:
    """
    Transformiert die Einheit-Spalten in Long-Format.

    Args:
        df: DataFrame mit Swissgrid-Daten
        timestamp_utc: UTC-Zeitstempel-Series
        spalten_filter: Filter-String, z.B. "Produktion" oder "Verbrauch"

    Returns:
        Long-DataFrame mit Spalten zeitstempel_utc, swissgrid_einheit, wert_mwh
    """
    rows = []

    # Finde alle relevanten Spalten und mappe sie auf Einheit-Codes
    matched_columns = {}  # column_name → einheit_code
    for col in df.columns:
        if not col.startswith(spalten_filter + " Kanton"):
            continue
        einheit_code = map_einheit_from_column(col)
        if einheit_code:
            matched_columns[col] = einheit_code

    if not matched_columns:
        print(f"    ! WARNUNG: Keine '{spalten_filter}'-Spalten für Einheiten gefunden!")
        return pd.DataFrame()

    print(f"    {len(matched_columns)} {spalten_filter}-Spalten gemappt")

    # Long-Format aufbauen
    for col, einheit_code in matched_columns.items():
        values = column_to_numeric(df[col]) * KWH_TO_MWH

        sub_df = pd.DataFrame({
            "zeitstempel_utc": timestamp_utc,
            "swissgrid_einheit": einheit_code,
            "wert_mwh": values,
        })
        # Nur valide Werte behalten
        sub_df = sub_df[sub_df["wert_mwh"].notna()]
        rows.append(sub_df)

    result = pd.concat(rows, ignore_index=True)
    result = result.sort_values(["zeitstempel_utc", "swissgrid_einheit"]).reset_index(drop=True)
    return result


def transform_grenzkupplung_long(
        df: pd.DataFrame,
        timestamp_utc: pd.Series,
) -> pd.DataFrame:
    """Transformiert die Grenzkupplung-Spalten in Long-Format."""
    rows = []

    matched_columns = {}
    for col in df.columns:
        for swissgrid_col, code in GRENZKUPPLUNG_SPALTEN.items():
            if swissgrid_col in col:
                matched_columns[col] = code
                break

    if not matched_columns:
        print(f"    ! WARNUNG: Keine Grenzkupplung-Spalten gefunden!")
        return pd.DataFrame()

    print(f"    {len(matched_columns)} Grenzkupplung-Spalten gemappt")

    for col, richtung_code in matched_columns.items():
        values = column_to_numeric(df[col]) * KWH_TO_MWH

        sub_df = pd.DataFrame({
            "zeitstempel_utc": timestamp_utc,
            "richtung_code": richtung_code,
            "energie_mwh": values,
        })
        sub_df = sub_df[sub_df["energie_mwh"].notna()]
        rows.append(sub_df)

    result = pd.concat(rows, ignore_index=True)
    result = result.sort_values(["zeitstempel_utc", "richtung_code"]).reset_index(drop=True)
    return result


def transform_ch_aggregat_wide(
        df: pd.DataFrame,
        timestamp_utc: pd.Series,
) -> pd.DataFrame:
    """Transformiert die CH-Aggregat-Spalten in Wide-Format."""
    result = pd.DataFrame({"zeitstempel_utc": timestamp_utc})

    for swissgrid_col, target_col in CH_AGGREGAT_SPALTEN.items():
        # Finde die echte Spalte: Swissgrid hat oft "<DE> | <EN>" Format
        matching = [c for c in df.columns if c.startswith(swissgrid_col)]
        if not matching:
            print(f"    ! Nicht gefunden: '{swissgrid_col}'")
            continue
        col = matching[0]
        values = column_to_numeric(df[col]) * KWH_TO_MWH
        result[target_col] = values

    return result


def transform_year(
        year: int,
        file_path: Path,
        intermediate_dir: Path,
        force: bool = False,
) -> bool:
    """Transformiert ein einzelnes Jahr."""
    fact_dir = intermediate_dir / "fact"
    fact_dir.mkdir(parents=True, exist_ok=True)

    output_files = {
        "erzeugung": fact_dir / f"swissgrid_erzeugung_15min_{year}.parquet",
        "verbrauch": fact_dir / f"swissgrid_verbrauch_15min_{year}.parquet",
        "grenzkupplung": fact_dir / f"swissgrid_grenzkupplung_15min_{year}.parquet",
        "ch_aggregat": fact_dir / f"swissgrid_ch_aggregat_15min_{year}.parquet",
    }

    print(f"\n→ Swissgrid {year}")
    print(f"  Input: {file_path.name}")

    # Idempotenz-Check
    all_exist = all(p.exists() for p in output_files.values())
    if all_exist and not force:
        print(f"  ✓ Alle vier Output-Files existieren bereits — übersprungen")
        return True

    # === Sheet einlesen ===
    print(f"  ↓ Sheet '{ZEITREIHEN_SHEET}' einlesen", end=" ", flush=True)
    try:
        df = load_swissgrid_sheet(file_path)
    except Exception as e:
        print(f"\n  ! Fehler beim Einlesen: {e}")
        return False
    print(f"({len(df):,} Zeilen, {len(df.columns)} Spalten)")

    # === Zeitstempel UTC ===
    print(f"  → Zeitstempel Europe/Zurich → UTC konvertieren")
    timestamp_utc = convert_to_utc(df)

    # === Erzeugung ===
    print(f"  → Erzeugung-Spalten transformieren (long)")
    erzeugung_df = transform_einheiten_long(df, timestamp_utc, "Produktion")
    if not erzeugung_df.empty:
        erzeugung_df = erzeugung_df.rename(columns={"wert_mwh": "erzeugung_mwh"})
        erzeugung_df.to_parquet(output_files["erzeugung"], index=False)
        size_mb = output_files["erzeugung"].stat().st_size / (1024 * 1024)
        print(f"    ✓ {output_files['erzeugung'].name} ({size_mb:.1f} MB, {len(erzeugung_df):,} Zeilen)")

    # === Verbrauch ===
    print(f"  → Verbrauch-Spalten transformieren (long)")
    verbrauch_df = transform_einheiten_long(df, timestamp_utc, "Verbrauch")
    if not verbrauch_df.empty:
        verbrauch_df = verbrauch_df.rename(columns={"wert_mwh": "verbrauch_mwh"})
        verbrauch_df.to_parquet(output_files["verbrauch"], index=False)
        size_mb = output_files["verbrauch"].stat().st_size / (1024 * 1024)
        print(f"    ✓ {output_files['verbrauch'].name} ({size_mb:.1f} MB, {len(verbrauch_df):,} Zeilen)")

    # === Grenzkupplung ===
    print(f"  → Grenzkupplung-Spalten transformieren (long)")
    grenz_df = transform_grenzkupplung_long(df, timestamp_utc)
    if not grenz_df.empty:
        grenz_df.to_parquet(output_files["grenzkupplung"], index=False)
        size_mb = output_files["grenzkupplung"].stat().st_size / (1024 * 1024)
        print(f"    ✓ {output_files['grenzkupplung'].name} ({size_mb:.1f} MB, {len(grenz_df):,} Zeilen)")

    # === CH-Aggregat ===
    print(f"  → CH-Aggregat-Spalten transformieren (wide)")
    aggregat_df = transform_ch_aggregat_wide(df, timestamp_utc)
    if not aggregat_df.empty:
        aggregat_df.to_parquet(output_files["ch_aggregat"], index=False)
        size_mb = output_files["ch_aggregat"].stat().st_size / (1024 * 1024)
        print(f"    ✓ {output_files['ch_aggregat'].name} ({size_mb:.1f} MB, {len(aggregat_df):,} Zeilen)")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Transform Swissgrid 15-Min-Daten in vier Faktentabellen"
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
        "--year", action="append", type=int, default=None,
        help="Nur ein spezifisches Jahr ziehen (mehrfach möglich)",
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
            print("FEHLER: Kein Snapshot mit Swissgrid-Daten gefunden.")
            sys.exit(1)

    snapshot_dir = SNAPSHOT_ROOT / snapshot_date

    # Verfügbare Files finden
    available_files = find_swissgrid_files(snapshot_dir)
    if not available_files:
        print(f"FEHLER: Keine Swissgrid-Files in {snapshot_dir / 'swissgrid'}.")
        sys.exit(1)

    # Welche Jahre verarbeiten?
    if args.year:
        years_to_process = []
        for y in args.year:
            if y not in available_files:
                print(f"FEHLER: Jahr {y} nicht verfügbar. "
                      f"Verfügbar: {sorted(available_files.keys())}")
                sys.exit(1)
            years_to_process.append(y)
    else:
        years_to_process = sorted(available_files.keys())

    # === Output-Datum ===
    intermediate_date = args.intermediate_date or date.today().isoformat()
    intermediate_dir = INTERMEDIATE_ROOT / intermediate_date
    intermediate_dir.mkdir(parents=True, exist_ok=True)

    print(f"Snapshot-Datum:       {snapshot_date}")
    print(f"Snapshot-Verzeichnis: {snapshot_dir}")
    print(f"Output-Datum:         {intermediate_date}")
    print(f"Output-Verzeichnis:   {intermediate_dir}")
    print(f"Jahre zu verarbeiten: {years_to_process}")
    if args.force:
        print("Modus: FORCE")

    # === Verarbeitung ===
    success_count = 0
    fail_count = 0

    for year in years_to_process:
        ok = transform_year(
            year, available_files[year],
            intermediate_dir, force=args.force,
        )
        if ok:
            success_count += 1
        else:
            fail_count += 1

    # === Manifest ===
    existing_manifest = load_manifest(intermediate_dir)
    if existing_manifest:
        manifest = existing_manifest
    else:
        manifest = init_manifest(intermediate_date, "transform_swissgrid.py")

    fact_dir = intermediate_dir / "fact"
    for year in years_to_process:
        for table_name in ["erzeugung", "verbrauch", "grenzkupplung", "ch_aggregat"]:
            file_path = fact_dir / f"swissgrid_{table_name}_15min_{year}.parquet"
            if file_path.exists():
                add_file_to_manifest(
                    manifest, "fact", f"swissgrid_{table_name}_15min", str(year),
                    file_path,
                    f"transform_swissgrid.py from {available_files[year].relative_to(PIPELINE_ROOT.parent)}",
                )

    manifest_path = write_manifest(manifest, intermediate_dir)

    print()
    print("=" * 60)
    print(f"Erfolgreich:  {success_count} / {len(years_to_process)}")
    if fail_count:
        print(f"Fehlgeschlagen: {fail_count}")
    print(f"Manifest:     {manifest_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()