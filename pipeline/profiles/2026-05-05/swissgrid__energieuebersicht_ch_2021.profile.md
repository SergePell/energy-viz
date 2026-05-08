# Profil: energieuebersicht_ch_2021.xlsx

**Erstellt:** 2026-05-05T21:18:11
**Pfad:** `C:\Users\pelle\SynologyDrive\Docs\Studium\FHGR\Masterthesis\energy-viz\pipeline\raw\snapshots\2026-05-05\swissgrid\energieuebersicht_ch_2021.xlsx`
**Format:** XLSX

**Sheets:** Einstellungen, Datetime, Uebersicht, Zeitreihen0h15, Zeitreihen1h00

## Sheet: `Einstellungen`

**Zeilen:** 43
**Spalten:** 22

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Energieübersicht Schweiz 2021` | str | 32 (74.42%) | 11 | `Anleitung`, `Ausgewählt | Selected:`, `Betrachtungszeitraum | Observation Period`, `Bis | To:`, `Das hier vorliegende Excel-Sheet beinhaltet die Gesamtübersicht der wichtigsten Eckdaten der Regelzone Schweiz.

Die Daten sind aggregierte Viertelstunden- oder Stundenwerte, welche zu ihrer Referenz im Blatt «Zeitreihen» abgelegt sind. Die Daten sind dieselben, wie auch von Swissgrid zu Abrechnungszwecken verwendet werden.

Nebst den Zeitreihen finden Sie auf dem Blatt «Übersicht» die Summen der jeweiligen Energiegrösse welche für den eingestellten Zeitraum direkt berechnet werden. Der Betrachtungszeitraum kann auf dieser Seite eingestellt werden.

Achtung: Bei MS-Excel 2003 und älter werden einige Felder nicht automatisch berechnet. Drücken Sie daher STRG+ALT+F9 nachdem Sie die Datei geöffnet haben.`, … (+6) |
| `Unnamed: 1` | str | 42 (97.67%) | 1 | `18.07.2022 13:54:37` |
| `Unnamed: 2` | object | 39 (90.7%) | 3 | `1`, `DD`, `MW / MWh` |
| `Unnamed: 3` | object | 40 (93.02%) | 2 | `1`, `MM` |
| `Unnamed: 4` | object | 40 (93.02%) | 3 | `2021`, `2022`, `YYYY` |
| `Unnamed: 5` | object | 40 (93.02%) | 2 | `0`, `hh` |
| `Unnamed: 6` | object | 40 (93.02%) | 2 | `0`, `min` |
| `Unnamed: 7` | datetime64[us] | 41 (95.35%) | 2 | 2021-01-01 00:00:00 … 2022-01-01 00:00:00 |
| `Unnamed: 8` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 9` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 10` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 11` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 12` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 13` | float64 | 43 (100.0%) | 0 |  |
| `1` | float64 | 13 (30.23%) | 30 | 2.0 … 31.0 (mean 16.50) |
| `1.1` | float64 | 32 (74.42%) | 11 | 2.0 … 12.0 (mean 7.00) |
| `2021` | float64 | 42 (97.67%) | 1 | 2022.0 … 2022.0 (mean 2022.00) |
| `0` | float64 | 20 (46.51%) | 23 | 1.0 … 23.0 (mean 12.00) |
| `0.1` | float64 | 40 (93.02%) | 3 | 15.0 … 45.0 (mean 30.00) |
| `kW / kWh` | str | 42 (97.67%) | 1 | `MW / MWh` |
| `Frühstes Datum` | str | 39 (90.7%) | 4 | `Faktor:`, `Prefix:`, `Spätestes Datum`, `anzMonate` |
| `2021-01-01 00:00:00` | object | 39 (90.7%) | 4 | `1`, `12`, `2022-01-01 00:00:00`, `M` |

## Sheet: `Datetime`

