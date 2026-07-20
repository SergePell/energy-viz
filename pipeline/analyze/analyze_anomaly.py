"""
Stufe 2 der Analyse-Pipeline: Anomalieerkennung mit Isolation Forest.

Liest die Residuen aus Stufe 1 und bewertet jeden Zeitpunkt:
- univariate Baseline (nur Residuum)
- multivariater Forest mit schrittweise wachsendem Kontext (Temperatur,
  Preis, Strahlung, Niederschlag)

Feiertage werden NICHT als Modellmerkmal genutzt (ein seltenes Binaerflag
bildet eine eigene kleine Gruppe und wird dadurch erst recht isoliert).
Stattdessen wird je Tag mitexportiert, ob er ein de-facto landesweiter
Feiertag ist. Die Entscheidung, ab welchem Score ein Tag als Anomalie gilt,
faellt im Frontend ueber den justierbaren Schwellenwert. Dieses Skript
exportiert nur den Score und den Kontext, keine fertige Klassifikation.

Abhaengigkeiten: pandas, pyarrow, scikit-learn, holidays
"""

from pathlib import Path
from collections import Counter
import json
import os
import pandas as pd
from sklearn.ensemble import IsolationForest
import holidays


# ============================================================
# CONFIG
# ============================================================
SNAPSHOT = os.environ.get("ENERGYVIZ_SNAPSHOT", "2026-05-10")
PIPELINE_ROOT = Path(__file__).resolve().parent.parent
FACT = PIPELINE_ROOT / "intermediate" / SNAPSHOT / "fact"
ANALYZE = PIPELINE_ROOT / "output" / "analyze"

IF_PARAMS = dict(n_estimators=100, max_samples=256, random_state=42)

# Liu et al. (2008) begegnen Swamping und Masking durch kleine Stichproben.
# Bei den Monatsreihen (n rund 300 bzw. 96) wuerde max_samples=256 fast den
# ganzen Datensatz umfassen und das Subsampling aushebeln. Deshalb ein
# reihenspezifischer Wert.
# Decision-Log: verworfen wurde ein einheitliches max_samples=256.
MAX_SAMPLES_KURZ = 64

# Ein Tag gilt als (de-facto landesweiter) Feiertag, wenn er in mindestens
# so vielen Kantonen offizieller Feiertag ist. 14 von 26 = Mehrheit.
# Decision-Log: Berchtoldstag liegt knapp darunter.
KANTON_SCHWELLE = 14
JAHRE = range(2009, 2027)


def build_feiertage(jahre, schwelle) -> dict:
    """De-facto landesweite Feiertage durch Aggregation ueber alle Kantone."""
    # 'Stadt Zurich' ist kein Kanton, sondern eine Stadt; der Kanton ZH ist
    # separat enthalten. Ohne Ausschluss wuerden Zuercher Feiertage doppelt zaehlen.
    subs = [s for s in holidays.Switzerland().subdivisions if s != "Stadt Zurich"]
    result = {}
    for y in jahre:
        cnt, nm = Counter(), {}
        for sd in subs:
            for d, n in holidays.Switzerland(subdiv=sd, years=[y]).items():
                cnt[d] += 1
                nm[d] = n
        for d, c in cnt.items():
            if c >= schwelle:
                result[d] = nm[d]
    return result


FEIERTAGE = build_feiertage(JAHRE, KANTON_SCHWELLE)


# ============================================================
# Laden / Aggregieren
# ============================================================
def load_resid(name: str) -> pd.Series:
    with open(ANALYZE / f"{name}_resid.json", encoding="utf-8") as f:
        df = pd.DataFrame(json.load(f))
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")["resid"].astype(float)


def daily_from_parquet(path: Path, value_col: str, how: str) -> pd.Series:
    df = pd.read_parquet(path, columns=["zeitstempel_utc", value_col])
    df["zeitstempel_utc"] = pd.to_datetime(df["zeitstempel_utc"], utc=True)
    s = df.set_index("zeitstempel_utc")[value_col].sort_index()
    s.index = s.index.tz_convert("Europe/Zurich")
    out = getattr(s.resample("D"), how)()
    out.index = out.index.tz_localize(None)
    return out


