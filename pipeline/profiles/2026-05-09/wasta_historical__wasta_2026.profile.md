# Profil: wasta_2026.xlsx

**Erstellt:** 2026-05-09T18:43:49
**Pfad:** `C:\Users\pelle\SynologyDrive\Docs\Studium\FHGR\Masterthesis\energy-viz\pipeline\raw\snapshots\2026-05-09\wasta_historical\wasta_2026.xlsx`
**Format:** XLSX
**SHA-256:** `0ae37c32a5308e8eea357270280bcff6fd3da41bc3b3f0baeb215e2067fef439`
**Quelle:** https://pubdb.bfe.admin.ch/de/publication/download/12596
**Grösse:** 558.9 KB

**Sheets:** WASTA_01.01.2026_v1, WASTA_01.01.2026_v2

## Sheet: `WASTA_01.01.2026_v1`

**Zeilen:** 728
**Spalten:** 88

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `ZE-Nr` | int64 | 0 (0.0%) | 728 | 100100 … 900200 (mean 352571.79) |
| `ZE-Name` | str | 0 (0.0%) | 728 | `Val Giuv`, `Curnera Druckminderer`, `Val Strem` |
| `WKA-Name` | str | 0 (0.0%) | 646 | `Val Giuv`, `Curnera Vorderrhein`, `Val Strem` |
| `WKA-Typ` | str | 0 (0.0%) | 4 | `L`, `P`, `S`, `U` |
| `ZE-Standort` | str | 0 (0.0%) | 590 | `Rueras`, `Schiebekammer Curnera`, `Sedrun` |
| `ZE-Kanton` | str | 16 (2.2%) | 25 | `GR`, `GR`, `GR` |
| `ZE-Status` | str | 0 (0.0%) | 4 | `ausser Betrieb/reduzierter Betrieb`, `im Bau`, `im Normalbetrieb`, `im Umbau` |
| `Funktion:Turbinieren` | str | 21 (2.88%) | 1 | `T` |
| `Funktion:Pumpen` | str | 686 (94.23%) | 1 | `P` |
| `QTurbine[m3/s]` | float64 | 0 (0.0%) | 250 | 0.0 … 1500.0 (mean 41.67) |
| `Inst.Turbinenleistung[MW]` | float64 | 0 (0.0%) | 371 | 0.0 … 1269.0 (mean 25.04) |
| `"LTURBINE[MW]"/100*"PROZ.ANTEILCH"` | float64 | 0 (0.0%) | 372 | 0.0 … 1269.0 (mean 23.75) |
| `Max.LeistungGenerator[MW]` | float64 | 0 (0.0%) | 365 | 0.0 … 1200.0 (mean 24.03) |
| `"LGENERATOR[MW]"/100*"PROZ.ANTEILCH"` | float64 | 0 (0.0%) | 366 | 0.0 … 1200.0 (mean 22.82) |
| `Prod.ohneUmwaelzen-Winter[GWh]` | float64 | 0 (0.0%) | 372 | 0.0 … 1108.08 (mean 24.05) |
| `Prod.ohneUmwaelzen-Sommer[GWh]` | float64 | 0 (0.0%) | 421 | 0.0 … 995.02 (mean 32.76) |
| `Prod.ohneUmwaelzen-Jahr[GWh]` | float64 | 0 (0.0%) | 446 | 0.0 … 2103.1 (mean 56.81) |
| `"PROD.OHNEUMWaeLZB.-J."/100*"PROZ.ANTEILCH"` | float64 | 0 (0.0%) | 447 | 0.0 … 2103.1 (mean 51.32) |
| `QPumpe[m3/s]` | float64 | 0 (0.0%) | 40 | 0.0 … 360.0 (mean 1.29) |
| `Inst.Pumpenleistung[MW]` | float64 | 0 (0.0%) | 43 | 0.0 … 1000.0 (mean 5.63) |
| `Max.LeistungsaufnahmeMotoren[MW]` | float64 | 0 (0.0%) | 38 | 0.0 … 1000.0 (mean 5.59) |
| `Bed.ohneUmwaelzen-Winter[GWh]` | float64 | 0 (0.0%) | 25 | 0.0 … 31.08 (mean 0.21) |
| `Bed.ohneUmwaelzen-Sommer[GWh]` | float64 | 0 (0.0%) | 31 | 0.0 … 210.6 (mean 1.05) |
| `Bed.ohneUmwaelzen-Jahr[GWh]` | float64 | 0 (0.0%) | 32 | 0.0 … 226.88 (mean 1.26) |
| `ZE-ErsteInbetriebnahme` | int64 | 0 (0.0%) | 159 | 1816 … 2028 (mean 1957.96) |
| `ZE-LetzteInbetriebnahme` | float64 | 154 (21.15%) | 93 | 1923.0 … 2027.0 (mean 1992.89) |
| `ZE-Kote[m.u.M.]` | float64 | 0 (0.0%) | 681 | 193.0 … 2577.0 (mean 826.71) |
| `Proz.AnteilCH[%]` | float64 | 0 (0.0%) | 13 | 0.0 … 100.0 (mean 97.88) |
| `Kantonsanteil:Kanton1` | str | 0 (0.0%) | 26 | `GR`, `GR`, `GR` |
| `Kantonsanteil1[%]` | float64 | 0 (0.0%) | 36 | 0.0 … 100.0 (mean 96.03) |
| `Kantonsanteil:Kanton2` | str | 688 (94.51%) | 14 | `AG`, `AI`, `BL`, `FR`, `GR`, … (+9) |
| `Kantonsanteil2[%]` | float64 | 688 (94.51%) | 28 | 0.0 … 98.74 (mean 46.03) |
| `Kantonsanteil:Kanton3` | str | 723 (99.31%) | 4 | `SG`, `TG`, `TI`, `ZG` |
| `Kantonsanteil3[%]` | float64 | 723 (99.31%) | 4 | 9.55 … 54.0 (mean 25.77) |
| `GenutzteGewaesser1` | str | 0 (0.0%) | 420 | `Aua da Val Giuv`, `Rein da Curnera`, `Strem` |
| `GenutzteGewaesser2` | str | 413 (56.73%) | 262 | `Aua da Milez`, `Stausee Curnera`, `Rein da Curnera` |
| `GenutzteGewaesser3` | str | 581 (79.81%) | 132 | `Stausee Nalps`, `Rein da Nalps`, `Rein da Sumvitg` |
| `GenutzteGewaesser4` | str | 631 (86.68%) | 90 | `Rein da Tuma`, `Vorderrhein`, `Cuschinabach` |
| `GenutzteGewaesser5` | str | 665 (91.35%) | 57 | `Stausee Curnera`, `Stausee Runcahez`, `Stausee Zervreila` |
| `GenutzteGewaesser6` | str | 685 (94.09%) | 40 | `Stausee Nalps`, `Aua da Crusch`, `Valser Rhein` |
| `GenutzteGewaesser7` | str | 701 (96.29%) | 26 | `Stausee Santa Maria`, `Aua da Gierm`, `Niemetbach` |
| `GenutzteGewaesser8` | str | 712 (97.8%) | 16 | `Bavona`, `Carassino`, `Parebach`, `Petit Hongrin`, `Reuse de Saleinaz`, … (+11) |
| `GenutzteGewaesser9` | str | 717 (98.49%) | 11 | `Pisciabach`, `R. de Tompey`, `Reuse de Saleinaz`, `Riale Passera`, `Tersolbach`, … (+6) |
| `GenutzteGewaesser10` | str | 720 (98.9%) | 8 | `Lac du Pesseux`, `Oberalpbach`, `R. des Champs`, `Reno di Lei`, `Sella`, `Torrent de Planeureuse`, `Torrent de Treutsebo`, `Wildwueestibach` |
| `GenutzteGewaesser11` | str | 721 (99.04%) | 7 | `Aua da Val`, `Ausgleichsbecken Vallorcine`, `R. des Plans`, `Stausee Sufers`, `Torrent de Treutsebo`, `Torrent du Tour`, `Wolfisbach` |
| `GenutzteGewaesser12` | str | 722 (99.18%) | 6 | `Ausgleichsbecken Hintersand`, `Ausgleichsbecken Vallorcine`, `R. du Sepey`, `Rein da Cristallina`, `Stausee Valle di Lei`, `Torrent du Tour` |
| `Ersatzenergie:Richtung1` | str | 645 (88.6%) | 2 | `A`, `B` |
| `Ersatzenergie:Partner1` | str | 645 (88.6%) | 69 | `Repower AG Zentrale Waltensburg`, `EWZ Zentrale Rothenbrunnen EWZ`, `RE Zentrale Klosters` |
| `Ersatzenergie:Richtung2` | str | 706 (96.98%) | 2 | `A`, `B` |
| `Ersatzenergie:Partner2` | str | 706 (96.98%) | 22 | `KW Stoffel AG`, `Schluchseewerke`, `RKS Zentrale Saeckingen` |
| `Ersatzenergie:Richtung3` | str | 717 (98.49%) | 2 | `A`, `B` |
| `Ersatzenergie:Partner3` | str | 717 (98.49%) | 10 | `Axpo Power AG Zentrale Wildegg-Brugg`, `ED Zentrale Laufenburg`, `ED Zentrale Rheinfelden`, `EdF Zentrale Kembs`, `Groupe E SA Cen. Hauterive, Schiffenen`, … (+5) |
| `Ersatzenergie:Richtung4` | str | 724 (99.45%) | 2 | `A`, `B` |
| `Ersatzenergie:Partner4` | str | 724 (99.45%) | 4 | `Axpo Power AG Ruechlig-Dotierzentrale`, `CFF Centrale Vernayaz`, `EWM Zentr. Tobel`, `FMV Zentrale Chippis` |
| `Ersatzenergie:Richtung5` | str | 727 (99.86%) | 1 | `A` |
| `Ersatzenergie:Partner5` | str | 727 (99.86%) | 1 | `Hydroelectra AG Zentr. Halde` |
| `Ersatzenergie:Richtung6` | str | 727 (99.86%) | 1 | `A` |
| `Ersatzenergie:Partner6` | str | 727 (99.86%) | 1 | `Weberei Walenstadt` |
| `RechteName1` | str | 0 (0.0%) | 5 | `Andere Rechtsgrundlage`, `Bewilligung`, `Ehehaftes Recht`, `Konzession`, `Verfuegungsrecht` |
| `RechteEndjahr1` | int64 | 0 (0.0%) | 86 | 2001 … 9999 (mean 2997.87) |
| `RechteName2` | str | 718 (98.63%) | 3 | `Ehehaftes Recht`, `Konzession`, `Zusatzkonzession` |
| `RechteEndjahr2` | float64 | 718 (98.63%) | 2 | 2030.0 … 9999.0 (mean 8405.20) |
| `RechteName3` | float64 | 728 (100.0%) | 0 |  |
| `RechteEndjahr3` | float64 | 728 (100.0%) | 0 |  |
| `Bemerkung1` | str | 268 (36.81%) | 238 | `Die konzessionierte Ausbauwassermenge betraegt 426 I/s`, `KEV gefoerderte Anlage`, `Wiederinbetriebnahme per 12.2017 nach dem Felssturz von 03.2016` |
| `Bemerkung2` | str | 536 (73.63%) | 133 | `Bei der Wasserfassung Aua da Val Giuv ist die minimale Restwassermenge von 15 I/s abzugeben`, `KEV gefoerderte Anlage`, `Arbeiten: Sanierungen an Kaverne und Wasserfassung, Modernisierung der Schutz- und Steuerungsanlagen` |
| `Bemerkung3` | str | 641 (88.05%) | 63 | `Das Nutzungsrecht endet neu per Oktober 2039`, `KEV gefoerderte Anlage`, `                                   ` |
| `Bemerkung4` | str | 684 (93.96%) | 33 | `Im 2026 wird die Anlage voraussichtlich ausser Betrieb gehen!`, `DKW Staumauer Mapragg mit in Planung        `, ` ` |
| `Bemerkung5` | str | 701 (96.29%) | 20 | ` `, `  `, `      `, `       `, `            `, … (+15) |
| `Bemerkung6` | str | 714 (98.08%) | 10 | ` `, `                            `, `Bassin des Esserts Puiss.inst. des turb. Francis axe Gr.1 =  50.5 MW  `, `KEV gefoerderte Anlage`, `Revision des Triebwasserweges`, … (+5) |
| `Bemerkung7` | str | 718 (98.63%) | 7 | ` `, `      `, `                  `, `Ersatz der drei aeltesten Bahnstromgeneratoren von 1937`, `Maschinen sind etappenweise ausser Betrieb, aber die Zwillingsmaschine bleibt mehrheitlich in Betrieb`, `Puissance max.disponible Gr.1 =  48.5 MW                    `, `ab 2023 wieder in Betrieb` |
| `Bemerkung8` | str | 721 (99.04%) | 5 | ` `, `     `, `                         `, `                                                    `, `Les equipements haute chute, basse chute et Centrale de pompage de Chatelard-Vallorcine se trouvent dans le même batiment et leur` |
| `Bemerkung9` | float64 | 728 (100.0%) | 0 |  |
| `ZE-KoordinatenE` | int64 | 0 (0.0%) | 701 | 2486880 … 2844830 (mean 2668816.31) |
| `ZE-KoordinatenN` | int64 | 0 (0.0%) | 700 | 1083247 … 1283470 (mean 1178086.28) |
| `InternationalesKW` | str | 694 (95.33%) | 1 | `J` |
| `NutzungstypCode` | str | 623 (85.58%) | 6 | `A`, `B`, `D`, `T`, `U`, `W` |
| `NutzungstypBeschreibung` | str | 623 (85.58%) | 6 | `Abwasser`, `Beschneiungswasser`, `Dotierwasser`, `Trinkwasser`, `Tunnelwasser`, `Waesserwasser` |
| `UntertypCode` | str | 3 (0.41%) | 3 | `A`, `F`, `N` |
| `UntertypBeschreibung` | str | 3 (0.41%) | 3 | `Ausleitkraftwerk`, `Flusskraftwerk mit Stauwerk`, `Nebennutzungskraftwerk` |
| `Max.Bruttofallhoehe[m]` | float64 | 0 (0.0%) | 602 | 0.0 … 1883.0 (mean 268.85) |
| `Min.Bruttofallhoehe[m]` | float64 | 0 (0.0%) | 555 | 0.0 … 1734.0 (mean 242.67) |
| `Max.Nettofallhoehe[m]` | float64 | 0 (0.0%) | 496 | 0.0 … 1768.3 (mean 199.96) |
| `Min.Nettofallhoehe[m]` | float64 | 0 (0.0%) | 480 | 0.0 … 1628.4 (mean 178.10) |
| `Max.Bruttofoerderhoehe[m]` | float64 | 0 (0.0%) | 40 | 0.0 … 1053.2 (mean 22.41) |
| `Min.Bruttofoerderhoehe[m]` | float64 | 0 (0.0%) | 40 | 0.0 … 1005.0 (mean 18.59) |
| `Max.Nettofoerderhoehe[m]` | float64 | 0 (0.0%) | 38 | 0.0 … 923.4 (mean 17.53) |
| `Min.Nettofoerderhoehe[m]` | float64 | 0 (0.0%) | 37 | 0.0 … 822.8 (mean 14.28) |

