# Profil: energieuebersicht_ch_2022.xlsx

**Erstellt:** 2026-05-05T21:18:24
**Pfad:** `C:\Users\pelle\SynologyDrive\Docs\Studium\FHGR\Masterthesis\energy-viz\pipeline\raw\snapshots\2026-05-05\swissgrid\energieuebersicht_ch_2022.xlsx`
**Format:** XLSX

**Sheets:** Einstellungen, Datetime, Uebersicht, Zeitreihen0h15, Zeitreihen1h00

## Sheet: `Einstellungen`

**Zeilen:** 43
**Spalten:** 22

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Energieübersicht Schweiz 2022` | str | 32 (74.42%) | 11 | `Anleitung`, `Ausgewählt | Selected:`, `Betrachtungszeitraum | Observation Period`, `Bis | To:`, `Das hier vorliegende Excel-Sheet beinhaltet die Gesamtübersicht der wichtigsten Eckdaten der Regelzone Schweiz.

Die Daten sind aggregierte Viertelstunden- oder Stundenwerte, welche zu ihrer Referenz im Blatt «Zeitreihen» abgelegt sind. Die Daten sind dieselben, wie auch von Swissgrid zu Abrechnungszwecken verwendet werden.

Nebst den Zeitreihen finden Sie auf dem Blatt «Übersicht» die Summen der jeweiligen Energiegrösse welche für den eingestellten Zeitraum direkt berechnet werden. Der Betrachtungszeitraum kann auf dieser Seite eingestellt werden.

Achtung: Bei MS-Excel 2003 und älter werden einige Felder nicht automatisch berechnet. Drücken Sie daher STRG+ALT+F9 nachdem Sie die Datei geöffnet haben.`, … (+6) |
| `Unnamed: 1` | str | 42 (97.67%) | 1 | `18.07.2023 08:25:53` |
| `Unnamed: 2` | object | 39 (90.7%) | 3 | `1`, `DD`, `MW / MWh` |
| `Unnamed: 3` | object | 40 (93.02%) | 2 | `1`, `MM` |
| `Unnamed: 4` | object | 40 (93.02%) | 3 | `2022`, `2023`, `YYYY` |
| `Unnamed: 5` | object | 40 (93.02%) | 2 | `0`, `hh` |
| `Unnamed: 6` | object | 40 (93.02%) | 2 | `0`, `min` |
| `Unnamed: 7` | datetime64[us] | 41 (95.35%) | 2 | 2022-01-01 00:00:00 … 2023-01-01 00:00:00 |
| `Unnamed: 8` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 9` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 10` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 11` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 12` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 13` | float64 | 43 (100.0%) | 0 |  |
| `1` | float64 | 13 (30.23%) | 30 | 2.0 … 31.0 (mean 16.50) |
| `1.1` | float64 | 32 (74.42%) | 11 | 2.0 … 12.0 (mean 7.00) |
| `2022` | float64 | 42 (97.67%) | 1 | 2023.0 … 2023.0 (mean 2023.00) |
| `0` | float64 | 20 (46.51%) | 23 | 1.0 … 23.0 (mean 12.00) |
| `0.1` | float64 | 40 (93.02%) | 3 | 15.0 … 45.0 (mean 30.00) |
| `kW / kWh` | str | 42 (97.67%) | 1 | `MW / MWh` |
| `Frühstes Datum` | str | 39 (90.7%) | 4 | `Faktor:`, `Prefix:`, `Spätestes Datum`, `anzMonate` |
| `2022-01-01 00:00:00` | object | 39 (90.7%) | 4 | `1`, `12`, `2023-01-01 00:00:00`, `M` |

## Sheet: `Datetime`

