# Profil: energieuebersicht_ch_2025.xlsx

**Erstellt:** 2026-05-05T21:19:04
**Pfad:** `C:\Users\pelle\SynologyDrive\Docs\Studium\FHGR\Masterthesis\energy-viz\pipeline\raw\snapshots\2026-05-05\swissgrid\energieuebersicht_ch_2025.xlsx`
**Format:** XLSX

**Sheets:** Einstellungen, Datetime, Uebersicht, Zeitreihen0h15

## Sheet: `Einstellungen`

**Zeilen:** 43
**Spalten:** 22

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Energieübersicht Schweiz 2025` | str | 32 (74.42%) | 11 | `Anleitung`, `Ausgewählt | Selected:`, `Betrachtungszeitraum | Observation Period`, `Bis | To:`, `Das hier vorliegende Excel-Sheet beinhaltet die Gesamtübersicht der wichtigsten Eckdaten der Regelzone Schweiz.

Die Daten sind aggregierte Viertelstunden, welche zu ihrer Referenz im Blatt «Zeitreihen» abgelegt sind. Ab 2025 sind die Daten linksbündig, das heißt: der Zeitstempel bei "00:00" betrifft das Zeitintervall 00:00 – 00:15. Die Daten sind dieselben, wie auch von Swissgrid zu Abrechnungszwecken verwendet werden.

Nebst den Zeitreihen finden Sie auf dem Blatt «Übersicht» die Summen der jeweiligen Energiegrösse welche für den eingestellten Zeitraum direkt berechnet werden. Der Betrachtungszeitraum kann auf dieser Seite eingestellt werden.

Achtung: Bei MS-Excel 2003 und älter werden einige Felder nicht automatisch berechnet. Drücken Sie daher STRG+ALT+F9 nachdem Sie die Datei geöffnet haben.`, … (+6) |
| `Unnamed: 1` | str | 42 (97.67%) | 1 | `23.04.2026 09:59:08` |
| `Unnamed: 2` | object | 39 (90.7%) | 3 | `1`, `DD`, `MW / MWh` |
| `Unnamed: 3` | object | 40 (93.02%) | 2 | `1`, `MM` |
| `Unnamed: 4` | object | 40 (93.02%) | 3 | `2025`, `2026`, `YYYY` |
| `Unnamed: 5` | object | 40 (93.02%) | 2 | `0`, `hh` |
| `Unnamed: 6` | object | 40 (93.02%) | 2 | `0`, `min` |
| `Unnamed: 7` | datetime64[us] | 41 (95.35%) | 2 | 2025-01-01 00:00:00 … 2026-01-01 00:00:00 |
| `Unnamed: 8` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 9` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 10` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 11` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 12` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 13` | float64 | 43 (100.0%) | 0 |  |
| `1` | float64 | 13 (30.23%) | 30 | 2.0 … 31.0 (mean 16.50) |
| `1.1` | float64 | 32 (74.42%) | 11 | 2.0 … 12.0 (mean 7.00) |
| `2025` | float64 | 42 (97.67%) | 1 | 2026.0 … 2026.0 (mean 2026.00) |
| `0` | float64 | 20 (46.51%) | 23 | 1.0 … 23.0 (mean 12.00) |
| `0.1` | float64 | 40 (93.02%) | 3 | 15.0 … 45.0 (mean 30.00) |
| `kW / kWh` | str | 42 (97.67%) | 1 | `MW / MWh` |
| `Frühstes Datum` | str | 39 (90.7%) | 4 | `Faktor:`, `Prefix:`, `Spätestes Datum`, `anzMonate` |
| `2025-01-01 00:00:00` | object | 39 (90.7%) | 4 | `1`, `12`, `2026-01-01 00:00:00`, `M` |

## Sheet: `Datetime`

