# coding: utf-8
"""
Cyber Astra — CLI entry point.

Modos:
  cyber-astra                       → menu interativo (para todo mundo!)
  cyber-astra -n Ana -d 15061990 …  → direto, com prompts para o que faltar
  cyber-astra --only synthesis      → relatório parcial
"""

from __future__ import annotations

import argparse
import sys

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from . import animations, art, display, geocoder, prompts, wheel
from .engine import calculate

console = Console()

SECTIONS = ("planets", "synthesis", "aspects", "insights", "houses", "wheel")

MENU = {
    "pt": {
        "option_chart": "🌟  Criar meu mapa astral",
        "option_synastry": "💞  Comparar dois mapas (sinastria)",
        "option_lang": "🌐  Idioma / Language",
        "option_help": "❓  O que é isso? Como funciona?",
        "option_exit": "🚪  Sair",
        "choose": "Digite o número da opção e aperte Enter",
        "current_lang": "atual: Português 🇧🇷",
        "help_body": (
            "[bold]O que é um mapa astral?[/]\n"
            "É um retrato do céu no exato momento em que você nasceu. "
            "A partir dele a gente te conta sobre sua personalidade, "
            "seus talentos e seus caminhos.\n\n"
            "[bold]O que você precisa ter em mãos:[/]\n"
            "  📅  Data de nascimento\n"
            "  ⏰  Horário (se não souber, tudo bem — aperta Enter!)\n"
            "  🏙️   Cidade onde nasceu\n\n"
            "[dim]Nada é enviado para lugar nenhum: as contas acontecem "
            "aqui mesmo, no seu computador. ✨[/]"
        ),
        "name": "Como você se chama?",
        "back": "Pressione Enter para voltar ao menu",
        "close": "Pressione Enter para fechar esta janela ✨",
        "bye": "Até logo! Que as estrelas te guiem 🌟",
        "geocoding": "Procurando essa cidade no mapa…",
        "calculating": "Consultando as estrelas e fazendo as contas…",
        "city_not_found": "Hmm, não achei essa cidade. Tenta de novo — "
                          "pode escrever com estado ou país junto!",
        "geo_error": "Tive um problema ao localizar essa cidade",
        "offline_tip": "Dica: sem internet? Use --lat, --lon e --tz.",
        "calc_error": "Ops, algo deu errado nos cálculos",
    },
    "en": {
        "option_chart": "🌟  Create my birth chart",
        "option_synastry": "💞  Compare two charts (synastry)",
        "option_lang": "🌐  Language / Idioma",
        "option_help": "❓  What is this? How does it work?",
        "option_exit": "🚪  Quit",
        "choose": "Type the option number and press Enter",
        "current_lang": "current: English 🇬🇧",
        "help_body": (
            "[bold]What is a birth chart?[/]\n"
            "It's a snapshot of the sky at the exact moment you were born. "
            "From it we tell you about your personality, your talents, "
            "and your paths.\n\n"
            "[bold]What you'll need:[/]\n"
            "  📅  Date of birth\n"
            "  ⏰  Time of birth (no idea? press Enter, it's fine!)\n"
            "  🏙️   City of birth\n\n"
            "[dim]Nothing is sent anywhere: all the math happens "
            "right here, on your computer. ✨[/]"
        ),
        "name": "What's your name?",
        "back": "Press Enter to go back to the menu",
        "close": "Press Enter to close this window ✨",
        "bye": "See you! May the stars guide you 🌟",
        "geocoding": "Finding that city on the map…",
        "calculating": "Consulting the stars and doing the math…",
        "city_not_found": "Hmm, couldn't find that city. Try again — "
                          "you can add state or country!",
        "geo_error": "I had trouble locating that city",
        "offline_tip": "Tip: offline? Use --lat, --lon and --tz.",
        "calc_error": "Oops, something went wrong with the calculations",
    },
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cyber-astra",
        description="🔮 Cyber Astra — seu mapa astral na linha de comando",
    )
    parser.add_argument("--name", "-n", help="Nome da pessoa")
    parser.add_argument("--date", "-d",
                        help="Data de nascimento (15/06/1990 ou 15061990)")
    parser.add_argument("--time", "-t",
                        help="Horário de nascimento (14:30 ou 1430)")
    parser.add_argument("--location", "-l",
                        help="Local de nascimento (cidade, país)")
    parser.add_argument("--lang", choices=["pt", "en"], default="pt",
                        help="Idioma do relatório (padrão: pt)")
    parser.add_argument("--no-wheel", action="store_true",
                        help="Pula o diagrama da roda")
    parser.add_argument("--only", choices=SECTIONS, default=None,
                        help="Exibe apenas uma seção")
    parser.add_argument("--lat", type=float, default=None,
                        help="Latitude manual (modo offline)")
    parser.add_argument("--lon", type=float, default=None,
                        help="Longitude manual (modo offline)")
    parser.add_argument("--tz", default=None,
                        help="Timezone manual, ex: America/Sao_Paulo (offline)")
    parser.add_argument("--app-mode", action="store_true",
                        help=argparse.SUPPRESS)
    return parser


