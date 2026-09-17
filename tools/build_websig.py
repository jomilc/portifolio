"""
Pipeline de dados do WebSIG — Dr. Jomil Costa Abreu Sales

Converte os shapefiles e GeoTIFFs originais dos artigos em camadas leves para a web
(GeoJSON simplificado + PNG em Web Mercator) e grava um manifest.json que o app lê.

Uso:
    python tools/build_websig.py --src "caminho/para/SHAPEFILES_APA_ITUPARARANGA"

Para incluir camadas de outro artigo, acrescente um bloco em ARTICLES (mesmo formato
do artigo 1), aponte os arquivos em "src" e rode o script de novo. Nada no app.py
precisa mudar: o painel de camadas é montado a partir do manifest.
"""

import argparse
import json
import os
import shutil
import unicodedata
import warnings
from datetime import datetime

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import shapely
from PIL import Image
from pyproj import CRS, Transformer
from rasterio.warp import Resampling, calculate_default_transform, reproject
from shapely.geometry import MultiPolygon, Polygon
from shapely.geometry.base import BaseGeometry

warnings.filterwarnings("ignore")

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SRC = os.path.join(REPO_ROOT, "SHAPEFILES_APA_ITUPARARANGA")
DEFAULT_OUT = os.path.join(REPO_ROOT, "static", "websig")

UTM_23S = "EPSG:31983"  # SIRGAS 2000 / UTM 23S — CRS métrico para simplificação e áreas

# -----------------------------------------------------------------------------
# PALETAS (amostradas das legendas das figuras oficiais do artigo)
# -----------------------------------------------------------------------------
LULC_CLASSES = {
    1: ("Corpos d'água", "#88C0D8"),
    2: ("Floresta nativa", "#3E7840"),
    3: ("Silvicultura", "#707830"),
    4: ("Área urbana", "#F0A8C0"),
    5: ("Agricultura", "#F0B060"),
    6: ("Formação campestre", "#D0E878"),
}
CO2_CLASSES = {
    1: ("Área antrópica", "#AAAAAA"),
    2: ("Baixo potencial", "#D9EF8B"),
    3: ("Moderado potencial", "#91CF60"),
    4: ("Alto potencial", "#1A9641"),
    5: ("Muito alto potencial", "#005A2B"),
}
ZONES = {
    "ZCB": ("Zona de Conservação da Biodiversidade", "#6CC45C"),
    "ZCRH": ("Zona de Conservação dos Recursos Hídricos", "#C27AD8"),
    "ZOR": ("Zona de Ocupação Rural", "#8397E8"),
    "ZOD": ("Zona de Ocupação Diversificada", "#B8577A"),
    "ZOC": ("Zona de Ocupação Consolidada", "#EE9A7E"),
}
RAMPS = {
    "ylgn": ["#FFFFE5", "#F7FCB9", "#D9F0A3", "#ADDD8E", "#78C679", "#41AB5D", "#238443", "#006837", "#004529"],
    "ndvi": ["#A50026", "#F46D43", "#FEE08B", "#D9EF8B", "#66BD63", "#1A9850", "#006837"],
    "viridis": ["#440154", "#3B528B", "#21918C", "#5EC962", "#FDE725"],
    "gpp": ["#EAF6D2", "#B8E1A0", "#7BC77B", "#479F5E", "#117540"],
}

CONTINUOUS_LEVELS = 128
MAX_PX_CATEGORICAL = 3000
MAX_PX_CONTINUOUS = 2000

SENTINEL_SRC = "Sentinel-2 MSI L2A (ESA/Copernicus) · processamento dos autores"

