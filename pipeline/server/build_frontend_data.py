"""
Serving-Schicht: erzeugt aus den Fact-Daten frontend-fertige JSON.
Schreibt nach <repo>/public/data/.

Outputs:
  verbrauch_national_daily.json    [{date, mwh}]
  verbrauch_national_monthly.json  [{date, mwh}]
  erzeugung_kanton_<jahr>.json     [{kanton, mwh, einheit, ist_gruppe}]  (26 Kantone)
  erzeugung_kanton_monat.json      [{kanton, date, mwh}]
  energiemix_monat.json            [{date, Laufwasser, Speicher, ...}]
  grenzfluss_monat.json            [{date, richtung_code, energie_mwh}]
  anlagen_standorte.json           [{typ, name, kanton_code, lat, lon, leistung_mw, produktion_gwh, ...}]
  gesamtenergie_sankey.json        {jahr: [{source, target, value}, ...]}   aus OGD115
  wetter_national_daily.json       [{date, temp, niederschlag, sonne, wolken, wind}]
  + kopiert: landesverbrauch_daily_anomaly.json, kanton_geometry.geojson
"""

from pathlib import Path
import glob
import json
import math
import shutil
import pandas as pd
import os

SNAPSHOT = os.environ.get("ENERGYVIZ_SNAPSHOT", "2026-05-10")
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


def _json_safe(obj):
    """Ersetzt NaN und inf rekursiv durch None.

    json.dumps schreibt NaN sonst woertlich in die Datei; das ist kein
    gueltiges JSON und laesst JSON.parse im Browser mit SyntaxError abbrechen
    (Ursache der unsichtbaren Standort-Marker). Betrifft z.B. Grenzkraftwerke
    ohne Schweizer kanton_code.
    """
    if isinstance(obj, float):
        return obj if math.isfinite(obj) else None
    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_json_safe(v) for v in obj]
    return obj


def write_json(name: str, payload):
    """Schreibt eine JSON nach OUT, NaN-sicher.

    _json_safe raeumt NaN/inf zu None, allow_nan=False wirkt als Riegel:
    kaeme je wieder ein NaN durch, scheitert der Build sofort statt still
    ungueltiges JSON zu schreiben.
    """
    (OUT / name).write_text(
        json.dumps(_json_safe(payload), ensure_ascii=False, allow_nan=False),
        encoding="utf-8")


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


def grenzfluss_monatlich() -> list:
    frames = []
    for pfad in sorted(FACT.glob("swissgrid_grenzkupplung_15min_*.parquet")):
        frames.append(pd.read_parquet(pfad))
    df = pd.concat(frames, ignore_index=True)

    df["jahr"] = df["zeitstempel_utc"].dt.year
    df["monat"] = df["zeitstempel_utc"].dt.month

    grp = (df.groupby(["jahr", "monat", "richtung_code"])["energie_mwh"]
             .sum()
             .reset_index())

    grp["date"] = pd.to_datetime(
        grp["jahr"].astype(str) + "-" + grp["monat"].astype(str).str.zfill(2) + "-01"
    ).dt.strftime("%Y-%m-%d")

    return grp[["date", "richtung_code", "energie_mwh"]].to_dict("records")


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


# === Anlagenstandorte ===

