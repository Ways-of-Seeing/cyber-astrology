# coding: utf-8
"""
cyber_astra.synthesis re-exports synthesis functions.
"""

from synthesis import (
    calculate_aspects,
    calculate_elements,
    calculate_moon_phase,
    angular_distance,
    MAJOR_ASPECTS,
    MOON_PHASES,
    SIGN_ELEMENTS,
    SIGN_MODALITIES,
)

__all__ = [
    "calculate_aspects",
    "calculate_elements",
    "calculate_moon_phase",
    "angular_distance",
    "MAJOR_ASPECTS",
    "MOON_PHASES",
    "SIGN_ELEMENTS",
    "SIGN_MODALITIES",
]
