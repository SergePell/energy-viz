# Profil: energieuebersicht_ch_2015.xls

**Erstellt:** 2026-05-05T21:17:06
**Pfad:** `C:\Users\pelle\SynologyDrive\Docs\Studium\FHGR\Masterthesis\energy-viz\pipeline\raw\snapshots\2026-05-05\swissgrid\energieuebersicht_ch_2015.xls`
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
| `Unnamed: 1` | datetime64[us] | 34 (97.14%) | 1 | 2016-04-06 10:40:15.888000 … 2016-04-06 10:40:15.888000 |
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
| `Unnamed: 0` | object | 0 (0.0%) | 35037 | `Zeitstempel`, `2015-01-01 00:15:00`, `2015-01-01 00:30:00` |
| `Summe endverbrauchte Energie Regelblock Schweiz | Total energy consumed by end users in the Swiss controlblock` | object | 0 (0.0%) | 35041 | `kWh`, `1790683.264`, `1777125.512` |
| `Summe produzierte Energie Regelblock Schweiz | Total energy production Swiss controlblock` | object | 0 (0.0%) | 35041 | `kWh`, `1697771.888`, `1686388.388` |
| `Summe verbrauchte Energie Regelblock Schweiz | Total energy consumption Swiss controlblock` | object | 0 (0.0%) | 35041 | `kWh`, `1922526.092`, `1907137.941` |
| `Netto Ausspeisung aus dem Übertragungsnetz Schweiz | Net outflow of the Swiss transmission grid` | object | 0 (0.0%) | 17747 | `kWh`, `177077.893`, `172626.54` |
| `Vertikale Einspeisung ins Übertragungsnetz Schweiz | Grid feed-in Swiss transmission grid` | object | 0 (0.0%) | 35040 | `kWh`, `1362135.367`, `1353115.668` |
| `Positive Sekundär-Regelenergie | Positive secundary control energy` | object | 0 (0.0%) | 671 | `kWh`, `37500`, `22200` |
| `Negative Sekundär-Regelenergie | Negative secundary control energy` | object | 0 (0.0%) | 639 | `kWh`, `0`, `0` |
| `Positive Tertiär-Regelenergie | Positive tertiary control energy` | object | 0 (0.0%) | 111 | `kWh`, `0`, `0` |
| `Negative Tertiär-Regelenergie | Negative tertiary control energy` | object | 0 (0.0%) | 182 | `kWh`, `0`, `0` |
| `Verbundaustausch CH->AT | Cross Border Exchange CH->AT` | object | 0 (0.0%) | 1150 | `kWh`, `0`, `0` |
| `Verbundaustausch AT->CH | Cross Border Exchange AT->CH` | object | 0 (0.0%) | 4259 | `kWh`, `153000`, `167100` |
| `Verbundaustausch CH->DE | Cross Border Exchange CH->DE` | object | 0 (0.0%) | 12776 | `kWh`, `0`, `5400` |
| `Verbundaustausch DE->CH | Cross Border Exchange DE->CH` | object | 0 (0.0%) | 33594 | `kWh`, `423359`, `414862` |
| `Verbundaustausch CH->FR | Cross Border Exchange CH->FR` | object | 0 (0.0%) | 17207 | `kWh`, `154295.25`, `152295.25` |
| `Verbundaustausch FR->CH | Cross Border Exchange FR->CH` | object | 0 (0.0%) | 27907 | `kWh`, `260396.75`, `261396.75` |
| `Verbundaustausch CH->IT | Cross Border Exchange CH->IT` | object | 0 (0.0%) | 34369 | `kWh`, `485671`, `497316` |
| `Verbundaustausch IT->CH | Cross Border Exchange IT->CH` | object | 0 (0.0%) | 19822 | `kWh`, `18748`, `15145` |
| `Transit` | object | 0 (0.0%) | 34869 | `kWh`, `639966.25`, `655011.25` |
| `Import` | object | 0 (0.0%) | 34903 | `kWh`, `855503.75`, `858503.75` |
| `Export` | object | 0 (0.0%) | 34810 | `kWh`, `639966.25`, `655011.25` |
| `Durchschnittliche positive Sekundär-Regelenergie Preise | Average positive secondary control energy prices` | object | 0 (0.0%) | 3088 | `Euro/MWh`, `53.93`, `53.93` |
| `Durchschnittliche negative Sekundär-Regelenergie Preise | Average negative secondary control energy prices` | object | 0 (0.0%) | 3123 | `Euro/MWh`, `35.95`, `35.95` |
| `Durchschnittliche positive Tertiär-Regelenergie Preise | Average positive tertiary control energy prices` | object | 0 (0.0%) | 513 | `Euro/MWh`, `0`, `0` |
| `Durchschnittliche negative Tertiär-Regelenergie Preise | Average negative tertiary control energy prices` | object | 0 (0.0%) | 614 | `Euro/MWh`, `0`, `0` |
| `Produktion Kanton AG | Production Canton AG` | object | 0 (0.0%) | 35033 | `kWh`, `511741.53`, `509815.302` |
| `Verbrauch Kanton AG | Consumption Canton AG` | object | 0 (0.0%) | 35036 | `kWh`, `151007.989`, `149912.795` |
| `Produktion Kanton FR | Production Canton FR` | object | 0 (0.0%) | 34902 | `kWh`, `6656.875`, `6722.45` |
| `Verbrauch Kanton FR | Consumption Canton FR` | object | 0 (0.0%) | 35035 | `kWh`, `82368.233`, `80823.111` |
| `Produktion Kanton GL | Production Canton GL` | object | 0 (0.0%) | 35010 | `kWh`, `56448.8`, `53069.975` |
| `Verbrauch Kanton GL | Consumption Canton GL` | object | 0 (0.0%) | 34995 | `kWh`, `12761.314`, `12490.398` |
| `Produktion Kanton GR | Production Canton GR` | object | 0 (0.0%) | 35039 | `kWh`, `196506.552`, `193462.923` |
| `Verbrauch Kanton GR | Consumption Canton GR` | object | 0 (0.0%) | 35030 | `kWh`, `89630.507`, `88438.556` |
| `Produktion Kanton LU | Production Canton LU` | object | 0 (0.0%) | 34999 | `kWh`, `4575.772`, `4552.267` |
| `Verbrauch Kanton LU | Consumption Canton LU` | object | 0 (0.0%) | 35031 | `kWh`, `104483.795`, `104540.894` |
| `Produktion Kanton NE | Production Canton NE` | object | 0 (0.0%) | 30333 | `kWh`, `213.42`, `149.75` |
| `Verbrauch Kanton NE | Consumption Canton NE` | object | 0 (0.0%) | 34997 | `kWh`, `16473.67`, `16067.144` |
| `Produktion Kanton SO | Production Canton SO` | object | 0 (0.0%) | 35005 | `kWh`, `265062.989`, `265344.35` |
| `Verbrauch Kanton SO | Consumption Canton SO` | object | 0 (0.0%) | 35020 | `kWh`, `58681.086`, `58310.74` |
| `Produktion Kanton SG | Production Canton SG` | object | 0 (0.0%) | 35028 | `kWh`, `8114.4082`, `8283.16` |
| `Verbrauch Kanton SG | Consumption Canton SG` | object | 0 (0.0%) | 35040 | `kWh`, `95202.2116`, `93580.7232` |
| `Produktion Kanton TI | Production Canton TI` | object | 0 (0.0%) | 35038 | `kWh`, `145406.418`, `148643.839` |
| `Verbrauch Kanton TI | Consumption Canton TI` | object | 0 (0.0%) | 35029 | `kWh`, `91474.056`, `90226.643` |
| `Produktion Kanton TG | Production Canton TG` | object | 0 (0.0%) | 34899 | `kWh`, `3556.971`, `3068.419` |
| `Verbrauch Kanton TG | Consumption Canton TG` | object | 0 (0.0%) | 35021 | `kWh`, `52865.413`, `52617.621` |
| `Produktion Kanton VS | Production Canton VS` | object | 0 (0.0%) | 35039 | `kWh`, `224593.382`, `214355.622` |
| `Verbrauch Kanton VS | Consumption Canton VS` | object | 0 (0.0%) | 35030 | `kWh`, `121539.756`, `120750.926` |
| `Produktion Kantone AI, AR | Production Cantons AI, AR` | object | 0 (0.0%) | 34972 | `kWh`, `548.3278`, `550.648` |
| `Verbrauch Kantone AI, AR | Consumption Cantons AI, AR` | object | 0 (0.0%) | 35034 | `kWh`, `17986.2574`, `17725.5918` |
| `Produktion Kantone BL, BS | Production Cantons BL, BS` | object | 0 (0.0%) | 35008 | `kWh`, `24430.7`, `24565.271` |
| `Verbrauch Kantone BL, BS | Consumption Cantons BL, BS` | object | 0 (0.0%) | 35036 | `kWh`, `100348.256`, `99852.429` |
| `Produktion Kantone BE, JU | Production Cantons BE, JU` | object | 0 (0.0%) | 35039 | `kWh`, `127693.152`, `132088.45` |
| `Verbrauch Kantone BE, JU | Consumption Cantons BE, JU` | object | 0 (0.0%) | 35036 | `kWh`, `261407.665`, `266459.303` |
| `Produktion Kantone SZ, ZG | Production Cantons SZ, ZG` | object | 0 (0.0%) | 34989 | `kWh`, `1880.602`, `1873.434` |
| `Verbrauch Kantone SZ, ZG | Consumption Cantons SZ, ZG` | object | 0 (0.0%) | 35032 | `kWh`, `60423.521`, `59339.989` |
| `Produktion Kantone OW, NW, UR | Production Cantons OW, NW, UR` | object | 0 (0.0%) | 35031 | `kWh`, `8730.862`, `8199.245` |
| `Verbrauch Kantone OW, NW, UR | Consumption Cantons OW, NW, UR` | object | 0 (0.0%) | 35017 | `kWh`, `35483.442`, `34859.735` |
| `Produktion Kantone GE, VD | Production Cantons GE, VD` | object | 0 (0.0%) | 35033 | `kWh`, `26248.344`, `26345.301` |
| `Verbrauch Kantone GE, VD | Consumption Cantons GE, VD` | object | 0 (0.0%) | 35039 | `kWh`, `203085.875`, `199200.393` |
| `Produktion Kantone SH, ZH | Production Cantons SH, ZH` | object | 0 (0.0%) | 34967 | `kWh`, `21630.758`, `21669.423` |
| `Verbrauch Kantone SH, ZH | Consumption Cantons SH, ZH` | object | 0 (0.0%) | 35038 | `kWh`, `271428.077`, `268050.733` |
| `Produktion Kantonsübergreifend | Production across Cantons` | object | 0 (0.0%) | 35033 | `kWh`, `63184.653`, `62903.913` |
| `Verbrauch Kantonsübergreifend | Consumption across Cantons` | object | 0 (0.0%) | 35030 | `kWh`, `79607.162`, `77654.465` |
| `Produktion Regelzone CH - Ausländische Gebiete | Production control area CH - foreign territories` | object | 0 (0.0%) | 34813 | `kWh`, `547.372`, `724.646` |
| `Verbrauch Regelzone CH - Ausländische Gebiete | Consumption control area CH - foreign territories` | object | 0 (0.0%) | 35002 | `kWh`, `13057.831`, `13074.058` |

## Sheet: `Zeitreihen1h00`

**Zeilen:** 8,761
**Spalten:** 2

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `Unnamed: 0` | object | 0 (0.0%) | 8760 | `Zeitstempel`, `2015-01-01 01:00:00`, `2015-01-01 02:00:00` |
| `Vertikale Netzlast Übertragungsnetz Schweiz | Vertical load Swiss transmission grid` | object | 0 (0.0%) | 8761 | `MW`, `6157.680969`, `6196.002239` |