# Schweizer Kernkraftwerke: hardgecodet, weil die Standorte und Kennzahlen
# stabil und öffentlich sind (Bundesamt für Energie, ENSI). Mühleberg ist
# stillgelegt (2019), wird zur historischen Vollständigkeit mit aufgeführt.
KKW_STANDORTE = [
    {
        "typ": "Kernkraft", "name": "Beznau 1", "standort": "Döttingen",
        "kanton_code": "CH-AG", "typ_label": "Kernkraftwerk",
        "leistung_mw": 365.0, "produktion_gwh": 3000.0,
        "inbetriebnahme_jahr": 1969, "status_label": "im Normalbetrieb",
        "longitude": 8.2286, "latitude": 47.5525,
    },
    {
        "typ": "Kernkraft", "name": "Beznau 2", "standort": "Döttingen",
        "kanton_code": "CH-AG", "typ_label": "Kernkraftwerk",
        "leistung_mw": 365.0, "produktion_gwh": 3000.0,
        "inbetriebnahme_jahr": 1971, "status_label": "im Normalbetrieb",
        "longitude": 8.2286, "latitude": 47.5525,
    },
    {
        "typ": "Kernkraft", "name": "Gösgen", "standort": "Däniken",
        "kanton_code": "CH-SO", "typ_label": "Kernkraftwerk",
        "leistung_mw": 1010.0, "produktion_gwh": 8000.0,
        "inbetriebnahme_jahr": 1979, "status_label": "im Normalbetrieb",
        "longitude": 7.9689, "latitude": 47.3661,
    },
    {
        "typ": "Kernkraft", "name": "Leibstadt", "standort": "Leibstadt",
        "kanton_code": "CH-AG", "typ_label": "Kernkraftwerk",
        "leistung_mw": 1220.0, "produktion_gwh": 9500.0,
        "inbetriebnahme_jahr": 1984, "status_label": "im Normalbetrieb",
        "longitude": 8.1836, "latitude": 47.6019,
    },
    {
        "typ": "Kernkraft", "name": "Mühleberg", "standort": "Mühleberg",
        "kanton_code": "CH-BE", "typ_label": "Kernkraftwerk",
        "leistung_mw": 373.0, "produktion_gwh": 3000.0,
        "inbetriebnahme_jahr": 1972, "status_label": "stillgelegt (2019)",
        "longitude": 7.2686, "latitude": 46.9689,
    },
]

# Mapping von WASTA-Typ-Codes auf Anzeige-Labels
WASTA_TYP_LABELS = {
    "t1": "Laufkraftwerk",
    "t2": "Speicherkraftwerk",
    "t3": "Umwälzwerk",
    "t4": "Pumpspeicherkraftwerk",
}

# Filter-Schwellwert: nur Anlagen mit erwarteter Jahresproduktion oberhalb dieses
# Werts (in GWh) werden im Frontend gezeigt. Reduziert 723 auf rund 130-150 grosse
# Anlagen und hält die JSON-Datei klein. Kleinere Anlagen (< 20 GWh/Jahr) sind
# für die räumliche Übersicht ohnehin nicht relevant.
MIN_PRODUKTION_GWH = 20.0


def anlagen_standorte() -> list:
    """
    Kombiniert WASTA-Wasserkraftwerke (gefiltert auf grössere Anlagen im Betrieb)
    mit Kernkraftwerken zu einer einheitlichen Anlagen-Liste für die Frontend-Karte.
    """
    rows = []

    # === Wasserkraft aus WASTA ===
    wasta_pfad = DIM / "wasserkraftwerk.json"
    if wasta_pfad.exists():
        with open(wasta_pfad, encoding="utf-8") as f:
            wasta = json.load(f)

        eingang = len(wasta)
        for w in wasta:
            # Filter: nur im Normalbetrieb, mit Koordinaten und relevanter Grösse
            if w.get("status_code") != "os1":
                continue
            if w.get("longitude") is None or w.get("latitude") is None:
                continue
            produktion = w.get("produktion_erwartet_gwh") or 0.0
            if produktion < MIN_PRODUKTION_GWH:
                continue

            rows.append({
                "typ": "Wasserkraft",
                "name": w.get("name") or f"WASTA {w.get('wasta_nummer', '?')}",
                "standort": w.get("standort"),
                "kanton_code": w.get("kanton_code"),
                "typ_label": WASTA_TYP_LABELS.get(w.get("typ_code"), w.get("typ_label_de", "?")),
                "leistung_mw": round(float(w.get("leistung_turbine_max_mw") or 0.0), 1),
                "produktion_gwh": round(float(produktion), 1),
                "inbetriebnahme_jahr": w.get("inbetriebnahme_jahr"),
                "status_label": w.get("status_label_de", "im Normalbetrieb"),
                "longitude": round(float(w["longitude"]), 5),
                "latitude": round(float(w["latitude"]), 5),
            })
        print(f"  WASTA: {len(rows)} von {eingang} Anlagen nach Filter (>= {MIN_PRODUKTION_GWH} GWh/Jahr, im Normalbetrieb)")
    else:
        print(f"  ! WASTA-Datei nicht gefunden: {wasta_pfad}")

    # === Kernkraftwerke ===
    rows.extend(KKW_STANDORTE)
    print(f"  KKW: {len(KKW_STANDORTE)} Standorte (hardgecodet)")

    return rows


