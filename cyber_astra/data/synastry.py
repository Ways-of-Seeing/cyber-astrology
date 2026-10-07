# coding: utf-8
"""Synastry texts (PT/EN): element-pair chemistry, shared-sign notes,
couple verdicts and cross-aspect dynamics."""

# Compatibilidade por combinação de elementos (par não ordenado).
ELEMENT_PAIRS = {
    frozenset({"fire", "fire"}): {
        "pt": "Duas chamas juntas: entusiasmo em dobro, coragem compartilhada e uma relação que pulsa movimento. O cuidado é não transformar tudo em incêndio — ninguém apaga o fogo do outro, vocês precisam aprender a alternar quem ilumina.",
        "en": "Two flames together: double enthusiasm, shared courage, a relationship pulsing with movement. The care is not turning everything into a wildfire — no one puts out the other's fire; you need to take turns shining.",
    },
    frozenset({"fire", "earth"}): {
        "pt": "Fogo e Terra: um traz a faísca, o outro traz o solo. Pode ser a receita de grandes construções — ou um cabo de guerra entre pressa e paciência. Funciona quando o Fogo respeita o tempo da Terra e a Terra não sufoca a chama.",
        "en": "Fire and Earth: one brings the spark, the other brings the soil. It can be the recipe for great builds — or a tug-of-war between haste and patience. It works when Fire respects Earth's timing and Earth doesn't smother the flame.",
    },
    frozenset({"fire", "air"}): {
        "pt": "Fogo e Ar se alimentam: o Ar dá ideias e palavras à chama, o Fogo dá calor e direção às ideias. Química clássica, leve e estimulante. O risco é viver só de possibilidades — alguém precisa aterrissar os planos.",
        "en": "Fire and Air feed each other: Air gives ideas and words to the flame, Fire gives warmth and direction to ideas. Classic, light, stimulating chemistry. The risk is living on possibilities alone — someone has to land the plans.",
    },
    frozenset({"fire", "water"}): {
        "pt": "Fogo e Água: vapor ou apagamento, depende da dose. A intensidade emocional da Água pode assustar a franqueza do Fogo; a pressa do Fogo pode ferir a sensibilidade da Água. Quando há escuta, nasce uma das combinações mais transformadoras.",
        "en": "Fire and Water: steam or extinguishing, depending on the dose. Water's emotional intensity can scare Fire's frankness; Fire's haste can hurt Water's sensitivity. When there's listening, one of the most transformative combinations is born.",
    },
    frozenset({"earth", "earth"}): {
        "pt": "Terra com Terra: solidez, lealdade e uma relação construída tijolo a tijolo. Segurança não falta — o desafio é não deixar a rotina virar poeira. Pequenas aventuras regam esse jardim.",
        "en": "Earth with Earth: solidity, loyalty, a relationship built brick by brick. No lack of security — the challenge is not letting routine turn to dust. Small adventures water this garden.",
    },
    frozenset({"earth", "air"}): {
        "pt": "Terra e Ar falam línguas diferentes: um quer tocar, o outro quer pensar. Pode ser frustração — ou o encontro perfeito entre o pé no chão e a visão de longe. A ponte se constrói com paciência e curiosidade mútuas.",
        "en": "Earth and Air speak different languages: one wants to touch, the other wants to think. It can be frustration — or the perfect meeting of groundedness and long-range vision. The bridge is built with mutual patience and curiosity.",
    },
    frozenset({"earth", "water"}): {
        "pt": "Terra e Água são elementos férteis: a Água nutre, a Terra sustenta. Encontro de cuidado, afeto concreto e pertencimento. O cuidado é com o excesso de proteção — relação segura também precisa de horizonte.",
        "en": "Earth and Water are fertile elements: Water nourishes, Earth sustains. A meeting of care, concrete affection, and belonging. Watch out for overprotection — a safe relationship also needs a horizon.",
    },
    frozenset({"air", "air"}): {
        "pt": "Ar com Ar: conversas infinitas, humor compartilhado e uma mente que espelha a outra. A conexão mental é imediata — o trabalho é descer da nuvem das ideias para o corpo, o gesto e o cotidiano.",
        "en": "Air with Air: endless conversations, shared humor, one mind mirroring the other. Mental connection is immediate — the work is coming down from the cloud of ideas into body, gesture, and daily life.",
    },
    frozenset({"air", "water"}): {
        "pt": "Ar e Água: a mente tenta nomear o que o coração sente. Pode nascer poesia — ou mal-entendidos, quando um racionaliza o que o outro sente. A chave é traduzir sem julgar: sentimento não precisa de lógica para ser válido.",
        "en": "Air and Water: the mind tries to name what the heart feels. Poetry can be born — or misunderstandings, when one rationalizes what the other feels. The key is translating without judging: feelings don't need logic to be valid.",
    },
    frozenset({"water", "water"}): {
        "pt": "Água com Água: profundidade emocional rara, telepatia de quem sente junto. Intimidade não falta — o risco é se afogarem juntos nas mesmas marés. Âncoras externas (rotina, amigos, projetos) mantêm o mar navegável.",
        "en": "Water with Water: rare emotional depth, the telepathy of feeling together. No lack of intimacy — the risk is drowning together in the same tides. External anchors (routine, friends, projects) keep the sea navigable.",
    },
}