**Zeilen:** 35,137
**Spalten:** 1

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Unnamed: 0` | object | 96 (0.27%) | 35037 | `Zeitstempel 0h15`, `2025-01-01 00:00:00`, `2025-01-01 00:15:00` |

## Sheet: `Uebersicht`

**Zeilen:** 106
**Spalten:** 15

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Energieübersicht Schweiz 2025` | str | 93 (87.74%) | 13 | `Import/Export/Transit`, `Negative Sekundärregelenergie
Negative secondary control energy`, `Negative Tertiärregelenergie
Negative tertiary control energy`, `Netto Ausspeisung aus dem Übertragungsnetz Schweiz
Net outflow of the Swiss transmission grid`, `Periode:`, … (+8) |
| `Unnamed: 1` | str | 75 (70.75%) | 15 | `AT→CH`, `CH→AT`, `CH→DE`, `CH→FR`, `CH→IT`, … (+10) |
| `Unnamed: 2` | float64 | 97 (91.51%) | 9 | -389472.16 … 62077641.51142447 (mean 25083478.15) |
| `Unnamed: 3` | object | 74 (69.81%) | 12 | `-1134.012`, `-474.42797199999995`, `10420.962394481121`, `13589.085571999998`, `1714`, … (+7) |
| `Unnamed: 4` | float64 | 84 (79.25%) | 22 | 1875.568 … 30150080.508 (mean 6456691.89) |
| `Unnamed: 5` | float64 | 106 (100.0%) | 0 |  |
| `Unnamed: 6` | float64 | 106 (100.0%) | 0 |  |
| `Unnamed: 7` | str | 105 (99.06%) | 1 | `-` |
| `Unnamed: 8` | datetime64[us] | 105 (99.06%) | 1 | 2026-01-01 00:00:00 … 2026-01-01 00:00:00 |
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

