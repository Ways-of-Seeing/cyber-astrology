# coding: utf-8
"""Aspect interpretations (PT/EN) and lookup tables for aspect computation."""

# Orb definitions: angle in degrees, max orb in degrees.
ASPECTS = {
    "conjunction": {
        "angle": 0, "orb": 8, "symbol": "☌", "harmony": "fusion",
        "pt": {
            "nome": "Conjunção",
            "descricao": "Duas forças fundidas numa só. Os planetas em conjunção agem como um único princípio: não se separam, não se relativizam. É um ponto de concentração intensa de energia no mapa — poderoso, mas que pode cegar para outras perspectivas.",
            "dinamica": "{p1} e {p2} caminham colados: onde um age, o outro responde junto. Essa fusão amplifica ambos e pede consciência para não virar excesso.",
        },
        "en": {
            "nome": "Conjunction",
            "descricao": "Two forces fused into one. Planets in conjunction act as a single principle: they cannot be separated or relativized. It is a point of intense energy concentration in the chart — powerful, but potentially blinding to other perspectives.",
            "dinamica": "{p1} and {p2} walk side by side: where one acts, the other answers. This fusion amplifies both and asks for awareness so it does not become excess.",
        },
    },
    "sextile": {
        "angle": 60, "orb": 5, "symbol": "⚹", "harmony": "soft",
        "pt": {
            "nome": "Sextil",
            "descricao": "Um aspecto de oportunidade e cooperação. Os planetas em sextil se apoiam com leveza: o talento existe, mas precisa ser exercitado para florescer. É a porta que se abre quando você se move.",
            "dinamica": "{p1} e {p2} colaboram com facilidade: um oferece ao outro caminhos práticos de expressão. Cultivar essa parceria traz resultados naturais.",
        },
        "en": {
            "nome": "Sextile",
            "descricao": "An aspect of opportunity and cooperation. Planets in sextile support each other lightly: the talent exists, but it must be exercised to bloom. It is the door that opens when you move.",
            "dinamica": "{p1} and {p2} cooperate easily: one offers the other practical paths of expression. Cultivating this partnership brings natural results.",
        },
    },
    "square": {
        "angle": 90, "orb": 7, "symbol": "□", "harmony": "hard",
        "pt": {
            "nome": "Quadratura",
            "descricao": "Um aspecto de tensão criativa. Os planetas em quadratura disputam espaço: cada um puxa para um lado, gerando atrito — e é justamente o atrito que produz movimento, ambição e crescimento. É onde a vida te provoca a evoluir.",
            "dinamica": "{p1} e {p2} vivem em negociação difícil: o conflito entre eles é um motor. Integrá-los, em vez de escolher um, transforma tensão em realização.",
        },
        "en": {
            "nome": "Square",
            "descricao": "An aspect of creative tension. Planets in square compete for space: each pulls in its own direction, creating friction — and it is precisely friction that produces movement, ambition, and growth. This is where life provokes you to evolve.",
            "dinamica": "{p1} and {p2} live in hard negotiation: the conflict between them is an engine. Integrating them, rather than choosing one, turns tension into achievement.",
        },
    },
    "trine": {
        "angle": 120, "orb": 7, "symbol": "△", "harmony": "soft",
        "pt": {
            "nome": "Trígono",
            "descricao": "Um aspecto de fluidez e graça. Os planetas em trígono conversam no mesmo elemento: a energia circula sem esforço, como um dom que sempre esteve lá. O risco é tomar esse talento como garantido e não desenvolvê-lo.",
            "dinamica": "{p1} e {p2} fluem juntos sem atrito: é um canal de talento natural. Dar uso consciente a essa harmonia a transforma de conforto em mestria.",
        },
        "en": {
            "nome": "Trine",
            "descricao": "An aspect of flow and grace. Planets in trine speak the same element: energy circulates effortlessly, like a gift that was always there. The risk is taking this talent for granted and never developing it.",
            "dinamica": "{p1} and {p2} flow together without friction: a channel of natural talent. Putting this harmony to conscious use turns comfort into mastery.",
        },
    },
    "opposition": {
        "angle": 180, "orb": 8, "symbol": "☍", "harmony": "hard",
        "pt": {
            "nome": "Oposição",
            "descricao": "Um aspecto de polaridade e espelho. Os planetas em oposição se encaram de pontos opostos do mapa: cada um mostra ao outro o que lhe falta. A lição é o equilíbrio — oscilar entre os polos gera projeção; integrá-los gera plenitude.",
            "dinamica": "{p1} e {p2} se espelham à distância: você tende a viver um e projetar o outro nas pessoas. Reconhecer os dois como seus é o trabalho de uma vida — e vale a pena.",
        },
        "en": {
            "nome": "Opposition",
            "descricao": "An aspect of polarity and mirror. Planets in opposition face each other from opposite points of the chart: each shows the other what it lacks. The lesson is balance — swinging between poles creates projection; integrating them creates wholeness.",
            "dinamica": "{p1} and {p2} mirror each other from afar: you tend to live one and project the other onto people. Recognizing both as yours is the work of a lifetime — and worth it.",
        },
    },
}

# Order used when sorting aspects for display (most exact first anyway).
HARMONY_ORDER = {"fusion": 0, "soft": 1, "hard": 2}

# Planet "themes": short phrases used to compose aspect narratives.
PLANET_THEMES = {
    "sun":       {"pt": "sua identidade e propósito", "en": "your identity and purpose"},
    "moon":      {"pt": "suas emoções e necessidades", "en": "your emotions and needs"},
    "mercury":   {"pt": "sua mente e comunicação", "en": "your mind and communication"},
    "venus":     {"pt": "sua forma de amar e valorizar", "en": "your way of loving and valuing"},
    "mars":      {"pt": "sua ação e desejo", "en": "your action and desire"},
    "jupiter":   {"pt": "sua expansão e fé na vida", "en": "your expansion and faith in life"},
    "saturn":    {"pt": "sua disciplina e limites", "en": "your discipline and boundaries"},
    "uranus":    {"pt": "sua originalidade e rupturas", "en": "your originality and ruptures"},
    "neptune":   {"pt": "sua imaginação e transcendência", "en": "your imagination and transcendence"},
    "pluto":     {"pt": "sua transformação e poder", "en": "your transformation and power"},
    "ascendant": {"pt": "sua máscara e iniciativa", "en": "your mask and initiative"},
    "mc":        {"pt": "sua vocação e imagem pública", "en": "your vocation and public image"},
}


def get_aspect(aspect_key: str, lang: str = "pt") -> dict | None:
    entry = ASPECTS.get(aspect_key)
    if entry:
        return entry.get(lang, entry.get("pt"))
    return None
