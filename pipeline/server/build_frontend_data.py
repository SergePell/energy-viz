"""
Serving-Schicht: erzeugt aus den Fact-Daten frontend-fertige JSON.
Schreibt nach <repo>/public/data/.

Outputs:
  verbrauch_national_daily.json    [{date, mwh}]
  verbrauch_national_monthly.json  [{date, mwh}]
  erzeugung_kanton_<jahr>.json     [{kanton, mwh, einheit, ist_gruppe}]  (26 Kantone)
  + kopiert: landesverbrauch_daily_anomaly.json, kanton_geometry.geojson
"""

from pathlib import Path
import glob
import json
import shutil
import pandas as pd

SNAPSHOT = "2026-05-10"
PIPELINE_ROOT = Path(__file__).resolve().parent.parent
FACT = PIPELINE_ROOT / "intermediate" / SNAPSHOT / "fact"
DIM = PIPELINE_ROOT / "intermediate" / SNAPSHOT / "dim"
ANALYZE = PIPELINE_ROOT / "output" / "analyze"
OUT = PIPELINE_ROOT.parent / "public" / "data"
OUT.mkdir(parents=True, exist_ok=True)

VERBRAUCH_COL = "verbrauch_total_mwh"

# Swissgrid-Einheit -> ISO-Kantonscode(s). 7 Gruppen teilen ihren Wert.
EINHEIT_KANTONE = {
    "CH-AG": ["CH-AG"], "CH-FR": ["CH-FR"], "CH-GL": ["CH-GL"], "CH-GR": ["CH-GR"],
    "CH-LU": ["CH-LU"], "CH-NE": ["CH-NE"], "CH-SO": ["CH-SO"], "CH-SG": ["CH-SG"],
    "CH-TI": ["CH-TI"], "CH-TG": ["CH-TG"], "CH-VS": ["CH-VS"],
    "CH-AI_AR": ["CH-AI", "CH-AR"],
    "CH-BL_BS": ["CH-BL", "CH-BS"],
    "CH-BE_JU": ["CH-BE", "CH-JU"],
    "CH-SZ_ZG": ["CH-SZ", "CH-ZG"],
    "CH-OW_NW_UR": ["CH-OW", "CH-NW", "CH-UR"],
    "CH-GE_VD": ["CH-GE", "CH-VD"],
    "CH-SH_ZH": ["CH-SH", "CH-ZH"],
}


def national_consumption() -> pd.Series:
    files = sorted(glob.glob(str(FACT / "swissgrid_ch_aggregat_15min_*.parquet")))
    parts = [pd.read_parquet(f, columns=["zeitstempel_utc", VERBRAUCH_COL]) for f in files]
    df = pd.concat(parts, ignore_index=True)
    df["zeitstempel_utc"] = pd.to_datetime(df["zeitstempel_utc"], utc=True)
    s = df.set_index("zeitstempel_utc")[VERBRAUCH_COL].sort_index()
    s.index = s.index.tz_convert("Europe/Zurich")
    daily = s.resample("D").sum()
    daily.index = daily.index.tz_localize(None)
    return daily.iloc[1:-1]


def cantonal_generation_by_canton(year: int) -> list:
    """Gesamterzeugung je Einheit, aufgeloest auf 26 Kantone (Gruppen teilen ihren Wert)."""
    f = FACT / f"swissgrid_erzeugung_15min_{year}.parquet"
    gen = pd.read_parquet(f, columns=["swissgrid_einheit", "erzeugung_mwh"]) \
            .groupby("swissgrid_einheit")["erzeugung_mwh"].sum()
    rows = []
    for einheit, mwh in gen.items():
        kantone = EINHEIT_KANTONE.get(einheit)
        if not kantone:
            continue                                   # uebergreifend / Ausland weglassen
        ist_gruppe = len(kantone) > 1
        for k in kantone:
            rows.append({"kanton": k, "mwh": round(float(mwh), 1),
                         "einheit": einheit, "ist_gruppe": ist_gruppe})
    return rows



