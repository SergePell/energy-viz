# Profil: energieuebersicht_ch_2024.xlsx

**Erstellt:** 2026-05-05T21:18:50
**Pfad:** `C:\Users\pelle\SynologyDrive\Docs\Studium\FHGR\Masterthesis\energy-viz\pipeline\raw\snapshots\2026-05-05\swissgrid\energieuebersicht_ch_2024.xlsx`
**Format:** XLSX

**Sheets:** Einstellungen, Datetime, Uebersicht, Zeitreihen0h15

## Sheet: `Einstellungen`

**Zeilen:** 43
**Spalten:** 22

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Energieübersicht Schweiz 2024` | str | 32 (74.42%) | 11 | `Anleitung`, `Ausgewählt | Selected:`, `Betrachtungszeitraum | Observation Period`, `Bis | To:`, `Das hier vorliegende Excel-Sheet beinhaltet die Gesamtübersicht der wichtigsten Eckdaten der Regelzone Schweiz.

Die Daten sind aggregierte Viertelstunden- oder Stundenwerte, welche zu ihrer Referenz im Blatt «Zeitreihen» abgelegt sind. Die Daten sind dieselben, wie auch von Swissgrid zu Abrechnungszwecken verwendet werden.

Nebst den Zeitreihen finden Sie auf dem Blatt «Übersicht» die Summen der jeweiligen Energiegrösse welche für den eingestellten Zeitraum direkt berechnet werden. Der Betrachtungszeitraum kann auf dieser Seite eingestellt werden.

Achtung: Bei MS-Excel 2003 und älter werden einige Felder nicht automatisch berechnet. Drücken Sie daher STRG+ALT+F9 nachdem Sie die Datei geöffnet haben.`, … (+6) |
| `Unnamed: 1` | str | 42 (97.67%) | 1 | `31.01.2025 16:32:41` |
| `Unnamed: 2` | object | 39 (90.7%) | 3 | `1`, `DD`, `MW / MWh` |
| `Unnamed: 3` | object | 40 (93.02%) | 2 | `1`, `MM` |
| `Unnamed: 4` | object | 40 (93.02%) | 3 | `2024`, `2025`, `YYYY` |
| `Unnamed: 5` | object | 40 (93.02%) | 2 | `0`, `hh` |
| `Unnamed: 6` | object | 40 (93.02%) | 2 | `0`, `min` |
| `Unnamed: 7` | datetime64[us] | 41 (95.35%) | 2 | 2024-01-01 00:00:00 … 2025-01-01 00:00:00 |
| `Unnamed: 8` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 9` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 10` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 11` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 12` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 13` | float64 | 43 (100.0%) | 0 |  |
| `1` | float64 | 13 (30.23%) | 30 | 2.0 … 31.0 (mean 16.50) |
| `1.1` | float64 | 32 (74.42%) | 11 | 2.0 … 12.0 (mean 7.00) |
| `2024` | float64 | 42 (97.67%) | 1 | 2025.0 … 2025.0 (mean 2025.00) |
| `0` | float64 | 20 (46.51%) | 23 | 1.0 … 23.0 (mean 12.00) |
| `0.1` | float64 | 40 (93.02%) | 3 | 15.0 … 45.0 (mean 30.00) |
| `kW / kWh` | str | 42 (97.67%) | 1 | `MW / MWh` |
| `Frühstes Datum` | str | 39 (90.7%) | 4 | `Faktor:`, `Prefix:`, `Spätestes Datum`, `anzMonate` |
| `2024-01-01 00:00:00` | object | 39 (90.7%) | 4 | `1`, `12`, `2025-01-01 00:00:00`, `M` |

## Sheet: `Datetime`

