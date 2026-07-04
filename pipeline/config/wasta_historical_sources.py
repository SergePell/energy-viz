"""
WASTA-Historisch-Quellen-Konfiguration.

Hardcodiert pro Jahr eine URL — BFE nutzt Publikations-IDs, die nicht
mustertreu generiert werden. URLs stammen von:
https://www.bfe.admin.ch/bfe/de/home/versorgung/digitalisierung-und-geoinformation/geoinformation/geodaten/wasser/statistik-der-wasserkraftanlagen.html

Die Jahres-Zuordnung basiert auf der Annahme "neueste Publikations-ID = neuestes Jahr".
Falls beim ersten Profilieren auffällt, dass ein Jahr falsch zugeordnet ist,
hier korrigieren und Files erneut ziehen.
"""

WASTA_HISTORICAL_FILES = {
    2026: {
        "url": "https://pubdb.bfe.admin.ch/de/publication/download/12596",
        "extension": ".zip",
    },
    2025: {
        "url": "https://pubdb.bfe.admin.ch/de/publication/download/12108",
        "extension": ".zip",
    },
    2024: {
        "url": "https://pubdb.bfe.admin.ch/de/publication/download/11719",
        "extension": ".zip",
    },
    2023: {
        "url": "https://pubdb.bfe.admin.ch/de/publication/download/11372",
        "extension": ".zip",
    },
    2022: {
        "url": "https://pubdb.bfe.admin.ch/de/publication/download/10894",
        "extension": ".zip",
    },
    2021: {
        "url": "https://pubdb.bfe.admin.ch/de/publication/download/10471",
        "extension": ".zip",
    },
    2020: {
        "url": "https://pubdb.bfe.admin.ch/de/publication/download/10085",
        "extension": ".zip",
    },
    2019: {
        "url": "https://pubdb.bfe.admin.ch/de/publication/download/9690",
        "extension": ".zip",
    },
    2018: {
        "url": "https://pubdb.bfe.admin.ch/de/publication/download/9339",
        "extension": ".zip",
    },
    2017: {
        "url": "https://pubdb.bfe.admin.ch/de/publication/download/8632",
        "extension": ".zip",
    },
    2016: {
        "url": "https://pubdb.bfe.admin.ch/de/publication/download/8288",
        "extension": ".zip",
    },
    2015: {
        "url": "https://pubdb.bfe.admin.ch/de/publication/download/7844",
        "extension": ".zip",
    },
    2014: {
        "url": "https://pubdb.bfe.admin.ch/de/publication/download/7431",
        "extension": ".zip",
    },
}