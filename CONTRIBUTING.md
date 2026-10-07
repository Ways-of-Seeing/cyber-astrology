# 🤝 Contribuindo com o Cyber Astra

Primeiro: **obrigado por considerar contribuir!** 💜

Este projeto foi feito para pessoas que nunca usaram um terminal — e o mesmo
vale para contribuições: se esta for a sua **primeira vez no open source**,
você está exatamente no lugar certo. Não existe pergunta boba por aqui.

## 🚀 Preparando o ambiente

Você precisa de **Python 3.11+** e **git** instalados.

```bash
# 1. Faça um fork do repositório no GitHub, depois clone o SEU fork
git clone https://github.com/SEU-USUARIO/cyber-astrology.git
cd cyber-astrology

# 2. Crie o ambiente virtual e instale em modo editável
python3 -m venv .venv && .venv/bin/pip install -e .

# 3. Pronto! Rode para testar
cyber-astra
```

Qualquer mudança no código passa a valer imediatamente, sem precisar
reinstalar. Para rodar com flags:

```bash
cyber-astra -n "Teste" -d 15/06/1990 -t 14:30 -l "São Paulo" --only synthesis
```

## 🎨 Estilo de código

Não temos linter nem configuração rígida — o pedido é simples: **combine com o
código que já existe**. Na prática:

- ✅ **Type hints** em tudo (funções, dataclasses) — o projeto é Python 3.11+ moderno
- ✅ **`dataclasses`** para estruturas de dados (veja `engine.py`)
- ✅ **stdlib primeiro** — só adicione uma dependência se realmente necessário;
  o projeto é propositalmente leve (kerykeion, geopy, timezonefinder, rich)
- ✅ **Rich para output** — siga os padrões de tabelas/painéis/estilos já usados
  em `display.py` e `cli.py`
- ✅ **Bilíngue obrigatório**: todo texto de interpretação precisa existir em
  **PT e EN**. Textos voltados ao usuário no menu/CLI também (veja o dicionário
  `MENU` em `cli.py`)
- ✅ Comentários e docstrings em português, como o restante do código

## ✍️ Adicionando um novo texto de interpretação

Os textos ficam em `cyber_astra/data/` e seguem um padrão simples de
**dicionários aninhados por idioma**. Você não precisa entender astrologia ou
o resto do código para contribuir aqui — é editar um dicionário Python.

Exemplo (`cyber_astra/data/planet_signs.py`):

```python
PLANET_IN_SIGN = {
    # Chave: "<planeta_inglês>_<signo_inglês>", minúsculas, sem acento
    "sun_aries": {
        "pt": {
            "titulo": "☉ Sol em Áries",
            "descricao": "Você nasceu com o Sol em Áries, ...",
            "forcas": ["Coragem", "Iniciativa", "Liderança", "Entusiasmo"],
            "diretrizes": [
                "Canalize sua energia pioneira em projetos ...",
                "Pratique a paciência estratégica: ...",
            ],
            "desafios": "A impulsividade e a impaciência podem ...",
        },
        "en": {
            "title": "☉ Sun in Aries",
            "description": "Born with the Sun in Aries, ...",
            "strengths": ["Courage", "Initiative", "Leadership", "Enthusiasm"],
            "guidelines": [
                "Channel your pioneering energy into projects ...",
                "Practice strategic patience: ...",
            ],
            "challenges": "Impulsiveness and impatience can ...",
        },
    },
}
```

Regras de ouro:

1. **Sempre os dois idiomas** (`pt` e `en`) — as chaves internas mudam
   (`titulo`/`title`, `forcas`/`strengths`, etc.); copie a estrutura de uma
   entrada vizinha e só troque o conteúdo.
2. **Mantenha o tom** dos textos existentes: acolhedor, poético mas claro,
   falando diretamente com a pessoa ("você").
3. **Não mude chaves existentes** — elas são referenciadas pelo código.

Os outros arquivos de dados seguem a mesma ideia: `houses.py`, `aspects.py`,
`elements.py`, `moon_phases.py` e os `planets_*.py` agrupados por planeta.

## 🔀 Processo de Pull Request

1. **Fork** do repositório
2. **Crie uma branch** com nome descritivo:
   `git checkout -b add-sun-in-libra-text`
3. **Faça sua mudança** e teste localmente (`cyber-astra --only <seção>`)
4. **Abra o PR** descrevendo:
   - **O quê**: o que a mudança faz
   - **Por quê**: o que motivou (issue relacionada, melhoria, bug)
5. Prefira **PRs pequenos**: um texto novo, um bug consertado, uma melhoria por
   vez. PRs pequenos são revisados (e aceitos) muito mais rápido.

Se a sua mudança alterar comportamento visível ou estrutura, atualize o
README.md se necessário.

## 🎃 Notas sobre Hacktoberfest

- **Qualidade > quantidade**: PRs spam (espaços aleatórios, mudanças vazias)
  serão fechados — o Hacktoberfest também exclui esse tipo de contribuição.
- Comece pelas issues com **`good first issue`** ou **`hacktoberfest`**.
- PRs legítimos e úteis recebem a etiqueta **`hacktoberfest-accepted`** do
  mantenedor, mesmo que precisem de pequenos ajustes antes do merge.
- Travou em alguma parte? Comente na issue ou abra uma discussão — ajudamos de
  verdade, sem julgamento.

---

## 🇬🇧 English summary

Thanks for contributing! This project welcomes **first-time contributors**.

- **Setup**: fork & clone the repo, then
  `python3 -m venv .venv && .venv/bin/pip install -e .` and run `cyber-astra`.
- **Style**: Python 3.11+ with type hints everywhere, `dataclasses` for data,
  stdlib-first (keep dependencies light), match the existing Rich output style.
  All user-facing and interpretation texts must exist in **both PT and EN**.
- **Interpretation texts** live in `cyber_astra/data/` as nested dicts keyed by
  language (`"pt"` / `"en"`) — copy a neighboring entry's structure and change
  only the content. Never rename existing keys.
- **PRs**: fork → descriptive branch → small, focused PR → describe *what* and
  *why*. Test locally before opening.
- **Hacktoberfest**: quality over spam; look for `good first issue` and
  `hacktoberfest` labels; legit PRs get the `hacktoberfest-accepted` label.
