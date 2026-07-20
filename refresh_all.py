#!/usr/bin/env python3
"""
refresh_all.py — Vollstaendiger Pipeline-Neulauf fuer einen frischen, kohaerenten Snapshot.

ZWECK
    Zieht alle Quellen neu, transformiert sie und baut die Serving-Schicht,
    damit das Dashboard fuer eine Praesentation aktuelle Daten zeigt.

    WICHTIG: Das ist NICHT der Normalbetrieb. Die Thesis-Baseline ist bewusst
    eingefroren (SNAPSHOT in build_frontend_data.py). Dieses Skript erzeugt
    einen NEUEN, tagesdatierten Snapshot und laesst die eingefrorene Baseline
    im Code unangetastet. Es laeuft nur, wenn man es ausdruecklich will.

BENUTZUNG (aus dem Repo-Wurzelverzeichnis)
    python pipeline/refresh_all.py            # Dry-Run: zeigt nur, was liefe
    python pipeline/refresh_all.py --yes      # fuehrt den Neulauf wirklich aus
    python pipeline/refresh_all.py --yes --force   # ignoriert die Monats-Sperre

MONATS-LOGIK
    Ohne --force verweigert das Skript den Lauf, wenn der neueste Snapshot
    juenger als MIN_ABSTAND_TAGE ist. So aktualisiert man hoechstens einmal
    im Monat und ueberschreibt nicht versehentlich frische Daten.

KOHAERENZ
    Damit die Praesentation wirklich frische Daten zeigt, muessen ALLE
    Extract- UND Transform-Schritte in SCHRITTE stehen. Grund: das Skript
    setzt ENERGYVIZ_SNAPSHOT=<heute> in die Umgebung. build_frontend_data.py
    (und ggf. deine Transform-Skripte) lesen diese Variable als Override fuer
    ihre SNAPSHOT-Konstante und arbeiten dann auf dem heutigen Snapshot.
    Fehlt ein Transform-Schritt, existiert intermediate/<heute>/ nicht und
    der Build laeuft ins Leere.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import subprocess
import sys
from pathlib import Path

# --- Pfade -----------------------------------------------------------------
# Diese Datei liegt in pipeline/, also ist parent = pipeline/ und
# parent.parent = Repo-Wurzel. Die Schritte werden aus der Wurzel gestartet,
# damit relative Pfade wie "pipeline/extract/..." aufgehen.
PIPELINE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PIPELINE_DIR.parent
SNAPSHOT_ROOT = PIPELINE_DIR / "raw" / "snapshots"

# --- Konfiguration ---------------------------------------------------------
# Mindestabstand zwischen zwei Neulaeufen in Tagen. 28 ~ "einmal im Monat".
MIN_ABSTAND_TAGE = 28

# Ziel-Snapshot dieses Laufs (heutiges Datum im ISO-Format, z.B. "2026-07-05").
HEUTE = dt.date.today().isoformat()

# Erkennt Snapshot-Ordner der Form JJJJ-MM-TT.
DATUM_MUSTER = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# --- Die Schritte, in Ausfuehrungsreihenfolge ------------------------------
# Jeder Eintrag ist eine Kommandozeile als Liste (subprocess-Form, keine Shell).
# "{py}" wird durch den aktuell laufenden Python-Interpreter ersetzt, damit
# der Lauf dein venv verwendet.
#
# >>> HIER AN DEINE ECHTEN SKRIPTE ANPASSEN <<<
# Ich habe die zwei Schritte vorgetragen, die ich sicher kenne. Die TODOs
# fuellst du mit deinen tatsaechlichen Extract-/Transform-Aufrufen. Wenn du
# mir die Dateinamen schickst, ergaenze ich die Liste exakt.
SCHRITTE = [
    # 1) EXTRAHIEREN  ->  raw/snapshots/<heute>/
    ["{py}", "pipeline/extract/extract_bfe.py", "--dataset", "gesamtenergie_bilanz"],
    # TODO weitere BFE-Datensaetze (OGD32, OGD123, ...):
    # ["{py}", "pipeline/extract/extract_bfe.py", "--dataset", "<name>"],
    # TODO Wetter / Swissgrid / swisstopo, deine echten Extract-Skripte:
    # ["{py}", "pipeline/extract/extract_wetter.py"],

    # 2) TRANSFORMIEREN  ->  intermediate/<heute>/
    # TODO deine Transform-Skripte in der richtigen Reihenfolge:
    # ["{py}", "pipeline/transform/transform_wetter.py"],

    # 3) SERVING-SCHICHT BAUEN  ->  public/data/
    ["{py}", "pipeline/server/build_frontend_data.py"],
]


def neuester_snapshot() -> dt.date | None:
    """Gibt das Datum des juengsten Snapshot-Ordners zurueck, oder None."""
    if not SNAPSHOT_ROOT.exists():
        return None
    daten = []
    for p in SNAPSHOT_ROOT.iterdir():
        if p.is_dir() and DATUM_MUSTER.match(p.name):
            try:
                daten.append(dt.date.fromisoformat(p.name))
            except ValueError:
                pass  # Ordner mit passendem Muster aber unmoeglichem Datum ignorieren
    return max(daten) if daten else None


def monats_sperre_greift(force: bool) -> tuple[bool, str]:
    """
    Prueft die Monats-Sperre.
    Rueckgabe: (gesperrt?, erklaerender Text).
    """
    if force:
        return False, "--force gesetzt, Monats-Sperre uebersprungen."
    neuest = neuester_snapshot()
    if neuest is None:
        return False, "Noch kein Snapshot vorhanden, Neulauf erlaubt."
    alter = (dt.date.today() - neuest).days
    if alter < MIN_ABSTAND_TAGE:
        return True, (f"Neuester Snapshot ist {neuest.isoformat()} "
                      f"({alter} Tage alt, < {MIN_ABSTAND_TAGE}). "
                      f"Mit --force erzwingen.")
    return False, (f"Neuester Snapshot ist {neuest.isoformat()} "
                   f"({alter} Tage alt), Neulauf erlaubt.")


def schritt_ausfuehren(cmd: list[str], env: dict, dry_run: bool) -> None:
    """Fuehrt einen Schritt aus. Bei Fehler wird sofort abgebrochen."""
    aufgeloest = [sys.executable if teil == "{py}" else teil for teil in cmd]
    lesbar = " ".join(aufgeloest)
    if dry_run:
        print(f"  [DRY-RUN] {lesbar}")
        return
    print(f"  -> {lesbar}")
    ergebnis = subprocess.run(aufgeloest, cwd=REPO_ROOT, env=env)
    if ergebnis.returncode != 0:
        # Fail-fast: kein halber Snapshot wird weiterverarbeitet.
        raise SystemExit(
            f"\nSchritt fehlgeschlagen (Exit {ergebnis.returncode}): {lesbar}\n"
            f"Abbruch. Es wird kein halb gefuellter Snapshot weiterverarbeitet."
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Vollstaendiger Pipeline-Neulauf fuer einen frischen Snapshot."
    )
    parser.add_argument("--yes", action="store_true",
                        help="Neulauf wirklich ausfuehren (ohne dies nur Dry-Run).")
    parser.add_argument("--force", action="store_true",
                        help="Monats-Sperre ignorieren.")
    args = parser.parse_args()

    print("=" * 60)
    print(f"Pipeline-Neulauf  |  Ziel-Snapshot: {HEUTE}")
    print("=" * 60)

    gesperrt, grund = monats_sperre_greift(args.force)
    print(grund)
    if gesperrt:
        raise SystemExit("Nichts getan.")

    dry_run = not args.yes
    if dry_run:
        print("\nDRY-RUN (kein --yes). Es wird nur angezeigt, was liefe:\n")
    else:
        print("\nAusfuehrung startet. Bei einem Fehler wird sofort abgebrochen.\n")

    # Kindprozesse bekommen den Ziel-Snapshot als Umgebungsvariable.
    # So arbeiten build_frontend_data.py und (falls angepasst) die Transform-
    # Skripte auf dem heutigen Snapshot, ohne die eingefrorene Baseline im
    # Code zu veraendern.
    env = os.environ.copy()
    env["ENERGYVIZ_SNAPSHOT"] = HEUTE

    for i, cmd in enumerate(SCHRITTE, start=1):
        print(f"Schritt {i}/{len(SCHRITTE)}:")
        schritt_ausfuehren(cmd, env, dry_run)

    print("\n" + "=" * 60)
    if dry_run:
        print("Dry-Run beendet. Mit --yes wirklich ausfuehren.")
    else:
        print(f"Fertig. Frischer Snapshot: {HEUTE}")
        print("Die eingefrorene Thesis-Baseline im Code bleibt unveraendert.")
    print("=" * 60)


if __name__ == "__main__":
    main()