**Zeilen:** 35,137
**Spalten:** 3

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Unnamed: 0` | object | 96 (0.27%) | 35037 | `Zeitstempel 0h15`, `2021-01-01 00:15:00`, `2021-01-01 00:30:00` |
| `Unnamed: 1` | float64 | 35137 (100.0%) | 0 |  |
| `Unnamed: 2` | object | 26376 (75.07%) | 8760 | `Zeitstempel 1h00`, `2021-01-01 01:00:00`, `2021-01-01 02:00:00` |

## Sheet: `Uebersicht`

**Zeilen:** 112
**Spalten:** 15

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Energieübersicht Schweiz 2021` | str | 98 (87.5%) | 14 | `Import/Export/Transit`, `Negative Sekundärregelenergie
Negative secondary control energy`, `Negative Tertiärregelenergie
Negative tertiary control energy`, `Netto Ausspeisung aus dem Übertragungsnetz Schweiz
Net outflow of the Swiss transmission grid`, `Periode:`, … (+9) |
| `Unnamed: 1` | str | 79 (70.54%) | 15 | `AT→CH`, `CH→AT`, `CH→DE`, `CH→FR`, `CH→IT`, … (+10) |
| `Unnamed: 2` | float64 | 102 (91.07%) | 10 | -570613.9 … 64413508.55141924 (mean 27771179.77) |
| `Unnamed: 3` | object | 79 (70.54%) | 13 | `-1580`, `-392.108`, `10444.999896048`, `10550.038176196`, `12959.239645972`, … (+8) |
| `Unnamed: 4` | float64 | 90 (80.36%) | 22 | 1095.688 … 30947980.95 (mean 6333625.63) |
| `Unnamed: 5` | float64 | 112 (100.0%) | 0 |  |
| `Unnamed: 6` | float64 | 112 (100.0%) | 0 |  |
| `Unnamed: 7` | str | 111 (99.11%) | 1 | `-` |
| `Unnamed: 8` | datetime64[us] | 111 (99.11%) | 1 | 2022-01-01 00:00:00 … 2022-01-01 00:00:00 |
| `Unnamed: 9` | float64 | 112 (100.0%) | 0 |  |
| `Unnamed: 10` | str | 70 (62.5%) | 2 | `MW`, `MWh` |
| `Unnamed: 11` | float64 | 112 (100.0%) | 0 |  |
| `Unnamed: 12` | float64 | 112 (100.0%) | 0 |  |
| `Unnamed: 13` | str | 99 (88.39%) | 12 | `Beschreibung
Die Netto Ausspeisung aus dem Übertragungsnetz ist die Energiemenge, welche effektiv aus dem Übertragungsnetz über direkt angeschlossene Transformatoren zu nachgelagerten Verteilnetzen, Endverbrauchern und Kraftwerken transportiert wurde. Die Netto Ausspeisung ist der positive Anteil der Bilanzierung aller vertikalen Übergabepunkte im Übertragunsgnetz zu Verteilnetzbetreibern, Endverbrauchern und Kraftwerken. Sie wird in Viertelstundenauflösung und in kWh aufbereitet.
`, `Beschreibung
Die Summe der abgegebenen Energiemengen in MWh pro Viertelstunde genettet, welche die Erzeugungseinheiten auf Basis eines SDL-Vertrages und durch Abruf von Swissgrid beziehen.`, `Beschreibung
Die Summe der abgegebenen Energiemengen in MWh pro Viertelstunde, welche die Erzeugungseinheiten auf Basis eines SDL-Vertrages und durch Tertiärabruf von Swissgrid beziehen`, `Beschreibung
Die Summe der bezogenen Energiemengen in MWh pro Viertelstunde genettet, welche die Erzeugungseinheiten auf Basis eines SDL-Vertrages und durch Abruf an Swissgrid liefern.`, `Beschreibung
Die Summe der bezogenen Energiemengen in MWh pro Viertelstunde, welche die Erzeugungseinheiten auf Basis eines SDL-Vertrages und durch Tertiärabruf an Swissgrid liefern.`, … (+7) |
| `Unnamed: 14` | str | 101 (90.18%) | 11 | `Description
Average prices of control energy per 15 minutes rounded to two decimal places for secondary and tertiary control energy products.`, `Description
The net outflow of the Swiss transmission grid is the amount of energy, which effectively flows over transformers out of the transmission grid into the distribution grids, towards end- users and power plants. The net outflow is the positive part of the netting of the vertical in feeds and outflows of the transmission grid. The resolution is 15 minutes and the energy is shown as kWh`, `Description
The total of the consumed energy in the control block Switzerland. The aggregations of the consumption sequences for the balancing group are sent from the distribution network operators to Swissgrid. The sum contains all the energy consumed in the transmission and distribution grids. Included are grid losses, energy consumed for a power plant’s own requirements and to drive the pumps in pumped storage hydro power plant.`, `Description
The total of the end- user energy consumption includes all aggregates with the end-user consumptions for the Swiss Control block delivered by the distribution network operators to Swissgrid. Not included are grid losses or energy consumed for  power plant’s own requirements or to drive the pumps in pumped storage hydro power plant. 
`, `Description
The total of the fed in energy which generating units have sourced with secondary control energy Swissgrid based on an ancillary services contract. The energy quantity is a netting of production and consumption in MWh within a 15 minutes time period.`, … (+6) |

