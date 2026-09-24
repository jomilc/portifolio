import json

portfolio = {
    "researcher": {
        "name": "Dr. Jomil Costa Abreu Sales",
        "title": "Biólogo | Pós-Doutor em Ciências Florestais (ESALQ/USP) | Doutor em Ciências Ambientais (UNESP / TU Berlin / FCT Nova Lisboa)",
        "summary": "Especialista em Geotecnologias, Sensoriamento Remoto Térmico e Óptico, Modelagem Espacial de Recursos Naturais, Carbono e Ecologia da Paisagem. Experiência de quase duas décadas unindo rigor científico a soluções práticas de inteligência territorial, gestão de bacias hidrográficas, valoração de serviços ecossistêmicos e capacitação profissional em SIG (QGIS, ArcGIS, GEE, R e Python).",
        "links": {
            "lattes": "http://lattes.cnpq.br/0266681173969604",
            "orcid": "https://orcid.org/0000-0001-8722-8398",
            "scholar": "https://scholar.google.com/citations?user=3ymOKh8AAAAJ&hl=en",
            "researchgate": "https://www.researchgate.net/profile/Jomil-Sales",
            "email": "jomilc@gmail.com"
        },
        "stats": {
            "published_articles": 25,
            "book_chapters": 1,
            "conference_papers": 30,
            "technical_projects": 5,
            "supervised_theses_and_ics": 4
        }
    },
    "featured_article": {
        "id": "10.1.25",
        "title": "The Influence of Land Use and Land Cover on Surface Temperature in a Water Catchment Sub-Basin",
        "journal": "Sociedade & Natureza",
        "year": 2023,
        "volume": "35",
        "pages": "e69161",
        "doi": "10.14393/SN-v35-2023-69161",
        "authors": [
            "Arthur Pereira dos Santos",
            "Henzo Henrique Simionatto",
            "Letícia Tondato Arantes",
            "Vanessa Cezar Simonetti",
            "Renan Angrizani de Oliveira",
            "Jomil Costa Abreu Sales",
            "Darllan Collins da Cunha e Silva"
        ],
        "study_area": {
            "name": "Sub-bacia Hidrográfica do Ribeirão Santa Isabel",
            "municipality": "Paracatu",
            "state": "Minas Gerais (MG)",
            "biome": "Cerrado",
            "basin": "Bacia do Rio Paracatu / Bacia Hidrográfica do Rio São Francisco (UPGRH SF7)",
            "total_area_km2": 1227.6,
            "population_served": "~94.000 habitantes"
        },
        "context_challenge": {
            "problem": "Conflito severo pelo uso da água e risco iminente de colapso no abastecimento público urbano. A sub-bacia do Ribeirão Santa Isabel é o único manancial de captação para a população urbana de Paracatu, mas sofre forte pressão de outorgas para irrigação agrícola intensiva (pivôs centrais para soja, milho e café).",
            "historical_trigger": "Em 2017, a cidade enfrentou a maior crise hídrica em 100 anos, obrigando racionamento severo e intervenção do Ministério Público (MPMG) e IGAM, que declararam a bacia como Área de Conflito (DAC).",
            "public_policy_evaluated": "Criação do Parque Estadual de Paracatu em 2011 (Unidade de Conservação de Proteção Integral - UCI) e zoneamento agroambiental (ZAP) para proteção dos mananciais."
        },
        "geotechnology_stack": [
            {
                "tool": "QGIS 3.2.12",
                "application": "Padronização espacial de resolução (reamostragem para 30m por Vizinho Mais Próximo), cálculo de Radiância Espectral, Temperatura de Brilho (Brightness Temperature), correção de Emissividade e calibração de dispersão atmosférica (fator de correção USGS -0.29 K na banda 10 do Landsat-8)."
            },
            {
                "tool": "ArcGIS 10.5",
                "application": "Processamento vetorial, recorte de máscara da bacia (1:50.000 SEMEA), junção espacial de tabelas de atributos (Join) entre dados térmicos e uso do solo (LULC), estatística zonal e cartografia temática de alta precisão."
            },
            {
                "tool": "Google Earth Engine & MapBiomas (Coleção Nível 6)",
                "application": "Extração automatizada de séries históricas multitemporais de cobertura e uso da terra (LULC) baseada em algoritmos de Machine Learning e imagens Landsat de 30m."
            },
            {
                "tool": "USGS EarthExplorer / Landsat 5 TM & Landsat 8 TIRS",
                "application": "Aquisição de cenas orbitais sem nuvens selecionadas especificamente no período seco (inverno), garantindo estabilidade radiométrica, baixo vapor d'água atmosférico e controle de albedo."
            },
            {
                "tool": "Modelagem Estatística (R / Python)",
                "application": "Análise de variância (ANOVA) e Teste de Tukey (HSD) com nível de significância de 5% (p < 0.05) para validação das diferenças térmicas interanuais e entre classes de paisagem."
            }
        ],
        "data_series": {
            "years": [1990, 2005, 2020],
            "metrics": [
                {
                    "class": "Vegetação Nativa",
                    "area_1990_km2": 796.5,
                    "share_1990_pct": 64.84,
                    "lst_mean_1990_c": 18.58,
                    "area_2005_km2": 810.9,
                    "share_2005_pct": 66.05,
                    "lst_mean_2005_c": 22.29,
                    "area_2020_km2": 819.0,
                    "share_2020_pct": 66.71,
                    "lst_mean_2020_c": 20.93,
                    "net_area_change_km2": 22.5,
                    "net_share_change_pct": 1.87
                },
                {
                    "class": "Agropecuária",
                    "area_1990_km2": 429.3,
                    "share_1990_pct": 34.98,
                    "lst_mean_1990_c": 20.21,
                    "area_2005_km2": 414.9,
                    "share_2005_pct": 33.80,
                    "lst_mean_2005_c": 24.38,
                    "area_2020_km2": 405.9,
                    "share_2020_pct": 33.06,
                    "lst_mean_2020_c": 22.55,
                    "net_area_change_km2": -23.4,
                    "net_share_change_pct": -1.92
                },
                {
                    "class": "Áreas Não-Vegetadas (Solo Exposto)",
                    "area_1990_km2": 0.9,
                    "share_1990_pct": 0.09,
                    "lst_mean_1990_c": 21.72,
                    "area_2005_km2": 0.9,
                    "share_2005_pct": 0.075,
                    "lst_mean_2005_c": 24.22,
                    "area_2020_km2": 1.8,
                    "share_2020_pct": 0.18,
                    "lst_mean_2020_c": 26.53,
                    "net_area_change_km2": 0.9,
                    "net_share_change_pct": 0.09
                },
                {
                    "class": "Recursos Hídricos",
                    "area_1990_km2": 0.9,
                    "share_1990_pct": 0.09,
                    "lst_mean_1990_c": 23.20,
                    "area_2005_km2": 0.9,
                    "share_2005_pct": 0.075,
                    "lst_mean_2005_c": 22.82,
                    "area_2020_km2": 0.9,
                    "share_2020_pct": 0.05,
                    "lst_mean_2020_c": 21.77,
                    "net_area_change_km2": 0.0,
                    "net_share_change_pct": -0.04
                }
            ]
        },
        "scientific_conclusions": [
            "A vegetação nativa atua como um regulador térmico ativo, mantendo a temperatura de superfície entre 1,62 °C e 2,09 °C mais amena que as áreas agrícolas, e até 5,6 °C mais fria que o solo exposto.",
            "O aumento de 22,5 km² de vegetação nativa (+1,87% da bacia) comprova a efetividade prática da criação do Parque Estadual de Paracatu na recuperação e conservação das nascentes.",
            "A redução na temperatura de superfície sobre áreas florestadas reduz o estresse evaporativo da bacia e auxilia na manutenção da vazão de base nos meses críticos de estiagem."
        ]
    },
    "commercial_products": [
        {
            "id": "PROD-01",
            "name": "Diagnóstico Geoespacial de Segurança Hídrica e Gestão de Conflito de Outorgas",
            "category": "Consultoria e Inteligência Territorial",
            "target_audience": "Concessionárias de Saneamento (COPASA, Sabesp), Mineradoras, Comitês de Bacia Hidrográfica (CBHs) e Agroindústrias.",
            "business_problem": "Crises de abastecimento decorrentes da sobre-alocação de outorgas em mananciais compartilhados, gerando disputas jurídicas com Ministérios Públicos, paralisação de atividades econômicas e desabastecimento urbano.",
            "value_proposition": "Identificação precoce de zonas críticas de conflito por meio de modelagem hidrológica integrada a sensoriamento remoto multitemporal (30 anos). Evita multas, litígios com órgãos estaduais (IGAM/DAEE/ANA) e direciona investimentos de contingência.",
            "deliverables": [
                "Relatório Técnico e Pericial de Disponibilidade Hídrica e Conflito de Usos (conforme padrões MPMG e agências estaduais).",
                "Base cartográfica vetorial georreferenciada (Shapefile/GeoPackage) com zoneamento de vulnerabilidade hídrica.",
                "Webmap interativo para monitoramento contínuo das bacias de captação."
            ],
            "technologies": ["QGIS", "ArcGIS Pro", "MapBiomas", "Dados INMET/ANA", "Modelagem Hidrológica"]
        },
        {
            "id": "PROD-02",
            "name": "Monitoramento Termo-Espectral de Microclima & Valoração de Soluções Baseadas na Natureza (NbS)",
            "category": "ESG, Mercado de Carbono & Créditos de Biodiversidade",
            "target_audience": "Fundos de Investimento de Impacto, Empresas de Papel & Celulose, Desenvolvedores de Projetos de Créditos de Carbono e Restauração Ecológica.",
            "business_problem": "Dificuldade em quantificar e comprovar para investidores os benefícios ambientais adicionais (além do carbono em biomassa) de projetos de restauração florestal.",
            "value_proposition": "Comprovação métrica da regulação térmica da paisagem (LST) promovida por plantios florestais e regeneração natural. Demonstra que a restauração reduz a temperatura em até 5°C, protege os estoques de umidade no solo e atenua ondas de calor regionais, valorizando os créditos emitidos com prêmio de 'Co-benefícios Climáticos/Hídricos'.",
            "deliverables": [
                "Dashboard de métricas biofísicas de microclima (LST, Albedo, NDVI, Evapotranspiração).",
                "Auditoria e Certificação Técnica de Eficácia Térmica e Hidrológica de Restauração para relatórios ESG (GRI, TCFD, TNFD).",
                "Série histórica temporal de validação de impacto antes e depois da intervenção florestal."
            ],
            "technologies": ["Landsat 8/9 TIRS", "Sentinel-2", "Google Earth Engine", "Python / R Geoestatística"]
        },
        {
            "id": "PROD-03",
            "name": "Auditoria de Efetividade de Gestão de Áreas Protegidas (UCs, RPPNs e APPs)",
            "category": "Conformidade Regulatória & Perícia Ambiental",
            "target_audience": "Órgãos Gestores Ambientais (ICMBio, IEF, CETESB), Prefeituras Municipais e Escritórios de Advocacia Ambiental.",
            "business_problem": "Necessidade de prestar contas e avaliar juridicamente se a criação de Unidades de Conservação e planos de manejo estão efetivamente estancando o desmatamento e recuperando áreas degradadas.",
            "value_proposition": "Análise forense temporal com imagens de satélite calibradas, atestando com validação estatística formal (Tukey HSD) a evolução do uso da terra e a contenção da fronteira agrícola em zonas de amortecimento.",
            "deliverables": [
                "Laudo Técnico Pericial de Efetividade Territorial com assinatura de Biólogo habilitado (CRBio).",
                "Mapas comparativos de alta resolução com detecção de desmatamento ou regeneração anual.",
                "Matriz de risco de invasão antrópica para suporte à fiscalização em campo."
            ],
            "technologies": ["ArcGIS", "QGIS", "Séries Landsat 1990-2024", "Estatística Paramétrica"]
        }
    ],
    "training_courses": [
        {
            "id": "TRAIN-01",
            "title": "Masterclass: Sensoriamento Remoto Térmico e Balanço de Radiação em SIG (QGIS & ArcGIS)",
            "format": "Curso Teórico-Prático (Online ou In-Company)",
            "workload_hours": 32,
            "target_audience": "Engenheiros Ambientais, Florestais, Agrônomos, Biólogos, Geógrafos, Consultores Ambientais e Pós-Graduandos.",
            "objective": "Capacitar profissionais a processar bandas termais orbitais de forma autônoma, desde a calibração de radiância no topo da atmosfera até a correlação do microclima com dados socioambientais e hídricos.",
            "modules": [
                {
                    "module": "Módulo 1: Fundamentos Físicos & Aquisição de Dados Orbitais",
                    "topics": [
                        "Espectro eletromagnético: infravermelho termal (TIR) vs. óptico.",
                        "Constelações Landsat (TM, ETM+, TIRS) e Sentinel: características e metadados.",
                        "Seleção estratégica de cenas em períodos secos via USGS EarthExplorer."
                    ]
                },
                {
                    "module": "Módulo 2: Calibração Radiométrica e Cálculo de LST no QGIS",
                    "topics": [
                        "Conversão de Números Digitais (DN) em Radiância Espectral (ToA).",
                        "Cálculo de Temperatura de Brilho (Brightness Temperature em Kelvin e Celsius).",
                        "Emissividade da superfície baseada em NDVI e proporção de vegetação (PV).",
                        "Ajustes de espalhamento óptico e uso avançado da Calculadora Raster do QGIS."
                    ]
                },
                {
                    "module": "Módulo 3: Análise Espaço-Temporal e Cruzamento com MapBiomas no ArcGIS",
                    "topics": [
                        "Integração das coleções MapBiomas no ambiente SIG.",
                        "Padronização e reamostragem espacial de resoluções (Nearest Neighbor).",
                        "Zonal Statistics e extração de médias térmicas por tipologia de cobertura.",
                        "Criação de matrizes de transição de uso da terra."
                    ]
                },
                {
                    "module": "Módulo 4: Análise Estatística no R/Python e Layouts Executivos",
                    "topics": [
                        "Comprovação de significância estatística das anomalias térmicas (ANOVA e Teste de Tukey).",
                        "Elaboração de mapas temáticos com padrões cartográficos para relatórios executivos e órgãos de fiscalização.",
                        "Geração de indicadores de suporte à tomada de decisão para clientes e gestores."
                    ]
                }
            ],
            "skills_acquired": [
                "Domínio da calculadora raster no QGIS para equações físicas complexas",
                "Estatística zonal e manipulação de tabelas de atributos no ArcGIS",
                "Processamento de dados térmicos de satélites Landsat 5, 7, 8 e 9",
                "Capacidade de precificar e vender estudos microclimáticos para clientes do setor agro e ambiental"
            ]
        }
    ],
    "memorial_catalog": [
        {"id": 25, "year": 2023, "title": "The influence of land use and land cover on surface temperature in a water catchment sub-basin", "journal": "Sociedade & Natureza", "theme": "Recursos Hídricos & Sensoriamento Térmico", "tools": "QGIS, ArcGIS, MapBiomas, Landsat"},
        {"id": 24, "year": 2022, "title": "Análise espacial da distribuição do ensino em função da renda em uma bacia hidrográfica", "journal": "Nativa", "theme": "Geoestatística & Demografia", "tools": "ArcGIS, Krigagem Ordinária, Kernel"},
        {"id": 23, "year": 2022, "title": "Creation of an environmental sustainability index for water resources applied to watersheds", "journal": "Environment, Development and Sustainability", "theme": "Sustentabilidade Hídrica", "tools": "SIG, Análise Multicritério AHP"},
        {"id": 22, "year": 2022, "title": "Reflexos Ambientais do Desenvolvimento e Expansão das Atividades Humanas sobre a Qualidade da Água", "journal": "Revista Brasileira de Geografia Física", "theme": "Qualidade da Água", "tools": "Geoprocessamento, Análise Espacial"},
        {"id": 21, "year": 2021, "title": "Relação entre a integridade da mata ciliar e a distribuição de renda na Bacia Hidrográfica do Rio Una", "journal": "Scientia Plena", "theme": "Matas Ciliares & Economia", "tools": "ArcGIS, Mapas de Uso do Solo"},
        {"id": 20, "year": 2021, "title": "Developing of an urban environmental quality indicator", "journal": "Geography, Environment, Sustainability", "theme": "Qualidade Ambiental Urbana", "tools": "Lógica Fuzzy Mamdani, NDVI, IAF, Temperatura"},
        {"id": 19, "year": 2021, "title": "Application of geostatistical and deterministic interpolators applied for analysis of the spatial distribution of soil pH", "journal": "Scientia Agraria Paranaensis", "theme": "Geoestatística de Solos", "tools": "Krigagem Ordinária, Inverso da Distância (ISD)"},
        {"id": 18, "year": 2021, "title": "Spatial autocorrelation proposal of the relationship between socioeconomic conditions in Sorocaba", "journal": "Ciência e Natura", "theme": "Estatística Espacial", "tools": "Índice de Moran Global e Local"},
        {"id": 17, "year": 2021, "title": "Application of fuzzy systems to support development of socioenvironmental sustainability index", "journal": "Int. Journal of River Basin Management", "theme": "Modelagem Fuzzy", "tools": "Sistemas Fuzzy, SIG"},
        {"id": 16, "year": 2020, "title": "Análise espacial do custo de reposição de nutrientes do solo em uma bacia hidrográfica", "journal": "RAMA", "theme": "Economia Ambiental & Solos", "tools": "Método Custo de Reposição, Geoprocessamento"},
        {"id": 15, "year": 2019, "title": "Evaluation of flood risk in Sorocaba - Brazil, using fuzzy logic and geotechnology", "journal": "BJD", "theme": "Risco de Inundações", "tools": "Lógica Fuzzy, Modelagem de Terreno"},
        {"id": 14, "year": 2019, "title": "Proposal of methodology for spatial analysis applied to human development index in water basins", "journal": "GeoJournal", "theme": "IDH & Espacialização", "tools": "Krigagem Ordinária, SIG"},
        {"id": 13, "year": 2019, "title": "Valuation methodology of laminar erosion potential using fuzzy inference systems in a Brazilian savanna", "journal": "Env. Monitoring and Assessment", "theme": "Erosão Laminar & Cerrado", "tools": "Inferência Fuzzy Mamdani, SIG"},
        {"id": 12, "year": 2019, "title": "Análise espacial da avifauna e sua correlação com indicadores ambientais na Bacia do Rio Una", "journal": "Boletim de Geografia", "theme": "Biodiversidade & Paisagem", "tools": "Regressão Linear Múltipla, Métricas de Paisagem"},
        {"id": 11, "year": 2018, "title": "Losses on the Atlantic Mata vegetation induced by land use changes", "journal": "Cerne", "theme": "Mata Atlântica & Cenários", "tools": "Land Change Modeler, Sentinel-2, Landsat 5"},
        {"id": 10, "year": 2018, "title": "A importância do profissional habilitado e os riscos associados ao Cadastro Ambiental Rural", "journal": "RGSA", "theme": "CAR & Regularização Ambiental", "tools": "SICAR, Análise de Sobreposições Geográficas"},
        {"id": 9, "year": 2017, "title": "Identificação de áreas com perda de solo acima do tolerável usando NDVI para o cálculo do fator C da USLE", "journal": "Ra'e Ga", "theme": "Erosão & NDVI", "tools": "USLE/RUSLE, Calculadora Raster, NDVI"},
        {"id": 8, "year": 2017, "title": "Identificação de áreas prioritárias para conservação da avifauna na bacia do rio Una", "journal": "RICA", "theme": "Conservação de Habitats", "tools": "Índice de Circularidade, Efeito de Borda, NDVI"},
        {"id": 7, "year": 2016, "title": "Environmental impact assessment caused by timeline changes from land use using Markov chains", "journal": "Ciência e Natura", "theme": "Modelagem Preditiva", "tools": "Cadeias de Markov, Geoprocessamento"},
        {"id": 6, "year": 2016, "title": "Caracterização morfométricas e implicações no acúmulo de sedimentos em reservatórios (Represa Hedberg)", "journal": "Ra'e Ga", "theme": "Batimetria & Sedimentação", "tools": "Modelagem Hidráulica, Geoprocessamento"},
        {"id": 5, "year": 2016, "title": "Uso de indicadores morfométricos como ferramentas para avaliação de bacias hidrográficas", "journal": "RBGF", "theme": "Morfometria de Bacias", "tools": "IMUS, Análise de Relevo, SIG"},
        {"id": 4, "year": 2015, "title": "Use of fuzzy systems in elaboration of an anthropic pressure indicator for forest fragments", "journal": "Environmental Earth Sciences", "theme": "Pressão Antrópica & Fragmentação", "tools": "Sistemas Fuzzy, Índices de Forma"},
        {"id": 3, "year": 2015, "title": "Metodologia para seleção de áreas aptas à instalação de aterros sanitários consorciados utilizando SIG", "journal": "Ciência e Natura", "theme": "Aterros Sanitários & Multicritério", "tools": "Weighted Overlay, SIG Multicritério"},
        {"id": 2, "year": 2014, "title": "Development of methodology for evaluation of remaining forest fragments as management tool", "journal": "Ambiência", "theme": "Planejamento Florestal", "tools": "Ecologia da Paisagem, Geoprocessamento"},
        {"id": 1, "year": 2012, "title": "Estudo Preliminar Comparativo das Espécies de Peixes do Rio Itapetininga e lagoas marginais", "journal": "REB", "theme": "Ictiofauna & Conservação", "tools": "Ecologia de Comunidades Aquáticas"}
    ]
}

with open("/working_dir/c_915f0060088929f4/portfolio_app/portfolio_data.json", "w", encoding="utf-8") as f:
    json.dump(portfolio, f, ensure_ascii=False, indent=2)

print("portfolio_data.json criado com sucesso!")
