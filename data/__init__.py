# coding: utf-8
"""
Merge all interpretation dicts into a single PLANET_IN_SIGN lookup.
"""

from .planet_signs import PLANET_IN_SIGN as _PS
from .planets_mercury_venus import MERCURY_VENUS as _MV
from .planets_mars_jupiter_saturn import MARS_JUPITER_SATURN as _MJS
from .planets_outer import OUTER_PLANETS as _OP
from .houses import HOUSES

PLANET_IN_SIGN: dict = {}
PLANET_IN_SIGN.update(_PS)
PLANET_IN_SIGN.update(_MV)
PLANET_IN_SIGN.update(_MJS)
PLANET_IN_SIGN.update(_OP)


def get_planet_sign(planet_key: str, sign_key: str, lang: str = "pt") -> dict | None:
    """Return interpretation dict for planet+sign in given language."""
    entry = PLANET_IN_SIGN.get(f"{planet_key}_{sign_key}")
    if entry:
        return entry.get(lang, entry.get("pt"))
    return None


def get_house(house_num: int, lang: str = "pt") -> dict | None:
    entry = HOUSES.get(house_num)
    if entry:
        return entry.get(lang, entry.get("pt"))
    return None