def is_feiertag(d) -> bool:
    return d.date() in FEIERTAGE


# ============================================================
# Modell
# ============================================================
def score_if(df: pd.DataFrame, feature_cols: list, max_samples=None) -> pd.Series:
    X = df[feature_cols].astype(float).values
    params = dict(IF_PARAMS)
    if max_samples is not None:
        params["max_samples"] = max_samples
    model = IsolationForest(**params).fit(X)
    return pd.Series(model.score_samples(X), index=df.index)  # tief = anomal


def to_anomaly_score(score: pd.Series) -> pd.Series:
    """sklearn.score_samples liefert -s(x,n). Rueckumkehr ergibt Lius
    Anomalie-Score s(x,n) in (0,1]: nahe 1 = klare Anomalie, deutlich
    unter 0.5 = normal, alle Werte um 0.5 = keine ausgepraegten Anomalien
    (Liu et al., 2008). Bewusst keine Min-Max-Skalierung, damit die Werte
    zwischen Reihen und Laeufen vergleichbar bleiben."""
    return -score


def print_top(name: str, df: pd.DataFrame, score: pd.Series, feature_cols: list,
              ohne_feiertage: bool, feiertage_aktiv: bool = True):
    print(f"\n  [{name}]  {', '.join(feature_cols)}")
    s = score.sort_values()
    shown = 0
    for d, sc in s.items():
        if feiertage_aktiv and is_feiertag(d):
            if ohne_feiertage:
                continue
            tag = f"  (Feiertag: {FEIERTAGE[d.date()]})"
        else:
            tag = ""
        print(f"     {d.date()}  score={sc:+.3f}{tag}")
        shown += 1
        if shown >= 8:
            break
    if ohne_feiertage:
        print(f"     (Feiertage aus der Liste ausgeblendet, erklaert)")


def export(name: str, df: pd.DataFrame, score: pd.Series, feature_cols: list,
           feiertage_aktiv: bool = True):
    """Exportiert Score und Kontext je Tag.

    Bewusst keine Klassifikation in normal/anomal: Diese Entscheidung faellt
    im Frontend ueber den justierbaren Schwellenwert. Eine zweite, offline
    fixierte Schwelle wuerde zu zwei widerspruechlichen Anomaliedefinitionen
    im selben Projekt fuehren.
    """
    asc = to_anomaly_score(score)
    out = []
    for d in df.index:
        rec = {"date": d.strftime("%Y-%m-%d"),
               "resid": round(float(df.loc[d, "resid"]), 2)}
        for c in feature_cols:
            if c != "resid":
                rec[c] = round(float(df.loc[d, c]), 3)
        rec["is_feiertag"] = bool(feiertage_aktiv and is_feiertag(d))
        rec["feiertag_name"] = FEIERTAGE.get(d.date())
        rec["anomaly_score"] = round(float(asc.loc[d]), 4)
        out.append(rec)
    p = ANALYZE / f"{name}_anomaly.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"  -> {p.name}: {len(out)} Tage, "
          f"Score {asc.min():.3f} bis {asc.max():.3f} "
          f"(Median {asc.median():.3f}, 99%-Quantil {asc.quantile(0.99):.3f})")


