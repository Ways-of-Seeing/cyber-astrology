"""
Astrological engine: wraps kerykeion for natal chart calculations.
Returns a clean dict used by wheel and display modules.
"""

from kerykeion import AstrologicalSubject


PLANET_KEYS = [
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
    "Cap": "capricorn","Aqu": "aquarius",    "Pis": "pisces",
}

HOUSE_ATTRS = [
    "first_house", "second_house", "third_house", "fourth_house",
    "fifth_house", "sixth_house", "seventh_house", "eighth_house",
    "ninth_house", "tenth_house", "eleventh_house", "twelfth_house",
]


def _abbr(sign_str: str) -> str:
    """Normalise sign string to 3-char abbreviation."""
    return sign_str[:3].capitalize() if sign_str else "Ari"


def _house_num(house_val) -> int:
    """Extract integer house number from various kerykeion return types."""
    if isinstance(house_val, int):
        return house_val
    if isinstance(house_val, str):
        parts = house_val.replace("_", " ").split()
        for p in parts:
            try:
                return int(p)
            except ValueError:
                pass
        words = {
            "first": 1, "second": 2, "third": 3, "fourth": 4,
            "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8,
            "ninth": 9, "tenth": 10, "eleventh": 11, "twelfth": 12,
        }
        for w, n in words.items():
            if w in house_val.lower():
                return n
    return 1


def _parse_planet(obj) -> dict:
    abbr = _abbr(str(obj.sign))
    return {
        "longitude": float(obj.abs_pos),
        "degree_in_sign": float(obj.position),
        "sign_abbr": abbr,
        "sign_pt": SIGN_PT.get(abbr, abbr),
        "sign_key": SIGN_KEY.get(abbr, "aries"),
        "house": _house_num(obj.house),
        "retrograde": bool(getattr(obj, "retrograde", False)),
    }


def calculate(name: str, year: int, month: int, day: int,
              hour: int, minute: int,
              lat: float, lon: float, tz_str: str) -> dict:

    subject = AstrologicalSubject(
        name=name,
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        city="",
        nation="",
        lat=lat,
        lng=lon,
        tz_str=tz_str,
        online=False,
    )

    planets = {}
    for attr, name_pt, name_en, symbol in PLANET_KEYS:
        obj = getattr(subject, attr, None)
        if obj is not None:
            d = _parse_planet(obj)
            d.update({"name_pt": name_pt, "name_en": name_en,
                       "symbol": symbol, "key": attr})
            planets[attr] = d

    # House cusps
    house_cusps = []
    for attr in HOUSE_ATTRS:
        obj = getattr(subject, attr, None)
        house_cusps.append(float(obj.abs_pos) if obj else len(house_cusps) * 30.0)

    # Ascendant = first house cusp
    asc_obj = subject.first_house
    asc_abbr = _abbr(str(asc_obj.sign))
    ascendant = {
        "longitude": float(asc_obj.abs_pos),
        "degree_in_sign": float(asc_obj.position),
        "sign_abbr": asc_abbr,
        "sign_pt": SIGN_PT.get(asc_abbr, asc_abbr),
        "sign_key": SIGN_KEY.get(asc_abbr, "aries"),
        "name_pt": "Ascendente",
        "name_en": "Ascendant",
        "symbol": "AC",
        "key": "ascendant",
        "house": 1,
        "retrograde": False,
    }

    # MC = tenth house cusp
    mc_obj = subject.tenth_house
    mc_abbr = _abbr(str(mc_obj.sign))
    mc = {
        "longitude": float(mc_obj.abs_pos),
        "degree_in_sign": float(mc_obj.position),
        "sign_abbr": mc_abbr,
        "sign_pt": SIGN_PT.get(mc_abbr, mc_abbr),
        "sign_key": SIGN_KEY.get(mc_abbr, "capricorn"),
        "name_pt": "Meio do Céu",
        "name_en": "Midheaven",
        "symbol": "MC",
        "key": "mc",
        "house": 10,
        "retrograde": False,
    }

    return {
        "name": name,
        "planets": planets,
        "ascendant": ascendant,
        "mc": mc,
        "house_cusps": house_cusps,
    }
