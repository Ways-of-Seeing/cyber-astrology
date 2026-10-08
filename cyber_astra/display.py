# coding: utf-8
"""Rich-powered terminal display for the natal chart report."""

from __future__ import annotations

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from . import art
from . import synthesis
from . import synastry as syn
from .data import ASPECTS, ELEMENTS, MODALITIES, get_house, get_planet_sign
from .engine import Chart

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
    "ascendant": "bright_white",
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
        "synthesis_title": "🌟 SÍNTESE DO MAPA",
        "elements": "Equilíbrio dos Elementos",
        "modalities": "Ritmos (Modalidades)",
        "moon_phase": "Fase da Lua no Nascimento",
        "dominant": "dominante",
        "scarce": "mais escasso",
        "aspects_title": "🔗 ASPECTOS ENTRE PLANETAS",
        "aspect": "Aspecto",
        "orb": "Orbe",
        "nature": "Natureza",
        "harmonious": "Fluido",
        "challenging": "Desafiador",
        "fusing": "Fusão",
        "no_aspects": "Nenhum aspecto maior encontrado dentro das orbes.",
        "synastry_title": "💞 SINASTRIA — MAPAS CRUZADOS",
        "common_traits": "O que vocês têm em comum",
        "chemistry": "Química dos pares-chave",
        "cross_aspects": "Aspectos entre os dois mapas",
        "soft_count": "aspectos fluidos",
        "hard_count": "aspectos desafiadores",
        "fusion_count": "fusões",
        "no_common": "Os mapas de vocês são bem diferentes — e é justamente aí que mora a descoberta.",
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
        "synthesis_title": "🌟 CHART SYNTHESIS",
        "elements": "Elemental Balance",
        "modalities": "Rhythms (Modalities)",
        "moon_phase": "Moon Phase at Birth",
        "dominant": "dominant",
        "scarce": "scarcest",
        "aspects_title": "🔗 PLANETARY ASPECTS",
        "aspect": "Aspect",
        "orb": "Orb",
        "nature": "Nature",
        "harmonious": "Flowing",
        "challenging": "Challenging",
        "fusing": "Fusion",
        "no_aspects": "No major aspects found within orb.",
        "synastry_title": "💞 SYNASTRY — CROSSED CHARTS",
        "common_traits": "What you have in common",
        "chemistry": "Key-pair chemistry",
        "cross_aspects": "Aspects between the two charts",
        "soft_count": "flowing aspects",
        "hard_count": "challenging aspects",
        "fusion_count": "fusions",
        "no_common": "Your charts are quite different — and that's exactly where discovery lives.",
    },
}

_HARMONY_LABEL = {"soft": "harmonious", "hard": "challenging", "fusion": "fusing"}
_HARMONY_COLOR = {"soft": "green", "hard": "red", "fusion": "yellow"}


def _section_art(key: str) -> None:
    """Print a random compact art above a report section."""
    lines = art.section(key)
    if lines:
        console.print(art.render(lines, style="dim magenta"))


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
    _section_art("wheel")
    console.print()
    console.print(Panel(wheel_str, title="[bold cyan]Roda Natal[/]",
                        border_style="cyan", expand=True))


def show_planet_table(chart: Chart, lang: str = "pt"):
    L = LABELS[lang]
    _section_art("planets")
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

    for point in (chart.ascendant, chart.mc):
        table.add_row(
            f"[bright_white]{point.symbol} {point.name(lang)}[/]",
            f"[bright_white]{point.sign_name(lang)}[/]",
            f"[bright_white]{point.degree_in_sign:.1f}°[/]",
            str(point.house),
            "",
        )

    table.add_section()

    for key, pdata in sorted(chart.planets.items(),
                             key=lambda kv: kv[1].longitude):
        color = PLANET_COLOR.get(key, "white")
        retro = f"[dim]{L['retro']}[/]" if pdata.retrograde else ""
        table.add_row(
            f"[{color}]{pdata.symbol} {pdata.name(lang)}[/]",
            f"[{color}]{pdata.sign_name(lang)}[/]",
            f"[{color}]{pdata.degree_in_sign:.1f}°[/]",
            f"[{color}]{pdata.house}[/]",
            retro,
        )

    console.print(table)


