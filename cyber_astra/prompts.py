# coding: utf-8
"""
Friendly input helpers for people who have never touched a CLI.

- Dates without separators: 15061990, 150690, 15/06/1990, 15 6 90…
- Times without colons: 1430, 930, 14h30, 14:30, "14"…
- Optional machine location detection (IP-based), always with consent.
"""

from __future__ import annotations

import json
import re
import urllib.request
from datetime import datetime

from rich.console import Console
from rich.prompt import Confirm, Prompt

_IP_API = ("http://ip-api.com/json/?fields="
           "status,message,city,regionName,country,lat,lon,timezone")


class InvalidInput(ValueError):
    """Raised when a friendly parse fails; carries a user-facing message."""


# ── Datas ────────────────────────────────────────────────────────────────────

def parse_date_flexible(text: str) -> tuple[int, int, int]:
    """Parse dates like 15061990, 150690, 15/06/1990, 15 6 90, 1990-06-15."""
    groups = re.findall(r"\d+", text.strip())

    if len(groups) == 1:
        digits = groups[0]
        if len(digits) == 8:                      # DDMMYYYY
            day, month, year = digits[:2], digits[2:4], digits[4:]
        elif len(digits) == 6:                    # DDMMYY
            day, month, year = digits[:2], digits[2:4], digits[4:]
        else:
            raise InvalidInput(_date_hint())
    elif len(groups) == 3:
        if len(groups[0]) == 4:                   # YYYY MM DD
            year, month, day = groups
        else:                                     # DD MM YYYY
            day, month, year = groups
    else:
        raise InvalidInput(_date_hint())

    y, m, d = int(year), int(month), int(day)
    if y < 100:                                   # pivô de 2 dígitos
        y += 2000 if y <= 29 else 1900

    try:
        datetime(y, m, d)
    except ValueError:
        raise InvalidInput(_date_hint()) from None
    return y, m, d


def _date_hint() -> str:
    return ("Não entendi essa data. 😅 Pode digitar do seu jeito: "
            "15/06/1990, 15-06-90 ou até 15061990.")


# ── Horários ─────────────────────────────────────────────────────────────────

def parse_time_flexible(text: str) -> tuple[int, int]:
    """Parse times like 1430, 930, 14h30, 14:30, '14 30', '14'."""
    groups = re.findall(r"\d+", text.strip())

    if len(groups) == 1:
        digits = groups[0]
        if len(digits) <= 2:                      # "14" → 14:00
            hour, minute = int(digits), 0
        elif len(digits) == 3:                    # "930" → 09:30
            hour, minute = int(digits[0]), int(digits[1:])
        elif len(digits) == 4:                    # "1430" → 14:30
            hour, minute = int(digits[:2]), int(digits[2:])
        else:
            raise InvalidInput(_time_hint())
    elif len(groups) >= 2:                        # 14:30, 14h30, 14 30
        hour, minute = int(groups[0]), int(groups[1])
    else:
        raise InvalidInput(_time_hint())

    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise InvalidInput(_time_hint())
    return hour, minute


def _time_hint() -> str:
    return ("Não entendi esse horário. 😅 Tente 14:30, 14h30 ou 1430. "
            "Se não souber, é só apertar Enter — usamos meio-dia.")


# ── Perguntas com tentativa até acertar ──────────────────────────────────────

def ask_date(console: Console) -> tuple[int, int, int]:
    while True:
        raw = Prompt.ask(
            "[bold]📅 Data de nascimento[/] "
            "[dim](ex: 15/06/1990 ou 15061990)[/]",
            console=console)
        try:
            return parse_date_flexible(raw)
        except InvalidInput as e:
            console.print(f"[yellow]{e}[/]")


def ask_time(console: Console) -> tuple[int, int]:
    while True:
        raw = Prompt.ask(
            "[bold]⏰ Horário de nascimento[/] "
            "[dim](ex: 14:30 ou 1430 — Enter se não souber)[/]",
            default="", console=console)
        if not raw.strip():
            console.print("[dim]Sem problemas! Vou usar meio-dia (12:00). "
                          "O Ascendente e as Casas ficam aproximados.[/]")
            return 12, 0
        try:
            return parse_time_flexible(raw)
        except InvalidInput as e:
            console.print(f"[yellow]{e}[/]")


# ── Localização ──────────────────────────────────────────────────────────────

def detect_location(timeout: float = 5.0) -> dict | None:
    """Detect machine location by IP. Returns geo dict or None."""
    try:
        with urllib.request.urlopen(_IP_API, timeout=timeout) as resp:
            data = json.load(resp)
    except Exception:
        return None
    if data.get("status") != "success":
        return None
    parts = [data.get("city"), data.get("regionName"), data.get("country")]
    return {
        "display_name": ", ".join(p for p in parts if p),
        "lat": float(data["lat"]),
        "lon": float(data["lon"]),
        "timezone": data.get("timezone") or "UTC",
        "raw": data,
    }


def ask_location(console: Console) -> tuple[str, dict | None]:
    """
    Ask where the person was born. Offers machine detection (with consent).
    Returns (location_label, geo_dict_or_None). When geo is None, the caller
    should geocode location_label.
    """
    if Confirm.ask(
            "[bold]📍 Posso detectar a cidade onde você está agora?[/] "
            "[dim](se você nasceu aí mesmo, facilita!)[/]",
            choices=["s", "n"], default="s", console=console):
        with console.status("[dim]Consultando sua rede…[/]", spinner="moon"):
            geo = detect_location()
        if geo:
            console.print(f"[green]📍 Você está em:[/] [bold]{geo['display_name']}[/]")
            if Confirm.ask(
                    f"[bold]Você nasceu em {geo['display_name'].split(',')[0]}?[/]",
                    choices=["s", "n"], default="s", console=console):
                return geo["display_name"], geo
        else:
            console.print("[yellow]Não consegui detectar 😕 Sem problemas, "
                          "a gente digita![/]")

    city = Prompt.ask(
        "[bold]🏙️  Cidade onde você nasceu[/] "
        "[dim](ex: São Paulo, Recife, Lisboa)[/]",
        console=console)
    return city, None
