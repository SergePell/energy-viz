# Profil: energieuebersicht_ch_2026.xlsx

**Erstellt:** 2026-05-05T21:19:08
**Pfad:** `C:\Users\pelle\SynologyDrive\Docs\Studium\FHGR\Masterthesis\energy-viz\pipeline\raw\snapshots\2026-05-05\swissgrid\energieuebersicht_ch_2026.xlsx`
**Format:** XLSX

**Sheets:** Einstellungen, Datetime, Uebersicht, Zeitreihen0h15

## Sheet: `Einstellungen`

**Zeilen:** 43
**Spalten:** 22

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Energieübersicht Schweiz 2026` | str | 32 (74.42%) | 11 | `Anleitung`, `Ausgewählt | Selected:`, `Betrachtungszeitraum | Observation Period`, `Bis | To:`, `Das hier vorliegende Excel-Sheet beinhaltet die Gesamtübersicht der wichtigsten Eckdaten der Regelzone Schweiz.

Die Daten sind aggregierte Viertelstunden, welche zu ihrer Referenz im Blatt «Zeitreihen» abgelegt sind. Ab 2025 sind die Daten linksbündig, das heißt: der Zeitstempel bei "00:00" betrifft das Zeitintervall 00:00 – 00:15. Die Daten sind dieselben, wie auch von Swissgrid zu Abrechnungszwecken verwendet werden.

Nebst den Zeitreihen finden Sie auf dem Blatt «Übersicht» die Summen der jeweiligen Energiegrösse welche für den eingestellten Zeitraum direkt berechnet werden. Der Betrachtungszeitraum kann auf dieser Seite eingestellt werden.

Achtung: Bei MS-Excel 2003 und älter werden einige Felder nicht automatisch berechnet. Drücken Sie daher STRG+ALT+F9 nachdem Sie die Datei geöffnet haben.`, … (+6) |
| `Unnamed: 1` | str | 42 (97.67%) | 1 | `17.04.2026 07:42:29` |
| `Unnamed: 2` | object | 39 (90.7%) | 3 | `1`, `DD`, `MW / MWh` |
| `Unnamed: 3` | object | 40 (93.02%) | 3 | `1`, `3`, `MM` |
| `Unnamed: 4` | object | 40 (93.02%) | 2 | `2026`, `YYYY` |
| `Unnamed: 5` | object | 40 (93.02%) | 2 | `0`, `hh` |
| `Unnamed: 6` | object | 40 (93.02%) | 2 | `0`, `min` |
| `Unnamed: 7` | datetime64[us] | 41 (95.35%) | 2 | 2026-01-01 00:00:00 … 2026-03-01 00:00:00 |
| `Unnamed: 8` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 9` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 10` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 11` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 12` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 13` | float64 | 43 (100.0%) | 0 |  |
| `1` | float64 | 13 (30.23%) | 30 | 2.0 … 31.0 (mean 16.50) |
| `1.1` | float64 | 32 (74.42%) | 11 | 2.0 … 12.0 (mean 7.00) |
| `2026` | float64 | 42 (97.67%) | 1 | 2027.0 … 2027.0 (mean 2027.00) |
| `0` | float64 | 20 (46.51%) | 23 | 1.0 … 23.0 (mean 12.00) |
| `0.1` | float64 | 40 (93.02%) | 3 | 15.0 … 45.0 (mean 30.00) |
| `kW / kWh` | str | 42 (97.67%) | 1 | `MW / MWh` |
| `Frühstes Datum` | str | 39 (90.7%) | 4 | `Faktor:`, `Prefix:`, `Spätestes Datum`, `anzMonate` |
| `2026-01-01 00:00:00` | object | 39 (90.7%) | 4 | `1`, `12`, `2027-01-01 00:00:00`, `M` |

## Sheet: `Datetime`

