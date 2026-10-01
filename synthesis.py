# coding: utf-8
"""
synthesis.py — Astrological synthesis: aspects, elemental balance, and moon phase.
"""

import math
from typing import Any


SIGN_ELEMENTS = {
    # Fire
    "Ari": "fire", "Leo": "fire", "Sag": "fire",
    # Earth
    "Tau": "earth", "Vir": "earth", "Cap": "earth",
    # Air
    "Gem": "air", "Lib": "air", "Aqu": "air",
    # Water
    "Can": "water", "Sco": "water", "Pis": "water",
}

SIGN_MODALITIES = {
    # Cardinal
    "Ari": "cardinal", "Can": "cardinal", "Lib": "cardinal", "Cap": "cardinal",
    # Fixed
    "Tau": "fixed", "Leo": "fixed", "Sco": "fixed", "Aqu": "fixed",
    # Mutable
    "Gem": "mutable", "Vir": "mutable", "Sag": "mutable", "Pis": "mutable",
}

ELEMENT_NAMES = {
    "fire": {"name_pt": "Fogo", "name_en": "Fire", "symbol": "🔥"},
    "earth": {"name_pt": "Terra", "name_en": "Earth", "symbol": "🌍"},
    "air": {"name_pt": "Ar", "name_en": "Air", "symbol": "💨"},
    "water": {"name_pt": "Água", "name_en": "Water", "symbol": "💧"},
}

MODALITY_NAMES = {
    "cardinal": {"name_pt": "Cardinal", "name_en": "Cardinal"},
    "fixed": {"name_pt": "Fixo", "name_en": "Fixed"},
    "mutable": {"name_pt": "Mutável", "name_en": "Mutable"},
}

# Major astrological aspects
MAJOR_ASPECTS = [
    {"name_pt": "Conjunção", "name_en": "Conjunction", "angle": 0.0, "symbol": "☌", "default_orb": 8.0},
    {"name_pt": "Sextil", "name_en": "Sextile", "angle": 60.0, "symbol": "⚹", "default_orb": 6.0},
    {"name_pt": "Quadratura", "name_en": "Square", "angle": 90.0, "symbol": "□", "default_orb": 8.0},
    {"name_pt": "Trígono", "name_en": "Trine", "angle": 120.0, "symbol": "△", "default_orb": 8.0},
    {"name_pt": "Oposição", "name_en": "Opposition", "angle": 180.0, "symbol": "☍", "default_orb": 8.0},
]

# 8 Moon Phases (based on elongation = (moon_lon - sun_lon) % 360)
MOON_PHASES = [
    {
        "min_deg": 0.0, "max_deg": 45.0,
        "name_pt": "Lua Nova", "name_en": "New Moon",
        "symbol": "🌑", "waxing": True,
    },
    {
        "min_deg": 45.0, "max_deg": 90.0,
        "name_pt": "Lua Crescente", "name_en": "Waxing Crescent",
        "symbol": "🌒", "waxing": True,
    },
    {
        "min_deg": 90.0, "max_deg": 135.0,
        "name_pt": "Quarto Crescente", "name_en": "First Quarter",
        "symbol": "🌓", "waxing": True,
    },
    {
        "min_deg": 135.0, "max_deg": 180.0,
        "name_pt": "Gibosa Crescente", "name_en": "Waxing Gibbous",
        "symbol": "🌔", "waxing": True,
    },
    {
        "min_deg": 180.0, "max_deg": 225.0,
        "name_pt": "Lua Cheia", "name_en": "Full Moon",
        "symbol": "🌕", "waxing": False,
    },
    {
        "min_deg": 225.0, "max_deg": 270.0,
        "name_pt": "Gibosa Minguante", "name_en": "Waning Gibbous",
        "symbol": "🌖", "waxing": False,
    },
    {
        "min_deg": 270.0, "max_deg": 315.0,
        "name_pt": "Quarto Minguante", "name_en": "Third Quarter",
        "symbol": "🌗", "waxing": False,
    },
    {
        "min_deg": 315.0, "max_deg": 360.0,
        "name_pt": "Lua Minguante", "name_en": "Waning Crescent",
        "symbol": "🌘", "waxing": False,
    },
]


def angular_distance(deg1: float, deg2: float) -> float:
    """Calculate the shortest angular distance between two longitudes on a 360° circle."""
    diff = abs(deg1 - deg2) % 360.0
    return diff if diff <= 180.0 else 360.0 - diff


