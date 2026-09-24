"""
Conteúdo dos artigos científicos exibidos no portfólio.

Cada artigo segue a mesma estrutura do Artigo 1: pergunta central, problema e
hipótese, resultados, solução proposta, galeria de figuras com descrição e um
bloco de perguntas frequentes com respostas escritas a partir do próprio artigo.

As figuras ficam em artigos_midia/<pasta>/ e foram recortadas dos PDFs publicados.
"""

ARTIGOS = [
    # =====================================================================
    {
        "id": 1,
        "rotulo": "Artigo 1",
        "titulo": "Carbon Flux Potential Prediction Model Based on Land Cover and Land Use: "
                  "Application in the Itupararanga Environmental Protection Area, SP, Brazil",
        "tema": "Fluxo de CO₂ & Sentinel-2",
        "veiculo": "SSRN — preprint em fase final de publicação",
        "ano": "2024",
        "status": "destaque",
        "status_label": "Destaque · Preprint pós-revisão",
        "autores": "Jomil Costa Abreu Sales (autor correspondente, ESALQ/USP); Nícholas de Paula Nicomedes (UNESP); "
                   "Darllan Collins da Cunha e Silva (UNESP); Roberto Wagner Lourenço (UNESP)",
        "meu_papel": "Primeiro autor e autor correspondente",
        "financiamento": "FAPESP (Processo 2024/14444-2) e CAPES (Código 001)",
        "link_label": "Acessar o preprint no SSRN (ID 7268395)",
        "link_url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7268395",
        "referencia": "SALES, J. C. A.; NICOMEDES, N. P.; SILVA, D. C. C.; LOURENÇO, R. W. Carbon Flux Potential "
                      "Prediction Model Based on Land Cover and Land Use: Application in the Itupararanga "
                      "Environmental Protection Area, SP, Brazil. SSRN, 2024 (preprint).",
        "figuras_origem": "Figuras do próprio manuscrito, de autoria dos autores.",
        "pasta": "artigos_midia/artigo_01_preprint",
        "pergunta": "A estabilidade cartográfica da cobertura florestal em Unidades de Conservação de Uso "
                    "Sustentável garante, por si só, a manutenção da integridade funcional e da capacidade de "
                    "sequestro de carbono desses remanescentes frente às pressões antrópicas e ao efeito de borda?",
        "pergunta_nota": "A investigação questiona o dogma de que florestas que não foram derrubadas continuam "
                         "desempenhando seus serviços ecossistêmicos climáticos em sua plenitude funcional.",
        "problema": "Os órgãos ambientais e comitês de bacia monitoram o território apenas por métricas binárias "
                    "(desmatamento vs. persistência). Se a árvore não foi cortada, o mapa considera a área intacta — "
                    "mascarando a degradação metabólica silenciosa provocada por dessecação e efeito de borda.",
        "hipotese": "Remanescentes contínuos da APA sofrem degradação funcional invisível ao satélite óptico "
                    "tradicional, e a combinação espectral entre eficiência fotoquímica (sPRI) e biomassa foliar "
                    "(NDVI) a 10 m permite espacializar precocemente o declínio de CO₂ antes de qualquer corte raso.",
        "resultados": [
            "**Desacoplamento estrutura × função:** a cobertura da terra manteve **91,8% de persistência global** e a "
            "floresta nativa, **96,0% de estabilidade física** entre 2019 e 2023.",
            "**Retração do alto potencial:** as áreas de Alto Potencial de sequestro recuaram **-21,5%** "
            "(de 200,83 km² para 157,72 km² — perda líquida de 43,11 km²).",
            "**O achado central (95,7%):** 95,7% (65,66 km²) de toda a perda funcional ocorreu **dentro de matas que "
            "não sofreram desmatamento**.",
            "**Efeito de borda:** queda funcional de **46,4% até 20 m da borda**, contra **35,0% além de 200 m** do interior.",
            "**Validação orbital:** forte aderência ao MODIS GPP (500 m) — Pearson r = 0,705 (2019) e 0,662 (2023); "
            "Spearman ρ = 0,743 e 0,748; p < 0,001.",
        ],
        "solucao": [
            "**Modernização do monitoramento:** substituir o acompanhamento binário por sensoriamento funcional "
            "contínuo a 10 m (Sentinel-2) no Plano de Manejo da APA, com alertas precoces de perda de vigor.",
            "**Ações em borda e conectividade:** faixas de amortecimento de 50 m no entorno dos fragmentos mais "
            "vulneráveis nas zonas ZCRH e ZOR, com reflorestamento de borda.",
            "**Valoração ESG funcional:** condicionar ICMS Ecológico e certificação de créditos de carbono à "
            "integridade funcional medida por satélite, e não apenas à existência estática de árvores em pé.",
        ],
        "figuras": [
            {
                "arquivo": "Image_abstract_REV.png",
                "titulo": "Resumo gráfico do estudo",
                "descricao": "Painel-síntese do manuscrito, dividido em três blocos. À esquerda, a cadeia de "
                             "processamento: cenas Sentinel-2 L2A de inverno (2019 e 2023) a 10 m, o cálculo do NDVI "
                             "e do sPRI e a composição do índice de fluxo de CO₂ (sPRI × NDVI), com a comparação "
                             "cruzada com o GPP do MODIS. Ao centro, o achado principal, contrastando a persistência "
                             "da cobertura com a retração de 21,5% do alto potencial entre 2019 e 2023. À direita, a "
                             "projeção para 2028 pelo MOLUSCE/CA-Markov e a tabela de correlações (Pearson e "
                             "Spearman) que sustenta a validação.",
                "meta": {"Tipo": "Infográfico de síntese", "Sensor": "Sentinel-2 L2A e MODIS MOD17A2H",
                         "Resolução": "10 m e 500 m", "Datum": "SIRGAS 2000 / UTM 23S"},
            },
            {
                "arquivo": "Figure_01.png",
                "titulo": "Área de estudo e zoneamento da APA",
                "descricao": "Mapa de localização da APA de Itupararanga (938,31 km²) sobre imagem de satélite, com "
                             "o limite oficial em traço preto e as cinco zonas do Plano de Manejo em cores: "
                             "Conservação da Biodiversidade (ZCB), Conservação dos Recursos Hídricos (ZCRH), "
                             "Ocupação Rural (ZOR), Ocupação Diversificada (ZOD) e Ocupação Consolidada (ZOC). "
                             "Os mapas-índice situam a unidade no Estado de São Paulo e mostram os municípios "
                             "abrangidos. A ZCRH acompanha a represa e seus afluentes; a ZCB concentra-se ao sul.",
                "meta": {"Tipo": "Mapa temático de zoneamento", "Sensor": "Bases vetoriais do Plano de Manejo",
                         "Resolução": "Vetorial", "Datum": "SIRGAS 2000 / UTM 23S"},
            },
            {
                "arquivo": "Figure_02.png",
                "titulo": "Cobertura da terra em 2019 e 2023",
                "descricao": "Dois painéis lado a lado com a cobertura e uso da terra da APA em 2019 (A) e 2023 (B), "
                             "em seis classes: corpos d'água, floresta nativa, silvicultura, área urbana, agricultura "
                             "e formação campestre. A semelhança visual entre os dois painéis é o ponto da figura: é "
                             "ela que sustenta os 91,8% de persistência da cobertura e os 96,0% de estabilidade da "
                             "floresta — a leitura convencional que o estudo se propõe a questionar.",
                "meta": {"Tipo": "Mapa de uso e cobertura da terra", "Sensor": "MapBiomas 10 m (Sentinel-2)",
                         "Resolução": "10 m", "Datum": "SIRGAS 2000 / UTM 23S"},
            },
            {
                "arquivo": "Figure_03.png",
                "titulo": "Projeção da cobertura da terra para 2028",
                "descricao": "Cenário de cobertura da terra projetado para 2028 pelo plugin MOLUSCE (QGIS), "
                             "combinando rede neural artificial (ANN-MLP, 10.000 amostras e 500 iterações) com "
                             "autômatos celulares e cadeias de Markov. O mapa mantém as mesmas seis classes dos anos "
                             "observados, permitindo comparação direta, e indica continuidade da expansão agrícola e "
                             "urbana sobre as zonas de transição ao norte e a leste da APA.",
                "meta": {"Tipo": "Cenário preditivo", "Sensor": "Modelagem MOLUSCE (ANN-MLP + CA-Markov)",
                         "Resolução": "10 m", "Datum": "SIRGAS 2000 / UTM 23S"},
            },
            {
                "arquivo": "Figure_04s.png",
                "titulo": "Balanço de áreas por classe (2019, 2023 e 2028)",
                "descricao": "Gráfico de barras agrupadas com a área, em km², de cada classe de cobertura nos três "
                             "anos. A floresta nativa aparece praticamente estável (406,25 → 395,50 → 396,59 km²), "
                             "enquanto a área urbana cresce de 40,91 para 48,97 km² entre 2019 e 2023 e a agricultura "
                             "avança de 327,60 para 334,30 km². É a quantificação que isola a variável 'supressão "
                             "vegetal' e mostra que a conversão física de floresta foi pequena no período.",
                "meta": {"Tipo": "Gráfico estatístico", "Sensor": "Tabulação cruzada das classes",
                         "Resolução": "km² por classe", "Datum": "—"},
            },
            {
                "arquivo": "Figure_05.png",
                "titulo": "Classes de potencial de fluxo de CO₂ (2019 vs. 2023)",
                "descricao": "Mapas do proxy sPRI × NDVI estratificado em cinco classes — antrópica, baixo, moderado, "
                             "alto e muito alto potencial — para 2019 (A) e 2023 (B). Diferentemente da figura de "
                             "cobertura da terra, aqui a mudança é visível: as manchas verde-escuras de alto "
                             "potencial encolhem e se fragmentam, e a classe moderada (verde-claro) domina a paisagem "
                             "em 2023. É a principal evidência empírica do estudo.",
                "meta": {"Tipo": "Mapa biofísico de carbono", "Sensor": "Sentinel-2 L2A (B02, B03, B04, B08)",
                         "Resolução": "10 m", "Datum": "SIRGAS 2000 / UTM 23S"},
            },
            {
                "arquivo": "Figure_06.png",
                "titulo": "Projeção do potencial de CO₂ para 2028",
                "descricao": "Aplicação da modelagem markoviana diretamente sobre as classes biofísicas de carbono, "
                             "projetando o cenário de 2028. O alto potencial recua para 145,21 km² e as classes "
                             "moderada e baixa se expandem proporcionalmente, indicando que, sem intervenção de "
                             "restauração e contenção do efeito de borda, o declínio funcional continua avançando "
                             "pelo interior dos maciços florestais.",
                "meta": {"Tipo": "Cenário preditivo biofísico", "Sensor": "Modelagem CA-Markov",
                         "Resolução": "10 m", "Datum": "SIRGAS 2000 / UTM 23S"},
            },
            {
                "arquivo": "Figure_07.png",
                "titulo": "Distribuição das classes de carbono (km²)",
                "descricao": "Gráfico de barras com a área de cada classe de potencial de fluxo de CO₂ nos três anos. "
                             "A leitura direta mostra o alto potencial caindo de 200,83 km² (2019) para 157,72 km² "
                             "(2023) e 145,21 km² (2028), enquanto a classe moderada sobe de 437,03 para 501,98 e "
                             "524,50 km². O muito alto potencial, mais raro, reduz-se de 3,14 para 1,49 km².",
                "meta": {"Tipo": "Gráfico de transição funcional", "Sensor": "Estatística espacial cruzada",
                         "Resolução": "km² por classe", "Datum": "—"},
            },
            {
                "arquivo": "Figure_08.png",
                "titulo": "Produtividade primária bruta (MODIS GPP)",
                "descricao": "Mapas do produto MOD17A2H (NASA) de produtividade primária bruta acumulada no inverno "
                             "austral, a 500 m de resolução, para 2019 (A) e 2023 (B), processados no Google Earth "
                             "Engine. Os valores variam de 0,017 a 0,061 kg C m⁻² por estação. Por ser uma medida "
                             "biofísica independente e consagrada, serve de referência externa para testar se a "
                             "retração espectral captada pelo Sentinel-2 corresponde a uma queda real de fotossíntese.",
                "meta": {"Tipo": "Mapa de produtividade vegetal", "Sensor": "MODIS Terra/Aqua (MOD17A2H)",
                         "Resolução": "500 m", "Datum": "SIRGAS 2000 / UTM 23S"},
            },
            {
                "arquivo": "Figure_09.png",
                "titulo": "Validação cruzada e regressão estatística",
                "descricao": "Gráficos de dispersão entre o proxy de fluxo de CO₂ (eixo Y) e o GPP do MODIS (eixo X) "
                             "para 2019 (A) e 2023 (B), com reta de ajuste linear. A cor dos pontos indica a pureza "
                             "vegetal do pixel (≥ 70%). As correlações são fortes e significativas: Pearson r = 0,705 "
                             "com n = 3.685 pixels em 2019 e r = 0,662 com n = 3.749 em 2023, ambos com p < 0,001.",
                "meta": {"Tipo": "Gráfico de correlação", "Sensor": "Sentinel-2 (10 m) × MODIS GPP (500 m)",
                         "Resolução": "Pixels agregados", "Datum": "—"},
            },
        ],
        "perguntas": [
            {
                "pergunta": "Qual é a principal descoberta do estudo?",
                "resposta": "O desacoplamento entre estrutura e função da floresta. Entre 2019 e 2023 a cobertura "
                            "florestal permaneceu 96,0% estável no mapa, mas as áreas de alto potencial de sequestro "
                            "de CO₂ recuaram 21,5% (de 200,83 km² para 157,72 km²). O ponto crítico é que 95,7% dessa "
                            "perda (65,66 km²) ocorreu dentro de áreas que continuaram classificadas como floresta — "
                            "ou seja, uma degradação invisível ao monitoramento tradicional de desmatamento.",
            },
            {
                "pergunta": "Como o fluxo de CO₂ foi calculado a partir do Sentinel-2?",
                "resposta": "O proxy é o produto sPRI × NDVI. O NDVI = (B08 − B04)/(B08 + B04) mede o vigor e a "
                            "biomassa foliar ativa. O PRI adaptado ao Sentinel-2 usa (B02 − B03)/(B02 + B03) e o sPRI "
                            "é seu escalonamento positivo, (PRI + 1)/2, que expressa a eficiência fotoquímica do uso "
                            "da luz. A multiplicação modula a biomassa verde pela eficiência com que a planta "
                            "efetivamente usa a radiação, aproximando-se da capacidade real de absorção de carbono.",
            },
            {
                "pergunta": "Como o resultado foi validado?",
                "resposta": "Por comparação com uma fonte independente: o produto de produtividade primária bruta "
                            "(GPP) do sensor MODIS (MOD17A2H, 500 m), processado no Google Earth Engine para a estação "
                            "seca. A comparação usou apenas pixels com pureza vegetal ≥ 70%. Os coeficientes foram "
                            "Pearson r = 0,705 (n = 3.685) em 2019 e r = 0,662 (n = 3.749) em 2023, com Spearman ρ de "
                            "0,743 e 0,748 — todos significativos a p < 0,001.",
            },
            {
                "pergunta": "Como funciona a projeção para 2028?",
                "resposta": "A simulação usou o plugin MOLUSCE, no QGIS, combinando uma rede neural artificial do tipo "
                            "Multi-Layer Perceptron (10.000 amostras e 500 iterações) com autômatos celulares e cadeias "
                            "de Markov. O modelo aprende as transições observadas entre 2019 e 2023 em função de "
                            "variáveis como declividade e distância de estradas e núcleos urbanos, e projeta o cenário "
                            "de 2028: o alto potencial de fixação cai para 145,21 km².",
            },
            {
                "pergunta": "O que o efeito de borda tem a ver com isso?",
                "resposta": "A perda funcional não é homogênea dentro do fragmento: a queda foi de 46,4% na faixa de "
                            "até 20 m da borda florestal, contra 35,0% além de 200 m, no interior. Isso indica "
                            "dessecação e estresse fisiológico avançando de fora para dentro — exatamente o processo "
                            "que o monitoramento por corte raso não enxerga.",
            },
            {
                "pergunta": "Quais são as recomendações práticas para a gestão da APA?",
                "resposta": "Três frentes: (1) incluir no Plano de Manejo o monitoramento funcional contínuo a 10 m, "
                            "com alertas de perda de vigor, em vez de acompanhar apenas desmatamento; (2) delimitar "
                            "faixas de amortecimento de 50 m e promover reflorestamento de borda nos fragmentos mais "
                            "vulneráveis das zonas ZCRH e ZOR; e (3) condicionar repasses de ICMS Ecológico e a "
                            "certificação de créditos de carbono à integridade funcional medida por satélite.",
            },
        ],
    },
    # =====================================================================
    {
        "id": 2,
        "rotulo": "Artigo 2",
        "titulo": "Evaluation of the Native Vegetation Index (IVEG) Using Ordered Weighted Averaging (OWA) "
                  "for Environmental Fiscal Policy in São Paulo",
        "tema": "Política fiscal ambiental & decisão multicritério",
        "veiculo": "SSAFR 2026 (San Sebastián) — em submissão",
        "ano": "2025/2026",
        "status": "submissao",
        "status_label": "Em submissão",
        "autores": "Jomil Costa Abreu Sales e colaboradores (ESALQ/USP)",
        "meu_papel": "Primeiro autor",
        "financiamento": "FAPESP — Pós-doutorado (ESALQ/USP)",
        "link_label": "",
        "link_url": "",
        "referencia": "SALES, J. C. A. et al. Evaluation of the Native Vegetation Index (IVEG) using Ordered "
                      "Weighted Averaging for environmental fiscal policy in São Paulo. 21st Symposium on Systems "
                      "Analysis in Forest Resources (SSAFR 2026), San Sebastián, Espanha. Em submissão.",
        "figuras_origem": "",
        "pasta": "artigos_midia/artigo_02_iveg_owa",
        "pergunta": "Como diferentes atitudes de decisão diante do risco alteram a distribuição do ICMS Ecológico "
                    "entre os municípios paulistas quando o Índice de Vegetação Nativa (IVEG) é combinado por "
                    "operadores de média ponderada ordenada (OWA)?",
        "pergunta_nota": "O estudo trata o repasse fiscal ambiental como um problema de decisão multicritério, e não "
                         "como uma fórmula fixa.",
        "problema": "O ICMS Ecológico distribui recursos entre os 645 municípios de São Paulo a partir de índices "
                    "ambientais, entre eles o IVEG. A forma de combinar esses critérios embute, de maneira implícita, "
                    "uma postura do gestor diante do risco e da compensação entre critérios — mas essa escolha "
                    "raramente é explicitada ou testada.",
        "hipotese": "Operadores OWA permitem representar explicitamente o grau de compensação e de aversão ao risco "
                    "na composição do índice, mostrando como cada postura decisória redistribui os repasses e quais "
                    "municípios são sensíveis a essa escolha.",
        "resultados": [
            "Trabalho em fase de submissão: os resultados serão publicados aqui assim que o artigo for aceito.",
        ],
        "solucao": [
            "Metodologia apresentada no *21st Symposium on Systems Analysis in Forest Resources* (SSAFR 2026, "
            "San Sebastián, Espanha).",
        ],
        "figuras": [],
        "figuras_pendentes": "As figuras deste artigo ainda não foram publicadas. Assim que estiverem disponíveis, "
                             "basta salvá-las em <code>artigos_midia/artigo_02_iveg_owa/</code> para que apareçam aqui.",
        "perguntas": [
            {
                "pergunta": "O que é o IVEG?",
                "resposta": "O Índice de Vegetação Nativa é um dos componentes ambientais usados pelo Estado de São "
                            "Paulo na repartição do ICMS Ambiental entre municípios, ao lado de índices como o de "
                            "áreas protegidas, o de reservatórios de água e o de resíduos sólidos.",
            },
            {
                "pergunta": "O que o OWA acrescenta à análise?",
                "resposta": "Os operadores de média ponderada ordenada (Ordered Weighted Averaging) permitem variar, "
                            "de forma controlada, o grau de compensação entre critérios e a atitude do decisor diante "
                            "do risco. Na prática, tornam explícito o que costuma ficar implícito na fórmula de "
                            "rateio e permitem simular cenários de repasse.",
            },
            {
                "pergunta": "Qual é o estágio do trabalho?",
                "resposta": "Em submissão, com apresentação no 21st Symposium on Systems Analysis in Forest Resources "
                            "(SSAFR 2026), em San Sebastián, na Espanha. Os resultados e as figuras serão publicados "
                            "nesta página após a aceitação.",
            },
        ],
    },
    # =====================================================================
    {
        "id": 3,
        "rotulo": "Artigo 3",
        "titulo": "The Influence of Land Use and Land Cover on Surface Temperature in a Water Catchment Sub-Basin",
        "tema": "Temperatura de superfície & segurança hídrica",
        "veiculo": "Sociedade & Natureza, v. 35, e69161",
        "ano": "2023",
        "status": "publicado",
        "status_label": "Publicado · 2023",
        "autores": "Arthur Pereira dos Santos; Henzo Henrique Simionatto; Letícia Tondato Arantes; "
                   "Vanessa Cezar Simonetti; Renan Angrizani de Oliveira; Jomil Costa Abreu Sales; "
                   "Darllan Collins da Cunha e Silva",
        "meu_papel": "Coautor — administração do projeto, recursos, supervisão e revisão formal",
        "financiamento": "",
        "link_label": "Acessar o artigo (DOI 10.14393/SN-v35-2023-69161)",
        "link_url": "https://doi.org/10.14393/SN-v35-2023-69161",
        "referencia": "SANTOS, A. P.; SIMIONATTO, H. H.; ARANTES, L. T.; SIMONETTI, V. C.; OLIVEIRA, R. A.; "
                      "SALES, J. C. A.; SILVA, D. C. C. The Influence of Land Use and Land Cover on Surface "
                      "Temperature in a Water Catchment Sub-Basin. Sociedade & Natureza, v. 35, e69161, 2023.",
        "figuras_origem": "Figuras reproduzidas do artigo publicado em acesso aberto sob licença CC BY 4.0.",
        "pasta": "artigos_midia/artigo_03_lst_cerrado",
        "pergunta": "Como as mudanças no uso e na cobertura da terra alteraram a temperatura de superfície da "
                    "sub-bacia do Ribeirão Santa Isabel, em Paracatu (MG), entre 1990 e 2020 — e o que isso significa "
                    "para o único manancial de captação do município?",
        "pergunta_nota": "A área foi escolhida justamente por concentrar conflitos de uso da água e por ser a única "
                         "fonte de captação de Paracatu.",
        "problema": "A gestão de mananciais costuma ser discutida em termos de vazão e outorga, sem considerar o "
                    "efeito térmico do uso da terra. Em regiões de Cerrado sob pressão agrícola, o aquecimento da "
                    "superfície aumenta a evapotranspiração e a perda de água justamente onde ela é mais crítica.",
        "hipotese": "A temperatura de superfície responde de forma mensurável à classe de uso e cobertura: áreas "
                    "vegetadas mantêm temperaturas sistematicamente mais baixas do que áreas agrícolas e de solo "
                    "exposto, e essa diferença pode ser quantificada com série histórica Landsat.",
        "resultados": [
            "**Vegetação mais fria em toda a série:** a LST média da vegetação ficou abaixo da agricultura nos três "
            "anos — 18,58 °C contra 20,21 °C (1990), 22,29 contra 24,38 °C (2005) e 20,93 contra 22,55 °C (2020), "
            "uma diferença de **1,62 °C a 2,09 °C**.",
            "**Conservação com efeito:** a vegetação passou de 796,5 km² (64,8%) para 819,0 km² (66,7%) da sub-bacia, "
            "enquanto a agricultura recuou de 429,3 km² para 405,9 km² em 30 anos.",
            "**Solo exposto aquece:** a classe de área não vegetada apresentou aumento médio de LST próximo de "
            "**5 °C** no período, e também ampliou sua área.",
            "**Água amortece:** a classe de recursos hídricos apresentou redução de cerca de 1,5 °C, com as variações "
            "mais suaves entre todas as classes.",
            "**Diferença estatisticamente testada:** as médias entre as classes de vegetação e agricultura foram "
            "comparadas pelo teste de Tukey a 5% de significância.",
        ],
        "solucao": [
            "**Manter e ampliar a cobertura vegetal na área de captação:** o ganho de 22,5 km² de vegetação em 30 anos "
            "acompanhou a estabilização térmica da sub-bacia.",
            "**Tratar solo exposto como prioridade:** é a classe com maior aquecimento (~5 °C) e a que mais amplifica "
            "a perda de água por evaporação.",
            "**Usar a LST como indicador de apoio à outorga:** a série Landsat permite acompanhar, sem custo de campo, "
            "o efeito térmico das mudanças de uso sobre o manancial.",
        ],
        "figuras": [
            {
                "arquivo": "figura_01.png",
                "titulo": "Área de estudo",
                "descricao": "Localização da sub-bacia do Ribeirão Santa Isabel, em Paracatu (MG), sobre imagem de "
                             "satélite. O limite da sub-bacia aparece em laranja, a rede de drenagem em azul e os "
                             "pontos verdes marcam o Parque Estadual de Paracatu. O mapa-índice à esquerda situa a "
                             "área no Brasil e em Minas Gerais. A sub-bacia soma 1.227,6 km² e é o único ponto de "
                             "captação de água do município.",
                "meta": {"Tipo": "Mapa de localização", "Sensor": "Imagem orbital de alta resolução",
                         "Resolução": "—", "Datum": "SIRGAS 2000 / UTM 23S"},
            },
            {
                "arquivo": "figura_02.png",
                "titulo": "Variação espaço-temporal da temperatura de superfície",
                "descricao": "Três painéis com a temperatura de superfície (LST) da sub-bacia em 1990, 2005 e 2020, "
                             "na mesma escala de cores (11 °C em azul a 31 °C em vermelho), o que permite comparação "
                             "direta entre os anos. O painel de 1990 é predominantemente frio; 2005 concentra as "
                             "manchas mais quentes, sobretudo no setor sul; e 2020 apresenta padrão intermediário. "
                             "Os fundos de vale e as áreas vegetadas permanecem mais frios em todos os anos.",
                "meta": {"Tipo": "Mapa térmico multitemporal", "Sensor": "Landsat-5 TM e Landsat-8 TIRS",
                         "Resolução": "30 m", "Datum": "SIRGAS 2000 / UTM 23S"},
            },
            {
                "arquivo": "figura_03.png",
                "titulo": "Uso e cobertura da terra (1990, 2005 e 2020)",
                "descricao": "Mapas de uso e cobertura da terra para os mesmos três anos, a partir da coleção "
                             "MapBiomas (Nível 6). As classes incluem formação florestal, formação savânica, formação "
                             "campestre, pastagem, mosaico de agricultura e pastagem, soja, café, outras lavouras "
                             "temporárias, silvicultura, áreas não vegetadas e corpos d'água. Comparados com a figura "
                             "anterior, os mapas mostram a correspondência espacial entre as manchas agrícolas e as "
                             "áreas termicamente mais quentes.",
                "meta": {"Tipo": "Mapa de uso e cobertura", "Sensor": "MapBiomas (série Landsat)",
                         "Resolução": "30 m", "Datum": "SIRGAS 2000 / UTM 23S"},
            },
            {
                "arquivo": "figura_04.png",
                "titulo": "Variação da LST média por classe",
                "descricao": "Gráfico de linhas comparando a temperatura média de cada classe temática entre 1990 e "
                             "2020: área não vegetada, malha urbana, vegetação e recursos hídricos. A leitura "
                             "principal é a inclinação das curvas — a classe de área não vegetada é a que mais "
                             "aquece no período, enquanto a vegetação se mantém na faixa mais baixa do gráfico.",
                "meta": {"Tipo": "Gráfico de séries", "Sensor": "Estatística zonal LST × classes",
                         "Resolução": "°C por classe", "Datum": "—"},
            },
            {
                "arquivo": "figura_05.png",
                "titulo": "Box plot das classes vegetação e agricultura",
                "descricao": "Distribuição dos valores de LST nas classes de vegetação e agricultura no primeiro e no "
                             "último ano da série (1990 e 2020), com a média destacada em azul. Os quatro grupos "
                             "mostram que a agricultura tem mediana e dispersão superiores às da vegetação nos dois "
                             "momentos, sustentando a diferença detectada pelo teste de Tukey a 5%.",
                "meta": {"Tipo": "Gráfico de distribuição", "Sensor": "Amostragem de pixels por classe",
                         "Resolução": "°C", "Datum": "—"},
            },
        ],
        "perguntas": [
            {
                "pergunta": "Qual foi a diferença de temperatura entre vegetação e agricultura?",
                "resposta": "A vegetação foi sistematicamente mais fria: 18,58 °C contra 20,21 °C em 1990, 22,29 °C "
                            "contra 24,38 °C em 2005 e 20,93 °C contra 22,55 °C em 2020. A diferença média ficou "
                            "entre 1,62 °C e 2,09 °C, dependendo do ano.",
            },
            {
                "pergunta": "Quais dados e sensores foram usados?",
                "resposta": "A temperatura de superfície foi calculada a partir das bandas termais do Landsat-5 TM e "
                            "do Landsat-8 TIRS/OLI para 1990, 2005 e 2020. O uso e a cobertura da terra vieram da "
                            "coleção MapBiomas (Nível 6, base Landsat, 30 m), e o cruzamento entre LST e classes foi "
                            "feito em ambiente SIG, com teste de Tukey a 5% de significância.",
            },
            {
                "pergunta": "Por que essa sub-bacia foi escolhida?",
                "resposta": "Porque o Ribeirão Santa Isabel é o único manancial de captação de Paracatu (MG) e "
                            "concentra conflitos de uso da água ligados à intensidade da atividade agrícola na "
                            "região — o município já precisou alterar o ponto de captação por causa dessa pressão.",
            },
            {
                "pergunta": "O resultado indica melhora ou piora ambiental?",
                "resposta": "Melhora na cobertura: a vegetação cresceu de 64,8% para 66,7% da sub-bacia e a "
                            "agricultura recuou, o que sugere efeito das práticas de conservação adotadas. O alerta "
                            "fica por conta das áreas não vegetadas, que aumentaram de área e apresentaram "
                            "aquecimento médio próximo de 5 °C no período.",
            },
        ],
    },
    # =====================================================================
    {
        "id": 4,
        "rotulo": "Artigo 4",
        "titulo": "Análise espacial da distribuição do ensino em função da renda em uma bacia hidrográfica",
        "tema": "Geoestatística & desigualdade territorial",
        "veiculo": "Nativa, v. 10, n. 1, p. 05-15",
        "ano": "2022",
        "status": "publicado",
        "status_label": "Publicado · 2022",
        "autores": "Jomil Costa Abreu Sales; Camille Vasconcelos Silva; Darllan Collins da Cunha e Silva; "
                   "Omar Yazbek Bitar; Roberto Wagner Lourenço",
        "meu_papel": "Primeiro autor",
        "financiamento": "",
        "link_label": "Acessar o artigo (DOI 10.31413/nativa.v10i1.13137)",
        "link_url": "https://doi.org/10.31413/nativa.v10i1.13137",
        "referencia": "SALES, J. C. A.; SILVA, C. V.; SILVA, D. C. C.; BITAR, O. Y.; LOURENÇO, R. W. Análise espacial "
                      "da distribuição do ensino em função da renda em uma bacia hidrográfica. Nativa, Sinop, v. 10, "
                      "n. 1, p. 05-15, 2022.",
        "figuras_origem": "Figuras reproduzidas do artigo publicado em periódico de acesso aberto.",
        "pasta": "artigos_midia/artigo_04_rio_una",
        "pergunta": "A distribuição espacial da escolaridade na Bacia Hidrográfica do Rio Una acompanha a "
                    "distribuição da renda per capita dos setores censitários — e, se acompanha, em quais faixas "
                    "etárias essa relação se sustenta?",
        "pergunta_nota": "A bacia abastece a represa de Itupararanga, manancial de mais de 1,5 milhão de pessoas, o "
                         "que liga a questão social à gestão do território.",
        "problema": "Indicadores como o PIB e mesmo o IDH municipal escondem desigualdades internas ao município. "
                    "Sem espacializar renda e escolaridade dentro da bacia, políticas públicas de educação e de "
                    "gestão ambiental são desenhadas sobre uma média que não existe no território.",
        "hipotese": "A geoestatística aplicada aos setores censitários permite prever a distribuição contínua de "
                    "renda e escolaridade e revelar se as áreas de menor renda coincidem com as de menor "
                    "escolaridade e com a vocação agrícola da bacia.",
        "resultados": [
            "**Concentração de baixa renda:** 61,50% da área da bacia é ocupada por população com renda per capita "
            "inferior a meio salário mínimo; apenas 14,81% da área, próxima ao centro urbano, supera essa faixa.",
            "**Correlação só na população adulta:** pelo teste de Pearson, houve correlação entre renda e "
            "escolaridade **apenas na faixa acima de 20 anos** — crianças e jovens acessam a escola pública "
            "independentemente da renda familiar.",
            "**Coincidência espacial:** as áreas de menor renda e menor escolaridade coincidem com as porções de "
            "maior vocação agrícola, distantes do núcleo urbano (cerca de 36% da bacia é de uso agrícola).",
            "**Dependência espacial confirmada:** os semivariogramas mostraram forte dependência espacial para as "
            "faixas de 11 a 13 anos e acima de 20 anos, e dependência moderada nas demais variáveis.",
            "**Escolas concentradas:** o mapa de densidade de Kernel mostra a rede escolar concentrada no norte e "
            "nordeste da bacia, acompanhando a distribuição da população.",
        ],
        "solucao": [
            "**Priorizar as áreas rurais do centro-sul da bacia** em programas de alfabetização e educação de jovens "
            "e adultos, que é onde renda e escolaridade caem juntas.",
            "**Usar o mapeamento como instrumento de gestão ambiental:** a educação é apontada no estudo como "
            "ferramenta de prevenção e de conscientização na gestão do manancial.",
            "**Substituir a média municipal por análise setorizada** no desenho de políticas públicas — o IDH de "
            "Ibiúna (0,710) esconde a variação interna da bacia.",
        ],
        "figuras": [
            {
                "arquivo": "figura_01.png",
                "titulo": "Localização da Bacia Hidrográfica do Rio Una",
                "descricao": "Mapa de localização da BHRU, no município de Ibiúna (SP), a cerca de 75 km da capital. "
                             "O limite da bacia aparece em vermelho, a hidrografia em azul e a represa de "
                             "Itupararanga em destaque, com os municípios vizinhos (Votorantim, Alumínio, Mairinque, "
                             "Piedade) nomeados. Os mapas-índice situam a área no Estado de São Paulo.",
                "meta": {"Tipo": "Mapa de localização", "Sensor": "Bases vetoriais IBGE",
                         "Resolução": "Vetorial", "Datum": "SIRGAS 2000 / UTM 23K"},
            },
            {
                "arquivo": "figura_02.png",
                "titulo": "Distribuição da renda per capita",
                "descricao": "Superfície contínua de renda per capita obtida por krigagem ordinária a partir dos "
                             "setores censitários do Censo 2010. As sete faixas vão de R$ 322,83 a R$ 749,39. O "
                             "gradiente é claro: as maiores rendas (azul) concentram-se ao norte, junto ao núcleo "
                             "urbano, e caem progressivamente em direção ao sul rural (laranja e vermelho), onde "
                             "predomina o uso agrícola.",
                "meta": {"Tipo": "Superfície interpolada", "Sensor": "Censo Demográfico 2010 (IBGE)",
                         "Resolução": "Krigagem ordinária", "Datum": "WGS 84 / UTM 23K"},
            },
            {
                "arquivo": "figura_03.png",
                "titulo": "Fluxo escolar por faixa etária",
                "descricao": "Quatro painéis com a distribuição do fluxo escolar na bacia para as faixas de 5 a 6 (A), "
                             "11 a 13 (B), 15 a 17 (C) e 18 a 20 anos (D), cada um interpolado separadamente. A "
                             "comparação entre os painéis mostra que o padrão espacial muda com a idade: as faixas "
                             "mais jovens apresentam cobertura mais homogênea, enquanto as faixas mais velhas "
                             "concentram os melhores índices próximo às áreas urbanizadas.",
                "meta": {"Tipo": "Superfícies interpoladas", "Sensor": "Censo Demográfico 2010 (IBGE)",
                         "Resolução": "Krigagem ordinária", "Datum": "WGS 84 / UTM 23K"},
            },
            {
                "arquivo": "figura_04.png",
                "titulo": "Índice de escolaridade da população adulta",
                "descricao": "Distribuição do índice de escolaridade da população com mais de 20 anos, variando de "
                             "64,12% a 99,5%. É a variável que apresentou correlação significativa com a renda: o "
                             "mapa reproduz de perto o padrão da figura de renda per capita, com os menores índices "
                             "no sul e no oeste rural da bacia.",
                "meta": {"Tipo": "Superfície interpolada", "Sensor": "Censo Demográfico 2010 (IBGE)",
                         "Resolução": "Krigagem ordinária", "Datum": "WGS 84 / UTM 23K"},
            },
            {
                "arquivo": "figura_05.png",
                "titulo": "Semivariogramas das variáveis",
                "descricao": "Painel com os semivariogramas experimentais ajustados aos modelos teóricos para a renda "
                             "per capita e para cada faixa de escolaridade. São eles que justificam o uso da "
                             "krigagem: o índice de dependência espacial ficou entre 1,39% e 50%, com forte "
                             "dependência espacial nas faixas de 11 a 13 anos e acima de 20 anos.",
                "meta": {"Tipo": "Gráficos geoestatísticos", "Sensor": "Ajuste de semivariograma",
                         "Resolução": "—", "Datum": "—"},
            },
            {
                "arquivo": "figura_06.png",
                "titulo": "Localização e densidade das escolas",
                "descricao": "À esquerda, a localização das escolas na bacia sobre a malha de setores censitários; à "
                             "direita, a densidade obtida pelo estimador de Kernel, em seis classes. A concentração "
                             "no norte e nordeste explica por que os índices de escolaridade caem à medida que os "
                             "setores se afastam do núcleo urbano.",
                "meta": {"Tipo": "Mapa de pontos e densidade", "Sensor": "Georreferenciamento escolar",
                         "Resolução": "Estimador de Kernel", "Datum": "WGS 84 / UTM 23K"},
            },
        ],
        "perguntas": [
            {
                "pergunta": "Renda e escolaridade estão correlacionadas na bacia?",
                "resposta": "Sim, mas apenas na população adulta. O teste de Pearson mostrou correlação significativa "
                            "somente na faixa acima de 20 anos: quanto maior a renda, maior a probabilidade de a "
                            "pessoa ser alfabetizada. Nas faixas de 5 a 20 anos não houve correlação, o que é "
                            "atribuído ao acesso à escola pública independentemente da renda familiar.",
            },
            {
                "pergunta": "Que métodos geoestatísticos foram usados?",
                "resposta": "Krigagem ordinária para interpolar renda e escolaridade a partir dos 43 setores "
                            "censitários da bacia, com validação pelos semivariogramas (índice de dependência "
                            "espacial entre 1,39% e 50%), e estimador de densidade de Kernel para a distribuição das "
                            "escolas. Os dados vieram do Censo Demográfico de 2010.",
            },
            {
                "pergunta": "Qual é o retrato de renda da bacia?",
                "resposta": "61,50% da área da bacia é ocupada por população com renda per capita inferior a meio "
                            "salário mínimo, e apenas 14,81% da área — concentrada junto ao centro urbano — fica "
                            "acima dessa faixa. A renda cai à medida que se afasta do núcleo urbano, acompanhando a "
                            "vocação agrícola da bacia.",
            },
            {
                "pergunta": "Por que esse tema aparece num portfólio ambiental?",
                "resposta": "Porque a bacia do Rio Una é um dos principais contribuintes da represa de Itupararanga, "
                            "manancial de mais de 1,5 milhão de pessoas. O estudo trata escolaridade e renda como "
                            "variáveis territoriais que ajudam a explicar a pressão sobre o manancial e a orientar "
                            "políticas de educação ambiental onde elas têm mais efeito.",
            },
        ],
    },
    # =====================================================================
    {
        "id": 5,
        "rotulo": "Artigo 5",
        "titulo": "Creation of an environmental sustainability index for water resources applied to watersheds",
        "tema": "Índice multicritério & sustentabilidade hídrica",
        "veiculo": "Environment, Development and Sustainability, v. 25, p. 11285-11305",
        "ano": "2023",
        "status": "publicado",
        "status_label": "Publicado · 2023 (Springer)",
        "autores": "Darllan Collins da Cunha e Silva; Renan Angrizani Oliveira; Vanessa Cezar Simonetti; "
                   "Bruno Pereira Toniolo; Jomil Costa Abreu Sales; Roberto Wagner Lourenço",
        "meu_papel": "Coautor",
        "financiamento": "",
        "link_label": "Acessar o artigo (DOI 10.1007/s10668-022-02527-9)",
        "link_url": "https://doi.org/10.1007/s10668-022-02527-9",
        "referencia": "SILVA, D. C. C.; OLIVEIRA, R. A.; SIMONETTI, V. C.; TONIOLO, B. P.; SALES, J. C. A.; "
                      "LOURENÇO, R. W. Creation of an environmental sustainability index for water resources applied "
                      "to watersheds. Environment, Development and Sustainability, v. 25, p. 11285-11305, 2023.",
        "figuras_origem": "Figuras do artigo publicado (Springer Nature).",
        "pasta": "artigos_midia/artigo_05_wrsi_ahp",
        "pergunta": "É possível resumir em um único número, comparável entre sub-bacias, a sustentabilidade dos "
                    "recursos hídricos — integrando qualidade da água, saneamento e condição da vegetação?",
        "pergunta_nota": "O índice foi construído para ser replicável: uma vez definidos os pesos, podem ser "
                         "aplicados a outras bacias, permitindo comparação.",
        "problema": "A avaliação de bacias costuma tratar separadamente qualidade da água, cobertura vegetal e "
                    "saneamento. O gestor recebe indicadores desconexos, difíceis de hierarquizar, e sem uma medida "
                    "que aponte onde intervir primeiro.",
        "hipotese": "A integração de um índice físico-químico da água (PWI), um índice de vegetação úmida (WVI) e um "
                    "índice de saneamento e potencial de degradação (PWDI), ponderados pelo método AHP, produz um "
                    "índice sintético (WRSI) sensível o bastante para diferenciar sub-bacias e apoiar decisão.",
        "resultados": [
            "**Índice sintético WRSI:** varia de 0 (pior condição) a 1 (melhor) e resulta da agregação de três "
            "indicadores — PWI (qualidade físico-química da água), WVI (vegetação úmida) e PWDI (saneamento) — "
            "ponderados por AHP.",
            "**Diagnóstico da bacia:** cerca de **24% da área** apresentou WRSI em torno de **0,6**, condição "
            "classificada como regular; valores acima de 0,9 seriam os desejáveis.",
            "**Piores condições onde há agricultura e saneamento precário:** os menores valores concentram-se nas "
            "sub-bacias rurais do centro e do sul, que combinam uso agrícola predominante e ausência de coleta de esgoto.",
            "**Mata ciliar fragilizada:** os valores de integridade das matas ciliares (WPI) são baixos em toda a "
            "bacia, inclusive na porção mais preservada ao sul.",
            "**Estresse hídrico na vegetação:** o WVI mostrou vegetação sob estresse nas áreas urbanas e agrícolas, "
            "enquanto na região norte os valores ficaram acima de 0,9.",
        ],
        "solucao": [
            "**Priorizar saneamento rural:** o PWDI ficou abaixo de 0,5 em toda a bacia, indicando que a coleta e o "
            "tratamento de esgoto são o gargalo mais imediato.",
            "**Recompor matas ciliares** nas faixas de até 30 m dos cursos d'água, onde o índice de integridade se "
            "mostrou consistentemente baixo.",
            "**Adotar o WRSI como instrumento de comparação e acompanhamento** entre sub-bacias, já que os pesos "
            "definidos pelo AHP podem ser replicados em outras bacias.",
        ],
        "figuras": [
            {
                "arquivo": "figura_01.png",
                "titulo": "Localização da Bacia do Rio Una",
                "descricao": "Mapa de localização da bacia do Rio Una, em Ibiúna (SP), com o limite em vermelho, a "
                             "hidrografia e a represa de Itupararanga ao norte. Os mapas-índice mostram a posição da "
                             "bacia no Brasil, no Estado de São Paulo e na região.",
                "meta": {"Tipo": "Mapa de localização", "Sensor": "Bases vetoriais oficiais",
                         "Resolução": "Vetorial", "Datum": "SIRGAS 2000 / UTM 23K"},
            },
            {
                "arquivo": "figura_02.png",
                "titulo": "Pontos de coleta de água",
                "descricao": "Distribuição dos pontos de amostragem de água (em laranja) sobre a divisão da bacia em "
                             "11 sub-bacias numeradas, com a hidrografia detalhada. É essa malha de sub-bacias que "
                             "organiza todos os demais mapas do estudo e permite comparar os índices entre si.",
                "meta": {"Tipo": "Mapa de amostragem", "Sensor": "Levantamento de campo",
                         "Resolução": "11 sub-bacias", "Datum": "SIRGAS 2000 / UTM 23K"},
            },
            {
                "arquivo": "figura_03.png",
                "titulo": "Índice físico-químico da água (PWI)",
                "descricao": "Distribuição do PWI por sub-bacia, com valores entre 0,634 e 0,806 e escala de cor do "
                             "vermelho (pior) ao verde-escuro (melhor). Os piores valores concentram-se nas "
                             "sub-bacias do sul e do sudoeste, enquanto as melhores condições aparecem ao norte e a "
                             "leste da bacia.",
                "meta": {"Tipo": "Mapa de índice por sub-bacia", "Sensor": "Parâmetros físico-químicos de água",
                         "Resolução": "11 sub-bacias", "Datum": "SIRGAS 2000 / UTM 23K"},
            },
            {
                "arquivo": "figura_04.png",
                "titulo": "NDWI das áreas florestais e WVI por sub-bacia",
                "descricao": "À esquerda (A), o NDWI calculado para as áreas florestais, em que os tons alaranjados "
                             "indicam vegetação com menor conteúdo de água — inclusive valores negativos, de alto "
                             "estresse hídrico. À direita (B), o índice de vegetação úmida (WVI) agregado por "
                             "sub-bacia, de 0,49 a 0,94. A vegetação mais estressada está nas áreas urbanas e "
                             "agrícolas, onde compete por água com as atividades antrópicas.",
                "meta": {"Tipo": "Índice espectral e agregação zonal", "Sensor": "Imagem orbital multiespectral",
                         "Resolução": "Pixel e sub-bacia", "Datum": "SIRGAS 2000 / UTM 23K"},
            },
            {
                "arquivo": "figura_05.png",
                "titulo": "Mapas de SSI, WPI e WSUI",
                "descricao": "Três mapas na mesma escala (0 a 0,8) com os componentes do diagnóstico: SSI (condição "
                             "sanitária), WPI (integridade das matas ciliares) e WSUI (uso da água). O WPI aparece "
                             "inteiramente nas duas faixas mais baixas, evidenciando mata ciliar fragilizada em toda "
                             "a bacia; o SSI mostra as piores condições no centro e no sul, áreas rurais sem coleta "
                             "de esgoto.",
                "meta": {"Tipo": "Mapas de indicadores", "Sensor": "Dados censitários e geoprocessamento",
                         "Resolução": "11 sub-bacias", "Datum": "SIRGAS 2000 / UTM 23K"},
            },
            {
                "arquivo": "figura_06.png",
                "titulo": "Índice de potencial de degradação (PWDI)",
                "descricao": "Distribuição do PWDI por sub-bacia, com valores de 0,029 a 0,482 — todos abaixo de 0,5, "
                             "ou seja, menos da metade do valor máximo admitido para o índice. Os piores resultados "
                             "estão nas sub-bacias do sul e do centro, onde se somam a falta de gestão na "
                             "distribuição de água para consumo humano e o lançamento de esgoto doméstico.",
                "meta": {"Tipo": "Mapa de índice por sub-bacia", "Sensor": "Censo Demográfico e geoprocessamento",
                         "Resolução": "11 sub-bacias", "Datum": "SIRGAS 2000 / UTM 23K"},
            },
            {
                "arquivo": "figura_07.png",
                "titulo": "Índice de sustentabilidade dos recursos hídricos (WRSI)",
                "descricao": "Resultado final do estudo: à esquerda (A), os valores contínuos do WRSI por sub-bacia, "
                             "de 0,50 a 0,64; à direita (B), a mesma informação reclassificada em duas categorias, "
                             "Regular (verde) e Poor (laranja). As sub-bacias classificadas como ruins são as rurais, "
                             "de predomínio agrícola e saneamento precário.",
                "meta": {"Tipo": "Mapa síntese multicritério", "Sensor": "Agregação AHP de PWI, WVI e PWDI",
                         "Resolução": "11 sub-bacias", "Datum": "SIRGAS 2000 / UTM 23K"},
            },
        ],
        "perguntas": [
            {
                "pergunta": "O que é o WRSI e como ele é calculado?",
                "resposta": "O Water Resources Sustainability Index é um índice sintético que varia de 0 (pior "
                            "condição) a 1 (melhor). Ele agrega três indicadores — o PWI, de qualidade físico-química "
                            "da água; o WVI, de vegetação úmida; e o PWDI, ligado ao saneamento e ao potencial de "
                            "degradação — ponderados pelo método de Análise Hierárquica de Processos (AHP).",
            },
            {
                "pergunta": "Por que usar AHP para definir os pesos?",
                "resposta": "Porque o AHP converte julgamentos de importância relativa em pesos numéricos "
                            "consistentes, por meio de uma matriz de comparação pareada entre as variáveis, com "
                            "verificação do índice de consistência. Definidos uma vez, esses pesos podem ser "
                            "replicados em outras bacias, o que mantém a integridade do índice e permite comparação.",
            },
            {
                "pergunta": "Qual foi o diagnóstico da bacia estudada?",
                "resposta": "Cerca de 24% da área apresentou WRSI em torno de 0,6 — condição regular, quando o "
                            "desejável seria acima de 0,9. As piores condições estão nas sub-bacias rurais do centro "
                            "e do sul, que combinam predomínio agrícola e saneamento básico precário. O PWDI ficou "
                            "abaixo de 0,5 em toda a bacia.",
            },
            {
                "pergunta": "Qual é a principal limitação do estudo?",
                "resposta": "O próprio artigo aponta: o componente de saneamento usa dados do Censo Demográfico de "
                            "2010, o último disponível na época (o censo de 2020 não foi realizado por causa da "
                            "pandemia). Os autores sugerem, para trabalhos futuros, uma análise temporal com dados de "
                            "mesmo ano-base e a comparação com outros métodos de decisão multicritério.",
            },
        ],
    },
    # =====================================================================
    {
        "id": 6,
        "rotulo": "Artigo 6",
        "titulo": "Reflexos Ambientais do Desenvolvimento e Expansão das Atividades Humanas sobre a Qualidade da Água",
        "tema": "Expansão antrópica & qualidade da água",
        "veiculo": "Revista Brasileira de Geografia Física, v. 15, n. 1, p. 175-198",
        "ano": "2022",
        "status": "publicado",
        "status_label": "Publicado · 2022",
        "autores": "Roberto Wagner Lourenço; Jomil Costa Abreu Sales; Leticia Tondato Arantes; "
                   "Camille Vasconcelos Silva; Darllan Collins da Cunha e Silva",
        "meu_papel": "Segundo autor",
        "financiamento": "",
        "link_label": "Acessar o artigo (DOI 10.26848/rbgf.v15.1.p176-198)",
        "link_url": "https://doi.org/10.26848/rbgf.v15.1.p176-198",
        "referencia": "LOURENÇO, R. W.; SALES, J. C. A.; ARANTES, L. T.; SILVA, C. V.; SILVA, D. C. C. Reflexos "
                      "Ambientais do Desenvolvimento e Expansão das Atividades Humanas sobre a Qualidade da Água. "
                      "Revista Brasileira de Geografia Física, v. 15, n. 1, p. 175-198, 2022.",
        "figuras_origem": "Figuras reproduzidas do artigo publicado em acesso aberto sob licença CC BY 4.0.",
        "pasta": "artigos_midia/artigo_06_fosforo_agua",
        "pergunta": "Como 25 anos de expansão urbana e agrícola na Bacia Hidrográfica do Rio Una se refletiram na "
                    "qualidade da água do manancial que abastece a represa de Itupararanga?",
        "pergunta_nota": "O estudo liga, no mesmo território, a dinâmica de uso da terra, o desenvolvimento humano e "
                         "os parâmetros de qualidade da água monitorados pela CETESB.",
        "problema": "A degradação de mananciais raramente é acompanhada de forma integrada: o uso da terra é "
                    "monitorado por um órgão, a qualidade da água por outro, e os indicadores sociais por um terceiro. "
                    "Sem cruzar as três dimensões, não se identifica qual atividade responde pela carga de nutrientes.",
        "hipotese": "O avanço das classes antrópicas — sobretudo agricultura e área urbana — sobre as áreas naturais "
                    "da bacia se expressa de forma detectável nos parâmetros de qualidade da água, em especial no "
                    "fósforo total, indicador de eutrofização.",
        "resultados": [
            "**Perda florestal expressiva:** a floresta caiu de 5.580,39 ha (57,88% da bacia) em 1991 para "
            "3.574,66 ha (37,06%) em 2016.",
            "**Agricultura dobrou:** a classe agrícola cresceu cerca de **105%** no período, um acréscimo de "
            "1.831,23 ha, passando a ocupar 35,99% da bacia.",
            "**Paisagem majoritariamente antrópica:** somadas as classes de origem humana (área urbana, "
            "reflorestamento, pastagem e agricultura), elas ocupam **54,13%** da bacia.",
            "**IQA estável, mas apenas regular:** entre 2005 e 2015 o Índice de Qualidade da Água manteve-se sempre "
            "na faixa regular (valores entre 39 e 50, dentro do intervalo > 36 e ≤ 51).",
            "**Fósforo acima do limite legal:** o parâmetro fósforo total superou o valor estabelecido pela Resolução "
            "CONAMA, indicando fontes difusas de poluição ligadas às atividades agrícola e urbana.",
        ],
        "solucao": [
            "**Controle de fontes difusas na área agrícola**, que concentra o aporte de nutrientes responsável pela "
            "eutrofização do manancial.",
            "**Ampliação do saneamento básico**, apontado como um dos vetores diretos da degradação da qualidade da água.",
            "**Contenção da supressão de vegetação**, já que a perda florestal acompanhou, no mesmo período, a "
            "elevação dos indicadores de pressão sobre a água.",
        ],
        "figuras": [
            {
                "arquivo": "figura_01.png",
                "titulo": "Área de estudo",
                "descricao": "Localização da Bacia Hidrográfica do Rio Una, em Ibiúna (SP), com o limite em vermelho, "
                             "a hidrografia e a represa de Itupararanga ao norte. A bacia integra a UGRHI 10 "
                             "(Sorocaba e Médio Tietê) e, junto com os rios Sorocabuçu e Sorocamirim, alimenta o "
                             "reservatório de Itupararanga.",
                "meta": {"Tipo": "Mapa de localização", "Sensor": "Bases vetoriais oficiais",
                         "Resolução": "Vetorial", "Datum": "SIRGAS 2000 / UTM 23K"},
            },
            {
                "arquivo": "figura_02.png",
                "titulo": "Composição do uso da terra (2016)",
                "descricao": "Gráfico de setores com a participação de cada classe de uso e cobertura em 2016: "
                             "floresta 37,06%, agricultura 35,98%, áreas urbanas 15,16%, campo sujo 7,89%, "
                             "reflorestamento 2,44%, áreas alagadas 0,91% e pasto 0,56%. Somadas, as classes "
                             "antrópicas superam a metade da bacia.",
                "meta": {"Tipo": "Gráfico de composição", "Sensor": "Classificação de imagens orbitais",
                         "Resolução": "% da área", "Datum": "—"},
            },
            {
                "arquivo": "figura_03.png",
                "titulo": "Mapa de uso e cobertura da terra (2016)",
                "descricao": "Mapa temático da bacia em 2016, com sete classes de uso e cobertura. A região central e "
                             "sudoeste é predominantemente agrícola (laranja), enquanto a expansão urbana (magenta) "
                             "se destaca na porção centro-sul, ao longo dos eixos viários. Os fragmentos florestais "
                             "(verde-escuro) aparecem dispersos e fragmentados pela matriz agrícola.",
                "meta": {"Tipo": "Mapa de uso e cobertura", "Sensor": "Classificação de imagens orbitais",
                         "Resolução": "—", "Datum": "WGS 84 / UTM 23K"},
            },
            {
                "arquivo": "figura_04.png",
                "titulo": "Evolução das classes de uso (1991-2016)",
                "descricao": "Gráfico de barras comparando a área, em hectares, de cada classe nos quatro anos "
                             "analisados (1991, 2001, 2010 e 2016). A leitura é direta: as barras da floresta "
                             "decrescem ano a ano, enquanto as da agricultura e das áreas urbanas crescem de forma "
                             "contínua ao longo dos 25 anos.",
                "meta": {"Tipo": "Gráfico comparativo", "Sensor": "Tabulação das classes",
                         "Resolução": "hectares", "Datum": "—"},
            },
            {
                "arquivo": "figura_05.png",
                "titulo": "Uso da terra em 1991, 2001, 2010 e 2016",
                "descricao": "Quatro mapas na mesma legenda, um para cada ano da série. A sequência mostra a matriz "
                             "verde de 1991 sendo progressivamente substituída pelo laranja da agricultura e pelo "
                             "magenta da área urbana, que se adensa na porção central da bacia.",
                "meta": {"Tipo": "Série multitemporal", "Sensor": "Classificação de imagens orbitais",
                         "Resolução": "—", "Datum": "WGS 84 / UTM 23K"},
            },
            {
                "arquivo": "figura_06.png",
                "titulo": "Perdas e ganhos de área entre 1991 e 2001",
                "descricao": "Gráfico de barras divergentes: à esquerda (roxo) as perdas e à direita (verde) os "
                             "ganhos de cada classe, em hectares, no primeiro intervalo da série. A floresta aparece "
                             "com a maior perda do período (594 ha) e a agricultura com o maior ganho (665 ha).",
                "meta": {"Tipo": "Gráfico de balanço", "Sensor": "Tabulação cruzada de classes",
                         "Resolução": "hectares", "Datum": "—"},
            },
            {
                "arquivo": "figura_07.png",
                "titulo": "Mudanças e permanências entre 1991 e 2001",
                "descricao": "À esquerda (A), o mapa das transições entre classes no período, com cada combinação de "
                             "origem e destino em uma cor. À direita (B), o mapa de permanência, mostrando o que não "
                             "mudou. Apesar da maior perda absoluta, a floresta foi também a classe com maior área "
                             "de permanência (4.521,82 ha).",
                "meta": {"Tipo": "Mapas de transição", "Sensor": "Tabulação cruzada de classes",
                         "Resolução": "—", "Datum": "WGS 84 / UTM 23K"},
            },
            {
                "arquivo": "figura_08.png",
                "titulo": "Perdas e ganhos de área entre 2010 e 2016",
                "descricao": "Mesmo formato de barras divergentes da figura anterior, agora para o intervalo final da "
                             "série. O padrão se repete e se intensifica: a agricultura lidera os ganhos, enquanto "
                             "floresta e campo concentram as perdas.",
                "meta": {"Tipo": "Gráfico de balanço", "Sensor": "Tabulação cruzada de classes",
                         "Resolução": "hectares", "Datum": "—"},
            },
            {
                "arquivo": "figura_09.png",
                "titulo": "Mudanças e permanências entre 2010 e 2016",
                "descricao": "Mapas de transição (A) e de permanência (B) para o intervalo de 2010 a 2016. A área de "
                             "floresta que permaneceu estável caiu para 2.889,99 ha, enquanto as áreas agrícolas "
                             "praticamente dobraram sua extensão em relação ao início da série.",
                "meta": {"Tipo": "Mapas de transição", "Sensor": "Tabulação cruzada de classes",
                         "Resolução": "—", "Datum": "WGS 84 / UTM 23K"},
            },
            {
                "arquivo": "figura_10.png",
                "titulo": "Índice de Desenvolvimento Humano por setor censitário",
                "descricao": "Mapa temático do IDH dos setores censitários da bacia em 2010, classificados conforme "
                             "as faixas do PNUD. Predominam as classes alto e muito alto (verdes), com um único "
                             "setor na faixa média (amarelo), ao sul — o mesmo setor rural onde os indicadores de "
                             "saneamento e renda são mais frágeis.",
                "meta": {"Tipo": "Mapa temático socioeconômico", "Sensor": "Censo Demográfico 2010 (IBGE)",
                         "Resolução": "Setores censitários", "Datum": "WGS 84 / UTM 23K"},
            },
            {
                "arquivo": "figura_11.png",
                "titulo": "Índice de Qualidade da Água (2005-2015)",
                "descricao": "Série anual dos valores médios do IQA reportados pela CETESB entre 2005 e 2015, de 39 a "
                             "50 pontos. Todos os anos permanecem dentro da faixa 'regular' (acima de 36 e até 51), "
                             "sem tendência clara de melhora ou piora ao longo da década.",
                "meta": {"Tipo": "Série temporal", "Sensor": "Relatórios de qualidade da CETESB",
                         "Resolução": "Média anual", "Datum": "—"},
            },
            {
                "arquivo": "figura_12.png",
                "titulo": "Fósforo total e nitrato (2005-2015)",
                "descricao": "Gráfico de barras com as médias anuais de fósforo total (azul, eixo à esquerda) e "
                             "nitrato (verde, eixo à direita), em mg/L, entre 2005 e 2015. É a figura que sustenta a "
                             "conclusão do estudo: o fósforo se mantém elevado ao longo de toda a série, acima do "
                             "limite legal, indicando aporte contínuo de fontes difusas agrícolas e urbanas e risco "
                             "de eutrofização do manancial.",
                "meta": {"Tipo": "Série temporal de parâmetros", "Sensor": "Monitoramento CETESB",
                         "Resolução": "Média anual (mg/L)", "Datum": "—"},
            },
        ],
        "perguntas": [
            {
                "pergunta": "O que aconteceu com a floresta da bacia em 25 anos?",
                "resposta": "A área de floresta caiu de 5.580,39 ha em 1991, quando ocupava 57,88% da bacia, para "
                            "3.574,66 ha em 2016, ou 37,06%. No mesmo período a agricultura cresceu cerca de 105%, um "
                            "acréscimo de 1.831,23 ha, tornando-se a segunda maior classe da bacia.",
            },
            {
                "pergunta": "Qual parâmetro de qualidade da água ficou fora do limite?",
                "resposta": "O fósforo total. Apesar de o Índice de Qualidade da Água (IQA) se manter na faixa "
                            "regular durante toda a série de 2005 a 2015, o fósforo apresentou valores acima do "
                            "limite estabelecido pela Resolução CONAMA, o que indica aporte de fontes difusas de "
                            "poluição e acelera o processo de eutrofização.",
            },
            {
                "pergunta": "De onde vem esse fósforo?",
                "resposta": "Das atividades que dominam a bacia: agricultura, que responde por cerca de 36% da área e "
                            "aporta fertilizantes por escoamento difuso, e ocupação urbana sem saneamento adequado. "
                            "O estudo também pondera que as amostras da CETESB são coletadas no exutório da bacia, "
                            "onde se acumula a carga de todo o território a montante.",
            },
            {
                "pergunta": "Como o estudo conecta desenvolvimento humano e qualidade da água?",
                "resposta": "Ele espacializa o IDH por setor censitário e o compara com a dinâmica de uso da terra e "
                            "com os parâmetros de qualidade da água. A leitura conjunta mostra que a expansão das "
                            "atividades antrópicas — urbanização em larga escala, ausência de saneamento e supressão "
                            "de vegetação — é o que exerce maior influência sobre a qualidade do recurso hídrico.",
            },
        ],
    },
]

ARTIGOS_POR_ID = {a["id"]: a for a in ARTIGOS}
