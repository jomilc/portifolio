# Pipeline do Agente Autônomo Diário (1 Artigo por Dia)
# Dr. Jomil Costa Abreu Sales

import json
import os

PROMPT_TEMPLATE = """
Você é um analista sênior de inteligência geoespacial e novos negócios.
Converta o seguinte artigo em produto de mercado e módulo de ensino:

Artigo: {title} ({year})
Resumo: {abstract}

Saída desejada:
1. Dor de negócio resolvida (fora da academia)
2. Ferramentas aplicadas (QGIS, ArcGIS, GEE, R, Python)
3. Produtos e entregáveis comerciais (relatórios, shapefiles, webmaps)
4. Módulo de curso prático (ementa, exercícios de SIG, competências)
"""

def ingest_article(article_json_data, data_file="portfolio_data.json"):
    with open(data_file, "r", encoding="utf-8") as f:
        db = json.load(f)
    db.setdefault("processed_articles", []).append(article_json_data)
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    print("Artigo incorporado com sucesso ao banco do dashboard!")

if __name__ == "__main__":
    print("Módulo de automação carregado.")
