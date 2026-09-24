# 🌍 Portfólio Científico & Comercial em Streamlit
### Dr. Jomil Costa Abreu Sales

Este aplicativo transforma a produção científica do **Memorial Circunstanciado** em um **portfólio interativo e comercial estilo dashboard**, com foco em inteligência territorial, soluções de mercado (ESG, segurança hídrica, créditos de carbono) e capacidade de ensino de geoprocessamento e sensoriamento remoto (QGIS, ArcGIS, Google Earth Engine, R e Python).

---

## 🚀 Como Executar Localmente

1. Certifique-se de ter o Python instalado (versão 3.9 ou superior).
2. No terminal, dentro da pasta do projeto, instale as dependências:
   pip install -r requirements.txt
3. Inicie o aplicativo Streamlit:
   streamlit run app.py
4. O navegador abrirá automaticamente em `http://localhost:8501`.

---

## 🌐 Como Hospedar Gratuitamente Online (Para o LinkedIn)

Para ter o portfólio acessível publicamente via link (por exemplo: `https://jomilcosta-portfolio.streamlit.app`):

1. **Suba os arquivos para um repositório no GitHub:**
   - Crie um repositório novo no seu GitHub (ex.: `portfolio-jomil-costa`).
   - Faça o upload dos arquivos: `app.py`, `portfolio_data.json`, `requirements.txt` e `README.md`.
2. **Conecte ao Streamlit Community Cloud:**
   - Acesse share.streamlit.io e faça login com sua conta do GitHub.
   - Clique em **"New app"**.
   - Selecione o repositório, o branch (`main`) e o arquivo principal (`app.py`).
   - Clique em **"Deploy!"**.
3. **Pronto!**
   - Em menos de 2 minutos, seu dashboard estará online com uma URL pública oficial pronta para adicionar na seção "Destaque" do seu LinkedIn e no seu currículo.

---

## 📂 Estrutura dos Arquivos

- `app.py`: Código-fonte completo da interface interativa em Streamlit.
- `portfolio_data.json`: Base de dados estruturada contendo o estudo de caso piloto detalhado, catálogo de 25 artigos do memorial, soluções comerciais e cursos de capacitação técnica.
- `requirements.txt`: Dependências mínimas necessárias para a execução.
- `agent_pipeline.py`: Modelo conceitual do agente autônomo diário para ingestão e enriquecimento de novos artigos.
- `dashboard_preview.html`: Visualização web estática e imediata com gráficos interativos em Chart.js e Tailwind.
