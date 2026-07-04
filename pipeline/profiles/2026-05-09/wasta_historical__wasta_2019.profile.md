# Profil: wasta_2019.xlsx

**Erstellt:** 2026-05-09T18:43:47
**Pfad:** `C:\Users\pelle\SynologyDrive\Docs\Studium\FHGR\Masterthesis\energy-viz\pipeline\raw\snapshots\2026-05-09\wasta_historical\wasta_2019.xlsx`
**Format:** XLSX
**SHA-256:** `96fac9552bef1010a33d62be9a9b7cf7c7e1fbb6c32b263fc0802ad8df069254`
**Quelle:** https://pubdb.bfe.admin.ch/de/publication/download/9690
**Grösse:** 169.5 KB

**Sheets:** Vorschau

## Sheet: `Vorschau`

**Zeilen:** 696
**Spalten:** 104

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `ZE-Nr` | int64 | 0 (0.0%) | 696 | 100100 … 900200 (mean 351963.41) |
| `ZE-Name` | str | 0 (0.0%) | 696 | `Val Giuv`, `Val Strem`, `Sedrun 1` |
| `WKA-Name` | str | 0 (0.0%) | 665 | `Val Giuf`, `Val Strem`, `Sedrun 1` |
| `WKA-Typ` | str | 0 (0.0%) | 4 | `L`, `P`, `S`, `U` |
| `ZE-Standort` | str | 0 (0.0%) | 556 | `Rueras`, `Sedrun`, `Sedrun` |
| `ZE-Kanton` | str | 15 (2.16%) | 25 | `Graubünden`, `Graubünden`, `Graubünden` |
| `ZE-Status` | str | 0 (0.0%) | 4 | `ausser Betrieb/reduzierter Betrieb`, `im Bau`, `im Normalbetrieb`, `im Umbau` |
| `Funktion: Turbinieren` | str | 18 (2.59%) | 1 | `T` |
| `Funktion: Pumpen` | str | 656 (94.25%) | 1 | `P` |
| `QTurbine [m3/sec]` | float64 | 0 (0.0%) | 246 | 0.0 … 1500.0 (mean 43.14) |
| `Inst. Turbinenleistung` | float64 | 0 (0.0%) | 358 | 0.0 … 1285.0 (mean 25.85) |
| `("LTURBINE[MW]"/100)*"PROZ.ANTEILCH"` | float64 | 0 (0.0%) | 360 | 0.0 … 1285.0 (mean 24.56) |
| `Max. Leistung ab Generator` | float64 | 0 (0.0%) | 329 | 0.0 … 1260.0 (mean 25.02) |
| `("LGENERATOR[MW]"/100)*"PROZ.ANTEILCH"` | float64 | 0 (0.0%) | 333 | 0.0 … 1260.0 (mean 23.77) |
| `Prod. ohne Umwälzbetrieb - W.` | float64 | 0 (0.0%) | 347 | 0.0 … 1558.3 (mean 24.86) |
| `Prod. ohne Umwälzbetrieb - S.` | float64 | 0 (0.0%) | 418 | 0.0 … 642.7 (mean 33.72) |
| `Prod. ohne Umwälzbetrieb - J.` | float64 | 0 (0.0%) | 429 | 0.0 … 2201.0 (mean 58.58) |
| `("PROD.OHNEUMWÄLZBETRIEB-J."/100)*"PROZ.ANTEILCH"` | float64 | 0 (0.0%) | 427 | 0.0 … 2201.0 (mean 52.85) |
| `QPumpe [m3/sec]` | float64 | 0 (0.0%) | 39 | 0.0 … 360.0 (mean 1.32) |
| `Inst. Pumpenleistung` | float64 | 0 (0.0%) | 41 | 0.0 … 1000.0 (mean 5.73) |
| `Leistungsaufnahme Motoren` | float64 | 0 (0.0%) | 37 | 0.0 … 1000.0 (mean 5.70) |
| `Bedarf ohne Umwälzb. - W.` | float64 | 0 (0.0%) | 21 | 0.0 … 28.75 (mean 0.19) |
| `Bedarf ohne Umwälzb. - S.` | float64 | 0 (0.0%) | 30 | 0.0 … 197.4 (mean 1.14) |
| `Bedarf ohne Umwälzb. - J.` | float64 | 0 (0.0%) | 33 | 0.0 … 205.9 (mean 1.33) |
| `ZE-Erste Inbetriebnahme` | int64 | 0 (0.0%) | 153 | 1816 … 2023 (mean 1955.39) |
| `ZE-Letzte Inbetriebnahme` | float64 | 124 (17.82%) | 88 | 1915.0 … 2019.0 (mean 1985.91) |
| `ZE-Kote` | float64 | 0 (0.0%) | 648 | 200.0 … 2273.2 (mean 816.53) |
| `Proz. Anteil CH` | float64 | 0 (0.0%) | 13 | 0.0 … 100.0 (mean 97.78) |
| `Kantonsanteil: Kanton Name (1)` | str | 0 (0.0%) | 26 | `Graubünden`, `Graubünden`, `Graubünden` |
| `Kantonsanteil (1)` | float64 | 0 (0.0%) | 37 | 0.0 … 100.0 (mean 95.06) |
| `Kantonsanteil: Kanton Name (2)` | str | 659 (94.68%) | 14 | `Aargau`, `Appenzell I.Rh.`, `Basel-Landschaft`, `Freiburg`, `Graubünden`, … (+9) |
| `Kantonsanteil (2)` | float64 | 659 (94.68%) | 30 | 0.0 … 98.74 (mean 48.10) |
| `Kantonsanteil: Kanton Name (3)` | str | 692 (99.43%) | 4 | `St.Gallen`, `Tessin`, `Thurgau`, `Zug` |
| `Kantonsanteil (3)` | float64 | 692 (99.43%) | 4 | 9.55 … 54.0 (mean 27.36) |
| `Genutzte Gewässer - Name (1)` | str | 0 (0.0%) | 409 | `Aua da Milez`, `Strem`, `Froda` |
| `Genutzte Gewässer - Name (2)` | str | 433 (62.21%) | 215 | `Aua da Val Giuf`, `Rein da Curnera`, `Rein da Nalps` |
| `Genutzte Gewässer - Name (3)` | str | 570 (81.9%) | 109 | `Rein da Nalps`, `Rein da Sumvitg`, `Quellen Cuolms da Runs` |
| `Genutzte Gewässer - Name (4)` | str | 608 (87.36%) | 77 | `Rein da Tuma`, `Vorderrhein`, `Ual da Siat` |
| `Genutzte Gewässer - Name (5)` | str | 643 (92.39%) | 46 | `Stausee Curnera`, `Stausee Zervreila`, `Lago di Lei` |
| `Genutzte Gewässer - Name (6)` | str | 660 (94.83%) | 32 | `Stausee Nalps`, `Valser Rhein`, `Madriserrhein` |
| `Genutzte Gewässer - Name (7)` | str | 672 (96.55%) | 21 | `Stausee Sta.Maria`, `Maleggabach`, `Speicher Gigerwald` |
| `("LGENERATOR[MW]"/100)*"PROZ.ANTEILCH".1` | float64 | 0 (0.0%) | 333 | 0.0 … 1260.0 (mean 23.77) |
| `Genutzte Gewässer - Name (8)` | str | 683 (98.13%) | 12 | `Nant de Drance, Triège`, `Niemetbach`, `Petit Hongrin`, `R. Giacobi`, `Reuse de Saleinaz`, … (+7) |
| `Genutzte Gewässer - Name (9)` | str | 684 (98.28%) | 11 | `Parebach`, `R. Passera`, `R. de Tompey`, `Reuse de Saleinaz`, `Tersolbach`, … (+6) |
| `Genutzte Gewässer - Name (10)` | str | 690 (99.14%) | 6 | `Pisciabach`, `R. Sella`, `R. des Champs`, `Torrent de Planeureuse`, `Torrent de Treutse Bô`, `Wildwüestibach` |
| `Genutzte Gewässer - Name (11)` | str | 691 (99.28%) | 5 | `R. des Plans`, `Reno di Lei`, `Torrent de Treutse-Bô`, `Torrent du Tour`, `Wolfisbach` |
| `Genutzte Gewässer - Name (12)` | str | 692 (99.43%) | 4 | `R. du Sepey`, `Stausee Sufers`, `Torrent du Tour`, `Triège-CFF` |
| `Ersatzenergie: Richtung (1)` | str | 612 (87.93%) | 2 | `A`, `B` |
| `Ersatzenergie: Partner (1)` | str | 612 (87.93%) | 71 | `Repower AG (Zentrale Waltensburg)`, `EWZ (Zentrale Rothenbrunnen EWZ)`, `RE (Zentrale Klosters)` |
| `Ersatzenergie: Richtung (2)` | str | 676 (97.13%) | 2 | `A`, `B` |
| `Ersatzenergie: Partner (2)` | str | 676 (97.13%) | 20 | `AET    (Diversi centrali)`, `BKW   (Centr. Aarberg,Hagneck,Kallnach)`, `ED (Zentrale Wyhlen)`, `FMO     (Centrale d'Orsières)`, `GKW        (Zentrale Neubrigg)`, … (+15) |
| `Ersatzenergie: Richtung (3)` | str | 685 (98.42%) | 2 | `A`, `B` |
| `Ersatzenergie: Partner (3)` | str | 685 (98.42%) | 11 | `Axpo Power AG (Zentrale Wildegg-Brugg)`, `ED (Zentrale Laufenburg)`, `ED (Zentrale Rheinfelden)`, `EdF (Zentrale Kembs)`, `Groupe E SA (Cen. Hauterive, Schiffenen)`, … (+6) |
| `Ersatzenergie: Richtung (4)` | str | 692 (99.43%) | 2 | `A`, `B` |
| `Ersatzenergie: Partner (4)` | str | 692 (99.43%) | 4 | `Axpo Power AG (Rüchlig-Dotierzentrale)`, `CFF      (Centrale Vernayaz)`, `EWM            (Zentr. Tobel)`, `FMV (Zentrale Chippis)` |
| `Ersatzenergie: Richtung (5)` | str | 695 (99.86%) | 1 | `A` |
| `Ersatzenergie: Partner (5)` | str | 695 (99.86%) | 1 | `Hydroelectra AG (Zentr. Mels (Halde))` |
| `Ersatzenergie :Richtung (6)` | str | 695 (99.86%) | 1 | `A` |
| `Ersatzenergie: Partner (6)` | str | 695 (99.86%) | 1 | `Weberei Walenstadt` |
| `Ersatzenergie: Richtung (7)` | float64 | 696 (100.0%) | 0 |  |
| `Ersatzenergie: Partner (7)` | float64 | 696 (100.0%) | 0 |  |
| `Ersatzenergie: Richtung (8)` | float64 | 696 (100.0%) | 0 |  |
| `Ersatzenergie: Partner (8)` | float64 | 696 (100.0%) | 0 |  |
| `Ersatzenergie: Richtung (9)` | float64 | 696 (100.0%) | 0 |  |
| `Ersatzenergie: Partner (9)` | float64 | 696 (100.0%) | 0 |  |
| `Ersatzenergie: Richtung (10)` | float64 | 696 (100.0%) | 0 |  |
| `Ersatzenergie: Partner (10)` | float64 | 696 (100.0%) | 0 |  |
| `Ersatzenergie: Richtung (11)` | float64 | 696 (100.0%) | 0 |  |
| `Ersatzenergie: Partner (11)` | float64 | 696 (100.0%) | 0 |  |
| `Ersatzenergie: Richtung (12)` | float64 | 696 (100.0%) | 0 |  |
| `Ersatzenergie: Partner (12)` | float64 | 696 (100.0%) | 0 |  |
| `Rechte - Name (1)` | str | 4 (0.57%) | 5 | `Andere Rechtsgrundlage`, `Bewilligung`, `Ehehaftes Recht`, `Konzession(en)`, `Verfügungsrecht` |
| `Rechte - Endjahr (1)` | float64 | 4 (0.57%) | 84 | 1998.0 … 9999.0 (mean 3239.02) |
| `Rechte - Name (2)` | str | 674 (96.84%) | 4 | `Andere Rechtsgrundlage`, `Bewilligung`, `Ehehaftes Recht`, `Konzession(en)` |
| `Rechte - Endjahr (2)` | float64 | 674 (96.84%) | 5 | 2030.0 … 9999.0 (mean 8554.23) |
| `Rechte - Name (3)` | str | 694 (99.71%) | 2 | `Andere Rechtsgrundlage`, `Ehehaftes Recht` |
| `Rechte - Endjahr (3)` | float64 | 694 (99.71%) | 1 | 9999.0 … 9999.0 (mean 9999.00) |
| `Rechte - Name (4)` | float64 | 696 (100.0%) | 0 |  |
| `Rechte - Endjahr (4)` | float64 | 696 (100.0%) | 0 |  |
| `Rechte - Name (5)` | float64 | 696 (100.0%) | 0 |  |
| `Rechte - Endjahr (5)` | float64 | 696 (100.0%) | 0 |  |
| `Rechte - Name (6)` | float64 | 696 (100.0%) | 0 |  |
| `Rechte - Endjahr (6)` | float64 | 696 (100.0%) | 0 |  |
| `Rechte - Name (7)` | float64 | 696 (100.0%) | 0 |  |
| `Rechte - Endjahr (7)` | float64 | 696 (100.0%) | 0 |  |
| `Rechte - Name (8)` | float64 | 696 (100.0%) | 0 |  |
| `Rechte - Endjahr (8)` | float64 | 696 (100.0%) | 0 |  |
| `Rechte - Name (9)` | float64 | 696 (100.0%) | 0 |  |
| `Rechte - Endjahr (9)` | float64 | 696 (100.0%) | 0 |  |
| `Rechte - Name (10)` | float64 | 696 (100.0%) | 0 |  |
| `Rechte - Endjahr (10)` | float64 | 696 (100.0%) | 0 |  |
| `Bemerkung (1)` | str | 463 (66.52%) | 176 | `- Zentralen Sedrun 1 und Sedrun 2 in einer Kaverne`, `- Zentralen Sedrun 1 und Sedrun 2 in einer Kaverne`, `- Kote Maschinensaalboden bezieht sich auf die Höhe der Turbinenachse` |
| `Bemerkung (2)` | str | 587 (84.34%) | 85 | `                                   `, `                                         `, ` ` |
| `Bemerkung (3)` | str | 637 (91.52%) | 45 | ` `, `  Ausbauwassermenge (an 60 Tagen erreicht)		=   0.87 m3/s`, `                    	             ` |
| `Bemerkung (4)` | str | 656 (94.25%) | 35 | `			`, `  Installierte Leistung sämtlicher Turbinen		=   1.27 MW`, `  Ausbauwassermenge (an 138 Tagen erreicht)		=   1100 m3/s` |
| `Bemerkung (5)` | str | 669 (96.12%) | 21 | ` `, `  Maximal mögliche Leistung ab Generatoren		=   1.40 MW`, `  Installierte Leistung sämtlicher Turbinen		=   84.90 MW` |
| `Bemerkung (6)` | str | 675 (96.98%) | 20 | `			Val Ferpècle est`, ` `, `      `, `                 	        `, `                          		Châtelard-Barberine 2 = 82 MW          `, … (+15) |
| `Bemerkung (7)` | str | 678 (97.41%) | 16 | ` `, `      `, `               			Puissance max.disponible        Gr.1 	=  48.5 MW                    `, `                  `, `                   `, … (+11) |
| `Bemerkung (8)` | str | 680 (97.7%) | 13 | ` `, `     `, `      `, `                         `, `                          `, … (+8) |
| `Bemerkung (9)` | str | 680 (97.7%) | 15 | ` `, `                     	      `, `                         	`, `                          `, `                                         `, … (+10) |
| `Bemerkung (10)` | str | 681 (97.84%) | 12 | ` `, `       `, `         `, `          `, `                     	     `, … (+7) |
| `ZE-Koordinaten unscharf (Ost)` | int64 | 0 (0.0%) | 643 | 2486880 … 2844830 (mean 2669148.10) |
| `ZE-Koordinaten unscharf (Nord)` | int64 | 0 (0.0%) | 638 | 1081630 … 1283470 (mean 1179139.55) |
| `Internationales KW` | str | 662 (95.11%) | 1 | `Ja` |