# -----------------------------------------------------------------------------
# CATÁLOGO DE CAMADAS POR ARTIGO
# -----------------------------------------------------------------------------
ARTICLES = [
    {
        "id": "art1",
        "title": "Fluxo de CO₂ na APA de Itupararanga",
        "subtitle": "Preprint 2024 · Sentinel-2 10 m · MOLUSCE 2028",
        "citation": "Sales, J. C. A.; Nicomedes, N. P.; Silva, D. C. C.; Lourenço, R. W. Carbon Flux Potential "
                    "Prediction Model Based on Land Cover and Land Use: Application in the Itupararanga "
                    "Environmental Protection Area, SP, Brazil. SSRN, 2024 (preprint).",
        "url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7268395",
        "home_layer": "apa_limite",
        "defaults": ["apa_limite", "co2c_2023"],
        "compare": ["co2c_2019", "co2c_2023"],
        "groups": [
            {
                "id": "limites",
                "title": "Limites & zoneamento",
                "layers": [
                    {
                        "id": "apa_limite", "kind": "vector", "name": "Limite oficial da APA",
                        "src": "01_Study_Area/EPA_Boundary_SIRGAS_UTM.shp", "builder": "apa_boundary",
                        "style": {"color": "#0F172A", "weight": 3, "fill": False, "halo": True},
                        "source": "Fundação Florestal / SEMIL-SP",
                        "description": "Perímetro legal da APA de Itupararanga (938,31 km²), Lei Estadual nº 10.100/1998.",
                    },
                    {
                        "id": "apa_zonas", "kind": "vector", "name": "Zoneamento do Plano de Manejo",
                        "src": "01_Study_Area/EPA_Zones_SIRGAS_UTM.shp", "builder": "apa_zones",
                        "style": {"weight": 1, "fillOpacity": 0.45},
                        "source": "Plano de Manejo da APA de Itupararanga",
                        "description": "Cinco zonas de gestão (ZCB, ZCRH, ZOR, ZOD e ZOC), dissolvidas por zona.",
                    },
                    {
                        "id": "municipios", "kind": "vector", "name": "Municípios da APA",
                        "src": "01_Study_Area/Municipalities_SaoPaulo_2010.shp", "builder": "municipalities",
                        "style": {"color": "#1E293B", "weight": 1.6, "dashArray": "5 4", "fill": False, "halo": True},
                        "source": "IBGE — malha municipal e Censo 2010",
                        "description": "Municípios com mais de 1 km² dentro da APA, com área abrangida e dados do Censo 2010.",
                    },
                    {
                        "id": "sp_estado", "kind": "vector", "name": "Estado de São Paulo",
                        "src": "01_Study_Area/SaoPaulo_State_SIRGAS_UTM.shp", "builder": "state",
                        "style": {"color": "#475569", "weight": 1.2, "fill": False, "halo": True},
                        "source": "IBGE",
                        "description": "Contorno estadual para contexto regional.",
                    },
                ],
            },
            {
                "id": "lulc",
                "title": "Cobertura e uso da terra",
                "layers": [
                    {
                        "id": f"lc_{year}", "kind": "raster", "mode": "categorical",
                        "name": f"Cobertura da terra {year}" + (" (projeção)" if year == 2028 else ""),
                        "year": year, "src": f"02_Land_Cover/LC_{year}_SIRGAS_UTM.tif",
                        "classes": LULC_CLASSES,
                        "stats": ("02_Land_Cover/land_cover_statistics_2019_2023_2028.csv", year),
                        "source": ("Simulação MOLUSCE (ANN-MLP + CA-Markov) · QGIS" if year == 2028
                                   else "MapBiomas Coleção 10 m (beta, Sentinel-2) reclassificado"),
                        "description": ("Cenário projetado de cobertura da terra para 2028." if year == 2028
                                        else f"Cobertura e uso da terra em {year}, reclassificada em 6 classes."),
                    }
                    for year in (2019, 2023, 2028)
                ],
            },
            {
                "id": "co2_classes",
                "title": "Potencial de fluxo de CO₂ (classes)",
                "layers": [
                    {
                        "id": f"co2c_{year}", "kind": "raster", "mode": "categorical",
                        "name": f"Classes de CO₂ {year}" + (" (projeção)" if year == 2028 else ""),
                        "year": year, "src": f"03_CO2_Flux/CO2Flux_Classified_{year}_SIRGAS_UTM.tif",
                        "classes": CO2_CLASSES,
                        "stats": ("03_CO2_Flux/co2flux_statistics_2019_2023_2028.csv", year),
                        "source": ("Simulação MOLUSCE sobre as classes de CO₂" if year == 2028 else SENTINEL_SRC),
                        "description": ("Cenário projetado das classes de potencial de fluxo de CO₂ para 2028."
                                        if year == 2028 else
                                        f"Classes do proxy sPRI × NDVI em {year} (5 classes de potencial)."),
                    }
                    for year in (2019, 2023, 2028)
                ],
            },
            {
                "id": "floresta",
                "collapsed": True,
                "title": "Manchas florestais (vetor)",
                "layers": [
                    {
                        "id": f"floresta_{year}", "kind": "vector", "name": f"Contorno florestal {year}",
                        "year": year, "src": f"03_CO2_Flux/Natural_Areas_CO2Potential_{year}.shp",
                        "builder": "forest_outline",
                        "style": {"color": color, "weight": 1.3, "fill": False},
                        "source": SENTINEL_SRC,
                        "description": f"Contorno das manchas de floresta nativa ({year}) usadas na análise de CO₂. "
                                       "Simplificado a 15 m; manchas e clareiras menores que 2 ha omitidas.",
                    }
                    for year, color in ((2019, "#F59E0B"), (2023, "#7C3AED"))
                ],
            },
            {
                "id": "co2_proxy",
                "collapsed": True,
                "title": "Proxy contínuo sPRI × NDVI",
                "layers": [
                    {
                        "id": f"co2_{year}", "kind": "raster", "mode": "continuous", "name": f"sPRI × NDVI {year}",
                        "year": year, "src": f"03_CO2_Flux/CO2Flux_{year}_SIRGAS_UTM.tif",
                        "vmin": 0.0, "vmax": 0.30, "ramp": "ylgn", "unit": "índice", "decimals": 3,
                        "source": SENTINEL_SRC,
                        "description": f"Proxy espectral relativo do potencial de sequestro de CO₂ ({year}).",
                    }
                    for year in (2019, 2023)
                ],
            },
            {
                "id": "indices",
                "collapsed": True,
                "title": "Índices espectrais",
                "layers": [
                    *[
                        {
                            "id": f"ndvi_{year}", "kind": "raster", "mode": "continuous", "name": f"NDVI {year}",
                            "year": year, "src": f"05_Spectral_Indices/NDVI_{year}_SIRGAS_UTM.tif",
                            "vmin": -0.1, "vmax": 0.7, "ramp": "ndvi", "unit": "índice", "decimals": 2,
                            "source": SENTINEL_SRC,
                            "description": f"NDVI = (B08 − B04) / (B08 + B04), inverno seco de {year}.",
                        }
                        for year in (2019, 2023)
                    ],
                    *[
                        {
                            "id": f"spri_{year}", "kind": "raster", "mode": "continuous", "name": f"sPRI {year}",
                            "year": year, "src": f"05_Spectral_Indices/sPRI_{year}_SIRGAS_UTM.tif",
                            "vmin": 0.42, "vmax": 0.50, "ramp": "viridis", "unit": "índice", "decimals": 3,
                            "source": SENTINEL_SRC,
                            "description": f"sPRI = (PRI + 1) / 2, com PRI = (B02 − B03) / (B02 + B03), {year}.",
                        }
                        for year in (2019, 2023)
                    ],
                ],
            },
            {
                "id": "modis",
                "collapsed": True,
                "title": "Validação MODIS GPP (500 m)",
                "layers": [
                    {
                        "id": f"gpp_{year}", "kind": "raster", "mode": "continuous", "name": f"MODIS GPP jun–ago {year}",
                        "year": year, "src": f"04_MODIS_Validation/MODIS_GPP_{year}_JunAug_APA.tif",
                        "vmin": 0.017, "vmax": 0.061, "ramp": "gpp", "unit": "kg C m⁻² estação⁻¹", "decimals": 3,
                        "max_px": None,
                        "source": "NASA LP DAAC — MOD17A2H (Google Earth Engine)",
                        "description": f"Produtividade Primária Bruta acumulada no inverno de {year}, "
                                       "referência independente para validar o proxy.",
                    }
                    for year in (2019, 2023)
                ],
            },
        ],
    },
]