def show_synthesis(chart: Chart, lang: str = "pt"):
    """Big Three + element/modality balance + natal Moon phase."""
    L = LABELS[lang]
    _section_art("synthesis")
    console.print()
    console.rule(f"[bold cyan]{L['synthesis_title']}[/]")

    # ── Big Three narrative ─────────────────────────────────────────────────
    console.print(
        Panel(
            f"[white]{synthesis.big_three(chart, lang)}[/]",
            title="[bold yellow]☉ ☽ AC[/]",
            border_style="yellow",
            expand=True,
        )
    )

    # ── Moon phase ──────────────────────────────────────────────────────────
    phase = synthesis.moon_phase(chart, lang)
    console.print(
        Panel(
            f"[white]{phase['descricao']}[/]",
            title=f"[bold bright_blue]{phase['symbol']} {L['moon_phase']}: {phase['nome']}[/]",
            border_style="bright_blue",
            expand=True,
        )
    )

    # ── Element & modality balance ──────────────────────────────────────────
    elements = synthesis.element_balance(chart)
    modalities = synthesis.modality_balance(chart)

    def _balance_lines(counts: dict[str, int], texts: dict, label: str) -> list[str]:
        dominant = max(counts, key=counts.get)
        scarce = min(counts, key=counts.get)
        lines = [f"[bold]{label}[/]"]
        for key, count in counts.items():
            entry = texts[key][lang if lang in ("pt", "en") else "pt"]
            tags = []
            if key == dominant and counts[dominant] != counts[scarce]:
                tags.append(f"[dim]({L['dominant']})[/]")
            if key == scarce and counts[dominant] != counts[scarce]:
                tags.append(f"[dim]({L['scarce']})[/]")
            lines.append(f"  {entry['nome']}: {'●' * count}{'○' * (8 - count)} "
                         f"{count}  {' '.join(tags)}")
        dom_text = texts[dominant][lang if lang in ("pt", "en") else "pt"]
        lines.append(f"\n[white]{dom_text['dominante']}[/]")
        if counts[scarce] <= 1 and counts[dominant] != counts[scarce]:
            scarce_text = texts[scarce][lang if lang in ("pt", "en") else "pt"]
            lines.append(f"\n[dim]{scarce_text['ausente']}[/]")
        return lines

    body = "\n".join(_balance_lines(elements, ELEMENTS, L["elements"]))
    body += "\n\n" + "\n".join(_balance_lines(modalities, MODALITIES, L["modalities"]))

    console.print(
        Panel(
            body,
            title=f"[bold magenta]⚖️ {L['elements']} · {L['modalities']}[/]",
            border_style="magenta",
            expand=True,
        )
    )


def show_aspects(chart: Chart, lang: str = "pt"):
    """Aspect table + narrative panels for the tightest aspects."""
    L = LABELS[lang]
    _section_art("aspects")
    console.print()
    console.rule(f"[bold cyan]{L['aspects_title']}[/]")

    aspects = synthesis.compute_aspects(chart)
    if not aspects:
        console.print(f"[dim]{L['no_aspects']}[/]")
        return

    # ── Summary table ───────────────────────────────────────────────────────
    table = Table(box=box.SIMPLE_HEAD, header_style="bold cyan")
    table.add_column(L["aspect"], min_width=30)
    table.add_column(L["nature"], min_width=12)
    table.add_column(L["orb"], justify="right", min_width=8)

    for asp in aspects:
        spec = ASPECTS[asp.key]
        name = spec[lang if lang in ("pt", "en") else "pt"]["nome"]
        hcolor = _HARMONY_COLOR[asp.harmony]
        nature = L[_HARMONY_LABEL[asp.harmony]]
        table.add_row(
            f"[{hcolor}]{asp.symbol} {name}[/]  {asp.label(chart, lang)}",
            f"[{hcolor}]{nature}[/]",
            f"[dim]{asp.orb:.1f}°[/]",
        )
    console.print(table)

    # ── Narratives for the 3 most exact aspects ─────────────────────────────
    for asp in aspects[:3]:
        spec = ASPECTS[asp.key]
        texts = spec[lang if lang in ("pt", "en") else "pt"]
        hcolor = _HARMONY_COLOR[asp.harmony]
        console.print(
            Panel(
                f"[white]{synthesis.aspect_narrative(asp, chart, lang)}[/]",
                title=f"[bold {hcolor}]{asp.symbol} {texts['nome']} — {asp.label(chart, lang)}[/]",
                border_style=hcolor,
                expand=True,
            )
        )


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
    desc = entry.get(desc_key, "")
    strengths = entry.get(str_key, [])
    guidelines = entry.get(gui_key, [])
    challenges = entry.get(chal_key, "")

    body_parts = [f"[white]{desc}[/]\n"]

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


def show_insights(chart: Chart, lang: str = "pt"):
    L = LABELS[lang]
    _section_art("synthesis")
    console.print()
    console.rule(f"[bold cyan]{L['insights_title']}[/]")

    ordered_keys = [
        "ascendant", "sun", "moon", "mercury", "venus", "mars",
        "jupiter", "saturn", "uranus", "neptune", "pluto",
    ]

    all_data = {"ascendant": chart.ascendant, **chart.planets}

    for key in ordered_keys:
        pdata = all_data.get(key)
        if not pdata:
            continue
        entry = get_planet_sign(key, pdata.sign_key, lang)
        color = PLANET_COLOR.get(key, "white")
        if entry:
            _render_insight(entry, lang, color)
        else:
            console.print(Panel(L["no_data"],
                                title=f"[{color}]{pdata.symbol} {pdata.name(lang)}[/]",
                                border_style=color))


