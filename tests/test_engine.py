# coding: utf-8
"""
tests/test_engine.py — Tests for chart calculation engine.
"""

import pytest
import engine


def test_calculate_returns_expected_structure():
    """Verify that calculate produces planets, ascendant, mc, and house cusps."""
    chart = engine.calculate(
        name="Offline Test",
        year=1990,
        month=6,
        day=15,
        hour=14,
        minute=30,
        lat=-23.5505,
        lon=-46.6333,
        tz_str="America/Sao_Paulo",
    )

    assert chart["name"] == "Offline Test"
    assert "planets" in chart
    assert "ascendant" in chart
    assert "mc" in chart
    assert "house_cusps" in chart
    assert len(chart["house_cusps"]) == 12

    # Verify all 10 standard astrological bodies are present
    expected_bodies = [
        "sun", "moon", "mercury", "venus", "mars",
        "jupiter", "saturn", "uranus", "neptune", "pluto",
    ]
    for body in expected_bodies:
        assert body in chart["planets"]
        p = chart["planets"][body]
        assert "longitude" in p
        assert 0.0 <= p["longitude"] < 360.0
        assert "sign_abbr" in p
        assert "house" in p
        assert 1 <= p["house"] <= 12