# Textos quando os dois têm o mesmo ponto no mesmo signo.
SAME_SIGN = {
    "sun": {
        "pt": "Vocês dois têm o Sol em {sign}: a essência de vocês fala a mesma língua. Os mesmos valores fundamentais, o mesmo ritmo de brilho — entender o outro é quase instintivo. O espelho também cobra: os defeitos do outro podem lembrar os seus.",
        "en": "You both have the Sun in {sign}: your essences speak the same language. The same core values, the same rhythm of shining — understanding each other is almost instinctive. The mirror also charges: the other's flaws may remind you of your own.",
    },
    "moon": {
        "pt": "Vocês dois têm a Lua em {sign}: sentem do mesmo jeito e precisam das mesmas coisas para se sentir seguros. É a receita de um porto seguro emocional — desde que os momentos de tempestade não coincidam sempre.",
        "en": "You both have the Moon in {sign}: you feel the same way and need the same things to feel safe. It's the recipe for an emotional safe harbor — as long as stormy moments don't always coincide.",
    },
    "ascendant": {
        "pt": "Vocês dois têm Ascendente em {sign}: chegam no mundo do mesmo jeito. A primeira impressão que causam é parecida, e a forma de começar as coisas combina. Parceria de fachada bonita — cuidem para a intimidade acompanhar.",
        "en": "You both have the Ascendant in {sign}: you meet the world the same way. The first impression you make is similar, and your way of starting things matches. A partnership with a beautiful facade — make sure intimacy keeps up.",
    },
    "mercury": {
        "pt": "Vocês dois têm Mercúrio em {sign}: pensam e conversam no mesmo formato. Discussões fluem, piadas internas nascem fácil e ninguém precisa ficar se explicando demais.",
        "en": "You both have Mercury in {sign}: you think and talk in the same format. Discussions flow, inside jokes are born easily, and no one needs to over-explain themselves.",
    },
    "venus": {
        "pt": "Vocês dois têm Vênus em {sign}: amam e demonstram afeto do mesmo jeito. O que um considera romântico, o outro considera também — sintonia rara na linguagem do carinho.",
        "en": "You both have Venus in {sign}: you love and show affection the same way. What one considers romantic, the other does too — a rare attunement in the language of care.",
    },
    "mars": {
        "pt": "Vocês dois têm Marte em {sign}: agem, desejam e brigam no mesmo estilo. Ótimo para projetos em dupla — e nas brigas, pelo menos ninguém é pego de surpresa.",
        "en": "You both have Mars in {sign}: you act, desire, and fight in the same style. Great for duo projects — and in fights, at least no one is caught off guard.",
    },
}

