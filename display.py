# coding: utf-8
"""
Rich-powered terminal display for the natal chart report.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich import box
from data import get_planet_sign, get_house

console = Console()

PLANET_COLOR = {
    "sun":      "yellow",
    "moon":     "bright_blue",
    "mercury":  "green",
    "venus":    "magenta",
    "mars":     "red",
    "jupiter":  "orange3",
    "saturn":   "dark_olive_green3",
    "uranus":   "cyan",
    "neptune":  "blue",
    "pluto":    "dark_red",
    "ascendant":"bright_white",
    "mc":       "bright_white",
}

LABELS = {
    "pt": {
        "chart_title": "MAPA ASTRAL",
        "location_report": "📍 Localização Geocodificada",
        "planets_title": "🪐 POSIÇÕES PLANETÁRIAS",
        "planet": "Planeta",
        "sign": "Signo",
        "degree": "Grau",
        "house": "Casa",
        "retro": "R",
        "insights_title": "✨ INSIGHTS ASTROLÓGICOS",
        "strengths": "Pontos Fortes",
        "guidelines": "Diretrizes de Vida",
        "challenges": "Desafios",
        "house_meaning": "🏠 SIGNIFICADO DAS CASAS COM PLANETAS",
        "in_house": "na Casa",
        "retrograde": "Retrógrado",
        "no_data": "[italic dim]Interpretação não disponível[/]",
    },
    "en": {
        "chart_title": "NATAL CHART",
        "location_report": "📍 Geocoded Location",
        "planets_title": "🪐 PLANETARY POSITIONS",
        "planet": "Planet",
        "sign": "Sign",
        "degree": "Degree",
        "house": "House",
        "retro": "R",
        "insights_title": "✨ ASTROLOGICAL INSIGHTS",
        "strengths": "Strengths",
        "guidelines": "Life Guidelines",
        "challenges": "Challenges",
        "house_meaning": "🏠 HOUSE MEANINGS WITH PLANETS",
        "in_house": "in House",
        "retrograde": "Retrograde",
        "no_data": "[italic dim]Interpretation not available[/]",
    },
}


def show_header(name: str, birth_str: str, lang: str = "pt"):
    L = LABELS[lang]
    console.print()
    console.print(
        Panel(
            f"[bold yellow]{name}[/]\n[dim]{birth_str}[/]",
            title=f"[bold cyan]{L['chart_title']}[/]",
            border_style="cyan",
            expand=True,
        )
    )


def show_location(geo: dict, lang: str = "pt"):
    L = LABELS[lang]
    console.print()
    console.print(
        Panel(
            f"[green]{geo['display_name']}[/]\n"
            f"[dim]Latitude:[/] [white]{geo['lat']:.4f}°[/]   "
            f"[dim]Longitude:[/] [white]{geo['lon']:.4f}°[/]   "
            f"[dim]Timezone:[/] [white]{geo['timezone']}[/]",
            title=L["location_report"],
            border_style="green",
            expand=False,
        )
    )


def show_wheel(wheel_str: str):
    console.print()
    console.print(Panel(wheel_str, title="[bold cyan]Roda Natal[/]",
                        border_style="cyan", expand=True))


def show_planet_table(chart_data: dict, lang: str = "pt"):
    L = LABELS[lang]
    console.print()
    table = Table(
        title=L["planets_title"],
        box=box.SIMPLE_HEAD,
        header_style="bold cyan",
        show_lines=False,
    )
    table.add_column(L["planet"], style="bold", min_width=14)
    table.add_column(L["sign"], min_width=14)
    table.add_column(L["degree"], justify="right", min_width=8)
    table.add_column(L["house"], justify="center", min_width=6)
    table.add_column("", min_width=3)

    sign_field = "sign_pt" if lang == "pt" else "sign_abbr"

    # Ascendant first
    asc = chart_data["ascendant"]
    table.add_row(
        f"[bright_white]{asc['symbol']} {asc['name_' + lang]}[/]",
        f"[bright_white]{asc[sign_field]}[/]",
        f"[bright_white]{asc['degree_in_sign']:.1f}°[/]",
        "1",
        "",
    )

    # MC
    mc = chart_data["mc"]
    table.add_row(
        f"[bright_white]{mc['symbol']} {mc['name_' + lang]}[/]",
        f"[bright_white]{mc[sign_field]}[/]",
        f"[bright_white]{mc['degree_in_sign']:.1f}°[/]",
        "10",
        "",
    )

    table.add_section()

    for key, pdata in sorted(chart_data["planets"].items(),
                              key=lambda kv: kv[1]["longitude"]):
        color = PLANET_COLOR.get(key, "white")
        retro = f"[dim]{L['retro']}[/]" if pdata["retrograde"] else ""
        table.add_row(
            f"[{color}]{pdata['symbol']} {pdata['name_' + lang]}[/]",
            f"[{color}]{pdata[sign_field]}[/]",
            f"[{color}]{pdata['degree_in_sign']:.1f}°[/]",
            f"[{color}]{pdata['house']}[/]",
            retro,
        )

    console.print(table)


def _render_insight(entry: dict, lang: str, color: str):
    """Print a single planet insight panel."""
    if lang == "pt":
        title_key, desc_key, str_key, gui_key, chal_key = (
            "titulo", "descricao", "forcas", "diretrizes", "desafios"
        )
    else:
        title_key, desc_key, str_key, gui_key, chal_key = (
            "title", "description", "strengths", "guidelines", "challenges"
        )

    L = LABELS[lang]
    title = entry.get(title_key, "")
    desc  = entry.get(desc_key, "")
    strengths = entry.get(str_key, [])
    guidelines = entry.get(gui_key, [])
    challenges = entry.get(chal_key, "")

    body_parts = []
    body_parts.append(f"[white]{desc}[/]\n")

    if strengths:
        sl = "  ".join(f"[bold {color}]{s}[/]" for s in strengths)
        body_parts.append(f"[dim]{L['strengths']}:[/] {sl}\n")

    if guidelines:
        body_parts.append(f"\n[bold]{L['guidelines']}:[/]")
        for g in guidelines:
            body_parts.append(f"  [dim]▸[/] {g}")

    if challenges:
        body_parts.append(f"\n[dim]{L['challenges']}:[/] [italic]{challenges}[/]")

    console.print(
        Panel(
            "\n".join(body_parts),
            title=f"[bold {color}]{title}[/]",
            border_style=color,
            expand=True,
        )
    )


def show_insights(chart_data: dict, lang: str = "pt"):
    L = LABELS[lang]
    console.print()
    console.rule(f"[bold cyan]{L['insights_title']}[/]")

    # Order: ascendant, sun, moon, then rest
    ordered_keys = ["ascendant"] + [k for k in [
        "sun", "moon", "mercury", "venus", "mars",
        "jupiter", "saturn", "uranus", "neptune", "pluto"
    ]]

    all_data = {"ascendant": chart_data["ascendant"]}
    all_data.update(chart_data["planets"])

    for key in ordered_keys:
        pdata = all_data.get(key)
        if not pdata:
            continue
        sign_key = pdata["sign_key"]
        entry = get_planet_sign(key, sign_key, lang)
        color = PLANET_COLOR.get(key, "white")
        if entry:
            _render_insight(entry, lang, color)
        else:
            console.print(Panel(L["no_data"],
                                title=f"[{color}]{pdata['symbol']} {pdata['name_pt' if lang == 'pt' else 'name_en']}[/]",
                                border_style=color))


def show_house_meanings(chart_data: dict, lang: str = "pt"):
    L = LABELS[lang]
    console.print()
    console.rule(f"[bold cyan]{L['house_meaning']}[/]")

    # Map house → planets in it
    house_planets: dict[int, list] = {}
    for key, pdata in chart_data["planets"].items():
        h = pdata["house"]
        house_planets.setdefault(h, []).append(pdata)
    # Add ascendant to house 1, mc to house 10
    house_planets.setdefault(1, []).insert(0, chart_data["ascendant"])

    for h_num in sorted(house_planets.keys()):
        planets_here = house_planets[h_num]
        house_entry = get_house(h_num, lang)
        if not house_entry:
            continue
        planet_tags = " ".join(
            f"[bold]{p['symbol']} {p['name_pt' if lang == 'pt' else 'name_en']}[/]"
            for p in planets_here
        )
        if lang == "pt":
            title = house_entry["titulo"]
            desc  = house_entry["descricao"]
        else:
            title = house_entry["title"]
            desc  = house_entry["description"]

        console.print(
            Panel(
                f"{planet_tags}\n\n[white]{desc}[/]",
                title=f"[bold cyan]{title}[/]",
                border_style="cyan",
                expand=True,
            )
        )