# === Gesamtenergiestatistik (OGD115) ===

# Struktur der Sankey: Träger (links) -> Verwendung (rechts)
GEST_TRAEGER = [
    "Elektrizität", "Erdölprodukte", "Gas", "Fernwärme",
    "Holzenergie", "Uebrige erneuerbare Energien",
    "Müll und Industrieabfälle", "Kohle",
]
# Sektor-Namen (kurz) -> BFE-Rubrik (voll)
GEST_SEKTOR_RUBRIK = {
    "Haushalte": "Endverbrauch - Haushalte",
    "Industrie": "Endverbrauch - Industrie",
    "Verkehr": "Endverbrauch - Verkehr",
    "Dienstleistungen": "Endverbrauch - Dienstleistungen",
    "Landwirtschaft": "Endverbrauch - Statistische Differenz inkl. Landwirtschaft",
}


def gesamtenergie_sankey() -> dict:
    """
    Erzeugt Sankey-Daten je Jahr aus der BFE-Gesamtenergiestatistik (OGD115).
    Rohdaten: Long-Format (Jahr, Rubrik, Energieträger, TJ).

    Datenquelle: sources.py-Eintrag "gesamtenergie_bilanz"
      -> Snapshot-Pfad: raw/snapshots/<snapshot>/bfe/gesamtenergie_bilanz.csv

    Output-Schema:
        {
          "1980": [{source, target, value}, ...],
          ...
          "2024": [...]
        }
    """
    # Neuesten Snapshot finden, der die OGD115-CSV enthaelt.
    # Entkoppelt vom global gepinnten SNAPSHOT, weil extract_bfe.py
    # immer in einen tagesdatierten Snapshot schreibt.
    snapshot_root = PIPELINE_ROOT / "raw" / "snapshots"
    kandidaten = sorted(
        snapshot_root.glob("*/bfe/gesamtenergie_bilanz.csv"),
        key=lambda p: p.parent.parent.name,  # ISO-Datum, lexikografisch = chronologisch
        reverse=True,
    )
    if not kandidaten:
        print(f"  ! OGD115 CSV in keinem Snapshot gefunden "
              f"({snapshot_root}\\*\\bfe\\gesamtenergie_bilanz.csv)")
        print(f"    Fuehre 'python pipeline/extract/extract_bfe.py --dataset gesamtenergie_bilanz' aus.")
        return {}
    src_pfad = kandidaten[0]
    df = pd.read_csv(src_pfad)
    df["TWh"] = df["TJ"] / 3600
    ergebnis = {}

    for jahr in sorted(df["Jahr"].unique()):
        d = df[df["Jahr"] == jahr]
        links = []

        # Endverbrauch je Sektor x Traeger
        for sektor_kurz, rubrik in GEST_SEKTOR_RUBRIK.items():
            sub = d[d["Rubrik"] == rubrik]
            for _, r in sub.iterrows():
                if r["Energietraeger"] in GEST_TRAEGER and r["TWh"] > 0.01:
                    links.append({
                        "source": r["Energietraeger"],
                        "target": sektor_kurz,
                        "value": round(float(r["TWh"]), 2),
                    })

        # Nichtenergetischer Verbrauch (Chemie, Kunststoffe)
        ne = d[d["Rubrik"] == "Nichtenergetischer Verbrauch"]
        for _, r in ne.iterrows():
            if r["Energietraeger"] in GEST_TRAEGER and r["TWh"] > 0.01:
                links.append({
                    "source": r["Energietraeger"],
                    "target": "Nichtenergetisch",
                    "value": round(float(r["TWh"]), 2),
                })

        # Nettoexport der Elektrizitaet als eigener Fluss (Bruttoverbrauch negativ = Export-Saldo)
        brutto_strom = d[(d["Rubrik"] == "Bruttoverbrauch") &
                         (d["Energietraeger"] == "Elektrizität")]["TWh"].sum()
        if brutto_strom < 0:
            links.append({
                "source": "Elektrizität",
                "target": "Export",
                "value": round(abs(float(brutto_strom)), 2),
            })

        # Umwandlungs- und Netzverluste
        verluste = d[d["Rubrik"] ==
                     "Eigenverbrauch des Energiesektors, Netzverluste, Verbrauch der Speicherungen"]
        for tr in ["Elektrizität", "Erdölprodukte", "Gas"]:
            v = verluste[verluste["Energietraeger"] == tr]["TWh"].sum()
            if v > 0.01:
                links.append({
                    "source": tr,
                    "target": "Verluste",
                    "value": round(float(v), 2),
                })

        ergebnis[int(jahr)] = links

    return ergebnis