# Temas em forma nominal para a sinastria ("a forma de amar de Ana").
SYNASTRY_THEMES = {
    "sun": {"pt": "a identidade e o propósito", "en": "the identity and purpose"},
    "moon": {"pt": "as emoções e as necessidades", "en": "the emotions and needs"},
    "mercury": {"pt": "a mente e a comunicação", "en": "the mind and communication"},
    "venus": {"pt": "a forma de amar", "en": "the way of loving"},
    "mars": {"pt": "a ação e o desejo", "en": "the action and desire"},
    "jupiter": {"pt": "a expansão e a fé na vida", "en": "the expansion and faith in life"},
    "saturn": {"pt": "a disciplina e os limites", "en": "the discipline and boundaries"},
    "ascendant": {"pt": "a máscara e a iniciativa", "en": "the mask and initiative"},
}

# Dinâmicas dos aspectos cruzados. Placeholders: {n1} {p1} {n2} {p2}.
SYNASTRY_DYNAMICS = {
    "conjunction": {
        "pt": "{p1} de {n1} e {p2} de {n2} se fundem: nesse ponto vocês funcionam como um só. É o lugar mais intenso da conexão — magnético, inegável, impossível de ignorar.",
        "en": "{p1} ({n1}) and {p2} ({n2}) fuse: at this point you function as one. It's the most intense spot of the connection — magnetic, undeniable, impossible to ignore.",
    },
    "sextile": {
        "pt": "{p1} de {n1} e {p2} de {n2} se apoiam com leveza: é uma porta de oportunidades na relação, que se abre toda vez que vocês investem nela.",
        "en": "{p1} ({n1}) and {p2} ({n2}) support each other lightly: a door of opportunity in the relationship, opening every time you invest in it.",
    },
    "square": {
        "pt": "{p1} de {n1} e {p2} de {n2} se provocam: há atrito aqui, e é dele que nasce o crescimento da dupla. O segredo é brigar pelo assunto, nunca contra a pessoa.",
        "en": "{p1} ({n1}) and {p2} ({n2}) provoke each other: there's friction here, and it's from it that the duo's growth is born. The secret is fighting about the issue, never against the person.",
    },
    "trine": {
        "pt": "{p1} de {n1} e {p2} de {n2} fluem sem esforço: é um canal de graça na relação, daqueles que parecem presente de fábrica.",
        "en": "{p1} ({n1}) and {p2} ({n2}) flow effortlessly: a channel of grace in the relationship, the kind that feels factory-gifted.",
    },
    "opposition": {
        "pt": "{p1} de {n1} e {p2} de {n2} se espelham de lados opostos: cada um carrega o que falta no outro. Pode virar projeção — ou a mais completa das parcerias.",
        "en": "{p1} ({n1}) and {p2} ({n2}) mirror each other from opposite sides: each carries what the other lacks. It can become projection — or the most complete of partnerships.",
    },
}

# Vereditos pela proporção harmonia × tensão.
VERDICTS = {
    "harmonious": {
        "titulo": {"pt": "Corrente de harmonia", "en": "Stream of harmony"},
        "pt": "O mapa de vocês conversa por canais suaves: afinidades superam os atritos. A relação tem colchão de nuvem — o trabalho é não adormecer nela, mantendo a curiosidade viva.",
        "en": "Your charts talk through gentle channels: affinities outweigh frictions. The relationship has a cloud cushion — the work is not falling asleep on it, keeping curiosity alive.",
    },
    "balanced": {
        "titulo": {"pt": "Equilíbrio dinâmico", "en": "Dynamic balance"},
        "pt": "Harmonia e tensão se equilibram no mapa de vocês: tem colo e tem desafio, na medida. É o tipo de conexão que amadurece com o tempo — cada atrito vencido vira fundação.",
        "en": "Harmony and tension balance out in your charts: there's comfort and there's challenge, in measure. It's the kind of connection that matures with time — every friction overcome becomes foundation.",
    },
    "intense": {
        "titulo": {"pt": "Forja de intensidade", "en": "Forge of intensity"},
        "pt": "O mapa de vocês pulsa tensão criativa: nada aqui é morno. Relações assim transformam — desde que a energia vire movimento, não desgaste. Combinem rituais de paz para os dias de tempestade.",
        "en": "Your charts pulse with creative tension: nothing here is lukewarm. Relationships like this transform — as long as the energy becomes movement, not wear. Agree on peace rituals for stormy days.",
    },
}