# ============================================================
# Reihen
# ============================================================
def analyse_verbrauch():
    print("\n================ VERBRAUCH (taeglich) ================")
    df = pd.DataFrame({"resid": load_resid("landesverbrauch_daily")}).dropna()

    have_ctx = True
    try:
        wetter = FACT / "wetter_stuendlich.parquet"
        df["temp"] = daily_from_parquet(wetter, "temperature_2m", "mean")
        df["strahlung"] = daily_from_parquet(wetter, "shortwave_radiation", "mean")
        df["niederschlag"] = daily_from_parquet(wetter, "precipitation", "mean")
        df["preis"] = daily_from_parquet(FACT / "strompreis_stuendlich.parquet",
                                         "preis_eur_mwh", "mean")
    except FileNotFoundError as e:
        have_ctx = False
        print(f"  (Kontext-Parquet fehlt, nur Baseline: {e.filename})")

    # E0: naive Baseline, Feiertage SICHTBAR (zeigt das Problem)
    print_top("E0 Baseline univariat", df, score_if(df, ["resid"]), ["resid"],
              ohne_feiertage=False)

    if have_ctx:
        d2 = df.dropna(subset=["temp", "preis", "strahlung", "niederschlag"])
        print(f"  (multivariater Zeitraum: {d2.index.min().date()} bis "
              f"{d2.index.max().date()}, {len(d2)} Tage)")
        # E1-E3: Kontext, Feiertage erklaert (ausgeblendet) -> echte Anomalien
        print_top("E1 +Temperatur", d2, score_if(d2, ["resid", "temp"]),
                  ["resid", "temp"], ohne_feiertage=True)
        print_top("E2 +Preis", d2, score_if(d2, ["resid", "temp", "preis"]),
                  ["resid", "temp", "preis"], ohne_feiertage=True)
        feats = ["resid", "temp", "preis", "strahlung", "niederschlag"]
        sc = score_if(d2, feats)
        print_top("E3 +Strahlung +Niederschlag", d2, sc, feats, ohne_feiertage=True)
        export("landesverbrauch_daily", d2, sc, feats)
    else:
        sc = score_if(df, ["resid"])
        export("landesverbrauch_daily", df, sc, ["resid"])


def monthly_precip_anom(path: Path) -> pd.DataFrame:
    """Nationaler Monatsniederschlag, saisonbereinigt (Anomalie + 3-Monats-Mittel)."""
    df = pd.read_parquet(path, columns=["zeitstempel_utc", "precipitation"])
    df["zeitstempel_utc"] = pd.to_datetime(df["zeitstempel_utc"], utc=True)
    s = df.set_index("zeitstempel_utc")["precipitation"].sort_index()
    s.index = s.index.tz_convert("Europe/Zurich")
    m = s.resample("MS").mean()
    m.index = m.index.tz_localize(None)
    clim = m.groupby(m.index.month).transform("mean")     # Monats-Klimatologie
    anom = (m - clim)
    return pd.DataFrame({"niederschlag_anom": anom,
                         "niederschlag_3m": anom.rolling(3, min_periods=1).mean()})


def analyse_wasserkraft():
    print("\n================ WASSERKRAFT (monatlich) ================")
    df = pd.DataFrame({"resid": load_resid("wasserkraft_monthly")}).dropna()

    # Hauptartefakt: Baseline univariat auf der vollen Reihe (ab 2000).
    # max_samples reihenspezifisch, sonst saehe jeder Baum 85 % der Daten.
    sc = score_if(df, ["resid"], max_samples=MAX_SAMPLES_KURZ)
    print_top("Baseline univariat (volle Reihe)", df, sc, ["resid"],
              ohne_feiertage=False, feiertage_aktiv=False)
    export("wasserkraft_monthly", df, sc, ["resid"], feiertage_aktiv=False)

    # Experiment daneben: Niederschlag als Erklaerungsgroesse (nur 2017+)
    wetter = FACT / "wetter_stuendlich.parquet"
    if wetter.exists():
        d2 = df.join(monthly_precip_anom(wetter)).dropna(subset=["niederschlag_anom"])
        feats = ["resid", "niederschlag_anom", "niederschlag_3m"]
        # Frueher stand hier min(256, len(d2)). Das ergab max_samples = n und
        # damit gar kein Subsampling; zugleich unterdrueckte es die
        # sklearn-Warnung, die auf genau dieses Problem hingewiesen haette.
        sc2 = score_if(d2, feats, max_samples=MAX_SAMPLES_KURZ)
        print_top("Experiment +Niederschlag (ab 2017)", d2, sc2, feats,
                  ohne_feiertage=False, feiertage_aktiv=False)


def main():
    analyse_verbrauch()
    analyse_wasserkraft()


if __name__ == "__main__":
    main()