def cantonal_generation_monthly() -> list:
    """Monatliche Erzeugung je Kanton (alle Jahre), Gruppen auf Kantone aufgeloest."""
    files = sorted(glob.glob(str(FACT / "swissgrid_erzeugung_15min_*.parquet")))
    parts = [pd.read_parquet(f, columns=["zeitstempel_utc", "swissgrid_einheit", "erzeugung_mwh"])
             for f in files]
    df = pd.concat(parts, ignore_index=True)
    df["zeitstempel_utc"] = pd.to_datetime(df["zeitstempel_utc"], utc=True)
    df["zeitstempel_utc"] = df["zeitstempel_utc"].dt.tz_convert("Europe/Zurich")
    df["monat"] = df["zeitstempel_utc"].dt.tz_localize(None).dt.to_period("M").dt.to_timestamp()
    g = df.groupby(["swissgrid_einheit", "monat"])["erzeugung_mwh"].sum().reset_index()
    rows = []
    for _, r in g.iterrows():
        for k in EINHEIT_KANTONE.get(r["swissgrid_einheit"], []):
            rows.append({"kanton": k, "date": r["monat"].strftime("%Y-%m-%d"),
                         "mwh": round(float(r["erzeugung_mwh"]), 1)})
    return rows



# Energiemix aus bilanz_erzeugung_monat.json (Long-Format, energieform_code).
# Codes -> Anzeigenamen. PASSE DIE LINKE SEITE AN DIE ECHTEN CODES AN.
MIX_CODES = {
    "wasserkraft_laufwerk": "Laufwasser",
    "wasserkraft_speicherwerk": "Speicher",
    "kernkraft": "Kernkraft",
    "photovoltaik": "Photovoltaik",
    "wind": "Wind",
    "thermisch_aggregiert": "Thermisch",
    "andere_aggregiert": "Andere",
}


def energiemix_monatlich() -> list:
    """Monatlicher Mix in GWh je Energieform aus dem Long-Fact, nur definitive Monate."""
    df = pd.read_json(FACT / "bilanz_erzeugung_monat.json")
    if "ist_definitiv" in df.columns:
        df = df[df["ist_definitiv"] == True]
    df["date"] = pd.to_datetime(dict(year=df["jahr"], month=df["monat"], day=1))
    df["name"] = df["energieform_code"].map(MIX_CODES)
    unbekannt = sorted(df.loc[df["name"].isna(), "energieform_code"].unique())
    if unbekannt:
        print(f"  ! unbekannte energieform_code (nicht im Mapping): {unbekannt}")
    df = df.dropna(subset=["name"])
    # erzeugung_mwh -> GWh, je Monat und Energieform summieren, dann breit machen
    df["gwh"] = df["erzeugung_mwh"] / 1000.0
    piv = df.pivot_table(index="date", columns="name", values="gwh", aggfunc="sum").fillna(0.0)
    rows = []
    for d, r in piv.sort_index().iterrows():
        eintrag = {"date": d.strftime("%Y-%m-%d")}
        for name in MIX_CODES.values():
            eintrag[name] = round(float(r.get(name, 0.0)), 1)
        rows.append(eintrag)
    return rows


def write_series(name: str, s: pd.Series):
    payload = [{"date": d.strftime("%Y-%m-%d"), "mwh": round(float(v), 1)} for d, v in s.items()]
    (OUT / name).write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print(f"  {name}  ({len(payload)} Punkte)")


def latest_full_year() -> int:
    years = [int(Path(f).stem.split("_")[-1])
             for f in glob.glob(str(FACT / "swissgrid_erzeugung_15min_*.parquet"))]
    return max(years)


def main():
    print("Serving-Schicht -> public/data/")
    daily = national_consumption()
    write_series("verbrauch_national_daily.json", daily)
    write_series("verbrauch_national_monthly.json", daily.resample("MS").sum())

    year = latest_full_year()
    rows = cantonal_generation_by_canton(year)
    (OUT / f"erzeugung_kanton_{year}.json").write_text(
        json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    print(f"  erzeugung_kanton_{year}.json  ({len(rows)} Kantone)")

    monat = cantonal_generation_monthly()
    (OUT / "erzeugung_kanton_monat.json").write_text(
        json.dumps(monat, ensure_ascii=False), encoding="utf-8")
    print(f"  erzeugung_kanton_monat.json  ({len(monat)} Kanton-Monate)")

    mix = energiemix_monatlich()
    (OUT / "energiemix_monat.json").write_text(
        json.dumps(mix, ensure_ascii=False), encoding="utf-8")
    print(f"  energiemix_monat.json  ({len(mix)} Monate)")

    for src in [ANALYZE / "landesverbrauch_daily_anomaly.json",
                DIM / "kanton_geometry.geojson"]:
        if src.exists():
            shutil.copy(src, OUT / src.name)
            print(f"  kopiert: {src.name}")
        else:
            print(f"  (fehlt: {src.name})")


if __name__ == "__main__":
    main()