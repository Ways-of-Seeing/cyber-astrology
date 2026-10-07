"""
Synastry: cross-chart aspects, shared traits and couple synthesis.

Reuses the aspect geometry from `synthesis` and the interpretation
datasets from `data.synastry` — no new dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass

from .data import ASPECTS, SIGN_ELEMENT
from .data.synastry import (
    ELEMENT_PAIRS,
    SAME_SIGN,
    SYNASTRY_DYNAMICS,
    SYNASTRY_THEMES,
    VERDICTS,
)
from .engine import Chart
from .synthesis import _angular_distance, element_balance, moon_phase

_ASPECT_POINTS = [
    "sun", "moon", "mercury", "venus", "mars",
    "jupiter", "saturn", "ascendant",
]

# Pairs highlighted in the "chemistry" panels (same point on both charts
# plus the classic Venus × Mars cross).
_KEY_PAIRS = [
    ("sun", "sun"), ("moon", "moon"), ("venus", "venus"),
    ("mars", "mars"), ("venus", "mars"),
]

# Same-sign traits worth reporting, in order.
_SAME_SIGN_POINTS = ["sun", "moon", "ascendant", "venus", "mercury", "mars"]

_POINT_LABEL = {
    "sun": {"pt": "Sol", "en": "Sun"},
    "moon": {"pt": "Lua", "en": "Moon"},
    "mercury": {"pt": "Mercúrio", "en": "Mercury"},
    "venus": {"pt": "Vênus", "en": "Venus"},
    "mars": {"pt": "Marte", "en": "Mars"},
    "ascendant": {"pt": "Ascendente", "en": "Ascendant"},
}


@dataclass
class CrossAspect:
    """An aspect between a point of chart A and a point of chart B."""

    key: str
    symbol: str
    harmony: str        # "fusion" | "soft" | "hard"
    point_a: str
    point_b: str
    orb: float

    def label(self, chart_a: Chart, chart_b: Chart, lang: str) -> str:
        pa = chart_a.all_points()[self.point_a]
        pb = chart_b.all_points()[self.point_b]
        return (f"{pa.symbol} {pa.name(lang)} ({chart_a.name}) "
                f"{self.symbol} "
                f"{pb.symbol} {pb.name(lang)} ({chart_b.name})")


def cross_aspects(chart_a: Chart, chart_b: Chart) -> list[CrossAspect]:
    """Aspects between chart A and chart B points, sorted by orb."""
    points_a = chart_a.all_points()
    points_b = chart_b.all_points()
    found: list[CrossAspect] = []

    for ka in _ASPECT_POINTS:
        for kb in _ASPECT_POINTS:
            pa, pb = points_a.get(ka), points_b.get(kb)
            if not pa or not pb:
                continue
            dist = _angular_distance(pa.longitude, pb.longitude)
            for key, spec in ASPECTS.items():
                orb = abs(dist - spec["angle"])
                if orb <= spec["orb"]:
                    found.append(CrossAspect(
                        key=key, symbol=spec["symbol"],
                        harmony=spec["harmony"],
                        point_a=ka, point_b=kb, orb=orb,
                    ))
                    break

    return sorted(found, key=lambda a: a.orb)


def shared_traits(chart_a: Chart, chart_b: Chart, lang: str = "pt") -> list[str]:
    """Notable things the two charts have in common, as ready-to-print texts."""
    traits: list[str] = []
    points_a = chart_a.all_points()
    points_b = chart_b.all_points()

    # Same point, same sign.
    for key in _SAME_SIGN_POINTS:
        pa, pb = points_a.get(key), points_b.get(key)
        if pa and pb and pa.sign_key == pb.sign_key:
            text = SAME_SIGN[key][lang if lang in ("pt", "en") else "pt"]
            traits.append(text.format(sign=pa.sign_name(lang)))

    # Same dominant element.
    dom_a = max(element_balance(chart_a), key=element_balance(chart_a).get)
    dom_b = max(element_balance(chart_b), key=element_balance(chart_b).get)
    if dom_a == dom_b:
        from .data import ELEMENTS
        nome = ELEMENTS[dom_a][lang if lang in ("pt", "en") else "pt"]["nome"]
        if lang == "pt":
            traits.append(f"Os dois têm {nome} como elemento dominante: "
                          "a energia de fundo de vocês é a mesma — sintonia de ritmo natural.")
        else:
            traits.append(f"You both have {nome} as dominant element: "
                          "your background energy is the same — a natural rhythm attunement.")

    # Same natal Moon phase.
    if moon_phase(chart_a, lang)["key"] == moon_phase(chart_b, lang)["key"]:
        phase = moon_phase(chart_a, lang)
        if lang == "pt":
            traits.append(f"Os dois nasceram na mesma fase da lua ({phase['symbol']} "
                          f"{phase['nome']}): os ciclos de vida de vocês batem no mesmo compasso.")
        else:
            traits.append(f"You were both born under the same moon phase "
                          f"({phase['symbol']} {phase['nome']}): your life cycles beat in the same time.")

    return traits


def couple_verdict(aspects: list[CrossAspect], lang: str = "pt") -> dict:
    """Overall verdict from the harmony × tension balance."""
    soft = sum(1 for a in aspects if a.harmony == "soft")
    hard = sum(1 for a in aspects if a.harmony == "hard")

    if soft >= hard * 1.5:
        key = "harmonious"
    elif hard >= soft * 1.5:
        key = "intense"
    else:
        key = "balanced"

    v = VERDICTS[key]
    lang = lang if lang in ("pt", "en") else "pt"
    return {
        "key": key,
        "titulo": v["titulo"][lang],
        "texto": v[lang],
        "soft": soft,
        "hard": hard,
        "fusion": sum(1 for a in aspects if a.harmony == "fusion"),
    }


def key_pair_chemistry(chart_a: Chart, chart_b: Chart,
                       lang: str = "pt") -> list[dict]:
    """Element-pair chemistry for the key point pairs."""
    points_a = chart_a.all_points()
    points_b = chart_b.all_points()
    panels: list[dict] = []

    for ka, kb in _KEY_PAIRS:
        pa, pb = points_a.get(ka), points_b.get(kb)
        if not pa or not pb:
            continue
        el_a = SIGN_ELEMENT[pa.sign_key]
        el_b = SIGN_ELEMENT[pb.sign_key]
        text = ELEMENT_PAIRS[frozenset({el_a, el_b})]
        label_a = _POINT_LABEL[ka][lang if lang in ("pt", "en") else "pt"]
        label_b = _POINT_LABEL[kb][lang if lang in ("pt", "en") else "pt"]
        if lang == "pt":
            title = (f"{pa.symbol} {label_a} de {chart_a.name} em {pa.sign_pt}"
                     f"  ×  {pb.symbol} {label_b} de {chart_b.name} em {pb.sign_pt}")
        else:
            title = (f"{pa.symbol} {chart_a.name}'s {label_a} in {pa.sign_name(lang)}"
                     f"  ×  {pb.symbol} {chart_b.name}'s {label_b} in {pb.sign_name(lang)}")
        panels.append({"title": title, "body": text[lang if lang in ("pt", "en") else "pt"]})

    return panels


def cross_narrative(aspect: CrossAspect, chart_a: Chart, chart_b: Chart,
                    lang: str = "pt") -> str:
    """Rich text for one cross-aspect."""
    lang = lang if lang in ("pt", "en") else "pt"
    general = ASPECTS[aspect.key][lang]["descricao"]
    theme_a = SYNASTRY_THEMES[aspect.point_a][lang]
    theme_b = SYNASTRY_THEMES[aspect.point_b][lang]
    dynamic = SYNASTRY_DYNAMICS[aspect.key][lang].format(
        p1=theme_a, n1=chart_a.name, p2=theme_b, n2=chart_b.name)
    return f"{general}\n\n{dynamic[0].upper() + dynamic[1:]}"
