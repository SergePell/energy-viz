# Profil: energieuebersicht_ch_2019.xls

**Erstellt:** 2026-05-05T21:17:47
**Pfad:** `C:\Users\pelle\SynologyDrive\Docs\Studium\FHGR\Masterthesis\energy-viz\pipeline\raw\snapshots\2026-05-05\swissgrid\energieuebersicht_ch_2019.xls`
**Format:** XLS

**Sheets:** Einstellungen, Uebersicht, Zeitreihen0h15, Zeitreihen1h00

## Sheet: `Einstellungen`

**Zeilen:** 35
**Spalten:** 22

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `nan` | str | 25 (71.43%) | 10 | `Anleitung`, `Ausgewählt / Selected:`, `Betrachtungszeitraum / Observation Period`, `Bis / To:`, `Das hier vorliegende Excel-Sheet beinhaltet die Gesamtübersicht der wichtigsten Eckdaten der Regelzone Schweiz.
Die Daten sind aggregierte Viertelstunden- oder Stundenwerte, welche zu ihrer Referenz im Blatt "Zeitreihen" abgelegt sind. Die Daten sind dieselben, wie auch von Swissgrid zu Abrechnungszwecken verwendet werden.
Nebst den Zeitreihen finden Sie auf dem Blatt "Übersicht" die Summen der jeweiligen Energiegrösse welche für den eingestellten Zeitraum direkt berechnet werden. Der Betrachtungszeitraum kann auf dieser Seite eingestellt werden.
Achtung: Bei MS-Excel 2003 und älter werden einige Felder nicht automatisch berechnet. Drücken Sie daher STRG+ALT+F9 nachdem Sie die Datei geöffnet haben.`, … (+5) |
| `Unnamed: 1` | datetime64[us] | 34 (97.14%) | 1 | 2021-02-24 10:22:05.888000 … 2021-02-24 10:22:05.888000 |
| `Unnamed: 2` | object | 32 (91.43%) | 3 | `0`, `DD`, `MW/MWh` |
| `Unnamed: 3` | object | 33 (94.29%) | 2 | `1`, `MM` |
| `Unnamed: 4` | object | 33 (94.29%) | 2 | `1900`, `YYYY` |
| `Unnamed: 5` | object | 33 (94.29%) | 2 | `0`, `hh` |
| `Unnamed: 6` | object | 33 (94.29%) | 2 | `0`, `min` |
| `Unnamed: 7` | float64 | 35 (100.0%) | 0 |  |
| `Unnamed: 8` | float64 | 35 (100.0%) | 0 |  |
| `Unnamed: 9` | float64 | 35 (100.0%) | 0 |  |
| `Unnamed: 10` | float64 | 35 (100.0%) | 0 |  |
| `Unnamed: 11` | float64 | 35 (100.0%) | 0 |  |
| `Unnamed: 12` | float64 | 35 (100.0%) | 0 |  |
| `Unnamed: 13` | float64 | 35 (100.0%) | 0 |  |
| `1` | float64 | 5 (14.29%) | 30 | 2.0 … 31.0 (mean 16.50) |
| `nan.1` | float64 | 35 (100.0%) | 0 |  |
| `nan.2` | float64 | 35 (100.0%) | 0 |  |
| `0` | float64 | 12 (34.29%) | 23 | 1.0 … 23.0 (mean 12.00) |
| `0.1` | float64 | 32 (91.43%) | 3 | 15.0 … 45.0 (mean 30.00) |
| `kW/kWh` | str | 34 (97.14%) | 1 | `MW/MWh` |
| `Frühstes Datum` | str | 31 (88.57%) | 4 | `Faktor:`, `Prefix:`, `Spätestes Datum`, `anzMonate` |
| `1899-12-30 23:00:00` | object | 31 (88.57%) | 3 | `00:00:00`, `1`, `M` |

## Sheet: `Uebersicht`