**Zeilen:** 35,137
**Spalten:** 1

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Unnamed: 0` | object | 0 (0.0%) | 35133 | `Zeitstempel 0h15`, `2024-01-01 00:15:00`, `2024-01-01 00:30:00` |

## Sheet: `Uebersicht`

**Zeilen:** 106
**Spalten:** 15

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Energieübersicht Schweiz 2024` | str | 93 (87.74%) | 13 | `Import/Export/Transit`, `Negative Sekundärregelenergie
Negative secondary control energy`, `Negative Tertiärregelenergie
Negative tertiary control energy`, `Netto Ausspeisung aus dem Übertragungsnetz Schweiz
Net outflow of the Swiss transmission grid`, `Periode:`, … (+8) |
| `Unnamed: 1` | str | 75 (70.75%) | 15 | `AT→CH`, `CH→AT`, `CH→DE`, `CH→FR`, `CH→IT`, … (+10) |
| `Unnamed: 2` | float64 | 97 (91.51%) | 9 | -383495.684 … 75565203.36793235 (mean 27548967.28) |
| `Unnamed: 3` | object | 74 (69.81%) | 12 | `-1358`, `-568.172`, `10014.04162074`, `12376.82791604`, `15397.61373604`, … (+7) |
| `Unnamed: 4` | float64 | 84 (79.25%) | 22 | 1816.584 … 39175314.648 (mean 6867417.12) |
| `Unnamed: 5` | float64 | 106 (100.0%) | 0 |  |
| `Unnamed: 6` | float64 | 106 (100.0%) | 0 |  |
| `Unnamed: 7` | str | 105 (99.06%) | 1 | `-` |
| `Unnamed: 8` | datetime64[us] | 105 (99.06%) | 1 | 2025-01-01 00:00:00 … 2025-01-01 00:00:00 |
| `Unnamed: 9` | float64 | 106 (100.0%) | 0 |  |
| `Unnamed: 10` | str | 66 (62.26%) | 2 | `MW`, `MWh` |
| `Unnamed: 11` | float64 | 106 (100.0%) | 0 |  |
| `Unnamed: 12` | float64 | 106 (100.0%) | 0 |  |
| `Unnamed: 13` | str | 94 (88.68%) | 11 | `Beschreibung
Die Netto Ausspeisung aus dem Übertragungsnetz ist die Energiemenge, welche effektiv aus dem Übertragungsnetz über direkt angeschlossene Transformatoren zu nachgelagerten Verteilnetzen, Endverbrauchern und Kraftwerken transportiert wurde. Die Netto Ausspeisung ist der positive Anteil der Bilanzierung aller vertikalen Übergabepunkte im Übertragunsgnetz zu Verteilnetzbetreibern, Endverbrauchern und Kraftwerken. Sie wird in Viertelstundenauflösung und in kWh aufbereitet.
`, `Beschreibung
Die Summe der abgegebenen Energiemengen in MWh pro Viertelstunde genettet, welche die Erzeugungseinheiten auf Basis eines SDL-Vertrages und durch Abruf von Swissgrid beziehen.`, `Beschreibung
Die Summe der abgegebenen Energiemengen in MWh pro Viertelstunde, welche die Erzeugungseinheiten auf Basis eines SDL-Vertrages und durch Tertiärabruf von Swissgrid beziehen`, `Beschreibung
Die Summe der bezogenen Energiemengen in MWh pro Viertelstunde genettet, welche die Erzeugungseinheiten auf Basis eines SDL-Vertrages und durch Abruf an Swissgrid liefern.`, `Beschreibung
Die Summe der bezogenen Energiemengen in MWh pro Viertelstunde, welche die Erzeugungseinheiten auf Basis eines SDL-Vertrages und durch Tertiärabruf an Swissgrid liefern.`, … (+6) |
| `Unnamed: 14` | str | 96 (90.57%) | 10 | `Description
Average prices of control energy per 15 minutes rounded to two decimal places for secondary and tertiary control energy products.`, `Description
The net outflow of the Swiss transmission grid is the amount of energy, which effectively flows over transformers out of the transmission grid into the distribution grids, towards end- users and power plants. The net outflow is the positive part of the netting of the vertical in feeds and outflows of the transmission grid. The resolution is 15 minutes and the energy is shown as kWh`, `Description
The total of the consumed energy in the control block Switzerland. The aggregations of the consumption sequences for the balancing group are sent from the distribution network operators to Swissgrid. The sum contains all the energy consumed in the transmission and distribution grids. Included are grid losses, energy consumed for a power plant’s own requirements and to drive the pumps in pumped storage hydro power plant.`, `Description
The total of the end- user energy consumption includes all aggregates with the end-user consumptions for the Swiss Control block delivered by the distribution network operators to Swissgrid. Not included are grid losses or energy consumed for  power plant’s own requirements or to drive the pumps in pumped storage hydro power plant. 
`, `Description
The total of the fed in energy which generating units have sourced with secondary control energy Swissgrid based on an ancillary services contract. The energy quantity is a netting of production and consumption in MWh within a 15 minutes time period.`, … (+5) |

