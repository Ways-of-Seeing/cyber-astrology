# coding: utf-8
"""
prompts.py — Input parsing and validation for dates, times, and CLI prompts.
"""

import re
from datetime import datetime


def parse_date(s: str) -> tuple[int, int, int]:
    """
    Parse flexible date formats into (year, month, day).

    Supported formats:
      - DD/MM/AAAA (e.g. '15/06/1990')
      - DD-MM-AAAA (e.g. '15-06-1990')
      - AAAA-MM-DD (e.g. '1990-06-15')
      - DD/MM/AA   (e.g. '15/06/90')
      - DD-MM-AA   (e.g. '15-06-90')
      - DDMMAAAA   (e.g. '15061990')
      - AAAAMMDD   (e.g. '19900615')
      - AAAA/MM/DD (e.g. '1990/06/15')

    Raises ValueError on invalid formats or dates.
    """
    cleaned = s.strip()
    formats = (
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%d/%m/%y",
        "%d-%m-%y",
        "%d%m%Y",
        "%Y%m%d",
        "%Y/%m/%d",
    )
    for fmt in formats:
        try:
            d = datetime.strptime(cleaned, fmt)
            return d.year, d.month, d.day
        except ValueError:
            pass

    raise ValueError(f"Data inválida: '{s}'. Use DD/MM/AAAA.")


def parse_time(s: str) -> tuple[int, int]:
    """
    Parse flexible time formats into (hour, minute).

    Supported formats:
      - HH:MM  (e.g. '14:30', '9:30', '09:30')
      - HH.MM  (e.g. '14.30', '9.30')
      - HHhMM  (e.g. '14h30', '9h30', '09h30')
      - HHh    (e.g. '14h', '9h')
      - HHMM   (e.g. '1430', '0930')

    Validates hours in [0, 23] and minutes in [0, 59].
    Raises ValueError on invalid formats or out-of-range times.
    """
    val = s.strip()

    # Digits only: e.g. '1430' -> 14:30, '930' -> 09:30
    if re.fullmatch(r"\d{3,4}", val):
        if len(val) == 4:
            h, mi = int(val[:2]), int(val[2:])
        else:
            h, mi = int(val[:1]), int(val[1:])
    else:
        m = re.match(r"^(\d{1,2})(?:[:\.](\d{2})|[hH](\d{2})?)$", val)
        if m:
            h = int(m.group(1))
            mi = int(m.group(2) or m.group(3)) if (m.group(2) or m.group(3)) is not None else 0
        else:
            raise ValueError(f"Horário inválido: '{s}'. Use HH:MM.")

    if not (0 <= h <= 23 and 0 <= mi <= 59):
        raise ValueError(f"Horário fora do intervalo: '{s}'. Use valores entre 00:00 e 23:59.")

    return h, mi
