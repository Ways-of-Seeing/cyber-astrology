"""
Astrological engine: wraps kerykeion for natal chart calculations.
Returns a typed `Chart` used by wheel, synthesis and display modules.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field

# libephemeris emits noisy fallback warnings (sealed-mode ephemeris);
# they don't affect the planets we use. Must be set before kerykeion
# imports libephemeris, since the level is read at import time.
os.environ.setdefault("LIBEPHEMERIS_LOG_LEVEL", "ERROR")

from kerykeion import AstrologicalSubjectFactory  # noqa: E402

_logger = logging.getLogger("libephemeris")
_logger.setLevel(logging.ERROR)
for _handler in _logger.handlers:
    _handler.setLevel(logging.ERROR)

PLANET_KEYS: list[tuple[str, str, str, str]] = [
    ("sun",     "Sol",      "Sun",      "☉"),
    ("moon",    "Lua",      "Moon",     "☽"),
    ("mercury", "Mercúrio", "Mercury",  "☿"),
    ("venus",   "Vênus",    "Venus",    "♀"),
    ("mars",    "Marte",    "Mars",     "♂"),
    ("jupiter", "Júpiter",  "Jupiter",  "♃"),
    ("saturn",  "Saturno",  "Saturn",   "♄"),
    ("uranus",  "Urano",    "Uranus",   "♅"),
    ("neptune", "Netuno",   "Neptune",  "♆"),
    ("pluto",   "Plutão",   "Pluto",    "♇"),
]

SIGN_PT = {
    "Ari": "Áries",       "Tau": "Touro",     "Gem": "Gêmeos",
    "Can": "Câncer",      "Leo": "Leão",      "Vir": "Virgem",
    "Lib": "Libra",       "Sco": "Escorpião", "Sag": "Sagitário",
    "Cap": "Capricórnio", "Aqu": "Aquário",   "Pis": "Peixes",
}

SIGN_KEY = {
    "Ari": "aries",    "Tau": "taurus",      "Gem": "gemini",
    "Can": "cancer",   "Leo": "leo",         "Vir": "virgo",
    "Lib": "libra",    "Sco": "scorpio",     "Sag": "sagittarius",
    "Cap": "capricorn", "Aqu": "aquarius",   "Pis": "pisces",
}

SIGN_EN = {
    "aries": "Aries",       "taurus": "Taurus",     "gemini": "Gemini",
    "cancer": "Cancer",     "leo": "Leo",           "virgo": "Virgo",
    "libra": "Libra",       "scorpio": "Scorpio",   "sagittarius": "Sagittarius",
    "capricorn": "Capricorn", "aquarius": "Aquarius", "pisces": "Pisces",
}

HOUSE_ATTRS = [
    "first_house", "second_house", "third_house", "fourth_house",
    "fifth_house", "sixth_house", "seventh_house", "eighth_house",
    "ninth_house", "tenth_house", "eleventh_house", "twelfth_house",
]

_HOUSE_WORDS = {
    "first": 1, "second": 2, "third": 3, "fourth": 4,
    "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8,
    "ninth": 9, "tenth": 10, "eleventh": 11, "twelfth": 12,
}


@dataclass
class Planet:
    """A celestial point (planet, Ascendant or MC) in the natal chart."""

    key: str
    name_pt: str
    name_en: str
    symbol: str
    longitude: float          # absolute position 0–360
    degree_in_sign: float     # position within the sign 0–30
    sign_abbr: str
    sign_pt: str
    sign_key: str
    house: int
    retrograde: bool = False

    def name(self, lang: str) -> str:
        return self.name_pt if lang == "pt" else self.name_en

    def sign_name(self, lang: str) -> str:
        return self.sign_pt if lang == "pt" else SIGN_EN.get(self.sign_key, self.sign_abbr)


@dataclass
class Chart:
    """A complete natal chart."""

    name: str
    planets: dict[str, Planet]
    ascendant: Planet
    mc: Planet
    house_cusps: list[float] = field(default_factory=list)

    def all_points(self) -> dict[str, Planet]:
        """Planets plus Ascendant and MC, keyed by planet key."""
        return {"ascendant": self.ascendant, "mc": self.mc, **self.planets}


def _abbr(sign_str: str) -> str:
    """Normalise sign string to 3-char abbreviation."""
    return sign_str[:3].capitalize() if sign_str else "Ari"


def _house_num(house_val: object) -> int:
    """Extract integer house number from various kerykeion return types."""
    if isinstance(house_val, int):
        return house_val
    if isinstance(house_val, str):
        for part in house_val.replace("_", " ").split():
            try:
                return int(part)
            except ValueError:
                pass
        for word, num in _HOUSE_WORDS.items():
            if word in house_val.lower():
                return num
    return 1


def _parse_point(obj: object, key: str, name_pt: str, name_en: str,
                 symbol: str, house: int | None = None) -> Planet:
    abbr = _abbr(str(obj.sign))
    return Planet(
        key=key,
        name_pt=name_pt,
        name_en=name_en,
        symbol=symbol,
        longitude=float(obj.abs_pos),
        degree_in_sign=float(obj.position),
        sign_abbr=abbr,
        sign_pt=SIGN_PT.get(abbr, abbr),
        sign_key=SIGN_KEY.get(abbr, "aries"),
        house=house if house is not None else _house_num(obj.house),
        retrograde=bool(getattr(obj, "retrograde", False)),
    )


def calculate(name: str, year: int, month: int, day: int,
              hour: int, minute: int,
              lat: float, lon: float, tz_str: str) -> Chart:
    subject = AstrologicalSubjectFactory.from_birth_data(
        name=name,
        year=year, month=month, day=day,
        hour=hour, minute=minute,
        lat=lat, lng=lon,
        tz_str=tz_str,
        online=False,
    )

    planets: dict[str, Planet] = {}
    for attr, name_pt, name_en, symbol in PLANET_KEYS:
        obj = getattr(subject, attr, None)
        if obj is not None:
            planets[attr] = _parse_point(obj, attr, name_pt, name_en, symbol)

    house_cusps: list[float] = []
    for attr in HOUSE_ATTRS:
        obj = getattr(subject, attr, None)
        house_cusps.append(float(obj.abs_pos) if obj else len(house_cusps) * 30.0)

    ascendant = _parse_point(subject.first_house, "ascendant",
                             "Ascendente", "Ascendant", "AC", house=1)
    mc = _parse_point(subject.tenth_house, "mc",
                      "Meio do Céu", "Midheaven", "MC", house=10)

    return Chart(
        name=name,
        planets=planets,
        ascendant=ascendant,
        mc=mc,
        house_cusps=house_cusps,
    )
