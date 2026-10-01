# coding: utf-8
"""
tests/test_prompts.py — Unit tests for date and time parsing in cyber_astra.prompts.
"""

import pytest
from cyber_astra.prompts import parse_date, parse_time


class TestParseDate:
    """Test date parsing with various standard and compact formats."""

    @pytest.mark.parametrize(
        "date_str, expected",
        [
            ("15/06/1990", (1990, 6, 15)),
            ("15-06-1990", (1990, 6, 15)),
            ("1990-06-15", (1990, 6, 15)),
            ("15/06/90", (1990, 6, 15)),
            ("15-06-90", (1990, 6, 15)),
            ("15061990", (1990, 6, 15)),
            ("19900615", (1990, 6, 15)),
            ("1990/06/15", (1990, 6, 15)),
            ("  15/06/1990  ", (1990, 6, 15)),  # whitespace trimming
            ("01/01/2000", (2000, 1, 1)),
            ("29/02/2024", (2024, 2, 29)),  # leap year
        ],
    )
    def test_valid_date_formats(self, date_str, expected):
        assert parse_date(date_str) == expected

    @pytest.mark.parametrize(
        "invalid_str",
        [
            "invalid",
            "",
            "32/01/1990",       # invalid day
            "15/13/1990",       # invalid month
            "29/02/2023",       # non-leap year Feb 29
            "1990-02-30",       # invalid Feb 30
            "12345",            # too short
            "150619901",        # too long
            "15.06.1990.20",
        ],
    )
    def test_invalid_date_formats(self, invalid_str):
        with pytest.raises(ValueError, match="Data inválida"):
            parse_date(invalid_str)


class TestParseTime:
    """Test time parsing with flexible formats (colons, dots, 'h' letter, compact digits)."""

    @pytest.mark.parametrize(
        "time_str, expected",
        [
            ("14:30", (14, 30)),
            ("14.30", (14, 30)),
            ("14h30", (14, 30)),
            ("14H30", (14, 30)),
            ("1430", (14, 30)),
            ("9:30", (9, 30)),
            ("09:30", (9, 30)),
            ("9.30", (9, 30)),
            ("9h30", (9, 30)),
            ("09h30", (9, 30)),
            ("930", (9, 30)),
            ("14h", (14, 0)),
            ("9h", (9, 0)),
            ("00:00", (0, 0)),
            ("23:59", (23, 59)),
            ("  14:30  ", (14, 30)),  # whitespace trimming
        ],
    )
    def test_valid_time_formats(self, time_str, expected):
        assert parse_time(time_str) == expected

    @pytest.mark.parametrize(
        "invalid_str",
        [
            "invalid",
            "",
            "24:00",      # hour out of bounds
            "25:30",      # hour out of bounds
            "14:60",      # minute out of bounds
            "14:99",      # minute out of bounds
            "99999",      # too many digits
            "12",         # too short without 'h'
            "14:5",       # incomplete format
            "ab:cd",
        ],
    )
    def test_invalid_time_formats(self, invalid_str):
        with pytest.raises(ValueError):
            parse_time(invalid_str)