# -----------------------------------------------------------------------------
# UTILITÁRIOS
# -----------------------------------------------------------------------------
def fix_mojibake(text):
    """Corrige textos UTF-8 lidos como Latin-1 (ex.: 'ConservaÃ§Ã£o')."""
    if isinstance(text, str) and ("Ã" in text or "Â" in text):
        try:
            return text.encode("latin1").decode("utf8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return text
    return text


def ascii_lower(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()


def describe_crs(crs):
    if crs is None:
        return "não definido"
    crs = CRS.from_user_input(crs.to_wkt() if hasattr(crs, "to_wkt") else crs)
    epsg = crs.to_epsg()
    return f"{crs.name} (EPSG:{epsg})" if epsg else crs.name


def read_vector(path):
    gdf = gpd.read_file(path)
    gdf["geometry"] = shapely.force_2d(gdf.geometry.values)
    return gdf


def _polygonal(geom):
    fixed = shapely.make_valid(geom, method="structure", keep_collapsed=False)
    if fixed.geom_type == "Polygon":
        return fixed
    polygons = []
    for part in shapely.get_parts(fixed):
        # coleções ainda podem trazer linhas/pontos residuais da correção
        polygons.extend(p for p in shapely.get_parts(part) if p.geom_type == "Polygon")
    return MultiPolygon(polygons)


def make_polygonal(geom):
    """Corrige a geometria mantendo só a parte poligonal (sem linhas/pontos residuais)."""
    if isinstance(geom, BaseGeometry):
        return _polygonal(geom)
    return np.array([_polygonal(g) for g in geom], dtype=object)


def drop_small_parts(geom, min_area_m2):
    """Remove partes e buracos menores que min_area_m2 (geometria em CRS métrico)."""
    kept = []
    for part in shapely.get_parts(geom):
        if part.area < min_area_m2:
            continue
        holes = [ring for ring in part.interiors if Polygon(ring).area >= min_area_m2]
        kept.append(Polygon(part.exterior, holes))
    return MultiPolygon(kept)


def write_geojson(gdf, path):
    gdf = gdf.to_crs(4326)
    if os.path.exists(path):
        os.remove(path)
    # sem RFC7946: combinado com COORDINATE_PRECISION ele degenera slivers em
    # linhas/pontos e grava GeometryCollection, que quebra a consulta por ponto
    gdf.to_file(path, driver="GeoJSON", COORDINATE_PRECISION=5, WRITE_BBOX="YES")
    # O driver do GDAL grava com indentação; regrava compacto para reduzir o download
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))


