# AI_INSTRUCTIONS.md — Guia para ChatGPT, Claude & Copilot

Ao interagir com este repositório através do **ChatGPT (OpenAI Projects / GPTs Customizados)**, **Claude Code**, **Cursor** ou **GitHub Copilot**, siga as seguintes diretrizes:

## 1. Identidade e Domínio do Autor
O usuário é o **Dr. Jomil Costa Abreu Sales**, Pós-Doutor em Ciências Florestais pela ESALQ/USP e Doutor em Ciências Ambientais. Ele é especialista em geotecnologias, sensoriamento remoto, modelagem de estoques de carbono e consultoria ambiental (regularização, licenciamento, perícias e tutoria de SIG).
Sempre mantenha um tom colaborativo, rigoroso, técnico e objetivo.

## 2. Regras de Edição do `app.py`
- O aplicativo é um arquivo autossuficiente e modular em Streamlit.
- Não remova chaves do `PORTFOLIO_DB` ou variáveis como `REAL_APA_GEOJSON`.
- Toda nova funcionalidade deve respeitar a paleta de cores corporativa:
  - Verde Florestal Principal: `#15803D` / `#065F46`
  - Azul Cartográfico / Hídrico: `#0284C7` / `#0369A1`
  - Âmbar / Consultoria: `#D97706` / `#B45309`
  - Fundo Esfumaçado Suave: `#EDF4EE`
- O menu principal é sincronizado entre a barra lateral e a grade de ícones de aplicativo de celular na Página Inicial.

## 3. Comandos Úteis
- Iniciar Streamlit: `streamlit run app.py`
- Testar compilação: `python -m py_compile app.py`