# === Wetter (Open-Meteo) ===

def wetter_national_daily() -> list:
    """
    Erzeugt taegliche nationale Wetter-Aggregate aus dem stuendlichen Fact.

    Vorgehen: pro Tag pro Station aggregieren (Temperatur/Sonne/Wolken/Wind
    als Mittelwert, Niederschlag als Summe), dann ueber die 18 Kantonsstationen
    mitteln.

    Output-Schema:
        [{date, temp, niederschlag, sonne, wolken, wind}, ...]
    """
    pfad = FACT / "wetter_stuendlich.parquet"
    if not pfad.exists():
        print(f"  ! Wetter-Parquet nicht gefunden ({pfad})")
        return []

    df = pd.read_parquet(pfad)
    df["zeitstempel_utc"] = pd.to_datetime(df["zeitstempel_utc"], utc=True)
    df["datum"] = df["zeitstempel_utc"].dt.tz_convert("Europe/Zurich").dt.date

    # Pro Tag und Station
    tag_station = df.groupby(["datum", "wetterstation_code"]).agg({
        "temperature_2m": "mean",
        "precipitation": "sum",
        "shortwave_radiation": "mean",
        "cloud_cover": "mean",
        "wind_speed_10m": "mean",
    }).reset_index()

    # Nationaler Durchschnitt ueber die Stationen
    national = tag_station.groupby("datum").agg({
        "temperature_2m": "mean",
        "precipitation": "mean",
        "shortwave_radiation": "mean",
        "cloud_cover": "mean",
        "wind_speed_10m": "mean",
    }).reset_index()

    rows = []
    for _, r in national.iterrows():
        rows.append({
            "date": r["datum"].strftime("%Y-%m-%d"),
            "temp": round(float(r["temperature_2m"]), 1),
            "niederschlag": round(float(r["precipitation"]), 1),
            "sonne": int(round(float(r["shortwave_radiation"]))),
            "wolken": int(round(float(r["cloud_cover"]))),
            "wind": round(float(r["wind_speed_10m"]), 1),
        })
    return rows


def write_series(name: str, s: pd.Series):
    payload = [{"date": d.strftime("%Y-%m-%d"), "mwh": round(float(v), 1)} for d, v in s.items()]
    write_json(name, payload)
    print(f"  {name}  ({len(payload)} Punkte)")


def latest_full_year() -> int:
    years = [int(Path(f).stem.split("_")[-1])
             for f in glob.glob(str(FACT / "swissgrid_erzeugung_15min_*.parquet"))]
    return max(years)