def hex_to_rgb(color):
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def build_lut(stops, levels):
    """Interpola a rampa em `levels` cores RGB distintas (necessário para a consulta por pixel)."""
    stops_rgb = np.array([hex_to_rgb(s) for s in stops], dtype=float)
    positions = np.linspace(0, 1, len(stops))
    t = np.linspace(0, 1, levels)
    lut = np.stack([np.interp(t, positions, stops_rgb[:, c]) for c in range(3)], axis=1).round().astype(int)
    seen = set()
    for i in range(levels):
        rgb = tuple(lut[i])
        while rgb in seen:
            rgb = (rgb[0], rgb[1], min(255, rgb[2] + 1) if rgb[2] < 255 else rgb[2] - 1)
        seen.add(rgb)
        lut[i] = rgb
    return ["#%02X%02X%02X" % tuple(c) for c in lut]


# -----------------------------------------------------------------------------
# CONSTRUTORES DE VETORES
# -----------------------------------------------------------------------------
def build_apa_boundary(spec, src_path, ctx):
    gdf = read_vector(src_path).to_crs(UTM_23S)
    geom = make_polygonal(gdf.union_all())
    ctx["apa_utm"] = geom
    out = gpd.GeoDataFrame(
        {"nome": ["APA de Itupararanga"], "area_km2": [round(geom.area / 1e6, 2)]},
        geometry=[geom], crs=UTM_23S,
    )
    fields = [["nome", "Unidade", "text"], ["area_km2", "Área", "km2"]]
    return out, {"fields": fields}


