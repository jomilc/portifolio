# Portfólio científico — Dr. Jomil Costa Abreu Sales

Aplicação Streamlit com a produção científica, o WebSIG interativo dos artigos e os serviços de
consultoria ambiental.

## Rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## WebSIG

A seção **WebSIG Interativo (APA Itupararanga)** carrega um mapa Leaflet onde cada camada é ligada e
desligada com um clique, sem recarregar a página: os dados são baixados sob demanda da pasta
`static/`, servida pelo próprio Streamlit (`.streamlit/config.toml` → `enableStaticServing = true`).

```
tools/build_websig.py   pipeline: shapefiles/GeoTIFFs → GeoJSON + PNG (Web Mercator) + manifest
websig/map.html         front-end do mapa (painel de camadas, legenda, consulta, comparação)
static/websig/          dados publicados: manifest.json, vectors/*.geojson, rasters/*.png
```

O mapa oferece consulta por clique (valores de todas as camadas ativas no ponto), legenda com áreas
por classe, controle de opacidade, metadados por camada e comparação de dois rasters com cortina
deslizante.

### Regerar os dados

Os arquivos originais (shapefiles e GeoTIFFs, ~400 MB) não ficam no repositório. Para regerar
`static/websig/` a partir deles:

```bash
pip install -r tools/requirements-build.txt
python tools/build_websig.py --src "caminho/para/SHAPEFILES_APA_ITUPARARANGA"
```

O script reprojeta tudo para Web Mercator, simplifica os vetores, reamostra os rasters para a web
(≈16–25 m), aplica a paleta das figuras do artigo e grava o `manifest.json`.

### Acrescentar camadas de outro artigo

Basta editar a lista `ARTICLES` em `tools/build_websig.py` — um bloco por artigo, com seus grupos e
camadas — e rodar o script de novo. O painel, a legenda, a consulta e a tabela de metadados do app
são montados a partir do manifest; `app.py` não precisa ser alterado.
