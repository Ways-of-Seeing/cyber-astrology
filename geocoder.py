"""
Geocoding: location string → lat, lon, timezone, display name
"""

from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder


def geocode(location_str: str) -> dict:
    geolocator = Nominatim(user_agent="cyber_astrology_v1", timeout=10)
    location = geolocator.geocode(location_str, language="pt")
    if location is None:
        location = geolocator.geocode(location_str, language="en")
    if location is None:
        raise ValueError(f"Localização não encontrada: '{location_str}'")

    tf = TimezoneFinder()
    timezone = tf.timezone_at(lat=location.latitude, lng=location.longitude)
    if timezone is None:
        timezone = "UTC"

    return {
        "display_name": location.address,
        "lat": location.latitude,
        "lon": location.longitude,
        "timezone": timezone,
        "raw": location.raw,
    }