def build_apa_zones(spec, src_path, ctx):
    gdf = read_vector(src_path)
    gdf["Name"] = gdf["Name"].map(fix_mojibake)

    def zone_code(name):
        n = ascii_lower(name)
        for key, code in (("biodiversidade", "ZCB"), ("recursos", "ZCRH"), ("consolidada", "ZOC"),
                          ("diversificada", "ZOD"), ("rural", "ZOR")):
            if key in n:
                return code
        raise ValueError(f"Zona não reconhecida: {name}")

    gdf["zona"] = gdf["Name"].map(zone_code)
    gdf = gdf.to_crs(UTM_23S)
    gdf["geometry"] = make_polygonal(gdf.geometry.values)
    dissolved = gdf.dissolve(by="zona").reset_index()
    dissolved["geometry"] = make_polygonal(dissolved.geometry.simplify(10, preserve_topology=True).values)
    apa_area = ctx["apa_utm"].area
    dissolved["nome"] = dissolved["zona"].map(lambda c: ZONES[c][0])
    dissolved["area_km2"] = (dissolved.geometry.area / 1e6).round(2)
    dissolved["pct_apa"] = (dissolved.geometry.area / apa_area * 100).round(1)
    order = list(ZONES)
    dissolved = dissolved.sort_values("zona", key=lambda s: s.map(order.index))
    out = dissolved[["zona", "nome", "area_km2", "pct_apa", "geometry"]]
    legend = {
        "type": "categorical",
        "classes": [
            {"value": code, "label": f"{code} — {label}", "color": color,
             "area_km2": float(out.loc[out.zona == code, "area_km2"].sum()),
             "pct": float(out.loc[out.zona == code, "pct_apa"].sum())}
            for code, (label, color) in ZONES.items()
        ],
    }
    fields = [["nome", "Zona", "text"], ["zona", "Sigla", "text"], ["area_km2", "Área", "km2"],
              ["pct_apa", "Parcela da APA", "pct"]]
    return out, {"fields": fields, "categorize": {"field": "zona", "colors": {c: v[1] for c, v in ZONES.items()}},
                 "legend": legend}


