# coding: utf-8
"""
tests/test_synthesis.py — Unit tests for astrological synthesis (aspects, element balance, moon phase).
"""

import pytest
from cyber_astra.synthesis import (
    calculate_aspects,
    calculate_elements,
    calculate_moon_phase,
    angular_distance,
    MAJOR_ASPECTS,
    MOON_PHASES,
)


class TestAngularDistance:
    """Test shortest angular distance on a 360° circle."""

    def test_same_angle(self):
        assert angular_distance(45.0, 45.0) == 0.0

    def test_simple_distance(self):
        assert angular_distance(10.0, 70.0) == 60.0
        assert angular_distance(70.0, 10.0) == 60.0

    def test_opposite(self):
        assert angular_distance(0.0, 180.0) == 180.0

    def test_wrap_around_circle(self):
        # 10° and 350° are 20° apart
        assert angular_distance(10.0, 350.0) == 20.0
        assert angular_distance(350.0, 10.0) == 20.0


class TestAspects:
    """Test aspect calculation against known fixture."""

    def test_aspects_detected(self, known_chart_data):
        aspects = calculate_aspects(known_chart_data)
        assert len(aspects) > 0

        # Aspects should be sorted by orb ascending (tightest first)
        orbs = [a["orb"] for a in aspects]
        assert orbs == sorted(orbs)

        # Check specific expected major aspects in 1990-06-15 chart
        aspect_pairs = {(a["body1"], a["body2"], a["aspect"]): a for a in aspects}

        # Uranus (278.16°) and Neptune (283.71°) conjunction (diff ~5.55°)
        uranus_neptune = (
            aspect_pairs.get(("uranus", "neptune", "Conjunção"))
            or aspect_pairs.get(("neptune", "uranus", "Conjunção"))
        )
        assert uranus_neptune is not None
        assert uranus_neptune["target_angle"] == 0.0
        assert 5.0 <= uranus_neptune["orb"] <= 6.0

        # Venus (49.05°) and Jupiter (105.94°) sextile (diff ~56.89°, orb ~3.11°)
        venus_jupiter = (
            aspect_pairs.get(("venus", "jupiter", "Sextil"))
            or aspect_pairs.get(("jupiter", "venus", "Sextil"))
        )
        assert venus_jupiter is not None
        assert venus_jupiter["target_angle"] == 60.0
        assert 3.0 <= venus_jupiter["orb"] <= 4.0

        # Sun (84.35°) and Moon (348.43°) square (diff ~95.92°, orb ~5.92°)
        sun_moon = (
            aspect_pairs.get(("sun", "moon", "Quadratura"))
            or aspect_pairs.get(("moon", "sun", "Quadratura"))
        )
        assert sun_moon is not None
        assert sun_moon["target_angle"] == 90.0

        # Moon (348.43°) and Pluto (225.40°) trine (diff ~123.03°, orb ~3.03°)
        moon_pluto = (
            aspect_pairs.get(("moon", "pluto", "Trígono"))
            or aspect_pairs.get(("pluto", "moon", "Trígono"))
        )
        assert moon_pluto is not None
        assert moon_pluto["target_angle"] == 120.0

        # Venus (49.05°) and Pluto (225.40°) opposition (diff ~176.35°, orb ~3.65°)
        venus_pluto = (
            aspect_pairs.get(("venus", "pluto", "Oposição"))
            or aspect_pairs.get(("pluto", "venus", "Oposição"))
        )
        assert venus_pluto is not None
        assert venus_pluto["target_angle"] == 180.0

    def test_orb_factor_scaling(self, known_chart_data):
        tight_aspects = calculate_aspects(known_chart_data, orb_factor=0.5)
        loose_aspects = calculate_aspects(known_chart_data, orb_factor=1.5)
        assert len(tight_aspects) <= len(loose_aspects)

    def test_aspects_with_angles(self, known_chart_data):
        aspects_no_angles = calculate_aspects(known_chart_data, include_angles=False)
        aspects_with_angles = calculate_aspects(known_chart_data, include_angles=True)
        assert len(aspects_with_angles) >= len(aspects_no_angles)
        angle_bodies = {"ascendant", "mc"}
        has_angle = any(
            a["body1"] in angle_bodies or a["body2"] in angle_bodies
            for a in aspects_with_angles
        )
        assert has_angle


