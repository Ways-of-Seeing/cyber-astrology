# coding: utf-8
"""Element and modality balance interpretations (PT/EN)."""

SIGN_ELEMENT = {
    "aries": "fire", "leo": "fire", "sagittarius": "fire",
    "taurus": "earth", "virgo": "earth", "capricorn": "earth",
    "gemini": "air", "libra": "air", "aquarius": "air",
    "cancer": "water", "scorpio": "water", "pisces": "water",
}

SIGN_MODALITY = {
    "aries": "cardinal", "cancer": "cardinal", "libra": "cardinal", "capricorn": "cardinal",
    "taurus": "fixed", "leo": "fixed", "scorpio": "fixed", "aquarius": "fixed",
    "gemini": "mutable", "virgo": "mutable", "sagittarius": "mutable", "pisces": "mutable",
}

ELEMENTS = {
    "fire": {
        "symbol": "🔥",
        "pt": {
            "nome": "Fogo",
            "dominante": "O Fogo domina seu mapa: você é movido por entusiasmo, intuição e vontade de agir. Há uma chama interior que precisa de propósito — quando encontra, irradia; quando não encontra, inquieta. Sua energia inspira, mas pede pausas para não queimar a própria fonte.",
            "ausente": "O Fogo é o elemento mais escasso no seu mapa: o entusiasmo e a fé na vida podem precisar de cultivo consciente. Cerque-se de pessoas e projetos que acendam sua chama — e lembre-se de que a ousadia também se aprende.",
        },
        "en": {
            "nome": "Fire",
            "dominante": "Fire dominates your chart: you are moved by enthusiasm, intuition, and the will to act. There is an inner flame that needs purpose — when it finds one, it radiates; when it doesn't, it grows restless. Your energy inspires, but asks for pauses so it doesn't burn its own source.",
            "ausente": "Fire is the scarcest element in your chart: enthusiasm and faith in life may need conscious cultivation. Surround yourself with people and projects that light your flame — and remember that boldness can also be learned.",
        },
    },
    "earth": {
        "symbol": "🌱",
        "pt": {
            "nome": "Terra",
            "dominante": "A Terra domina seu mapa: você constrói a vida com as mãos, no ritmo do concreto. Praticidade, constância e senso de realidade são seus alicerces. Seu desafio é não confundir segurança com estagnação — o solo fértil também precisa de novas sementes.",
            "ausente": "A Terra é o elemento mais escasso no seu mapa: fincar raízes e cuidar do corpo e das finanças podem exigir esforço deliberado. Rotinas simples e contato com a natureza funcionam como âncoras poderosas para você.",
        },
        "en": {
            "nome": "Earth",
            "dominante": "Earth dominates your chart: you build life with your hands, at the pace of the concrete. Practicality, constancy, and a sense of reality are your foundations. Your challenge is not to confuse security with stagnation — fertile soil also needs new seeds.",
            "ausente": "Earth is the scarcest element in your chart: putting down roots and caring for body and finances may require deliberate effort. Simple routines and contact with nature work as powerful anchors for you.",
        },
    },
    "air": {
        "symbol": "🌬️",
        "pt": {
            "nome": "Ar",
            "dominante": "O Ar domina seu mapa: você vive no mundo das ideias, das palavras e das conexões. Sua mente é rápida e curiosa, e relacionamentos são oxigênio. O cuidado é não pairar só no conceito — aterrissar as ideias em gestos concretos as torna reais.",
            "ausente": "O Ar é o elemento mais escasso no seu mapa: objetivar sentimentos em palavras e manter distância racional podem não vir de graça. Escrever, conversar e estudar são exercícios que expandem esse músculo.",
        },
        "en": {
            "nome": "Air",
            "dominante": "Air dominates your chart: you live in the world of ideas, words, and connections. Your mind is quick and curious, and relationships are oxygen. The care is not to hover only in concepts — landing ideas into concrete gestures makes them real.",
            "ausente": "Air is the scarcest element in your chart: putting feelings into words and keeping rational distance may not come for free. Writing, talking, and studying are exercises that expand this muscle.",
        },
    },
    "water": {
        "symbol": "🌊",
        "pt": {
            "nome": "Água",
            "dominante": "A Água domina seu mapa: você sente antes de pensar, e sente fundo. Empatia, memória emocional e imaginação são suas correntezas. O cuidado é não se afogar no que absorve dos outros — fronteiras claras mantêm sua água limpa.",
            "ausente": "A Água é o elemento mais escasso no seu mapa: nomear e acolher emoções — suas e alheias — pode ser um território a explorar. Práticas de escuta e introspecção irrigam essa dimensão.",
        },
        "en": {
            "nome": "Water",
            "dominante": "Water dominates your chart: you feel before you think, and you feel deeply. Empathy, emotional memory, and imagination are your currents. The care is not to drown in what you absorb from others — clear boundaries keep your water clean.",
            "ausente": "Water is the scarcest element in your chart: naming and welcoming emotions — yours and others' — may be territory to explore. Practices of listening and introspection irrigate this dimension.",
        },
    },
}