**Zeilen:** 35,041
**Spalten:** 65

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Unnamed: 0` | str | 0 (0.0%) | 35037 | `Zeitstempel`, `01.01.2025 00:00`, `01.01.2025 00:15` |
| `Summe endverbrauchte Energie Regelblock Schweiz | Total energy consumed by end users in the Swiss controlblock` | object | 0 (0.0%) | 35041 | `kWh`, `1659414.8431931555`, `1654563.4831204708` |
| `Summe produzierte Energie Regelblock Schweiz | Total energy production Swiss controlblock` | object | 0 (0.0%) | 35041 | `kWh`, `1346483.7230000002`, `1336186.057` |
| `Summe verbrauchte Energie Regelblock Schweiz | Total energy consumption Swiss controlblock` | object | 0 (0.0%) | 35041 | `kWh`, `1894980.135373`, `1883657.4474529994` |
| `Netto Ausspeisung aus dem Übertragungsnetz Schweiz | Net outflow of the Swiss transmission grid` | object | 0 (0.0%) | 19043 | `kWh`, `501763.71562699985`, `506524.8135469996` |
| `Vertikale Einspeisung ins Übertragungsnetz Schweiz | Grid feed-in Swiss transmission grid` | object | 0 (0.0%) | 35041 | `kWh`, `1466277.0416269999`, `1465358.1405469996` |
| `Positive Sekundär-Regelenergie | Positive secundary control energy` | object | 0 (0.0%) | 33331 | `kWh`, `18260.102000000003`, `28628.197` |
| `Negative Sekundär-Regelenergie | Negative secundary control energy` | object | 0 (0.0%) | 32930 | `kWh`, `-29.325`, `0` |
| `Positive Tertiär-Regelenergie | Positive tertiary control energy` | object | 0 (0.0%) | 925 | `kWh`, `51750`, `51750` |
| `Negative Tertiär-Regelenergie | Negative tertiary control energy` | object | 0 (0.0%) | 608 | `kWh`, `0`, `0` |
| `Verbundaustausch CH->AT | Cross Border Exchange CH->AT` | object | 0 (0.0%) | 17092 | `kWh`, `44500`, `13899.999999999998` |
| `Verbundaustausch AT->CH | Cross Border Exchange AT->CH` | object | 0 (0.0%) | 21420 | `kWh`, `222630`, `223640` |
| `Verbundaustausch CH->DE | Cross Border Exchange CH->DE` | object | 0 (0.0%) | 27696 | `kWh`, `6800`, `700` |
| `Verbundaustausch DE->CH | Cross Border Exchange DE->CH` | object | 0 (0.0%) | 29821 | `kWh`, `817935.9999999999`, `743470.0000000001` |
| `Verbundaustausch CH->FR | Cross Border Exchange CH->FR` | object | 0 (0.0%) | 18632 | `kWh`, `94388`, `92752.00000000001` |
| `Verbundaustausch FR->CH | Cross Border Exchange FR->CH` | object | 0 (0.0%) | 34556 | `kWh`, `368563`, `351840.00000000006` |
| `Verbundaustausch CH->IT | Cross Border Exchange CH->IT` | object | 0 (0.0%) | 34736 | `kWh`, `727187.9999999999`, `680404` |
| `Verbundaustausch IT->CH | Cross Border Exchange IT->CH` | object | 0 (0.0%) | 26653 | `kWh`, `12887`, `18002.000000000004` |
| `Transit` | object | 0 (0.0%) | 34751 | `kWh`, `872876`, `787756.0000000001` |
| `Import` | object | 0 (0.0%) | 34835 | `kWh`, `1422015.9999999998`, `1336952.0000000002` |
| `Export` | object | 0 (0.0%) | 34842 | `kWh`, `872875.9999999999`, `787756.0000000001` |
| `Durchschnittliche positive Sekundär-Regelenergie Preise | Average positive secondary control energy prices` | object | 0 (0.0%) | 19231 | `Euro/MWh`, `294.81`, `559.75` |
| `Durchschnittliche negative Sekundär-Regelenergie Preise | Average negative secondary control energy prices` | object | 0 (0.0%) | 21598 | `Euro/MWh`, `39.24`, `0` |
| `Durchschnittliche positive Tertiär-Regelenergie Preise | Average positive tertiary control energy prices` | object | 0 (0.0%) | 16155 | `Euro/MWh`, `155.10000000000002`, `155.10000000000002` |
| `Durchschnittliche negative Tertiär-Regelenergie Preise | Average negative tertiary control energy prices` | object | 0 (0.0%) | 11727 | `Euro/MWh`, `0`, `0` |
| `Produktion Kanton AG | Production Canton AG` | object | 0 (0.0%) | 35041 | `kWh`, `506882.46499999997`, `507043.911` |
| `Verbrauch Kanton AG | Consumption Canton AG` | object | 0 (0.0%) | 35041 | `kWh`, `154357.28600000005`, `156974.1619999999` |
| `Produktion Kanton FR | Production Canton FR` | object | 0 (0.0%) | 35038 | `kWh`, `9306.135999999999`, `9389.394` |
| `Verbrauch Kanton FR | Consumption Canton FR` | object | 0 (0.0%) | 35031 | `kWh`, `84200.12199999999`, `83945.13999999998` |
| `Produktion Kanton GL | Production Canton GL` | object | 0 (0.0%) | 35036 | `kWh`, `22279.578999999998`, `25880.159999999996` |
| `Verbrauch Kanton GL | Consumption Canton GL` | object | 0 (0.0%) | 35036 | `kWh`, `11138.966`, `10858.787` |
| `Produktion Kanton GR | Production Canton GR` | object | 0 (0.0%) | 35041 | `kWh`, `79466.86700000001`, `78600.25799999999` |
| `Verbrauch Kanton GR | Consumption Canton GR` | object | 0 (0.0%) | 35040 | `kWh`, `76374.08100000002`, `76356.56599999999` |
| `Produktion Kanton LU | Production Canton LU` | object | 0 (0.0%) | 35035 | `kWh`, `6976.613000000001`, `7146.725` |
| `Verbrauch Kanton LU | Consumption Canton LU` | object | 0 (0.0%) | 35038 | `kWh`, `96906.24`, `96016.40100000001` |
| `Produktion Kanton NE | Production Canton NE` | object | 0 (0.0%) | 34763 | `kWh`, `321.799`, `297.84000000000003` |
| `Verbrauch Kanton NE | Consumption Canton NE` | object | 0 (0.0%) | 35025 | `kWh`, `14355.237`, `14104.865999999998` |
| `Produktion Kanton SO | Production Canton SO` | object | 0 (0.0%) | 35039 | `kWh`, `263314.72899999993`, `263102.37700000004` |
| `Verbrauch Kanton SO | Consumption Canton SO` | object | 0 (0.0%) | 35039 | `kWh`, `40334.20599999999`, `40683.89899999999` |
| `Produktion Kanton SG | Production Canton SG` | object | 0 (0.0%) | 35039 | `kWh`, `9035.937800000002`, `9382.144199999997` |
| `Verbrauch Kanton SG | Consumption Canton SG` | object | 0 (0.0%) | 35041 | `kWh`, `92677.6594`, `91026.42120000001` |
| `Produktion Kanton TI | Production Canton TI` | object | 0 (0.0%) | 35041 | `kWh`, `21785.35`, `20054.713000000003` |
| `Verbrauch Kanton TI | Consumption Canton TI` | object | 0 (0.0%) | 35040 | `kWh`, `80666.60499999997`, `79706.04699999999` |
| `Produktion Kanton TG | Production Canton TG` | object | 0 (0.0%) | 35016 | `kWh`, `4152.845`, `4310.246` |
| `Verbrauch Kanton TG | Consumption Canton TG` | object | 0 (0.0%) | 35039 | `kWh`, `53415.14499999998`, `53074.62599999995` |
| `Produktion Kanton VS | Production Canton VS` | object | 0 (0.0%) | 35041 | `kWh`, `188570.90199999994`, `180579.23299999995` |
| `Verbrauch Kanton VS | Consumption Canton VS` | object | 0 (0.0%) | 35039 | `kWh`, `157104.63600000006`, `155613.10700000002` |
| `Produktion Kantone AI, AR | Production Cantons AI, AR` | object | 0 (0.0%) | 35034 | `kWh`, `955.7222`, `976.2988` |
| `Verbrauch Kantone AI, AR | Consumption Cantons AI, AR` | object | 0 (0.0%) | 35038 | `kWh`, `16240.511600000002`, `15847.047799999998` |
| `Produktion Kantone BL, BS | Production Cantons BL, BS` | object | 0 (0.0%) | 35033 | `kWh`, `23703.419`, `24057.597` |
| `Verbrauch Kantone BL, BS | Consumption Cantons BL, BS` | object | 0 (0.0%) | 35038 | `kWh`, `92203.57`, `92454.86600000001` |
| `Produktion Kantone BE, JU | Production Cantons BE, JU` | object | 0 (0.0%) | 35040 | `kWh`, `58575.41399999998`, `55170.101` |
| `Verbrauch Kantone BE, JU | Consumption Cantons BE, JU` | object | 0 (0.0%) | 35041 | `kWh`, `228827.8859999999`, `230406.02799999993` |
| `Produktion Kantone SZ, ZG | Production Cantons SZ, ZG` | object | 0 (0.0%) | 35031 | `kWh`, `5004.696`, `5003.418000000001` |
| `Verbrauch Kantone SZ, ZG | Consumption Cantons SZ, ZG` | object | 0 (0.0%) | 35037 | `kWh`, `58266.431`, `57887.52700000001` |
| `Produktion Kantone OW, NW, UR | Production Cantons OW, NW, UR` | object | 0 (0.0%) | 35036 | `kWh`, `10274.564`, `9351.599` |
| `Verbrauch Kantone OW, NW, UR | Consumption Cantons OW, NW, UR` | object | 0 (0.0%) | 35030 | `kWh`, `31812.56700000001`, `31343.600000000002` |
| `Produktion Kantone GE, VD | Production Cantons GE, VD` | object | 0 (0.0%) | 35041 | `kWh`, `28985.000999999997`, `28952.908` |
| `Verbrauch Kantone GE, VD | Consumption Cantons GE, VD` | object | 0 (0.0%) | 35041 | `kWh`, `249591.732`, `246870.00299999997` |
| `Produktion Kantone SH, ZH | Production Cantons SH, ZH` | object | 0 (0.0%) | 35032 | `kWh`, `21357.967000000004`, `21640.989` |
| `Verbrauch Kantone SH, ZH | Consumption Cantons SH, ZH` | object | 0 (0.0%) | 35041 | `kWh`, `288071.2880000001`, `286650.2669999998` |
| `Produktion Kantonsübergreifend | Production across Cantons` | object | 0 (0.0%) | 35040 | `kWh`, `80285.354`, `79923.912` |
| `Verbrauch Kantonsübergreifend | Consumption across Cantons` | object | 0 (0.0%) | 35041 | `kWh`, `52433.26137299968`, `47961.099452999595` |
| `Produktion Regelzone CH - Ausländische Gebiete | Production control area CH - foreign territories` | object | 0 (0.0%) | 34997 | `kWh`, `5248.362999999999`, `5322.233` |
| `Verbrauch Regelzone CH - Ausländische Gebiete | Consumption control area CH - foreign territories` | object | 0 (0.0%) | 35025 | `kWh`, `16002.705`, `15876.986999999997` |
