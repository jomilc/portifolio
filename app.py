import streamlit as st
import json
import re
import os
import base64
import pandas as pd
import streamlit.components.v1 as components

from artigos_data import ARTIGOS, ARTIGOS_POR_ID

st.set_page_config(
    page_title="Dr. Jomil Costa Abreu Sales | Biólogo & Consultoria Ambiental",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

PORTFOLIO_DB = {
  "researcher": {
    "name": "Dr. Jomil Costa Abreu Sales",
    "title": "Biólogo | Pós-Doutor em Ciências Florestais (ESALQ/USP) | Doutor em Ciências Ambientais (UNESP / TU Berlin / FCT Nova Lisboa)",
    "summary": "Especialista em Geotecnologias, Sensoriamento Remoto, Modelagem Preditiva de Uso da Terra, Fluxo de Carbono e Ecologia da Paisagem. Desenvolvedor de metodologias para detecção de degradação florestal funcional invisível ao desmatamento tradicional, valoração de serviços ecossistêmicos e inteligência territorial para tomada de decisão.",
    "links": {
      "lattes": "http://lattes.cnpq.br/0266681173969604",
      "orcid": "https://orcid.org/0000-0001-8722-8398",
      "scholar": "https://scholar.google.com/citations?user=3ymOKh8AAAAJ&hl=en",
      "researchgate": "https://www.researchgate.net/profile/Jomil-Sales",
      "ssrn": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7268395",
      "email": "jomil.sales@usp.br",
      "linkedin": "https://www.linkedin.com/in/jomil-costa-phd-53817838/"
    },
    "stats": {
      "published_articles": 25,
      "preprints_under_review": 1,
      "monitored_territories_ha": "216.500+ ha",
      "satellites_mastered": "Sentinel-2 • Landsat 5/8/9 • MODIS",
      "tools_stack": "QGIS (MOLUSCE) • ArcGIS • GEE • R • Python"
    }
  },
  "featured_manuscript": {
    "id": "PREPRINT-2024",
    "title": "Carbon Flux Potential Prediction Model Based on Land Cover and Land Use: Application in the Itupararanga Environmental Protection Area, SP, Brazil",
    "status": "Versão Ajustada do Preprint (Pós-Revisão por Pares)",
    "original_preprint_url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7268395",
    "doi_status": "Preprint em fase final de publicação (sem DOI definitivo ainda)",
    "authors": [
      "Jomil Costa Abreu Sales (Autor Correspondente - ESALQ/USP)",
      "Nícholas de Paula Nicomedes (UNESP)",
      "Darllan Collins da Cunha e Silva (UNESP)",
      "Roberto Wagner Lourenço (UNESP)"
    ],
    "funding": "FAPESP (Processo 2024/14444-2) e CAPES (Código 001)",
    "study_area": {
      "name": "Área de Proteção Ambiental (APA) de Itupararanga",
      "legal_basis": "Lei Estadual nº 10.100/1998 e Lei nº 11.579/2003",
      "municipalities": "Alumínio, Cotia, Ibiúna, Mairinque, Piedade, São Roque, Vargem Grande Paulista e Votorantim",
      "state": "São Paulo (SP), Brasil",
      "biome": "Mata Atlântica (Floresta Ombrófila Densa)",
      "total_area_km2": 938.31,
      "reservoir": "Represa de Itupararanga (Rio Sorocaba) - vital para abastecimento e energia (CBA)",
      "zoning": [
        "Zona de Conservação da Biodiversidade (ZCB)",
        "Zona de Conservação de Recursos Hídricos (ZCRH)",
        "Zona de Ocupação Rural (ZOR)",
        "Zona de Ocupação Diversificada (ZOD)",
        "Zona de Ocupação Consolidada (ZOC)"
      ]
    },
    "central_discovery": {
      "headline": "Degradação Funcional Oculta dentro de Unidade de Conservação da Mata Atlântica",
      "the_paradox": "Enquanto a cobertura da terra permaneceu 91.8% estável entre 2019 e 2023 (e as florestas tiveram 96.0% de persistência), as áreas de Alto Potencial de Sequestro de Carbono sofreram uma retração severa de -21.5% (de 200.83 km² para 157.72 km²).",
      "crucial_finding": "95.7% dessa perda ocorreu DENTRO de áreas de floresta que NÃO sofreram desmatamento cartográfico (65.66 km² continuaram como floresta, mas perderam vigor fotossintético e capacidade de retenção de CO2). Esse declínio é totalmente invisível ao monitoramento clássico de uso do solo!",
      "edge_effect": "A perda de potencial fotossintético foi maior próximo às bordas dos fragmentos (46.4% de perda a até 20m da borda vs. 35.0% além de 200m)."
    },
    "geotechnology_method": {
      "satellites": "Sentinel-2 L2A (10 m de resolução espacial, bandas B02-Azul, B03-Verde, B04-Vermelho e B08-NIR, cenas de inverno seco 2019 e 2023 com 0.0035% de nuvens).",
      "indices_formulas": [
        {
          "name": "NDVI",
          "formula": "(B08 - B04) / (B08 + B04)",
          "description": "Índice de Vegetação por Diferença Normalizada (vigor e biomassa verde)."
        },
        {
          "name": "PRI",
          "formula": "(B02 - B03) / (B02 + B03)",
          "description": "Índice de Refletância Fotoquímica adaptado às bandas do Sentinel-2 (eficiência do uso da luz)."
        },
        {
          "name": "sPRI",
          "formula": "(PRI + 1) / 2",
          "description": "Escalonamento linear positivo (0 a 1)."
        },
        {
          "name": "CO2 Flux Proxy",
          "formula": "sPRI × NDVI",
          "description": "Indicador espectral relativo do potencial de sequestro de CO2."
        }
      ],
      "lulc_source": "MapBiomas Coleção 10 m (beta, baseada em Sentinel-2), reclassificada em 6 classes.",
      "predictive_model_2028": "Plugin MOLUSCE (QGIS) combinando Rede Neural Artificial (ANN-MLP com 10.000 amostras e 500 iterações) e Autômatos Celulares com Cadeias de Markov (CA-Markov).",
      "validation_gpp": "Validação cruzada independente com dados de Produtividade Primária Bruta (GPP MODIS MOD17A2H, 500m) no Google Earth Engine, confirmando forte correlação estatística: Pearson r = 0.705 (2019) e 0.662 (2023); Spearman rho = 0.743 (2019) e 0.748 (2023); p < 0.001."
    },
    "data_comparison": {
      "lulc_table": [
        {
          "classe": "Corpos Hídricos",
          "area_2019_km2": 26.78,
          "area_2023_km2": 25.21,
          "area_2028_km2": 24.46,
          "delta_pct_19_23": -5.9
        },
        {
          "classe": "Floresta Nativa",
          "area_2019_km2": 406.25,
          "area_2023_km2": 395.5,
          "area_2028_km2": 396.59,
          "delta_pct_19_23": -2.6
        },
        {
          "classe": "Silvicultura",
          "area_2019_km2": 36.92,
          "area_2023_km2": 39.08,
          "area_2028_km2": 39.11,
          "delta_pct_19_23": 5.9
        },
        {
          "classe": "Área Urbana",
          "area_2019_km2": 40.91,
          "area_2023_km2": 48.97,
          "area_2028_km2": 49.6,
          "delta_pct_19_23": 19.7
        },
        {
          "classe": "Agricultura / Cultivos",
          "area_2019_km2": 327.6,
          "area_2023_km2": 334.3,
          "area_2028_km2": 343.27,
          "delta_pct_19_23": 2.0
        },
        {
          "classe": "Formação Campestre / Arbustiva",
          "area_2019_km2": 99.85,
          "area_2023_km2": 95.25,
          "area_2028_km2": 85.27,
          "delta_pct_19_23": -4.6
        }
      ],
      "carbon_potential_table": [
        {
          "classe": "Área Antrópica (Emissão)",
          "area_2019_km2": 40.32,
          "share_2019_pct": 4.3,
          "area_2023_km2": 34.59,
          "share_2023_pct": 3.69,
          "area_2028_km2": 32.34,
          "share_2028_pct": 3.45
        },
        {
          "classe": "Baixo Potencial",
          "area_2019_km2": 257.12,
          "share_2019_pct": 27.4,
          "area_2023_km2": 242.54,
          "share_2023_pct": 25.85,
          "area_2028_km2": 234.72,
          "share_2028_pct": 25.02
        },
        {
          "classe": "Moderado Potencial",
          "area_2019_km2": 437.03,
          "share_2019_pct": 46.57,
          "area_2023_km2": 501.98,
          "share_2023_pct": 53.5,
          "area_2028_km2": 524.5,
          "share_2028_pct": 55.92
        },
        {
          "classe": "Alto Potencial",
          "area_2019_km2": 200.83,
          "share_2019_pct": 21.4,
          "area_2023_km2": 157.72,
          "share_2023_pct": 16.81,
          "area_2028_km2": 145.21,
          "share_2028_pct": 15.48
        },
        {
          "classe": "Muito Alto Potencial",
          "area_2019_km2": 3.14,
          "share_2019_pct": 0.33,
          "area_2023_km2": 1.49,
          "share_2023_pct": 0.16,
          "area_2028_km2": 1.29,
          "share_2028_pct": 0.14
        }
      ]
    },
    "management_recommendations": [
      "Vigilância e contenção prioritária no anel de 250 m a 1.000 m da represa de Itupararanga, onde se concentram 70.8% da nova expansão urbana periurbana.",
      "Manejo de bordas e adensamento florestal nos fragmentos de Mata Atlântica para combater o efeito de borda e restabelecer o potencial fotossintético.",
      "Diferenciação mandatória da silvicultura em protocolos de monitoramento, evitando confundir ciclos de corte/plantio com desmatamento de floresta nativa.",
      "Adoção de monitoramento funcional periódico (índices espectrais de fluxo de CO2) junto ao mapeamento clássico de cobertura da terra, pois 95.7% da degradação ocorreu sem alteração da classe florestal."
    ]
  },
  "top_5_articles": [
    {
      "rank": 1,
      "type": "Preprint (Versão Pós-Revisão)",
      "year": "2024",
      "title": "Carbon Flux Potential Prediction Model Based on Land Cover and Land Use: Application in the Itupararanga Environmental Protection Area, SP, Brazil",
      "venue": "SSRN (Submetido / Pós-Revisão)",
      "theme": "Modelagem de Fluxo de Carbono & Mata Atlântica",
      "tools": "Sentinel-2 (10m), QGIS (MOLUSCE), GEE, MODIS GPP",
      "key_contribution": "Demonstrou que 95.7% da perda de potencial de carbono ocorreu sem perda de cobertura florestal na APA Itupararanga (-21.5% de áreas de alto potencial)."
    },
    {
      "rank": 2,
      "type": "Artigo em Periódico",
      "year": "2023",
      "title": "The Influence of Land Use and Land Cover on Surface Temperature in a Water Catchment Sub-Basin",
      "venue": "Sociedade & Natureza, v. 35, e69161",
      "theme": "Sensoriamento Térmico (LST) & Segurança Hídrica",
      "tools": "Landsat 5 & 8, QGIS, ArcGIS, MapBiomas",
      "key_contribution": "Provou que florestas nativas no Cerrado mantêm a temperatura 1.62°C a 2.09°C mais baixa que agropecuária e reduzem perdas por evapotranspiração em manancial crítico."
    },
    {
      "rank": 3,
      "type": "Artigo em Periódico",
      "year": "2022",
      "title": "Análise espacial da distribuição do ensino em função da renda em uma bacia hidrográfica",
      "venue": "Nativa, v. 10, p. 05-15",
      "theme": "Geoestatística & Demografia Espacial",
      "tools": "ArcGIS, Krigagem Ordinária, Estimador Kernel",
      "key_contribution": "Modelou espacialmente a correlação entre vulnerabilidade socioeconômica e carência educacional na Bacia do Rio Una."
    },
    {
      "rank": 4,
      "type": "Artigo em Periódico",
      "year": "2022",
      "title": "Creation of an environmental sustainability index for water resources applied to watersheds",
      "venue": "Environment, Development and Sustainability, v. 1, p. 1-21",
      "theme": "Sustentabilidade Hídrica & Análise Multicritério",
      "tools": "AHP (Analytic Hierarchy Process), Geoprocessamento",
      "key_contribution": "Desenvolveu o índice WRSI integrando qualidade da água, saneamento e cobertura vegetal para gestão territorial de bacias."
    },
    {
      "rank": 5,
      "type": "Artigo em Periódico",
      "year": "2022",
      "title": "Reflexos Ambientais do Desenvolvimento e Expansão das Atividades Humanas sobre a Qualidade da Água",
      "venue": "Revista Brasileira de Geografia Física, v. 15, p. 176-198",
      "theme": "Qualidade da Água & Expansão Antrópica",
      "tools": "Geoprocessamento, Análise Espacial de Nutrientes",
      "key_contribution": "Identificou o enriquecimento por fósforo associado ao avanço agrícola e urbano e seus reflexos na integridade dos mananciais."
    }
  ],
  "commercial_solutions": [
    {
      "id": "SOL-01",
      "title": "Auditoria de Degradação Florestal Funcional Oculta para UCs e Projetos REDD+",
      "target": "Gestores de UCs (Fundação Florestal, ICMBio), Fundos de Carbono, Empresas de Papel & Celulose.",
      "value": "Monitoramento de alta resolução (Sentinel-2 10m) que detecta a perda de vigor fotossintético e capacidade de estocagem de carbono DENTRO de florestas que parecem intactas nos mapas tradicionais. Permite intervenção precoce de restauração e precificação com alta integridade técnica de créditos de carbono.",
      "deliverables": "Relatório de integridade funcional, mapas vetoriais de perda de vigor e séries históricas de fluxo de CO2.",
      "stack": [
        "Sentinel-2",
        "QGIS",
        "Modelagem sPRI × NDVI",
        "GEE"
      ]
    },
    {
      "id": "SOL-02",
      "title": "Modelagem Preditiva de Cenários de Uso do Solo e Ocupação com Redes Neurais (CA-Markov)",
      "target": "Prefeituras Municipais, Planos Diretores, Concessionárias de Saneamento e Órgãos de Licenciamento.",
      "value": "Simulação de cenários futuros de expansão urbana e agrícola (5 a 10 anos à frente) usando redes neurais artificiais MLP e Autômatos Celulares no QGIS (MOLUSCE). Identifica vetores de invasão em mananciais e zonas de amortecimento antes que os danos aconteçam.",
      "deliverables": "Mapas preditivos de transição, matrizes de probabilidade de mudança de uso e relatório executivo para zoneamento ambiental.",
      "stack": [
        "QGIS MOLUSCE",
        "Redes Neurais MLP",
        "Cadeias de Markov",
        "MapBiomas"
      ]
    },
    {
      "id": "SOL-03",
      "title": "Implantação de WebSIG e Plataformas Interativas de Inteligência Territorial",
      "target": "Comitês de Bacia Hidrográfica, Agroindústrias e Secretarias de Meio Ambiente.",
      "value": "Conversão de bases cartográficas complexas (shapefiles, rasters de satélite, dados de outorga) em plataformas WebSIG interativas de fácil acesso em navegadores, permitindo cruzamento de camadas, consultas de atributos e tomada de decisão ágil.",
      "deliverables": "Ambiente WebSIG interativo em nuvem, shapefiles padronizados, dashboards de indicadores territoriais.",
      "stack": [
        "Streamlit",
        "Folium",
        "Leafmap",
        "GeoJSON",
        "Python"
      ]
    }
  ],
  "professional_trajectory": {
    "postdoc_experience": [
      {
        "institution": "ESALQ/USP (2024 - Atual)",
        "role": "Pesquisador de Pós-Doutorado (Bolsista FAPESP)",
        "project": "DecisionES-BR: Apoio à Decisão para o Fornecimento de Serviços Ecossistêmicos sob Mudança Global (Cooperação H2020 Marie Curie)",
        "activities": "Modelagem espacial de serviços ecossistêmicos, otimização de restauração na Mata Atlântica e colaboração em docência de Métodos Quantitativos e Pesquisa Operacional."
      },
      {
        "institution": "Freie Universität Berlin (2023 - 2024)",
        "role": "Pesquisador Convidado (Sensoriamento Remoto)",
        "project": "Modelagem e Simulação de Florestas Virtuais e Dados LiDAR",
        "activities": "Desenvolvimento de algoritmos em ambiente R para simulação de ecossistemas virtuais e nuvens de pontos LiDAR para estimativa de biomassa e estrutura florestal."
      },
      {
        "institution": "UNESP - ICTS Sorocaba (2023 - 2024)",
        "role": "Pós-Doutorando",
        "project": "Análise Temporal do Fluxo de Carbono e Modelo de Predição Através de Índices Espectrais (APA Itupararanga)",
        "activities": "Modelagem espectral sPRI x NDVI e simulação preditiva de cenários futuros."
      }
    ],
    "environmental_consulting": [
      {
        "role": "Consultor Ambiental Autônomo (Habilitação FIA / SEMIL)",
        "period": "2010 - 2012",
        "scope": "Vistorias de fiscalização de passivos ambientais, análise de cumprimento de Termos de Ajuste de Conduta (TAC) do Ministério Público, fiscalização de Autos de Infração Ambiental (AIA) e acompanhamento de PRADs em colaboração com CETESB."
      },
      {
        "role": "Analista Ambiental (MEDRAL Meio Ambiente)",
        "period": "2011 - 2012",
        "scope": "Licenciamento Ambiental completo (LP, LI, LO), relatórios técnicos (EIA/RIMA, RAP, EIV, RAD) em linhas de transmissão de energia e empreendimentos imobiliários; mapeamento de APPs e Reserva Legal em SIG."
      }
    ],
    "university_teaching": [
      {
        "institution": "Universidade de Sorocaba (UNISO)",
        "role": "Professor Adjunto I (2018 - 2021)",
        "scope": "Docência nos cursos de Engenharia Ambiental, Engenharia Agronômica, Ciências Biológicas e Psicologia em disciplinas como Sistemas de Informações Geográficas (SIG), Cartografia Básica, Ecologia e Recuperação de Áreas Degradadas. Membro do Colegiado de Engenharia Ambiental."
      },
      {
        "institution": "UNESP & ESALQ/USP",
        "role": "Tutor e Docente Convidado",
        "scope": "Aulas práticas de geotecnologias, manipulação de imagens de satélite, análise estatística e apoio a turmas de pós-graduação e graduação."
      }
    ],
    "technical_projects": [
      "Revisão do Plano Diretor e Legislação Urbanística Específica do Município de Rio Grande da Serra/SP (IPT/CTGeo).",
      "Delimitação das Zonas Potenciais à Contaminação por Nitrato nas Águas Subterrâneas dos Sistemas Aquíferos Bauru e Guarani no Estado de São Paulo (IPT)."
    ]
  }
}

@st.cache_data
def get_portfolio_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(current_dir, "portfolio_data.json"),
        os.path.join(current_dir, "portfolio_data (1).json"),
        "portfolio_data.json"
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return PORTFOLIO_DB

data = get_portfolio_data()
res = data["researcher"]
paper = data["featured_manuscript"]
top5 = data["top_5_articles"]
sols = data["commercial_solutions"]
traj = data["professional_trajectory"]

def get_profile_photo_b64():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(current_dir, "foto_curriculo1.jpg"),
        os.path.join(current_dir, "foto_curriculo1.png"),
        os.path.join(current_dir, "foto_curriculo.jpg"),
        os.path.join(current_dir, "foto.jpg"),
        os.path.join(current_dir, "perfil.jpg"),
        "foto_curriculo1.jpg",
        "foto_curriculo1.png",
        "foto_curriculo.jpg",
        "foto.jpg"
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                from PIL import Image
                import io
                im = Image.open(c)
                w, h = im.size
                if h > w and w >= 800:
                    # Enquadramento facial centralizado e com zoom aumentado (foco clássico de retrato no rosto de Jomil)
                    scale_factor = w / 1200.0
                    cx = int(380 * scale_factor)
                    cy = int(800 * scale_factor)
                    side = int(560 * scale_factor)
                    left = max(0, cx - side // 2)
                    top = max(0, cy - side // 2)
                    right = min(w, left + side)
                    bottom = min(h, top + side)
                    im = im.crop((left, top, right, bottom))
                elif w > h:
                    side = h
                    left = int((w - side) / 2)
                    im = im.crop((left, 0, left + side, h))
                
                im = im.resize((450, 450), Image.Resampling.LANCZOS)
                buf = io.BytesIO()
                im.save(buf, format="JPEG", quality=95)
                return base64.b64encode(buf.getvalue()).decode("utf-8")
            except Exception:
                try:
                    with open(c, "rb") as img_f:
                        return base64.b64encode(img_f.read()).decode("utf-8")
                except Exception:
                    pass
    return None

def get_biology_symbol_svg(size=28):
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block; filter: drop-shadow(0 1px 2px rgba(0,0,0,0.15));">
      <defs>
        <linearGradient id="bioBgGrad_{size}" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#C2E6F8" />
          <stop offset="100%" stop-color="#80C4EE" />
        </linearGradient>
      </defs>
      <circle cx="50" cy="50" r="47" fill="url(#bioBgGrad_{size})" stroke="#5BAFE3" stroke-width="2.5" />
      <ellipse cx="44" cy="22" rx="16" ry="7" stroke="#0284C7" stroke-width="3" fill="none" transform="rotate(-15 44 22)" />
      <ellipse cx="48" cy="34" rx="15" ry="6.5" stroke="#0284C7" stroke-width="3" fill="none" transform="rotate(-10 48 34)" />
      <ellipse cx="46" cy="46" rx="13" ry="5.5" stroke="#0284C7" stroke-width="3" fill="none" transform="rotate(-12 46 46)" />
      <line x1="33" y1="20" x2="55" y2="24" stroke="#0284C7" stroke-width="2.2" />
      <line x1="36" y1="33" x2="59" y2="35" stroke="#0284C7" stroke-width="2.2" />
      <line x1="36" y1="45" x2="56" y2="47" stroke="#0284C7" stroke-width="2.2" />
      <path d="M48 48 C43 56, 49 68, 59 78 C65 84, 66 89, 62 92 C58 95, 53 91, 51 84 C48 74, 42 62, 45 49 Z" fill="#0369A1" />
      <circle cx="58" cy="85" r="4" fill="#E0F2FE" />
      <path d="M15 62 C18 80, 36 92, 53 95 C46 88, 30 80, 26 67 C23 58, 20 60, 15 62 Z" fill="#65A30D" />
      <path d="M16 63 C25 80, 42 90, 52 94 C34 90, 22 78, 16 63 Z" fill="#84CC16" />
      <path d="M62 43 C78 52, 91 68, 86 85 C81 92, 68 95, 57 93 C67 88, 76 78, 74 65 C72 54, 67 47, 62 43 Z" fill="#15803D" />
      <path d="M72 68 C76 68, 78 72, 77 75 C75 79, 70 80, 67 77 C65 74, 66 70, 70 70 C72 70, 73 72, 72 73" stroke="#86EFAC" stroke-width="2.2" fill="none" stroke-linecap="round" />
    </svg>"""

def get_figure_image_b64(fig_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base = fig_name.rsplit('.', 1)[0]
    candidates = [
        os.path.join(current_dir, fig_name),
        os.path.join(current_dir, base + '.png'),
        os.path.join(current_dir, base + '.jpg'),
        os.path.join(current_dir, base + '.jpeg'),
        os.path.join(current_dir, "artigos_midia", "artigo_01_preprint", fig_name),
        os.path.join(current_dir, "artigos_midia", "artigo_01_preprint", base + '.png'),
        os.path.join(current_dir, "artigos_midia", "artigo_01_preprint", base + '.jpg'),
        os.path.join(current_dir, "artigos_midia", "artigo_01_preprint", base + '.jpeg'),
        fig_name,
        base + '.png',
        base + '.jpg'
    ]
    # Busca automática em todas as subpastas de artigos_midia
    artigos_midia_dir = os.path.join(current_dir, "artigos_midia")
    if os.path.exists(artigos_midia_dir):
        for root, dirs, files in os.walk(artigos_midia_dir):
            for f in files:
                if f.lower() == fig_name.lower() or f.lower().startswith(base.lower()):
                    candidates.append(os.path.join(root, f))
    # Caso especial para figure 4s
    if '04' in fig_name:
        candidates.extend([
            os.path.join(current_dir, 'Figure_04s.png'),
            os.path.join(current_dir, 'Figure_04.png'),
            os.path.join(current_dir, 'artigos_midia', 'artigo_01_preprint', 'Figure_04s.png'),
            os.path.join(current_dir, 'artigos_midia', 'artigo_01_preprint', 'Figure_04.png'),
            'Figure_04s.png', 'Figure_04.png'
        ])
    for c in candidates:
        if os.path.exists(c):
            try:
                with open(c, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            except Exception:
                pass
    return None

def get_biology_symbol_html(size=28):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(current_dir, "simbolo-da-biologia.webp"),
        os.path.join(current_dir, "simolo-da-biologia.webp"),
        os.path.join(current_dir, "simbolo-da-biologia.web"),
        os.path.join(current_dir, "simolo-da-biologia.web"),
        os.path.join(current_dir, "simbolo_biologia.webp"),
        os.path.join(current_dir, "simbolo_biologia.png"),
        "simbolo-da-biologia.webp",
        "simolo-da-biologia.webp",
        "simbolo-da-biologia.web",
        "simolo-da-biologia.web",
        "simbolo_biologia.webp",
        "simbolo_biologia.png"
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                with open(c, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode("utf-8")
                    return f'<img src="data:image/webp;base64,{b64}" width="{size}" height="{size}" style="vertical-align: middle; border-radius: 50%; object-fit: contain; filter: drop-shadow(0 1px 2px rgba(0,0,0,0.15)); display: inline-block;" />'
            except Exception:
                pass
    return get_biology_symbol_svg(size)

WEBSIG_STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "websig")
WEBSIG_MAP_TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "websig", "map.html")

@st.cache_data
def read_text_file(path, mtime):
    # mtime entra na chave do cache para refletir um novo build sem reiniciar o app
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_websig_manifest():
    path = os.path.join(WEBSIG_STATIC_DIR, "manifest.json")
    if not os.path.exists(path):
        return None
    return json.loads(read_text_file(path, os.path.getmtime(path)))

def get_arte_cartao(base):
    """Arte do cartão de atuação.

    Usa a imagem salva em static/ilustracoes/ (servida pelo Streamlit, sem
    embutir em base64). Sem imagem, cai no desenho SVG de ilustracoes/.
    """
    raiz = os.path.dirname(os.path.abspath(__file__))
    for ext in ("png", "jpg", "jpeg", "webp"):
        arquivo = os.path.join(raiz, "static", "ilustracoes", f"{base}.{ext}")
        if os.path.exists(arquivo):
            versao = int(os.path.getmtime(arquivo))
            return f'<img class="arte" src="app/static/ilustracoes/{base}.{ext}?v={versao}" alt="" />', True
    desenho = os.path.join(raiz, "ilustracoes", f"{base}.svg")
    if os.path.exists(desenho):
        return read_text_file(desenho, os.path.getmtime(desenho)), False
    return "", False

def get_websig_map_html():
    return read_text_file(WEBSIG_MAP_TEMPLATE, os.path.getmtime(WEBSIG_MAP_TEMPLATE))

def html_block(html):
    """Renderiza um bloco HTML com segurança.

    No Markdown, uma linha em branco encerra o bloco HTML e faz o restante
    indentado virar bloco de código — que aparecia como script na página.
    """
    st.markdown("\n".join(line.strip() for line in html.strip().splitlines() if line.strip()),
                unsafe_allow_html=True)

def inline_md(text):
    """Converte a marcação inline dos textos dos artigos (**negrito**) para HTML."""
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text

@st.cache_data
def get_article_figure_b64(pasta, arquivo):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for candidate in (os.path.join(current_dir, pasta, arquivo), os.path.join(current_dir, arquivo)):
        if os.path.exists(candidate):
            try:
                with open(candidate, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            except OSError:
                pass
    return None

photo_b64 = get_profile_photo_b64()

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;0,900;1,400&family=Inter:wght@400;500;600;700;800&display=swap');

    /* Fundo da Página: Tons de verde esfumaçado, bem clarinho */
    .stApp {
        background: linear-gradient(180deg, #EDF4EE 0%, #F5F8F5 45%, #E9F1EB 100%) !important;
        background-attachment: fixed !important;
        color: #1E293B;
    }
    div[data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #EDF4EE 0%, #F5F8F5 45%, #E9F1EB 100%) !important;
    }
    div[data-testid="stSidebar"] {
        background-color: #EEF4F0 !important;
        border-right: 1.5px solid #D1E0D5 !important;
    }

    .hero-magazine {
        background: linear-gradient(rgba(14, 43, 23, 0.72), rgba(14, 43, 23, 0.72)), 
                    url('https://images.unsplash.com/photo-1511497584788-87676104235f?auto=format&fit=crop&w=1600&q=80') center/cover no-repeat;
        border-radius: 12px;
        padding: 1.6rem 2.2rem;
        margin-top: -3.5rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border-left: 6px solid #16A34A;
    }
    .hero-title {
        font-family: 'Merriweather', serif;
        font-size: 2.35rem;
        font-weight: 900;
        color: #FFFFFF;
        letter-spacing: -0.02em;
        line-height: 1.15;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #F1F5F9;
        font-weight: 500;
        line-height: 1.4;
        margin-top: 0.35rem;
    }

    .profile-photo-img {
        width: 82px;
        height: 82px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #15803D;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    .profile-photo-hero {
        width: 96px;
        height: 96px;
        border-radius: 50%;
        object-fit: cover;
        border: 3.5px solid #FFFFFF;
        box-shadow: 0 4px 10px rgba(0,0,0,0.25);
    }

    .profile-card {
        margin-top: -3.8rem;
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        padding: 0.95rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        border-top: 4px solid #15803D;
    }
    .crbio-badge {
        display: inline-block;
        background-color: #ECFDF5;
        color: #065F46;
        border: 1px solid #A7F3D0;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        font-size: 0.76rem;
        font-weight: 700;
    }

    div[data-testid="stSidebar"] div.stButton > button {
        width: 100% !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 0.65rem 0.95rem !important;
        border-radius: 8px !important;
        font-size: 0.90rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.35rem !important;
        border: 1.5px solid #CBD5E1 !important;
        background-color: #FFFFFF !important;
        color: #334155 !important;
        transition: all 0.15s ease-in-out !important;
    }
    div[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #F1F5F9 !important;
        border-color: #15803D !important;
        color: #15803D !important;
        transform: translateX(2px);
    }
    div[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
        background-color: #ECFDF5 !important;
        border-color: #15803D !important;
        border-left: 6px solid #15803D !important;
        color: #065F46 !important;
        font-weight: 800 !important;
        box-shadow: 0 2px 4px rgba(21, 128, 61, 0.12) !important;
    }

    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 0.9rem;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        border-top: 3.5px solid #15803D;
        min-height: 105px;
    }
    .kpi-label {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #64748B;
        letter-spacing: 0.04em;
        margin-bottom: 0.25rem;
    }
    .kpi-value {
        font-family: 'Inter', sans-serif;
        font-size: 1.45rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.2;
        margin-bottom: 0.2rem;
    }
    .kpi-subtext {
        font-size: 0.82rem;
        font-weight: 600;
        color: #15803D;
        line-height: 1.3;
    }

    .clipping-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }
    .service-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #15803D;
        border-radius: 8px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }

    /* Grade de Ícones de Aplicativo de Celular (Mobile App Launcher) */
    .app-launcher-wrapper {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 14px;
        padding: 1.4rem 1.6rem 1.6rem 1.6rem;
        margin: 1.2rem 0 1.8rem 0;
        box-shadow: 0 4px 14px rgba(0,0,0,0.03);
    }
    .app-icon-card {
        background: #FFFFFF;
        border: 1.5px solid #CBD5E1;
        border-radius: 18px;
        padding: 1.25rem 0.75rem 1rem 0.75rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        transition: all 0.22s ease-in-out;
        min-height: 195px;
        height: 195px;
        justify-content: flex-start;
        cursor: pointer;
        user-select: none;
        position: relative;
    }
    .app-icon-squircle {
        width: 72px;
        height: 72px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 0.75rem;
        transition: transform 0.22s ease;
        flex-shrink: 0;
    }
    .app-icon-title {
        font-family: 'Merriweather', serif;
        font-size: 0.98rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.3rem;
        line-height: 1.25;
    }
    .app-icon-sub {
        font-size: 0.76rem;
        color: #64748B;
        line-height: 1.35;
    }
    
    /* Faz o botão do Streamlit cobrir exatamente o card com transparência total */
    div[data-testid="column"]:has(.app-icon-card) div.stButton {
        margin-top: -200px !important;
        height: 200px !important;
        position: relative !important;
        z-index: 10 !important;
        margin-bottom: 0px !important;
    }
    div[data-testid="column"]:has(.app-icon-card) div.stButton > button {
        height: 200px !important;
        width: 100% !important;
        opacity: 0 !important;
        background: transparent !important;
        border: none !important;
        cursor: pointer !important;
        border-radius: 18px !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    /* Efeito de movimento e hover ao passar o mouse sobre o card */
    div[data-testid="column"]:has(.app-icon-card):hover .app-icon-card {
        transform: translateY(-6px);
        border-color: #15803D;
        box-shadow: 0 10px 24px rgba(21, 128, 61, 0.16);
    }
    div[data-testid="column"]:has(.app-icon-card):hover .app-icon-squircle {
        transform: scale(1.08);
    }
    
    /* Cartão de Metadados Cartográficos */
    .metadata-card {
        background-color: #F8FAFC;
        border: 1.5px solid #CBD5E1;
        border-radius: 10px;
        padding: 1.1rem 1.4rem;
        margin-top: 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    .metadata-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 12px;
        margin-top: 0.6rem;
    }
    .metadata-item {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 0.55rem 0.8rem;
    }
    .metadata-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .metadata-val {
        font-size: 0.85rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 0.15rem;
    }
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    bio_symbol_sidebar = get_biology_symbol_html(size=26)
    
    if photo_b64:
        photo_html_sidebar = '<div style="width: 86px; height: 86px; min-width: 86px; min-height: 86px; border-radius: 50%; overflow: hidden; border: 3px solid #15803D; box-shadow: 0 2px 8px rgba(0,0,0,0.18); flex-shrink: 0; margin-right: 12px; background-color: #15803D;"><img src="data:image/jpeg;base64,' + photo_b64 + '" style="width: 100%; height: 100%; object-fit: cover; object-position: center center; display: block;" /></div>'
    else:
        photo_html_sidebar = '<div style="width: 86px; height: 86px; border-radius: 50%; background: #15803D; color: #FFF; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; font-weight: 800; border: 3px solid #A7F3D0; margin-right: 12px; flex-shrink: 0;">JC</div>'

    st.markdown(f"""
    <div class="profile-card">
        <div style="display: flex; align-items: center; margin-bottom: 0.6rem;">
            {photo_html_sidebar}
            <div>
                <span class="crbio-badge">CRBio nº 68816/01-D</span>\
                <div style="display: flex; align-items: center; gap: 6px; margin-top: 0.2rem;">
                    <b style="font-size: 1.05rem; color: #0F172A; font-family: 'Merriweather', serif;">Dr. Jomil Costa Abreu Sales</b>
                    {bio_symbol_sidebar}
                </div>
            </div>
        </div>
        <div style="font-size: 0.78rem; color: #475569; line-height: 1.35; border-top: 1px solid #F1F5F9; padding-top: 0.5rem;">
            <b>Biólogo | Pós-Doutor em Ciências Florestais (ESALQ/USP)</b><br>
            Doutor em Ciências Ambientais (UNESP / TU Berlin)<br>
            <span style="color: #15803D; font-weight: 700;">Geotecnologias, Sensoriamento Remoto & IA</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-size: 0.78rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.4rem;'>Menu Principal</p>", unsafe_allow_html=True)
    
    menu_options = [
        "Página Inicial",
        "Artigos Científicos & Publicações",
        "WebSIG Interativo (APA Itupararanga)",
        "Criações com IA & Produtos",
        "Consultoria Ambiental & Tutoria em SIG",
        "Trajetória Profissional & Docência"
    ]
    
    if "active_section" not in st.session_state:
        st.session_state.active_section = menu_options[0]

    for opt in menu_options:
        is_active = (st.session_state.active_section == opt)
        if st.button(
            opt,
            key=f"nav_btn_{opt}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.active_section = opt
            st.rerun()

    selected_section = st.session_state.active_section

    st.markdown("---")
    st.markdown("<p style='font-size: 0.76rem; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 0.3rem;'>Links & Identificadores</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 8px; padding: 0.7rem 0.9rem;">
        <!-- LinkedIn -->
        <a href="https://www.linkedin.com/in/jomil-costa-phd-53817838/" target="_blank" rel="noopener noreferrer" style="display: flex; align-items: center; padding: 0.35rem 0; color: #334155; text-decoration: none; font-size: 0.82rem; font-weight: 600; border-bottom: 1px solid #F1F5F9;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="#0A66C2" style="margin-right: 8px; flex-shrink: 0;"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 8.76a1.65 1.65 0 1 0-.02-3.3 1.65 1.65 0 0 0 .02 3.3m1.4 9.74V9.93H5.06v8.57h2.8z"/></svg>
            LinkedIn Perfil
        </a>
        <!-- ORCID -->
        <a href="https://orcid.org/0000-0001-8722-8398" target="_blank" rel="noopener noreferrer" style="display: flex; align-items: center; padding: 0.35rem 0; color: #334155; text-decoration: none; font-size: 0.82rem; font-weight: 600; border-bottom: 1px solid #F1F5F9;">
            <svg width="18" height="18" viewBox="0 0 256 256" style="margin-right: 8px; flex-shrink: 0;"><path fill="#A6CE39" d="M128 0C57.3 0 0 57.3 0 128s57.3 128 128 128 128-57.3 128-128S198.7 0 128 0z"/><path fill="#FFF" d="M86.3 186.2H70.9V79.1h15.4v107.1zm41.3-70.8c-1.3-.8-3.4-1.2-6.2-1.2h-11.8v40.3h11.8c2.9 0 5-.4 6.3-1.3 1.3-.9 2.2-2.1 2.8-3.8.6-1.7.9-3.9.9-6.7 0-4.4-.8-7.7-2.3-9.8-1.5-2.2-3.7-3.4-6.6-3.8 2.2-.8 3.9-2 5.1-3.6 1.2-1.7 1.8-3.8 1.8-6.4 0-2.4-.6-4.4-1.8-6.1-1.3-1.6-3.1-2.8-5.5-3.6zm19.8 45.4c-2.3 3.9-5.4 6.8-9.4 8.7-3.9 1.9-8.7 2.9-14.2 2.9h-26v-73.4h26c5.4 0 10.1 1 14 3 3.9 2 6.9 4.8 9 8.6 2.1 3.7 3.2 8.3 3.2 13.6 0 5.4-1 9.9-3.1 13.5-2.1 3.7-5 6.4-8.5 8.2 4.1 1.7 7.4 4.3 9.8 7.9 2.4 3.6 3.6 8.1 3.6 13.5 0 5.8-1.5 10.7-4.4 14.7z"/><circle fill="#FFF" cx="78.4" cy="54.2" r="9.3"/></svg>
            ORCID 0000-0001-8722-8398
        </a>
        <!-- Currículo Lattes (CNPq) -->
        <a href="http://lattes.cnpq.br/0266681173969604" target="_blank" rel="noopener noreferrer" style="display: flex; align-items: center; padding: 0.35rem 0; color: #334155; text-decoration: none; font-size: 0.82rem; font-weight: 600; border-bottom: 1px solid #F1F5F9;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="#0284C7" style="margin-right: 8px; flex-shrink: 0;"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>
            Currículo Lattes (CNPq)
        </a>
        <!-- Google Acadêmico -->
        <a href="https://scholar.google.com/citations?user=3ymOKh8AAAAJ&hl=en" target="_blank" rel="noopener noreferrer" style="display: flex; align-items: center; padding: 0.35rem 0; color: #334155; text-decoration: none; font-size: 0.82rem; font-weight: 600; border-bottom: 1px solid #F1F5F9;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="#4285F4" style="margin-right: 8px; flex-shrink: 0;"><path d="M12 3L1 9l4 2.18v6L12 21l7-3.82v-6l2-1.09V17h2V9L12 3zm6.82 6L12 12.72 5.18 9 12 5.28 18.82 9zM17 15.99l-5 2.73-5-2.73v-3.72L12 15l5-2.73v3.72z"/></svg>
            Google Acadêmico
        </a>
        <!-- ResearchGate -->
        <a href="https://www.researchgate.net/profile/Jomil-Sales" target="_blank" rel="noopener noreferrer" style="display: flex; align-items: center; padding: 0.35rem 0; color: #334155; text-decoration: none; font-size: 0.82rem; font-weight: 600; border-bottom: 1px solid #F1F5F9;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="#00CCBB" style="margin-right: 8px; flex-shrink: 0;"><path d="M19.5 21a3 3 0 0 0 3-3v-4.5a3 3 0 0 0-3-3h-1.5v-3A4.5 4.5 0 0 0 13.5 3h-6A4.5 4.5 0 0 0 3 7.5v9A4.5 4.5 0 0 0 7.5 21h12zM7.5 5h6A2.5 2.5 0 0 1 16 7.5v3h-8.5A2.5 2.5 0 0 1 5 8V7.5A2.5 2.5 0 0 1 7.5 5zm-2.5 11.5v-4A2.5 2.5 0 0 1 7.5 10H16v.5A2.5 2.5 0 0 1 13.5 13H10v2h3.5A2.5 2.5 0 0 1 16 17.5v.5H7.5A2.5 2.5 0 0 1 5 16.5z"/></svg>
            ResearchGate
        </a>
        <!-- Preprint SSRN -->
        <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7268395" target="_blank" rel="noopener noreferrer" style="display: flex; align-items: center; padding: 0.35rem 0; color: #334155; text-decoration: none; font-size: 0.82rem; font-weight: 600; border-bottom: 1px solid #F1F5F9;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="#D97706" style="margin-right: 8px; flex-shrink: 0;"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
            Preprint SSRN (ID 7268395)
        </a>
        <!-- Contato E-mail -->
        <a href="mailto:jomil.sales@usp.br" style="display: flex; align-items: center; padding: 0.35rem 0; color: #334155; text-decoration: none; font-size: 0.82rem; font-weight: 600;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="#15803D" style="margin-right: 8px; flex-shrink: 0;"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
            Contato: jomil.sales@usp.br
        </a>
    </div>
    """, unsafe_allow_html=True)

bio_symbol_hero = get_biology_symbol_html(size=36)
if photo_b64:
    photo_html_hero = '<div style="width: 104px; height: 104px; min-width: 104px; min-height: 104px; border-radius: 50%; overflow: hidden; border: 3.5px solid #FFFFFF; box-shadow: 0 4px 14px rgba(0,0,0,0.25); flex-shrink: 0; margin-right: 20px; background-color: #FFFFFF;"><img src="data:image/jpeg;base64,' + photo_b64 + '" style="width: 100%; height: 100%; object-fit: cover; object-position: center center; display: block;" /></div>'
else:
    photo_html_hero = '<div style="width: 104px; height: 104px; border-radius: 50%; background: #15803D; color: #FFF; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; font-weight: 800; border: 3.5px solid #FFFFFF; margin-right: 20px; flex-shrink: 0;">JC</div>'

st.markdown(f"""
<div class="hero-magazine">
    <div style="display: flex; align-items: center; flex-wrap: wrap;">
        {photo_html_hero}
        <div>
            <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                <span class="hero-title">Dr. Jomil Costa Abreu Sales</span>
                {bio_symbol_hero}
            </div>
            <div class="hero-subtitle">Biólogo (CRBio nº 68816/01-D) • Pós-Doutor em Ciências Florestais (ESALQ/USP) • Geotecnologias, WebSIG & Consultoria Ambiental</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


if selected_section == "Página Inicial":
    st.markdown("""
    <div style="margin: 1.1rem 0 0.6rem 0;">
        <h3 style="font-family: 'Merriweather', serif; color: #0F172A; margin: 0 0 0.2rem 0; font-size: 1.32rem;">
            Painel de Acesso & Áreas de Atuação
        </h3>
        <p style="font-size: 0.9rem; color: #475569; margin: 0;">
            Clique diretamente nos ícones abaixo para acessar as pesquisas científicas, geotecnologias e serviços especializados:
        </p>
    </div>
    """, unsafe_allow_html=True)

    app_cols = st.columns(5)

    # 1. Artigos Científicos (Livro de Estudos Ambientais com Broto Germinando - Sem Cruz Médica)
    with app_cols[0]:
        st.markdown("""
        <div class="app-icon-card" title="Clique para acessar Artigos Científicos">
            <div class="app-icon-squircle" style="background: linear-gradient(135deg, #065F46 0%, #10B981 100%); box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);">
                <svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                    <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                    <path d="M12 7c-1.5-2.2-3.5-3-3.5-3s.5 2.2 1.8 3.5c1 1 1.7 1.5 1.7 1.5"></path>
                    <path d="M12 7c1.5-2.2 3.5-3 3.5-3s-.5 2.2-1.8 3.5c-1 1-1.7 1.5-1.7 1.5"></path>
                    <line x1="12" y1="7" x2="12" y2="15"></line>
                </svg>
            </div>
            <div class="app-icon-title">Artigos Científicos</div>
            <div class="app-icon-sub">Pesquisas, Hipóteses & Produtos</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Artigos", key="launch_app_prod", use_container_width=True):
            st.session_state.active_section = "Artigos Científicos & Publicações"
            st.rerun()

    # 2. WebSIG Espacial (Mapa e Polígonos Cartográficos)
    with app_cols[1]:
        st.markdown("""
        <div class="app-icon-card" title="Clique para acessar o WebSIG Espacial">
            <div class="app-icon-squircle" style="background: linear-gradient(135deg, #0369A1 0%, #0284C7 100%); box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);">
                <svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon>
                    <line x1="8" y1="2" x2="8" y2="18"></line>
                    <line x1="16" y1="6" x2="16" y2="22"></line>
                </svg>
            </div>
            <div class="app-icon-title">WebSIG Espacial</div>
            <div class="app-icon-sub">APA Itupararanga & SIG</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("WebSIG", key="launch_app_websig", use_container_width=True):
            st.session_state.active_section = "WebSIG Interativo (APA Itupararanga)"
            st.rerun()

    # 3. Criações com IA (Rosto de Robô / Agente de IA Evidente com Antena, Olhos e Visor)
    with app_cols[2]:
        st.markdown("""
        <div class="app-icon-card" title="Clique para acessar Criações com IA">
            <div class="app-icon-squircle" style="background: linear-gradient(135deg, #4338CA 0%, #7C3AED 100%); box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);">
                <svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="12" y1="1" x2="12" y2="4"></line>
                    <circle cx="12" cy="1.2" r="1.2" fill="#FFFFFF"></circle>
                    <rect x="3" y="5" width="18" height="15" rx="4" ry="4"></rect>
                    <circle cx="8" cy="11" r="2.2" fill="#FFFFFF"></circle>
                    <circle cx="16" cy="11" r="2.2" fill="#FFFFFF"></circle>
                    <line x1="8" y1="16" x2="16" y2="16"></line>
                    <line x1="1" y1="12" x2="3" y2="12"></line>
                    <line x1="21" y1="12" x2="23" y2="12"></line>
                </svg>
            </div>
            <div class="app-icon-title">Criações com IA</div>
            <div class="app-icon-sub">Agentes & Modelos ML</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("IA", key="launch_app_ai", use_container_width=True):
            st.session_state.active_section = "Criações com IA & Produtos"
            st.rerun()

    # 4. Consultoria & Tutoria SIG (Quadro Técnico de Ensino com Planta/Folha Ambiental)
    with app_cols[3]:
        st.markdown("""
        <div class="app-icon-card" title="Clique para acessar Consultoria & Tutoria SIG">
            <div class="app-icon-squircle" style="background: linear-gradient(135deg, #B45309 0%, #F59E0B 100%); box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);">
                <svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="2" y="3" width="20" height="13" rx="2" ry="2"></rect>
                    <path d="M12 6.5c-2 0-3.6 1.5-3.6 3.5 0 2.6 3.6 3.8 3.6 3.8s3.6-1.2 3.6-3.8c0-2-1.6-3.5-3.6-3.5z"></path>
                    <line x1="12" y1="6.5" x2="12" y2="13.8"></line>
                    <line x1="12" y1="16" x2="12" y2="21"></line>
                    <line x1="8" y1="21" x2="16" y2="21"></line>
                </svg>
            </div>
            <div class="app-icon-title">Consultoria & Tutoria SIG</div>
            <div class="app-icon-sub">Geoprocessamento & Licenciamento</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Consultoria", key="launch_app_cons", use_container_width=True):
            st.session_state.active_section = "Consultoria Ambiental & Tutoria em SIG"
            st.rerun()

    # 5. Trajetória & Docência (Capelo Acadêmico de Docência Universitária)
    with app_cols[4]:
        st.markdown("""
        <div class="app-icon-card" title="Clique para acessar Trajetória & Docência">
            <div class="app-icon-squircle" style="background: linear-gradient(135deg, #1E293B 0%, #475569 100%); box-shadow: 0 4px 12px rgba(71, 85, 105, 0.3);">
                <svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 10v6M2 10l10-5 10 5-10 5z"></path>
                    <path d="M6 12v5c3 3 9 3 12 0v-5"></path>
                </svg>
            </div>
            <div class="app-icon-title">Trajetória & Docência</div>
            <div class="app-icon-sub">Memorial, USP & Cursos</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Trajetória", key="launch_app_traj", use_container_width=True):
            st.session_state.active_section = "Trajetória Profissional & Docência"
            st.rerun()




    st.markdown("""
    <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 10px; padding: 1.4rem 1.8rem; margin-top: 1.2rem; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
        <h4 style="font-family: 'Merriweather', serif; color: #0F172A; margin: 0 0 0.5rem 0; font-size: 1.15rem;">
            Apresentação & Propósito do Portfólio
        </h4>
        <p style="font-size: 0.94rem; color: #334155; line-height: 1.6; margin-bottom: 0.8rem;">
            Este ecossistema digital reúne a produção de pesquisa, inovação geoespacial e soluções ambientais do <b>Dr. Jomil Costa Abreu Sales</b>. 
            Com formação interdisciplinar em Biologia, Doutorado em Ciências Ambientais e Pós-Doutorado pelo Departamento de Ciências Florestais da <b>ESALQ/USP</b>, 
            sua atuação conecta o rigor de publicações científicas de ponta à prestação de serviços técnicos especializados em <b>ESG, créditos de carbono, conservação da biodiversidade e segurança hídrica</b>.
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px; margin-top: 1rem;">
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-left: 4px solid #15803D; border-radius: 8px; padding: 0.9rem;">
                <b style="color: #0F172A; font-size: 0.9rem;">🛰️ Geotecnologias & Sensoriamento Remoto</b>
                <p style="font-size: 0.82rem; color: #475569; margin: 0.3rem 0 0 0; line-height: 1.4;">
                    Processamento de dados Sentinel-2 (10 m), Landsat e MODIS em nuvem (Google Earth Engine e Python) para detecção precoce de degradação florestal funcional invisível ao desmatamento tradicional.
                </p>
            </div>
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-left: 4px solid #0284C7; border-radius: 8px; padding: 0.9rem;">
                <b style="color: #0F172A; font-size: 0.9rem;">🤖 Inteligência Artificial & RAG Científico</b>
                <p style="font-size: 0.82rem; color: #475569; margin: 0.3rem 0 0 0; line-height: 1.4;">
                    Desenvolvimento de agentes conversacionais que explicam artigos com rigor acadêmico, além de modelos de transição de uso do solo com redes neurais artificiais (ANN-MLP).
                </p>
            </div>
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-left: 4px solid #D97706; border-radius: 8px; padding: 0.9rem;">
                <b style="color: #0F172A; font-size: 0.9rem;">💼 Consultoria Ambiental & Regularização</b>
                <p style="font-size: 0.82rem; color: #475569; margin: 0.3rem 0 0 0; line-height: 1.4;">
                    Elaboração de EIA/RIMA, PRADs, laudos de cobertura vegetal e valoração de serviços ecossistêmicos com suporte analítico ao ICMS Ecológico e IVEG.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


elif selected_section in ["Artigos Científicos & Publicações", "Produção Científica & Interativa", "Artigos Científicos"]:
    html_block("""
    <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-left: 6px solid #15803D; border-radius: 10px; padding: 1.3rem 1.6rem; margin-bottom: 1.2rem; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
        <h2 style="font-family: 'Merriweather', serif; color: #0F172A; margin: 0 0 0.3rem 0; font-size: 1.65rem;">
            📚 Artigos Científicos &amp; Dossiês de Pesquisa
        </h2>
        <p style="font-size: 0.96rem; color: #475569; margin: 0; line-height: 1.5;">
            Conheça abaixo as pesquisas e publicações científicas, estruturadas sob a ótica executiva de <b>Pergunta Central, Problema &amp; Hipótese, Resultados Obtidos e Soluções Propostas</b>, com navegação pelas figuras originais de cada estudo.
        </p>
    </div>
    """)

    if "selected_article_id" not in st.session_state:
        st.session_state.selected_article_id = 1

    st.markdown("<p style='font-size: 0.82rem; font-weight: 700; color: #475569; text-transform: uppercase; margin-bottom: 0.4rem;'>Selecione a publicação para visualizar o dossiê &amp; as figuras do estudo:</p>", unsafe_allow_html=True)

    STATUS_CORES = {
        "destaque": ("#15803D", "#DCFCE7", "#BBF7D0"),
        "publicado": ("#0369A1", "#E0F2FE", "#BAE6FD"),
        "submissao": ("#B45309", "#FEF3C7", "#FDE68A"),
    }

    art_cols = st.columns(3)
    for idx_a, artigo_card in enumerate(ARTIGOS):
        with art_cols[idx_a % 3]:
            is_active = (artigo_card["id"] == st.session_state.selected_article_id)
            cor_txt, cor_bg, cor_bd = STATUS_CORES[artigo_card["status"]]
            borda = "#15803D" if is_active else "#E2E8F0"
            fundo = "#F0FDF4" if is_active else "#FFFFFF"
            html_block(f"""
            <div style="border: 2px solid {borda}; background: {fundo}; border-radius: 12px; padding: 1rem 1.1rem; margin-bottom: 0.45rem; height: 236px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; gap: 8px;">
                        <span style="font-size: 0.72rem; font-weight: 800; color: {cor_txt}; background: {cor_bg}; border: 1px solid {cor_bd}; padding: 0.18rem 0.5rem; border-radius: 5px; white-space: nowrap;">{artigo_card["status_label"]}</span>
                        <span style="font-size: 0.78rem; color: #94A3B8; font-weight: 800;">#{artigo_card["id"]}</span>
                    </div>
                    <div style="font-size: 0.74rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.75rem; line-height: 1.35;">{artigo_card["tema"]}</div>
                    <div style="font-size: 0.78rem; color: #475569; margin-top: 0.4rem; line-height: 1.4;">{len(artigo_card["figuras"])} figura(s) · {len(artigo_card["perguntas"])} perguntas</div>
                </div>
                <div style="border-top: 1px solid #E2E8F0; padding-top: 0.6rem;">
                    <div style="font-family: 'Merriweather', serif; font-size: 0.9rem; font-weight: 700; color: #0F172A; line-height: 1.3; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;">{artigo_card["titulo"]}</div>
                    <div style="font-size: 0.76rem; color: #64748B; margin-top: 0.35rem; line-height: 1.35;">{artigo_card["veiculo"]} · <b>{artigo_card["ano"]}</b></div>
                </div>
            </div>
            """)
            btn_label = f"Visualizar #{artigo_card['id']}" + (" (Ativo)" if is_active else "")
            if st.button(btn_label, key=f"sel_art_btn_{artigo_card['id']}", use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state.selected_article_id = artigo_card["id"]
                st.rerun()

    artigo = ARTIGOS_POR_ID[st.session_state.selected_article_id]
    cor_txt, cor_bg, cor_bd = STATUS_CORES[artigo["status"]]

    # -------------------------------------------------------------------------
    # CABEÇALHO DO ARTIGO SELECIONADO
    # -------------------------------------------------------------------------
    chips = [(artigo["status_label"], cor_txt, cor_bg, cor_bd),
             (artigo["veiculo"], "#334155", "#F1F5F9", "#E2E8F0"),
             (artigo["tema"], "#334155", "#F1F5F9", "#E2E8F0")]
    if artigo.get("financiamento"):
        chips.append((artigo["financiamento"], "#92400E", "#FEF3C7", "#FDE68A"))
    chips_html = "".join(
        f'<span style="font-size: 0.74rem; font-weight: 700; color: {c}; background: {b}; border: 1px solid {d}; padding: 0.2rem 0.55rem; border-radius: 5px;">{t}</span>'
        for t, c, b, d in chips)
    link_html = ""
    if artigo.get("link_url"):
        link_html = f'<br><a href="{artigo["link_url"]}" target="_blank" rel="noopener noreferrer" style="color: #15803D; font-weight: 700;">{artigo["link_label"]} ↗</a>'
    html_block(f"""
    <div style="background-color: #FFFFFF; border: 1.5px solid #CBD5E1; border-radius: 10px; padding: 1.4rem 1.6rem; margin: 1rem 0 1.2rem 0; box-shadow: 0 3px 8px rgba(0,0,0,0.03);">
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 0.6rem;">{chips_html}</div>
        <h3 style="font-family: 'Merriweather', serif; color: #0F172A; font-size: 1.32rem; margin: 0.3rem 0 0.6rem 0; line-height: 1.35;">{artigo["titulo"]}</h3>
        <p style="font-size: 0.87rem; color: #475569; margin: 0; line-height: 1.55;">
            <b>Autores:</b> {artigo["autores"]}<br>
            <b>Minha participação:</b> {artigo["meu_papel"]}{link_html}
        </p>
    </div>
    """)

    # -------------------------------------------------------------------------
    # OS 4 PILARES DA INVESTIGAÇÃO
    # -------------------------------------------------------------------------
    html_block("""
    <div style="margin: 1.3rem 0 0.7rem 0;">
        <h4 style="font-family: 'Merriweather', serif; color: #0F172A; margin: 0 0 0.2rem 0; font-size: 1.25rem;">
            🎯 Estrutura Fundamental da Pesquisa: Da Pergunta à Solução Territorial
        </h4>
        <p style="font-size: 0.9rem; color: #475569; margin: 0;">
            Síntese executiva dos fundamentos metodológicos, empíricos e práticos que norteiam este estudo:
        </p>
    </div>
    """)

    pilar_cols = st.columns(2)
    with pilar_cols[0]:
        html_block(f"""
        <div style="background: #FFFFFF; border: 1.5px solid #CBD5E1; border-left: 6px solid #0284C7; border-radius: 10px; padding: 1.2rem; min-height: 275px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.6rem;">
                <span style="font-size: 1.4rem;">❓</span>
                <b style="font-size: 1.05rem; color: #0369A1; font-family: 'Merriweather', serif;">1. A Pergunta Central do Artigo</b>
            </div>
            <div style="font-size: 0.93rem; color: #0F172A; font-weight: 600; line-height: 1.5; background: #F0F9FF; padding: 0.7rem 0.9rem; border-radius: 6px; border: 1px solid #BAE6FD; margin-bottom: 0.6rem;">"{artigo["pergunta"]}"</div>
            <p style="font-size: 0.85rem; color: #334155; line-height: 1.45; margin: 0;">{artigo["pergunta_nota"]}</p>
        </div>
        """)
    with pilar_cols[1]:
        html_block(f"""
        <div style="background: #FFFFFF; border: 1.5px solid #CBD5E1; border-left: 6px solid #D97706; border-radius: 10px; padding: 1.2rem; min-height: 275px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.6rem;">
                <span style="font-size: 1.4rem;">⚠️</span>
                <b style="font-size: 1.05rem; color: #B45309; font-family: 'Merriweather', serif;">2. O Problema Levantado &amp; Hipótese</b>
            </div>
            <div style="font-size: 0.86rem; color: #1E293B; line-height: 1.45; margin-bottom: 0.5rem;"><b>O Problema Territorial:</b> {artigo["problema"]}</div>
            <div style="font-size: 0.86rem; color: #92400E; background: #FEF3C7; padding: 0.6rem 0.8rem; border-radius: 6px; border: 1px solid #FDE68A; line-height: 1.4;"><b>A Hipótese Científica:</b> {artigo["hipotese"]}</div>
        </div>
        """)

    pilar_cols2 = st.columns(2)
    with pilar_cols2[0]:
        itens = "".join(f"<li style='margin-bottom: 0.35rem;'>{inline_md(r)}</li>" for r in artigo["resultados"])
        html_block(f"""
        <div style="background: #FFFFFF; border: 1.5px solid #CBD5E1; border-left: 6px solid #15803D; border-radius: 10px; padding: 1.2rem; min-height: 300px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.6rem;">
                <span style="font-size: 1.4rem;">📊</span>
                <b style="font-size: 1.05rem; color: #15803D; font-family: 'Merriweather', serif;">3. Os Resultados Obtidos (Evidências)</b>
            </div>
            <ul style="font-size: 0.85rem; color: #1E293B; line-height: 1.45; margin: 0 0 0 1.1rem; padding: 0;">{itens}</ul>
        </div>
        """)
    with pilar_cols2[1]:
        itens = "".join(f"<p style='margin: 0 0 0.45rem 0;'>{inline_md(s)}</p>" for s in artigo["solucao"])
        html_block(f"""
        <div style="background: #FFFFFF; border: 1.5px solid #CBD5E1; border-left: 6px solid #0D9488; border-radius: 10px; padding: 1.2rem; min-height: 300px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.6rem;">
                <span style="font-size: 1.4rem;">💡</span>
                <b style="font-size: 1.05rem; color: #0F766E; font-family: 'Merriweather', serif;">4. A Solução para o Problema</b>
            </div>
            <div style="font-size: 0.85rem; color: #1E293B; line-height: 1.45;">{itens}</div>
        </div>
        """)

    # -------------------------------------------------------------------------
    # FIGURAS DO ARTIGO
    # -------------------------------------------------------------------------
    html_block("""
    <div style="margin: 1.6rem 0 0.8rem 0; border-top: 2px solid #E2E8F0; padding-top: 1.3rem;">
        <h4 style="font-family: 'Merriweather', serif; color: #0F172A; margin: 0; font-size: 1.28rem;">
            🗺️ Figuras &amp; Produtos Cartográficos do Artigo
        </h4>
        <p style="font-size: 0.88rem; color: #475569; margin: 0.3rem 0 0 0; line-height: 1.45;">
            A figura ativa é exibida em alta resolução. Use os botões abaixo dela para navegar entre as figuras do estudo e ler a descrição correspondente.
        </p>
    </div>
    """)

    figuras = artigo["figuras"]
    if not figuras:
        html_block(f"""
        <div style="background-color: #FFFBEB; border: 1.5px dashed #F59E0B; border-radius: 10px; padding: 1.6rem 1.4rem; margin: 0.6rem 0 1.2rem 0; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.4rem;">🗂️</div>
            <b style="color: #92400E; font-size: 1rem;">Figuras ainda não disponíveis</b>
            <p style="font-size: 0.86rem; color: #78350F; margin: 0.4rem 0 0 0; line-height: 1.5;">{artigo.get("figuras_pendentes", "")}</p>
        </div>
        """)
    else:
        fig_key = f"fig_idx_{artigo['id']}"
        if fig_key not in st.session_state:
            st.session_state[fig_key] = 0
        current_idx = max(0, min(st.session_state[fig_key], len(figuras) - 1))
        cur_fig = figuras[current_idx]

        fig_b64 = get_article_figure_b64(artigo["pasta"], cur_fig["arquivo"])
        if fig_b64:
            html_block(f"""
            <div style="background-color: #0F172A; border: 3px solid #1E293B; border-radius: 12px; padding: 1rem; text-align: center; margin: 0.9rem 0 0.6rem 0; box-shadow: 0 6px 18px rgba(0,0,0,0.15);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem; padding: 0 0.5rem; gap: 10px;">
                    <span style="color: #94A3B8; font-size: 0.8rem; font-weight: 600;">Figura {current_idx + 1} de {len(figuras)}</span>
                    <span style="color: #38BDF8; font-size: 0.8rem; font-weight: 600;">{cur_fig["titulo"]}</span>
                </div>
                <img src="data:image/png;base64,{fig_b64}" style="width: 100%; max-width: 1100px; border-radius: 6px; background: #FFFFFF; box-shadow: 0 4px 14px rgba(0,0,0,0.4);" />
            </div>
            """)
        else:
            html_block(f"""
            <div style="background-color: #F8FAFC; border: 2px dashed #94A3B8; border-radius: 10px; padding: 2rem 1.2rem; text-align: center; margin: 0.9rem 0 0.6rem 0;">
                <div style="font-size: 2.2rem; margin-bottom: 0.3rem;">🖼️</div>
                <b style="color: #0F172A; font-size: 1.05rem;">{cur_fig["titulo"]}</b>
                <p style="font-size: 0.86rem; color: #64748B; margin: 0.3rem 0 0 0;">Arquivo não encontrado em <code>{artigo["pasta"]}/{cur_fig["arquivo"]}</code>.</p>
            </div>
            """)

        nav_col1, nav_col2, nav_col3 = st.columns([1.2, 3.6, 1.2])
        with nav_col1:
            if st.button("◀ Figura anterior", key=f"btn_prev_fig_{artigo['id']}", use_container_width=True):
                st.session_state[fig_key] = (current_idx - 1) % len(figuras)
                st.rerun()
        with nav_col2:
            html_block(f"""
            <div style="text-align: center; background: #FFFFFF; border: 1.5px solid #CBD5E1; border-radius: 8px; padding: 0.45rem 0.8rem; box-shadow: 0 1px 4px rgba(0,0,0,0.03);">
                <span style="font-size: 0.88rem; font-weight: 800; color: #15803D;">Figura {current_idx + 1} de {len(figuras)}</span>
                <span style="font-size: 0.84rem; color: #475569; margin-left: 6px;">• {cur_fig["titulo"]}</span>
            </div>
            """)
        with nav_col3:
            if st.button("Próxima figura ▶", key=f"btn_next_fig_{artigo['id']}", use_container_width=True, type="primary"):
                st.session_state[fig_key] = (current_idx + 1) % len(figuras)
                st.rerun()

        st.markdown("<p style='font-size: 0.74rem; font-weight: 700; color: #64748B; text-transform: uppercase; margin: 0.5rem 0 0.3rem 0;'>Seleção rápida (clique no número para alternar):</p>", unsafe_allow_html=True)
        film_cols = st.columns(len(figuras))
        for f_idx, f_item in enumerate(figuras):
            with film_cols[f_idx]:
                if st.button(f"{f_idx + 1:02d}", key=f"film_frame_{artigo['id']}_{f_idx}", use_container_width=True,
                             type="primary" if f_idx == current_idx else "secondary", help=f_item["titulo"]):
                    st.session_state[fig_key] = f_idx
                    st.rerun()

        meta_items = "".join(
            f'<div class="metadata-item"><div class="metadata-label">{k}</div><div class="metadata-val">{v}</div></div>'
            for k, v in cur_fig["meta"].items())
        fonte = artigo.get("figuras_origem", "")
        fonte_html = f'<div style="font-size: 0.76rem; color: #64748B; margin-top: 0.9rem; border-top: 1px solid #E2E8F0; padding-top: 0.6rem;"><b>Fonte:</b> {artigo["referencia"]} {fonte}</div>' if fonte else ""
        html_block(f"""
        <div style="background-color: #FFFFFF; border: 1.5px solid #CBD5E1; border-radius: 10px; padding: 1.3rem 1.5rem; margin: 1rem 0 1.4rem 0; box-shadow: 0 3px 10px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #E2E8F0; padding-bottom: 0.6rem; margin-bottom: 0.9rem; gap: 10px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.25rem;">🔎</span>
                    <b style="font-size: 1.05rem; color: #0F172A;">{cur_fig["titulo"]}</b>
                </div>
                <span style="font-size: 0.76rem; font-weight: 700; color: #15803D; background: #DCFCE7; padding: 0.2rem 0.6rem; border-radius: 4px; white-space: nowrap;">Descrição da figura</span>
            </div>
            <p style="color: #1E293B; font-size: 0.94rem; line-height: 1.65; margin: 0;">{cur_fig["descricao"]}</p>
            <div class="metadata-grid">{meta_items}</div>
            {fonte_html}
        </div>
        """)

    # -------------------------------------------------------------------------
    # PERGUNTAS FREQUENTES (RESPOSTAS ESCRITAS A PARTIR DO ARTIGO)
    # -------------------------------------------------------------------------
    html_block("""
    <div style="margin: 1.8rem 0 0.7rem 0; border-top: 2px solid #E2E8F0; padding-top: 1.2rem;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 1.35rem;">💬</span>
            <h4 style="font-family: 'Merriweather', serif; color: #0F172A; margin: 0; font-size: 1.25rem;">Perguntas frequentes sobre este artigo</h4>
        </div>
        <p style="font-size: 0.88rem; color: #475569; margin: 0.2rem 0 0.8rem 0;">
            Clique em uma pergunta para ver a resposta. O conteúdo foi redigido a partir do próprio artigo — números, fórmulas e conclusões vêm do texto publicado.
        </p>
    </div>
    """)

    for q_idx, qa in enumerate(artigo["perguntas"]):
        with st.expander(qa["pergunta"]):
            st.markdown(qa["resposta"])


elif selected_section == "WebSIG Interativo (APA Itupararanga)":
    st.markdown("""
    <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-left: 6px solid #15803D; border-radius: 10px; padding: 1.2rem 1.6rem; margin-bottom: 1.2rem; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
        <h2 style="font-family: 'Merriweather', serif; color: #0F172A; margin: 0 0 0.3rem 0; font-size: 1.6rem;">
            WebSIG & Produtos Cartográficos da APA de Itupararanga (938,31 km²)
        </h2>
        <p style="font-size: 0.95rem; color: #475569; margin: 0;">
            Visualizador interativo de shapefiles e rasters dos artigos, figuras oficiais do manuscrito e metadados
        </p>
    </div>
    """, unsafe_allow_html=True)

    websig_manifest = get_websig_manifest()

    tab_sig1, tab_sig2, tab_sig3 = st.tabs([
        "WebSIG Interativo (Camadas dos Artigos)",
        "Mapas Prontos do Artigo (Figuras Oficiais)",
        "Tabela de Metadados & Citação do Repositório"
    ])

    with tab_sig1:
        if websig_manifest is None:
            st.warning(
                "As camadas do WebSIG ainda não foram geradas. Rode `python tools/build_websig.py` "
                "com a pasta de shapefiles/rasters para criar `static/websig/`."
            )
        else:
            websig_html = get_websig_map_html()
            if hasattr(st, "iframe"):
                st.iframe(websig_html, height=720)
            else:  # Streamlit < 1.5x
                components.html(websig_html, height=720, scrolling=False)
            st.caption(
                "Ligue e desligue camadas no painel à esquerda (os dados carregam sob demanda, sem recarregar a página). "
                "Clique em qualquer ponto para consultar os valores das camadas ativas e use **Comparar** para a cortina 2019 × 2023."
            )

    with tab_sig2:
        st.markdown("### 🗺️ Atlas Cartográfico & Figuras Oficiais do Artigo")
        st.write("Abaixo estão reunidos todos os produtos cartográficos e gráficos finalizados que compõem o corpo do manuscrito da APA de Itupararanga:")

        fig_choice = st.radio(
            "Selecione o grupo de figuras para visualizar:",
            [
                "Resumo Gráfico (Graphical Abstract)",
                "Figura 1: Área de Estudo & Zoneamento da APA",
                "Figuras 2, 3 e 4: Cobertura da Terra (2019, 2023 & Projeção 2028)",
                "Figuras 5, 6 e 7: Potencial de Fluxo de CO₂ (2019, 2023 & 2028)",
                "Figuras 8 e 9: Validação Cruzada com MODIS GPP"
            ],
            horizontal=True
        )

        if fig_choice == "Resumo Gráfico (Graphical Abstract)":
            b64_abs = get_figure_image_b64("Image_abstract_REV.png")
            if b64_abs:
                st.markdown(f'''<div style="background: #FFFFFF; padding: 1rem; border-radius: 8px; border: 1.5px solid #CBD5E1; text-align: center; margin-bottom: 1rem; box-shadow: 0 2px 6px rgba(0,0,0,0.04);"><img src="data:image/png;base64,{b64_abs}" style="width: 100%; max-width: 1100px; border-radius: 6px;" /></div>''', unsafe_allow_html=True)
            st.markdown("""
            **Destaques do Resumo Gráfico:**
            - **Pipeline Espectral:** Sentinel-2 L2A (10 m) com cálculo simultâneo de biomassa verde (NDVI) e eficiência fotoquímica do uso da luz (sPRI).
            - **Achado Central:** Persistência de 91,8% da cobertura vegetal total (e 96% da floresta nativa), contrastando com retração de **-21,5%** nas áreas de alto potencial de fixação de CO₂ (de 200,8 km² para 157,7 km²).
            - **Simulação 2028:** Pelo modelo MOLUSCE / CA-Markov, o alto potencial cai para 145,2 km².
            - **Validação MODIS GPP:** Correlação significante com Produtividade Primária Bruta ($r = 0,66$ a $0,71$; $\\rho = 0,74$ a $0,75$; $p < 0,001$).
            """)

        elif fig_choice == "Figura 1: Área de Estudo & Zoneamento da APA":
            b64_f1 = get_figure_image_b64("Figure_01.png")
            if b64_f1:
                st.markdown(f'''<div style="background: #FFFFFF; padding: 1rem; border-radius: 8px; border: 1.5px solid #CBD5E1; text-align: center; margin-bottom: 1rem; box-shadow: 0 2px 6px rgba(0,0,0,0.04);"><img src="data:image/png;base64,{b64_f1}" style="width: 100%; max-width: 1050px; border-radius: 6px;" /></div>''', unsafe_allow_html=True)
            st.markdown("""
            **Descrição Cartográfica da Figura 1:**
            - **Enquadramento Geográfico:** Localização da APA de Itupararanga (938,31 km²) no contexto do Estado de São Paulo e Região Metropolitana de Sorocaba.
            - **Zoneamento Ambiental Oficial:**
              - **ZCB (Zona de Conservação da Biodiversidade - Verde):** Remanescentes contínuos mais preservados de Mata Atlântica ao sul da APA.
              - **ZCRH (Zona de Conservação de Recursos Hídricos - Roxo):** Faixa de proteção dos afluentes e do corpo da Represa de Itupararanga.
              - **ZOR (Zona de Ocupação Rural - Azul claro):** Predomínio de agricultura familiar e olericultura.
              - **ZOD e ZOC (Zonas de Ocupação Diversificada e Consolidada):** Centros urbanos de Ibiúna, São Roque e núcleos consolidados.
            """)

        elif fig_choice == "Figuras 2, 3 e 4: Cobertura da Terra (2019, 2023 & Projeção 2028)":
            b64_f2 = get_figure_image_b64("Figure_02.png")
            if b64_f2:
                st.markdown("##### Figura 2: Dinâmica Espaço-Temporal de Uso e Cobertura (2019 vs. 2023)")
                st.markdown(f'''<div style="background: #FFFFFF; padding: 1rem; border-radius: 8px; border: 1.5px solid #CBD5E1; text-align: center; margin-bottom: 1.2rem; box-shadow: 0 2px 6px rgba(0,0,0,0.04);"><img src="data:image/png;base64,{b64_f2}" style="width: 100%; max-width: 1050px; border-radius: 6px;" /></div>''', unsafe_allow_html=True)

            c_f3, c_f4 = st.columns(2)
            with c_f3:
                b64_f3 = get_figure_image_b64("Figure_03.png")
                if b64_f3:
                    st.markdown("##### Figura 3: Projeção Preditiva para 2028 (MOLUSCE)")
                    st.markdown(f'''<div style="background: #FFFFFF; padding: 0.8rem; border-radius: 8px; border: 1px solid #CBD5E1; text-align: center; margin-bottom: 1rem;"><img src="data:image/png;base64,{b64_f3}" style="width: 100%; border-radius: 6px;" /></div>''', unsafe_allow_html=True)
            with c_f4:
                b64_f4 = get_figure_image_b64("Figure_04s.png")
                if b64_f4:
                    st.markdown("##### Figura 4: Comparativo Quantitativo de Áreas (km²)")
                    st.markdown(f'''<div style="background: #FFFFFF; padding: 0.8rem; border-radius: 8px; border: 1px solid #CBD5E1; text-align: center; margin-bottom: 1rem;"><img src="data:image/png;base64,{b64_f4}" style="width: 100%; border-radius: 6px;" /></div>''', unsafe_allow_html=True)

        elif fig_choice == "Figuras 5, 6 e 7: Potencial de Fluxo de CO₂ (2019, 2023 & 2028)":
            b64_f5 = get_figure_image_b64("Figure_05.png")
            if b64_f5:
                st.markdown("##### Figura 5: Classes de Potencial de Fluxo de CO₂ (2019 vs. 2023)")
                st.markdown(f'''<div style="background: #FFFFFF; padding: 1rem; border-radius: 8px; border: 1.5px solid #CBD5E1; text-align: center; margin-bottom: 1.2rem; box-shadow: 0 2px 6px rgba(0,0,0,0.04);"><img src="data:image/png;base64,{b64_f5}" style="width: 100%; max-width: 1050px; border-radius: 6px;" /></div>''', unsafe_allow_html=True)

            c_f6, c_f7 = st.columns(2)
            with c_f6:
                b64_f6 = get_figure_image_b64("Figure_06.png")
                if b64_f6:
                    st.markdown("##### Figura 6: Projeção de Fluxo de CO₂ para 2028")
                    st.markdown(f'''<div style="background: #FFFFFF; padding: 0.8rem; border-radius: 8px; border: 1px solid #CBD5E1; text-align: center; margin-bottom: 1rem;"><img src="data:image/png;base64,{b64_f6}" style="width: 100%; border-radius: 6px;" /></div>''', unsafe_allow_html=True)
            with c_f7:
                b64_f7 = get_figure_image_b64("Figure_07.png")
                if b64_f7:
                    st.markdown("##### Figura 7: Distribuição das Classes de Carbono (km²)")
                    st.markdown(f'''<div style="background: #FFFFFF; padding: 0.8rem; border-radius: 8px; border: 1px solid #CBD5E1; text-align: center; margin-bottom: 1rem;"><img src="data:image/png;base64,{b64_f7}" style="width: 100%; border-radius: 6px;" /></div>''', unsafe_allow_html=True)

        elif fig_choice == "Figuras 8 e 9: Validação Cruzada com MODIS GPP":
            c_f8, c_f9 = st.columns(2)
            with c_f8:
                b64_f8 = get_figure_image_b64("Figure_08.png")
                if b64_f8:
                    st.markdown("##### Figura 8: Produtividade Primária Bruta (MODIS GPP 500 m)")
                    st.markdown(f'''<div style="background: #FFFFFF; padding: 0.8rem; border-radius: 8px; border: 1px solid #CBD5E1; text-align: center; margin-bottom: 1rem;"><img src="data:image/png;base64,{b64_f8}" style="width: 100%; border-radius: 6px;" /></div>''', unsafe_allow_html=True)
            with c_f9:
                b64_f9 = get_figure_image_b64("Figure_09.png")
                if b64_f9:
                    st.markdown("##### Figura 9: Regressão Estatística & Pureza Vegetal")
                    st.markdown(f'''<div style="background: #FFFFFF; padding: 0.8rem; border-radius: 8px; border: 1px solid #CBD5E1; text-align: center; margin-bottom: 1rem;"><img src="data:image/png;base64,{b64_f9}" style="width: 100%; border-radius: 6px;" /></div>''', unsafe_allow_html=True)
            st.markdown("""
            **Síntese da Validação Cruzada:**
            - **2019:** Pearson $r = 0,705$ | Spearman $\\rho = 0,743$ ($p < 0,001$, $n = 3.685$ pixels).
            - **2023:** Pearson $r = 0,662$ | Spearman $\\rho = 0,748$ ($p < 0,001$, $n = 3.749$ pixels).
            - O gradiente de cores reflete a pureza vegetal do pixel ($\ge 70\%$), confirmando forte aderência biofísica.
            """)
    with tab_sig3:
        st.markdown("### 📊 Tabela de Metadados Geoespaciais do Repositório")
        st.write("Camadas vetoriais e matriciais publicadas no WebSIG. O CRS é lido diretamente de cada arquivo original; no mapa, todas são reprojetadas para Web Mercator.")

        if websig_manifest is None:
            st.info("A tabela é montada a partir de `static/websig/manifest.json`, gerado por `tools/build_websig.py`.")
        else:
            metadata_records = []
            for websig_article in websig_manifest["articles"]:
                for websig_group in websig_article["groups"]:
                    for layer_id in websig_group["layers"]:
                        websig_layer = websig_manifest["layers"][layer_id]
                        layer_meta = websig_layer["meta"]
                        metadata_records.append({
                            "Camada": websig_layer["name"],
                            "Grupo": websig_group["title"],
                            "Arquivo original": layer_meta["file"],
                            "Tipo": layer_meta["type"],
                            "CRS original (lido do arquivo)": layer_meta["crs"],
                            "Resolução original": layer_meta["native_res"],
                            "Fonte primária": layer_meta["source"],
                            "Descrição": layer_meta["description"],
                        })

            df_meta = pd.DataFrame(metadata_records)
            st.dataframe(df_meta, use_container_width=True, hide_index=True)

        st.markdown("""
        <div style="background-color: #FFFFFF; border: 1.5px solid #CBD5E1; border-left: 6px solid #15803D; border-radius: 10px; padding: 1.2rem 1.6rem; margin-top: 1.4rem; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-family: 'Merriweather', serif; font-weight: 800; color: #0F172A; font-size: 1.05rem;">
                    Citação Oficial do Repositório de Dados Geoespaciais
                </span>
                <span style="background-color: #FEF3C7; color: #92400E; border: 1px solid #F59E0B; padding: 0.15rem 0.55rem; border-radius: 4px; font-size: 0.75rem; font-weight: 700;">
                    DADOS ABERTOS (PRE-PUBLICATION)
                </span>
            </div>
            <p style="font-size: 0.85rem; color: #475569; margin-bottom: 0.8rem; line-height: 1.45;">
                Como o manuscrito científico principal encontra-se em fase final de publicação (pós-revisão por pares), 
                utilize a referência bibliográfica e o identificador digital provisório abaixo para citação e reprodutibilidade do conjunto de dados geoespaciais:
            </p>
            <div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; padding: 0.85rem 1.1rem; font-family: 'Courier New', monospace; font-size: 0.82rem; color: #1E293B; line-height: 1.55; word-break: break-word;">
                <b>SALES, J. C. A.; NICOMEDES, N. P.; SILVA, D. C. C.; LOURENÇO, R. W.</b> Dataset: Spatial Modeling of Carbon Flux and Multi-temporal Land Cover Dynamics in the Itupararanga Environmental Protection Area (SP, Brazil). <i>Research Data Repository</i>, 2024. Disponível em: <a href="https://doi.org/10.xxxx/teste-teste-teste" target="_blank" style="color: #15803D; font-weight: bold;">https://doi.org/10.xxxx/teste-teste-teste</a>.
            </div>
            <div style="margin-top: 0.7rem; font-size: 0.78rem; color: #64748B;">
                <b>Identificador Provisório de Teste:</b> <a href="https://doi.org/10.xxxx/teste-teste-teste" target="_blank" style="color: #15803D; font-weight: 600;">https://doi.org/10.xxxx/teste-teste-teste</a> (link temporário para testes de repositório de dados abertos).
            </div>
        </div>
        """, unsafe_allow_html=True)



elif selected_section == "Criações com IA & Produtos":
    st.markdown("""
    <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-left: 6px solid #4F46E5; border-radius: 10px; padding: 1.4rem 1.8rem; margin-bottom: 1.4rem; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
        <h2 style="font-family: 'Merriweather', serif; color: #0F172A; margin: 0 0 0.3rem 0; font-size: 1.7rem;">
            🤖 Criações com Inteligência Artificial & Produtos Tecnológicos
        </h2>
        <p style="font-size: 1rem; color: #334155; margin: 0; line-height: 1.5;">
            Desenvolvimento de agentes conversacionais inteligentes, modelagem preditiva com redes neurais artificiais, algoritmos multicritério com lógica difusa e automação de sensoriamento remoto em nuvem.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_ai1, tab_ai2, tab_ai3, tab_ai4, tab_ai5 = st.tabs([
        "🧠 1. Agentes RAG Científicos",
        "🔮 2. Redes Neurais & MOLUSCE",
        "⚖️ 3. Decisão Difusa & OWA",
        "🛰️ 4. Pipelines GEE & Python",
        "💡 5. Meus Produtos & Projetos"
    ])

    with tab_ai1:
        st.markdown("### 🧠 Agentes Inteligentes & RAG Especializado em Literatura Científica")
        st.write("Sistemas de Recuperação Aumentada por Geração (Retrieval-Augmented Generation) projetados para superar as limitações de LLMs genéricos no meio acadêmico e ambiental:")
        
        c_a1, c_a2 = st.columns([3, 2])
        with c_a1:
            st.markdown("""
            - **Rigor Técnico contra Alucinações:** O agente é ancorado estritamente em papers, teses, relatórios de EIA/RIMA e matrizes de satélite, garantindo que valores numéricos, datas e fórmulas sejam reproduzidos com 100% de precisão.
            - **Interpretação Multiespectral:** Capaz de explicar fórmulas matemáticas de sensoriamento remoto (como `$sPRI \times NDVI$`), correlações estatísticas (Pearson, Spearman) e bandas orbitais (Sentinel-2, MODIS).
            - **Aplicação no Portfólio:** Na seção **Artigos Científicos & Publicações**, cada estudo traz um bloco de perguntas frequentes com respostas redigidas a partir do próprio artigo — os números, fórmulas e conclusões vêm do texto publicado, sem geração automática.
            """)
        with c_a2:
            st.markdown("""
            <div style="background: #F8FAFC; border: 1.5px solid #E2E8F0; border-radius: 8px; padding: 1.1rem;">
                <b style="color: #4F46E5; font-size: 0.92rem;">Stack Tecnológica do Agente:</b>
                <ul style="font-size: 0.85rem; color: #475569; margin-top: 0.4rem; padding-left: 1.2rem; line-height: 1.5;">
                    <li>Python 3.10+ / Streamlit</li>
                    <li>LangChain / LlamaIndex architecture</li>
                    <li>Embeddings vetoriais multilingues</li>
                    <li>API Google Gemini integrada</li>
                    <li>Base de conhecimento pós-revisão por pares</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    with tab_ai2:
        st.markdown("### 🔮 Modelagem Preditiva com Redes Neurais Artificiais (MOLUSCE / ANN-MLP)")
        st.write("Simulação espaço-temporal de mudanças de uso da terra e perdas funcionais de carbono através de inteligência artificial geoespacial:")
        
        st.markdown("""
        - **Arquitetura Neural ANN-MLP:** Treinamento de Redes Neurais Artificiais do tipo Multi-Layer Perceptron com 10.000 amostras aleatórias e 500 épocas de calibração, utilizando variáveis preditoras como declividade, distância de estradas e núcleos urbanos.
        - **Autômatos Celulares e Cadeias de Markov (CA-Markov):** Projeção preditiva probabilística de transição de classes para o horizonte de 2028 na APA de Itupararanga.
        - **Diferencial Competitivo:** Permite que empresas de créditos de carbono e órgãos de fiscalização ambiental antecipem áreas de degradação florestal futura antes que o corte raso ocorra.
        """)

    with tab_ai3:
        st.markdown("### ⚖️ Sistemas de Apoio à Decisão com Lógica Difusa e OWA (Ordered Weighted Averaging)")
        st.write("Algoritmos de inteligência computacional para ponderação de políticas públicas fiscais e ambientais:")
        
        st.markdown("""
        - **Modelagem Multicritério OWA:** Uso de operadores de média ponderada ordenada aplicados ao Índice de Vegetação Nativa (IVEG) para simular diferentes graus de atitude decisória (graus de tolerância ao risco e trade-offs compensatórios).
        - **Aplicação no ICMS Ecológico:** Calibração algorítmica para os 645 municípios de São Paulo, permitindo ao poder público alinhar transferências financeiras à preservação ecossistêmica de alta integridade.
        - **Reconhecimento Internacional:** Metodologia apresentada no *21st Symposium on Systems Analysis in Forest Resources (SSAFR 2026, San Sebastián, Espanha)*.
        """)

    with tab_ai4:
        st.markdown("### 🛰️ Automação de Sensoriamento Remoto em Nuvem (Google Earth Engine & Python)")
        st.write("Pipelines automatizados de processamento massivo de imagens de satélite:")
        
        st.markdown("""
        - **Scripts GEE Especializados:** Rotinas para filtragem automática de nuvens (QA60 Sentinel-2), mosaicos temporais sazonais e harmonização espectral.
        - **Validação Cruzada Multi-Sensor:** Cruzamento em nuvem entre índices de alta resolução espacial (Sentinel-2, 10 m) e dados térmicos/biofísicos globais (MODIS GPP MOD17A2H, 500 m).
        - **Reprodutibilidade Científica:** Código documentado segundo as melhores práticas de Ciência Aberta e princípios FAIR.
        """)

    with tab_ai5:
        st.markdown("### 💡 Meus Produtos, Modelos & Inovações em Construção")
        st.write("Espaço reservado para demonstrar ferramentas sob medida desenvolvidas pelo Dr. Jomil:")

        prod_col1, prod_col2 = st.columns(2)
        with prod_col1:
            st.markdown("""
            <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-left: 5px solid #15803D; border-radius: 8px; padding: 1.1rem; margin-bottom: 1rem; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
                <b style="color: #0F172A; font-size: 1rem;">🌿 Carbon-Insight APA</b>
                <div style="font-size: 0.78rem; color: #15803D; font-weight: 700; margin: 0.2rem 0 0.5rem 0;">Web App de Monitoramento de Carbono em Tempo Quase-Real</div>
                <p style="font-size: 0.85rem; color: #475569; line-height: 1.45; margin: 0;">
                    Aplicação para identificar talhões de floresta sob estresse hídrico e perda de capacidade fotossintética antes do aparecimento de clareiras.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with prod_col2:
            st.markdown("""
            <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-left: 5px solid #0284C7; border-radius: 8px; padding: 1.1rem; margin-bottom: 1rem; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
                <b style="color: #0F172A; font-size: 1rem;">🗺️ Geo-Decision OWA Tool</b>
                <div style="font-size: 0.78rem; color: #0284C7; font-weight: 700; margin: 0.2rem 0 0.5rem 0;">Ferramenta de Alocação de Recursos Fiscais Ambientais</div>
                <p style="font-size: 0.85rem; color: #475569; line-height: 1.45; margin: 0;">
                    Software interativo para simulação de cenários de repasse de ICMS Ambiental com controle de atitude de risco pelo gestor público.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.info("💡 Você pode adicionar ou personalizar novos produtos a qualquer momento editando as seções técnicas do seu aplicativo!")


elif selected_section in ["Consultoria Ambiental & Tutoria em SIG", "Consultoria Ambiental & Aulas", "Soluções Técnicas & Mercado (ESG)"]:
    st.markdown("""
    <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-left: 6px solid #15803D; border-radius: 10px; padding: 1.4rem 1.8rem; margin-bottom: 1.4rem; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
        <h2 style="font-family: 'Merriweather', serif; color: #0F172A; margin: 0 0 0.4rem 0; font-size: 1.7rem;">
            Consultoria Ambiental, Licenciamento & Aulas Especializadas
        </h2>
        <p style="font-size: 1.02rem; color: #334155; margin: 0; line-height: 1.5;">
            Atuação técnico-científica de alto nível em inteligência geoespacial, diagnósticos de impacto, recuperação ecológica e capacitação prática em softwares SIG para profissionais, empresas e acadêmicos.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_serv1, tab_serv2, tab_serv3, tab_serv4, tab_serv5, tab_serv6 = st.tabs([
        "Aulas & Tutoria em SIG",
        "Estudos e Avaliações de Impacto",
        "Licenciamento Ambiental",
        "Restauração Ecológica (PRAD)",
        "Regularização Rural (Código Florestal)",
        "Fiscalização, Multas & TAC"
    ])

    with tab_serv1:
        st.markdown("### Aulas e Tutoria em Geoprocessamento & Sensoriamento Remoto")
        st.write("Mentoria personalizada e treinamentos práticos (do nível básico ao avançado) com estudos de caso reais do mercado ambiental:")
        
        c_a1, c_a2 = st.columns(2)
        with c_a1:
            st.markdown("""
            <div class="service-card">
                <h4 style="color: #15803D; margin-top: 0;">Plataformas & Softwares Dominados:</h4>
                <ul style="font-size: 0.9rem; color: #334155; line-height: 1.6;">
                    <li><b>QGIS:</b> Manipulação vetorial e raster, georreferenciamento, modelagem no MOLUSCE, layout cartográfico profissional para órgãos ambientais.</li>
                    <li><b>ArcGIS Pro / ArcMap:</b> Análise espacial multicritério (AHP), modelagem hidrológica, interpolação geoestatística (Krigagem).</li>
                    <li><b>Google Earth Engine (GEE):</b> Processamento massivo em nuvem de coleções Sentinel-2, Landsat (séries temporais de 30 anos) e MODIS.</li>
                    <li><b>IDRISI / TerrSet:</b> Cadeias de Markov e Autômatos Celulares para projeção de mudanças de uso da terra e vulnerabilidade.</li>
                    <li><b>Programação Aplicada:</b> Scripts em Python (GeoPandas, Shapely, Rasterio) e R (pacotes sf, lidR para processamento de nuvens LiDAR).</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with c_a2:
            st.markdown("""
            <div class="service-card" style="border-left-color: #0284C7;">
                <h4 style="color: #0284C7; margin-top: 0;">Módulos Práticos & Objetivos:</h4>
                <ul style="font-size: 0.9rem; color: #334155; line-height: 1.6;">
                    <li>Elaboração de mapas temáticos padronizados para processos de licenciamento junto à CETESB e IBAMA.</li>
                    <li>Cálculo de Índices Biofísicos: NDVI, sPRI, EVI, NBR (cicatrizes de fogo) e Temperatura da Superfície (LST térmico).</li>
                    <li>Quantificação e modelagem do fluxo e estoque de Carbono para projetos ESG e Mercado Voluntário.</li>
                    <li>Delimitação automatizada de APPs hídricas e de topo de morro segundo a Lei 12.651/2012.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    with tab_serv2:
        st.markdown("### Estudos e Avaliações de Impacto Ambiental (Diagnósticos)")
        st.write("Elaboração, coordenação técnica e perícia em diagnósticos ambientais de todas as complexidades:")
        
        impact_studies = [
            ("AIA (Avaliação de Impacto Ambiental)", "O processo geral e estruturante de identificar, prever e interpretar as consequências que um empreendimento trará aos meios físico, biótico e socioeconômico. É o ponto de partida técnico de qualquer estudo.", "#15803D"),
            ("EIA (Estudo de Impacto Ambiental)", "O estudo técnico e científico mais complexo e aprofundado do mercado. Exigido obrigatoriamente para grandes obras de significativo impacto (hidrelétricas, rodovias, mineradoras, portos), detalhando fauna, flora, dinâmica do solo e impactos sociais.", "#DC2626"),
            ("RIMA (Relatório de Impacto Ambiental)", "O resumo executivo do EIA elaborado em linguagem clara, visual, didática e acessível, com infográficos e mapas, obrigatório para apresentação pública à sociedade e em audiências públicas.", "#D97706"),
            ("EAS (Estudo Ambiental Simplificado)", "Estudo técnico de menor complexidade exigido para empreendimentos cujo potencial de poluição ou degradação ambiental é considerado de baixo ou médio impacto.", "#0284C7"),
            ("RAS (Relatório Ambiental Simplificado)", "Análise rápida e objetiva das condições ambientais da região antes da implantação de empresas de pequeno ou médio porte (ex: loteamentos residenciais compactos, indústrias leves).", "#4F46E5"),
            ("PCA (Plano de Controle Ambiental)", "Documento contratado na fase de instalação de um projeto que detalha todas as medidas e planos executivos da empresa para mitigar, monitorar e controlar os efluentes, resíduos e poluição gerada.", "#059669")
        ]
        
        for name, desc, col in impact_studies:
            st.markdown(f"""
            <div class="service-card" style="border-left-color: {col};">
                <h4 style="color: {col}; margin: 0 0 0.35rem 0; font-family: 'Merriweather', serif;">{name}</h4>
                <p style="font-size: 0.88rem; color: #334155; line-height: 1.5; margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_serv3:
        st.markdown("### Licenciamento Ambiental (Etapas Obrigatórias)")
        st.write("Condução e instrução de processos regulatórios junto aos órgãos de fiscalização (CETESB, IBAMA e secretarias municipais):")
        
        lic_steps = [
            ("LP (Licença Prévia)", "O primeiro selo de aprovação governamental. O consultor a emite para atestar a viabilidade ambiental da localização e da concepção do projeto.", "#15803D"),
            ("LI (Licença de Instalação)", "A licença que autoriza o início físico das obras civis, terraplanagem e montagem da estrutura física do empreendimento, condicionada ao cumprimento das exigências da LP.", "#2563EB"),
            ("LO (Licença de Operação)", "A licença definitiva que autoriza o negócio a iniciar suas atividades produtivas e faturar. O consultor comprova tecnicamente o cumprimento de todas as exigências das etapas anteriores.", "#059669"),
            ("LAS (Licenciamento Ambiental Simplificado)", "Processo unificado e ágil onde as fases de LP, LI e LO são avaliadas e aprovadas em uma única etapa para empreendimentos de baixíssimo potencial poluidor.", "#D97706"),
            ("ASV (Autorização de Supressão de Vegetação)", "Documento legal indispensável emitido pelo órgão ambiental competente autorizando o corte legal e criterioso de exemplares arbóreos nativos para implantação da obra.", "#DC2626")
        ]
        
        for name, desc, col in lic_steps:
            st.markdown(f"""
            <div class="service-card" style="border-left-color: {col};">
                <h4 style="color: {col}; margin: 0 0 0.35rem 0; font-family: 'Merriweather', serif;">{name}</h4>
                <p style="font-size: 0.88rem; color: #334155; line-height: 1.5; margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_serv4:
        st.markdown("### Restauração e Recuperação Ecológica")
        st.write("Projetos técnicos com metodologia científica para recomposição de ecossistemas degradados:")
        
        rest_projects = [
            ("PRAD (Plano de Recuperação de Áreas Degradadas)", "Projeto técnico e executivo onde o consultor define como vai reverter a degradação do solo, conter processos erosivos e restabelecer a vegetação nativa com técnicas de bioengenharia e plantio de mudas pioneiras e secundárias.", "#15803D"),
            ("PRADA (Plano de Recuperação de Áreas Degradadas ou Alteradas)", "Equivalente ao PRAD, porém estruturado sob o regramento e os parâmetros específicos do Código Florestal para regularização exclusiva de imóveis e propriedades rurais.", "#059669"),
            ("PTRF (Projeto de Recomposição da Flora)", "Plano técnico focado no plantio, adensamento, enriquecimento e manejo silvicultural de espécies nativas regionais para restauração de áreas abertas ou sub-bosques.", "#2563EB")
        ]
        
        for name, desc, col in rest_projects:
            st.markdown(f"""
            <div class="service-card" style="border-left-color: {col};">
                <h4 style="color: {col}; margin: 0 0 0.35rem 0; font-family: 'Merriweather', serif;">{name}</h4>
                <p style="font-size: 0.88rem; color: #334155; line-height: 1.5; margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_serv5:
        st.markdown("### Regularização Rural (Código Florestal - Lei Federal nº 12.651/2012)")
        st.write("Adequação ambiental completa de propriedades e empreendimentos do agronegócio:")
        
        rural_reg = [
            ("APP (Área de Preservação Permanente)", "Faixas marginais de cursos d'água, nascentes, topos de morro e encostas com alta declividade protegidas por lei. O consultor atua na delimitação precisa em SIG e no projeto de regeneração.", "#0284C7"),
            ("RL (Reserva Legal)", "Percentual territorial obrigatório de cobertura florestal nativa que cada imóvel rural deve preservar. O consultor calcula a área, demarca no mapa e projeta compensações quando cabível.", "#15803D"),
            ("CAR (Cadastro Ambiental Rural)", "Registro público eletrônico obrigatório para todos os imóveis rurais do Brasil. Elaboração de shapefiles georreferenciados contendo o mosaico da propriedade.", "#D97706"),
            ("PRA (Programa de Regularização Ambiental)", "Termo de compromisso firmado pelo proprietário junto ao órgão ambiental estadual para sanar passivos anteriores de APP e Reserva Legal, implementando os planos desenhados pelo consultor.", "#059669")
        ]
        
        for name, desc, col in rural_reg:
            st.markdown(f"""
            <div class="service-card" style="border-left-color: {col};">
                <h4 style="color: {col}; margin: 0 0 0.35rem 0; font-family: 'Merriweather', serif;">{name}</h4>
                <p style="font-size: 0.88rem; color: #334155; line-height: 1.5; margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_serv6:
        st.markdown("### Fiscalização, Multas e Acordos Legais")
        st.markdown("""
        <div class="service-card" style="border-left-color: #DC2626;">
            <h4 style="color: #DC2626; margin: 0 0 0.35rem 0; font-family: 'Merriweather', serif;">TAC (Termo de Ajustamento de Conduta)</h4>
            <p style="font-size: 0.88rem; color: #334155; line-height: 1.5; margin: 0;">
                Acordo jurídico extrajudicial firmado entre a empresa ou proprietário autuado, o órgão ambiental fiscalizador (CETESB/IBAMA) e o Ministério Público (Gaema/Promotoria de Justiça). 
                O consultor ambiental é acionado para realizar a perícia forense, quantificar o dano real através de imagens históricas de satélite e desenhar as soluções técnicas executivas (cronogramas de recuperação, compensações ambientais) necessárias para suspender multas e evitar ações civis públicas.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Solicitar Proposta Técnica ou Agendar Tutoria")
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        st.write("Precisa de assessoria técnica especializada para o seu empreendimento, estudo de caso ou treinamento em SIG?")
        st.markdown("""
        - **E-mail Institucional:** `jomil.sales@usp.br`
        - **E-mail Profissional:** `jomilc@gmail.com`
        - **Registro Profissional:** Biólogo CRBio nº 68816/01-D
        - **LinkedIn:** [Perfil Profissional](https://www.linkedin.com/in/jomil-costa-phd-53817838/)
        """)
    with col_c2:
        st.link_button("Enviar Mensagem por E-mail", "mailto:jomil.sales@usp.br?subject=Solicitação de Consultoria / Aulas em SIG", use_container_width=True)
        st.link_button("Acessar Perfil no LinkedIn", "https://www.linkedin.com/in/jomil-costa-phd-53817838/", use_container_width=True)



elif selected_section == "Trajetória Profissional & Docência":
    TRAJETORIA_LINHA = [
        ("2005 — 2009", "Bacharelado e Licenciatura em Ciências Biológicas",
         "Pontifícia Universidade Católica (PUC) · formação em Biologia com habilitação para docência", False),
        ("2007 — 2008", "Iniciação Científica (PIBIC/CNPq)",
         "Primeiro contato com pesquisa aplicada em ecologia e ambiente", False),
        ("2009 — 2011", "Professor · Prefeitura Municipal de Sorocaba",
         "Início da atuação docente na rede pública", False),
        ("2010 — 2012", "Consultor Ambiental autônomo",
         "Habilitação FIA / SEMIL-SP · vistorias de passivos, apoio a TAC do Ministério Público e acompanhamento de PRADs", False),
        ("2011 — 2012", "Analista Ambiental · MEDRAL Meio Ambiente",
         "Licenciamento completo (LP, LI, LO), EIA/RIMA, RAP e EIV em linhas de transmissão e empreendimentos imobiliários", False),
        ("2013 — 2015", "Mestrado em Ciências Ambientais · UNESP Sorocaba",
         "Bolsas CNPq e Projeto Novos Talentos (IPT) · geoprocessamento aplicado a bacias hidrográficas", False),
        ("2015 — 2019", "Doutorado em Ciências Ambientais · UNESP",
         "Com período sanduíche em Portugal (programa BE MUNDUS) · análise espacial e indicadores socioambientais", False),
        ("2018 — 2021", "Professor Adjunto I · Universidade de Sorocaba (UNISO)",
         "SIG, Cartografia Básica, Ecologia e Recuperação de Áreas Degradadas nos cursos de Engenharia Ambiental, Agronômica, Biologia e Psicologia", False),
        ("2020 — 2023", "Professor de Ensino Médio",
         "Docência em Biologia e Ciências da Natureza", False),
        ("2023 — 2024", "Pós-doutorado · UNESP — ICTS Sorocaba",
         "Análise temporal do fluxo de carbono e modelo preditivo por índices espectrais na APA de Itupararanga", False),
        ("ago/2023 — jun/2024", "Pesquisador visitante · Freie Universität Berlin",
         "Instituto de Ciências Geográficas — Sensoriamento Remoto e Geoinformática, com o Prof. Dr. Fabian Fassnacht · simulação de florestas virtuais e dados LiDAR em R", False),
        ("2024 — atual", "Pós-doutorado em Ciências Florestais · ESALQ/USP",
         "Bolsista FAPESP no projeto DecisionES-BR (cooperação H2020 Marie Curie) · apoio à decisão para serviços ecossistêmicos sob mudança global", True),
        ("2026 — atual", "MBA em ESG e Negócios Sustentáveis · ESALQ/USP",
         "Formação executiva em ESG, sustentabilidade corporativa e negócios de baixo carbono, conectando a pesquisa ambiental à tomada de decisão empresarial", True),
    ]

    ATUACAO_CARTOES = [
        ("Sensoriamento remoto &amp; satélites", "sensoriamento",
         "Séries Sentinel-2, Landsat e MODIS processadas em nuvem (Google Earth Engine) para detectar mudança de cobertura, estresse hídrico e perda de vigor fotossintético antes que virem desmatamento."),
        ("Geoprocessamento &amp; cartografia", "cartografia",
         "Mapeamento e análise espacial em QGIS e ArcGIS: delimitação de APPs e Reserva Legal, geoestatística, modelagem multicritério (AHP e OWA) e produção cartográfica para órgãos ambientais."),
        ("Licenciamento &amp; perícia ambiental", "licenciamento",
         "EIA/RIMA, RAP, PRAD e laudos de cobertura vegetal; vistorias de passivos ambientais, apoio técnico a Termos de Ajustamento de Conduta e acompanhamento de autos de infração."),
        ("Docência &amp; formação", "docencia",
         "Professor Adjunto na UNISO e tutor na UNESP e na ESALQ/USP em SIG, Cartografia, Ecologia e Recuperação de Áreas Degradadas, além de orientações de iniciação científica, mestrado e doutorado."),
        ("Restauração &amp; serviços ecossistêmicos", "restauracao",
         "Projetos de recomposição florestal e priorização de áreas para restauração, integrando serviços ecossistêmicos à decisão territorial no pós-doutorado DecisionES-BR."),
        ("Carbono florestal &amp; Mata Atlântica", "carbono",
         "Modelagem do potencial de fluxo de CO₂ com índices espectrais e projeção de cenários (MOLUSCE / CA-Markov) aplicados à APA de Itupararanga e a remanescentes de Mata Atlântica."),
    ]

    html_block("""
    <style>
    .traj-hero { position: relative; border-radius: 12px; overflow: hidden; margin-bottom: 1.4rem; min-height: 250px; display: flex; align-items: flex-end; border-left: 6px solid #16A34A; box-shadow: 0 4px 16px rgba(0,0,0,0.10); background-image: linear-gradient(rgba(14,43,23,0.28), rgba(14,43,23,0.86)), url('https://images.unsplash.com/photo-1738625256303-d07f7c459982?auto=format&fit=crop&w=1800&q=80'); background-size: cover; background-position: center 55%; }
    .traj-hero-inner { padding: 1.5rem 1.8rem; }
    .traj-kicker { display: inline-block; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; color: #BBF7D0; border: 1px solid rgba(187,247,208,0.5); border-radius: 4px; padding: 0.18rem 0.55rem; margin-bottom: 0.6rem; }
    .traj-hero h2 { font-family: 'Merriweather', serif; color: #FFFFFF; font-size: 1.85rem; margin: 0 0 0.35rem 0; line-height: 1.2; letter-spacing: -0.01em; }
    .traj-hero p { color: #E2E8F0; font-size: 0.97rem; margin: 0; max-width: 780px; line-height: 1.5; }
    .sec-title { font-family: 'Merriweather', serif; color: #0F172A; font-size: 1.25rem; margin: 1.6rem 0 0.2rem 0; }
    .sec-sub { font-size: 0.9rem; color: #475569; margin: 0 0 0.9rem 0; }
    .tl { position: relative; }
    .tl::before { content: ""; position: absolute; left: 147px; top: 8px; bottom: 8px; width: 2px; background: linear-gradient(180deg, #BBF7D0, #15803D 45%, #BBF7D0); }
    .tl-item { display: grid; grid-template-columns: 132px 32px 1fr; align-items: start; margin-bottom: 0.7rem; }
    .tl-when { font-size: 0.79rem; font-weight: 800; color: #15803D; text-align: right; padding-top: 0.55rem; line-height: 1.25; }
    .tl-mark { position: relative; height: 100%; }
    .tl-mark i { position: absolute; left: 10px; top: 0.6rem; width: 11px; height: 11px; border-radius: 50%; background: #FFFFFF; border: 3px solid #15803D; box-shadow: 0 0 0 3px #ECFDF5; }
    .tl-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 4px solid #15803D; border-radius: 8px; padding: 0.6rem 0.95rem; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
    .tl-card b { font-family: 'Merriweather', serif; font-size: 0.93rem; color: #0F172A; }
    .tl-card span { display: block; font-size: 0.83rem; color: #475569; margin-top: 0.18rem; line-height: 1.45; }
    .tl-item.atual .tl-card { background: #F0FDF4; border-color: #BBF7D0; }
    .tl-item.atual .tl-mark i { background: #15803D; }
    .flip-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(255px, 1fr)); gap: 14px; margin-top: 0.4rem; }
    .flip-card { perspective: 1200px; height: 250px; outline: none; }
    .flip-inner { position: relative; width: 100%; height: 100%; transition: transform 0.7s cubic-bezier(0.4, 0.2, 0.2, 1); transform-style: preserve-3d; }
    .flip-card:hover .flip-inner, .flip-card:focus .flip-inner, .flip-card:focus-within .flip-inner { transform: rotateY(180deg); }
    .flip-front, .flip-back { position: absolute; inset: 0; backface-visibility: hidden; -webkit-backface-visibility: hidden; border-radius: 12px; overflow: hidden; box-shadow: 0 3px 12px rgba(15,23,42,0.10); }
    .flip-front { background: #F7FAF5; display: flex; align-items: flex-end; border: 1px solid #CBD5E1; }
    .flip-front .ilu { position: absolute; inset: 0; }
    .flip-front .ilu svg { width: 100%; height: 100%; display: block; }
    .flip-front .ilu img.arte { width: 100%; height: 100%; object-fit: cover; display: block; }
    .flip-front-hint { position: relative; margin: 0 0 0.75rem auto; margin-right: 0.75rem; font-size: 0.66rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #ECFDF5; background: rgba(14,43,23,0.72); border: 1px solid rgba(187,247,208,0.35); border-radius: 20px; padding: 0.22rem 0.6rem; }
    .flip-front-label { position: relative; width: 100%; padding: 0.85rem 1rem; background: linear-gradient(transparent, rgba(14,43,23,0.88) 55%); color: #FFFFFF; font-family: 'Merriweather', serif; font-weight: 700; font-size: 0.97rem; line-height: 1.3; }
    .flip-front-label em { display: block; font-style: normal; font-family: 'Inter', sans-serif; font-weight: 500; font-size: 0.72rem; color: #BBF7D0; margin-top: 0.25rem; letter-spacing: 0.05em; text-transform: uppercase; }
    .flip-back { transform: rotateY(180deg); background: linear-gradient(155deg, #14532D 0%, #15803D 100%); color: #ECFDF5; padding: 1.15rem 1.25rem; display: flex; flex-direction: column; justify-content: center; border: 1px solid #14532D; }
    .flip-back b { font-family: 'Merriweather', serif; font-size: 0.97rem; color: #FFFFFF; display: block; margin-bottom: 0.5rem; }
    .flip-back p { font-size: 0.85rem; line-height: 1.55; margin: 0; color: #DCFCE7; }
    .credito { font-size: 0.74rem; color: #94A3B8; margin: 0.7rem 0 1.2rem 0; }
    @media (max-width: 640px) {
    .tl::before { display: none; }
    .tl-item { grid-template-columns: 1fr; }
    .tl-mark { display: none; }
    .tl-when { text-align: left; padding: 0 0 0.2rem 0.1rem; }
    .traj-hero h2 { font-size: 1.4rem; }
    }
    </style>
    <div class="traj-hero">
        <div class="traj-hero-inner">
            <span class="traj-kicker">Trajetória</span>
            <h2>Duas décadas entre a floresta, o mapa e a sala de aula</h2>
            <p>Da graduação em Ciências Biológicas ao pós-doutorado em Ciências Florestais na ESALQ/USP, passando pelo licenciamento ambiental, pela docência universitária e pela pesquisa em sensoriamento remoto na Alemanha.</p>
        </div>
    </div>
    """)

    html_block("""
    <h3 class="sec-title">Formação &amp; atuação em linha do tempo</h3>
    <p class="sec-sub">Percurso acadêmico e profissional, do primeiro diploma à pesquisa atual.</p>
    """)

    itens_tl = "".join(
        f'<div class="tl-item{" atual" if atual else ""}">'
        f'<div class="tl-when">{quando}</div>'
        f'<div class="tl-mark"><i></i></div>'
        f'<div class="tl-card"><b>{titulo}</b><span>{detalhe}</span></div>'
        f'</div>'
        for quando, titulo, detalhe, atual in TRAJETORIA_LINHA)
    html_block(f'<div class="tl">{itens_tl}</div>')

    html_block("""
    <h3 class="sec-title">Áreas de atuação profissional</h3>
    <p class="sec-sub">Passe o mouse sobre cada imagem (ou toque, no celular) para ver o que envolve cada frente de trabalho.</p>
    """)

    cartoes = []
    for titulo, base, texto in ATUACAO_CARTOES:
        arte, tem_imagem = get_arte_cartao(base)
        # quando a imagem já traz o título, o rótulo vira só uma dica discreta
        rotulo = ('<div class="flip-front-hint">passe o mouse</div>' if tem_imagem
                  else f'<div class="flip-front-label">{titulo}<em>Passe o mouse</em></div>')
        cartoes.append(
            f'<div class="flip-card" tabindex="0"><div class="flip-inner">'
            f'<div class="flip-front"><div class="ilu">{arte}</div>{rotulo}</div>'
            f'<div class="flip-back"><b>{titulo}</b><p>{texto}</p></div>'
            f'</div></div>')
    cartoes = "".join(cartoes)
    html_block(f'<div class="flip-grid">{cartoes}</div>')
    html_block('<p class="credito">Imagem de capa: banco de imagens livre Unsplash.</p>')

    html_block("""
    <h3 class="sec-title">Detalhamento da experiência</h3>
    <p class="sec-sub">Pós-doutorados, docência no ensino superior e atuação no mercado ambiental.</p>
    """)

    tab_p1, tab_p2, tab_p3 = st.tabs([
        "Pós-Doutorados de Ponta",
        "Docência no Ensino Superior",
        "Consultoria & Licenciamento Ambiental"
    ])

    with tab_p1:
        st.markdown("#### Experiência Internacional e Pós-Doutoramento:")
        for pd_item in traj["postdoc_experience"]:
            st.markdown(f"""
            <div class="clipping-card" style="border-left: 4px solid #15803D;">
                <h4 style="color: #0F172A; margin: 0; font-family: 'Merriweather', serif;">{pd_item['institution']}</h4>
                <p style="font-size: 0.82rem; color: #15803D; font-weight: 700; margin-bottom: 0.4rem;">{pd_item['role']}</p>
                <p style="font-size: 0.85rem; color: #475569; margin-bottom: 0.3rem;"><b>Projeto:</b> {pd_item['project']}</p>
                <p style="font-size: 0.85rem; color: #334155; line-height: 1.45; margin-bottom: 0;">{pd_item['activities']}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_p2:
        st.markdown("#### Atuação Docente e Formação de Pessoas:")
        for t_item in traj["university_teaching"]:
            st.markdown(f"""
            <div class="clipping-card" style="border-left: 4px solid #2563EB;">
                <h4 style="color: #0F172A; margin: 0; font-family: 'Merriweather', serif;">{t_item['institution']}</h4>
                <p style="font-size: 0.82rem; color: #1D4ED8; font-weight: 700; margin-bottom: 0.4rem;">{t_item['role']}</p>
                <p style="font-size: 0.85rem; color: #334155; line-height: 1.45; margin-bottom: 0;">{t_item['scope']}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_p3:
        st.markdown("#### Atuação no Mercado Ambiental & Licenciamento:")
        for c_item in traj["environmental_consulting"]:
            st.markdown(f"""
            <div class="clipping-card" style="border-left: 4px solid #D97706;">
                <h4 style="color: #0F172A; margin: 0; font-family: 'Merriweather', serif;">{c_item['role']} ({c_item['period']})</h4>
                <p style="font-size: 0.85rem; color: #334155; line-height: 1.45; margin-bottom: 0;">{c_item['scope']}</p>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; font-size: 0.78rem; color: #64748B; padding: 0.5rem 0;">
    Dr. Jomil Costa Abreu Sales | Biólogo (CRBio nº 68816/01-D) | Pós-Doutor em Ciências Florestais (ESALQ/USP)<br>
    Portfólio Científico, WebSIG & Consultoria Ambiental © 2026
</div>
""", unsafe_allow_html=True)
