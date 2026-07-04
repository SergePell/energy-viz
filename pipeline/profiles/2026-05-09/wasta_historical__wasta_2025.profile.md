# Profil: wasta_2025.xlsx

**Erstellt:** 2026-05-09T18:43:49
**Pfad:** `C:\Users\pelle\SynologyDrive\Docs\Studium\FHGR\Masterthesis\energy-viz\pipeline\raw\snapshots\2026-05-09\wasta_historical\wasta_2025.xlsx`
**Format:** XLSX
**SHA-256:** `1c9d5005e04f6084d0e97913f93fc4babb87a0e2405224fc0f2c30bd8b425065`
**Quelle:** https://pubdb.bfe.admin.ch/de/publication/download/12108
**Grösse:** 253.5 KB

**Sheets:** WASTA 01.01.2025

## Sheet: `WASTA 01.01.2025`

**Zeilen:** 752
**Spalten:** 88

| Name | Typ | Nulls | Unique | Wertebereich / Beispiele |
|------|-----|-------|--------|--------------------------|
| `ZE-Nr` | int64 | 0 (0.0%) | 752 | 100100 … 900200 (mean 352624.81) |
| `ZE-Name` | str | 0 (0.0%) | 751 | `Val Giuv`, `Curnera Druckminderer`, `Val Strem` |
| `WKA-Name` | str | 0 (0.0%) | 684 | `Val Giuv`, `Curnera`, `Val Strem` |
| `WKA-Typ` | str | 0 (0.0%) | 6 | `D`, `L`, `P`, `PS`, `S`, `U` |
| `ZE-Standort` | str | 0 (0.0%) | 579 | `Rueras`, `Schiebekammer Curnera`, `Sedrun` |
| `ZE-Kanton (Land)` | str | 0 (0.0%) | 28 | `Graubünden`, `Graubünden`, `Graubünden` |
| `ZE-Status - beachten!` | str | 0 (0.0%) | 6 | `ausser Betrieb`, `ausser Betrieb/reduzierter Betrieb`, `im Bau`, `im Normalbetrieb`, `im Umbau`, `stillgelegt` |
| `Funktion: Turbinieren` | str | 20 (2.66%) | 1 | `T` |
| `Funktion: Pumpen` | str | 709 (94.28%) | 1 | `P` |
| `QTurbine [m3/s]` | float64 | 0 (0.0%) | 250 | 0.0 … 1500.0 (mean 40.29) |
| `Inst. Turbinenleistung [MW]` | float64 | 0 (0.0%) | 362 | 0.0 … 1269.0 (mean 24.30) |
| `("LTURBINE[MW]"/100)*"PROZ.ANTEILCH"` | float64 | 0 (0.0%) | 364 | 0.0 … 1269.0 (mean 23.09) |
| `Max. Leistung ab Generator [MW]` | float64 | 0 (0.0%) | 365 | 0.0 … 1200.0 (mean 23.64) |
| `("LGENERATOR[MW]"/100)*"PROZ.ANTEILCH"` | float64 | 0 (0.0%) | 364 | 0.0 … 1200.0 (mean 22.45) |
| `Prod. ohne Umwälzb. - Winter [GWh]` | float64 | 0 (0.0%) | 387 | 0.0 … 1108.08 (mean 23.21) |
| `Prod. ohne Umwälzb. - Sommer [MW]` | float64 | 0 (0.0%) | 439 | 0.0 … 995.02 (mean 32.47) |
| `Prod. ohne Umwälzb. - Jahr [GWh]` | float64 | 0 (0.0%) | 454 | 0.0 … 2103.1 (mean 55.67) |
| `("PROD.OHNEUMWÄLZB.-J."/100)*"PROZ.ANTEILCH"` | float64 | 0 (0.0%) | 449 | 0.0 … 2103.1 (mean 50.32) |
| `QPumpe [m3/s]` | float64 | 0 (0.0%) | 41 | 0.0 … 360.0 (mean 1.26) |
| `Inst. Pumpenleistung [MW]` | float64 | 0 (0.0%) | 44 | 0.0 … 1000.0 (mean 5.40) |
| `Max. Leistungsaufnahme Motoren [MW]` | float64 | 0 (0.0%) | 40 | 0.0 … 1000.0 (mean 5.35) |
| `Bedarf ohne Umwälzb. - Winter [GWh]` | float64 | 0 (0.0%) | 25 | 0.0 … 31.0 (mean 0.20) |
| `Bedarf ohne Umwälzb. - Sommer [GWh]` | float64 | 0 (0.0%) | 31 | 0.0 … 210.6 (mean 1.03) |
| `Bedarf ohne Umwälzb. - Jahr [GWh]` | float64 | 0 (0.0%) | 32 | 0.0 … 226.9 (mean 1.23) |
| `ZE-Erste Inbetriebnahme` | int64 | 0 (0.0%) | 160 | 1816 … 2026 (mean 1956.79) |
| `ZE-Letzte Inbetriebnahme` | float64 | 154 (20.48%) | 97 | 1923.0 … 2025.0 (mean 1987.68) |
| `ZE-Kote [m.ü.M.]` | float64 | 0 (0.0%) | 702 | 193.0 … 2577.0 (mean 820.79) |
| `Proz. Anteil CH [%]` | float64 | 0 (0.0%) | 13 | 0.0 … 100.0 (mean 97.94) |
| `Kantonsanteil: Kanton (1)` | str | 0 (0.0%) | 32 | `Graubünden`, `Graubünden`, `Graubünden` |
| `Kantonsanteil (1) [%]` | float64 | 0 (0.0%) | 36 | 0.0 … 100.0 (mean 95.40) |
| `Kantonsanteil: Kanton (2)` | str | 714 (94.95%) | 15 | `Aargau`, `Appenzell I.Rh.`, `Basel-Landschaft`, `Fribourg`, `Grigioni`, … (+10) |
| `Kantonsanteil (2) [%]` | float64 | 714 (94.95%) | 28 | 0.0 … 98.74 (mean 47.29) |
| `Kantonsanteil: Kanton (3)` | str | 748 (99.47%) | 4 | `St.Gallen`, `Thurgau`, `Ticino`, `Zug` |
| `Kantonsanteil (3) [%]` | float64 | 748 (99.47%) | 4 | 9.55 … 54.0 (mean 28.29) |
| `Genutzte Gewässer - Name (1)` | str | 0 (0.0%) | 440 | `Aua da Milez`, `Lai da Curnera`, `Strem` |
| `Genutzte Gewässer - Name (2)` | str | 465 (61.84%) | 236 | `Aua da Val Giuv`, `Rein da Curnera`, `Rein da Curnera` |
| `Genutzte Gewässer - Name (3)` | str | 613 (81.52%) | 122 | `Rein da Nalps`, `Rein da Sumvitg`, `Quellen Cuolms da Runs` |
| `Genutzte Gewässer - Name (4)` | str | 657 (87.37%) | 85 | `Rein da Tuma`, `Vorderrhein`, `Ual da Siat` |
| `Genutzte Gewässer - Name (5)` | str | 694 (92.29%) | 51 | `Stausee Curnera`, `Stausee Zervreila`, `Lago di Lei` |
| `Genutzte Gewässer - Name (6)` | str | 715 (95.08%) | 34 | `Stausee Nalps`, `Valser Rhein`, `Madriserrhein` |
| `Genutzte Gewässer - Name (7)` | str | 726 (96.54%) | 23 | `Stausee Sta.Maria`, `Maleggabach`, `Valtschielbach` |
| `Genutzte Gewässer - Name (8)` | str | 738 (98.14%) | 13 | `Nant de Drance, Triège`, `Niemetbach`, `Petit Hongrin`, `R. Giacobi `, `Reuse de Saleinaz`, … (+8) |
| `Genutzte Gewässer - Name (9)` | str | 740 (98.4%) | 11 | `Parebach`, `R. Passera`, `R. de Tompey`, `Reuse de Saleinaz`, `Tersolbach`, … (+6) |
| `Genutzte Gewässer - Name (10)` | str | 746 (99.2%) | 6 | `Pisciabach`, `R. Sella`, `R. des Champs`, `Torrent de Planeureuse`, `Torrent de Treutse Bô`, `Wildwüestibach` |
| `Genutzte Gewässer - Name (11)` | str | 747 (99.34%) | 5 | `R. des Plans`, `Reno di Lei`, `Torrent de Treutse-Bô`, `Torrent du Tour`, `Wolfisbach` |
| `Genutzte Gewässer - Name (12)` | str | 748 (99.47%) | 4 | `R. du Sepey`, `Stausee Sufers`, `Torrent du Tour`, `Triège-CFF` |
| `Ersatzenergie: Richtung (1)` | str | 667 (88.7%) | 2 | `A`, `B` |
| `Ersatzenergie: Partner (1)` | str | 667 (88.7%) | 71 | `Repower AG (Zentrale Waltensburg)`, `EWZ (Zentrale Rothenbrunnen EWZ)`, `RE (Zentrale Klosters)` |
| `Ersatzenergie: Richtung (2)` | str | 732 (97.34%) | 2 | `A`, `B` |
| `Ersatzenergie: Partner (2)` | str | 732 (97.34%) | 20 | `AET (Diversi centrali)`, `BKW (Centr. Aarberg,Hagneck,Kallnach)`, `ED (Zentrale Wyhlen)`, `FMO (Centrale d'Orsières)`, `GKW (Zentrale Neubrigg)`, … (+15) |
| `Ersatzenergie: Richtung (3)` | str | 741 (98.54%) | 2 | `A`, `B` |
| `Ersatzenergie: Partner (3)` | str | 741 (98.54%) | 10 | `Axpo Power AG (Zentrale Wildegg-Brugg)`, `ED (Zentrale Laufenburg)`, `ED (Zentrale Rheinfelden)`, `EdF (Zentrale Kembs)`, `Groupe E SA (Cen. Hauterive, Schiffenen)`, … (+5) |
| `Ersatzenergie: Richtung (4)` | str | 748 (99.47%) | 2 | `A`, `B` |
| `Ersatzenergie: Partner (4)` | str | 748 (99.47%) | 4 | `Axpo Power AG (Rüchlig-Dotierzentrale)`, `CFF (Centrale Vernayaz)`, `EWM (Zentr. Tobel)`, `FMV (Zentrale Chippis)` |
| `Ersatzenergie: Richtung (5)` | str | 751 (99.87%) | 1 | `A` |
| `Ersatzenergie: Partner (5)` | str | 751 (99.87%) | 1 | `Hydroelectra AG (Zentr. Mels Halde)` |
| `Ersatzenergie :Richtung (6)` | str | 751 (99.87%) | 1 | `A` |
| `Ersatzenergie: Partner (6)` | str | 751 (99.87%) | 1 | `Weberei Walenstadt` |
| `Rechte - Name (1)` | str | 0 (0.0%) | 14 | `Andere Rechtsgrundlage`, `Bewilligung`, `Ehehaftes Recht`, `Konzession(en)`, `Verfügungsrecht`, … (+9) |
| `Rechte - Endjahr (1)` | int64 | 0 (0.0%) | 91 | 1999 … 9999 (mean 3083.27) |
| `Rechte - Name (2)` | str | 737 (98.01%) | 5 | `Ehehaftes Recht`, `Konzession(en)`, `ancien droit d'eau`, `antico diritto d'acqua`, `concession(s)` |
| `Rechte - Endjahr (2)` | float64 | 737 (98.01%) | 4 | 2030.0 … 9999.0 (mean 7874.60) |
| `Rechte - Name (3)` | str | 751 (99.87%) | 1 | `Ehehaftes Recht` |
| `Rechte - Endjahr (3)` | float64 | 751 (99.87%) | 1 | 9999.0 … 9999.0 (mean 9999.00) |
| `Bemerkung (1)` | str | 299 (39.76%) | 225 | `KEV geförderte Anlage`, `KEV geförderte Anlage`, `KEV geförderte Anlage` |
| `Bemerkung (2)` | str | 577 (76.73%) | 110 | `Arbeiten: Sanierungen an Kaverne und Wasserfassung, Modernisierung der Schutz- und Steuerungsanlagen`, `Sanierungsarbeiten 2024: Maschinen revidiert, Schutz- und Steuerungsanlagen auf den neuesten Stand gebracht`, `KEV geförderte Anlage` |
| `Bemerkung (3)` | str | 677 (90.03%) | 47 | `KEV geförderte Anlage`, `                                   `, `KEV geförderte Anlage` |
| `Bemerkung (4)` | str | 711 (94.55%) | 29 | `Im 2026 wird die Anlage voraussichtlich ausser Betrieb gehen!`, `DKW Staumauer Mapragg mit in Planung        `, ` ` |
| `Bemerkung (5)` | str | 723 (96.14%) | 21 | ` `, `Dieses wird in den Räterichsbodensee geleitet (gepumptes Laufwasser oder Umwälbeztrieb)`, `       ` |
| `Bemerkung (6)` | str | 738 (98.14%) | 10 | ` `, `                   `, `                            `, `                                     `, `                                              `, … (+5) |
| `Bemerkung (7)` | str | 742 (98.67%) | 6 | ` `, `      `, `                  `, `Ersatz der drei ältesten Bahnstromgeneratoren von 1937`, `Puissance max.disponible Gr.1 =  48.5 MW                    `, `ab 2023 wieder in Betrieb` |
| `Bemerkung (8)` | str | 744 (98.94%) | 6 | ` `, `     `, `                         `, `                                                  `, `                                                    `, `Les équipements haute chute, basse chute et Centrale de pompage de Châtelard-Vallorcine se trouvent dans le même bâtiment et leur` |
| `Bemerkung (9)` | str | 745 (99.07%) | 6 | ` `, `      `, `         `, `                          `, `                                         `, `fonctionnement est étroitement lié` |
| `ZE-Koordinaten (Ost)` | int64 | 0 (0.0%) | 721 | 2486880 … 2844830 (mean 2667230.02) |
| `ZE-Koordinaten (Nord)` | int64 | 0 (0.0%) | 722 | 1083247 … 1283470 (mean 1178193.39) |
| `Internationales KW` | str | 718 (95.48%) | 4 | `A`, `D`, `F`, `I` |
| `Nutzungstyp (Code)` | str | 646 (85.9%) | 7 | `A`, `B`, `O`, `T`, `U`, `V`, `W` |
| `Nutzungstyp (Beschreibung)` | str | 646 (85.9%) | 13 | `Abwasser Kraftwerk`, `Dotierwasser Kraftwerk`, `Kraftwerk mit Beschneiungsanlage`, `Trinkwasser Kraftwerk`, `Tunnelwasser Kraftwerk`, … (+8) |
| `Nutz.-Untertyp (Code)` | str | 3 (0.4%) | 6 | `A`, `F`, `K`, `N`, `P`, `S` |
| `Nutz.-Untertyp (Beschreibung)` | str | 3 (0.4%) | 11 | `Ausleitkraftwerk`, `Flusskraftwerk (reines Stauwerk)`, `Kanalkraftwerk (Ausleitkanal mit reinem Stauwerk)`, `Nebennutzung (Abwasser, Trinkwasser, Dotierung, Beschneiung, Lockstrom)`, `Reines Umwälzwerk (Speicher u. - Speicher o.)`, … (+6) |
| `Max. Bruttofallhöhe [m]` | float64 | 0 (0.0%) | 597 | 0.0 … 1883.0 (mean 264.37) |
| `Min. Bruttofallhöhe [m]` | float64 | 0 (0.0%) | 351 | 0.0 … 1754.0 (mean 144.64) |
| `Max. Nettofallhöhe [m]` | float64 | 0 (0.0%) | 427 | 0.0 … 4700.0 (mean 174.33) |
| `Min. Nettofallhöhe [m]` | float64 | 0 (0.0%) | 227 | 0.0 … 1633.0 (mean 90.93) |
| `Max. Bruttoförderhöhe [m]` | float64 | 0 (0.0%) | 33 | 0.0 … 1010.0 (mean 17.48) |
| `Min. Bruttoförderhöhe [m]` | float64 | 0 (0.0%) | 28 | 0.0 … 831.0 (mean 12.08) |
| `Max. Nettoförderhöhe [m]` | float64 | 0 (0.0%) | 33 | 0.0 … 1005.0 (mean 16.18) |
| `Min. Nettoförderhöhe [m]` | float64 | 0 (0.0%) | 29 | 0.0 … 808.0 (mean 11.38) |