**Zeilen:** 35,137
**Spalten:** 1

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Unnamed: 0` | object | 26500 (75.42%) | 8637 | `Zeitstempel 0h15`, `2026-01-01 00:00:00`, `2026-01-01 00:15:00` |

## Sheet: `Uebersicht`

**Zeilen:** 106
**Spalten:** 15

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Energieübersicht Schweiz 2026` | str | 93 (87.74%) | 13 | `Import/Export/Transit`, `Negative Sekundärregelenergie
Negative secondary control energy`, `Negative Tertiärregelenergie
Negative tertiary control energy`, `Netto Ausspeisung aus dem Übertragungsnetz Schweiz
Net outflow of the Swiss transmission grid`, `Periode:`, … (+8) |
| `Unnamed: 1` | str | 75 (70.75%) | 15 | `AT→CH`, `CH→AT`, `CH→DE`, `CH→FR`, `CH→IT`, … (+10) |
| `Unnamed: 2` | float64 | 97 (91.51%) | 9 | -41276.5 … 11784565.046657667 (mean 4801376.65) |
| `Unnamed: 3` | object | 74 (69.81%) | 12 | `-271.25714000000005`, `-538`, `10569.792763172`, `1069`, `13794.452482908444`, … (+7) |
| `Unnamed: 4` | float64 | 84 (79.25%) | 22 | 1696.2720000000002 … 6650909.964 (mean 1065404.48) |
| `Unnamed: 5` | float64 | 106 (100.0%) | 0 |  |
| `Unnamed: 6` | float64 | 106 (100.0%) | 0 |  |
| `Unnamed: 7` | str | 105 (99.06%) | 1 | `-` |
| `Unnamed: 8` | datetime64[us] | 105 (99.06%) | 1 | 2026-03-01 00:00:00 … 2026-03-01 00:00:00 |
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