## Sheet: `Zeitreihen0h15`

**Zeilen:** 35,041
**Spalten:** 65

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Unnamed: 0` | str | 0 (0.0%) | 35037 | `Zeitstempel`, `01.01.2021 00:15`, `01.01.2021 00:30` |
| `Summe endverbrauchte Energie Regelblock Schweiz | Total energy consumed by end users in the Swiss controlblock` | object | 0 (0.0%) | 35041 | `kWh`, `1671630.088625`, `1661251.405625` |
| `Summe produzierte Energie Regelblock Schweiz | Total energy production Swiss controlblock` | object | 0 (0.0%) | 35041 | `kWh`, `1210856.088`, `1192987.411` |
| `Summe verbrauchte Energie Regelblock Schweiz | Total energy consumption Swiss controlblock` | object | 0 (0.0%) | 35041 | `kWh`, `1880710.202024`, `1877758.191115` |
| `Netto Ausspeisung aus dem Übertragungsnetz Schweiz | Net outflow of the Swiss transmission grid` | object | 0 (0.0%) | 20315 | `kWh`, `635189.489912`, `647088.60469` |
| `Vertikale Einspeisung ins Übertragungsnetz Schweiz | Grid feed-in Swiss transmission grid` | object | 0 (0.0%) | 35041 | `kWh`, `869233.8751`, `863927.1974` |
| `Positive Sekundär-Regelenergie | Positive secundary control energy` | object | 0 (0.0%) | 11850 | `kWh`, `17242`, `2639` |
| `Negative Sekundär-Regelenergie | Negative secundary control energy` | object | 0 (0.0%) | 10417 | `kWh`, `-2392`, `-431` |
| `Positive Tertiär-Regelenergie | Positive tertiary control energy` | object | 0 (0.0%) | 561 | `kWh`, `0`, `0` |
| `Negative Tertiär-Regelenergie | Negative tertiary control energy` | object | 0 (0.0%) | 616 | `kWh`, `0`, `0` |
| `Verbundaustausch CH->AT | Cross Border Exchange CH->AT` | object | 0 (0.0%) | 8756 | `kWh`, `0`, `0` |
| `Verbundaustausch AT->CH | Cross Border Exchange AT->CH` | object | 0 (0.0%) | 20872 | `kWh`, `269204`, `262096` |
| `Verbundaustausch CH->DE | Cross Border Exchange CH->DE` | object | 0 (0.0%) | 20909 | `kWh`, `65200`, `69200` |
| `Verbundaustausch DE->CH | Cross Border Exchange DE->CH` | object | 0 (0.0%) | 33845 | `kWh`, `531093`, `491500` |
| `Verbundaustausch CH->FR | Cross Border Exchange CH->FR` | object | 0 (0.0%) | 24301 | `kWh`, `233092.25`, `233492.25` |
| `Verbundaustausch FR->CH | Cross Border Exchange FR->CH` | object | 0 (0.0%) | 33359 | `kWh`, `163967`, `163367` |
| `Verbundaustausch CH->IT | Cross Border Exchange CH->IT` | object | 0 (0.0%) | 34337 | `kWh`, `158988`, `100505` |
| `Verbundaustausch IT->CH | Cross Border Exchange IT->CH` | object | 0 (0.0%) | 22802 | `kWh`, `154488`, `169811` |
| `Transit` | object | 0 (0.0%) | 34429 | `kWh`, `461448`, `403106` |
| `Import` | object | 0 (0.0%) | 34667 | `kWh`, `1113344.25`, `1085120.25` |
| `Export` | object | 0 (0.0%) | 34574 | `kWh`, `461448`, `403106` |
| `Durchschnittliche positive Sekundär-Regelenergie Preise | Average positive secondary control energy prices` | object | 0 (0.0%) | 5560 | `Euro/MWh`, `61.18`, `61.18` |
| `Durchschnittliche negative Sekundär-Regelenergie Preise | Average negative secondary control energy prices` | object | 0 (0.0%) | 5511 | `Euro/MWh`, `40.78`, `40.78` |
| `Durchschnittliche positive Tertiär-Regelenergie Preise | Average positive tertiary control energy prices` | object | 0 (0.0%) | 3856 | `Euro/MWh`, `0`, `0` |
| `Durchschnittliche negative Tertiär-Regelenergie Preise | Average negative tertiary control energy prices` | object | 0 (0.0%) | 3348 | `Euro/MWh`, `0`, `0` |
| `Produktion Kanton AG | Production Canton AG` | object | 0 (0.0%) | 35029 | `kWh`, `506916.405`, `506991.575` |
| `Verbrauch Kanton AG | Consumption Canton AG` | object | 0 (0.0%) | 35030 | `kWh`, `144870.3`, `143246.488` |
| `Produktion Kanton FR | Production Canton FR` | object | 0 (0.0%) | 35012 | `kWh`, `10722.881`, `10481.082` |
| `Verbrauch Kanton FR | Consumption Canton FR` | object | 0 (0.0%) | 35027 | `kWh`, `78892.188`, `79112.973` |
| `Produktion Kanton GL | Production Canton GL` | object | 0 (0.0%) | 35028 | `kWh`, `21967.513`, `23754.491` |
| `Verbrauch Kanton GL | Consumption Canton GL` | object | 0 (0.0%) | 35012 | `kWh`, `14092.582`, `13643.98` |
| `Produktion Kanton GR | Production Canton GR` | object | 0 (0.0%) | 35040 | `kWh`, `47645.798`, `38004.319` |
| `Verbrauch Kanton GR | Consumption Canton GR` | object | 0 (0.0%) | 35028 | `kWh`, `84823.099`, `82467.309` |
| `Produktion Kanton LU | Production Canton LU` | object | 0 (0.0%) | 35020 | `kWh`, `8873.861`, `9164.561` |
| `Verbrauch Kanton LU | Consumption Canton LU` | object | 0 (0.0%) | 35031 | `kWh`, `100781.61`, `99167.359` |
| `Produktion Kanton NE | Production Canton NE` | object | 0 (0.0%) | 31811 | `kWh`, `535.34`, `451.78` |
| `Verbrauch Kanton NE | Consumption Canton NE` | object | 0 (0.0%) | 34954 | `kWh`, `15180.41`, `14850.601` |
| `Produktion Kanton SO | Production Canton SO` | object | 0 (0.0%) | 35013 | `kWh`, `264093.73`, `264112.219` |
| `Verbrauch Kanton SO | Consumption Canton SO` | object | 0 (0.0%) | 35030 | `kWh`, `55417.585`, `54864.017` |
| `Produktion Kanton SG | Production Canton SG` | object | 0 (0.0%) | 35039 | `kWh`, `6349.7434`, `6508.962` |
| `Verbrauch Kanton SG | Consumption Canton SG` | object | 0 (0.0%) | 35040 | `kWh`, `91565.349`, `90028.4902` |
| `Produktion Kanton TI | Production Canton TI` | object | 0 (0.0%) | 35040 | `kWh`, `38767.47`, `35475.936` |
| `Verbrauch Kanton TI | Consumption Canton TI` | object | 0 (0.0%) | 35032 | `kWh`, `98775.281`, `97549.064` |
| `Produktion Kanton TG | Production Canton TG` | object | 0 (0.0%) | 34945 | `kWh`, `2698.005`, `2650.628` |
| `Verbrauch Kanton TG | Consumption Canton TG` | object | 0 (0.0%) | 35027 | `kWh`, `51680.733`, `51557.945` |
| `Produktion Kanton VS | Production Canton VS` | object | 0 (0.0%) | 35041 | `kWh`, `76232.611`, `74075.664` |
| `Verbrauch Kanton VS | Consumption Canton VS` | object | 0 (0.0%) | 35041 | `kWh`, `113342.497936`, `111850.482805` |
| `Produktion Kantone AI, AR | Production Cantons AI, AR` | object | 0 (0.0%) | 35016 | `kWh`, `702.3366`, `698.778` |
| `Verbrauch Kantone AI, AR | Consumption Cantons AI, AR` | object | 0 (0.0%) | 35027 | `kWh`, `17244.361`, `16985.3298` |
| `Produktion Kantone BL, BS | Production Cantons BL, BS` | object | 0 (0.0%) | 35024 | `kWh`, `21493.941`, `21557.589` |
| `Verbrauch Kantone BL, BS | Consumption Cantons BL, BS` | object | 0 (0.0%) | 35034 | `kWh`, `90915.523`, `91077.249` |
| `Produktion Kantone BE, JU | Production Cantons BE, JU` | object | 0 (0.0%) | 35037 | `kWh`, `44887.011`, `42879.557` |
| `Verbrauch Kantone BE, JU | Consumption Cantons BE, JU` | object | 0 (0.0%) | 35039 | `kWh`, `239879.51`, `246005.877` |
| `Produktion Kantone SZ, ZG | Production Cantons SZ, ZG` | object | 0 (0.0%) | 35012 | `kWh`, `3153.203`, `3160.377` |
| `Verbrauch Kantone SZ, ZG | Consumption Cantons SZ, ZG` | object | 0 (0.0%) | 35020 | `kWh`, `59896.425`, `58674.025` |
| `Produktion Kantone OW, NW, UR | Production Cantons OW, NW, UR` | object | 0 (0.0%) | 35031 | `kWh`, `9768.566`, `9764.704` |
| `Verbrauch Kantone OW, NW, UR | Consumption Cantons OW, NW, UR` | object | 0 (0.0%) | 35002 | `kWh`, `32685.315`, `32658.413` |
| `Produktion Kantone GE, VD | Production Cantons GE, VD` | object | 0 (0.0%) | 35034 | `kWh`, `27109.446`, `24469.448` |
| `Verbrauch Kantone GE, VD | Consumption Cantons GE, VD` | object | 0 (0.0%) | 35035 | `kWh`, `260040.413`, `260521.051` |
| `Produktion Kantone SH, ZH | Production Cantons SH, ZH` | object | 0 (0.0%) | 35001 | `kWh`, `20405.967`, `20517.589` |
| `Verbrauch Kantone SH, ZH | Consumption Cantons SH, ZH` | object | 0 (0.0%) | 35037 | `kWh`, `278109.595`, `277796.491` |
| `Produktion Kantonsübergreifend | Production across Cantons` | object | 0 (0.0%) | 35032 | `kWh`, `97665.574`, `97445.697` |
| `Verbrauch Kantonsübergreifend | Consumption across Cantons` | object | 0 (0.0%) | 35041 | `kWh`, `39143.313088`, `42522.34031` |
| `Produktion Regelzone CH - Ausländische Gebiete | Production control area CH - foreign territories` | object | 0 (0.0%) | 34950 | `kWh`, `866.686`, `822.455` |
| `Verbrauch Regelzone CH - Ausländische Gebiete | Consumption control area CH - foreign territories` | object | 0 (0.0%) | 35009 | `kWh`, `13374.112`, `13178.706` |

## Sheet: `Zeitreihen1h00`

**Zeilen:** 8,761
**Spalten:** 2

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Unnamed: 0` | str | 0 (0.0%) | 8760 | `Zeitstempel`, `01.01.2021 01:00`, `01.01.2021 02:00` |
| `Vertikale Netzlast Übertragungsnetz Schweiz | Vertical load Swiss transmission grid` | object | 0 (0.0%) | 8760 | `MW`, `5866.04367`, `5908.837095` |
