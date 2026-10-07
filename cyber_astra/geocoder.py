"""Geocoding: location string → lat, lon, timezone, display name.

Uses Nominatim (OpenStreetMap) + timezonefinder. Results are cached in
memory for the session. When offline, callers may supply coordinates
manually via CLI flags.
"""

from __future__ import annotations

from functools import lru_cache

from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder


@lru_cache(maxsize=64)
def geocode(location_str: str) -> dict:
    geolocator = Nominatim(user_agent="cyber_astra_v2", timeout=10)
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
