"""
Swissgrid-Quellen-Konfiguration.

Hardcodiert pro Jahr eine URL — Swissgrid nutzt JCR-UUIDs, die nicht
mustertreu generiert werden. Bei einem neuen Jahr (2027 etc.) den Link
manuell von https://www.swissgrid.ch/de/home/customers/topics/energy-data-ch.html
kopieren und ergänzen.

Format-Wechsel: Bis 2019 .xls, ab 2020 .xlsx.
"""

SWISSGRID_FILES = {
    2009: {
        "url": "https://www.swissgrid.ch/dam/jcr:4f32b90b-12d9-43fe-a8d9-7a4192a52ac3/EnergieUebersichtCH-2009.xls",
        "extension": ".xls",
    },
    2010: {
        "url": "https://www.swissgrid.ch/dam/jcr:dcf03a4a-ff98-4974-911a-50c77e51699e/EnergieUebersichtCH-2010.xls",
        "extension": ".xls",
    },
    2011: {
        "url": "https://www.swissgrid.ch/dam/jcr:6305d790-179a-4cb7-99c4-b9e96d427bea/EnergieUebersichtCH-2011.xls",
        "extension": ".xls",
    },
    2012: {
        "url": "https://www.swissgrid.ch/dam/jcr:cc1f9ce9-3eca-4d55-8236-e43d5105699f/EnergieUebersichtCH-2012.xls",
        "extension": ".xls",
    },
    2013: {
        "url": "https://www.swissgrid.ch/dam/jcr:bd42b565-13ba-4bb6-b038-4b40eefea226/EnergieUebersichtCH-2013.xls",
        "extension": ".xls",
    },
    2014: {
        "url": "https://www.swissgrid.ch/dam/jcr:e4760091-5fb1-4654-9623-341e40969193/EnergieUebersichtCH-2014.xls",
        "extension": ".xls",
    },
    2015: {
        "url": "https://www.swissgrid.ch/dam/jcr:7a201a6b-02cb-456e-ac9b-7dcdd033f592/EnergieUebersichtCH-2015.xls",
        "extension": ".xls",
    },
    2016: {
        "url": "https://www.swissgrid.ch/dam/jcr:7d2a26a1-26a4-41de-8920-be0d8b8b7c4f/EnergieUebersichtCH-2016.xls",
        "extension": ".xls",
    },
    2017: {
        "url": "https://www.swissgrid.ch/dam/jcr:9bcd738b-9444-4476-b295-8e29faaac462/EnergieUebersichtCH-2017.xls",
        "extension": ".xls",
    },
    2018: {
        "url": "https://www.swissgrid.ch/dam/jcr:1f3dadea-e71d-44f8-b845-abc335199c29/EnergieUebersichtCH-2018.xls",
        "extension": ".xls",
    },
    2019: {
        "url": "https://www.swissgrid.ch/dam/jcr:d8e15a7e-6575-46c3-b46d-f2ddd4a6b890/EnergieUebersichtCH-2019.xls",
        "extension": ".xls",
    },
    2020: {
        "url": "https://www.swissgrid.ch/dam/jcr:a6deeecb-74e8-4d67-a8ad-8c53c9dfbdd3/EnergieUebersichtCH-2020.xlsx",
        "extension": ".xlsx",
    },
    2021: {
        "url": "https://www.swissgrid.ch/dam/jcr:26fa6b22-5e81-44eb-abbd-4280c59c3697/EnergieUebersichtCH-2021.xlsx",
        "extension": ".xlsx",
    },
    2022: {
        "url": "https://www.swissgrid.ch/dam/jcr:e3af783a-6c00-40d9-bb3e-a630fb492dfb/EnergieUebersichtCH-2022.xlsx",
        "extension": ".xlsx",
    },
    2023: {
        "url": "https://www.swissgrid.ch/dam/jcr:32576046-3686-4a62-bc32-9b55a89a2142/EnergieUebersichtCH-2023.xlsx",
        "extension": ".xlsx",
    },
    2024: {
        "url": "https://www.swissgrid.ch/dam/jcr:4d4ca899-395d-4d3d-9958-5ace16ecbfbf/EnergieUebersichtCH-2024.xlsx",
        "extension": ".xlsx",
    },
    2025: {
        "url": "https://www.swissgrid.ch/dam/jcr:bbbbadc6-3656-4dfe-b81e-bbb9ad01be79/EnergieUebersichtCH-2025.xlsx",
        "extension": ".xlsx",
    },
    2026: {
        "url": "https://www.swissgrid.ch/dam/jcr:805e525c-44fe-4701-a227-6144193257ac/EnergieUebersichtCH-2026.xlsx",
        "extension": ".xlsx",
    },
}
