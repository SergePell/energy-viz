# Profil: energieuebersicht_ch_2023.xlsx

**Erstellt:** 2026-05-05T21:18:37
**Pfad:** `C:\Users\pelle\SynologyDrive\Docs\Studium\FHGR\Masterthesis\energy-viz\pipeline\raw\snapshots\2026-05-05\swissgrid\energieuebersicht_ch_2023.xlsx`
**Format:** XLSX

**Sheets:** Einstellungen, Datetime, Uebersicht, Zeitreihen0h15

## Sheet: `Einstellungen`

**Zeilen:** 43
**Spalten:** 22

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Energieübersicht Schweiz 2023` | str | 32 (74.42%) | 11 | `Anleitung`, `Ausgewählt | Selected:`, `Betrachtungszeitraum | Observation Period`, `Bis | To:`, `Das hier vorliegende Excel-Sheet beinhaltet die Gesamtübersicht der wichtigsten Eckdaten der Regelzone Schweiz.

Die Daten sind aggregierte Viertelstunden- oder Stundenwerte, welche zu ihrer Referenz im Blatt «Zeitreihen» abgelegt sind. Die Daten sind dieselben, wie auch von Swissgrid zu Abrechnungszwecken verwendet werden.

Nebst den Zeitreihen finden Sie auf dem Blatt «Übersicht» die Summen der jeweiligen Energiegrösse welche für den eingestellten Zeitraum direkt berechnet werden. Der Betrachtungszeitraum kann auf dieser Seite eingestellt werden.

Achtung: Bei MS-Excel 2003 und älter werden einige Felder nicht automatisch berechnet. Drücken Sie daher STRG+ALT+F9 nachdem Sie die Datei geöffnet haben.`, … (+6) |
| `Unnamed: 1` | str | 42 (97.67%) | 1 | `16.07.2024 08:51:56` |
| `Unnamed: 2` | object | 39 (90.7%) | 3 | `1`, `DD`, `MW / MWh` |
| `Unnamed: 3` | object | 40 (93.02%) | 2 | `1`, `MM` |
| `Unnamed: 4` | object | 40 (93.02%) | 3 | `2023`, `2024`, `YYYY` |
| `Unnamed: 5` | object | 40 (93.02%) | 2 | `0`, `hh` |
| `Unnamed: 6` | object | 40 (93.02%) | 2 | `0`, `min` |
| `Unnamed: 7` | datetime64[us] | 41 (95.35%) | 2 | 2023-01-01 00:00:00 … 2024-01-01 00:00:00 |
| `Unnamed: 8` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 9` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 10` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 11` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 12` | float64 | 43 (100.0%) | 0 |  |
| `Unnamed: 13` | float64 | 43 (100.0%) | 0 |  |
| `1` | float64 | 13 (30.23%) | 30 | 2.0 … 31.0 (mean 16.50) |
| `1.1` | float64 | 32 (74.42%) | 11 | 2.0 … 12.0 (mean 7.00) |
| `2023` | float64 | 42 (97.67%) | 1 | 2024.0 … 2024.0 (mean 2024.00) |
| `0` | float64 | 20 (46.51%) | 23 | 1.0 … 23.0 (mean 12.00) |
| `0.1` | float64 | 40 (93.02%) | 3 | 15.0 … 45.0 (mean 30.00) |
| `kW / kWh` | str | 42 (97.67%) | 1 | `MW / MWh` |
| `Frühstes Datum` | str | 39 (90.7%) | 4 | `Faktor:`, `Prefix:`, `Spätestes Datum`, `anzMonate` |
| `2023-01-01 00:00:00` | object | 39 (90.7%) | 4 | `1`, `12`, `2024-01-01 00:00:00`, `M` |

## Sheet: `Datetime`

**Zeilen:** 35,137
**Spalten:** 1

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Unnamed: 0` | object | 96 (0.27%) | 35037 | `Zeitstempel 0h15`, `2023-01-01 00:15:00`, `2023-01-01 00:30:00` |

## Sheet: `Uebersicht`