# ── Coleta de dados ──────────────────────────────────────────────────────────

def _collect_menu_inputs(L: dict, prefix: str = "") -> dict:
    """Friendly questionnaire for the menu flow."""
    who = f"[bright_magenta]{prefix}[/] " if prefix else ""
    name = Prompt.ask(f"{who}[bold]😊 {L['name']}[/]", console=console)
    year, month, day = prompts.ask_date(console)
    hour, minute = prompts.ask_time(console)
    location_label, geo = prompts.ask_location(console)
    return {
        "name": name, "year": year, "month": month, "day": day,
        "hour": hour, "minute": minute,
        "location_label": location_label, "geo": geo,
    }


def _collect_flag_inputs(args) -> dict:
    """Flags mode: prompt (friendly) only for what's missing."""
    name = args.name or Prompt.ask("[bold]Nome da pessoa[/]", console=console)

    if args.date:
        year, month, day = prompts.parse_date_flexible(args.date)
    else:
        year, month, day = prompts.ask_date(console)

    if args.time:
        hour, minute = prompts.parse_time_flexible(args.time)
    else:
        hour, minute = prompts.ask_time(console)

    if args.lat is not None and args.lon is not None:
        geo = {
            "display_name": args.location or "Coordenadas manuais",
            "lat": args.lat, "lon": args.lon,
            "timezone": args.tz or "UTC", "raw": {},
        }
        return {"name": name, "year": year, "month": month, "day": day,
                "hour": hour, "minute": minute,
                "location_label": geo["display_name"], "geo": geo}

    if args.location:
        location_label, geo = args.location, None
    else:
        location_label, geo = prompts.ask_location(console)
    return {"name": name, "year": year, "month": month, "day": day,
            "hour": hour, "minute": minute,
            "location_label": location_label, "geo": geo}


def _resolve_geo(data: dict, L: dict) -> dict | None:
    """Geocode the typed city (with retries) unless already resolved."""
    if data["geo"] is not None:
        return data["geo"]
    while True:
        with animations.stargazing(console, L["geocoding"]):
            try:
                return geocoder.geocode(data["location_label"])
            except ValueError:
                console.print(f"[yellow]{L['city_not_found']}[/]")
                data["location_label"] = Prompt.ask(
                    "[bold]🏙️  Cidade[/]", console=console)
            except Exception as e:
                console.print(f"[red]{L['geo_error']}:[/] {e}")
                console.print(f"[dim]{L['offline_tip']}[/]")
                return None


# ── Relatório ────────────────────────────────────────────────────────────────

def compute_chart(data: dict, L: dict):
    """Resolve geo + calculate the chart. Returns (chart, geo) or None."""
    geo = _resolve_geo(data, L)
    if geo is None:
        return None
    with animations.stargazing(console, L["calculating"]):
        try:
            chart = calculate(
                name=data["name"],
                year=data["year"], month=data["month"], day=data["day"],
                hour=data["hour"], minute=data["minute"],
                lat=geo["lat"], lon=geo["lon"],
                tz_str=geo["timezone"],
            )
        except Exception as e:
            console.print(f"[red]{L['calc_error']}:[/] {e}")
            return None
    return chart, geo


