# Guia de Contribuição / Contributing Guide

Obrigado pelo interesse em contribuir com o **cyber-astrology**! 🪐✨

---

## 🛠️ Configuração do Ambiente

1. **Clone o repositório e acesse o diretório**:
   ```bash
   git clone https://github.com/ways-of-seeing/cyber-astrology.git
   cd cyber-astrology
   ```

2. **Crie e ative um ambiente virtual**:
   ```bash
   python -m venv .venv

   # Linux / macOS:
   source .venv/bin/activate

   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   pip install pytest
   ```

---

## 🧪 Executando os Testes Automatizados

O projeto utiliza **[pytest](https://docs.pytest.org/)** para testes rápidos, determinísticos e sem dependência de rede:

```bash
# Rodar todos os testes
pytest

# Rodar com detalhes (verbose)
pytest -v

# Rodar apenas um arquivo de testes
pytest tests/test_prompts.py
pytest tests/test_synthesis.py
```

### Estrutura dos Testes

- `tests/conftest.py`: Fixture com mapa astral congelado (`known_chart_data`) para testes offline determinísticos.
- `tests/test_prompts.py`: Testes unitários para parsing flexível de datas (`DD/MM/AAAA`, `DD-MM-AA`, `AAAAMMDD`, etc.) e horários (`HH:MM`, `HH.MM`, `HHhMM`, `HHMM`).
- `tests/test_synthesis.py`: Testes para cálculo de aspectos maiores (conjunção, sextil, quadratura, trígono, oposição), equilíbrio elemental e de modalidades, e fases lunares.
- `tests/test_engine.py`: Validação estrutural do motor de cálculo astrológico.

---

## 💡 Boas Práticas

- Mantenha os testes unitários independentes de rede e geocodificação externa.
- Use fixtures para dados de exemplo quando testar novos módulos de interpretação e síntese.
- Certifique-se de que `pytest` passa antes de abrir um Pull Request.
