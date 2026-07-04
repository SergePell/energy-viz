"""
Stufe 1 der Analyse-Pipeline: Zeitreihenzerlegung (STL / MSTL).

Liest zwei Reihen aus den Fact-Tabellen eines Snapshots, zerlegt sie und
exportiert das Residuum als Bruecke zu Stufe 2 (Isolation Forest).

  taeglicher Verbrauch   <- swissgrid_ch_aggregat_15min_*.parquet  -> MSTL (7, 365)
  monatliche Wasserkraft <- bilanz_erzeugung_monat.json            -> STL  (12)

Liegt in pipeline/analyze/. Liest aus pipeline/intermediate/<snapshot>/fact/,
schreibt nach pipeline/output/analyze/.

Abhaengigkeiten: pandas, pyarrow, statsmodels >= 0.14, matplotlib
"""

from pathlib import Path
import glob
import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL, MSTL


# ============================================================
# CONFIG
# ============================================================
SNAPSHOT = "2026-05-10"                       # gegen welchen Stand gerechnet wird

PIPELINE_ROOT = Path(__file__).resolve().parent.parent   # .../pipeline
FACT = PIPELINE_ROOT / "intermediate" / SNAPSHOT / "fact"
OUTPUT = PIPELINE_ROOT / "output" / "analyze"
OUTPUT.mkdir(parents=True, exist_ok=True)

# Welche Swissgrid-Aggregatspalte als taeglicher "Landesverbrauch" dient.
# Designentscheidung (Decision-Log): Swissgrid kennt keinen Landesverbrauch im
# Sinne der BFE-Bilanz, verbrauch_total_mwh ist der naechstliegende Stellvertreter.
VERBRAUCH_COL = "verbrauch_total_mwh"

# Provisorische (nicht definitive) Monate am Reihenende verwerfen.
DROP_PROVISORISCH = True

HYDRO_CODES = ["wasserkraft_laufwerk", "wasserkraft_speicherwerk"]


# ============================================================
# Loader: zwei massgeschneiderte Funktionen fuer das echte Schema
# ============================================================
def load_daily_consumption() -> pd.Series:
    """Alle Jahres-Parquets des CH-Aggregats zusammenfuehren und auf
    Tagessumme (Schweizer Kalendertage) aggregieren."""
    files = sorted(glob.glob(str(FACT / "swissgrid_ch_aggregat_15min_*.parquet")))
    if not files:
        raise FileNotFoundError(f"Keine CH-Aggregat-Parquets in {FACT}")
    parts = [pd.read_parquet(f, columns=["zeitstempel_utc", VERBRAUCH_COL]) for f in files]
    df = pd.concat(parts, ignore_index=True)

    df["zeitstempel_utc"] = pd.to_datetime(df["zeitstempel_utc"], utc=True)
    s = df.set_index("zeitstempel_utc")[VERBRAUCH_COL].sort_index()

    # auf Schweizer Kalendertage beziehen, dann Tagessumme der 15-min-Energie
    s.index = s.index.tz_convert("Europe/Zurich")
    daily = s.resample("D").sum()
    daily.index = daily.index.tz_localize(None)   # naive Tagesdaten

    # Erster und letzter Kalendertag sind nach der Zeitzonen-Umrechnung Teiltage
    # (sie wuerden als kuenstliche Randausreisser erscheinen) -> abschneiden.
    daily = daily.iloc[1:-1]

    daily = daily.asfreq("D")
    miss = int(daily.isna().sum())
    if miss:
        daily = daily.interpolate(method="time", limit_direction="both")
        print(f"   {miss} fehlende Tage interpoliert")
    daily.name = "verbrauch_mwh_tag"
    return daily


def load_monthly_hydro() -> pd.Series:
    """Monatliche Wasserkraft = Lauf- plus Speicherwerk, pro Monat summiert."""
    with open(FACT / "bilanz_erzeugung_monat.json", encoding="utf-8") as f:
        df = pd.DataFrame(json.load(f))

    df = df[df["energieform_code"].isin(HYDRO_CODES)].copy()

    if DROP_PROVISORISCH and "ist_definitiv" in df.columns:
        prov = df.groupby(["jahr", "monat"])["ist_definitiv"].transform("min").astype(bool)
        n_prov = int((~prov).groupby([df["jahr"], df["monat"]]).first().sum())
        df = df[prov]
        if n_prov:
            print(f"   {n_prov} provisorische Monate verworfen")

    monthly = df.groupby(["jahr", "monat"])["erzeugung_mwh"].sum()
    idx = pd.to_datetime(
        monthly.index.get_level_values("jahr").astype(str) + "-"
        + monthly.index.get_level_values("monat").astype(str).str.zfill(2) + "-01"
    )
    s = pd.Series(monthly.values, index=idx, name="wasserkraft_mwh").sort_index()
    s = s.asfreq("MS")
    miss = int(s.isna().sum())
    if miss:
        s = s.interpolate(method="time", limit_direction="both")
        print(f"   {miss} fehlende Monate interpoliert")
    return s


# ============================================================
# Zerlegung, Plot, Export
# ============================================================
def plot(name, res):
    fig = res.plot()
    fig.set_size_inches(11, 8)
    fig.suptitle(name, y=1.01)
    fig.tight_layout()
    out = OUTPUT / f"{name}_decomposition.png"
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"   Plot -> {out}")


def export_resid(name, resid):
    out = OUTPUT / f"{name}_resid.json"
    payload = [
        {"date": d.strftime("%Y-%m-%d"),
         "resid": (None if pd.isna(v) else round(float(v), 4))}
        for d, v in resid.items()
    ]
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"   Residuum -> {out}  ({len(payload)} Punkte)")


def run(name, series, method, periods):
    print(f"\n== {name} ({method}) ==")
    print(f"   {len(series)} Punkte, {series.index.min().date()} bis {series.index.max().date()}")
    if method == "MSTL":
        res = MSTL(series, periods=periods).fit()
    else:
        res = STL(series, period=periods, robust=True).fit()
    print(f"   Residuum: mean={res.resid.mean():.2f}  std={res.resid.std():.2f}")
    plot(name, res)
    export_resid(name, res.resid)


def main():
    run("landesverbrauch_daily", load_daily_consumption(), "MSTL", (7, 365))
    run("wasserkraft_monthly", load_monthly_hydro(), "STL", 12)


if __name__ == "__main__":
    main()