def calculate_aspects(chart_data: dict[str, Any], orb_factor: float = 1.0, include_angles: bool = False) -> list[dict[str, Any]]:
    """
    Calculate astrological aspects between celestial bodies in chart_data.

    Args:
        chart_data: Dict containing 'planets' (and optionally 'ascendant', 'mc').
        orb_factor: Multiplier for maximum allowed orb (default 1.0).
        include_angles: Whether to include Ascendant and Midheaven (MC).

    Returns:
        List of detected aspect dicts sorted by orb (tightest first).
    """
    bodies: list[tuple[str, str, str, float]] = []
    planets = chart_data.get("planets", {})

    for key, pdata in planets.items():
        name_pt = pdata.get("name_pt", key)
        name_en = pdata.get("name_en", key)
        lon = float(pdata["longitude"])
        bodies.append((key, name_pt, name_en, lon))

    if include_angles:
        if "ascendant" in chart_data and chart_data["ascendant"]:
            asc = chart_data["ascendant"]
            bodies.append(("ascendant", asc.get("name_pt", "Ascendente"), asc.get("name_en", "Ascendant"), float(asc["longitude"])))
        if "mc" in chart_data and chart_data["mc"]:
            mc = chart_data["mc"]
            bodies.append(("mc", mc.get("name_pt", "Meio do Céu"), mc.get("name_en", "Midheaven"), float(mc["longitude"])))

    aspects_found = []
    num_bodies = len(bodies)

    for i in range(num_bodies):
        p1_key, p1_pt, p1_en, lon1 = bodies[i]
        for j in range(i + 1, num_bodies):
            p2_key, p2_pt, p2_en, lon2 = bodies[j]
            dist = angular_distance(lon1, lon2)

            for asp in MAJOR_ASPECTS:
                max_orb = asp["default_orb"] * orb_factor
                orb = abs(dist - asp["angle"])
                if orb <= max_orb:
                    aspects_found.append({
                        "body1": p1_key,
                        "body1_name_pt": p1_pt,
                        "body1_name_en": p1_en,
                        "body2": p2_key,
                        "body2_name_pt": p2_pt,
                        "body2_name_en": p2_en,
                        "aspect": asp["name_pt"],
                        "aspect_en": asp["name_en"],
                        "symbol": asp["symbol"],
                        "target_angle": asp["angle"],
                        "actual_angle": round(dist, 2),
                        "orb": round(orb, 2),
                    })

    aspects_found.sort(key=lambda x: x["orb"])
    return aspects_found


def calculate_elements(chart_data: dict[str, Any], include_angles: bool = False) -> dict[str, Any]:
    """
    Calculate elemental and modality balance for chart_data.

    Args:
        chart_data: Dict with 'planets' (and optionally 'ascendant', 'mc').
        include_angles: Whether to count Ascendant and MC in the distribution.

    Returns:
        Dict with 'elements', 'modalities', 'dominant_element', 'dominant_modality', and total count.
    """
    element_counts = {"fire": 0, "earth": 0, "air": 0, "water": 0}
    modality_counts = {"cardinal": 0, "fixed": 0, "mutable": 0}

    signs_to_check = []
    planets = chart_data.get("planets", {})
    for p in planets.values():
        abbr = p.get("sign_abbr", "")[:3].capitalize()
        if abbr:
            signs_to_check.append(abbr)

    if include_angles:
        for angle_key in ("ascendant", "mc"):
            if angle_key in chart_data and chart_data[angle_key]:
                abbr = chart_data[angle_key].get("sign_abbr", "")[:3].capitalize()
                if abbr:
                    signs_to_check.append(abbr)

    total = len(signs_to_check)
    for sign in signs_to_check:
        el = SIGN_ELEMENTS.get(sign)
        if el:
            element_counts[el] += 1
        mod = SIGN_MODALITIES.get(sign)
        if mod:
            modality_counts[mod] += 1

    elements_result = {}
    for el_key, count in element_counts.items():
        pct = round((count / total * 100), 1) if total > 0 else 0.0
        meta = ELEMENT_NAMES[el_key]
        elements_result[el_key] = {
            "count": count,
            "percentage": pct,
            "name_pt": meta["name_pt"],
            "name_en": meta["name_en"],
            "symbol": meta["symbol"],
        }

    modalities_result = {}
    for mod_key, count in modality_counts.items():
        pct = round((count / total * 100), 1) if total > 0 else 0.0
        meta = MODALITY_NAMES[mod_key]
        modalities_result[mod_key] = {
            "count": count,
            "percentage": pct,
            "name_pt": meta["name_pt"],
            "name_en": meta["name_en"],
        }

    dominant_element = max(element_counts, key=element_counts.get) if total > 0 else None
    dominant_modality = max(modality_counts, key=modality_counts.get) if total > 0 else None

    return {
        "total_bodies": total,
        "elements": elements_result,
        "modalities": modalities_result,
        "dominant_element": dominant_element,
        "dominant_modality": dominant_modality,
    }


def calculate_moon_phase(chart_data: dict[str, Any]) -> dict[str, Any]:
    """
    Calculate the lunar phase based on the Sun and Moon longitudes in chart_data.

    Args:
        chart_data: Dict with 'planets' containing 'sun' and 'moon' entries with 'longitude'.

    Returns:
        Dict with 'name_pt', 'name_en', 'symbol', 'elongation', 'illumination_pct', 'waxing'.
    """
    planets = chart_data.get("planets", {})
    if "sun" not in planets or "moon" not in planets:
        raise ValueError("chart_data must contain 'sun' and 'moon' with 'longitude'")

    sun_lon = float(planets["sun"]["longitude"])
    moon_lon = float(planets["moon"]["longitude"])

    elongation = (moon_lon - sun_lon) % 360.0

    # Illumination formula: (1 - cos(elongation)) / 2 * 100%
    rad = math.radians(elongation)
    illumination_pct = round((1.0 - math.cos(rad)) / 2.0 * 100.0, 1)

    matched_phase = MOON_PHASES[0]
    for phase in MOON_PHASES:
        if phase["min_deg"] <= elongation < phase["max_deg"]:
            matched_phase = phase
            break

    return {
        "name_pt": matched_phase["name_pt"],
        "name_en": matched_phase["name_en"],
        "symbol": matched_phase["symbol"],
        "elongation": round(elongation, 2),
        "illumination_pct": illumination_pct,
        "waxing": matched_phase["waxing"],
    }