**Zeilen:** 106
**Spalten:** 15

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Energieübersicht Schweiz 2023` | str | 93 (87.74%) | 13 | `Import/Export/Transit`, `Negative Sekundärregelenergie
Negative secondary control energy`, `Negative Tertiärregelenergie
Negative tertiary control energy`, `Netto Ausspeisung aus dem Übertragungsnetz Schweiz
Net outflow of the Swiss transmission grid`, `Periode:`, … (+8) |
| `Unnamed: 1` | str | 75 (70.75%) | 15 | `AT→CH`, `CH→AT`, `CH→DE`, `CH→FR`, `CH→IT`, … (+10) |
| `Unnamed: 2` | float64 | 97 (91.51%) | 9 | -522037.717 … 67960463.14481279 (mean 26269825.08) |
| `Unnamed: 3` | object | 74 (69.81%) | 12 | `-1302`, `-440.34`, `10118.174397628`, `12012.094258387999`, `15304.109337912001`, … (+7) |
| `Unnamed: 4` | float64 | 84 (79.25%) | 22 | 1631.78 … 32887785.936 (mean 6429678.45) |
| `Unnamed: 5` | float64 | 106 (100.0%) | 0 |  |
| `Unnamed: 6` | float64 | 106 (100.0%) | 0 |  |
| `Unnamed: 7` | str | 105 (99.06%) | 1 | `-` |
| `Unnamed: 8` | datetime64[us] | 105 (99.06%) | 1 | 2024-01-01 00:00:00 … 2024-01-01 00:00:00 |
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
| `Unnamed: 0` | str | 0 (0.0%) | 35037 | `Zeitstempel`, `01.01.2023 00:15`, `01.01.2023 00:30` |
| `Summe endverbrauchte Energie Regelblock Schweiz | Total energy consumed by end users in the Swiss controlblock` | object | 0 (0.0%) | 35041 | `kWh`, `1345452.398625`, `1335870.443625` |
| `Summe produzierte Energie Regelblock Schweiz | Total energy production Swiss controlblock` | object | 0 (0.0%) | 35041 | `kWh`, `1329172.12`, `1324571.606` |
| `Summe verbrauchte Energie Regelblock Schweiz | Total energy consumption Swiss controlblock` | object | 0 (0.0%) | 35041 | `kWh`, `1684850.74847`, `1647138.11337` |
| `Netto Ausspeisung aus dem Übertragungsnetz Schweiz | Net outflow of the Swiss transmission grid` | object | 0 (0.0%) | 15721 | `kWh`, `319871.726023`, `288360.519079` |
| `Vertikale Einspeisung ins Übertragungsnetz Schweiz | Grid feed-in Swiss transmission grid` | object | 0 (0.0%) | 35039 | `kWh`, `848336.942`, `851109.677` |
| `Positive Sekundär-Regelenergie | Positive secundary control energy` | object | 0 (0.0%) | 11511 | `kWh`, `0`, `0` |
| `Negative Sekundär-Regelenergie | Negative secundary control energy` | object | 0 (0.0%) | 11929 | `kWh`, `0`, `0` |
| `Positive Tertiär-Regelenergie | Positive tertiary control energy` | object | 0 (0.0%) | 1114 | `kWh`, `0`, `0` |
| `Negative Tertiär-Regelenergie | Negative tertiary control energy` | object | 0 (0.0%) | 756 | `kWh`, `0`, `0` |
| `Verbundaustausch CH->AT | Cross Border Exchange CH->AT` | object | 0 (0.0%) | 7955 | `kWh`, `46400`, `46800` |
| `Verbundaustausch AT->CH | Cross Border Exchange AT->CH` | object | 0 (0.0%) | 26629 | `kWh`, `185349`, `184848` |
| `Verbundaustausch CH->DE | Cross Border Exchange CH->DE` | object | 0 (0.0%) | 25275 | `kWh`, `5226`, `4400` |
| `Verbundaustausch DE->CH | Cross Border Exchange DE->CH` | object | 0 (0.0%) | 27274 | `kWh`, `550500`, `548090` |
| `Verbundaustausch CH->FR | Cross Border Exchange CH->FR` | object | 0 (0.0%) | 22687 | `kWh`, `82934`, `86906` |
| `Verbundaustausch FR->CH | Cross Border Exchange FR->CH` | object | 0 (0.0%) | 34050 | `kWh`, `181112`, `182777` |
| `Verbundaustausch CH->IT | Cross Border Exchange CH->IT` | object | 0 (0.0%) | 34326 | `kWh`, `427158`, `454412` |
| `Verbundaustausch IT->CH | Cross Border Exchange IT->CH` | object | 0 (0.0%) | 21312 | `kWh`, `868`, `95` |
| `Transit` | object | 0 (0.0%) | 34457 | `kWh`, `561718`, `592518` |
| `Import` | object | 0 (0.0%) | 34616 | `kWh`, `917829`, `915810` |
| `Export` | object | 0 (0.0%) | 34451 | `kWh`, `561718`, `592518` |
| `Durchschnittliche positive Sekundär-Regelenergie Preise | Average positive secondary control energy prices` | object | 0 (0.0%) | 15014 | `Euro/MWh`, `0`, `0` |
| `Durchschnittliche negative Sekundär-Regelenergie Preise | Average negative secondary control energy prices` | object | 0 (0.0%) | 13542 | `Euro/MWh`, `0`, `0` |
| `Durchschnittliche positive Tertiär-Regelenergie Preise | Average positive tertiary control energy prices` | object | 0 (0.0%) | 6693 | `Euro/MWh`, `0`, `0` |
| `Durchschnittliche negative Tertiär-Regelenergie Preise | Average negative tertiary control energy prices` | object | 0 (0.0%) | 7223 | `Euro/MWh`, `0`, `0` |
| `Produktion Kanton AG | Production Canton AG` | object | 0 (0.0%) | 35024 | `kWh`, `510107.593`, `510351.284` |
| `Verbrauch Kanton AG | Consumption Canton AG` | object | 0 (0.0%) | 35037 | `kWh`, `111939.242`, `111169.353` |
| `Produktion Kanton FR | Production Canton FR` | object | 0 (0.0%) | 35033 | `kWh`, `22474.309`, `22342.534` |
| `Verbrauch Kanton FR | Consumption Canton FR` | object | 0 (0.0%) | 35025 | `kWh`, `63813.127`, `64633.342` |
| `Produktion Kanton GL | Production Canton GL` | object | 0 (0.0%) | 35031 | `kWh`, `11531.172`, `10941.294` |
| `Verbrauch Kanton GL | Consumption Canton GL` | object | 0 (0.0%) | 35021 | `kWh`, `160056.588`, `158094.916` |
| `Produktion Kanton GR | Production Canton GR` | object | 0 (0.0%) | 35039 | `kWh`, `35791.099`, `36412.461` |
| `Verbrauch Kanton GR | Consumption Canton GR` | object | 0 (0.0%) | 35025 | `kWh`, `80620.351`, `80091.728` |
| `Produktion Kanton LU | Production Canton LU` | object | 0 (0.0%) | 35008 | `kWh`, `9216.695`, `8735.783` |
| `Verbrauch Kanton LU | Consumption Canton LU` | object | 0 (0.0%) | 35032 | `kWh`, `98876.823`, `97725.744` |
| `Produktion Kanton NE | Production Canton NE` | object | 0 (0.0%) | 34473 | `kWh`, `1006.376`, `1024.931` |
| `Verbrauch Kanton NE | Consumption Canton NE` | object | 0 (0.0%) | 34999 | `kWh`, `12035.581`, `11879.856` |
| `Produktion Kanton SO | Production Canton SO` | object | 0 (0.0%) | 35020 | `kWh`, `269960.541`, `269657.531` |
| `Verbrauch Kanton SO | Consumption Canton SO` | object | 0 (0.0%) | 35007 | `kWh`, `32712.755`, `32696.716` |
| `Produktion Kanton SG | Production Canton SG` | object | 0 (0.0%) | 35041 | `kWh`, `15327.139`, `15100.8026` |
| `Verbrauch Kanton SG | Consumption Canton SG` | object | 0 (0.0%) | 35041 | `kWh`, `78711.8418`, `78169.818` |
| `Produktion Kanton TI | Production Canton TI` | object | 0 (0.0%) | 35038 | `kWh`, `24056.536`, `22325.225` |
| `Verbrauch Kanton TI | Consumption Canton TI` | object | 0 (0.0%) | 35029 | `kWh`, `78521.537`, `77457.532` |
| `Produktion Kanton TG | Production Canton TG` | object | 0 (0.0%) | 34957 | `kWh`, `5808.62`, `5801.472` |
| `Verbrauch Kanton TG | Consumption Canton TG` | object | 0 (0.0%) | 35024 | `kWh`, `37699.423`, `37647.023` |
| `Produktion Kanton VS | Production Canton VS` | object | 0 (0.0%) | 35041 | `kWh`, `60579.015`, `62753.55` |
| `Verbrauch Kanton VS | Consumption Canton VS` | object | 0 (0.0%) | 35035 | `kWh`, `115280.833493`, `96684.650449` |
| `Produktion Kantone AI, AR | Production Cantons AI, AR` | object | 0 (0.0%) | 35010 | `kWh`, `1924.755`, `1779.5724` |
| `Verbrauch Kantone AI, AR | Consumption Cantons AI, AR` | object | 0 (0.0%) | 35032 | `kWh`, `11616.6842`, `11332.387` |
| `Produktion Kantone BL, BS | Production Cantons BL, BS` | object | 0 (0.0%) | 35015 | `kWh`, `25635.622`, `25759.466` |
| `Verbrauch Kantone BL, BS | Consumption Cantons BL, BS` | object | 0 (0.0%) | 35032 | `kWh`, `73433.829`, `73031.782` |
| `Produktion Kantone BE, JU | Production Cantons BE, JU` | object | 0 (0.0%) | 35038 | `kWh`, `87451.238`, `82921.503` |
| `Verbrauch Kantone BE, JU | Consumption Cantons BE, JU` | object | 0 (0.0%) | 35037 | `kWh`, `213980.347`, `209031.571` |
| `Produktion Kantone SZ, ZG | Production Cantons SZ, ZG` | object | 0 (0.0%) | 35017 | `kWh`, `6400.187`, `6350.652` |
| `Verbrauch Kantone SZ, ZG | Consumption Cantons SZ, ZG` | object | 0 (0.0%) | 35025 | `kWh`, `47236.653`, `46534.026` |
| `Produktion Kantone OW, NW, UR | Production Cantons OW, NW, UR` | object | 0 (0.0%) | 35028 | `kWh`, `19674.098`, `19554.939` |
| `Verbrauch Kantone OW, NW, UR | Consumption Cantons OW, NW, UR` | object | 0 (0.0%) | 35011 | `kWh`, `24341.649`, `24148.492` |
| `Produktion Kantone GE, VD | Production Cantons GE, VD` | object | 0 (0.0%) | 35036 | `kWh`, `79970.283`, `79603.255` |
| `Verbrauch Kantone GE, VD | Consumption Cantons GE, VD` | object | 0 (0.0%) | 35035 | `kWh`, `157039.967`, `154354.019` |
| `Produktion Kantone SH, ZH | Production Cantons SH, ZH` | object | 0 (0.0%) | 34994 | `kWh`, `19611.722`, `20106.026` |
| `Verbrauch Kantone SH, ZH | Consumption Cantons SH, ZH` | object | 0 (0.0%) | 35036 | `kWh`, `234192.903`, `232235.465` |
| `Produktion Kantonsübergreifend | Production across Cantons` | object | 0 (0.0%) | 35033 | `kWh`, `121351.543`, `122135.872` |
| `Verbrauch Kantonsübergreifend | Consumption across Cantons` | object | 0 (0.0%) | 35041 | `kWh`, `41844.191977`, `39470.272921` |
| `Produktion Regelzone CH - Ausländische Gebiete | Production control area CH - foreign territories` | object | 0 (0.0%) | 34938 | `kWh`, `1293.577`, `913.453` |
| `Verbrauch Regelzone CH - Ausländische Gebiete | Consumption control area CH - foreign territories` | object | 0 (0.0%) | 35004 | `kWh`, `10896.422`, `10749.42` |