MODALITIES = {
    "cardinal": {
        "pt": {
            "nome": "Cardinal",
            "dominante": "Com predominância Cardinal, você nasceu para iniciar. Começos te energizam: projetos, ciclos, movimentos. Seu aprendizado é sustentar o fôlego depois da largada — terminar também é um talento.",
            "ausente": "Com pouca energia Cardinal, dar o primeiro passo pode custar mais do que deveria. Rituais de início — pequenos e concretos — ajudam a destravar a ação.",
        },
        "en": {
            "nome": "Cardinal",
            "dominante": "With Cardinal predominance, you were born to initiate. Beginnings energize you: projects, cycles, movements. Your learning is to sustain momentum after the start — finishing is also a talent.",
            "ausente": "With little Cardinal energy, taking the first step may cost more than it should. Small, concrete starting rituals help unlock action.",
        },
    },
    "fixed": {
        "symbol": "",
        "pt": {
            "nome": "Fixo",
            "dominante": "Com predominância Fixa, você é a constância em pessoa. Persiste onde outros desistem, aprofunda onde outros passam rápido. O desafio é a rigidez: soltar o que já cumpriu seu ciclo também é sabedoria.",
            "ausente": "Com pouca energia Fixa, manter ritmo e resistir à dispersão pedem estrutura externa: hábitos, prazos e companhias constantes funcionam como trilhos.",
        },
        "en": {
            "nome": "Fixed",
            "dominante": "With Fixed predominance, you are constancy in person. You persist where others give up, deepen where others rush by. The challenge is rigidity: letting go of what has completed its cycle is also wisdom.",
            "ausente": "With little Fixed energy, keeping rhythm and resisting dispersion call for external structure: habits, deadlines, and steady company work as rails.",
        },
    },
    "mutable": {
        "pt": {
            "nome": "Mutável",
            "dominante": "Com predominância Mutável, você é adaptação pura. Lê o ambiente, ajusta a rota, traduz mundos diferentes entre si. O cuidado é não se perder de tanto se moldar — um centro claro torna sua flexibilidade imbatível.",
            "ausente": "Com pouca energia Mutável, mudanças inesperadas podem pesar. Treinar pequenas variações de rota no dia a dia fortalece sua elasticidade.",
        },
        "en": {
            "nome": "Mutable",
            "dominante": "With Mutable predominance, you are pure adaptation. You read the environment, adjust the route, translate different worlds to each other. The care is not to lose yourself from so much molding — a clear center makes your flexibility unbeatable.",
            "ausente": "With little Mutable energy, unexpected changes may weigh heavily. Training small route variations in daily life strengthens your elasticity.",
        },
    },
}


def get_element(element_key: str, lang: str = "pt") -> dict | None:
    entry = ELEMENTS.get(element_key)
    if entry:
        return entry.get(lang, entry.get("pt"))
    return None


def get_modality(modality_key: str, lang: str = "pt") -> dict | None:
    entry = MODALITIES.get(modality_key)
    if entry:
        return entry.get(lang, entry.get("pt"))
    return None