class TestElementBalance:
    """Test elemental and modality balance calculation against known fixture."""

    def test_element_counts_and_dominance(self, known_chart_data):
        result = calculate_elements(known_chart_data)
        elements = result["elements"]
        modalities = result["modalities"]

        # Expected counts for the 10 planets:
        # Earth (4): Venus (Tau), Saturn (Cap), Uranus (Cap), Neptune (Cap)
        # Water (3): Moon (Pis), Jupiter (Can), Pluto (Sco)
        # Air (2): Sun (Gem), Mercury (Gem)
        # Fire (1): Mars (Ari)
        assert elements["earth"]["count"] == 4
        assert elements["water"]["count"] == 3
        assert elements["air"]["count"] == 2
        assert elements["fire"]["count"] == 1

        assert result["total_bodies"] == 10
        assert result["dominant_element"] == "earth"

        # Check percentages
        assert elements["earth"]["percentage"] == 40.0
        assert elements["water"]["percentage"] == 30.0
        assert elements["air"]["percentage"] == 20.0
        assert elements["fire"]["percentage"] == 10.0

        # Modalities:
        # Cardinal (5): Mars (Ari), Jupiter (Can), Saturn (Cap), Uranus (Cap), Neptune (Cap)
        # Fixed (2): Venus (Tau), Pluto (Sco)
        # Mutable (3): Sun (Gem), Mercury (Gem), Moon (Pis)
        assert modalities["cardinal"]["count"] == 5
        assert modalities["mutable"]["count"] == 3
        assert modalities["fixed"]["count"] == 2
        assert result["dominant_modality"] == "cardinal"

    def test_element_balance_with_angles(self, known_chart_data):
        # Adding Ascendant (Sco -> Water, Fixed) and MC (Leo -> Fire, Fixed)
        result = calculate_elements(known_chart_data, include_angles=True)
        assert result["total_bodies"] == 12
        assert result["elements"]["water"]["count"] == 4  # +1 Sco
        assert result["elements"]["fire"]["count"] == 2   # +1 Leo
        assert result["modalities"]["fixed"]["count"] == 4 # +2 Fixed


class TestMoonPhase:
    """Test lunar phase calculation with known fixture and edge cases."""

    def test_moon_phase_known_chart(self, known_chart_data):
        # Sun: 84.35° (Gemini), Moon: 348.43° (Pisces)
        # Elongation = (348.43 - 84.35) % 360 = 264.08° (between 225° and 270°)
        phase = calculate_moon_phase(known_chart_data)

        assert phase["name_pt"] == "Gibosa Minguante"
        assert phase["name_en"] == "Waning Gibbous"
        assert phase["symbol"] == "🌖"
        assert phase["waxing"] is False
        assert 263.0 <= phase["elongation"] <= 265.0
        # Illumination should be around 55%
        assert 50.0 <= phase["illumination_pct"] <= 60.0

    @pytest.mark.parametrize(
        "sun_lon, moon_lon, expected_pt, expected_waxing",
        [
            (0.0, 10.0, "Lua Nova", True),
            (0.0, 60.0, "Lua Crescente", True),
            (0.0, 100.0, "Quarto Crescente", True),
            (0.0, 150.0, "Gibosa Crescente", True),
            (0.0, 185.0, "Lua Cheia", False),
            (0.0, 240.0, "Gibosa Minguante", False),
            (0.0, 290.0, "Quarto Minguante", False),
            (0.0, 340.0, "Lua Minguante", False),
        ],
    )
    def test_all_eight_phases(self, sun_lon, moon_lon, expected_pt, expected_waxing):
        mock_chart = {
            "planets": {
                "sun": {"longitude": sun_lon},
                "moon": {"longitude": moon_lon},
            }
        }
        res = calculate_moon_phase(mock_chart)
        assert res["name_pt"] == expected_pt
        assert res["waxing"] == expected_waxing

    def test_missing_sun_or_moon_raises_error(self):
        with pytest.raises(ValueError, match="chart_data must contain 'sun' and 'moon'"):
            calculate_moon_phase({"planets": {"sun": {"longitude": 0.0}}})
