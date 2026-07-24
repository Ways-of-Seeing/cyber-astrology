#!/usr/bin/env python3
# coding: utf-8
"""
astro.py — Mapa Astral na Linha de Comando

Uso:
  python astro.py                          # modo interativo
  python astro.py --lang en               # relatório em inglês
  python astro.py --no-wheel              # pula o diagrama
  python astro.py --only planets          # só tabela de planetas
  python astro.py --only insights         # só insights
  python astro.py --only houses           # só casas
"""

import sys
import re
from datetime import datetime

import click
from rich.console import Console
from rich.prompt import Prompt

import geocoder as geo_mod
import engine
import wheel as wheel_mod
import display

console = Console()


def parse_date(s: str) -> tuple[int, int, int]:
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%d/%m/%y"):
        try:
            d = datetime.strptime(s.strip(), fmt)
            return d.year, d.month, d.day
        except ValueError:
            pass
    raise ValueError(f"Data inválida: '{s}'. Use DD/MM/AAAA.")


def parse_time(s: str) -> tuple[int, int]:
    m = re.match(r"^(\d{1,2})[:\.](\d{2})$", s.strip())
    if not m:
        raise ValueError(f"Horário inválido: '{s}'. Use HH:MM.")
    h, mi = int(m.group(1)), int(m.group(2))
    if not (0 <= h <= 23 and 0 <= mi <= 59):
        raise ValueError("Horário fora do intervalo.")
    return h, mi


@click.command()
@click.option("--name",     "-n", default=None, help="Nome da pessoa")
@click.option("--date",     "-d", default=None, help="Data de nascimento (DD/MM/AAAA)")
@click.option("--time",     "-t", default=None, help="Horário de nascimento (HH:MM)")
@click.option("--location", "-l", default=None, help="Local de nascimento (cidade, país)")
@click.option("--lang",           default="pt", type=click.Choice(["pt", "en"]), show_default=True,
              help="Idioma do relatório")
@click.option("--no-wheel",       is_flag=True, default=False, help="Pula o diagrama da roda")
@click.option("--only",           default=None,
              type=click.Choice(["planets", "insights", "houses", "wheel"]),
              help="Exibe apenas uma seção")
def main(name, date, time, location, lang, no_wheel, only):
    """🔮 Gerador de Mapa Astral — linha de comando"""

    console.print("\n[bold cyan]🔮 MAPA ASTRAL[/] [dim]— Calculadora Astrológica[/]\n")

    # ── Input interativo se não fornecido via flags ─────────────────────────
    if not name:
        name = Prompt.ask("[bold]Nome da pessoa[/]")
    if not date:
        date = Prompt.ask("[bold]Data de nascimento[/] [dim](DD/MM/AAAA)[/]")
    if not time:
        time = Prompt.ask("[bold]Horário de nascimento[/] [dim](HH:MM)[/]")
    if not location:
        location = Prompt.ask("[bold]Local de nascimento[/] [dim](ex: São Paulo, Brasil)[/]")

    # ── Parse e validação ───────────────────────────────────────────────────
    try:
        year, month, day = parse_date(date)
        hour, minute = parse_time(time)
    except ValueError as e:
        console.print(f"[red]Erro:[/] {e}")
        sys.exit(1)

    birth_str = f"{day:02d}/{month:02d}/{year}  {hour:02d}:{minute:02d}  —  {location}"

    # ── Geocodificação ──────────────────────────────────────────────────────
    console.print("[dim]Geocodificando localização…[/]")
    try:
        geo = geo_mod.geocode(location)
    except Exception as e:
        console.print(f"[red]Erro na geocodificação:[/] {e}")
        sys.exit(1)

    # ── Cálculo do mapa ─────────────────────────────────────────────────────
    console.print("[dim]Calculando posições planetárias…[/]")
    try:
        chart = engine.calculate(
            name=name,
            year=year, month=month, day=day,
            hour=hour, minute=minute,
            lat=geo["lat"], lon=geo["lon"],
            tz_str=geo["timezone"],
        )
    except Exception as e:
        console.print(f"[red]Erro no cálculo astrológico:[/] {e}")
        sys.exit(1)

    # ── Exibição ─────────────────────────────────────────────────────────────
    display.show_header(name, birth_str, lang)
    display.show_location(geo, lang)

    if only == "wheel" or (only is None and not no_wheel):
        console.print("[dim]Renderizando roda natal…[/]")
        wheel_str = wheel_mod.render(chart)
        display.show_wheel(wheel_str)

    if only is None or only == "planets":
        display.show_planet_table(chart, lang)

    if only is None or only == "insights":
        display.show_insights(chart, lang)

    if only is None or only == "houses":
        display.show_house_meanings(chart, lang)

    console.print()
    console.rule("[dim]Fim do relatório[/]")
    console.print()


if __name__ == "__main__":
    main()