def build_municipalities(spec, src_path, ctx):
    apa = ctx["apa_utm"]
    apa_wgs = gpd.GeoSeries([apa], crs=UTM_23S).to_crs(4326)
    gdf = gpd.read_file(src_path, bbox=tuple(apa_wgs.total_bounds))
    gdf["geometry"] = shapely.force_2d(gdf.geometry.values)
    gdf = gdf.to_crs(UTM_23S)
    gdf["geometry"] = make_polygonal(gdf.geometry.values)
    inside = gdf.geometry.intersection(apa)
    gdf["area_apa_km2"] = (inside.area / 1e6).round(2)
    gdf = gdf[gdf["area_apa_km2"] >= 1.0].copy()
    inside = inside.loc[gdf.index]
    gdf["pct_apa"] = (inside.area / apa.area * 100).round(1)
    gdf["nome"] = gdf["nome"].map(fix_mojibake)
    gdf["populacao"] = pd.to_numeric(gdf["populacao"], errors="coerce").astype("Int64")
    gdf["pib"] = pd.to_numeric(gdf["pib"], errors="coerce").astype("Int64")
    label_pts = gpd.GeoSeries(inside.representative_point(), crs=UTM_23S).to_crs(4326)
    gdf["label_lat"] = label_pts.y.round(5)
    gdf["label_lon"] = label_pts.x.round(5)
    gdf["geometry"] = gdf.geometry.simplify(25, preserve_topology=True)
    gdf = gdf.sort_values("area_apa_km2", ascending=False)
    out = gdf[["nome", "codigo_ibg", "populacao", "pib", "area_apa_km2", "pct_apa", "label_lat", "label_lon",
               "geometry"]]
    fields = [["nome", "Município", "text"], ["area_apa_km2", "Área dentro da APA", "km2"],
              ["pct_apa", "Parcela da APA", "pct"], ["populacao", "População (Censo 2010)", "int"],
              ["pib", "PIB 2010 (R$ mil)", "int"], ["codigo_ibg", "Código IBGE", "text"]]
    return out, {"fields": fields, "label": {"field": "nome", "lat": "label_lat", "lon": "label_lon"}}


def build_state(spec, src_path, ctx):
    gdf = read_vector(src_path).to_crs(UTM_23S)
    gdf["geometry"] = gdf.geometry.simplify(400, preserve_topology=True)
    gdf["nome"] = gdf["nome"].map(fix_mojibake)
    return gdf[["nome", "geometry"]], {"fields": [["nome", "Estado", "text"]], "identify": False}


def build_forest_outline(spec, src_path, ctx):
    gdf = read_vector(src_path)
    forest = gdf[gdf["CLASS"].map(lambda c: ascii_lower(str(c)) == "floresta")].to_crs(UTM_23S)
    geom = drop_small_parts(make_polygonal(forest.union_all()), 2e4)
    geom = shapely.simplify(geom, 15, preserve_topology=True)
    out = gpd.GeoDataFrame({"classe": ["Floresta nativa"], "ano": [spec["year"]]}, geometry=[geom], crs=UTM_23S)
    return out, {"fields": [["classe", "Mancha florestal", "text"], ["ano", "Ano", "text"]]}


VECTOR_BUILDERS = {
    "apa_boundary": build_apa_boundary,
    "apa_zones": build_apa_zones,
    "municipalities": build_municipalities,
    "state": build_state,
    "forest_outline": build_forest_outline,
}


# -----------------------------------------------------------------------------
# RASTERS
# -----------------------------------------------------------------------------
def warp_to_web_mercator(src_path, categorical, max_px):
    with rasterio.open(src_path) as src:
        data = src.read(1)
        valid = np.ones(data.shape, dtype=bool)
        if np.issubdtype(data.dtype, np.floating):
            valid &= np.isfinite(data) & (data > -1e30)
        if src.nodata is not None and np.isfinite(src.nodata):
            valid &= data != src.nodata

        if categorical:
            arr = np.where(valid, data, 0).astype("uint8")
            nodata, resampling, dtype = 0, Resampling.mode, "uint8"
        else:
            arr = np.where(valid, data, np.nan).astype("float32")
            nodata, resampling, dtype = np.nan, Resampling.average, "float32"

        transform, width, height = calculate_default_transform(
            src.crs, "EPSG:3857", src.width, src.height, *src.bounds)
        if max_px and max(width, height) > max_px:
            factor = max(width, height) / max_px
            transform, width, height = calculate_default_transform(
                src.crs, "EPSG:3857", src.width, src.height, *src.bounds,
                resolution=(abs(transform.a) * factor, abs(transform.e) * factor))

        dst = np.full((height, width), nodata, dtype=dtype)
        reproject(arr, dst, src_transform=src.transform, src_crs=src.crs, src_nodata=nodata,
                  dst_transform=transform, dst_crs="EPSG:3857", dst_nodata=nodata, resampling=resampling)
        meta = {
            "crs": describe_crs(src.crs),
            "native_res": f"{abs(src.res[0]):g} m",
            "dtype": src.dtypes[0],
            "native_size": f"{src.width} × {src.height} px",
        }

    dst_valid = dst != 0 if categorical else np.isfinite(dst)
    rows, cols = np.where(dst_valid.any(axis=1))[0], np.where(dst_valid.any(axis=0))[0]
    r0, r1, c0, c1 = rows[0], rows[-1] + 1, cols[0], cols[-1] + 1
    dst = dst[r0:r1, c0:c1]
    minx = transform.c + c0 * transform.a
    maxy = transform.f + r0 * transform.e
    maxx = minx + dst.shape[1] * transform.a
    miny = maxy + dst.shape[0] * transform.e
    web_res = abs(transform.a)
    return dst, (minx, miny, maxx, maxy), web_res, meta