def show_house_meanings(chart: Chart, lang: str = "pt"):
    L = LABELS[lang]
    _section_art("houses")
    console.print()
    console.rule(f"[bold cyan]{L['house_meaning']}[/]")

    house_planets: dict[int, list] = {}
    for pdata in chart.planets.values():
        house_planets.setdefault(pdata.house, []).append(pdata)
    house_planets.setdefault(1, []).insert(0, chart.ascendant)

    for h_num in sorted(house_planets.keys()):
        planets_here = house_planets[h_num]
        house_entry = get_house(h_num, lang)
        if not house_entry:
            continue
        planet_tags = " ".join(
            f"[bold]{p.symbol} {p.name(lang)}[/]" for p in planets_here
        )
        if lang == "pt":
            title = house_entry["titulo"]
            desc = house_entry["descricao"]
        else:
            title = house_entry["title"]
            desc = house_entry["description"]

        console.print(
            Panel(
                f"{planet_tags}\n\n[white]{desc}[/]",
                title=f"[bold cyan]{title}[/]",
                border_style="cyan",
                expand=True,
            )
        )


def show_synastry(chart_a: Chart, chart_b: Chart, lang: str = "pt"):
    """Full synastry report: verdict, shared traits, chemistry, cross aspects."""
    L = LABELS[lang]
    _section_art("synastry")
    console.print()
    console.rule(f"[bold magenta]{L['synastry_title']}[/]")

    # ── Header with both names ──────────────────────────────────────────────
    console.print(
        Panel(
            f"[bold yellow]{chart_a.name}[/]  [bright_magenta]×[/]  "
            f"[bold cyan]{chart_b.name}[/]",
            title=f"[bold bright_magenta]{L['synastry_title']}[/]",
            border_style="bright_magenta",
            expand=True,
        )
    )

    aspects = syn.cross_aspects(chart_a, chart_b)
    verdict = syn.couple_verdict(aspects, lang)

    # ── Verdict panel ───────────────────────────────────────────────────────
    counts = (f"[green]{verdict['soft']} {L['soft_count']}[/]  ·  "
              f"[red]{verdict['hard']} {L['hard_count']}[/]  ·  "
              f"[yellow]{verdict['fusion']} {L['fusion_count']}[/]")
    console.print(
        Panel(
            f"{counts}\n\n[white]{verdict['texto']}[/]",
            title=f"[bold bright_magenta]⚖️ {verdict['titulo']}[/]",
            border_style="bright_magenta",
            expand=True,
        )
    )

    # ── Shared traits ───────────────────────────────────────────────────────
    traits = syn.shared_traits(chart_a, chart_b, lang)
    body = ("\n".join(f"  [dim]▸[/] {t}" for t in traits)
            if traits else f"[dim]{L['no_common']}[/]")
    console.print(
        Panel(
            body,
            title=f"[bold cyan]🤝 {L['common_traits']}[/]",
            border_style="cyan",
            expand=True,
        )
    )

    # ── Key-pair chemistry ──────────────────────────────────────────────────
    for panel in syn.key_pair_chemistry(chart_a, chart_b, lang):
        console.print(
            Panel(
                f"[white]{panel['body']}[/]",
                title=f"[bold yellow]{panel['title']}[/]",
                border_style="yellow",
                expand=True,
            )
        )

    # ── Cross aspects table ─────────────────────────────────────────────────
    if aspects:
        console.print()
        table = Table(title=L["cross_aspects"], box=box.SIMPLE_HEAD,
                      header_style="bold magenta")
        table.add_column(L["aspect"], min_width=38)
        table.add_column(L["nature"], min_width=12)
        table.add_column(L["orb"], justify="right", min_width=8)

        for asp in aspects[:15]:
            spec = ASPECTS[asp.key]
            name = spec[lang if lang in ("pt", "en") else "pt"]["nome"]
            hcolor = _HARMONY_COLOR[asp.harmony]
            table.add_row(
                f"[{hcolor}]{asp.symbol} {name}[/]  {asp.label(chart_a, chart_b, lang)}",
                f"[{hcolor}]{L[_HARMONY_LABEL[asp.harmony]]}[/]",
                f"[dim]{asp.orb:.1f}°[/]",
            )
        console.print(table)

        # ── Narratives for the 3 most exact cross-aspects ───────────────────
        for asp in aspects[:3]:
            spec = ASPECTS[asp.key]
            texts = spec[lang if lang in ("pt", "en") else "pt"]
            hcolor = _HARMONY_COLOR[asp.harmony]
            console.print(
                Panel(
                    f"[white]{syn.cross_narrative(asp, chart_a, chart_b, lang)}[/]",
                    title=f"[bold {hcolor}]{asp.symbol} {texts['nome']} — "
                          f"{asp.label(chart_a, chart_b, lang)}[/]",
                    border_style=hcolor,
                    expand=True,
                )
            )
