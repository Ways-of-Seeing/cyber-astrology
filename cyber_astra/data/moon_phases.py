# coding: utf-8
"""Natal Moon phase interpretations (PT/EN)."""

# Phase is derived from the elongation angle Moon − Sun (0–360°).
MOON_PHASES = [
    {
        "key": "new", "min": 0.0, "max": 45.0, "symbol": "🌑",
        "pt": {
            "nome": "Lua Nova",
            "descricao": "Você nasceu sob a Lua Nova, quando Sol e Lua caminham juntos e a noite está em seu ponto mais escuro — o momento das sementes. Sua vida tende a ser marcada por começos instintivos: você age por impulso vital, sem precisar ver o caminho inteiro antes de andar. Há em você uma fé cega e fecunda no novo. O aprendizado é enxergar o outro e o passado como fontes, não só o futuro.",
        },
        "en": {
            "nome": "New Moon",
            "descricao": "You were born under the New Moon, when Sun and Moon walk together and the night is at its darkest — the time of seeds. Your life tends to be marked by instinctive beginnings: you act from vital impulse, without needing to see the whole path before walking. There is in you a blind and fertile faith in the new. The learning is to see the other and the past as sources, not only the future.",
        },
    },
    {
        "key": "crescent", "min": 45.0, "max": 90.0, "symbol": "🌒",
        "pt": {
            "nome": "Lua Crescente",
            "descricao": "Você nasceu na fase Crescente, quando a primeira luz rompe a escuridão. Sua vida é um movimento contínuo de emergir: vencer a inércia, provar a si mesmo, construir tração. Há coragem silenciosa em você — a da planta que fende a terra. O aprendizado é não confundir luta permanente com identidade: nem tudo precisa ser conquistado à força.",
        },
        "en": {
            "nome": "Crescent Moon",
            "descricao": "You were born in the Crescent phase, when the first light breaks the darkness. Your life is a continuous movement of emerging: overcoming inertia, proving yourself, building traction. There is silent courage in you — that of the plant splitting the soil. The learning is not to confuse permanent struggle with identity: not everything must be won by force.",
        },
    },
    {
        "key": "first_quarter", "min": 90.0, "max": 135.0, "symbol": "🌓",
        "pt": {
            "nome": "Quarto Crescente",
            "descricao": "Você nasceu no Quarto Crescente, a quadratura Sol–Lua: a fase da crise em ação. Seu motor é o desafio — você cresce decidindo, cortando, construindo estruturas sobre o atrito. Tendência a crises produtivas: o impasse aparece para ser atravessado. O aprendizado é escolher as batalhas certas e descansar entre elas.",
        },
        "en": {
            "nome": "First Quarter",
            "descricao": "You were born in the First Quarter, the Sun–Moon square: the phase of crisis in action. Your engine is challenge — you grow by deciding, cutting, building structures over friction. A tendency to productive crises: the impasse appears to be crossed. The learning is choosing the right battles and resting between them.",
        },
    },
    {
        "key": "gibbous", "min": 135.0, "max": 180.0, "symbol": "🌔",
        "pt": {
            "nome": "Lua Gibosa",
            "descricao": "Você nasceu na fase Gibosa, quando a lua quase cheia é lapidada antes do brilho total. Sua vida é feita de refinamento: analisar, ajustar, aperfeiçoar, servir. Você enxerga o que falta — talento raro e valioso. O aprendizado é não deixar o aperfeiçoamento virar autocrítica infinita: o quase também é bonito.",
        },
        "en": {
            "nome": "Gibbous Moon",
            "descricao": "You were born in the Gibbous phase, when the nearly-full moon is polished before its total shine. Your life is made of refinement: analyzing, adjusting, perfecting, serving. You see what is missing — a rare and valuable talent. The learning is not to let perfecting become infinite self-criticism: the almost is also beautiful.",
        },
    },
    {
        "key": "full", "min": 180.0, "max": 225.0, "symbol": "🌕",
        "pt": {
            "nome": "Lua Cheia",
            "descricao": "Você nasceu sob a Lua Cheia, o ponto máximo de luz: Sol e Lua frente a frente, tudo iluminado. Sua vida pede consciência e relação — você se descobre no espelho do outro e nos ciclos de culminância. Tendência a viver em grandes contrastes, com clareza repentina sobre as coisas. O aprendizado é integrar os polos em vez de oscilar entre eles.",
        },
        "en": {
            "nome": "Full Moon",
            "descricao": "You were born under the Full Moon, the peak of light: Sun and Moon face to face, everything illuminated. Your life asks for awareness and relationship — you discover yourself in the mirror of the other and in cycles of culmination. A tendency to live in great contrasts, with sudden clarity about things. The learning is to integrate the poles instead of swinging between them.",
        },
    },
    {
        "key": "disseminating", "min": 225.0, "max": 270.0, "symbol": "🌖",
        "pt": {
            "nome": "Lua Minguante Gibosa",
            "descricao": "Você nasceu na fase de disseminação, quando a luz colhida começa a ser partilhada. Sua vida é feita de transmitir: ensinar, comunicar, distribuir o que aprendeu. Há em você um mensageiro nato, alguém que dá sentido às experiências ao contá-las. O aprendizado é filtrar: nem tudo precisa ser dito, nem todos precisam ouvir tudo.",
        },
        "en": {
            "nome": "Disseminating Moon",
            "descricao": "You were born in the disseminating phase, when the harvested light begins to be shared. Your life is made of transmitting: teaching, communicating, distributing what you learned. There is a born messenger in you, someone who gives meaning to experiences by telling them. The learning is to filter: not everything needs to be said, not everyone needs to hear everything.",
        },
    },
    {
        "key": "last_quarter", "min": 270.0, "max": 315.0, "symbol": "🌗",
        "pt": {
            "nome": "Quarto Minguante",
            "descricao": "Você nasceu no Quarto Minguante, a segunda quadratura Sol–Lua: a crise de consciência. Sua vida é marcada por revisões profundas — questionar estruturas herdadas, reorientar valores, desconstruir para reconstruir. Você carrega um espírito de transição, ponte entre o velho e o novo. O aprendizado é não romper por romper: discernir o que merece continuar.",
        },
        "en": {
            "nome": "Last Quarter",
            "descricao": "You were born in the Last Quarter, the second Sun–Moon square: the crisis of consciousness. Your life is marked by deep revisions — questioning inherited structures, reorienting values, deconstructing to rebuild. You carry a spirit of transition, a bridge between old and new. The learning is not to break for breaking's sake: discerning what deserves to continue.",
        },
    },
    {
        "key": "balsamic", "min": 315.0, "max": 360.0, "symbol": "🌘",
        "pt": {
            "nome": "Lua Balsâmica",
            "descricao": "Você nasceu na fase Balsâmica, a última luz antes da escuridão renovadora: a fase das sementes do futuro. Sua vida tem um tom de encerramento e visão — soltar, perdoar, curar e sonhar o próximo ciclo. Há em você uma sabedoria antiga e uma intuição do que está por vir. O aprendizado é não viver só no porvir: o presente também é seu lar.",
        },
        "en": {
            "nome": "Balsamic Moon",
            "descricao": "You were born in the Balsamic phase, the last light before the renewing darkness: the phase of the seeds of the future. Your life has a tone of closure and vision — releasing, forgiving, healing, and dreaming the next cycle. There is in you an ancient wisdom and an intuition of what is to come. The learning is not to live only in what lies ahead: the present is also your home.",
        },
    },
]