def save_palette_png(index_array, palette_rgb, path):
    height, width = index_array.shape
    img = Image.frombytes("P", (width, height), np.ascontiguousarray(index_array, dtype="uint8").tobytes())
    flat = [0, 0, 0] + [v for rgb in palette_rgb for v in rgb]
    flat += [0] * (768 - len(flat))
    img.putpalette(flat[:768])
    img.save(path, "PNG", optimize=True, transparency=0)


def build_raster(spec, src_root, out_dir, stats_cache):
    src_path = os.path.join(src_root, spec["src"])
    categorical = spec["mode"] == "categorical"
    max_px = spec.get("max_px", MAX_PX_CATEGORICAL if categorical else MAX_PX_CONTINUOUS)
    data, bounds_3857, web_res, meta = warp_to_web_mercator(src_path, categorical, max_px)

    if categorical:
        max_value = max(spec["classes"])
        palette = [(0, 0, 0)] * max_value
        for value, (_, color) in spec["classes"].items():
            palette[value - 1] = hex_to_rgb(color)
        index = data
        legend = {"type": "categorical", "classes": []}
        stats = {}
        if spec.get("stats"):
            csv_rel, year = spec["stats"]
            if csv_rel not in stats_cache:
                stats_cache[csv_rel] = pd.read_csv(os.path.join(src_root, csv_rel))
            df = stats_cache[csv_rel]
            stats = {int(r.Classe): (float(r.Area_km2), float(r.Pct)) for r in df[df.Ano == year].itertuples()}
        for value, (label, color) in spec["classes"].items():
            entry = {"value": value, "label": label, "color": color}
            if value in stats:
                entry["area_km2"], entry["pct"] = stats[value]
            legend["classes"].append(entry)
    else:
        lut = build_lut(RAMPS[spec["ramp"]], CONTINUOUS_LEVELS)
        vmin, vmax = spec["vmin"], spec["vmax"]
        scaled = (np.clip(data, vmin, vmax) - vmin) / (vmax - vmin)
        index = np.where(np.isfinite(data), 1 + np.round(scaled * (CONTINUOUS_LEVELS - 1)), 0).astype("uint8")
        palette = [hex_to_rgb(c) for c in lut]
        finite = data[np.isfinite(data)]
        legend = {
            "type": "continuous", "vmin": vmin, "vmax": vmax, "stops": RAMPS[spec["ramp"]], "lut": lut,
            "unit": spec["unit"], "decimals": spec["decimals"],
            "data_range": [round(float(finite.min()), 4), round(float(finite.max()), 4)],
        }

    rel_path = f"rasters/{spec['id']}.png"
    save_palette_png(index, palette, os.path.join(out_dir, rel_path))

    to_wgs = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
    west, south = to_wgs.transform(bounds_3857[0], bounds_3857[1])
    east, north = to_wgs.transform(bounds_3857[2], bounds_3857[3])
    return {
        "url": rel_path,
        "bounds": [[round(south, 6), round(west, 6)], [round(north, 6), round(east, 6)]],
        "bounds_3857": [round(v, 2) for v in bounds_3857],
        "width": int(index.shape[1]), "height": int(index.shape[0]),
        "web_res_m": round(web_res, 1),
        "legend": legend,
        "meta": {**meta, "type": f"Raster ({'temático' if categorical else 'contínuo'} · {meta['dtype']})"},
        "size_kb": round(os.path.getsize(os.path.join(out_dir, rel_path)) / 1024),
    }


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--src", default=DEFAULT_SRC, help="Pasta com os dados originais (shapefiles e GeoTIFFs)")
    parser.add_argument("--out", default=DEFAULT_OUT, help="Pasta de saída servida pelo Streamlit")
    args = parser.parse_args()

    if not os.path.isdir(args.src):
        raise SystemExit(f"Pasta de dados não encontrada: {args.src}")

    for sub in ("rasters", "vectors"):
        shutil.rmtree(os.path.join(args.out, sub), ignore_errors=True)
        os.makedirs(os.path.join(args.out, sub), exist_ok=True)

    manifest = {"generated": datetime.now().strftime("%Y-%m-%dT%H:%M"), "articles": [], "layers": {}}
    stats_cache = {}
    ctx = {}

    for article in ARTICLES:
        art_out = {k: article[k] for k in ("id", "title", "subtitle", "citation", "url", "home_layer",
                                           "defaults", "compare")}
        art_out["groups"] = []
        for group in article["groups"]:
            art_out["groups"].append({"id": group["id"], "title": group["title"],
                                      "collapsed": group.get("collapsed", False),
                                      "layers": [layer["id"] for layer in group["layers"]]})
            for spec in group["layers"]:
                src_path = os.path.join(args.src, spec["src"])
                print(f"· {spec['id']:<14} ← {spec['src']}")
                layer = {
                    "id": spec["id"], "name": spec["name"], "kind": spec["kind"], "article": article["id"],
                    "group": group["id"], "year": spec.get("year"),
                }
                if spec["kind"] == "vector":
                    info = gpd.read_file(src_path, rows=1)
                    gdf, extra = VECTOR_BUILDERS[spec["builder"]](spec, src_path, ctx)
                    rel_path = f"vectors/{spec['id']}.geojson"
                    write_geojson(gdf, os.path.join(args.out, rel_path))
                    geom_type = gdf.geom_type.iloc[0]
                    style = dict(spec["style"])
                    if not extra.get("legend"):
                        extra["legend"] = {"type": "line" if style.get("fill") is False else "fill",
                                           "color": style.get("color"), "dashArray": style.get("dashArray")}
                    bounds = gdf.to_crs(4326).total_bounds
                    layer.update({
                        "url": rel_path, "style": style, "fields": extra["fields"],
                        "categorize": extra.get("categorize"), "label": extra.get("label"),
                        "identify": extra.get("identify", True), "legend": extra["legend"],
                        "bounds": [[round(bounds[1], 6), round(bounds[0], 6)], [round(bounds[3], 6), round(bounds[2], 6)]],
                        "meta": {"crs": describe_crs(info.crs), "type": f"Vetor ({geom_type})",
                                 "native_res": "vetorial", "features": int(len(gdf))},
                        "size_kb": round(os.path.getsize(os.path.join(args.out, rel_path)) / 1024),
                    })
                else:
                    layer.update(build_raster(spec, args.src, args.out, stats_cache))
                layer["meta"].update({"file": os.path.basename(spec["src"]), "source": spec["source"],
                                      "description": spec["description"]})
                manifest["layers"][spec["id"]] = layer
                print(f"    {layer['size_kb']:>6} KB")
        manifest["articles"].append(art_out)

    with open(os.path.join(args.out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, separators=(",", ":"))

    total_kb = sum(layer["size_kb"] for layer in manifest["layers"].values())
    print(f"\nManifest com {len(manifest['layers'])} camadas · {total_kb / 1024:.1f} MB em {args.out}")


if __name__ == "__main__":
    main()