## Sheet: `WASTA_01.01.2026_v2`

**Zeilen:** 722
**Spalten:** 86

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `WASTA` | int64 | 0 (0.0%) | 722 | 100100 … 900200 (mean 352980.75) |
| `Name Zentrale (ZE)` | str | 0 (0.0%) | 722 | `Val Giuv`, `Curnera Druckminderer`, `Val Strem` |
| `Name Wasserkraftanlage (WKA)` | str | 0 (0.0%) | 640 | `Val Giuv`, `Curnera Vorderrhein`, `Val Strem` |
| `Name Standort Zentrale` | str | 0 (0.0%) | 587 | `Rueras`, `Schiebekammer Curnera`, `Sedrun` |
| `WKA Typ` | str | 0 (0.0%) | 5 | `L`, `P`, `PS`, `S`, `U` |
| `Kanton Standort Zentrale` | str | 16 (2.22%) | 25 | `GR`, `GR`, `GR` |
| `Staat Standort Zentrale` | str | 0 (0.0%) | 4 | `A`, `CH`, `D`, `F` |
| `Anteil CH [%]` | float64 | 0 (0.0%) | 13 | 0.0 … 1.0 (mean 0.98) |
| `Betriebsstatus Zentrale` | str | 0 (0.0%) | 4 | `ausser Betrieb`, `im Normalbetrieb`, `im Umbau`, `reduzierter Betrieb` |
| `Funktion Turbinieren` | str | 21 (2.91%) | 1 | `T` |
| `Funktion Pumpen` | str | 681 (94.32%) | 1 | `P` |
| `Ausbauwassermenge Turbinen [m³/s]` | float64 | 0 (0.0%) | 248 | 0.0 … 1500.0 (mean 41.94) |
| `installierte Leistung Turbinen [MW]` | float64 | 0 (0.0%) | 371 | 0.0 … 1269.0 (mean 25.06) |
| `Anteil CH Turbinen [MW] berechnet` | float64 | 0 (0.0%) | 375 | 0.0 … 1269.0 (mean 23.76) |
| `maximale Leistung ab Generatoren [MW]` | float64 | 0 (0.0%) | 364 | 0.0 … 1200.0 (mean 24.05) |
| `Anteil CH Generator [MW] berechnet` | float64 | 0 (0.0%) | 365 | 0.0 … 1200.0 (mean 22.82) |
| `mittlere Produktionserwartung im Jahr [GWh]` | float64 | 0 (0.0%) | 444 | 0.0 … 2103.1 (mean 57.01) |
| `davon im Winter [GWh]` | float64 | 0 (0.0%) | 370 | 0.0 … 1108.08 (mean 24.10) |
| `davon im Sommer [GWh]` | float64 | 0 (0.0%) | 419 | 0.0 … 995.02 (mean 32.91) |
| `Anteil CH Produktion [GWh] berechnet` | float64 | 0 (0.0%) | 445 | 0.0 … 2103.1 (mean 51.47) |
| `Ausbauwassermenge Pumpen [m³/s]` | float64 | 0 (0.0%) | 39 | 0.0 … 360.0 (mean 1.29) |
| `installierte Leistung Pumpen [MW]` | float64 | 0 (0.0%) | 42 | 0.0 … 1000.0 (mean 5.60) |
| `maximale Leistungsaufnahme der Motoren [MW]` | float64 | 0 (0.0%) | 37 | 0.0 … 1000.0 (mean 5.55) |
| `mittlerer Pumpenbedarf im Jahr [GWh]` | float64 | 0 (0.0%) | 32 | 0.0 … 226.88 (mean 1.27) |
| `davon im Winter [GWh].1` | float64 | 0 (0.0%) | 25 | 0.0 … 31.08 (mean 0.21) |
| `davon im Sommer [GWh].1` | float64 | 0 (0.0%) | 31 | 0.0 … 210.6 (mean 1.06) |
| `Anteil CH Pumpenbedarf [GWh] berechnet` | float64 | 0 (0.0%) | 33 | 0.0 … 226.88 (mean 1.15) |
| `erste Inbetriebnahme [a]` | int64 | 0 (0.0%) | 156 | 1816 … 2025 (mean 1957.39) |
| `letzte Inbetriebnahme [a]` | float64 | 148 (20.5%) | 93 | 1923.0 … 2027.0 (mean 1992.95) |
| `Kote Turbinenachse [m.ü.M]` | float64 | 0 (0.0%) | 676 | 193.0 … 2577.0 (mean 825.45) |
| `Kanton 1 (Initialen)` | str | 0 (0.0%) | 26 | `GR`, `GR`, `GR` |
| `Anteil Kanton 1 [%]` | float64 | 0 (0.0%) | 36 | 0.0 … 100.0 (mean 96.08) |
| `Kanton 2 (Initialen)` | str | 684 (94.74%) | 14 | `AG`, `AI`, `BL`, `FR`, `GR`, … (+9) |
| `Anteil Kanton 2 [%]` | float64 | 684 (94.74%) | 28 | 0.0 … 98.74 (mean 47.29) |
| `Kanton 3 (Initialen)` | str | 718 (99.45%) | 4 | `SG`, `TG`, `TI`, `ZG` |
| `Anteil Kanton 3 [%]` | float64 | 718 (99.45%) | 4 | 9.55 … 54.0 (mean 28.29) |
| `genutztes Gewässer 1` | str | 0 (0.0%) | 416 | `Aua da Val Giuv`, `Rein da Curnera`, `Strem` |
| `genutztes Gewässer 2` | str | 410 (56.79%) | 261 | `Aua da Milez`, `Stausee Curnera`, `Rein da Curnera` |
| `genutztes Gewässer 3` | str | 576 (79.78%) | 132 | `Stausee Nalps`, `Rein da Nalps`, `Rein da Sumvitg` |
| `genutztes Gewässer 4` | str | 626 (86.7%) | 90 | `Rein da Tuma`, `Vorderrhein`, `Cuschinabach` |
| `genutztes Gewässer 5` | str | 660 (91.41%) | 57 | `Stausee Curnera`, `Stausee Runcahez`, `Stausee Zervreila` |
| `genutztes Gewässer 6` | str | 679 (94.04%) | 40 | `Stausee Nalps`, `Aua da Crusch`, `Valser Rhein` |
| `genutztes Gewässer 7` | str | 695 (96.26%) | 26 | `Stausee Santa Maria`, `Aua da Gierm`, `Niemetbach` |
| `genutztes Gewässer 8` | str | 706 (97.78%) | 16 | `Bavona`, `Carassino`, `Parebach`, `Petit Hongrin`, `Reuse de Saleinaz`, … (+11) |
| `genutztes Gewässer 9` | str | 711 (98.48%) | 11 | `Pisciabach`, `R. de Tompey`, `Reuse de Saleinaz`, `Riale Passera`, `Tersolbach`, … (+6) |
| `genutztes Gewässer 10` | str | 714 (98.89%) | 8 | `Lac du Pesseux`, `Oberalpbach`, `R. des Champs`, `Reno di Lei`, `Sella`, `Torrent de Planeureuse`, `Torrent de Treutsebo`, `Wildwüestibach` |
| `genutztes Gewässer 11` | str | 715 (99.03%) | 7 | `Aua da Val`, `Ausgleichsbecken Vallorcine`, `R. des Plans`, `Stausee Sufers`, `Torrent de Treutsebo`, `Torrent du Tour`, `Wolfisbach` |
| `genutztes Gewässer 12` | str | 716 (99.17%) | 6 | `Ausgleichsbecken Hintersand`, `Ausgleichsbecken Vallorcine`, `R. du Sepey`, `Rein da Cristallina`, `Stausee Valle di Lei`, `Torrent du Tour` |
| `Ersatzenergie 1 (Richtung)` | str | 639 (88.5%) | 2 | `A`, `B` |
| `Ersatzenergie Partner 1 (Name)` | str | 639 (88.5%) | 69 | `Repower AG Zentrale Waltensburg`, `EWZ Zentrale Rothenbrunnen EWZ`, `RE Zentrale Klosters` |
| `Ersatzenergie 2 (Richtung)` | str | 700 (96.95%) | 2 | `A`, `B` |
| `Ersatzenergie Partner 2 (Name)` | str | 700 (96.95%) | 22 | `KW Stoffel AG`, `Schluchseewerke`, `RKS Zentrale Saeckingen` |
| `Ersatzenergie 3 (Richtung)` | str | 711 (98.48%) | 2 | `A`, `B` |
| `Ersatzenergie Partner 3 (Name)` | str | 711 (98.48%) | 10 | `Axpo Power AG Zentrale Wildegg-Brugg`, `ED Zentrale Laufenburg`, `ED Zentrale Rheinfelden`, `EdF Zentrale Kembs`, `Groupe E SA Cen. Hauterive, Schiffenen`, … (+5) |
| `Ersatzenergie 4 (Richtung)` | str | 718 (99.45%) | 2 | `A`, `B` |
| `Ersatzenergie Partner 4 (Name)` | str | 718 (99.45%) | 4 | `Axpo Power AG Ruechlig-Dotierzentrale`, `CFF Centrale Vernayaz`, `EWM Zentr. Tobel`, `FMV Zentrale Chippis` |
| `Ersatzenergie 5 (Richtung)` | str | 721 (99.86%) | 1 | `A` |
| `Ersatzenergie Partner 5 (Name)` | str | 721 (99.86%) | 1 | `Hydroelectra AG Zentr. Halde` |
| `Ersatzenergie 6 (Richtung)` | str | 721 (99.86%) | 1 | `A` |
| `Ersatzenergie Partner 6 (Name)` | str | 721 (99.86%) | 1 | `Weberei Walenstadt` |
| `Art der Rechtsgrundlage 1` | str | 0 (0.0%) | 5 | `Andere Rechtsgrundlage`, `Bewilligung`, `Ehehaftes Recht`, `Konzession`, `Verfügungsrecht` |
| `Endjahr der Rechtsgrundlage 1 [a]` | int64 | 0 (0.0%) | 86 | 2001 … 9999 (mean 3016.26) |
| `Art der Rechtsgrundlage 2` | str | 712 (98.61%) | 3 | `Ehehaftes Recht`, `Konzession`, `Zusatzkonzession` |
| `Endjahr der Rechtsgrundlage 2 [a]` | float64 | 712 (98.61%) | 2 | 2030.0 … 9999.0 (mean 8405.20) |
| `Bemerkung 1` | str | 268 (37.12%) | 232 | `Die konzessionierte Ausbauwassermenge betraegt 426 I/s`, `KEV gefoerderte Anlage`, `Wiederinbetriebnahme per 12.2017 nach dem Felssturz von 03.2016` |
| `Bemerkung 2` | str | 534 (73.96%) | 129 | `Bei der Wasserfassung Aua da Val Giuv ist die minimale Restwassermenge von 15 I/s abzugeben`, `KEV gefoerderte Anlage`, `Arbeiten: Sanierungen an Kaverne und Wasserfassung, Modernisierung der Schutz- und Steuerungsanlagen` |
| `Bemerkung 3` | str | 636 (88.09%) | 62 | `Das Nutzungsrecht endet neu per Oktober 2039`, `KEV gefoerderte Anlage`, `                                   ` |
| `Bemerkung 4` | str | 678 (93.91%) | 33 | `Im 2026 wird die Anlage voraussichtlich ausser Betrieb gehen!`, `DKW Staumauer Mapragg mit in Planung        `, ` ` |
| `Bemerkung 5` | str | 695 (96.26%) | 20 | ` `, `  `, `      `, `       `, `            `, … (+15) |
| `Bemerkung 6` | str | 708 (98.06%) | 10 | ` `, `                            `, `Bassin des Esserts Puiss.inst. des turb. Francis axe Gr.1 =  50.5 MW  `, `KEV gefoerderte Anlage`, `Revision des Triebwasserweges`, … (+5) |
| `Bemerkung 7` | str | 712 (98.61%) | 7 | ` `, `      `, `                  `, `Ersatz der drei aeltesten Bahnstromgeneratoren von 1937`, `Maschinen sind etappenweise ausser Betrieb, aber die Zwillingsmaschine bleibt mehrheitlich in Betrieb`, `Puissance max.disponible Gr.1 =  48.5 MW                    `, `ab 2023 wieder in Betrieb` |
| `Bemerkung 8` | str | 715 (99.03%) | 5 | ` `, `     `, `                         `, `                                                    `, `Les equipements haute chute, basse chute et Centrale de pompage de Chatelard-Vallorcine se trouvent dans le même batiment et leur` |
| `ZE-Koordinaten (E)` | int64 | 0 (0.0%) | 695 | 2486880 … 2844830 (mean 2668716.77) |
| `ZE-Koordinaten (N)` | int64 | 0 (0.0%) | 694 | 1083247 … 1283470 (mean 1178008.40) |
| `Untertyp (Code)` | str | 21 (2.91%) | 3 | `A`, `F`, `N` |
| `Name Untertyp` | str | 21 (2.91%) | 3 | `Ausleitkraftwerk`, `Flusskraftwerk (reines Stauwerk)`, `Nebennutzungskraftwerk` |
| `Nutzungstyp (Code)` | str | 620 (85.87%) | 6 | `A`, `B`, `D`, `T`, `U`, `W` |
| `Name Nutzungstyp` | str | 620 (85.87%) | 6 | `Abwasser`, `Beschneiungswasser`, `Dotierwasser`, `Trinkwasser`, `Tunnelwasser`, `Wässerwasser` |
| `maximale Bruttofallhöhe [m]` | float64 | 0 (0.0%) | 598 | 0.0 … 1883.0 (mean 268.67) |
| `minimale Bruttofallhöhe [m]` | float64 | 0 (0.0%) | 549 | 0.0 … 1734.0 (mean 242.36) |
| `maximale Nettofallhöhe [m]` | float64 | 0 (0.0%) | 493 | 0.0 … 1768.3 (mean 200.44) |
| `minimale Nettofallhöhe [m]` | float64 | 0 (0.0%) | 479 | 0.0 … 1628.4 (mean 178.48) |
| `maximale Bruttoförderhöhe [m]` | float64 | 0 (0.0%) | 39 | 0.0 … 1053.2 (mean 21.59) |
| `minimale Bruttoförderhöhe [m]` | float64 | 0 (0.0%) | 39 | 0.0 … 1005.0 (mean 17.80) |
| `maximale Nettoförderhöhe [m]` | float64 | 0 (0.0%) | 37 | 0.0 … 923.4 (mean 16.68) |
| `minimale Nettoförderhöhe [m]` | float64 | 0 (0.0%) | 36 | 0.0 … 822.8 (mean 13.46) |