def viertelstunde_pro_jahr(jahr: int) -> dict:
    """Viertelstundenprofil je Tag eines Jahres.

    Format: {"2022-08-19": [[minuten_seit_mitternacht, mwh], ...], ...}
    Die Minuten werden explizit gespeichert, weil Tage mit Zeitumstellung
    92 oder 100 statt 96 Werte haben.
    """
    f = FACT / f"swissgrid_ch_aggregat_15min_{jahr}.parquet"
    if not f.exists():
        return {}
    df = pd.read_parquet(f, columns=["zeitstempel_utc", VERBRAUCH_COL])
    df["zeitstempel_utc"] = pd.to_datetime(df["zeitstempel_utc"], utc=True)
    s = df.set_index("zeitstempel_utc")[VERBRAUCH_COL].sort_index()
    s.index = s.index.tz_convert("Europe/Zurich").tz_localize(None)
    out = {}
    for tag, grp in s.groupby(s.index.date):
        out[tag.strftime("%Y-%m-%d")] = [
            [int(ts.hour * 60 + ts.minute), round(float(v), 1)]
            for ts, v in grp.items()
        ]
    return out

def main():
    print("Serving-Schicht -> public/data/")
    daily = national_consumption()
    write_series("verbrauch_national_daily.json", daily)
    write_series("verbrauch_national_monthly.json", daily.resample("MS").sum())

    year = latest_full_year()
    rows = cantonal_generation_by_canton(year)
    write_json(f"erzeugung_kanton_{year}.json", rows)
    print(f"  erzeugung_kanton_{year}.json  ({len(rows)} Kantone)")

    monat = cantonal_generation_monthly()
    write_json("erzeugung_kanton_monat.json", monat)
    print(f"  erzeugung_kanton_monat.json  ({len(monat)} Kanton-Monate)")

    mix = energiemix_monatlich()
    write_json("energiemix_monat.json", mix)
    print(f"  energiemix_monat.json  ({len(mix)} Monate)")

    fluss = grenzfluss_monatlich()
    write_json("grenzfluss_monat.json", fluss)
    print(f"  grenzfluss_monat.json  ({len(fluss)} Zeilen)")

    anlagen = anlagen_standorte()
    write_json("anlagen_standorte.json", anlagen)
    print(f"  anlagen_standorte.json  ({len(anlagen)} Anlagen)")

    sankey = gesamtenergie_sankey()
    if sankey:
        write_json("gesamtenergie_sankey.json", sankey)
        print(f"  gesamtenergie_sankey.json  ({len(sankey)} Jahre)")

    wetter = wetter_national_daily()
    if wetter:
        write_json("wetter_national_daily.json", wetter)
        print(f"  wetter_national_daily.json  ({len(wetter)} Tage)")

    for src in [ANALYZE / "landesverbrauch_daily_anomaly.json",
                ANALYZE / "landesverbrauch_daily_decomp.json",
                ANALYZE / "wasserkraft_monthly_decomp.json",
                DIM / "kanton_geometry.geojson"]:
        if src.exists():
            shutil.copy(src, OUT / src.name)
            print(f"  kopiert: {src.name}")
        else:
            print(f"  (fehlt: {src.name})")

    vs_dir = OUT / "viertelstunde"
    vs_dir.mkdir(exist_ok=True)
    jahre = sorted(int(Path(f).stem.split("_")[-1])
                   for f in glob.glob(str(FACT / "swissgrid_ch_aggregat_15min_*.parquet")))
    n_tage = 0
    for j in jahre:
        tage = viertelstunde_pro_jahr(j)
        if not tage:
            continue
        (vs_dir / f"{j}.json").write_text(
            json.dumps(_json_safe(tage), ensure_ascii=False, allow_nan=False),
            encoding="utf-8")
        n_tage += len(tage)
    print(f"  viertelstunde/  ({len(jahre)} Jahre, {n_tage} Tage)")


if __name__ == "__main__":
    main()