def run_report(data: dict, lang: str, only: str | None = None,
               no_wheel: bool = False, animate: bool = False) -> bool:
    """Compute and display the chart. Returns False on failure."""
    L = MENU[lang]

    result = compute_chart(data, L)
    if result is None:
        return False
    chart, geo = result

    birth_str = (f"{data['day']:02d}/{data['month']:02d}/{data['year']}"
                 f"  {data['hour']:02d}:{data['minute']:02d}"
                 f"  —  {data['location_label']}")

    display.show_header(data["name"], birth_str, lang)
    display.show_location(geo, lang)

    if only == "wheel" or (only is None and not no_wheel):
        wheel_str = wheel.render(chart)
        if animate:
            with console.capture() as cap:
                display.show_wheel(wheel_str)
            animations.reveal_lines(console, cap.get().rstrip())
        else:
            display.show_wheel(wheel_str)

    if only is None or only == "planets":
        display.show_planet_table(chart, lang)
    if only is None or only == "synthesis":
        display.show_synthesis(chart, lang)
    if only is None or only == "aspects":
        display.show_aspects(chart, lang)
    if only is None or only == "insights":
        display.show_insights(chart, lang)
    if only is None or only == "houses":
        display.show_house_meanings(chart, lang)

    console.print()
    console.rule("[dim]✨ Fim do relatório ✨[/]" if lang == "pt"
                 else "[dim]✨ End of report ✨[/]")
    console.print()
    return True


# ── Menu ─────────────────────────────────────────────────────────────────────

def _show_menu(lang: str) -> None:
    L = MENU[lang]
    table = Table(box=None, show_header=False, pad_edge=False)
    table.add_column(style="bold cyan", justify="right", width=4)
    table.add_column()
    table.add_row("1", L["option_chart"])
    table.add_row("2", L["option_synastry"])
    table.add_row("3", f"{L['option_lang']}  [dim]({L['current_lang']})[/]")
    table.add_row("4", L["option_help"])
    table.add_row("5", L["option_exit"])
    console.print(Panel(table, border_style="bright_magenta",
                        padding=(1, 4), expand=False))


def run_synastry(lang: str) -> bool:
    """Collect two people, compute both charts, show the synastry report."""
    L = MENU[lang]
    p1 = "Pessoa 1 —" if lang == "pt" else "Person 1 —"
    p2 = "Pessoa 2 —" if lang == "pt" else "Person 2 —"

    console.print(f"\n[bold bright_magenta]{L['option_synastry']}[/]\n")
    data_a = _collect_menu_inputs(L, prefix=p1)
    console.print()
    data_b = _collect_menu_inputs(L, prefix=p2)

    result_a = compute_chart(data_a, L)
    result_b = compute_chart(data_b, L)
    if result_a is None or result_b is None:
        return False

    display.show_synastry(result_a[0], result_b[0], lang)
    console.print()
    console.rule("[dim]✨ Fim da sinastria ✨[/]" if lang == "pt"
                 else "[dim]✨ End of synastry ✨[/]")
    console.print()
    return True


def run_menu(lang: str = "pt", app_mode: bool = False) -> None:
    animations.twinkle_banner(console, lang=lang)
    while True:
        L = MENU[lang]
        _show_menu(lang)
        choice = Prompt.ask(f"[bold bright_magenta]{L['choose']}[/]",
                            choices=["1", "2", "3", "4", "5"], default="1",
                            console=console, show_choices=False)
        if choice == "1":
            console.print(art.render(art.section("chart")))
            data = _collect_menu_inputs(L)
            console.print()
            run_report(data, lang, animate=True)
            Prompt.ask(f"\n[bold magenta]{L['back']}[/]",
                       default="", show_default=False, console=console)
            console.print()
        elif choice == "2":
            console.print(art.render(art.section("synastry")))
            run_synastry(lang)
            Prompt.ask(f"\n[bold magenta]{L['back']}[/]",
                       default="", show_default=False, console=console)
            console.print()
        elif choice == "3":
            lang = "en" if lang == "pt" else "pt"
        elif choice == "4":
            console.print(art.render(art.section("help"), style="cyan"))
            console.print(Panel(L["help_body"], border_style="cyan",
                                padding=(1, 4), expand=False))
            console.print()
        else:
            console.print(art.render(art.section("exit")))
            console.print(f"\n[bold bright_magenta]{L['bye']}[/]\n")
            if app_mode:
                Prompt.ask(f"[bold magenta]{MENU[lang]['close']}[/]",
                           default="", show_default=False, console=console)
            return


# ── Entrada ──────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)

    menu_mode = args.app_mode or (
        argv is None and len(sys.argv) == 1
    ) or argv == []

    if menu_mode:
        run_menu(lang=args.lang, app_mode=args.app_mode)
        return

    try:
        data = _collect_flag_inputs(args)
    except prompts.InvalidInput as e:
        console.print(f"[red]Erro:[/] {e}")
        sys.exit(1)

    ok = run_report(data, args.lang, only=args.only,
                    no_wheel=args.no_wheel, animate=console.is_terminal)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