**Zeilen:** 8,637
**Spalten:** 65

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Unnamed: 0` | str | 0 (0.0%) | 8637 | `Zeitstempel`, `01.01.2026 00:00`, `01.01.2026 00:15` |
| `Summe endverbrauchte Energie Regelblock Schweiz | Total energy consumed by end users in the Swiss controlblock` | object | 0 (0.0%) | 8637 | `kWh`, `1795064.4572350704`, `1793718.38915817` |
| `Summe produzierte Energie Regelblock Schweiz | Total energy production Swiss controlblock` | object | 0 (0.0%) | 8637 | `kWh`, `1035916.6150000001`, `1041729.3059999999` |
| `Summe verbrauchte Energie Regelblock Schweiz | Total energy consumption Swiss controlblock` | object | 0 (0.0%) | 8637 | `kWh`, `1920830.1817929994`, `1912744.0327929999` |
| `Netto Ausspeisung aus dem Übertragungsnetz Schweiz | Net outflow of the Swiss transmission grid` | object | 0 (0.0%) | 7159 | `kWh`, `852572.7982069999`, `838874.4612070001` |
| `Vertikale Einspeisung ins Übertragungsnetz Schweiz | Grid feed-in Swiss transmission grid` | object | 0 (0.0%) | 8637 | `kWh`, `1587766.1202069998`, `1583967.786207` |
| `Positive Sekundär-Regelenergie | Positive secundary control energy` | object | 0 (0.0%) | 8364 | `kWh`, `276.646`, `78.296` |
| `Negative Sekundär-Regelenergie | Negative secundary control energy` | object | 0 (0.0%) | 8032 | `kWh`, `-6260.099999999999`, `-14551.848000000002` |
| `Positive Tertiär-Regelenergie | Positive tertiary control energy` | object | 0 (0.0%) | 522 | `kWh`, `62250`, `55500` |
| `Negative Tertiär-Regelenergie | Negative tertiary control energy` | object | 0 (0.0%) | 295 | `kWh`, `0`, `0` |
| `Verbundaustausch CH->AT | Cross Border Exchange CH->AT` | object | 0 (0.0%) | 4410 | `kWh`, `50300`, `30400` |
| `Verbundaustausch AT->CH | Cross Border Exchange AT->CH` | object | 0 (0.0%) | 6552 | `kWh`, `186429`, `183792.00000000003` |
| `Verbundaustausch CH->DE | Cross Border Exchange CH->DE` | object | 0 (0.0%) | 5813 | `kWh`, `6900`, `6900` |
| `Verbundaustausch DE->CH | Cross Border Exchange DE->CH` | object | 0 (0.0%) | 8446 | `kWh`, `979386`, `968869.9999999998` |
| `Verbundaustausch CH->FR | Cross Border Exchange CH->FR` | object | 0 (0.0%) | 2928 | `kWh`, `140664`, `154771.00000000003` |
| `Verbundaustausch FR->CH | Cross Border Exchange FR->CH` | object | 0 (0.0%) | 8602 | `kWh`, `311790`, `301123` |
| `Verbundaustausch CH->IT | Cross Border Exchange CH->IT` | object | 0 (0.0%) | 8615 | `kWh`, `429986`, `428417.00000000006` |
| `Verbundaustausch IT->CH | Cross Border Exchange IT->CH` | object | 0 (0.0%) | 7068 | `kWh`, `36042`, `39796` |
| `Transit` | object | 0 (0.0%) | 8629 | `kWh`, `627850`, `620488` |
| `Import` | object | 0 (0.0%) | 8624 | `kWh`, `1513647`, `1493580.9999999998` |
| `Export` | object | 0 (0.0%) | 8632 | `kWh`, `627850`, `620488` |
| `Durchschnittliche positive Sekundär-Regelenergie Preise | Average positive secondary control energy prices` | object | 0 (0.0%) | 6281 | `Euro/MWh`, `169`, `169` |
| `Durchschnittliche negative Sekundär-Regelenergie Preise | Average negative secondary control energy prices` | object | 0 (0.0%) | 6088 | `Euro/MWh`, `-70.11`, `-91.21` |
| `Durchschnittliche positive Tertiär-Regelenergie Preise | Average positive tertiary control energy prices` | object | 0 (0.0%) | 3489 | `Euro/MWh`, `124.27341365461848`, `124.06193693693693` |
| `Durchschnittliche negative Tertiär-Regelenergie Preise | Average negative tertiary control energy prices` | object | 0 (0.0%) | 2244 | `Euro/MWh`, `0`, `0` |
| `Produktion Kanton AG | Production Canton AG` | object | 0 (0.0%) | 8637 | `kWh`, `505796.011`, `505988.4829999998` |
| `Verbrauch Kanton AG | Consumption Canton AG` | object | 0 (0.0%) | 8637 | `kWh`, `165702.60099999997`, `167748.53699999995` |
| `Produktion Kanton FR | Production Canton FR` | object | 0 (0.0%) | 8637 | `kWh`, `7748.54`, `7718.014` |
| `Verbrauch Kanton FR | Consumption Canton FR` | object | 0 (0.0%) | 8637 | `kWh`, `95248.49799999999`, `96049.47099999999` |
| `Produktion Kanton GL | Production Canton GL` | object | 0 (0.0%) | 8637 | `kWh`, `2725.7729999999997`, `2561.057` |
| `Verbrauch Kanton GL | Consumption Canton GL` | object | 0 (0.0%) | 8635 | `kWh`, `12072.091`, `11965.972999999996` |
| `Produktion Kanton GR | Production Canton GR` | object | 0 (0.0%) | 8637 | `kWh`, `97152.48400000001`, `106048.50799999999` |
| `Verbrauch Kanton GR | Consumption Canton GR` | object | 0 (0.0%) | 8637 | `kWh`, `87804.33700000004`, `87685.358` |
| `Produktion Kanton LU | Production Canton LU` | object | 0 (0.0%) | 8636 | `kWh`, `7768.78`, `7752.896` |
| `Verbrauch Kanton LU | Consumption Canton LU` | object | 0 (0.0%) | 8637 | `kWh`, `95425.85599999999`, `95114.39399999997` |
| `Produktion Kanton NE | Production Canton NE` | object | 0 (0.0%) | 8618 | `kWh`, `195.625`, `283.89799999999997` |
| `Verbrauch Kanton NE | Consumption Canton NE` | object | 0 (0.0%) | 8637 | `kWh`, `14857.323000000002`, `14607.556` |
| `Produktion Kanton SO | Production Canton SO` | object | 0 (0.0%) | 8637 | `kWh`, `6280.342`, `5769.456` |
| `Verbrauch Kanton SO | Consumption Canton SO` | object | 0 (0.0%) | 8637 | `kWh`, `44020.45399999997`, `43915.19599999995` |
| `Produktion Kanton SG | Production Canton SG` | object | 0 (0.0%) | 8637 | `kWh`, `8993.9746`, `9009.798999999999` |
| `Verbrauch Kanton SG | Consumption Canton SG` | object | 0 (0.0%) | 8637 | `kWh`, `99897.5102`, `98711.07799999998` |
| `Produktion Kanton TI | Production Canton TI` | object | 0 (0.0%) | 8637 | `kWh`, `67083.252`, `69903.40699999999` |
| `Verbrauch Kanton TI | Consumption Canton TI` | object | 0 (0.0%) | 8637 | `kWh`, `84093.798`, `83623.81900000002` |
| `Produktion Kanton TG | Production Canton TG` | object | 0 (0.0%) | 8637 | `kWh`, `2701.5170000000003`, `2678.4400000000005` |
| `Verbrauch Kanton TG | Consumption Canton TG` | object | 0 (0.0%) | 8637 | `kWh`, `55844.58200000004`, `56145.721999999936` |
| `Produktion Kanton VS | Production Canton VS` | object | 0 (0.0%) | 8637 | `kWh`, `145791.54899999997`, `147984.73900000006` |
| `Verbrauch Kanton VS | Consumption Canton VS` | object | 0 (0.0%) | 8637 | `kWh`, `115410.08399999994`, `114761.44699999999` |
| `Produktion Kantone AI, AR | Production Cantons AI, AR` | object | 0 (0.0%) | 8637 | `kWh`, `495.2714`, `488.17600000000004` |
| `Verbrauch Kantone AI, AR | Consumption Cantons AI, AR` | object | 0 (0.0%) | 8636 | `kWh`, `18239.0828`, `17965.825000000004` |
| `Produktion Kantone BL, BS | Production Cantons BL, BS` | object | 0 (0.0%) | 8635 | `kWh`, `17352.51`, `17211.354` |
| `Verbrauch Kantone BL, BS | Consumption Cantons BL, BS` | object | 0 (0.0%) | 8636 | `kWh`, `95473.244`, `96600.437` |
| `Produktion Kantone BE, JU | Production Cantons BE, JU` | object | 0 (0.0%) | 8637 | `kWh`, `48039.115000000005`, `41580.26699999997` |
| `Verbrauch Kantone BE, JU | Consumption Cantons BE, JU` | object | 0 (0.0%) | 8637 | `kWh`, `257175.20899999986`, `254675.05700000012` |
| `Produktion Kantone SZ, ZG | Production Cantons SZ, ZG` | object | 0 (0.0%) | 8637 | `kWh`, `5683.503`, `5597.133` |
| `Verbrauch Kantone SZ, ZG | Consumption Cantons SZ, ZG` | object | 0 (0.0%) | 8637 | `kWh`, `62153.662999999986`, `61838.11` |
| `Produktion Kantone OW, NW, UR | Production Cantons OW, NW, UR` | object | 0 (0.0%) | 8637 | `kWh`, `9350.685`, `9273.502` |
| `Verbrauch Kantone OW, NW, UR | Consumption Cantons OW, NW, UR` | object | 0 (0.0%) | 8636 | `kWh`, `34663.68400000001`, `34268.501000000004` |
| `Produktion Kantone GE, VD | Production Cantons GE, VD` | object | 0 (0.0%) | 8637 | `kWh`, `20366.862`, `20350.982000000004` |
| `Verbrauch Kantone GE, VD | Consumption Cantons GE, VD` | object | 0 (0.0%) | 8637 | `kWh`, `204384.89599999995`, `198286.31300000002` |
| `Produktion Kantone SH, ZH | Production Cantons SH, ZH` | object | 0 (0.0%) | 8637 | `kWh`, `19881.532000000003`, `19872.380000000005` |
| `Verbrauch Kantone SH, ZH | Consumption Cantons SH, ZH` | object | 0 (0.0%) | 8637 | `kWh`, `305189.731`, `306512.69600000005` |
| `Produktion Kantonsübergreifend | Production across Cantons` | object | 0 (0.0%) | 8636 | `kWh`, `59820.252`, `58947.632` |
| `Verbrauch Kantonsübergreifend | Consumption across Cantons` | object | 0 (0.0%) | 8637 | `kWh`, `56918.42079299975`, `56315.21279300004` |
| `Produktion Regelzone CH - Ausländische Gebiete | Production control area CH - foreign territories` | object | 0 (0.0%) | 8631 | `kWh`, `2689.0370000000003`, `2709.1830000000004` |
| `Verbrauch Regelzone CH - Ausländische Gebiete | Consumption control area CH - foreign territories` | object | 0 (0.0%) | 8636 | `kWh`, `16255.117000000002`, `15953.33` |
