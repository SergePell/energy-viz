# Profil: wasta_2024.xlsx

**Erstellt:** 2026-05-09T18:43:48
**Pfad:** `C:\Users\pelle\SynologyDrive\Docs\Studium\FHGR\Masterthesis\energy-viz\pipeline\raw\snapshots\2026-05-09\wasta_historical\wasta_2024.xlsx`
**Format:** XLSX
**SHA-256:** `78255dbbd9c049e921fa94178be3cb042acbcc8fcbf825e3037bae840b3bf922`
**Quelle:** https://pubdb.bfe.admin.ch/de/publication/download/11719
**Grösse:** 217.4 KB

**Sheets:** WASTA 31.12.2023

## Sheet: `WASTA 31.12.2023`

**Zeilen:** 749
**Spalten:** 115

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `ZE-Nr` | int64 | 0 (0.0%) | 749 | 100100 … 900200 (mean 352150.68) |
| `ZE-Name` | str | 0 (0.0%) | 749 | `Val Giuv`, `Curnera Druckminderer`, `Val Strem` |
| `WKA-Name` | str | 0 (0.0%) | 713 | `Val Giuf`, `Curnera Druckminderer`, `Val Strem` |
| `WKA-Typ` | str | 0 (0.0%) | 4 | `L`, `P`, `S`, `U` |
| `ZE-Standort` | str | 0 (0.0%) | 590 | `Rueras`, `Schiebekammer Curnera Sataum.`, `Sedrun` |
| `ZE-Kanton` | str | 15 (2.0%) | 25 | `Graubünden`, `Graubünden`, `Graubünden` |
| `ZE-Status` | str | 0 (0.0%) | 5 | `ausser Betrieb/reduzierter Betrieb`, `im Bau`, `im Normalbetrieb`, `im Umbau`, `stillgelegt` |
| `Funktion: Turbinieren` | str | 20 (2.67%) | 1 | `T` |
| `Funktion: Pumpen` | str | 705 (94.13%) | 1 | `P` |
| `QTurbine [m3/sec]` | float64 | 0 (0.0%) | 249 | 0.0 … 1500.0 (mean 40.42) |
| `Inst. Turbinenleistung` | float64 | 0 (0.0%) | 369 | 0.0 … 1285.0 (mean 24.43) |
| `("LTURBINE[MW]"/100)*"PROZ.ANTEILCH"` | float64 | 0 (0.0%) | 369 | 0.0 … 1285.0 (mean 23.23) |
| `Max. Leistung ab Generator` | float64 | 0 (0.0%) | 340 | 0.0 … 1260.0 (mean 23.63) |
| `("LGENERATOR[MW]"/100)*"PROZ.ANTEILCH"` | float64 | 0 (0.0%) | 341 | 0.0 … 1260.0 (mean 22.46) |
| `Prod. ohne Umwälzbetrieb - W.` | float64 | 0 (0.0%) | 365 | 0.0 … 1108.08 (mean 23.21) |
| `Prod. ohne Umwälzbetrieb - S.` | float64 | 0 (0.0%) | 434 | 0.0 … 995.02 (mean 32.36) |
| `Prod. ohne Umwälzbetrieb - J.` | float64 | 0 (0.0%) | 445 | 0.0 … 2103.1 (mean 55.57) |
| `("PROD.OHNEUMWÄLZBETRIEB-J."/100)*"PROZ.ANTEILCH"` | float64 | 0 (0.0%) | 443 | 0.0 … 2103.1 (mean 50.21) |
| `QPumpe [m3/sec]` | float64 | 0 (0.0%) | 40 | 0.0 … 360.0 (mean 1.27) |
| `Inst. Pumpenleistung` | float64 | 0 (0.0%) | 44 | 0.0 … 1000.0 (mean 5.34) |
| `Leistungsaufnahme Motoren` | float64 | 0 (0.0%) | 40 | 0.0 … 1000.0 (mean 5.31) |
| `Bedarf ohne Umwälzb. - W.` | float64 | 0 (0.0%) | 24 | 0.0 … 29.98 (mean 0.25) |
| `Bedarf ohne Umwälzb. - S.` | float64 | 0 (0.0%) | 29 | 0.0 … 210.6 (mean 1.02) |
| `Bedarf ohne Umwälzb. - J.` | float64 | 0 (0.0%) | 32 | 0.0 … 226.88 (mean 1.27) |
| `ZE-Erste Inbetriebnahme` | int64 | 0 (0.0%) | 159 | 1816 … 2025 (mean 1956.53) |
| `ZE-Letzte Inbetriebnahme` | float64 | 150 (20.03%) | 97 | 1915.0 … 2025.0 (mean 1985.93) |
| `ZE-Kote` | float64 | 0 (0.0%) | 693 | 200.0 … 2273.2 (mean 822.11) |
| `Proz. Anteil CH` | float64 | 0 (0.0%) | 13 | 0.0 … 100.0 (mean 97.94) |
| `Kantonsanteil: Kanton Name (1)` | str | 0 (0.0%) | 26 | `Graubünden`, `Graubünden`, `Graubünden` |
| `Kantonsanteil (1)` | float64 | 0 (0.0%) | 37 | 0.0 … 100.0 (mean 95.39) |
| `Kantonsanteil: Kanton Name (2)` | str | 711 (94.93%) | 14 | `Aargau`, `Appenzell I.Rh.`, `Basel-Landschaft`, `Freiburg`, `Graubünden`, … (+9) |
| `Kantonsanteil (2)` | float64 | 711 (94.93%) | 30 | 0.0 … 98.74 (mean 47.31) |
| `Kantonsanteil: Kanton Name (3)` | str | 745 (99.47%) | 4 | `St.Gallen`, `Tessin`, `Thurgau`, `Zug` |
| `Kantonsanteil (3)` | float64 | 745 (99.47%) | 4 | 9.55 … 54.0 (mean 27.36) |
| `Genutzte Gewässer - Name (1)` | str | 0 (0.0%) | 438 | `Aua da Milez`, `Lai da Curnera`, `Strem` |
| `Genutzte Gewässer - Name (2)` | str | 469 (62.62%) | 229 | `Aua da Val Giuf`, `Rein da Curnera`, `Rein da Curnera` |
| `Genutzte Gewässer - Name (3)` | str | 617 (82.38%) | 114 | `Rein da Nalps`, `Rein da Sumvitg`, `Quellen Cuolms da Runs` |
| `Genutzte Gewässer - Name (4)` | str | 657 (87.72%) | 80 | `Rein da Tuma`, `Vorderrhein`, `Ual da Siat` |
| `Genutzte Gewässer - Name (5)` | str | 693 (92.52%) | 48 | `Stausee Curnera`, `Stausee Zervreila`, `Lago di Lei` |
| `Genutzte Gewässer - Name (6)` | str | 713 (95.19%) | 32 | `Stausee Nalps`, `Valser Rhein`, `Madriserrhein` |
| `Genutzte Gewässer - Name (7)` | str | 724 (96.66%) | 22 | `Stausee Sta.Maria`, `Maleggabach`, `Speicher Gigerwald` |
| `Genutzte Gewässer - Name (8)` | str | 736 (98.26%) | 12 | `Nant de Drance, Triège`, `Niemetbach`, `Petit Hongrin`, `R. Giacobi`, `Reuse de Saleinaz`, … (+7) |
| `Genutzte Gewässer - Name (9)` | str | 737 (98.4%) | 11 | `Parebach`, `R. Passera`, `R. de Tompey`, `Reuse de Saleinaz`, `Tersolbach`, … (+6) |
| `Genutzte Gewässer - Name (10)` | str | 743 (99.2%) | 6 | `Pisciabach`, `R. Sella`, `R. des Champs`, `Torrent de Planeureuse`, `Torrent de Treutse Bô`, `Wildwüestibach` |
| `Genutzte Gewässer - Name (11)` | str | 744 (99.33%) | 5 | `R. des Plans`, `Reno di Lei`, `Torrent de Treutse-Bô`, `Torrent du Tour`, `Wolfisbach` |
| `Genutzte Gewässer - Name (12)` | str | 745 (99.47%) | 4 | `R. du Sepey`, `Stausee Sufers`, `Torrent du Tour`, `Triège-CFF` |
| `Ersatzenergie: Richtung (1)` | str | 664 (88.65%) | 2 | `A`, `B` |
| `Ersatzenergie: Partner (1)` | str | 664 (88.65%) | 72 | `Repower AG (Zentrale Waltensburg)`, `EWZ (Zentrale Rothenbrunnen EWZ)`, `RE (Zentrale Klosters)` |
| `Ersatzenergie: Richtung (2)` | str | 729 (97.33%) | 2 | `A`, `B` |
| `Ersatzenergie: Partner (2)` | str | 729 (97.33%) | 20 | `AET    (Diversi centrali)`, `BKW   (Centr. Aarberg,Hagneck,Kallnach)`, `ED (Zentrale Wyhlen)`, `FMO     (Centrale d'Orsières)`, `GKW        (Zentrale Neubrigg)`, … (+15) |
| `Ersatzenergie: Richtung (3)` | str | 738 (98.53%) | 2 | `A`, `B` |
| `Ersatzenergie: Partner (3)` | str | 738 (98.53%) | 11 | `Axpo Power AG (Zentrale Wildegg-Brugg)`, `ED (Zentrale Laufenburg)`, `ED (Zentrale Rheinfelden)`, `EdF (Zentrale Kembs)`, `Groupe E SA (Cen. Hauterive, Schiffenen)`, … (+6) |
| `Ersatzenergie: Richtung (4)` | str | 745 (99.47%) | 2 | `A`, `B` |
| `Ersatzenergie: Partner (4)` | str | 745 (99.47%) | 4 | `Axpo Power AG (Rüchlig-Dotierzentrale)`, `CFF      (Centrale Vernayaz)`, `EWM            (Zentr. Tobel)`, `FMV (Zentrale Chippis)` |
| `Ersatzenergie: Richtung (5)` | str | 748 (99.87%) | 1 | `A` |
| `Ersatzenergie: Partner (5)` | str | 748 (99.87%) | 1 | `Hydroelectra AG (Zentr. Mels (Halde))` |
| `Ersatzenergie :Richtung (6)` | str | 748 (99.87%) | 1 | `A` |
| `Ersatzenergie: Partner (6)` | str | 748 (99.87%) | 1 | `Weberei Walenstadt` |
| `Ersatzenergie: Richtung (7)` | float64 | 749 (100.0%) | 0 |  |
| `Ersatzenergie: Partner (7)` | float64 | 749 (100.0%) | 0 |  |
| `Ersatzenergie: Richtung (8)` | float64 | 749 (100.0%) | 0 |  |
| `Ersatzenergie: Partner (8)` | float64 | 749 (100.0%) | 0 |  |
| `Ersatzenergie: Richtung (9)` | float64 | 749 (100.0%) | 0 |  |
| `Ersatzenergie: Partner (9)` | float64 | 749 (100.0%) | 0 |  |
| `Ersatzenergie: Richtung (10)` | float64 | 749 (100.0%) | 0 |  |
| `Ersatzenergie: Partner (10)` | float64 | 749 (100.0%) | 0 |  |
| `Ersatzenergie: Richtung (11)` | float64 | 749 (100.0%) | 0 |  |
| `Ersatzenergie: Partner (11)` | float64 | 749 (100.0%) | 0 |  |
| `Ersatzenergie: Richtung (12)` | float64 | 749 (100.0%) | 0 |  |
| `Ersatzenergie: Partner (12)` | float64 | 749 (100.0%) | 0 |  |
| `Rechte - Name (1)` | str | 6 (0.8%) | 5 | `Andere Rechtsgrundlage`, `Bewilligung`, `Ehehaftes Recht`, `Konzession(en)`, `Verfügungsrecht` |
| `Rechte - Endjahr (1)` | float64 | 6 (0.8%) | 90 | 1998.0 … 9999.0 (mean 3244.15) |
| `Rechte - Name (2)` | str | 722 (96.4%) | 4 | `Andere Rechtsgrundlage`, `Bewilligung`, `Ehehaftes Recht`, `Konzession(en)` |
| `Rechte - Endjahr (2)` | float64 | 722 (96.4%) | 9 | 1999.0 … 9999.0 (mean 7642.70) |
| `Rechte - Name (3)` | str | 747 (99.73%) | 2 | `Andere Rechtsgrundlage`, `Ehehaftes Recht` |
| `Rechte - Endjahr (3)` | float64 | 747 (99.73%) | 1 | 9999.0 … 9999.0 (mean 9999.00) |
| `Rechte - Name (4)` | float64 | 749 (100.0%) | 0 |  |
| `Rechte - Endjahr (4)` | float64 | 749 (100.0%) | 0 |  |
| `Rechte - Name (5)` | float64 | 749 (100.0%) | 0 |  |
| `Rechte - Endjahr (5)` | float64 | 749 (100.0%) | 0 |  |
| `Rechte - Name (6)` | float64 | 749 (100.0%) | 0 |  |
| `Rechte - Endjahr (6)` | float64 | 749 (100.0%) | 0 |  |
| `Rechte - Name (7)` | float64 | 749 (100.0%) | 0 |  |
| `Rechte - Endjahr (7)` | float64 | 749 (100.0%) | 0 |  |
| `Rechte - Name (8)` | float64 | 749 (100.0%) | 0 |  |
| `Rechte - Endjahr (8)` | float64 | 749 (100.0%) | 0 |  |
| `Rechte - Name (9)` | float64 | 749 (100.0%) | 0 |  |
| `Rechte - Endjahr (9)` | float64 | 749 (100.0%) | 0 |  |
| `Rechte - Name (10)` | float64 | 749 (100.0%) | 0 |  |
| `Rechte - Endjahr (10)` | float64 | 749 (100.0%) | 0 |  |
| `Bemerkung (1)` | str | 503 (67.16%) | 192 | `- Zentralen Sedrun 1 und Sedrun 2 in einer Kaverne`, `- Zentralen Sedrun 1 und Sedrun 2 in einer Kaverne`, `- Kote Maschinensaalboden bezieht sich auf die Höhe der Turbinenachse` |
| `Bemerkung (2)` | str | 624 (83.31%) | 93 | ` `, `- Laufkraftwerkgruppe`, `                                   ` |
| `Bemerkung (3)` | str | 678 (90.52%) | 55 | ` `, `Sanierung Gigerwald-Stausee eingeplant für Winter 24/25`, `Die neue 80 jährige sollte dieses Jahr eigentlich eintreffen (bis 2098)` |
| `Bemerkung (4)` | str | 699 (93.32%) | 43 | `			`, `- DKW Staumauer Mapragg mit in Planung        `, ` ` |
| `Bemerkung (5)` | str | 711 (94.93%) | 32 | ` `, `	Winter:	1,4 GWh`, `	in den Räterichsbodensee  (gepumptes Laufwasser)` |
| `Bemerkung (6)` | str | 723 (96.53%) | 23 | `	Sommer:	1,0 GWh`, `- Zentralen Handeck 3 (Isogyre) und Handeck 3 (Pumpzentrale) in einer Kaverne`, `                   ` |
| `Bemerkung (7)` | str | 729 (97.33%) | 13 | `	Jahr:	2,4 GWh`, ` `, `      `, `               			Puissance max.disponible        Gr.1 	=  48.5 MW                    `, `                  `, … (+8) |
| `Bemerkung (8)` | str | 732 (97.73%) | 12 | ` `, `     `, `      `, `                         `, `                                                  `, … (+7) |
| `Bemerkung (9)` | str | 733 (97.86%) | 12 | ` `, `      `, `                         `, `                         	`, `                          `, … (+7) |
| `Bemerkung (10)` | str | 737 (98.4%) | 10 | ` `, `       `, `         `, `                          `, `                                   `, … (+5) |
| `ZE-Koordinaten unscharf (Ost)` | int64 | 0 (0.0%) | 686 | 1141340 … 2844830 (mean 2663423.56) |
| `ZE-Koordinaten unscharf (Nord)` | int64 | 0 (0.0%) | 683 | 1081630 … 2643900 (mean 1182119.79) |
| `Internationales KW` | str | 715 (95.46%) | 1 | `Ja` |
| `Nutzungstyp (Code)` | str | 646 (86.25%) | 7 | `A`, `B`, `O`, `T`, `U`, `V`, `W` |
| `Nutzungstyp (Beschreibung)` | str | 646 (86.25%) | 7 | `Abwasser Kraftwerk`, `Dotierwasser Kraftwerk`, `Kraftwerk mit Beschneiungsanlage`, `Trinkwasser Kraftwerk`, `Tunnelwasser Kraftwerk`, `Wässerwasser Kraftwerk`, `Wässerwasser und Tunnelwasser Kraftwerk` |
| `Nutz.-Untertyp (Code)` | str | 3 (0.4%) | 6 | `A`, `F`, `K`, `N`, `P`, `S` |
| `Nutz.-Untertyp (Beschreibung)` | str | 3 (0.4%) | 11 | `Ausleitkraftwerk`, `Flusskraftwerk (reines Stauwerk)`, `Kanalkraftwerk (Ausleitkanal mit reinem Stauwerk)`, `Nebennutz. KW (Abw.,TW. Dotier., Beschn.,Lock)`, `Reines Umwälzwerk (Speicher u. - Speicher o.)`, … (+6) |
| `Maxim. Bruttofallhöhe [m]` | float64 | 0 (0.0%) | 574 | 0.0 … 1883.0 (mean 252.81) |
| `Minim. Bruttofallhöhe [m]` | float64 | 0 (0.0%) | 284 | 0.0 … 1754.0 (mean 117.80) |
| `Maxim. Nettofallhöhe [m]` | float64 | 0 (0.0%) | 415 | 0.0 … 4700.0 (mean 172.90) |
| `Minim. Nettofallhöhe [m]` | float64 | 0 (0.0%) | 217 | 0.0 … 1633.0 (mean 87.03) |
| `Maxim. Bruttoförderhöhe [m]` | float64 | 0 (0.0%) | 32 | 0.0 … 1010.0 (mean 17.51) |
| `Minim. Bruttoförderhöhe [m]` | float64 | 0 (0.0%) | 27 | 0.0 … 831.0 (mean 11.63) |
| `Maxim. Nettoförderhöhe [m]` | float64 | 0 (0.0%) | 33 | 0.0 … 1005.0 (mean 16.25) |
| `Minim. Nettoförderhöhe [m]` | float64 | 0 (0.0%) | 29 | 0.0 … 808.0 (mean 11.45) |
