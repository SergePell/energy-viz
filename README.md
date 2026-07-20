# energy-viz

Visual-Analytics-Prototyp zur explorativen Analyse von Energieformen und -erzeugung in der Schweiz.

Dieses Repository ist der im Rahmen der Masterarbeit *«Visual Analytics von Energieformen und -erzeugungen in der Schweiz»* (FHGR, Studienrichtung Data Visualization) entwickelte Forschungsprototyp. Er integriert öffentliche Energiedaten über die zeitliche, räumliche und thematische Dimension und verbindet interaktive Visualisierung mit vorberechneten analytischen Verfahren (Zeitreihenzerlegung und kontextuelle Anomalieerkennung).

Der wissenschaftliche Beitrag der Arbeit liegt im dokumentierten Designprozess, nicht im Werkzeug als Produkt. Der Prototyp dient als Machbarkeitsnachweis.

## Funktionen

Der Prototyp ist in vier Reiter gegliedert:

- **Analyse** – zentrale, gekoppelte Ansicht (Coordinated Multiple Views): Choroplethenkarte der kantonalen Erzeugung mit Standortmarkern, Verbrauchslinie mit Anomalie-Overlay und Schwellenwertsteuerung, Energiemix nach Energieträger, Zeitreihenzerlegung sowie Wetterlinie. Eine Interaktion in einer Ansicht wirkt auf die verbundenen.
- **Grenzüberschreitender Handel** – Sankey-Diagramm der bilateralen Stromflüsse, Länderbilanz, KPI-Kachel und Netto-Handelsbilanz-Zeitreihe mit Länder-Fokus.
- **Vergleich zweier Zeiträume** – direkte Gegenüberstellung zweier frei wählbarer Zeitfenster.
- **Gesamtenergiebilanz Schweiz** – Sankey der nationalen Energiebilanz (inkl. Erdöl und Gas) auf Basis der BFE-Gesamtenergiestatistik.

Analytische Kernbausteine: STL- und MSTL-Zerlegung (Trend, Saison, Residuum) sowie ein Isolation Forest auf dem Residuum mit den Kontextvariablen Temperatur, Strompreis, Globalstrahlung und Niederschlag zur Erkennung kontextueller Anomalien.

## Technologie-Stack

**Frontend:** React 19, Vite, D3 (7.9) und d3-sankey, Recharts (3).
**Datenpipeline:** Python mit pandas, scikit-learn (Isolation Forest), statsmodels (STL/MSTL) und pyarrow (Parquet).

## Datenquellen

| Quelle | Inhalt |
|---|---|
| Swissgrid | Landesverbrauch (15-Min), kantonale Erzeugung, grenzüberschreitender Handel |
| BFE (OGD32, OGD115, OGD123, WASTA) | monatliche Elektrizitätsbilanz, Gesamtenergiestatistik, Anlagenstammdaten |
| ENTSO-E Transparency | Day-Ahead-Spotpreis Schweiz (Gebotszone 10YCH-SWISSGRIDZ) |
| Open-Meteo | Temperatur, Globalstrahlung, Niederschlag |

## Architektur

Die Pipeline folgt einem Extract-Transform-Analyze-Serving-Ablauf. Jede Stufe schreibt ihre Ausgaben als Zwischenartefakte, sodass sich einzelne Schritte unabhängig ausführen lassen.

```
Rohdaten (API/CSV/XLSX)
   │  extract/     Quellen abholen
   ▼
   │  transform/   bereinigen, in Tidy-Struktur/Parquet überführen
   ▼
   │  analyze/     Zerlegung (analyze_decompose) und Anomalieerkennung (analyze_anomaly)
   ▼
   │  server/      build_frontend_data: JSON für das Frontend erzeugen
   ▼
public/data/*.json  →  React-Frontend
```

## Setup

### Voraussetzungen

- Node.js 18 oder neuer und npm
- Python 3.11 oder neuer
- Ein ENTSO-E-API-Token (kostenlos über die Transparency Platform), hinterlegt als `ENTSOE_API_TOKEN` in einer `.env`-Datei im Projektstamm

### Frontend starten

```bash
npm install
npm run dev
```

Der Entwicklungsserver läuft anschliessend auf `http://localhost:5173`. Das Frontend liest die vorbereiteten JSON-Dateien aus `public/data/` und benötigt zum reinen Betrachten die Pipeline nicht.

Weitere Skripte: `npm run build` (Produktions-Build), `npm run preview` (Build lokal prüfen), `npm run lint`.

### Datenpipeline ausführen

Die Python-Abhängigkeiten installieren (empfohlen in einer virtuellen Umgebung):

```bash
pip install -r requirements.txt
```

Anschliessend die gesamte Pipeline über den Orchestrator ausführen:

```bash
python refresh_all.py
```

Die Skripte sind idempotent aufgebaut: Bereits erzeugte Artefakte werden übersprungen. Ein erneutes Durchlaufen wird mit `--force` erzwungen:

```bash
python refresh_all.py --force
```

Einzelne Stufen lassen sich auch direkt aufrufen, zum Beispiel:

```bash
python pipeline/extract/extract_entsoe.py
python pipeline/analyze/analyze_decompose.py
python pipeline/analyze/analyze_anomaly.py
python pipeline/server/build_frontend_data.py
```

## Projektstruktur

```
energy-viz/
├── refresh_all.py            Orchestrator der gesamten Pipeline
├── pipeline/
│   ├── config/               Quellendefinitionen (Swissgrid, BFE/WASTA, ENTSO-E, Wetterstationen)
│   ├── extract/              Rohdaten je Quelle abholen
│   ├── transform/            Bereinigung und Tidy-/Parquet-Aufbereitung
│   ├── analyze/              Zeitreihenzerlegung und Anomalieerkennung
│   ├── server/               JSON-Aufbereitung fürs Frontend
│   ├── explore/              Snapshot-Profiling
│   └── utils/                Hilfsfunktionen (Manifest)
├── public/data/              generierte JSON-Daten für das Frontend
└── src/
    └── components/           React-Visualisierungskomponenten
```

## Reproduzierbarkeit

Die im Frontend gezeigten Analysen basieren auf einem eingefrorenen Datenstand vom **10. Mai 2026**. Der Snapshot wird über die Umgebungsvariable `ENERGYVIZ_SNAPSHOT` gesteuert und fällt ohne Angabe auf dieses Datum zurück, sodass die Ergebnisse reproduzierbar bleiben. Eine Ausnahme bildet die Übersicht zur Gesamtenergiebilanz (BFE OGD115), die den jeweils neuesten verfügbaren Snapshot verwendet.

## Autor und Kontext

Serge Pellegatta, Masterarbeit an der Fachhochschule Graubünden (FHGR), Studienrichtung Data Visualization, 2026. Betreuung: Michael Burch.

Der Prototyp ist ein akademischer Forschungsgegenstand und keine produktionsreife Anwendung. Die Daten stammen aus den oben genannten öffentlichen Quellen; deren jeweilige Nutzungsbedingungen sind zu beachten.
