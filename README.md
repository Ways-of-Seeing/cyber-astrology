# 🔮 Cyber Astra

[![Hacktoberfest](https://img.shields.io/badge/Hacktoberfest-friendly-orange)](https://hacktoberfest.com/)
[![Python](https://img.shields.io/badge/Python-%3E%3D3.11-blue.svg)](https://www.python.org/)
[![Licença: MIT](https://img.shields.io/badge/Licença-MIT-green.svg)](LICENSE)
[![PRs bem-vindos](https://img.shields.io/badge/PRs-bem--vindos-brightgreen.svg)](CONTRIBUTING.md)

**Seu mapa astral na linha de comando** — leituras ricas, insights e uma roda natal
em ASCII bonita. 100% Python moderno, leve e fácil de instalar.

## ✨ O que é isso?

O Cyber Astra é um programinha que roda no terminal do seu computador e calcula o
seu **mapa astral** — aquele retrato do céu no exato momento em que você nasceu.
A partir da data, horário e cidade de nascimento, ele te conta sobre sua
personalidade, seus talentos e seus caminhos, em **português 🇧🇷 ou inglês 🇬🇧**.

E o melhor: ele foi feito para **quem nunca usou um terminal na vida**.
Nada de comandos complicados — você abre o programa, responde umas perguntas
simples (digitar e apertar Enter) e o relatório aparece, com direito a céu
estrelado animado e tudo mais. 🌟

Ah, e seus dados ficam **no seu computador**: nenhuma informação pessoal é
enviada para lugar nenhum.

## 🌟 O que ele faz

- 🎨 **Banner animado de céu estrelado** e spinners simpáticos enquanto "consulta as estrelas"
- 📅 **Entrada de dados flexível**: datas como `15061990` ou `15/06/1990`; horários como
  `1430`, `14:30` ou `14h30`; horário em branco = meio-dia
- 🌍 **Localização inteligente**: digite a cidade e ele acha no mapa; ou deixe em
  branco e ele tenta detectar sua localização pelo IP (sempre pedindo permissão, s/n)
- 📡 **Modo offline**: forneça `--lat`, `--lon` e `--tz` e rode sem internet
- 🌐 **PT-BR e EN** com alternância direto no menu
- 💞 **Sinastria**: compare dois mapas — aspectos cruzados entre os planetas,
  características em comum, química por elementos dos pares-chave (Sol×Sol,
  Lua×Lua, Vênus×Marte…) e um veredito da conexão
- 🍎 **App para Mac**: gera um `Cyber Astra.app` que abre numa janela de Terminal
  amigável (fonte grande, fundo creme, título bonito) — perfeito para quem não usa terminal

## 📖 O que sai no relatório

- 🎡 **Roda natal em ASCII** — o desenho clássico do mapa
- 🪐 **Tabela de planetas** — signo, grau, casa e movimento retrógrado
- 🔥 **Síntese** — narrativa do Big Three (Sol, Lua e Ascendente), fase da Lua
  natal (8 fases), equilíbrio de elementos (fogo/terra/ar/água) e modalidades
  (cardinal/fixos/mutáveis)
- ⚡ **Aspectos** — conjunção ☌, sextil ⚹, quadratura □, trígono △ e oposição ☍
  com orbes, e narrativa para os 3 aspectos mais apertados
- 💡 **Insights por planeta em signo** — forças, diretrizes e desafios
- 🏠 **Significado das casas** ocupadas

## 📸 Em breve

> 📸 Em breve: screenshots e GIF do app

## 🚀 Começando em 3 minutos

Você só precisa de **Python 3.11 ou mais novo** instalado. Nunca usou um
terminal? Calma, é só copiar e colar cada bloco abaixo e apertar Enter.

### 1. Baixe o projeto

```bash
git clone https://github.com/Ways-of-Seeing/cyber-astrology.git
cd cyber-astrology
```

### 2. Crie o ambiente e instale

```bash
python3 -m venv .venv && .venv/bin/pip install -e .
```

### 3. Rode!

```bash
cyber-astra
```

Sem argumentos, abre o **menu interativo**:

```
1  🌟  Criar meu mapa astral
2  💞  Comparar dois mapas (sinastria)
3  🌐  Idioma / Language
4  ❓  O que é isso? Como funciona?
5  🚪  Sair
```

Digite o número da opção e aperte Enter. É só isso. 💜

### Outros jeitos de rodar

```bash
python -m cyber_astra     # mesma coisa que cyber-astra
./run.sh                  # atalho pronto
```

### Usando flags (para quem já curte um terminal)

```bash
cyber-astra -n "Ana" -d 15/06/1990 -t 14:30 -l "São Paulo, Brasil"
cyber-astra --lang en                         # relatório em inglês
cyber-astra --no-wheel                        # pula a roda ASCII
cyber-astra --only synthesis                  # só a síntese
cyber-astra --only planets|aspects|insights|houses|wheel
```

Flags disponíveis: `--name/-n`, `--date/-d`, `--time/-t`, `--location/-l`,
`--lang pt|en`, `--no-wheel`, `--only <seção>`, e `--lat --lon --tz` para modo
offline:

```bash
cyber-astra -l "São Paulo" --lat -23.55 --lon -46.63 --tz America/Sao_Paulo
```

### 🍎 App para Mac

```bash
bash app/build_app.sh     # cria o .venv (se preciso) e gera o app na raiz
open "Cyber Astra.app"    # para testar
```

O app abre uma janela de Terminal amigável — fonte tamanho 18, fundo creme e o
título *"✨ Cyber Astra — Seu Mapa Astral ✨"* — já no menu interativo.

## 🛠️ Feito com

- **Python 3.11+** — tipagem moderna, `dataclasses`, stdlib primeiro
- **[kerykeion](https://github.com/g-battaglia/kerykeion) ≥ 6** — cálculos
  astronômicos (base Swiss Ephemeris via libephemeris)
- **[geopy](https://geopy.readthedocs.io/)** — geocodificação via Nominatim
- **[timezonefinder](https://github.com/jannikmi/timezonefinder)** — fuso horário
  a partir das coordenadas
- **[rich](https://github.com/Textualize/rich)** — tabelas, painéis e cores no terminal
- **hatchling** — backend de build (`pyproject.toml`)

## 📁 Estrutura do projeto

```
cyber-astrology/
├── app/
│   └── build_app.sh      # gerador do Cyber Astra.app (macOS)
├── cyber_astra/
│   ├── __main__.py       # python -m cyber_astra
│   ├── cli.py            # entrada: argparse + menu interativo
│   ├── prompts.py        # parsers flexíveis de data/hora + localização por IP
│   ├── animations.py     # céu estrelado, spinner, revelação de linhas
│   ├── engine.py         # wrapper do kerykeion → dataclasses Chart/Planet
│   ├── geocoder.py       # cidade → lat/lon/fuso
│   ├── wheel.py          # roda natal em ASCII
│   ├── display.py        # renderização do relatório com Rich
│   ├── synthesis.py      # aspectos, elementos, fase da Lua, Big Three
│   └── data/             # interpretações PT/EN
│       ├── planet_signs.py
│       ├── planets_mercury_venus.py
│       ├── planets_mars_jupiter_saturn.py
│       ├── planets_outer.py
│       ├── houses.py
│       ├── aspects.py
│       ├── elements.py
│       └── moon_phases.py
├── run.sh                # atalho para rodar
├── pyproject.toml
└── README.md
```

## 🤝 Contribuindo

Quer contribuir? Maravilha! Leia o [CONTRIBUTING.md](CONTRIBUTING.md) — lá tem o
passo a passo para montar o ambiente, o estilo de código e como abrir seu
primeiro PR. Primeira vez contribuindo com open source? Esse projeto foi pensado
justamente para você. 💜

## 🎃 Hacktoberfest

O Cyber Astra participa do **Hacktoberfest**! Isso significa que contribuições
de iniciantes são mais do que bem-vindas:

- Procure issues com as etiquetas **`good first issue`** e **`hacktoberfest`** —
  elas foram escolhidas a dedo para quem está começando.
- A maioria dos "good first issue" aqui envolve **escrever ou melhorar textos de
  interpretação** (PT/EN) — não precisa ser expert em Python!
- Qualidade acima de quantidade: um PR pequeno e bem feito vale mais do que
  cinco apressados.

---

## 🇬🇧 English

**Cyber Astra** is a friendly natal-chart CLI in modern Python 3.11+, designed
for people who have **never used a terminal**: menu-driven, animated ASCII
starfield banner, spinners, flexible inputs (dates like `15061990` or
`15/06/1990`; times like `1430` or `14h30`; blank time = noon), optional
IP-based location detection (with consent), and PT-BR/EN support. It also ships
a macOS app builder (`app/build_app.sh` → `Cyber Astra.app`) that opens a
friendly Terminal window.

### Quickstart

```bash
python3 -m venv .venv && .venv/bin/pip install -e .
cyber-astra                                   # interactive menu
cyber-astra -n "Ana" -d 15/06/1990 -t 14:30 -l "São Paulo, Brazil"
cyber-astra --lang en
cyber-astra --only synthesis|planets|aspects|insights|houses|wheel
cyber-astra --lat -23.55 --lon -46.63 --tz America/Sao_Paulo   # offline
```

### Report sections

ASCII natal wheel, planet table (sign/degree/house/retrograde), synthesis (Big
Three, natal Moon phase, element and modality balance), aspects with orbs and
narratives, planet-in-sign insights (strengths/guidelines/challenges) and house
meanings.

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) — beginners are very welcome, and we keep
issues labeled `good first issue` and `hacktoberfest` ready for first-time
contributors. Interpretation texts are required in both PT and EN.

## 📄 Licença

MIT © 2025 Lucas Rafaldini — veja [LICENSE](LICENSE).
