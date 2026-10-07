"""
Chart synthesis: aspects, element/modality balance, natal Moon phase
and the Big Three (Sun/Moon/Ascendant) narrative.

All computations are pure geometry over absolute longitudes — no extra
dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass

from .data import (
    ASPECTS,
    BIG_THREE,
    PLANET_THEMES,
    SIGN_ELEMENT,
    SIGN_MODALITY,
    get_moon_phase,
)
from .engine import Chart

# Points included in aspect computation, in display order.
_ASPECT_POINTS = [
    "sun", "moon", "mercury", "venus", "mars",
    "jupiter", "saturn", "uranus", "neptune", "pluto",
    "ascendant", "mc",
]

# Points that weigh into element/modality balance.
_BALANCE_POINTS = [
    "sun", "moon", "mercury", "venus", "mars",
    "jupiter", "saturn", "ascendant",
]


@dataclass
class Aspect:
    """An angular relationship between two chart points."""

    key: str            # aspect key, e.g. "trine"
    symbol: str
    harmony: str        # "fusion" | "soft" | "hard"
    point1: str         # planet keys
    point2: str
    orb: float          # exactness, in degrees
    angle: float        # nominal aspect angle

    def label(self, chart: Chart, lang: str) -> str:
        points = chart.all_points()
        p1, p2 = points[self.point1], points[self.point2]
        return f"{p1.symbol} {p1.name(lang)} {self.symbol} {p2.symbol} {p2.name(lang)}"


def _angular_distance(a: float, b: float) -> float:
    """Smallest distance between two longitudes, 0–180."""
    diff = abs(a - b) % 360.0
    return min(diff, 360.0 - diff)


def compute_aspects(chart: Chart) -> list[Aspect]:
    """Major aspects between all chart points, sorted by orb (exactness)."""
    points = chart.all_points()
    keys = [k for k in _ASPECT_POINTS if k in points]
    found: list[Aspect] = []

    for i, k1 in enumerate(keys):
        for k2 in keys[i + 1:]:
            dist = _angular_distance(points[k1].longitude, points[k2].longitude)
            for key, spec in ASPECTS.items():
                orb = abs(dist - spec["angle"])
                if orb <= spec["orb"]:
                    found.append(Aspect(
                        key=key,
                        symbol=spec["symbol"],
                        harmony=spec["harmony"],
                        point1=k1,
                        point2=k2,
                        orb=orb,
                        angle=float(spec["angle"]),
                    ))
                    break

    return sorted(found, key=lambda a: a.orb)


def element_balance(chart: Chart) -> dict[str, int]:
    """Count of planets per element (fire/earth/air/water)."""
    counts = {"fire": 0, "earth": 0, "air": 0, "water": 0}
    points = chart.all_points()
    for key in _BALANCE_POINTS:
        point = points.get(key)
        if point:
            counts[SIGN_ELEMENT[point.sign_key]] += 1
    return counts


def modality_balance(chart: Chart) -> dict[str, int]:
    """Count of planets per modality (cardinal/fixed/mutable)."""
    counts = {"cardinal": 0, "fixed": 0, "mutable": 0}
    points = chart.all_points()
    for key in _BALANCE_POINTS:
        point = points.get(key)
        if point:
            counts[SIGN_MODALITY[point.sign_key]] += 1
    return counts


def moon_phase(chart: Chart, lang: str = "pt") -> dict:
    """Natal Moon phase from Sun–Moon elongation."""
    elongation = (chart.planets["moon"].longitude
                  - chart.planets["sun"].longitude) % 360.0
    return get_moon_phase(elongation, lang)


def big_three(chart: Chart, lang: str = "pt") -> str:
    """Procedural narrative combining Sun, Moon and Ascendant signs."""
    texts = BIG_THREE[lang if lang in BIG_THREE else "pt"]
    sun = chart.planets["sun"]
    moon = chart.planets["moon"]
    asc = chart.ascendant

    def sign_of(point) -> str:
        return point.sign_name(lang)

    signs = {"sun": sun.sign_key, "moon": moon.sign_key, "asc": asc.sign_key}
    names = {"sun": sign_of(sun), "moon": sign_of(moon), "asc": sign_of(asc)}

    unique = set(signs.values())
    combos = texts["combos"]
    if len(unique) == 1:
        combo = combos["same"].format(sign=names["sun"])
    elif len(unique) == 2:
        # Find the pair that shares a sign.
        pair = next(
            (a, b) for i, (a, va) in enumerate(signs.items())
            for b, vb in list(signs.items())[i + 1:] if va == vb
        )
        labels_pt = {"sun": "Sol", "moon": "Lua", "asc": "Ascendente"}
        labels_en = {"sun": "Sun", "moon": "Moon", "asc": "Ascendant"}
        labels = labels_pt if lang == "pt" else labels_en
        joiner = " e " if lang == "pt" else " and "
        combo = combos["two_same"].format(
            s1=labels[pair[0]], s2=labels[pair[1]],
            sign=names[pair[0]], what=f"{labels[pair[0]]}{joiner}{labels[pair[1]]}",
        )
    else:
        combo = combos["all_diff"]

    return texts["template"].format(
        sun=names["sun"], moon=names["moon"], asc=names["asc"], combo=combo,
    )


def aspect_narrative(aspect: Aspect, chart: Chart, lang: str = "pt") -> str:
    """Rich text for a single aspect: general meaning + pair dynamic."""
    spec = ASPECTS[aspect.key]
    texts = spec[lang if lang in spec else "pt"]
    points = chart.all_points()
    p1 = points[aspect.point1]
    p2 = points[aspect.point2]
    theme1 = PLANET_THEMES[aspect.point1][lang if lang in ("pt", "en") else "pt"]
    theme2 = PLANET_THEMES[aspect.point2][lang if lang in ("pt", "en") else "pt"]
    dynamic = texts["dinamica"].format(p1=theme1, p2=theme2)
    dynamic = dynamic[0].upper() + dynamic[1:]
    return f"{texts['descricao']}\n\n{dynamic}"
