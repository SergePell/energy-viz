"""
Quellen-Konfiguration für die Extract-Pipeline.

Jede Quelle ist ein Eintrag mit:
- slug: opendata.swiss Dataset-Slug (Teil der URL nach /dataset/)
- preferred_formats: Liste der gewünschten Formate, in Reihenfolge der Priorität
- rq_bezug: Welche Forschungsfrage(n) bedient die Quelle
- priority: A (Kern), B (Stretch), C (nur Kontext)
- notes: Kurze inhaltliche Notiz für Dokumentation

Ergänzungen einer neuen Quelle: einfach einen weiteren Eintrag im SOURCES-Dict.
"""

SOURCES = {
    # === Anlagen-Stammdaten (Geo + Stammdaten) ===
    "pv_grossanlagen": {
        "slug": "photovoltaik-grossanlagen-in-der-schweiz",
        "preferred_formats": ["CSV", "GeoPackage"],
        "rq_bezug": "RQ, SQ-1",
        "priority": "A",
        "notes": "Standorte und Leistungen der PV-Grossanlagen, Stammdaten",
    },
    "windenergieanlagen": {
        "slug": "windenergieanlagen",
        "preferred_formats": ["CSV", "GeoPackage"],
        "rq_bezug": "RQ, SQ-1",
        "priority": "A",
        "notes": "Standorte und Leistungen Windenergieanlagen, Stammdaten",
    },
    "biogasanlagen": {
        "slug": "biogasanlagen",
        "preferred_formats": ["CSV", "GeoPackage"],
        "rq_bezug": "RQ, SQ-1",
        "priority": "A",
        "notes": "Standorte und Leistungen Biogasanlagen, Stammdaten",
    },
    "wasta_wasserkraft": {
        "slug": "statistik-der-wasserkraftanlagen-wasta",
        "preferred_formats": ["CSV", "GeoPackage"],
        "rq_bezug": "RQ, SQ-1",
        "priority": "A",
        "notes": "WASTA — Wasserkraftanlagen mit Standort, Leistung, Mittel-Erzeugung",
    },
    "kernkraftwerke": {
        "slug": "kernkraftwerke",
        "preferred_formats": ["CSV", "GeoPackage"],
        "rq_bezug": "RQ, SQ-1",
        "priority": "A",
        "notes": "Standorte der Schweizer KKW, Stammdaten (sehr klein)",
    },

    # === Bilanz-Zeitreihen (Erzeugung, Verbrauch, aggregiert) ===
    "bilanz_monatswerte": {
        "slug": "schweizerische-elektrizitatsstatistik-schweizerische-elektrizitatsbilanz-monatswerte",
        "preferred_formats": ["CSV", "XLSX"],
        "rq_bezug": "RQ, SQ-1, SQ-2",
        "priority": "A",
        "notes": "Monatliche Schweizer Elektrizitätsbilanz, CH-gesamt, pro Energieform",
    },
    "bilanz_jahreswerte": {
        "slug": "schweizerische-elektrizitatsbilanz-jahreswerte",
        "preferred_formats": ["CSV", "XLSX"],
        "rq_bezug": "RQ, SQ-1",
        "priority": "A",
        "notes": "Jährliche Schweizer Elektrizitätsbilanz, lange Zeitreihe (CH-gesamt)",
    },

    # === Energiedashboard CH (aktuell, höhere Auflösung) ===
    # Ersetzt die veralteten Datensätze 'aussenhandel_laender' (nur bis 2016)
    # und 'endverbrauch_gruppen' (nur bis 2019). Das Energiedashboard ist
    # die aktuelle Datenbasis des BFE — methodisch sauber, weil deine Arbeit
    # auf derselben Grundlage operiert wie das BFE-Dashboard, gegen das du
    # dich in SQ-3 abgrenzst.
    "energiedashboard_verbrauch": {
        "slug": "energiedashboard-ch-landesverbrauch-und-endverbrauch",
        "preferred_formats": ["CSV", "XLSX", "JSON"],
        "rq_bezug": "RQ, SQ-1, SQ-3",
        "priority": "A",
        "notes": "Aktuelle Landes- und Endverbrauchsdaten des BFE-Energiedashboards",
    },
}


def get_priority_a_sources() -> dict:
    """Gibt nur die Quellen mit Priorität A zurück."""
    return {k: v for k, v in SOURCES.items() if v["priority"] == "A"}


def get_source(source_id: str) -> dict:
    """Gibt eine einzelne Quelle zurück. Wirft KeyError, wenn nicht existiert."""
    if source_id not in SOURCES:
        raise KeyError(
            f"Source '{source_id}' nicht in Konfiguration. "
            f"Verfügbar: {list(SOURCES.keys())}"
        )
    return SOURCES[source_id]