**Zeilen:** 112
**Spalten:** 15

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `nan` | str | 98 (87.5%) | 14 | `Import/Export/Transit`, `Negative Sekundärregelenergie
Negative secondary control energy`, `Negative Tertiärregelenergie
Negative tertiary control energy`, `Netto Ausspeisung aus dem Übertragungsnetz Schweiz
Net outflow of the Swiss transmission grid`, `Periode:`, … (+9) |
| `Unnamed: 1` | str | 79 (70.54%) | 15 | `AT→CH`, `CH→AT`, `CH→DE`, `CH→FR`, `CH→IT`, … (+10) |
| `Unnamed: 2` | float64 | 102 (91.07%) | 1 | 0.0 … 0.0 (mean 0.00) |
| `Unnamed: 3` | str | 90 (80.36%) | 2 | `E`, `Pmax` |
| `Unnamed: 4` | float64 | 101 (90.18%) | 1 | 0.0 … 0.0 (mean 0.00) |
| `Unnamed: 5` | float64 | 112 (100.0%) | 0 |  |
| `Unnamed: 6` | float64 | 112 (100.0%) | 0 |  |
| `Unnamed: 7` | str | 111 (99.11%) | 1 | `-` |
| `Unnamed: 8` | float64 | 112 (100.0%) | 0 |  |
| `Unnamed: 9` | float64 | 112 (100.0%) | 0 |  |
| `Unnamed: 10` | str | 70 (62.5%) | 2 | `MW`, `MWh` |
| `Unnamed: 11` | float64 | 112 (100.0%) | 0 |  |
| `Unnamed: 12` | float64 | 112 (100.0%) | 0 |  |
| `Unnamed: 13` | str | 99 (88.39%) | 12 | `Beschreibung:
Die Netto Ausspeisung aus dem Übertragungsnetz ist die Energiemenge, welche effektiv aus dem Übertragungsnetz über direkt angeschlossene Transformatoren zu nachgelagerten Verteilnetzen, Endverbrauchern und Kraftwerken transportiert wurde. Die Netto Ausspeisung ist der positive Anteil der Bilanzierung aller vertikalen Übergabepunkte im Übertragunsgnetz zu Verteilnetzbetreibern, Endverbrauchern und Kraftwerken. Sie wird in Viertelstundenauflösung und in kWh aufbereitet.
`, `Beschreibung:
Die Summe der abgegebenen Energiemengen in MWh pro Viertelstunde genettet, welche die Erzeugungseinheiten auf Basis eines SDL-Vertrages und durch Abruf von Swissgrid beziehen.`, `Beschreibung:
Die Summe der abgegebenen Energiemengen in MWh pro Viertelstunde, welche die Erzeugungseinheiten auf Basis eines SDL-Vertrages und durch Tertiärabruf von Swissgrid beziehen`, `Beschreibung:
Die Summe der bezogenen Energiemengen in MWh pro Viertelstunde genettet, welche die Erzeugungseinheiten auf Basis eines SDL-Vertrages und durch Abruf an Swissgrid liefern.`, `Beschreibung:
Die Summe der bezogenen Energiemengen in MWh pro Viertelstunde, welche die Erzeugungseinheiten auf Basis eines SDL-Vertrages und durch Tertiärabruf an Swissgrid liefern.`, … (+7) |
| `Unnamed: 14` | str | 101 (90.18%) | 11 | `Description
"The amount of power flows out of the transmission network into distribution and large customer networks"* The vertical load has a 1 hour resolution and the power is in MW. Horizontal exchanges with other European TSO are not considered. The load is metered at the exchange points.

*Glossary of terms from entsoe`, `Description
Average prices of control energy per 15 minutes rounded to two decimal places for secondary and tertiary control energy products.`, `Description
The net outflow of the Swiss transmission grid is the amount of energy, which effectively flows over transformers out of the transmission grid into the distribution grids, towards end- users and power plants. The net outflow is the positive part of the netting of the vertical in feeds and outflows of the transmission grid. The resolution is 15 minutes and the energy is shown as kWh`, `Description
The total of the consumed energy in the control block Switzerland. The aggregations of the consumption sequences for the balancing group are sent from the distribution network operators to Swissgrid. The sum contains all the energy consumed in the transmission and distribution grids. Included are grid losses, energy consumed for a power plant’s own requirements and to drive the pumps in pumped storage hydro power plant.`, `Description
The total of the end- user energy consumption includes all aggregates with the end-user consumptions for the Swiss Control block delivered by the distribution network operators to Swissgrid. Not included are grid losses or energy consumed for  power plant’s own requirements or to drive the pumps in pumped storage hydro power plant. 
`, … (+6) |