# Big Three narrative templates (procedural synthesis).
BIG_THREE = {
    "pt": {
        "titulo": "Os Três Grandes — Sol, Lua e Ascendente",
        "template": (
            "Sua essência é {sun} (Sol): é nesse signo que moram seu propósito e sua vitalidade — "
            "o que você veio se tornar. Suas emoções falam {moon} (Lua): é assim que você se nutre, "
            "reage e busca conforto quando ninguém está olhando. E o mundo te conhece primeiro como "
            "{asc} (Ascendente): sua porta de entrada, o estilo com que você inicia tudo. "
            "{combo}"
        ),
        "combos": {
            "same": "Como os três coincidem em {sign}, sua personalidade é concentrada e direta: quem te vê, te vê por inteiro.",
            "two_same": "Com {s1} e {s2} em {sign}, há uma forte coerência entre {what}: uma parte grande de você fala a mesma língua.",
            "all_diff": "Com três signos diferentes, você é um mapa plural: essência, emoção e aparência trazem tons distintos — uma riqueza que pede integração consciente.",
        },
    },
    "en": {
        "titulo": "The Big Three — Sun, Moon and Ascendant",
        "template": (
            "Your essence is {sun} (Sun): this is where your purpose and vitality live — "
            "what you came to become. Your emotions speak {moon} (Moon): this is how you nourish yourself, "
            "react, and seek comfort when no one is watching. And the world meets you first as "
            "{asc} (Ascendant): your front door, the style with which you begin everything. "
            "{combo}"
        ),
        "combos": {
            "same": "Since all three coincide in {sign}, your personality is concentrated and direct: whoever sees you, sees all of you.",
            "two_same": "With {s1} and {s2} in {sign}, there is a strong coherence between {what}: a large part of you speaks the same language.",
            "all_diff": "With three different signs, you are a plural map: essence, emotion, and appearance bring distinct tones — a richness that asks for conscious integration.",
        },
    },
}


def get_moon_phase(elongation: float, lang: str = "pt") -> dict:
    """Return the phase entry for a Moon−Sun elongation (0–360)."""
    for phase in MOON_PHASES:
        if phase["min"] <= elongation < phase["max"]:
            return {**phase.get(lang, phase["pt"]), "symbol": phase["symbol"], "key": phase["key"]}
    return {**MOON_PHASES[0].get(lang, MOON_PHASES[0]["pt"]),
            "symbol": MOON_PHASES[0]["symbol"], "key": MOON_PHASES[0]["key"]}