## Sheet: `Zeitreihen0h15`

**Zeilen:** 35,137
**Spalten:** 65

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Unnamed: 0` | str | 0 (0.0%) | 35133 | `Zeitstempel`, `01.01.2024 00:15`, `01.01.2024 00:30` |
| `Summe endverbrauchte Energie Regelblock Schweiz | Total energy consumed by end users in the Swiss controlblock` | object | 0 (0.0%) | 35137 | `kWh`, `1443841.995625`, `1442365.748625` |
| `Summe produzierte Energie Regelblock Schweiz | Total energy production Swiss controlblock` | object | 0 (0.0%) | 35137 | `kWh`, `1296448.71`, `1294126.969` |
| `Summe verbrauchte Energie Regelblock Schweiz | Total energy consumption Swiss controlblock` | object | 0 (0.0%) | 35137 | `kWh`, `1939192.35146`, `1921877.642453` |
| `Netto Ausspeisung aus dem Übertragungsnetz Schweiz | Net outflow of the Swiss transmission grid` | object | 0 (0.0%) | 9942 | `kWh`, `604676.57354`, `592319.128547` |
| `Vertikale Einspeisung ins Übertragungsnetz Schweiz | Grid feed-in Swiss transmission grid` | object | 0 (0.0%) | 35131 | `kWh`, `854345.392`, `852382.105` |
| `Positive Sekundär-Regelenergie | Positive secundary control energy` | object | 0 (0.0%) | 11577 | `kWh`, `25`, `252` |
| `Negative Sekundär-Regelenergie | Negative secundary control energy` | object | 0 (0.0%) | 11735 | `kWh`, `-3860`, `-1382` |
| `Positive Tertiär-Regelenergie | Positive tertiary control energy` | object | 0 (0.0%) | 863 | `kWh`, `37500`, `37500` |
| `Negative Tertiär-Regelenergie | Negative tertiary control energy` | object | 0 (0.0%) | 633 | `kWh`, `0`, `0` |
| `Verbundaustausch CH->AT | Cross Border Exchange CH->AT` | object | 0 (0.0%) | 16175 | `kWh`, `48100`, `42000` |
| `Verbundaustausch AT->CH | Cross Border Exchange AT->CH` | object | 0 (0.0%) | 21574 | `kWh`, `80575`, `85479` |
| `Verbundaustausch CH->DE | Cross Border Exchange CH->DE` | object | 0 (0.0%) | 30718 | `kWh`, `57996`, `55800` |
| `Verbundaustausch DE->CH | Cross Border Exchange DE->CH` | object | 0 (0.0%) | 23808 | `kWh`, `522180`, `491811` |
| `Verbundaustausch CH->FR | Cross Border Exchange CH->FR` | object | 0 (0.0%) | 23436 | `kWh`, `84932`, `78828` |
| `Verbundaustausch FR->CH | Cross Border Exchange FR->CH` | object | 0 (0.0%) | 34274 | `kWh`, `412292`, `404015` |
| `Verbundaustausch CH->IT | Cross Border Exchange CH->IT` | object | 0 (0.0%) | 34367 | `kWh`, `254431`, `250664` |
| `Verbundaustausch IT->CH | Cross Border Exchange IT->CH` | object | 0 (0.0%) | 21677 | `kWh`, `73970`, `74193` |
| `Transit` | object | 0 (0.0%) | 34541 | `kWh`, `445459`, `427292` |
| `Import` | object | 0 (0.0%) | 34696 | `kWh`, `1089017`, `1055498` |
| `Export` | object | 0 (0.0%) | 34674 | `kWh`, `445459`, `427292` |
| `Durchschnittliche positive Sekundär-Regelenergie Preise | Average positive secondary control energy prices` | object | 0 (0.0%) | 17235 | `Euro/MWh`, `38.7`, `38.8` |
| `Durchschnittliche negative Sekundär-Regelenergie Preise | Average negative secondary control energy prices` | object | 0 (0.0%) | 17477 | `Euro/MWh`, `-10.21`, `8.32` |
| `Durchschnittliche positive Tertiär-Regelenergie Preise | Average positive tertiary control energy prices` | object | 0 (0.0%) | 7692 | `Euro/MWh`, `57.67`, `57.67` |
| `Durchschnittliche negative Tertiär-Regelenergie Preise | Average negative tertiary control energy prices` | object | 0 (0.0%) | 5873 | `Euro/MWh`, `0`, `0` |
| `Produktion Kanton AG | Production Canton AG` | object | 0 (0.0%) | 35123 | `kWh`, `512107.929`, `512528.372` |
| `Verbrauch Kanton AG | Consumption Canton AG` | object | 0 (0.0%) | 35135 | `kWh`, `123604.19`, `122947.461` |
| `Produktion Kanton FR | Production Canton FR` | object | 0 (0.0%) | 35128 | `kWh`, `17113.001`, `17033.774` |
| `Verbrauch Kanton FR | Consumption Canton FR` | object | 0 (0.0%) | 35126 | `kWh`, `72020.246`, `73027.768` |
| `Produktion Kanton GL | Production Canton GL` | object | 0 (0.0%) | 35128 | `kWh`, `8832.946`, `8810.179` |
| `Verbrauch Kanton GL | Consumption Canton GL` | object | 0 (0.0%) | 35106 | `kWh`, `143826.721`, `142278.996` |
| `Produktion Kanton GR | Production Canton GR` | object | 0 (0.0%) | 35135 | `kWh`, `69188.509`, `71754.822` |
| `Verbrauch Kanton GR | Consumption Canton GR` | object | 0 (0.0%) | 35130 | `kWh`, `98282.488`, `98425.798` |
| `Produktion Kanton LU | Production Canton LU` | object | 0 (0.0%) | 35114 | `kWh`, `9554.883`, `9480.929` |
| `Verbrauch Kanton LU | Consumption Canton LU` | object | 0 (0.0%) | 35125 | `kWh`, `88883.557`, `90549.587` |
| `Produktion Kanton NE | Production Canton NE` | object | 0 (0.0%) | 34727 | `kWh`, `580.311`, `565.699` |
| `Verbrauch Kanton NE | Consumption Canton NE` | object | 0 (0.0%) | 35065 | `kWh`, `12971.249`, `12885.877` |
| `Produktion Kanton SO | Production Canton SO` | object | 0 (0.0%) | 35102 | `kWh`, `271084.581`, `270882.056` |
| `Verbrauch Kanton SO | Consumption Canton SO` | object | 0 (0.0%) | 35108 | `kWh`, `35527.911`, `35604.314` |
| `Produktion Kanton SG | Production Canton SG` | object | 0 (0.0%) | 35133 | `kWh`, `13250.7236`, `13395.9944` |
| `Verbrauch Kanton SG | Consumption Canton SG` | object | 0 (0.0%) | 35134 | `kWh`, `103439.5498`, `97289.4734` |
| `Produktion Kanton TI | Production Canton TI` | object | 0 (0.0%) | 35135 | `kWh`, `28545.575`, `26840.557` |
| `Verbrauch Kanton TI | Consumption Canton TI` | object | 0 (0.0%) | 35127 | `kWh`, `81903.75`, `80570.032` |
| `Produktion Kanton TG | Production Canton TG` | object | 0 (0.0%) | 35018 | `kWh`, `4424.73`, `4339.045` |
| `Verbrauch Kanton TG | Consumption Canton TG` | object | 0 (0.0%) | 35120 | `kWh`, `43279.547`, `43279.963` |
| `Produktion Kanton VS | Production Canton VS` | object | 0 (0.0%) | 35137 | `kWh`, `49175.695`, `46248.567` |
| `Verbrauch Kanton VS | Consumption Canton VS` | object | 0 (0.0%) | 35131 | `kWh`, `191438.88`, `187292.507` |
| `Produktion Kantone AI, AR | Production Cantons AI, AR` | object | 0 (0.0%) | 35117 | `kWh`, `1431.6354`, `1428.5566` |
| `Verbrauch Kantone AI, AR | Consumption Cantons AI, AR` | object | 0 (0.0%) | 35125 | `kWh`, `13236.6452`, `13178.8746` |
| `Produktion Kantone BL, BS | Production Cantons BL, BS` | object | 0 (0.0%) | 35104 | `kWh`, `31321.657`, `31391.13` |
| `Verbrauch Kantone BL, BS | Consumption Cantons BL, BS` | object | 0 (0.0%) | 35127 | `kWh`, `77064.93`, `77267.468` |
| `Produktion Kantone BE, JU | Production Cantons BE, JU` | object | 0 (0.0%) | 35134 | `kWh`, `76137.629`, `75709.967` |
| `Verbrauch Kantone BE, JU | Consumption Cantons BE, JU` | object | 0 (0.0%) | 35135 | `kWh`, `246064.589`, `247149.214` |
| `Produktion Kantone SZ, ZG | Production Cantons SZ, ZG` | object | 0 (0.0%) | 35110 | `kWh`, `6209.724`, `6022.193` |
| `Verbrauch Kantone SZ, ZG | Consumption Cantons SZ, ZG` | object | 0 (0.0%) | 35118 | `kWh`, `50537.468`, `50674.625` |
| `Produktion Kantone OW, NW, UR | Production Cantons OW, NW, UR` | object | 0 (0.0%) | 35132 | `kWh`, `10894.643`, `10760.79` |
| `Verbrauch Kantone OW, NW, UR | Consumption Cantons OW, NW, UR` | object | 0 (0.0%) | 35098 | `kWh`, `27995.643`, `27521.791` |
| `Produktion Kantone GE, VD | Production Cantons GE, VD` | object | 0 (0.0%) | 35131 | `kWh`, `41352.81`, `41058.415` |
| `Verbrauch Kantone GE, VD | Consumption Cantons GE, VD` | object | 0 (0.0%) | 35134 | `kWh`, `229333.429`, `224283.806` |
| `Produktion Kantone SH, ZH | Production Cantons SH, ZH` | object | 0 (0.0%) | 35109 | `kWh`, `22468.38`, `22550.21` |
| `Verbrauch Kantone SH, ZH | Consumption Cantons SH, ZH` | object | 0 (0.0%) | 35135 | `kWh`, `251422.561`, `252227.424` |
| `Produktion Kantonsübergreifend | Production across Cantons` | object | 0 (0.0%) | 35126 | `kWh`, `119689.268`, `120907.426` |
| `Verbrauch Kantonsübergreifend | Consumption across Cantons` | object | 0 (0.0%) | 35137 | `kWh`, `36427.03346`, `33431.673453` |
| `Produktion Regelzone CH - Ausländische Gebiete | Production control area CH - foreign territories` | object | 0 (0.0%) | 35067 | `kWh`, `3084.08`, `2418.287` |
| `Verbrauch Regelzone CH - Ausländische Gebiete | Consumption control area CH - foreign territories` | object | 0 (0.0%) | 35096 | `kWh`, `11931.964`, `11990.99` |
