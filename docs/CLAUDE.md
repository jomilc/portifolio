# CLAUDE.md — Diretrizes para Claude Code

Este arquivo orienta o **Claude Code** ao operar neste repositório.

## 🔬 Visão Geral do Projeto
- **Nome:** Portfólio Científico, WebSIG & Inteligência Artificial
- **Autor:** Dr. Jomil Costa Abreu Sales (Biólogo, CRBio nº 68816/01-D, Pós-Doutor em Ciências Florestais na ESALQ/USP, Doutor em Ciências Ambientais pela UNESP / TU Berlin / FCT Nova Lisboa).
- **Finalidade:** Dashboard executivo interativo em Streamlit que integra:
  1. Portfólio científico com 6 artigos (com destaque para o Preprint 2024 na APA de Itupararanga).
  2. WebSIG cartográfico da APA de Itupararanga (Folium/Leaflet + GeoPandas + camadas temáticas).
  3. Assistente RAG conversacional fundamentado estritamente nas pesquisas.
  4. Módulo de Consultoria Ambiental & Tutoria em SIG/Geoprocessamento.
  5. Vitrine de criações e modelos com Inteligência Artificial.

## 🛠️ Stack Tecnológica & Comandos
- **Linguagem:** Python 3.10+
- **Framework Principal:** Streamlit
- **Bibliotecas Geoespaciais:** GeoPandas, Folium, Streamlit-Folium, Shapely
- **Processamento de Imagens:** Pillow (PIL), Base64 embedding
- **Manipulação de Dados:** Pandas, NumPy, JSON

### Comandos de Execução
- **Executar aplicativo localmente:**
  ```bash
  streamlit run app.py
  ```
- **Verificar sintaxe sem iniciar servidor:**
  ```bash
  python3 -m py_compile app.py
  ```
- **Instalar dependências:**
  ```bash
  pip install -r requirements.txt
  ```

## 📐 Padrões Arquiteturais e de Código
1. **Navegação State-Driven:** A navegação entre páginas/setores utiliza exclusivamente `st.session_state.active_section` acompanhado de `st.rerun()`.
2. **Resiliência a Falhas (Graceful Fallback):** Todas as chamadas a bibliotecas externas (como `geopandas`) possuem blocos `try/except` com dados embutidos ou fallbacks geométricos em GeoJSON.
3. **Carregamento de Figuras:** A função `get_figure_image_b64(fig_name)` busca de forma flexível tanto na raiz quanto na pasta `artigos_midia/` e suas subpastas (`artigo_01_preprint/`, etc.).
4. **Enquadramento Facial:** A função `get_profile_photo_b64()` utiliza corte proporcional no rosto (centro em X=380, Y=800 em 1200x1600) ou a imagem pré-recortada `foto_curriculo1.jpg`.
5. **Rigor Técnico e Terminologia:** O autor é pesquisador sênior da USP. Mantenha precisão metodológica impecável em termos de sensoriamento remoto, modelagem preditiva e legislação ambiental.