## Sheet: `Zeitreihen0h15`

**Zeilen:** 35,041
**Spalten:** 65

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Unnamed: 0` | object | 0 (0.0%) | 35037 | `Zeitstempel`, `2019-01-01 00:15:00`, `2019-01-01 00:30:00` |
| `Summe endverbrauchte Energie Regelblock Schweiz | Total energy consumed by end users in the Swiss controlblock` | object | 0 (0.0%) | 35040 | `kWh`, `1540639.983`, `1527919.449` |
| `Summe produzierte Energie Regelblock Schweiz | Total energy production Swiss controlblock` | object | 0 (0.0%) | 35041 | `kWh`, `1348915.471313`, `1334778.597189` |
| `Summe verbrauchte Energie Regelblock Schweiz | Total energy consumption Swiss controlblock` | object | 0 (0.0%) | 35041 | `kWh`, `1805275.110583`, `1774762.221959` |
| `Netto Ausspeisung aus dem Übertragungsnetz Schweiz | Net outflow of the Swiss transmission grid` | object | 0 (0.0%) | 15586 | `kWh`, `410240.653877`, `401305.931042` |
| `Vertikale Einspeisung ins Übertragungsnetz Schweiz | Grid feed-in Swiss transmission grid` | object | 0 (0.0%) | 35041 | `kWh`, `900748.397313`, `895294.538189` |
| `Positive Sekundär-Regelenergie | Positive secundary control energy` | object | 0 (0.0%) | 11724 | `kWh`, `4164`, `350` |
| `Negative Sekundär-Regelenergie | Negative secundary control energy` | object | 0 (0.0%) | 11224 | `kWh`, `-5300`, `-773` |
| `Positive Tertiär-Regelenergie | Positive tertiary control energy` | object | 0 (0.0%) | 185 | `kWh`, `0`, `0` |
| `Negative Tertiär-Regelenergie | Negative tertiary control energy` | object | 0 (0.0%) | 145 | `kWh`, `0`, `0` |
| `Verbundaustausch CH->AT | Cross Border Exchange CH->AT` | object | 0 (0.0%) | 5155 | `kWh`, `600`, `10400` |
| `Verbundaustausch AT->CH | Cross Border Exchange AT->CH` | object | 0 (0.0%) | 14552 | `kWh`, `246700`, `194100` |
| `Verbundaustausch CH->DE | Cross Border Exchange CH->DE` | object | 0 (0.0%) | 24345 | `kWh`, `41059`, `33072` |
| `Verbundaustausch DE->CH | Cross Border Exchange DE->CH` | object | 0 (0.0%) | 32271 | `kWh`, `871268`, `774948` |
| `Verbundaustausch CH->FR | Cross Border Exchange CH->FR` | object | 0 (0.0%) | 24025 | `kWh`, `225431.5`, `215231.5` |
| `Verbundaustausch FR->CH | Cross Border Exchange FR->CH` | object | 0 (0.0%) | 28914 | `kWh`, `100550`, `100550` |
| `Verbundaustausch CH->IT | Cross Border Exchange CH->IT` | object | 0 (0.0%) | 34139 | `kWh`, `539342`, `434424` |
| `Verbundaustausch IT->CH | Cross Border Exchange IT->CH` | object | 0 (0.0%) | 20056 | `kWh`, `62378`, `76075` |
| `Transit` | object | 0 (0.0%) | 34895 | `kWh`, `804486.5`, `694165.5` |
| `Import` | object | 0 (0.0%) | 34935 | `kWh`, `1279259.75`, `1144678.75` |
| `Export` | object | 0 (0.0%) | 34892 | `kWh`, `804486.5`, `694165.5` |
| `Durchschnittliche positive Sekundär-Regelenergie Preise | Average positive secondary control energy prices` | object | 0 (0.0%) | 3164 | `Euro/MWh`, `60.31`, `60.31` |
| `Durchschnittliche negative Sekundär-Regelenergie Preise | Average negative secondary control energy prices` | object | 0 (0.0%) | 3087 | `Euro/MWh`, `40.21`, `40.21` |
| `Durchschnittliche positive Tertiär-Regelenergie Preise | Average positive tertiary control energy prices` | object | 0 (0.0%) | 815 | `Euro/MWh`, `0`, `0` |
| `Durchschnittliche negative Tertiär-Regelenergie Preise | Average negative tertiary control energy prices` | object | 0 (0.0%) | 672 | `Euro/MWh`, `0`, `0` |
| `Produktion Kanton AG | Production Canton AG` | object | 0 (0.0%) | 35030 | `kWh`, `483231.569`, `483394.176` |
| `Verbrauch Kanton AG | Consumption Canton AG` | object | 0 (0.0%) | 35030 | `kWh`, `126134.893`, `124564.392` |
| `Produktion Kanton FR | Production Canton FR` | object | 0 (0.0%) | 35030 | `kWh`, `10249.69`, `10201.835` |
| `Verbrauch Kanton FR | Consumption Canton FR` | object | 0 (0.0%) | 35027 | `kWh`, `69918.522`, `68029.867` |
| `Produktion Kanton GL | Production Canton GL` | object | 0 (0.0%) | 35022 | `kWh`, `30588.952`, `27623.973` |
| `Verbrauch Kanton GL | Consumption Canton GL` | object | 0 (0.0%) | 35005 | `kWh`, `56813.165`, `56484.246` |
| `Produktion Kanton GR | Production Canton GR` | object | 0 (0.0%) | 35040 | `kWh`, `69767.551`, `64961.944` |
| `Verbrauch Kanton GR | Consumption Canton GR` | object | 0 (0.0%) | 35030 | `kWh`, `75362.77`, `75337.136` |
| `Produktion Kanton LU | Production Canton LU` | object | 0 (0.0%) | 35015 | `kWh`, `8242.75`, `7457.739` |
| `Verbrauch Kanton LU | Consumption Canton LU` | object | 0 (0.0%) | 35027 | `kWh`, `91239.974`, `90450.59` |
| `Produktion Kanton NE | Production Canton NE` | object | 0 (0.0%) | 28972 | `kWh`, `781.46`, `803.81` |
| `Verbrauch Kanton NE | Consumption Canton NE` | object | 0 (0.0%) | 34898 | `kWh`, `14835.09`, `14415.19` |
| `Produktion Kanton SO | Production Canton SO` | object | 0 (0.0%) | 35015 | `kWh`, `268887.388`, `269445.598` |
| `Verbrauch Kanton SO | Consumption Canton SO` | object | 0 (0.0%) | 35023 | `kWh`, `51336.32`, `50124.857` |
| `Produktion Kanton SG | Production Canton SG` | object | 0 (0.0%) | 35037 | `kWh`, `10791.7948`, `10639.4328` |
| `Verbrauch Kanton SG | Consumption Canton SG` | object | 0 (0.0%) | 35041 | `kWh`, `95981.6026`, `81980.1698` |
| `Produktion Kanton TI | Production Canton TI` | object | 0 (0.0%) | 35035 | `kWh`, `25708.699`, `24518.384` |
| `Verbrauch Kanton TI | Consumption Canton TI` | object | 0 (0.0%) | 35033 | `kWh`, `79706.8`, `78847.839` |
| `Produktion Kanton TG | Production Canton TG` | object | 0 (0.0%) | 34923 | `kWh`, `3339.399`, `3288.846` |
| `Verbrauch Kanton TG | Consumption Canton TG` | object | 0 (0.0%) | 35021 | `kWh`, `46304.754`, `46140.535` |
| `Produktion Kanton VS | Production Canton VS` | object | 0 (0.0%) | 35041 | `kWh`, `106368.854313`, `109826.590189` |
| `Verbrauch Kanton VS | Consumption Canton VS` | object | 0 (0.0%) | 35041 | `kWh`, `104900.35146`, `103836.825001` |
| `Produktion Kantone AI, AR | Production Cantons AI, AR` | object | 0 (0.0%) | 35013 | `kWh`, `1853.9352`, `1857.2432` |
| `Verbrauch Kantone AI, AR | Consumption Cantons AI, AR` | object | 0 (0.0%) | 35030 | `kWh`, `15613.4734`, `15278.2622` |
| `Produktion Kantone BL, BS | Production Cantons BL, BS` | object | 0 (0.0%) | 35006 | `kWh`, `26170.083`, `25616.99` |
| `Verbrauch Kantone BL, BS | Consumption Cantons BL, BS` | object | 0 (0.0%) | 35032 | `kWh`, `88054.869`, `87377.787` |
| `Produktion Kantone BE, JU | Production Cantons BE, JU` | object | 0 (0.0%) | 35038 | `kWh`, `141293.685`, `140411.546` |
| `Verbrauch Kantone BE, JU | Consumption Cantons BE, JU` | object | 0 (0.0%) | 35038 | `kWh`, `226741.503`, `227358.992` |
| `Produktion Kantone SZ, ZG | Production Cantons SZ, ZG` | object | 0 (0.0%) | 34997 | `kWh`, `2748.317`, `2720.468` |
| `Verbrauch Kantone SZ, ZG | Consumption Cantons SZ, ZG` | object | 0 (0.0%) | 35030 | `kWh`, `50004.859`, `48788.535` |
| `Produktion Kantone OW, NW, UR | Production Cantons OW, NW, UR` | object | 0 (0.0%) | 35031 | `kWh`, `12255.289`, `10934.633` |
| `Verbrauch Kantone OW, NW, UR | Consumption Cantons OW, NW, UR` | object | 0 (0.0%) | 35007 | `kWh`, `29345.122`, `28984.733` |
| `Produktion Kantone GE, VD | Production Cantons GE, VD` | object | 0 (0.0%) | 35035 | `kWh`, `39807.981`, `37456.38` |
| `Verbrauch Kantone GE, VD | Consumption Cantons GE, VD` | object | 0 (0.0%) | 35037 | `kWh`, `254135.731`, `253943.085` |
| `Produktion Kantone SH, ZH | Production Cantons SH, ZH` | object | 0 (0.0%) | 34987 | `kWh`, `22384.238`, `21566.876` |
| `Verbrauch Kantone SH, ZH | Consumption Cantons SH, ZH` | object | 0 (0.0%) | 35040 | `kWh`, `258097.952`, `256777.717` |
| `Produktion Kantonsübergreifend | Production across Cantons` | object | 0 (0.0%) | 35037 | `kWh`, `80786.005`, `78857.38` |
| `Verbrauch Kantonsübergreifend | Consumption across Cantons` | object | 0 (0.0%) | 35041 | `kWh`, `58314.235123`, `53410.971958` |
| `Produktion Regelzone CH - Ausländische Gebiete | Production control area CH - foreign territories` | object | 0 (0.0%) | 23718 | `kWh`, `279.675`, `275.225` |
| `Verbrauch Regelzone CH - Ausländische Gebiete | Consumption control area CH - foreign territories` | object | 0 (0.0%) | 34966 | `kWh`, `4216.443`, `4224.925` |

## Sheet: `Zeitreihen1h00`

**Zeilen:** 8,761
**Spalten:** 2

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Unnamed: 0` | object | 0 (0.0%) | 8760 | `Zeitstempel`, `2019-01-01 01:00:00`, `2019-01-01 02:00:00` |
| `Vertikale Netzlast Übertragungsnetz Schweiz | Vertical load Swiss transmission grid` | object | 0 (0.0%) | 8761 | `MW`, `5569.868233`, `5730.919475` |