**Zeilen:** 35,137
**Spalten:** 3

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Unnamed: 0` | object | 96 (0.27%) | 35037 | `Zeitstempel 0h15`, `2022-01-01 00:15:00`, `2022-01-01 00:30:00` |
| `Unnamed: 1` | float64 | 35137 (100.0%) | 0 |  |
| `Unnamed: 2` | object | 26376 (75.07%) | 8760 | `Zeitstempel 1h00`, `2022-01-01 01:00:00`, `2022-01-01 02:00:00` |

## Sheet: `Uebersicht`

**Zeilen:** 112
**Spalten:** 15

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Energieübersicht Schweiz 2022` | str | 98 (87.5%) | 14 | `Import/Export/Transit`, `Negative Sekundärregelenergie
Negative secondary control energy`, `Negative Tertiärregelenergie
Negative tertiary control energy`, `Netto Ausspeisung aus dem Übertragungsnetz Schweiz
Net outflow of the Swiss transmission grid`, `Periode:`, … (+9) |
| `Unnamed: 1` | str | 79 (70.54%) | 15 | `AT→CH`, `CH→AT`, `CH→DE`, `CH→FR`, `CH→IT`, … (+10) |
| `Unnamed: 2` | float64 | 102 (91.07%) | 10 | -596733.20065 … 64678189.226866804 (mean 27782985.90) |
| `Unnamed: 3` | object | 79 (70.54%) | 13 | `-1147`, `-382.832`, `10310.206879816`, `11675.597942428`, `14078.390695588`, … (+8) |
| `Unnamed: 4` | float64 | 90 (80.36%) | 22 | 1371.44 … 32695110.559 (mean 6640872.44) |
| `Unnamed: 5` | float64 | 112 (100.0%) | 0 |  |
| `Unnamed: 6` | float64 | 112 (100.0%) | 0 |  |
| `Unnamed: 7` | str | 111 (99.11%) | 1 | `-` |
| `Unnamed: 8` | datetime64[us] | 111 (99.11%) | 1 | 2023-01-01 00:00:00 … 2023-01-01 00:00:00 |
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
| `Unnamed: 0` | str | 0 (0.0%) | 35037 | `Zeitstempel`, `01.01.2022 00:15`, `01.01.2022 00:30` |
| `Summe endverbrauchte Energie Regelblock Schweiz | Total energy consumed by end users in the Swiss controlblock` | object | 0 (0.0%) | 35041 | `kWh`, `1555423.369625`, `1552197.596625` |
| `Summe produzierte Energie Regelblock Schweiz | Total energy production Swiss controlblock` | object | 0 (0.0%) | 35041 | `kWh`, `1442339.754`, `1431794.195` |
| `Summe verbrauchte Energie Regelblock Schweiz | Total energy consumption Swiss controlblock` | object | 0 (0.0%) | 35041 | `kWh`, `1918280.671868`, `1917482.205604` |
| `Netto Ausspeisung aus dem Übertragungsnetz Schweiz | Net outflow of the Swiss transmission grid` | object | 0 (0.0%) | 21607 | `kWh`, `435976.885581`, `441481.251423` |
| `Vertikale Einspeisung ins Übertragungsnetz Schweiz | Grid feed-in Swiss transmission grid` | object | 0 (0.0%) | 35039 | `kWh`, `886147.891`, `883107.664` |
| `Positive Sekundär-Regelenergie | Positive secundary control energy` | object | 0 (0.0%) | 12822 | `kWh`, `24243`, `30114` |
| `Negative Sekundär-Regelenergie | Negative secundary control energy` | object | 0 (0.0%) | 11018 | `kWh`, `-418`, `0` |
| `Positive Tertiär-Regelenergie | Positive tertiary control energy` | object | 0 (0.0%) | 957 | `kWh`, `0`, `0` |
| `Negative Tertiär-Regelenergie | Negative tertiary control energy` | object | 0 (0.0%) | 634 | `kWh`, `0`, `0` |
| `Verbundaustausch CH->AT | Cross Border Exchange CH->AT` | object | 0 (0.0%) | 9870 | `kWh`, `9000`, `0` |
| `Verbundaustausch AT->CH | Cross Border Exchange AT->CH` | object | 0 (0.0%) | 26166 | `kWh`, `280829`, `305375` |
| `Verbundaustausch CH->DE | Cross Border Exchange CH->DE` | object | 0 (0.0%) | 13693 | `kWh`, `0`, `0` |
| `Verbundaustausch DE->CH | Cross Border Exchange DE->CH` | object | 0 (0.0%) | 33928 | `kWh`, `792930`, `805242` |
| `Verbundaustausch CH->FR | Cross Border Exchange CH->FR` | object | 0 (0.0%) | 27051 | `kWh`, `108843`, `93040` |
| `Verbundaustausch FR->CH | Cross Border Exchange FR->CH` | object | 0 (0.0%) | 33789 | `kWh`, `206076`, `208041` |
| `Verbundaustausch CH->IT | Cross Border Exchange CH->IT` | object | 0 (0.0%) | 34227 | `kWh`, `691519`, `745165` |
| `Verbundaustausch IT->CH | Cross Border Exchange IT->CH` | object | 0 (0.0%) | 21768 | `kWh`, `6953`, `6577` |
| `Transit` | object | 0 (0.0%) | 34329 | `kWh`, `809362`, `838205` |
| `Import` | object | 0 (0.0%) | 34622 | `kWh`, `1286788`, `1325235` |
| `Export` | object | 0 (0.0%) | 34364 | `kWh`, `809362`, `838205` |
| `Durchschnittliche positive Sekundär-Regelenergie Preise | Average positive secondary control energy prices` | object | 0 (0.0%) | 17445 | `Euro/MWh`, `143.96`, `143.96` |
| `Durchschnittliche negative Sekundär-Regelenergie Preise | Average negative secondary control energy prices` | object | 0 (0.0%) | 15797 | `Euro/MWh`, `95.98`, `95.98` |
| `Durchschnittliche positive Tertiär-Regelenergie Preise | Average positive tertiary control energy prices` | object | 0 (0.0%) | 7572 | `Euro/MWh`, `0`, `0` |
| `Durchschnittliche negative Tertiär-Regelenergie Preise | Average negative tertiary control energy prices` | object | 0 (0.0%) | 8100 | `Euro/MWh`, `0`, `0` |
| `Produktion Kanton AG | Production Canton AG` | object | 0 (0.0%) | 35017 | `kWh`, `512117.359`, `512024.572` |
| `Verbrauch Kanton AG | Consumption Canton AG` | object | 0 (0.0%) | 35037 | `kWh`, `135050.424`, `134373.626` |
| `Produktion Kanton FR | Production Canton FR` | object | 0 (0.0%) | 35005 | `kWh`, `51790.171`, `51502.519` |
| `Verbrauch Kanton FR | Consumption Canton FR` | object | 0 (0.0%) | 35025 | `kWh`, `73229.045`, `73536.432` |
| `Produktion Kanton GL | Production Canton GL` | object | 0 (0.0%) | 35033 | `kWh`, `20838.342`, `18366.346` |
| `Verbrauch Kanton GL | Consumption Canton GL` | object | 0 (0.0%) | 35024 | `kWh`, `197025.816`, `201927.616` |
| `Produktion Kanton GR | Production Canton GR` | object | 0 (0.0%) | 35039 | `kWh`, `43890.56`, `40254.494` |
| `Verbrauch Kanton GR | Consumption Canton GR` | object | 0 (0.0%) | 35027 | `kWh`, `83649.545`, `83779.598` |
| `Produktion Kanton LU | Production Canton LU` | object | 0 (0.0%) | 35010 | `kWh`, `11482.339`, `11517.933` |
| `Verbrauch Kanton LU | Consumption Canton LU` | object | 0 (0.0%) | 35035 | `kWh`, `102738.195`, `108404.982` |
| `Produktion Kanton NE | Production Canton NE` | object | 0 (0.0%) | 33915 | `kWh`, `949.759`, `1096.576` |
| `Verbrauch Kanton NE | Consumption Canton NE` | object | 0 (0.0%) | 34988 | `kWh`, `14365.556`, `14068.307` |
| `Produktion Kanton SO | Production Canton SO` | object | 0 (0.0%) | 35015 | `kWh`, `269925.976`, `270134.69` |
| `Verbrauch Kanton SO | Consumption Canton SO` | object | 0 (0.0%) | 35010 | `kWh`, `36690.751`, `36834.401` |
| `Produktion Kanton SG | Production Canton SG` | object | 0 (0.0%) | 35038 | `kWh`, `16276.6742`, `16866.783` |
| `Verbrauch Kanton SG | Consumption Canton SG` | object | 0 (0.0%) | 35040 | `kWh`, `84329.077`, `83101.1574` |
| `Produktion Kanton TI | Production Canton TI` | object | 0 (0.0%) | 35028 | `kWh`, `35253.175`, `33442.662` |
| `Verbrauch Kanton TI | Consumption Canton TI` | object | 0 (0.0%) | 35027 | `kWh`, `109026.567`, `108256.887` |
| `Produktion Kanton TG | Production Canton TG` | object | 0 (0.0%) | 34940 | `kWh`, `3904.838`, `4147.372` |
| `Verbrauch Kanton TG | Consumption Canton TG` | object | 0 (0.0%) | 35027 | `kWh`, `46423.864`, `46224.488` |
| `Produktion Kanton VS | Production Canton VS` | object | 0 (0.0%) | 35040 | `kWh`, `59791.926`, `62637.785` |
| `Verbrauch Kanton VS | Consumption Canton VS` | object | 0 (0.0%) | 35041 | `kWh`, `101790.405449`, `100816.371027` |
| `Produktion Kantone AI, AR | Production Cantons AI, AR` | object | 0 (0.0%) | 35011 | `kWh`, `3470.3358`, `3470.821` |
| `Verbrauch Kantone AI, AR | Consumption Cantons AI, AR` | object | 0 (0.0%) | 35030 | `kWh`, `14685.991`, `14240.8896` |
| `Produktion Kantone BL, BS | Production Cantons BL, BS` | object | 0 (0.0%) | 35023 | `kWh`, `28987.447`, `29010.31` |
| `Verbrauch Kantone BL, BS | Consumption Cantons BL, BS` | object | 0 (0.0%) | 35029 | `kWh`, `87334.408`, `87043.281` |
| `Produktion Kantone BE, JU | Production Cantons BE, JU` | object | 0 (0.0%) | 35039 | `kWh`, `122551.612`, `118941.679` |
| `Verbrauch Kantone BE, JU | Consumption Cantons BE, JU` | object | 0 (0.0%) | 35037 | `kWh`, `239392.687`, `240601.63` |
| `Produktion Kantone SZ, ZG | Production Cantons SZ, ZG` | object | 0 (0.0%) | 34996 | `kWh`, `9527.196`, `9366.988` |
| `Verbrauch Kantone SZ, ZG | Consumption Cantons SZ, ZG` | object | 0 (0.0%) | 35028 | `kWh`, `55134.465`, `54625.102` |
| `Produktion Kantone OW, NW, UR | Production Cantons OW, NW, UR` | object | 0 (0.0%) | 35027 | `kWh`, `25073.042`, `23920.183` |
| `Verbrauch Kantone OW, NW, UR | Consumption Cantons OW, NW, UR` | object | 0 (0.0%) | 35003 | `kWh`, `29253.345`, `29056.285` |
| `Produktion Kantone GE, VD | Production Cantons GE, VD` | object | 0 (0.0%) | 35037 | `kWh`, `72383.086`, `70942.102` |
| `Verbrauch Kantone GE, VD | Consumption Cantons GE, VD` | object | 0 (0.0%) | 35037 | `kWh`, `188887.481`, `177208.012` |
| `Produktion Kantone SH, ZH | Production Cantons SH, ZH` | object | 0 (0.0%) | 35015 | `kWh`, `20145.314`, `19697.792` |
| `Verbrauch Kantone SH, ZH | Consumption Cantons SH, ZH` | object | 0 (0.0%) | 35036 | `kWh`, `260072.787`, `260629.269` |
| `Produktion Kantonsübergreifend | Production across Cantons` | object | 0 (0.0%) | 35036 | `kWh`, `130321.247`, `130766.131` |
| `Verbrauch Kantonsübergreifend | Consumption across Cantons` | object | 0 (0.0%) | 35041 | `kWh`, `46543.590419`, `50139.225577` |
| `Produktion Regelzone CH - Ausländische Gebiete | Production control area CH - foreign territories` | object | 0 (0.0%) | 34945 | `kWh`, `3659.355`, `3686.457` |
| `Verbrauch Regelzone CH - Ausländische Gebiete | Consumption control area CH - foreign territories` | object | 0 (0.0%) | 34997 | `kWh`, `12656.672`, `12614.646` |

## Sheet: `Zeitreihen1h00`

**Zeilen:** 8,761
**Spalten:** 2

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Unnamed: 0` | str | 0 (0.0%) | 8760 | `Zeitstempel`, `01.01.2022 01:00`, `01.01.2022 02:00` |
| `Vertikale Netzlast Übertragungsnetz Schweiz | Vertical load Swiss transmission grid` | object | 0 (0.0%) | 8761 | `MW`, `5203.460248`, `5004.220127` |
