"""
Wetterstations-Konfiguration für Open-Meteo.

18 Stationen, 1:1-Mapping zu den 18 räumlichen Einheiten der Swissgrid-Daten:
- 11 Einzelkantone: AG, FR, GL, GR, LU, NE, SO, SG, TI, TG, VS
- 7 Gruppen: AI/AR, BL/BS, BE/JU, SZ/ZG, OW/NW/UR, GE/VD, SH/ZH

Pro Einheit ist eine repräsentative Koordinate (typischerweise Hauptort)
gewählt. Limitation: bei topografisch heterogenen Einheiten (insb. Alpen-
Kantone wie GR, VS, TI) repräsentiert eine Koordinate die ganze Region nur
unzureichend. Dies ist im Decision-Log dokumentiert.

Koordinaten in WGS84 (EPSG:4326), Format: (Längengrad, Breitengrad).
"""

WEATHER_STATIONS = {
    # Einzelkantone
    "CH-AG": {
        "name": "Aarau",
        "longitude": 8.0444,
        "latitude": 47.3924,
        "altitude_m": 384,
        "swissgrid_einheit": "CH-AG",
    },
    "CH-FR": {
        "name": "Fribourg",
        "longitude": 7.1620,
        "latitude": 46.8023,
        "altitude_m": 610,
        "swissgrid_einheit": "CH-FR",
    },
    "CH-GL": {
        "name": "Glarus",
        "longitude": 9.0680,
        "latitude": 47.0408,
        "altitude_m": 470,
        "swissgrid_einheit": "CH-GL",
    },
    "CH-GR": {
        "name": "Chur",
        "longitude": 9.5320,
        "latitude": 46.8508,
        "altitude_m": 593,
        "swissgrid_einheit": "CH-GR",
    },
    "CH-LU": {
        "name": "Luzern",
        "longitude": 8.3093,
        "latitude": 47.0502,
        "altitude_m": 436,
        "swissgrid_einheit": "CH-LU",
    },
    "CH-NE": {
        "name": "Neuchâtel",
        "longitude": 6.9293,
        "latitude": 46.9899,
        "altitude_m": 430,
        "swissgrid_einheit": "CH-NE",
    },
    "CH-SO": {
        "name": "Solothurn",
        "longitude": 7.5380,
        "latitude": 47.2080,
        "altitude_m": 432,
        "swissgrid_einheit": "CH-SO",
    },
    "CH-SG": {
        "name": "St. Gallen",
        "longitude": 9.3768,
        "latitude": 47.4245,
        "altitude_m": 670,
        "swissgrid_einheit": "CH-SG",
    },
    "CH-TI": {
        "name": "Lugano",
        "longitude": 8.9520,
        "latitude": 46.0037,
        "altitude_m": 273,
        "swissgrid_einheit": "CH-TI",
    },
    "CH-TG": {
        "name": "Frauenfeld",
        "longitude": 8.8979,
        "latitude": 47.5580,
        "altitude_m": 405,
        "swissgrid_einheit": "CH-TG",
    },
    "CH-VS": {
        "name": "Sion",
        "longitude": 7.3597,
        "latitude": 46.2270,
        "altitude_m": 491,
        "swissgrid_einheit": "CH-VS",
    },
    # Gruppen
    "CH-AI_AR": {
        "name": "Appenzell",
        "longitude": 9.4099,
        "latitude": 47.3308,
        "altitude_m": 780,
        "swissgrid_einheit": "CH-AI_AR",
    },
    "CH-BL_BS": {
        "name": "Basel",
        "longitude": 7.5886,
        "latitude": 47.5596,
        "altitude_m": 261,
        "swissgrid_einheit": "CH-BL_BS",
    },
    "CH-BE_JU": {
        "name": "Bern",
        "longitude": 7.4474,
        "latitude": 46.9480,
        "altitude_m": 540,
        "swissgrid_einheit": "CH-BE_JU",
    },
    "CH-SZ_ZG": {
        "name": "Zug",
        "longitude": 8.5151,
        "latitude": 47.1662,
        "altitude_m": 425,
        "swissgrid_einheit": "CH-SZ_ZG",
    },
    "CH-OW_NW_UR": {
        "name": "Altdorf",
        "longitude": 8.6442,
        "latitude": 46.8800,
        "altitude_m": 458,
        "swissgrid_einheit": "CH-OW_NW_UR",
    },
    "CH-GE_VD": {
        "name": "Lausanne",
        "longitude": 6.6323,
        "latitude": 46.5197,
        "altitude_m": 495,
        "swissgrid_einheit": "CH-GE_VD",
    },
    "CH-SH_ZH": {
        "name": "Zürich",
        "longitude": 8.5417,
        "latitude": 47.3769,
        "altitude_m": 408,
        "swissgrid_einheit": "CH-SH_ZH",
    },
}


# Open-Meteo Variablen
# Liste in API-Format: kommasepariert übergeben in &hourly=
WEATHER_VARIABLES = [
    "temperature_2m",         # Temperatur in 2m Höhe (°C)
    "shortwave_radiation",    # Globalstrahlung (W/m²)
    "direct_radiation",       # Direkte Strahlung (W/m²)
    "wind_speed_10m",         # Windgeschwindigkeit in 10m Höhe (m/s)
    "cloud_cover",            # Bewölkung (%)
    "precipitation",          # Niederschlag (mm)
]