"""
ENTSO-E-Konfiguration für Strompreise CH.

Day-Ahead-Spotpreis ist der wichtige Preisindikator: was kostet 1 MWh Strom
für den nächsten Tag, ausgehandelt am Spotmarkt am Vortag um 12:00 Uhr.

Die ENTSO-E Transparency Platform liefert diese Daten ab Anfang 2015 für CH.
Document Type A44 (Price Document) im API-Endpunkt.

Für Erweiterungen: Bidding Zones der Nachbarländer können bei Bedarf
ergänzt werden (DE-LU, AT, FR, IT-North).
"""

# Bidding Zone für CH (Schweiz)
# Ist eine ENTSO-E EIC-Codierung (Energy Identification Code)
ENTSOE_BIDDING_ZONE_CH = "10YCH-SWISSGRIDZ"

# Document Type für Day-Ahead-Spotpreise
DOCUMENT_TYPE_PRICE = "A44"

# API-Basis
ENTSOE_API_BASE = "https://web-api.tp.entsoe.eu/api"

# Default-Zeitraum: ab 2017 (synchron zu Open-Meteo)
DEFAULT_START_YEAR = 2017