"""Gera o site estatico do portfolio para o GitHub Pages.

Le os mesmos dados que o app Streamlit usa (artigos_data.py, portfolio_data.json
e static/websig/manifest.json) e escreve um index.html autossuficiente na raiz do
repositorio. Assim o conteudo tem uma fonte unica: editar artigos_data.py e rodar

    python tools/build_site.py

atualiza o site e o app juntos.

As imagens sao referenciadas por caminho relativo (nao embutidas em base64), que e
o que faz sentido num site estatico: o navegador cacheia cada arquivo.
"""

import html
import json
import os
import re
import sys
from urllib.parse import quote

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from artigos_data import ARTIGOS  # noqa: E402

SAIDA = os.path.join(RAIZ, "index.html")
MANIFESTO = os.path.join(RAIZ, "static", "websig", "manifest.json")

# Codigo do site no GoatCounter (o subdominio da conta). Vazio = medicao desligada:
# a secao de estatisticas continua funcionando, mostrando so os dados locais.
GOATCOUNTER = ""

STATUS_CORES = {
    "destaque": ("#15803D", "#DCFCE7", "#BBF7D0"),
    "publicado": ("#0369A1", "#E0F2FE", "#BAE6FD"),
    "submissao": ("#B45309", "#FEF3C7", "#FDE68A"),
}

SECOES = [
    ("inicio", "Página Inicial"),
    ("artigos", "Artigos Científicos & Publicações"),
    ("websig", "WebSIG Interativo (APA Itupararanga)"),
    ("ia", "Criações com IA & Produtos"),
    ("consultoria", "Consultoria Ambiental & Tutoria em SIG"),
    ("trajetoria", "Trajetória Profissional & Docência"),
    ("estatisticas", "Estatísticas de Acesso"),
]


def esc(texto):
    return html.escape(str(texto), quote=True)


def inline_md(texto):
    """Mesma conversao usada pelo app: **negrito** e `codigo`."""
    texto = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", texto)
    texto = re.sub(r"`(.+?)`", r"<code>\1</code>", texto)
    return texto


def carregar_dados():
    caminho = os.path.join(RAIZ, "portfolio_data.json")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    raise SystemExit("portfolio_data.json nao encontrado")


def preparar_foto():
    """Recorta a foto de perfil uma vez, em vez de a cada carregamento como no app."""
    destino = os.path.join(RAIZ, "static", "perfil.jpg")
    origem = None
    for nome in ("foto_curriculo1.jpg", "foto_curriculo.jpg"):
        candidato = os.path.join(RAIZ, nome)
        if os.path.exists(candidato):
            origem = candidato
            break
    if origem is None:
        return None
    try:
        from PIL import Image
    except ImportError:
        return None
    im = Image.open(origem)
    w, h = im.size
    if h > w and w >= 800:
        # mesmo enquadramento facial do app.py
        escala = w / 1200.0
        cx, cy, lado = int(380 * escala), int(800 * escala), int(560 * escala)
        esq = max(0, cx - lado // 2)
        topo = max(0, cy - lado // 2)
        im = im.crop((esq, topo, min(w, esq + lado), min(h, topo + lado)))
    elif w > h:
        lado = h
        esq = int((w - lado) / 2)
        im = im.crop((esq, 0, esq + lado, h))
    im = im.resize((450, 450), Image.Resampling.LANCZOS)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    im.convert("RGB").save(destino, format="JPEG", quality=92)
    return "static/perfil.jpg"


# ---------------------------------------------------------------- componentes

def abas(nome, titulos, paineis):
    """Abas em HTML+JS, no lugar de st.tabs."""
    botoes = "".join(
        f'<button class="tab{" on" if i == 0 else ""}" data-tabs="{nome}" data-i="{i}">{t}</button>'
        for i, t in enumerate(titulos))
    corpos = "".join(
        f'<div class="tabpane{" on" if i == 0 else ""}" data-tabs="{nome}" data-i="{i}">{c}</div>'
        for i, c in enumerate(paineis))
    return f'<div class="tabs" role="tablist">{botoes}</div><div class="tabbody">{corpos}</div>'


def cartao_servico(nome, desc, cor):
    return (f'<div class="service-card" style="border-left-color:{cor};">'
            f'<h4 style="color:{cor};margin:0 0 .35rem 0;font-family:Merriweather,serif;">{esc(nome)}</h4>'
            f'<p style="font-size:.88rem;color:#334155;line-height:1.5;margin:0;">{esc(desc)}</p></div>')


# ------------------------------------------------------------------- secoes

def secao_inicio():
    icones = [
        ("artigos", "Artigos Científicos", "Pesquisas, Hipóteses & Produtos",
         "linear-gradient(135deg,#065F46 0%,#10B981 100%)", "rgba(16,185,129,.3)",
         '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>'
         '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>'
         '<path d="M12 7c-1.5-2.2-3.5-3-3.5-3s.5 2.2 1.8 3.5c1 1 1.7 1.5 1.7 1.5"></path>'
         '<path d="M12 7c1.5-2.2 3.5-3 3.5-3s-.5 2.2-1.8 3.5c-1 1-1.7 1.5-1.7 1.5"></path>'
         '<line x1="12" y1="7" x2="12" y2="15"></line>'),
        ("websig", "WebSIG Espacial", "APA Itupararanga & SIG",
         "linear-gradient(135deg,#0369A1 0%,#0284C7 100%)", "rgba(2,132,199,.3)",
         '<polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon>'
         '<line x1="8" y1="2" x2="8" y2="18"></line><line x1="16" y1="6" x2="16" y2="22"></line>'),
        ("ia", "Criações com IA", "Agentes & Modelos ML",
         "linear-gradient(135deg,#4338CA 0%,#7C3AED 100%)", "rgba(124,58,237,.3)",
         '<line x1="12" y1="1" x2="12" y2="4"></line><circle cx="12" cy="1.2" r="1.2" fill="#FFF"></circle>'
         '<rect x="3" y="5" width="18" height="15" rx="4" ry="4"></rect>'
         '<circle cx="8" cy="11" r="2.2" fill="#FFF"></circle><circle cx="16" cy="11" r="2.2" fill="#FFF"></circle>'
         '<line x1="8" y1="16" x2="16" y2="16"></line><line x1="1" y1="12" x2="3" y2="12"></line>'
         '<line x1="21" y1="12" x2="23" y2="12"></line>'),
        ("consultoria", "Consultoria & Tutoria SIG", "Geoprocessamento & Licenciamento",
         "linear-gradient(135deg,#B45309 0%,#F59E0B 100%)", "rgba(245,158,11,.3)",
         '<rect x="2" y="3" width="20" height="13" rx="2" ry="2"></rect>'
         '<path d="M12 6.5c-2 0-3.6 1.5-3.6 3.5 0 2.6 3.6 3.8 3.6 3.8s3.6-1.2 3.6-3.8c0-2-1.6-3.5-3.6-3.5z"></path>'
         '<line x1="12" y1="6.5" x2="12" y2="13.8"></line><line x1="12" y1="16" x2="12" y2="21"></line>'
         '<line x1="8" y1="21" x2="16" y2="21"></line>'),
        ("trajetoria", "Trajetória & Docência", "Memorial, USP & Cursos",
         "linear-gradient(135deg,#1E293B 0%,#475569 100%)", "rgba(71,85,105,.3)",
         '<path d="M22 10v6M2 10l10-5 10 5-10 5z"></path><path d="M6 12v5c3 3 9 3 12 0v-5"></path>'),
    ]
    cartoes = "".join(
        f'<button class="app-icon-card" data-goto="{alvo}" title="Clique para acessar {esc(titulo)}">'
        f'<span class="app-icon-squircle" style="background:{grad};box-shadow:0 4px 12px {sombra};">'
        f'<svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" '
        f'stroke-linecap="round" stroke-linejoin="round">{svg}</svg></span>'
        f'<span class="app-icon-title">{esc(titulo)}</span>'
        f'<span class="app-icon-sub">{esc(sub)}</span></button>'
        for alvo, titulo, sub, grad, sombra, svg in icones)

    pilares = [
        ("#15803D", "🛰️ Geotecnologias & Sensoriamento Remoto",
         "Processamento de dados Sentinel-2 (10 m), Landsat e MODIS em nuvem (Google Earth Engine e Python) "
         "para detecção precoce de degradação florestal funcional invisível ao desmatamento tradicional."),
        ("#0284C7", "🤖 Inteligência Artificial & RAG Científico",
         "Desenvolvimento de agentes conversacionais que explicam artigos com rigor acadêmico, além de modelos "
         "de transição de uso do solo com redes neurais artificiais (ANN-MLP)."),
        ("#D97706", "💼 Consultoria Ambiental & Regularização",
         "Elaboração de EIA/RIMA, PRADs, laudos de cobertura vegetal e valoração de serviços ecossistêmicos "
         "com suporte analítico ao ICMS Ecológico e IVEG."),
    ]
    blocos = "".join(
        f'<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-left:4px solid {cor};'
        f'border-radius:8px;padding:.9rem;">'
        f'<b style="color:#0F172A;font-size:.9rem;">{esc(t)}</b>'
        f'<p style="font-size:.82rem;color:#475569;margin:.3rem 0 0 0;line-height:1.4;">{esc(d)}</p></div>'
        for cor, t, d in pilares)

    return f"""
<div style="margin:1.1rem 0 .6rem 0;">
  <h3 style="font-family:Merriweather,serif;color:#0F172A;margin:0 0 .2rem 0;font-size:1.32rem;">
    Painel de Acesso &amp; Áreas de Atuação</h3>
  <p style="font-size:.9rem;color:#475569;margin:0;">
    Clique diretamente nos ícones abaixo para acessar as pesquisas científicas, geotecnologias e serviços especializados:</p>
</div>
<div class="app-launcher-wrapper"><div class="app-grid">{cartoes}</div></div>
<div style="background:#FFFFFF;border:1px solid #CBD5E1;border-radius:10px;padding:1.4rem 1.8rem;
     margin-top:1.2rem;box-shadow:0 2px 6px rgba(0,0,0,.03);">
  <h4 style="font-family:Merriweather,serif;color:#0F172A;margin:0 0 .5rem 0;font-size:1.15rem;">
    Apresentação &amp; Propósito do Portfólio</h4>
  <p style="font-size:.94rem;color:#334155;line-height:1.6;margin-bottom:.8rem;">
    Este ecossistema digital reúne a produção de pesquisa, inovação geoespacial e soluções ambientais do
    <b>Dr. Jomil Costa Abreu Sales</b>. Com formação interdisciplinar em Biologia, Doutorado em Ciências
    Ambientais e Pós-Doutorado pelo Departamento de Ciências Florestais da <b>ESALQ/USP</b>, sua atuação
    conecta o rigor de publicações científicas de ponta à prestação de serviços técnicos especializados em
    <b>ESG, créditos de carbono, conservação da biodiversidade e segurança hídrica</b>.</p>
  <div class="tri-grid">{blocos}</div>
</div>
{bloco_compartilhar()}
"""


def bloco_figuras(artigo):
    figuras = artigo["figuras"]
    if not figuras:
        return (f'<div style="background:#FFFBEB;border:1.5px dashed #F59E0B;border-radius:10px;'
                f'padding:1.6rem 1.4rem;margin:.6rem 0 1.2rem 0;text-align:center;">'
                f'<div style="font-size:2rem;margin-bottom:.4rem;">🗂️</div>'
                f'<b style="color:#92400E;font-size:1rem;">Figuras ainda não disponíveis</b>'
                f'<p style="font-size:.86rem;color:#78350F;margin:.4rem 0 0 0;line-height:1.5;">'
                f'{esc(artigo.get("figuras_pendentes", ""))}</p></div>')

    aid = artigo["id"]
    pasta = artigo["pasta"].replace("\\", "/")
    quadros = []
    for i, fig in enumerate(figuras):
        metas = "".join(
            f'<div class="metadata-item"><div class="metadata-label">{esc(k)}</div>'
            f'<div class="metadata-val">{esc(v)}</div></div>'
            for k, v in fig["meta"].items())
        fonte = artigo.get("figuras_origem", "")
        fonte_html = ""
        if fonte:
            fonte_html = (f'<div style="font-size:.76rem;color:#64748B;margin-top:.9rem;'
                          f'border-top:1px solid #E2E8F0;padding-top:.6rem;">'
                          f'<b>Fonte:</b> {esc(artigo["referencia"])} {esc(fonte)}</div>')
        quadros.append(
            f'<div class="fig-frame{" on" if i == 0 else ""}" data-fig="{aid}" data-i="{i}">'
            f'<div class="fig-stage">'
            f'<div class="fig-bar"><span>Figura {i + 1} de {len(figuras)}</span>'
            f'<span class="fig-name">{esc(fig["titulo"])}</span></div>'
            f'<img loading="lazy" src="{esc(pasta)}/{esc(fig["arquivo"])}" alt="{esc(fig["titulo"])}" /></div>'
            f'<div class="fig-desc">'
            f'<div class="fig-desc-head"><div style="display:flex;align-items:center;gap:8px;">'
            f'<span style="font-size:1.25rem;">🔎</span>'
            f'<b style="font-size:1.05rem;color:#0F172A;">{esc(fig["titulo"])}</b></div>'
            f'<span class="pill-green">Descrição da figura</span></div>'
            f'<p style="color:#1E293B;font-size:.94rem;line-height:1.65;margin:0;">{esc(fig["descricao"])}</p>'
            f'<div class="metadata-grid">{metas}</div>{fonte_html}</div></div>')

    tiras = "".join(
        f'<button class="film{" on" if i == 0 else ""}" data-film="{aid}" data-i="{i}" '
        f'title="{esc(f["titulo"])}">{i + 1:02d}</button>'
        for i, f in enumerate(figuras))

    return (f'<div class="fig-wrap" data-figwrap="{aid}">{"".join(quadros)}'
            f'<div class="fig-nav">'
            f'<button class="btn" data-figstep="{aid}" data-d="-1">◀ Figura anterior</button>'
            f'<div class="fig-count"><span class="fig-count-txt" data-figcount="{aid}">'
            f'Figura 1 de {len(figuras)}</span></div>'
            f'<button class="btn btn-primary" data-figstep="{aid}" data-d="1">Próxima figura ▶</button></div>'
            f'<p class="mini-label">Seleção rápida (clique no número para alternar):</p>'
            f'<div class="film-strip">{tiras}</div></div>')


def secao_artigos():
    cartoes = []
    for a in ARTIGOS:
        cor_txt, cor_bg, cor_bd = STATUS_CORES[a["status"]]
        cartoes.append(
            f'<button class="art-card{" on" if a is ARTIGOS[0] else ""}" data-art="{a["id"]}">'
            f'<span class="art-top">'
            f'<span class="art-status" style="color:{cor_txt};background:{cor_bg};border-color:{cor_bd};">'
            f'{esc(a["status_label"])}</span>'
            f'<span class="art-num">#{a["id"]}</span></span>'
            f'<span class="art-tema">{esc(a["tema"])}</span>'
            f'<span class="art-cont">{len(a["figuras"])} figura(s) · {len(a["perguntas"])} perguntas</span>'
            f'<span class="art-foot"><span class="art-titulo">{esc(a["titulo"])}</span>'
            f'<span class="art-venue">{esc(a["veiculo"])} · <b>{esc(a["ano"])}</b></span></span>'
            f'</button>')

    dossies = []
    for a in ARTIGOS:
        cor_txt, cor_bg, cor_bd = STATUS_CORES[a["status"]]
        chips = [(a["status_label"], cor_txt, cor_bg, cor_bd),
                 (a["veiculo"], "#334155", "#F1F5F9", "#E2E8F0"),
                 (a["tema"], "#334155", "#F1F5F9", "#E2E8F0")]
        if a.get("financiamento"):
            chips.append((a["financiamento"], "#92400E", "#FEF3C7", "#FDE68A"))
        chips_html = "".join(
            f'<span style="font-size:.74rem;font-weight:700;color:{c};background:{b};'
            f'border:1px solid {d};padding:.2rem .55rem;border-radius:5px;">{esc(t)}</span>'
            for t, c, b, d in chips)
        link = ""
        if a.get("link_url"):
            link = (f'<br><a href="{esc(a["link_url"])}" target="_blank" rel="noopener noreferrer" '
                    f'style="color:#15803D;font-weight:700;">{esc(a["link_label"])} ↗</a>')
        resultados = "".join(f'<li>{inline_md(esc(r))}</li>' for r in a["resultados"])
        soluc = "".join(f'<p>{inline_md(esc(s))}</p>' for s in a["solucao"])
        faq = "".join(
            f'<details class="qa"><summary>{esc(q["pergunta"])}</summary>'
            f'<div class="qa-body"><p>{esc(q["resposta"])}</p></div></details>'
            for q in a["perguntas"])

        dossies.append(f"""
<div class="dossie{' on' if a is ARTIGOS[0] else ''}" data-dossie="{a['id']}">
  <div class="card-head">
    <div class="chips">{chips_html}</div>
    <h3>{esc(a['titulo'])}</h3>
    <p><b>Autores:</b> {esc(a['autores'])}<br><b>Minha participação:</b> {esc(a['meu_papel'])}{link}</p>
  </div>

  <div style="margin:1.3rem 0 .7rem 0;">
    <h4 class="h-serif">🎯 Estrutura Fundamental da Pesquisa: Da Pergunta à Solução Territorial</h4>
    <p class="sub">Síntese executiva dos fundamentos metodológicos, empíricos e práticos que norteiam este estudo:</p>
  </div>
  <div class="pilares">
    <div class="pilar" style="border-left-color:#0284C7;">
      <div class="pilar-h"><span>❓</span><b style="color:#0369A1;">1. A Pergunta Central do Artigo</b></div>
      <div class="quote">"{esc(a['pergunta'])}"</div>
      <p>{esc(a['pergunta_nota'])}</p>
    </div>
    <div class="pilar" style="border-left-color:#D97706;">
      <div class="pilar-h"><span>⚠️</span><b style="color:#B45309;">2. O Problema Levantado &amp; Hipótese</b></div>
      <div class="txt"><b>O Problema Territorial:</b> {esc(a['problema'])}</div>
      <div class="hip"><b>A Hipótese Científica:</b> {esc(a['hipotese'])}</div>
    </div>
    <div class="pilar" style="border-left-color:#15803D;">
      <div class="pilar-h"><span>📊</span><b style="color:#15803D;">3. Os Resultados Obtidos (Evidências)</b></div>
      <ul class="lista">{resultados}</ul>
    </div>
    <div class="pilar" style="border-left-color:#0D9488;">
      <div class="pilar-h"><span>💡</span><b style="color:#0F766E;">4. A Solução para o Problema</b></div>
      <div class="txt">{soluc}</div>
    </div>
  </div>

  <div class="rule">
    <h4 class="h-serif">🗺️ Figuras &amp; Produtos Cartográficos do Artigo</h4>
    <p class="sub">A figura ativa é exibida em alta resolução. Use os botões abaixo dela para navegar entre
       as figuras do estudo e ler a descrição correspondente.</p>
  </div>
  {bloco_figuras(a)}

  <div class="rule">
    <div style="display:flex;align-items:center;gap:8px;">
      <span style="font-size:1.35rem;">💬</span>
      <h4 class="h-serif" style="margin:0;">Perguntas frequentes sobre este artigo</h4>
    </div>
    <p class="sub">Clique em uma pergunta para ver a resposta. O conteúdo foi redigido a partir do próprio
       artigo — números, fórmulas e conclusões vêm do texto publicado.</p>
  </div>
  {faq}
</div>""")

    return f"""
<div class="banner" style="border-left-color:#15803D;">
  <h2>📚 Artigos Científicos &amp; Dossiês de Pesquisa</h2>
  <p>Conheça abaixo as pesquisas e publicações científicas, estruturadas sob a ótica executiva de
     <b>Pergunta Central, Problema &amp; Hipótese, Resultados Obtidos e Soluções Propostas</b>,
     com navegação pelas figuras originais de cada estudo.</p>
</div>
<p class="mini-label">Selecione a publicação para visualizar o dossiê &amp; as figuras do estudo:</p>
<div class="art-grid">{''.join(cartoes)}</div>
{''.join(dossies)}
"""


def tabela_metadados():
    if not os.path.exists(MANIFESTO):
        return ('<p class="sub">A tabela é montada a partir de <code>static/websig/manifest.json</code>, '
                'gerado por <code>tools/build_websig.py</code>.</p>')
    with open(MANIFESTO, "r", encoding="utf-8") as f:
        man = json.load(f)
    colunas = ["Camada", "Grupo", "Arquivo original", "Tipo", "CRS original (lido do arquivo)",
               "Resolução original", "Fonte primária", "Descrição"]
    linhas = []
    for art in man["articles"]:
        for grupo in art["groups"]:
            for lid in grupo["layers"]:
                cam = man["layers"][lid]
                m = cam["meta"]
                valores = [cam["name"], grupo["title"], m["file"], m["type"], m["crs"],
                           m["native_res"], m["source"], m["description"]]
                linhas.append("<tr>" + "".join(f"<td>{esc(v)}</td>" for v in valores) + "</tr>")
    cab = "".join(f"<th>{esc(c)}</th>" for c in colunas)
    return (f'<div class="tbl-wrap"><table class="tbl"><thead><tr>{cab}</tr></thead>'
            f'<tbody>{"".join(linhas)}</tbody></table></div>')


def secao_websig():
    mapa = ('<iframe class="sig-frame" src="websig/map.html" title="WebSIG interativo da APA de Itupararanga" '
            'loading="lazy"></iframe>'
            '<p class="caption">Ligue e desligue camadas no painel à esquerda (os dados carregam sob demanda, '
            'sem recarregar a página). Clique em qualquer ponto para consultar os valores das camadas ativas '
            'e use <b>Comparar</b> para a cortina 2019 × 2023.</p>')

    def figura(arquivo, titulo=None, largura="1050px"):
        cap = f'<h5 class="fig-h5">{esc(titulo)}</h5>' if titulo else ""
        return (f'{cap}<div class="plate"><img loading="lazy" src="{esc(arquivo)}" '
                f'style="max-width:{largura};" alt="{esc(titulo or arquivo)}" /></div>')

    grupos = [
        ("Resumo Gráfico (Graphical Abstract)",
         figura("Image_abstract_REV.png", largura="1100px") +
         '<div class="notes"><b>Destaques do Resumo Gráfico:</b><ul>'
         '<li><b>Pipeline Espectral:</b> Sentinel-2 L2A (10 m) com cálculo simultâneo de biomassa verde (NDVI) '
         'e eficiência fotoquímica do uso da luz (sPRI).</li>'
         '<li><b>Achado Central:</b> Persistência de 91,8% da cobertura vegetal total (e 96% da floresta nativa), '
         'contrastando com retração de <b>-21,5%</b> nas áreas de alto potencial de fixação de CO₂ '
         '(de 200,8 km² para 157,7 km²).</li>'
         '<li><b>Simulação 2028:</b> Pelo modelo MOLUSCE / CA-Markov, o alto potencial cai para 145,2 km².</li>'
         '<li><b>Validação MODIS GPP:</b> Correlação significante com Produtividade Primária Bruta '
         '(r = 0,66 a 0,71; ρ = 0,74 a 0,75; p &lt; 0,001).</li></ul></div>'),
        ("Figura 1: Área de Estudo & Zoneamento da APA",
         figura("Figure_01.png") +
         '<div class="notes"><b>Descrição Cartográfica da Figura 1:</b><ul>'
         '<li><b>Enquadramento Geográfico:</b> Localização da APA de Itupararanga (938,31 km²) no contexto do '
         'Estado de São Paulo e Região Metropolitana de Sorocaba.</li>'
         '<li><b>ZCB (Zona de Conservação da Biodiversidade — verde):</b> remanescentes contínuos mais '
         'preservados de Mata Atlântica ao sul da APA.</li>'
         '<li><b>ZCRH (Conservação de Recursos Hídricos — roxo):</b> faixa de proteção dos afluentes e do corpo '
         'da Represa de Itupararanga.</li>'
         '<li><b>ZOR (Ocupação Rural — azul claro):</b> predomínio de agricultura familiar e olericultura.</li>'
         '<li><b>ZOD e ZOC:</b> centros urbanos de Ibiúna, São Roque e núcleos consolidados.</li></ul></div>'),
        ("Figuras 2, 3 e 4: Cobertura da Terra (2019, 2023 & Projeção 2028)",
         figura("Figure_02.png", "Figura 2: Dinâmica Espaço-Temporal de Uso e Cobertura (2019 vs. 2023)") +
         '<div class="duo">' +
         figura("Figure_03.png", "Figura 3: Projeção Preditiva para 2028 (MOLUSCE)", "100%") +
         figura("Figure_04s.png", "Figura 4: Comparativo Quantitativo de Áreas (km²)", "100%") + '</div>'),
        ("Figuras 5, 6 e 7: Potencial de Fluxo de CO₂ (2019, 2023 & 2028)",
         figura("Figure_05.png", "Figura 5: Classes de Potencial de Fluxo de CO₂ (2019 vs. 2023)") +
         '<div class="duo">' +
         figura("Figure_06.png", "Figura 6: Projeção de Fluxo de CO₂ para 2028", "100%") +
         figura("Figure_07.png", "Figura 7: Distribuição das Classes de Carbono (km²)", "100%") + '</div>'),
        ("Figuras 8 e 9: Validação Cruzada com MODIS GPP",
         '<div class="duo">' +
         figura("Figure_08.png", "Figura 8: Produtividade Primária Bruta (MODIS GPP 500 m)", "100%") +
         figura("Figure_09.png", "Figura 9: Regressão Estatística & Pureza Vegetal", "100%") + '</div>'
         '<div class="notes"><b>Síntese da Validação Cruzada:</b><ul>'
         '<li><b>2019:</b> Pearson r = 0,705 | Spearman ρ = 0,743 (p &lt; 0,001, n = 3.685 pixels).</li>'
         '<li><b>2023:</b> Pearson r = 0,662 | Spearman ρ = 0,748 (p &lt; 0,001, n = 3.749 pixels).</li>'
         '<li>O gradiente de cores reflete a pureza vegetal do pixel (≥ 70%), confirmando forte aderência '
         'biofísica.</li></ul></div>'),
    ]
    seletor = "".join(
        f'<button class="chip{" on" if i == 0 else ""}" data-atlas="{i}">{esc(t)}</button>'
        for i, (t, _) in enumerate(grupos))
    paineis = "".join(
        f'<div class="atlas-pane{" on" if i == 0 else ""}" data-atlas="{i}">{c}</div>'
        for i, (_, c) in enumerate(grupos))
    atlas = (f'<h3 class="h-serif">🗺️ Atlas Cartográfico &amp; Figuras Oficiais do Artigo</h3>'
             f'<p class="sub">Abaixo estão reunidos todos os produtos cartográficos e gráficos finalizados que '
             f'compõem o corpo do manuscrito da APA de Itupararanga:</p>'
             f'<div class="chips-row">{seletor}</div>{paineis}')

    citacao = """
<div class="cite-card">
  <div class="cite-head">
    <span>Citação Oficial do Repositório de Dados Geoespaciais</span>
    <span class="pill-amber">DADOS ABERTOS (PRE-PUBLICATION)</span>
  </div>
  <p class="sub">Como o manuscrito científico principal encontra-se em fase final de publicação (pós-revisão
     por pares), utilize a referência bibliográfica e o identificador digital provisório abaixo para citação
     e reprodutibilidade do conjunto de dados geoespaciais:</p>
  <div class="cite-box">
    <b>SALES, J. C. A.; NICOMEDES, N. P.; SILVA, D. C. C.; LOURENÇO, R. W.</b> Dataset: Spatial Modeling of
    Carbon Flux and Multi-temporal Land Cover Dynamics in the Itupararanga Environmental Protection Area
    (SP, Brazil). <i>Research Data Repository</i>, 2024.
  </div>
</div>"""

    meta = ('<h3 class="h-serif">📊 Tabela de Metadados Geoespaciais do Repositório</h3>'
            '<p class="sub">Camadas vetoriais e matriciais publicadas no WebSIG. O CRS é lido diretamente de '
            'cada arquivo original; no mapa, todas são reprojetadas para Web Mercator.</p>'
            + tabela_metadados() + citacao)

    return f"""
<div class="banner" style="border-left-color:#15803D;">
  <h2>WebSIG &amp; Produtos Cartográficos da APA de Itupararanga (938,31 km²)</h2>
  <p>Visualizador interativo de shapefiles e rasters dos artigos, figuras oficiais do manuscrito e metadados.</p>
</div>
{abas('sig', ['WebSIG Interativo (Camadas dos Artigos)', 'Mapas Prontos do Artigo (Figuras Oficiais)',
              'Tabela de Metadados &amp; Citação do Repositório'], [mapa, atlas, meta])}
"""


def painel_forest_lab():
    """Item 1 da secao de IA: o simulador Forest Lab embutido e documentado."""
    grupos = [
        ("1", "Pioneiras (gramíneas, <i>Cecropia</i>, <i>Trema</i>)", "ano 0 (banco de sementes)",
         "≥ 28%", "15–35", "20", "0,35"),
        ("2", "Arbustos pioneiros (<i>Piper</i>, <i>Miconia</i>, <i>Vismia</i>)", "ano 2",
         "≥ 15%", "15–40", "6", "0,40"),
        ("3", "Secundárias iniciais (<i>Inga</i>, <i>Schizolobium</i>)", "ano 3",
         "≥ 12%", "40–80", "26", "0,52"),
        ("4", "Secundárias tardias (<i>Cedrela</i>, <i>Virola</i>)", "ano 4",
         "qualquer", "100–220", "34", "0,65"),
        ("5", "Clímax (<i>Carapa</i>, <i>Manilkara</i>, <i>Hymenaea</i>)", "ano 5",
         "qualquer", "300–600", "43", "0,80"),
        ("6", "Arvoretas e palmeiras tolerantes à sombra (<i>Euterpe</i>, <i>Geonoma</i>)", "ano 10",
         "≤ 30%", "70–140", "10", "0,45"),
        ("7", "Emergentes (<i>Bertholletia</i>, <i>Dinizia</i>, <i>Cariniana</i>)", "ano 12",
         "qualquer", "500–900", "68", "0,72"),
    ]
    linhas_grupos = "".join(
        f"<tr><td style='text-align:center;font-weight:800;color:#15803D;'>{n}</td><td>{g}</td>"
        f"<td>{entra}</td><td style='text-align:center;'>{luz}</td>"
        f"<td style='text-align:center;'>{vida}</td><td style='text-align:center;'>{alt}</td>"
        f"<td style='text-align:center;'>{dens}</td></tr>"
        for n, g, entra, luz, vida, alt, dens in grupos)

    galeria = [
        ("01_floresta_3d.jpg", "Floresta 3D no ano 150",
         "Dossel fechado de floresta secundária tardia com o corredor ripário serpenteando a paisagem."),
        ("02_lidar.jpg", "Modo Nuvem LiDAR no ano 150",
         "Varredura aerotransportada emulada com cerca de 420 mil retornos, colorida por altura (Z)."),
        ("03_borda_urbana.jpg", "Efeito de borda urbana no ano 300",
         "Zona de contato com a expansão urbana a leste, onde a biomassa cai cerca de 48%."),
        ("04_zona_urbana.jpg", "Zona urbana no ano 300",
         "Malha viária, edifícios iluminados, casas e a fumaça da fábrica carregada pelo vento."),
    ]
    figs = "".join(
        f'<figure class="flab-shot"><img src="static/forest_lab/{arq}" loading="lazy" '
        f'alt="{tit}" width="1400" height="787">'
        f'<figcaption><b>{tit}.</b> {leg}</figcaption></figure>'
        for arq, tit, leg in galeria)

    referencias = [
        "Botkin, D. B., Janak, J. F., &amp; Wallis, J. R. (1972). Some ecological consequences of a computer "
        "model of forest growth. <i>Journal of Ecology, 60</i>(3), 849–872.",
        "Budowski, G. (1965). Distribution of tropical American rain forest species in the light of "
        "successional processes. <i>Turrialba, 15</i>(1), 40–42.",
        "Chave, J., Réjou-Méchain, M., Búrquez, A., <i>et al.</i> (2014). Improved allometric models to "
        "estimate the aboveground biomass of tropical trees. <i>Global Change Biology, 20</i>(10), 3177–3190.",
        "Chazdon, R. L. (2014). <i>Second growth: The promise of tropical forest regeneration in an age of "
        "deforestation</i>. University of Chicago Press.",
        "Connell, J. H., &amp; Slatyer, R. O. (1977). Mechanisms of succession in natural communities and "
        "their role in community stability and organization. <i>The American Naturalist, 111</i>(982), "
        "1119–1144.",
        "Denslow, J. S. (1987). Tropical rainforest gaps and tree species diversity. <i>Annual Review of "
        "Ecology and Systematics, 18</i>, 431–451.",
        "Finegan, B. (1996). Pattern and process in neotropical secondary rain forests: The first 100 years "
        "of succession. <i>Trends in Ecology &amp; Evolution, 11</i>(3), 119–124.",
        "Guariguata, M. R., &amp; Ostertag, R. (2001). Neotropical secondary forest succession: Changes in "
        "structural and functional characteristics. <i>Forest Ecology and Management, 148</i>(1–3), 185–206.",
        "Köhler, P., &amp; Huth, A. (1998). The effects of tree species grouping in tropical rainforest "
        "modelling: Simulations with the individual-based model FORMIND. <i>Ecological Modelling, "
        "109</i>(3), 301–321.",
        "Laurance, W. F., Lovejoy, T. E., Vasconcelos, H. L., <i>et al.</i> (2002). Ecosystem decay of "
        "Amazonian forest fragments: A 22-year investigation. <i>Conservation Biology, 16</i>(3), 605–618.",
        "Monsi, M., &amp; Saeki, T. (2005). On the factor light in plant communities and its importance for "
        "matter production (original de 1953). <i>Annals of Botany, 95</i>(3), 549–567.",
        "Naiman, R. J., Décamps, H., &amp; McClain, M. E. (2005). <i>Riparia: Ecology, conservation, and "
        "management of streamside communities</i>. Elsevier Academic Press.",
        "Phillips, O. L., &amp; Gentry, A. H. (1994). Increasing turnover through time in tropical forests. "
        "<i>Science, 263</i>(5149), 954–958.",
        "Poorter, L., Bongers, F., Aide, T. M., <i>et al.</i> (2016). Biomass resilience of Neotropical "
        "secondary forests. <i>Nature, 530</i>(7589), 211–214.",
        "Winiwarter, L., Esmorís Pena, A. M., Weiser, H., <i>et al.</i> (2022). Virtual laser scanning with "
        "HELIOS++: A novel take on ray tracing-based simulation of topographic full-waveform 3D laser "
        "scanning. <i>Remote Sensing of Environment, 269</i>, 112772.",
    ]
    lista_ref = "".join(f"<li>{r}</li>" for r in referencias)

    return f"""
<div class="flab-hero">
  <div class="flab-hero-in">
    <span class="flab-kicker">Produto autoral · Versão 1.0.0 · 2026</span>
    <h3>🌳 Forest Lab — Simulador 3D de Crescimento Florestal, Sucessão Ecológica e Interferência Antrópica</h3>
    <p>Mil anos de sucessão florestal tropical em 100 hectares (1.000 m × 1.000 m), calculados e desenhados
       em tempo real dentro do navegador. O simulador compara uma borda ripária natural com duas bordas
       antrópicas — vinhedo/agricultura e expansão urbana — e permite explorar a estrutura da floresta com
       uma nuvem de pontos LiDAR aerotransportada emulada.</p>
    <div class="flab-badges">
      <span>DOI 10.5281/zenodo.23859145</span><span>three.js r128 · WebGL</span>
      <span>Interface PT-BR / EN</span><span>~420 mil retornos LiDAR</span>
      <span>Roda offline após a 1ª carga</span>
    </div>
  </div>
</div>

<div class="flab-acoes">
  <button class="btn btn-primary" data-fullscreen="flab-palco">⛶ Ver em tela cheia</button>
  <button class="btn" data-amplo="1">⤢ Modo amplo</button>
  <a class="btn" href="forest_lab/" target="_blank" rel="noopener">↗ Abrir só o simulador</a>
  <a class="btn" href="https://doi.org/10.5281/zenodo.23859145" target="_blank"
     rel="noopener">Registro no Zenodo</a>
  <a class="btn" href="https://github.com/jomilc/forest-growth-simulator" target="_blank"
     rel="noopener">Código-fonte no GitHub</a>
  <a class="btn" href="https://github.com/jomilc/forest-growth-simulator/blob/main/README.md"
     target="_blank" rel="noopener">Documentação técnica</a>
</div>

<div class="flab-palco" id="flab-palco">
  <iframe class="flab-frame" src="forest_lab/" loading="lazy" allowfullscreen
          title="Forest Lab — simulador interativo de sucessão florestal"></iframe>
</div>
<p class="caption">O simulador é interativo: arraste para girar a câmera, use a roda do mouse para aproximar
   e a barra inferior para percorrer os 1.000 anos. Toda a simulação roda localmente, no seu computador —
   nenhum dado é coletado ou enviado. A primeira carga busca three.js e Tailwind em CDN público e exige
   WebGL; o cálculo completo da história de 1.000 anos leva cerca de 0,6–0,7 s. O botão <b>❓ Ajuda</b>
   dentro do simulador traz o guia completo, e o tópico 7 lista todas as referências.
   Para abrir apenas o simulador, sem o portfólio em volta, use
   <a href="forest_lab/" target="_blank" rel="noopener"><b>jomilc.github.io/portifolio/forest_lab/</b></a>.</p>

<div class="rule">
  <h4 class="h-serif">O que o simulador faz</h4>
  <p class="sub">Um modelo de clareira baseado em indivíduos e dirigido pela luz, no espírito do JABOWA
     (Botkin et al., 1972) e do FORMIND (Köhler &amp; Huth, 1998). Os 3.300 pontos da paisagem são sítios,
     e cada sítio é ocupado por gerações sucessivas de qualquer grupo funcional.</p>
  <div class="split">
    <div class="notes"><ul>
      <li><b>Cinco fases de sucessão (anos 0–1.000):</b> gramíneas rasteiras iniciais (0–3); expansão
          herbácea e pioneira (3–15); floresta secundária e sub-bosque (15–60); floresta secundária
          tardia/clímax (60–150); floresta madura com megaárvores emergentes (150+).</li>
      <li><b>Sete grupos funcionais</b> que se substituem conforme a luz que chega a cada sítio. Árvores
          mortas não voltam: o sítio é recolonizado por plantas novas, na ordem sucessional.</li>
      <li><b>Efeitos de borda:</b> rio meandrante com mata de galeria (borda natural, cerca de −7% de
          biomassa); vinhedo/agricultura a oeste (cerca de −24% na zona de contato); expansão urbana a leste
          (cerca de −48% na zona de contato). As bordas reduzem o crescimento e elevam a mortalidade de
          árvores grandes (Laurance et al., 2002).</li>
      <li><b>Dinâmica de clareiras:</b> quedas naturais de árvores grandes esmagam vizinhas menores e abrem o
          dossel. Há ainda uma ferramenta para abrir uma clareira numa emergente e acompanhar a recuperação —
          ao derrubar a árvore, um bando de araras-azuis e vermelhas abandona a copa, lembrete visual da
          perda de hábitat e biodiversidade.</li>
      <li><b>Detalhe da zona urbana:</b> ao ligar a expansão urbana, a cidade sobe em animação, com malha
          viária e faixas de pedestres, edifícios com janelas acesas, casas de telhado de duas águas e uma
          fábrica cuja fumaça deriva com o vento. São elementos visuais; o cálculo do efeito de borda é o
          mesmo.</li>
      <li><b>Modo Nuvem LiDAR:</b> varredura aerotransportada emulada de alta densidade (cerca de 420.000
          retornos), colorível por espécie e fuste, por altura (Z) ou por solo/vegetação. É uma emulação
          simplificada em navegador, inspirada na abordagem de varredura a laser virtual do HELIOS++
          (Winiwarter et al., 2022) — não executa o HELIOS++.</li>
    </ul></div>
    <div class="aside">
      <b style="color:#15803D;font-size:.92rem;">Variáveis de controle</b>
      <ul><li>Precipitação</li><li>Fertilidade do solo</li><li>Taxa de clareiras</li>
          <li>Densidade foliar</li>
          <li>Pulso de chuva de 6 s, com formação de nuvens e ganho modesto de crescimento</li></ul>
      <b style="color:#15803D;font-size:.92rem;display:block;margin-top:.9rem;">Métricas e gráficos</b>
      <ul><li>Evolução de cada grupo ao longo de 1.000 anos</li>
          <li>Crescimento diamétrico (cm/ano) e mortalidade (%/ano) por grupo, com média móvel de 15 anos</li>
          <li>Cobertura de dossel, a partir do modelo de luz</li>
          <li>Perfil vertical LiDAR e altura máxima</li>
          <li>Biomassa acima do solo (AGB, Mg/ha) pela alometria pantropical de Chave et al. (2014)</li></ul>
      <b style="color:#15803D;font-size:.92rem;display:block;margin-top:.9rem;">Câmeras predefinidas</b>
      <ul><li>Isométrica, nadir (ALS), borda urbana, borda rural, corredor ripário e sub-bosque</li></ul>
    </div>
  </div>
</div>

<div class="rule">
  <h4 class="h-serif">Registros da simulação</h4>
  <p class="sub">Capturas da versão 1.0.0, depositada no Zenodo.</p>
  <div class="flab-galeria">{figs}</div>
</div>

<div class="rule">
  <h4 class="h-serif">Modelo de crescimento</h4>
  <details class="qa"><summary>Luz, recrutamento e os sete grupos funcionais</summary>
    <div class="qa-body">
      <p><b>Luz.</b> A área foliar de cada copa é distribuída sobre uma grade de 40 m e em camadas de 5 m de
         altura, da base da copa até o topo. A luz abaixo de uma dada altura segue a lei de Lambert–Beer,
         <code>L = exp(−k · IAF acima)</code>, com <code>k = 0,5</code> (Monsi &amp; Saeki, 1953/2005). No
         chão da floresta madura a luz cai para cerca de 3%.</p>
      <p style="margin-top:.7rem;"><b>Recrutamento.</b> Um sítio vazio é recolonizado conforme a luz que
         chega ao solo (facilitação e tolerância; Connell &amp; Slatyer, 1977). Seguindo o padrão de
         "composição florística inicial" (Finegan, 1996), árvores de estágios mais tardios podem se
         estabelecer entre as pioneiras já nos primeiros anos, mas crescem devagar enquanto sombreadas.</p>
      <div class="tbl-wrap" style="margin-top:.9rem;"><table class="tbl">
        <thead><tr><th>#</th><th>Grupo (gêneros de exemplo)</th><th>Entra em</th><th>Luz no solo</th>
          <th>Longevidade (anos)</th><th>Altura máx. (m)</th><th>Densidade da madeira (g/cm³)</th></tr></thead>
        <tbody>{linhas_grupos}</tbody>
      </table></div>
      <p style="margin-top:.8rem;font-size:.85rem;color:#64748B;">Agrupamento segundo Budowski (1965),
         Finegan (1996) e Chazdon (2014). Cada sítio tem um grupo "de origem" — o pool de espécies da
         paisagem — e é recolonizado sobretudo por ele, com chance menor para os demais (chuva de sementes).
         Numa clareira dentro da floresta (solo iluminado, entorno sombreado), o sol direto quebra a dormência
         do banco de sementes do solo e pioneiras podem germinar em qualquer sítio, produzindo o pulso de
         colonizadoras (Finegan, 1996; Denslow, 1987).</p>
    </div>
  </details>
  <details class="qa"><summary>Crescimento, persistência das pioneiras e sub-bosque sob as emergentes</summary>
    <div class="qa-body">
      <p><b>Crescimento.</b> A altura cresce rumo ao máximo do grupo (curva monomolecular). O crescimento
         desacelera sob a sombra de árvores mais altas (supressão) e com solo pobre ou estresse de borda. O
         raio da copa segue a altura alometricamente. Alturas nunca diminuem.</p>
      <p style="margin-top:.7rem;"><b>Pioneiras e arbustos persistem a pleno sol.</b> Enquanto uma pioneira ou
         arbusto pioneiro recebe ao menos 70% da luz plena no topo, ela não morre por senescência,
         mortalidade de fundo ou estresse de borda. Ela desaparece apenas quando árvores mais altas começam a
         sombreá-la. As únicas exceções são a destruição física: uma árvore grande caindo sobre ela, uma
         clareira aberta pelo usuário, ou a conversão do terreno em cidade ou agricultura. Na execução padrão,
         nenhuma das mortes de pioneiras ou arbustos ao longo de 1.000 anos acontece a pleno sol. O povoamento
         pioneiro começa a declinar por volta dos 20–25 anos, quando as secundárias iniciais o ultrapassam em
         altura, e quase desaparece aos 150 anos — sobrevivendo então só em clareiras e ao longo das bordas,
         como descrito por Denslow (1987) e Laurance et al. (2002).</p>
      <p style="margin-top:.7rem;"><b>Sub-bosque sob as emergentes.</b> A sombra profunda e úmida sob copas
         emergentes grandes (&gt; 45 m) é o melhor hábitat para arvoretas e palmeiras tolerantes à sombra. Sob
         essas copas elas se estabelecem três vezes mais rápido e morrem cerca de três vezes menos. Cerca de
         90 sítios exclusivos de sub-bosque ficam próximos às emergentes. O resultado: o sub-bosque maduro
         (anos 300–1.000) abriga cerca de 890 plantas em vez de cerca de 700 (+25%), com aproximadamente o
         dobro de plantas sob cada emergente grande. Ele também é mais estável — cerca de 1,6% das plantas são
         substituídas por ano, e a variação de um ano para o outro fica em torno de 0,5%.</p>
    </div>
  </details>
  <details class="qa"><summary>Mortalidade, biomassa e calibração</summary>
    <div class="qa-body">
      <p><b>Mortalidade (demais casos).</b></p>
      <ul class="lista" style="margin-top:.5rem;">
        <li>Mortalidade de fundo de 0,4–4% ao ano, conforme o grupo e escalonada pelo controle de "taxa de
            clareiras". Florestas tropicais renovam-se a cerca de 1–2% ao ano (Phillips &amp; Gentry, 1994).</li>
        <li>Senescência ao fim da longevidade sorteada.</li>
        <li>Sombreamento dos grupos exigentes de luz, que produz autodesbaste.</li>
        <li>Fotoinibição de arvoretas tolerantes à sombra em clareiras grandes (Denslow, 1987).</li>
        <li>Mortalidade adicional perto das bordas.</li>
        <li>Esmagamento de vizinhas menores quando uma árvore grande cai.</li>
      </ul>
      <p style="margin-top:.8rem;"><b>Biomassa.</b> Cada sítio representa uma coorte de árvores reais do seu
         grupo. A AGB usa a alometria pantropical de Chave et al. (2014), com o diâmetro estimado a partir do
         raio da copa.</p>
      <p style="margin-top:.7rem;"><b>Calibração.</b> A execução padrão alcança cerca de 85 Mg/ha aos 60 anos,
         135 Mg/ha aos 100 anos e 210 Mg/ha aos 150 anos; cerca de 260–290 Mg/ha na floresta madura; altura de
         dossel de cerca de 32 m aos 60 anos e emergentes de 68 m após cerca de 400 anos. Esses valores estão
         dentro das faixas relatadas para florestas secundárias e maduras neotropicais (Chave et al., 2014;
         Poorter et al., 2016). As intensidades de borda foram calibradas para que as zonas de contato percam
         cerca de 48% (cidade), 25% (vinhedo) e 7% (rio) da sua biomassa.</p>
      <p style="margin-top:.7rem;"><b>Reprodutibilidade.</b> Todos os sorteios aleatórios vêm de um <i>hash</i>
         de semente fixa, e as intensidades de borda foram calibradas na média de 4 sementes independentes. A
         história inteira de 1.000 anos é calculada de uma vez e recalculada quando o cenário muda — mover a
         linha do tempo para frente e para trás sempre mostra a mesma floresta.</p>
    </div>
  </details>
  <details class="qa"><summary>Requisitos, execução e importação de dados</summary>
    <div class="qa-body">
      <ul class="lista">
        <li><b>Conexão de internet na primeira carga.</b> A página busca three.js r128 e Tailwind CSS 3.4.17
            em CDNs públicos (cdnjs, jsDelivr e cdn.tailwindcss.com).</li>
        <li><b>GPU dedicada ou integrada recente é recomendada.</b> O renderizador reduz a resolução
            automaticamente em máquinas mais lentas.</li>
        <li><b>Funciona em computadores e celulares.</b> Em telas pequenas o layout se adapta: um menu
            compacto de ícones ☰ agrupa todos os controles, a barra de reprodução encolhe para a linha do
            tempo durante a simulação e os avisos de efeito de borda ficam numa aba ⓘ arrastável. Orientação
            paisagem é recomendada; em dispositivos de toque a qualidade gráfica é reduzida automaticamente
            para manter a animação fluida.</li>
        <li><b>Importação de dados.</b> Um arquivo JSON com posições e dimensões de árvores
            (<code>dados_floresta_1000anos.json</code>, por exemplo exportado de um fluxo em Google Colab)
            pode substituir o modelo de sucessão embutido.</li>
        <li><b>Sem instalação, servidor ou conta.</b> Toda a simulação roda localmente no navegador e nenhum
            dado é coletado ou enviado.</li>
      </ul>
    </div>
  </details>
</div>

<div class="rule">
  <h4 class="h-serif">Bibliotecas e referência conceitual</h4>
  <div class="notes"><ul>
    <li><b>three.js r128</b> — biblioteca de renderização 3D, licença MIT. <code>threejs.org</code></li>
    <li><b>Tailwind CSS 3.4.17</b> — estilização da interface, licença MIT. <code>tailwindcss.com</code></li>
    <li><b>HELIOS++</b> — Heidelberg LiDAR Operations Simulator, 3DGeo Research Group, Universidade de
        Heidelberg. Serviu como referência conceitual para o modo Nuvem LiDAR; não é embutido nem
        executado.</li>
  </ul></div>
  <details class="qa" style="margin-top:1rem;"><summary>Referências científicas (15)</summary>
    <div class="qa-body"><ol class="lista" style="margin-left:1.3rem;">{lista_ref}</ol></div>
  </details>
</div>

<div class="cite-card">
  <div class="cite-head"><span>Como citar o Forest Lab</span>
    <span class="pill-green">DOI 10.5281/zenodo.23859145</span></div>
  <p style="font-size:.84rem;color:#475569;margin:0 0 .6rem 0;">Versão 1.0.0 · Zenodo, 2026 · Metadados
     legíveis por máquina em <code>CITATION.cff</code>.</p>
  <div class="cite-box">SALES, J.; C.; A. Forest Lab: Crescimento florestal, sucessão ecológica e
     interferência antrópica. Versão 1.0.0. Zenodo, 2026. DOI: 10.5281/zenodo.23859145. Disponível em:
     https://orcid.org/0000-0001-8722-8398.</div>
  <div class="cite-box" style="margin-top:.6rem;">Sales, J. C. A. (2026). <i>Forest Lab: Forest growth,
     ecological succession and anthropogenic interference</i> (Version 1.0.0) [Computer software]. Zenodo.
     https://doi.org/10.5281/zenodo.23859145</div>
  <p style="font-size:.8rem;color:#64748B;margin:.7rem 0 0 0;">© 2026 Jomil Costa Abreu Sales. Todos os
     direitos reservados. Visualização e uso acadêmico não comercial com citação são permitidos; ver
     <code>LICENSE.txt</code>. Bibliotecas de terceiros permanecem sob as suas próprias licenças.</p>
</div>"""


def secao_ia():
    p1 = """
<h3 class="h-serif">🧠 Agentes Inteligentes &amp; RAG Especializado em Literatura Científica</h3>
<p class="sub">Sistemas de Recuperação Aumentada por Geração (Retrieval-Augmented Generation) projetados para
   superar as limitações de LLMs genéricos no meio acadêmico e ambiental:</p>
<div class="split">
  <div class="notes"><ul>
    <li><b>Rigor Técnico contra Alucinações:</b> o agente é ancorado estritamente em papers, teses, relatórios
        de EIA/RIMA e matrizes de satélite, garantindo que valores numéricos, datas e fórmulas sejam
        reproduzidos com precisão.</li>
    <li><b>Interpretação Multiespectral:</b> capaz de explicar fórmulas de sensoriamento remoto
        (como <code>sPRI × NDVI</code>), correlações estatísticas (Pearson, Spearman) e bandas orbitais
        (Sentinel-2, MODIS).</li>
    <li><b>Aplicação no Portfólio:</b> na seção <b>Artigos Científicos</b>, cada estudo traz um bloco de
        perguntas frequentes com respostas redigidas a partir do próprio artigo — os números, fórmulas e
        conclusões vêm do texto publicado, sem geração automática.</li>
  </ul></div>
  <div class="aside">
    <b style="color:#4F46E5;font-size:.92rem;">Stack Tecnológica do Agente:</b>
    <ul><li>Python 3.10+ / Streamlit</li><li>LangChain / LlamaIndex architecture</li>
        <li>Embeddings vetoriais multilingues</li><li>API Google Gemini integrada</li>
        <li>Base de conhecimento pós-revisão por pares</li></ul>
  </div>
</div>"""
    p2 = """
<h3 class="h-serif">🔮 Modelagem Preditiva com Redes Neurais Artificiais (MOLUSCE / ANN-MLP)</h3>
<p class="sub">Simulação espaço-temporal de mudanças de uso da terra e perdas funcionais de carbono através de
   inteligência artificial geoespacial:</p>
<div class="notes"><ul>
  <li><b>Arquitetura Neural ANN-MLP:</b> treinamento de Redes Neurais Artificiais do tipo Multi-Layer
      Perceptron com 10.000 amostras aleatórias e 500 épocas de calibração, usando variáveis preditoras como
      declividade, distância de estradas e núcleos urbanos.</li>
  <li><b>Autômatos Celulares e Cadeias de Markov (CA-Markov):</b> projeção preditiva probabilística de
      transição de classes para o horizonte de 2028 na APA de Itupararanga.</li>
  <li><b>Diferencial Competitivo:</b> permite que empresas de créditos de carbono e órgãos de fiscalização
      ambiental antecipem áreas de degradação florestal futura antes que o corte raso ocorra.</li>
</ul></div>"""
    p3 = """
<h3 class="h-serif">⚖️ Sistemas de Apoio à Decisão com Lógica Difusa e OWA</h3>
<p class="sub">Algoritmos de inteligência computacional para ponderação de políticas públicas fiscais e
   ambientais:</p>
<div class="notes"><ul>
  <li><b>Modelagem Multicritério OWA:</b> operadores de média ponderada ordenada aplicados ao Índice de
      Vegetação Nativa (IVEG) para simular diferentes graus de atitude decisória (tolerância ao risco e
      trade-offs compensatórios).</li>
  <li><b>Aplicação no ICMS Ecológico:</b> calibração algorítmica para os 645 municípios de São Paulo,
      permitindo ao poder público alinhar transferências financeiras à preservação ecossistêmica de alta
      integridade.</li>
  <li><b>Reconhecimento Internacional:</b> metodologia apresentada no <i>21st Symposium on Systems Analysis
      in Forest Resources (SSAFR 2026, San Sebastián, Espanha)</i>.</li>
</ul></div>"""
    p4 = """
<h3 class="h-serif">🛰️ Automação de Sensoriamento Remoto em Nuvem (GEE &amp; Python)</h3>
<p class="sub">Pipelines automatizados de processamento massivo de imagens de satélite:</p>
<div class="notes"><ul>
  <li><b>Scripts GEE Especializados:</b> rotinas para filtragem automática de nuvens (QA60 Sentinel-2),
      mosaicos temporais sazonais e harmonização espectral.</li>
  <li><b>Validação Cruzada Multi-Sensor:</b> cruzamento em nuvem entre índices de alta resolução espacial
      (Sentinel-2, 10 m) e dados biofísicos globais (MODIS GPP MOD17A2H, 500 m).</li>
  <li><b>Reprodutibilidade Científica:</b> código documentado segundo as melhores práticas de Ciência Aberta
      e princípios FAIR.</li>
</ul></div>"""
    p5 = """
<h3 class="h-serif">💡 Meus Produtos, Modelos &amp; Inovações em Construção</h3>
<p class="sub">Ferramentas sob medida desenvolvidas pelo Dr. Jomil:</p>
<div class="duo">
  <div class="prod" style="border-left-color:#15803D;">
    <b>🌿 Carbon-Insight APA</b>
    <div class="prod-sub" style="color:#15803D;">Web App de Monitoramento de Carbono em Tempo Quase-Real</div>
    <p>Aplicação para identificar talhões de floresta sob estresse hídrico e perda de capacidade
       fotossintética antes do aparecimento de clareiras.</p>
  </div>
  <div class="prod" style="border-left-color:#0284C7;">
    <b>🗺️ Geo-Decision OWA Tool</b>
    <div class="prod-sub" style="color:#0284C7;">Ferramenta de Alocação de Recursos Fiscais Ambientais</div>
    <p>Software interativo para simulação de cenários de repasse de ICMS Ambiental com controle de atitude
       de risco pelo gestor público.</p>
  </div>
</div>"""
    return f"""
<div class="banner" style="border-left-color:#4F46E5;">
  <h2>🤖 Criações com Inteligência Artificial &amp; Produtos Tecnológicos</h2>
  <p>Desenvolvimento de agentes conversacionais inteligentes, modelagem preditiva com redes neurais
     artificiais, algoritmos multicritério com lógica difusa e automação de sensoriamento remoto em nuvem, além do simulador 3D de
     sucessão florestal Forest Lab, que roda interativamente dentro desta página.</p>
</div>
{abas('ia', ['🌳 1. Forest Lab — Simulador 3D', '🧠 2. Agentes RAG Científicos',
             '🔮 3. Redes Neurais &amp; MOLUSCE', '⚖️ 4. Decisão Difusa &amp; OWA',
             '🛰️ 5. Pipelines GEE &amp; Python', '💡 6. Meus Produtos &amp; Projetos'],
            [painel_forest_lab(), p1, p2, p3, p4, p5])}
"""


def secao_consultoria():
    aulas = """
<h3 class="h-serif">Aulas e Tutoria em Geoprocessamento &amp; Sensoriamento Remoto</h3>
<p class="sub">Mentoria personalizada e treinamentos práticos (do básico ao avançado) com estudos de caso
   reais do mercado ambiental:</p>
<div class="duo">
  <div class="service-card">
    <h4 style="color:#15803D;margin-top:0;">Plataformas &amp; Softwares Dominados:</h4>
    <ul class="lista">
      <li><b>QGIS:</b> manipulação vetorial e raster, georreferenciamento, modelagem no MOLUSCE, layout
          cartográfico profissional para órgãos ambientais.</li>
      <li><b>ArcGIS Pro / ArcMap:</b> análise espacial multicritério (AHP), modelagem hidrológica,
          interpolação geoestatística (Krigagem).</li>
      <li><b>Google Earth Engine:</b> processamento massivo em nuvem de coleções Sentinel-2, Landsat
          (séries de 30 anos) e MODIS.</li>
      <li><b>IDRISI / TerrSet:</b> Cadeias de Markov e Autômatos Celulares para projeção de mudanças de uso
          da terra e vulnerabilidade.</li>
      <li><b>Programação Aplicada:</b> Python (GeoPandas, Shapely, Rasterio) e R (sf, lidR para nuvens
          LiDAR).</li>
    </ul>
  </div>
  <div class="service-card" style="border-left-color:#0284C7;">
    <h4 style="color:#0284C7;margin-top:0;">Módulos Práticos &amp; Objetivos:</h4>
    <ul class="lista">
      <li>Elaboração de mapas temáticos padronizados para licenciamento junto à CETESB e ao IBAMA.</li>
      <li>Cálculo de índices biofísicos: NDVI, sPRI, EVI, NBR (cicatrizes de fogo) e temperatura de
          superfície (LST).</li>
      <li>Quantificação e modelagem do fluxo e estoque de carbono para projetos ESG e mercado voluntário.</li>
      <li>Delimitação automatizada de APPs hídricas e de topo de morro segundo a Lei 12.651/2012.</li>
    </ul>
  </div>
</div>"""

    estudos = [
        ("AIA (Avaliação de Impacto Ambiental)",
         "O processo geral e estruturante de identificar, prever e interpretar as consequências que um "
         "empreendimento trará aos meios físico, biótico e socioeconômico. É o ponto de partida técnico de "
         "qualquer estudo.", "#15803D"),
        ("EIA (Estudo de Impacto Ambiental)",
         "O estudo técnico e científico mais complexo e aprofundado do mercado. Exigido obrigatoriamente para "
         "grandes obras de significativo impacto (hidrelétricas, rodovias, mineradoras, portos), detalhando "
         "fauna, flora, dinâmica do solo e impactos sociais.", "#DC2626"),
        ("RIMA (Relatório de Impacto Ambiental)",
         "O resumo executivo do EIA elaborado em linguagem clara, visual e acessível, com infográficos e "
         "mapas, obrigatório para apresentação pública à sociedade e em audiências públicas.", "#D97706"),
        ("EAS (Estudo Ambiental Simplificado)",
         "Estudo técnico de menor complexidade exigido para empreendimentos cujo potencial de poluição ou "
         "degradação ambiental é considerado de baixo ou médio impacto.", "#0284C7"),
        ("RAS (Relatório Ambiental Simplificado)",
         "Análise rápida e objetiva das condições ambientais da região antes da implantação de empresas de "
         "pequeno ou médio porte (por exemplo, loteamentos residenciais compactos e indústrias leves).",
         "#4F46E5"),
        ("PCA (Plano de Controle Ambiental)",
         "Documento contratado na fase de instalação que detalha as medidas e planos executivos da empresa "
         "para mitigar, monitorar e controlar efluentes, resíduos e poluição gerada.", "#059669"),
    ]
    licenca = [
        ("LP (Licença Prévia)",
         "O primeiro selo de aprovação governamental, que atesta a viabilidade ambiental da localização e da "
         "concepção do projeto.", "#15803D"),
        ("LI (Licença de Instalação)",
         "Autoriza o início físico das obras civis, terraplanagem e montagem da estrutura, condicionada ao "
         "cumprimento das exigências da LP.", "#2563EB"),
        ("LO (Licença de Operação)",
         "A licença definitiva que autoriza o negócio a iniciar suas atividades produtivas, mediante "
         "comprovação técnica do cumprimento das etapas anteriores.", "#059669"),
        ("LAS (Licenciamento Ambiental Simplificado)",
         "Processo unificado e ágil em que LP, LI e LO são avaliadas em uma única etapa, para empreendimentos "
         "de baixíssimo potencial poluidor.", "#D97706"),
        ("ASV (Autorização de Supressão de Vegetação)",
         "Documento legal emitido pelo órgão ambiental competente autorizando o corte criterioso de exemplares "
         "arbóreos nativos para implantação da obra.", "#DC2626"),
    ]
    restaura = [
        ("PRAD (Plano de Recuperação de Áreas Degradadas)",
         "Projeto técnico e executivo que define como reverter a degradação do solo, conter processos erosivos "
         "e restabelecer a vegetação nativa com bioengenharia e plantio de mudas pioneiras e secundárias.",
         "#15803D"),
        ("PRADA (Plano de Recuperação de Áreas Degradadas ou Alteradas)",
         "Equivalente ao PRAD, estruturado sob os parâmetros específicos do Código Florestal para "
         "regularização de imóveis e propriedades rurais.", "#059669"),
        ("PTRF (Projeto de Recomposição da Flora)",
         "Plano focado no plantio, adensamento, enriquecimento e manejo silvicultural de espécies nativas "
         "regionais para restauração de áreas abertas ou sub-bosques.", "#2563EB"),
    ]
    rural = [
        ("APP (Área de Preservação Permanente)",
         "Faixas marginais de cursos d'água, nascentes, topos de morro e encostas íngremes protegidas por lei. "
         "Atuação na delimitação precisa em SIG e no projeto de regeneração.", "#0284C7"),
        ("RL (Reserva Legal)",
         "Percentual territorial obrigatório de cobertura florestal nativa que cada imóvel rural deve "
         "preservar: cálculo da área, demarcação no mapa e projeto de compensações quando cabível.", "#15803D"),
        ("CAR (Cadastro Ambiental Rural)",
         "Registro público eletrônico obrigatório para todos os imóveis rurais do Brasil, com elaboração de "
         "shapefiles georreferenciados do mosaico da propriedade.", "#D97706"),
        ("PRA (Programa de Regularização Ambiental)",
         "Termo de compromisso firmado junto ao órgão ambiental estadual para sanar passivos de APP e Reserva "
         "Legal, implementando os planos desenhados pelo consultor.", "#059669"),
    ]
    fiscal = cartao_servico(
        "TAC (Termo de Ajustamento de Conduta)",
        "Acordo jurídico extrajudicial firmado entre a empresa ou proprietário autuado, o órgão ambiental "
        "fiscalizador (CETESB/IBAMA) e o Ministério Público. O consultor realiza a perícia forense, quantifica "
        "o dano real com imagens históricas de satélite e desenha as soluções técnicas executivas "
        "(cronogramas de recuperação e compensações) necessárias para suspender multas e evitar ações civis "
        "públicas.", "#DC2626")

    def lista(titulo, sub, itens):
        return (f'<h3 class="h-serif">{titulo}</h3><p class="sub">{sub}</p>'
                + "".join(cartao_servico(n, d, c) for n, d, c in itens))

    contato = """
<div class="rule">
  <h4 class="h-serif">Solicitar Proposta Técnica ou Agendar Tutoria</h4>
  <p class="sub">Precisa de assessoria técnica especializada para o seu empreendimento, estudo de caso ou
     treinamento em SIG?</p>
  <div class="split">
    <div class="notes"><ul>
      <li><b>E-mail Institucional:</b> <code>jomil.sales@usp.br</code></li>
      <li><b>E-mail Profissional:</b> <code>jomilc@gmail.com</code></li>
      <li><b>Registro Profissional:</b> Biólogo CRBio nº 68816/01-D</li>
    </ul></div>
    <div class="aside" style="display:flex;flex-direction:column;gap:10px;justify-content:center;">
      <a class="btn btn-primary" href="mailto:jomil.sales@usp.br?subject=Solicita%C3%A7%C3%A3o%20de%20Consultoria%20/%20Aulas%20em%20SIG">Enviar mensagem por e-mail</a>
      <a class="btn" href="https://www.linkedin.com/in/jomil-costa/" target="_blank" rel="noopener noreferrer">Acessar perfil no LinkedIn</a>
    </div>
  </div>
</div>"""

    paineis = [
        aulas,
        lista("Estudos e Avaliações de Impacto Ambiental (Diagnósticos)",
              "Elaboração, coordenação técnica e perícia em diagnósticos ambientais de todas as "
              "complexidades:", estudos),
        lista("Licenciamento Ambiental (Etapas Obrigatórias)",
              "Condução e instrução de processos regulatórios junto aos órgãos de fiscalização (CETESB, "
              "IBAMA e secretarias municipais):", licenca),
        lista("Restauração e Recuperação Ecológica",
              "Projetos técnicos com metodologia científica para recomposição de ecossistemas degradados:",
              restaura),
        lista("Regularização Rural (Código Florestal — Lei nº 12.651/2012)",
              "Adequação ambiental completa de propriedades e empreendimentos do agronegócio:", rural),
        '<h3 class="h-serif">Fiscalização, Multas e Acordos Legais</h3>' + fiscal,
    ]
    return f"""
<div class="banner" style="border-left-color:#15803D;">
  <h2>Consultoria Ambiental, Licenciamento &amp; Aulas Especializadas</h2>
  <p>Atuação técnico-científica de alto nível em inteligência geoespacial, diagnósticos de impacto,
     recuperação ecológica e capacitação prática em softwares SIG para profissionais, empresas e acadêmicos.</p>
</div>
{abas('serv', ['Aulas &amp; Tutoria em SIG', 'Estudos e Avaliações de Impacto', 'Licenciamento Ambiental',
               'Restauração Ecológica (PRAD)', 'Regularização Rural', 'Fiscalização, Multas &amp; TAC'],
      paineis)}
{contato}
"""


TRAJETORIA_LINHA = [
    ("2005 — 2009", "Bacharelado e Licenciatura em Ciências Biológicas",
     "Pontifícia Universidade Católica (PUC) · formação em Biologia com habilitação para docência", False),
    ("2007 — 2008", "Iniciação Científica (PIBIC/CNPq)",
     "Primeiro contato com pesquisa aplicada em ecologia e ambiente", False),
    ("2009 — 2011", "Professor · Prefeitura Municipal de Sorocaba",
     "Início da atuação docente na rede pública", False),
    ("2010 — 2012", "Consultor Ambiental autônomo",
     "Habilitação FIA / SEMIL-SP · vistorias de passivos, apoio a TAC do Ministério Público e acompanhamento "
     "de PRADs", False),
    ("2011 — 2012", "Analista Ambiental · MEDRAL Meio Ambiente",
     "Licenciamento completo (LP, LI, LO), EIA/RIMA, RAP e EIV em linhas de transmissão e empreendimentos "
     "imobiliários", False),
    ("2013 — 2015", "Mestrado em Ciências Ambientais · UNESP Sorocaba",
     "Bolsas CNPq e Projeto Novos Talentos (IPT) · geoprocessamento aplicado a bacias hidrográficas", False),
    ("2015 — 2019", "Doutorado em Ciências Ambientais · UNESP",
     "Com período sanduíche em Portugal (programa BE MUNDUS) · análise espacial e indicadores "
     "socioambientais", False),
    ("2018 — 2021", "Professor Adjunto I · Universidade de Sorocaba (UNISO)",
     "SIG, Cartografia Básica, Ecologia e Recuperação de Áreas Degradadas nos cursos de Engenharia Ambiental, "
     "Agronômica, Biologia e Psicologia", False),
    ("2020 — 2023", "Professor de Ensino Médio",
     "Docência em Biologia e Ciências da Natureza", False),
    ("2023 — 2024", "Pós-doutorado · UNESP — ICTS Sorocaba",
     "Análise temporal do fluxo de carbono e modelo preditivo por índices espectrais na APA de Itupararanga",
     False),
    ("ago/2023 — jun/2024", "Pesquisador visitante · Freie Universität Berlin",
     "Instituto de Ciências Geográficas — Sensoriamento Remoto e Geoinformática, com o Prof. Dr. Fabian "
     "Fassnacht · simulação de florestas virtuais e dados LiDAR em R", False),
    ("2024 — atual", "Pós-doutorado em Ciências Florestais · ESALQ/USP",
     "Bolsista FAPESP no projeto DecisionES-BR (cooperação H2020 Marie Curie) · apoio à decisão para serviços "
     "ecossistêmicos sob mudança global", True),
    ("2026 — atual", "MBA em ESG e Negócios Sustentáveis · ESALQ/USP",
     "Formação executiva em ESG, sustentabilidade corporativa e negócios de baixo carbono, conectando a "
     "pesquisa ambiental à tomada de decisão empresarial", True),
]

ATUACAO_CARTOES = [
    ("Sensoriamento remoto &amp; satélites", "sensoriamento",
     "Séries Sentinel-2, Landsat e MODIS processadas em nuvem (Google Earth Engine) para detectar mudança de "
     "cobertura, estresse hídrico e perda de vigor fotossintético antes que virem desmatamento."),
    ("Geoprocessamento &amp; cartografia", "cartografia",
     "Mapeamento e análise espacial em QGIS e ArcGIS: delimitação de APPs e Reserva Legal, geoestatística, "
     "modelagem multicritério (AHP e OWA) e produção cartográfica para órgãos ambientais."),
    ("Licenciamento &amp; perícia ambiental", "licenciamento",
     "EIA/RIMA, RAP, PRAD e laudos de cobertura vegetal; vistorias de passivos ambientais, apoio técnico a "
     "Termos de Ajustamento de Conduta e acompanhamento de autos de infração."),
    ("Docência &amp; formação", "docencia",
     "Professor Adjunto na UNISO e tutor na UNESP e na ESALQ/USP em SIG, Cartografia, Ecologia e Recuperação "
     "de Áreas Degradadas, além de orientações de iniciação científica, mestrado e doutorado."),
    ("Restauração &amp; serviços ecossistêmicos", "restauracao",
     "Projetos de recomposição florestal e priorização de áreas para restauração, integrando serviços "
     "ecossistêmicos à decisão territorial no pós-doutorado DecisionES-BR."),
    ("Carbono florestal &amp; Mata Atlântica", "carbono",
     "Modelagem do potencial de fluxo de CO₂ com índices espectrais e projeção de cenários (MOLUSCE / "
     "CA-Markov) aplicados à APA de Itupararanga e a remanescentes de Mata Atlântica."),
]


def arte_cartao(base):
    for ext in ("jpg", "png", "jpeg", "webp"):
        caminho = os.path.join(RAIZ, "static", "ilustracoes", f"{base}.{ext}")
        if os.path.exists(caminho):
            return f'<img class="arte" loading="lazy" src="static/ilustracoes/{base}.{ext}" alt="" />', True
    svg = os.path.join(RAIZ, "ilustracoes", f"{base}.svg")
    if os.path.exists(svg):
        with open(svg, "r", encoding="utf-8") as f:
            return f.read(), False
    return "", False


def secao_trajetoria(traj):
    linha = "".join(
        f'<div class="tl-item{" atual" if atual else ""}">'
        f'<div class="tl-when">{esc(quando)}</div><div class="tl-mark"><i></i></div>'
        f'<div class="tl-card"><b>{esc(titulo)}</b><span>{esc(detalhe)}</span></div></div>'
        for quando, titulo, detalhe, atual in TRAJETORIA_LINHA)

    cartoes = []
    for titulo, base, texto in ATUACAO_CARTOES:
        arte, tem_imagem = arte_cartao(base)
        rotulo = ('<div class="flip-front-hint">passe o mouse</div>' if tem_imagem
                  else f'<div class="flip-front-label">{titulo}<em>Passe o mouse</em></div>')
        cartoes.append(
            f'<div class="flip-card" tabindex="0"><div class="flip-inner">'
            f'<div class="flip-front"><div class="ilu">{arte}</div>{rotulo}</div>'
            f'<div class="flip-back"><b>{titulo}</b><p>{esc(texto)}</p></div></div></div>')

    pos = "".join(
        f'<div class="clipping-card" style="border-left:4px solid #15803D;">'
        f'<h4>{esc(i["institution"])}</h4>'
        f'<p class="role" style="color:#15803D;">{esc(i["role"])}</p>'
        f'<p class="meta"><b>Projeto:</b> {esc(i["project"])}</p>'
        f'<p class="body">{esc(i["activities"])}</p></div>'
        for i in traj["postdoc_experience"])
    doc = "".join(
        f'<div class="clipping-card" style="border-left:4px solid #2563EB;">'
        f'<h4>{esc(i["institution"])}</h4>'
        f'<p class="role" style="color:#1D4ED8;">{esc(i["role"])}</p>'
        f'<p class="body">{esc(i["scope"])}</p></div>'
        for i in traj["university_teaching"])
    cons = "".join(
        f'<div class="clipping-card" style="border-left:4px solid #D97706;">'
        f'<h4>{esc(i["role"])} ({esc(i["period"])})</h4>'
        f'<p class="body">{esc(i["scope"])}</p></div>'
        for i in traj["environmental_consulting"])

    return f"""
<div class="traj-hero"><div class="traj-hero-inner">
  <span class="traj-kicker">Trajetória</span>
  <h2>Duas décadas entre a floresta, o mapa e a sala de aula</h2>
  <p>Da graduação em Ciências Biológicas ao pós-doutorado em Ciências Florestais na ESALQ/USP, passando pelo
     licenciamento ambiental, pela docência universitária e pela pesquisa em sensoriamento remoto na Alemanha.</p>
</div></div>
<h3 class="sec-title">Formação &amp; atuação em linha do tempo</h3>
<p class="sec-sub">Percurso acadêmico e profissional, do primeiro diploma à pesquisa atual.</p>
<div class="tl">{linha}</div>
<h3 class="sec-title">Áreas de atuação profissional</h3>
<p class="sec-sub">Passe o mouse sobre cada imagem (ou toque, no celular) para ver o que envolve cada frente
   de trabalho.</p>
<div class="flip-grid">{''.join(cartoes)}</div>
<p class="credito">Imagem de capa: banco de imagens livre Unsplash.</p>
<h3 class="sec-title">Detalhamento da experiência</h3>
<p class="sec-sub">Pós-doutorados, docência no ensino superior e atuação no mercado ambiental.</p>
{abas('traj', ['Pós-Doutorados de Ponta', 'Docência no Ensino Superior',
               'Consultoria &amp; Licenciamento Ambiental'], [pos, doc, cons])}
"""


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;0,900;1,400&family=Inter:wght@400;500;600;700;800&display=swap');

*,*::before,*::after{box-sizing:border-box;}
body{margin:0;font-family:Inter,system-ui,sans-serif;color:#1E293B;
     background:linear-gradient(180deg,#EDF4EE 0%,#F5F8F5 45%,#E9F1EB 100%);
     background-attachment:fixed;min-height:100vh;}
img{max-width:100%;}
a{color:#15803D;}

.shell{display:flex;align-items:flex-start;gap:0;max-width:1700px;margin:0 auto;}
.sidebar{width:310px;flex:0 0 310px;background:#EEF4F0;border-right:1.5px solid #D1E0D5;
         padding:1.1rem .95rem 2rem .95rem;min-height:100vh;position:sticky;top:0;
         max-height:100vh;overflow-y:auto;}
.main{flex:1 1 auto;min-width:0;padding:1.5rem 2rem 2.5rem 2rem;}

.profile-card{background:#FFF;border:1px solid #CBD5E1;border-top:4px solid #15803D;border-radius:10px;
              padding:.95rem;margin-bottom:1rem;box-shadow:0 1px 4px rgba(0,0,0,.04);}
.crbio-badge{display:inline-block;background:#ECFDF5;color:#065F46;border:1px solid #A7F3D0;
             padding:.15rem .5rem;border-radius:4px;font-size:.76rem;font-weight:700;}
.avatar{width:86px;height:86px;border-radius:50%;object-fit:cover;border:3px solid #15803D;
        box-shadow:0 2px 8px rgba(0,0,0,.18);flex-shrink:0;margin-right:12px;background:#15803D;}
.mini-cap{font-size:.78rem;font-weight:700;color:#64748B;text-transform:uppercase;
          letter-spacing:.05em;margin:0 0 .4rem 0;}

.nav-btn{display:block;width:100%;text-align:left;padding:.65rem .95rem;border-radius:8px;
         font-size:.90rem;font-weight:600;margin-bottom:.35rem;border:1.5px solid #CBD5E1;
         background:#FFF;color:#334155;cursor:pointer;font-family:inherit;
         transition:all .15s ease-in-out;}
.nav-btn:hover{background:#F1F5F9;border-color:#15803D;color:#15803D;transform:translateX(2px);}
.nav-btn.on{background:#ECFDF5;border-color:#15803D;border-left:6px solid #15803D;color:#065F46;
            font-weight:800;box-shadow:0 2px 4px rgba(21,128,61,.12);}

.links{background:#FFF;border:1px solid #CBD5E1;border-radius:8px;padding:.7rem .9rem;}
.links a{display:flex;align-items:center;padding:.35rem 0;color:#334155;text-decoration:none;
         font-size:.82rem;font-weight:600;border-bottom:1px solid #F1F5F9;}
.links a:last-child{border-bottom:none;}
.links a:hover{color:#15803D;}
.links svg{margin-right:8px;flex-shrink:0;}

.hero-magazine{background:linear-gradient(rgba(14,43,23,.72),rgba(14,43,23,.72)),
               url('https://images.unsplash.com/photo-1511497584788-87676104235f?auto=format&fit=crop&w=1600&q=80') center/cover no-repeat;
               border-radius:12px;padding:1.6rem 2.2rem;margin-bottom:1.4rem;
               box-shadow:0 4px 15px rgba(0,0,0,.08);border-left:6px solid #16A34A;}
.hero-row{display:flex;align-items:center;flex-wrap:wrap;gap:20px;}
.hero-photo{width:104px;height:104px;border-radius:50%;object-fit:cover;border:3.5px solid #FFF;
            box-shadow:0 4px 14px rgba(0,0,0,.25);flex-shrink:0;}
.hero-title{font-family:Merriweather,serif;font-size:2.35rem;font-weight:900;color:#FFF;
            letter-spacing:-.02em;line-height:1.15;}
.hero-subtitle{font-size:1.15rem;color:#F1F5F9;font-weight:500;line-height:1.4;margin-top:.35rem;}

.sec{display:none;}
.sec.on{display:block;}

.banner{background:#FFF;border:1px solid #CBD5E1;border-left:6px solid #15803D;border-radius:10px;
        padding:1.3rem 1.6rem;margin-bottom:1.2rem;box-shadow:0 2px 5px rgba(0,0,0,.03);}
.banner h2{font-family:Merriweather,serif;color:#0F172A;margin:0 0 .3rem 0;font-size:1.65rem;}
.banner p{font-size:.96rem;color:#475569;margin:0;line-height:1.5;}
.h-serif{font-family:Merriweather,serif;color:#0F172A;font-size:1.25rem;margin:0 0 .2rem 0;}
.sub{font-size:.9rem;color:#475569;margin:0 0 .9rem 0;line-height:1.5;}
.mini-label{font-size:.78rem;font-weight:700;color:#64748B;text-transform:uppercase;
            letter-spacing:.04em;margin:.8rem 0 .4rem 0;}
.rule{margin:1.7rem 0 .8rem 0;border-top:2px solid #E2E8F0;padding-top:1.3rem;}
.tri-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:1rem;}
.duo{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;}
.split{display:grid;grid-template-columns:3fr 2fr;gap:16px;align-items:start;}

.app-launcher-wrapper{background:#FFF;border:1px solid #CBD5E1;border-radius:14px;
                      padding:1.4rem 1.6rem;margin:1.2rem 0 1.8rem 0;box-shadow:0 4px 14px rgba(0,0,0,.03);}
.app-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;}
.app-icon-card{background:#FFF;border:1.5px solid #CBD5E1;border-radius:18px;
               padding:1.25rem .75rem 1rem .75rem;display:flex;flex-direction:column;align-items:center;
               text-align:center;box-shadow:0 4px 12px rgba(0,0,0,.04);transition:all .22s ease-in-out;
               min-height:195px;cursor:pointer;font-family:inherit;}
.app-icon-card:hover{transform:translateY(-6px);border-color:#15803D;
                     box-shadow:0 10px 24px rgba(21,128,61,.16);}
.app-icon-card:hover .app-icon-squircle{transform:scale(1.08);}
.app-icon-squircle{width:72px;height:72px;border-radius:20px;display:flex;align-items:center;
                   justify-content:center;margin-bottom:.75rem;transition:transform .22s ease;flex-shrink:0;}
.app-icon-title{font-family:Merriweather,serif;font-size:.98rem;font-weight:700;color:#0F172A;
                margin-bottom:.3rem;line-height:1.25;}
.app-icon-sub{font-size:.76rem;color:#64748B;line-height:1.35;}

.art-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:14px;
          margin-bottom:1.4rem;}
.art-card{border:2px solid #E2E8F0;background:#FFF;border-radius:12px;padding:1rem 1.1rem;
          min-height:236px;display:flex;flex-direction:column;justify-content:space-between;
          box-shadow:0 2px 6px rgba(0,0,0,.03);cursor:pointer;text-align:left;font-family:inherit;
          transition:all .18s ease;}
.art-card:hover{border-color:#86EFAC;transform:translateY(-3px);box-shadow:0 8px 18px rgba(21,128,61,.12);}
.art-card.on{border-color:#15803D;background:#F0FDF4;}
.art-top{display:flex;justify-content:space-between;align-items:center;gap:8px;}
.art-status{font-size:.72rem;font-weight:800;border:1px solid;padding:.18rem .5rem;border-radius:5px;
            white-space:nowrap;}
.art-num{font-size:.78rem;color:#94A3B8;font-weight:800;}
.art-tema{display:block;font-size:.74rem;font-weight:700;color:#64748B;text-transform:uppercase;
          letter-spacing:.05em;margin-top:.75rem;line-height:1.35;}
.art-cont{display:block;font-size:.78rem;color:#475569;margin-top:.4rem;line-height:1.4;}
.art-foot{display:block;border-top:1px solid #E2E8F0;padding-top:.6rem;margin-top:.7rem;}
.art-titulo{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;
            font-family:Merriweather,serif;font-size:.9rem;font-weight:700;color:#0F172A;line-height:1.3;}
.art-venue{display:block;font-size:.76rem;color:#64748B;margin-top:.35rem;line-height:1.35;}

.dossie{display:none;}
.dossie.on{display:block;}
.card-head{background:#FFF;border:1.5px solid #CBD5E1;border-radius:10px;padding:1.4rem 1.6rem;
           margin:1rem 0 1.2rem 0;box-shadow:0 3px 8px rgba(0,0,0,.03);}
.card-head h3{font-family:Merriweather,serif;color:#0F172A;font-size:1.32rem;margin:.3rem 0 .6rem 0;
              line-height:1.35;}
.card-head p{font-size:.87rem;color:#475569;margin:0;line-height:1.55;}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:.6rem;}

.pilares{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:16px;}
.pilar{background:#FFF;border:1.5px solid #CBD5E1;border-left:6px solid #15803D;border-radius:10px;
       padding:1.2rem;box-shadow:0 2px 6px rgba(0,0,0,.03);}
.pilar-h{display:flex;align-items:center;gap:8px;margin-bottom:.6rem;}
.pilar-h span{font-size:1.4rem;}
.pilar-h b{font-size:1.05rem;font-family:Merriweather,serif;}
.pilar .quote{font-size:.93rem;color:#0F172A;font-weight:600;line-height:1.5;background:#F0F9FF;
              padding:.7rem .9rem;border-radius:6px;border:1px solid #BAE6FD;margin-bottom:.6rem;}
.pilar p{font-size:.85rem;color:#334155;line-height:1.45;margin:0;}
.pilar .txt{font-size:.86rem;color:#1E293B;line-height:1.45;margin-bottom:.5rem;}
.pilar .txt p{margin:0 0 .45rem 0;}
.pilar .hip{font-size:.86rem;color:#92400E;background:#FEF3C7;padding:.6rem .8rem;border-radius:6px;
            border:1px solid #FDE68A;line-height:1.4;}
.lista{font-size:.85rem;color:#1E293B;line-height:1.5;margin:0 0 0 1.1rem;padding:0;}
.lista li{margin-bottom:.35rem;}

.fig-frame{display:none;}
.fig-frame.on{display:block;}
.fig-stage{background:#0F172A;border:3px solid #1E293B;border-radius:12px;padding:1rem;text-align:center;
           margin:.9rem 0 .6rem 0;box-shadow:0 6px 18px rgba(0,0,0,.15);}
.fig-bar{display:flex;justify-content:space-between;align-items:center;margin-bottom:.6rem;
         padding:0 .5rem;gap:10px;font-size:.8rem;font-weight:600;color:#94A3B8;}
.fig-name{color:#38BDF8;text-align:right;}
.fig-stage img{width:100%;max-width:1100px;border-radius:6px;background:#FFF;
               box-shadow:0 4px 14px rgba(0,0,0,.4);}
.fig-nav{display:grid;grid-template-columns:auto 1fr auto;gap:10px;align-items:center;margin:.3rem 0;}
.fig-count{text-align:center;background:#FFF;border:1.5px solid #CBD5E1;border-radius:8px;
           padding:.45rem .8rem;box-shadow:0 1px 4px rgba(0,0,0,.03);}
.fig-count-txt{font-size:.88rem;font-weight:800;color:#15803D;}
.film-strip{display:flex;flex-wrap:wrap;gap:6px;}
.film{flex:1 1 44px;min-width:44px;padding:.4rem 0;border-radius:7px;border:1.5px solid #CBD5E1;
      background:#FFF;color:#334155;font-weight:700;font-size:.82rem;cursor:pointer;font-family:inherit;}
.film:hover{border-color:#15803D;color:#15803D;}
.film.on{background:#15803D;border-color:#15803D;color:#FFF;}
.fig-desc{background:#FFF;border:1.5px solid #CBD5E1;border-radius:10px;padding:1.3rem 1.5rem;
          margin:1rem 0 1.4rem 0;box-shadow:0 3px 10px rgba(0,0,0,.03);}
.fig-desc-head{display:flex;justify-content:space-between;align-items:center;gap:10px;
               border-bottom:1px solid #E2E8F0;padding-bottom:.6rem;margin-bottom:.9rem;}
.pill-green{font-size:.76rem;font-weight:700;color:#15803D;background:#DCFCE7;padding:.2rem .6rem;
            border-radius:4px;white-space:nowrap;}
.pill-amber{background:#FEF3C7;color:#92400E;border:1px solid #F59E0B;padding:.15rem .55rem;
            border-radius:4px;font-size:.75rem;font-weight:700;white-space:nowrap;}
.metadata-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;
               margin-top:.6rem;}
.metadata-item{background:#FFF;border:1px solid #E2E8F0;border-radius:6px;padding:.55rem .8rem;}
.metadata-label{font-size:.72rem;font-weight:700;color:#64748B;text-transform:uppercase;
                letter-spacing:.04em;}
.metadata-val{font-size:.85rem;font-weight:700;color:#0F172A;margin-top:.15rem;}

.qa{background:#FFF;border:1px solid #E2E8F0;border-radius:8px;margin-bottom:.5rem;overflow:hidden;}
.qa summary{cursor:pointer;padding:.75rem 1rem;font-weight:600;font-size:.9rem;color:#0F172A;
            list-style:none;display:flex;justify-content:space-between;align-items:center;gap:10px;}
.qa summary::-webkit-details-marker{display:none;}
.qa summary::after{content:"+";color:#15803D;font-weight:800;font-size:1.1rem;flex-shrink:0;}
.qa[open] summary::after{content:"\\2212";}
.qa summary:hover{background:#F8FAFC;}
.qa-body{padding:0 1rem 1rem 1rem;}
.qa-body p{font-size:.9rem;color:#334155;line-height:1.65;margin:0;}

.tabs{display:flex;flex-wrap:wrap;gap:4px;border-bottom:2px solid #E2E8F0;margin-bottom:1.1rem;}
.tab{background:none;border:none;border-bottom:3px solid transparent;padding:.6rem .9rem;
     font-size:.88rem;font-weight:600;color:#64748B;cursor:pointer;font-family:inherit;
     margin-bottom:-2px;}
.tab:hover{color:#15803D;}
.tab.on{color:#15803D;border-bottom-color:#15803D;font-weight:800;}
.tabpane{display:none;}
.tabpane.on{display:block;}
.chips-row{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:1rem;}
.chip{background:#FFF;border:1.5px solid #CBD5E1;border-radius:20px;padding:.4rem .9rem;font-size:.82rem;
      font-weight:600;color:#334155;cursor:pointer;font-family:inherit;}
.chip:hover{border-color:#15803D;color:#15803D;}
.chip.on{background:#15803D;border-color:#15803D;color:#FFF;}
.atlas-pane{display:none;}
.atlas-pane.on{display:block;}

.sig-frame{width:100%;height:760px;border:1.5px solid #CBD5E1;border-radius:10px;background:#FFF;}
.caption{font-size:.84rem;color:#64748B;margin-top:.5rem;line-height:1.5;}
.plate{background:#FFF;padding:1rem;border-radius:8px;border:1.5px solid #CBD5E1;text-align:center;
       margin-bottom:1.2rem;box-shadow:0 2px 6px rgba(0,0,0,.04);}
.fig-h5{font-size:.95rem;font-weight:700;color:#0F172A;margin:.4rem 0 .5rem 0;}
.notes{background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:.9rem 1.1rem;
       font-size:.88rem;color:#334155;line-height:1.55;}
.notes ul{margin:.4rem 0 0 1.1rem;padding:0;}
.notes li{margin-bottom:.3rem;}
.aside{background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:8px;padding:1.1rem;}
.aside ul{font-size:.85rem;color:#475569;margin:.4rem 0 0 1.2rem;padding:0;line-height:1.5;}
.prod{background:#FFF;border:1px solid #CBD5E1;border-left:5px solid #15803D;border-radius:8px;
      padding:1.1rem;box-shadow:0 2px 6px rgba(0,0,0,.03);}
.prod b{color:#0F172A;font-size:1rem;}
.prod-sub{font-size:.78rem;font-weight:700;margin:.2rem 0 .5rem 0;}
.prod p{font-size:.85rem;color:#475569;line-height:1.45;margin:0;}
.service-card{background:#FFF;border:1px solid #E2E8F0;border-left:5px solid #15803D;border-radius:8px;
              padding:1.1rem 1.3rem;margin-bottom:1rem;box-shadow:0 2px 4px rgba(0,0,0,.03);}
.clipping-card{background:#FFF;border:1px solid #E2E8F0;border-radius:8px;padding:1.2rem;
               margin-bottom:1rem;box-shadow:0 2px 5px rgba(0,0,0,.03);}
.clipping-card h4{color:#0F172A;margin:0;font-family:Merriweather,serif;}
.clipping-card .role{font-size:.82rem;font-weight:700;margin:.15rem 0 .4rem 0;}
.clipping-card .meta{font-size:.85rem;color:#475569;margin:0 0 .3rem 0;}
.clipping-card .body{font-size:.85rem;color:#334155;line-height:1.45;margin:0;}

.tbl-wrap{overflow-x:auto;border:1.5px solid #CBD5E1;border-radius:10px;background:#FFF;}
.tbl{border-collapse:collapse;width:100%;font-size:.82rem;}
.tbl th{background:#F1F5F9;color:#0F172A;text-align:left;padding:.6rem .8rem;font-weight:700;
        border-bottom:2px solid #CBD5E1;white-space:nowrap;}
.tbl td{padding:.55rem .8rem;border-bottom:1px solid #F1F5F9;color:#334155;vertical-align:top;}
.tbl tr:hover td{background:#F8FAFC;}
.cite-card{background:#FFF;border:1.5px solid #CBD5E1;border-left:6px solid #15803D;border-radius:10px;
           padding:1.2rem 1.6rem;margin-top:1.4rem;box-shadow:0 2px 5px rgba(0,0,0,.03);}
.cite-head{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:.5rem;
           font-family:Merriweather,serif;font-weight:800;color:#0F172A;font-size:1.05rem;}
.cite-box{background:#F8FAFC;border:1px solid #CBD5E1;border-radius:6px;padding:.85rem 1.1rem;
          font-family:'Courier New',monospace;font-size:.82rem;color:#1E293B;line-height:1.55;
          word-break:break-word;}

.btn{display:inline-block;text-align:center;padding:.55rem 1rem;border-radius:8px;border:1.5px solid #CBD5E1;
     background:#FFF;color:#334155;font-weight:600;font-size:.86rem;cursor:pointer;font-family:inherit;
     text-decoration:none;}
.btn:hover{border-color:#15803D;color:#15803D;}
.btn-primary{background:#15803D;border-color:#15803D;color:#FFF;}
.btn-primary:hover{background:#166534;color:#FFF;}

.traj-hero{position:relative;border-radius:12px;overflow:hidden;margin-bottom:1.4rem;min-height:250px;
           display:flex;align-items:flex-end;border-left:6px solid #16A34A;
           box-shadow:0 4px 16px rgba(0,0,0,.10);
           background-image:linear-gradient(rgba(14,43,23,.28),rgba(14,43,23,.86)),
             url('https://images.unsplash.com/photo-1738625256303-d07f7c459982?auto=format&fit=crop&w=1800&q=80');
           background-size:cover;background-position:center 55%;}
.traj-hero-inner{padding:1.5rem 1.8rem;}
.traj-kicker{display:inline-block;font-size:.72rem;font-weight:800;letter-spacing:.12em;
             text-transform:uppercase;color:#BBF7D0;border:1px solid rgba(187,247,208,.5);
             border-radius:4px;padding:.18rem .55rem;margin-bottom:.6rem;}
.traj-hero h2{font-family:Merriweather,serif;color:#FFF;font-size:1.85rem;margin:0 0 .35rem 0;
              line-height:1.2;letter-spacing:-.01em;}
.traj-hero p{color:#E2E8F0;font-size:.97rem;margin:0;max-width:780px;line-height:1.5;}
.sec-title{font-family:Merriweather,serif;color:#0F172A;font-size:1.25rem;margin:1.6rem 0 .2rem 0;}
.sec-sub{font-size:.9rem;color:#475569;margin:0 0 .9rem 0;}
.tl{position:relative;}
.tl::before{content:"";position:absolute;left:147px;top:8px;bottom:8px;width:2px;
            background:linear-gradient(180deg,#BBF7D0,#15803D 45%,#BBF7D0);}
.tl-item{display:grid;grid-template-columns:132px 32px 1fr;align-items:start;margin-bottom:.7rem;}
.tl-when{font-size:.79rem;font-weight:800;color:#15803D;text-align:right;padding-top:.55rem;
         line-height:1.25;}
.tl-mark{position:relative;height:100%;}
.tl-mark i{position:absolute;left:10px;top:.6rem;width:11px;height:11px;border-radius:50%;background:#FFF;
           border:3px solid #15803D;box-shadow:0 0 0 3px #ECFDF5;}
.tl-card{background:#FFF;border:1px solid #E2E8F0;border-left:4px solid #15803D;border-radius:8px;
         padding:.6rem .95rem;box-shadow:0 1px 3px rgba(0,0,0,.04);}
.tl-card b{font-family:Merriweather,serif;font-size:.93rem;color:#0F172A;}
.tl-card span{display:block;font-size:.83rem;color:#475569;margin-top:.18rem;line-height:1.45;}
.tl-item.atual .tl-card{background:#F0FDF4;border-color:#BBF7D0;}
.tl-item.atual .tl-mark i{background:#15803D;}
.flip-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(255px,1fr));gap:14px;margin-top:.4rem;}
.flip-card{perspective:1200px;height:250px;outline:none;}
.flip-inner{position:relative;width:100%;height:100%;
            transition:transform .7s cubic-bezier(.4,.2,.2,1);transform-style:preserve-3d;}
.flip-card:hover .flip-inner,.flip-card:focus .flip-inner,.flip-card:focus-within .flip-inner{
            transform:rotateY(180deg);}
.flip-front,.flip-back{position:absolute;inset:0;backface-visibility:hidden;
            -webkit-backface-visibility:hidden;border-radius:12px;overflow:hidden;
            box-shadow:0 3px 12px rgba(15,23,42,.10);}
.flip-front{background:#F7FAF5;display:flex;align-items:flex-end;border:1px solid #CBD5E1;}
.flip-front .ilu{position:absolute;inset:0;}
.flip-front .ilu svg{width:100%;height:100%;display:block;}
.flip-front .ilu img.arte{width:100%;height:100%;object-fit:cover;display:block;}
.flip-front-hint{position:relative;margin:0 .75rem .75rem auto;font-size:.66rem;font-weight:700;
                 letter-spacing:.08em;text-transform:uppercase;color:#ECFDF5;background:rgba(14,43,23,.72);
                 border:1px solid rgba(187,247,208,.35);border-radius:20px;padding:.22rem .6rem;}
.flip-front-label{position:relative;width:100%;padding:.85rem 1rem;
                  background:linear-gradient(transparent,rgba(14,43,23,.88) 55%);color:#FFF;
                  font-family:Merriweather,serif;font-weight:700;font-size:.97rem;line-height:1.3;}
.flip-front-label em{display:block;font-style:normal;font-family:Inter,sans-serif;font-weight:500;
                     font-size:.72rem;color:#BBF7D0;margin-top:.25rem;letter-spacing:.05em;
                     text-transform:uppercase;}
.flip-back{transform:rotateY(180deg);background:linear-gradient(155deg,#14532D 0%,#15803D 100%);
           color:#ECFDF5;padding:1.15rem 1.25rem;display:flex;flex-direction:column;
           justify-content:center;border:1px solid #14532D;}
.flip-back b{font-family:Merriweather,serif;font-size:.97rem;color:#FFF;display:block;
             margin-bottom:.5rem;}
.flip-back p{font-size:.85rem;line-height:1.55;margin:0;color:#DCFCE7;}
.credito{font-size:.74rem;color:#94A3B8;margin:.7rem 0 1.2rem 0;}

.rodape{text-align:center;font-size:.78rem;color:#64748B;padding:1.2rem 0;margin-top:2rem;
        border-top:1px solid #E2E8F0;line-height:1.6;}

.flab-hero{border-radius:12px;overflow:hidden;margin-bottom:1rem;border-left:6px solid #16A34A;
           box-shadow:0 4px 16px rgba(0,0,0,.10);
           background-image:linear-gradient(rgba(6,32,16,.80),rgba(6,32,16,.90)),
             url('static/forest_lab/01_floresta_3d.jpg');
           background-size:cover;background-position:center 60%;}
.flab-hero-in{padding:1.5rem 1.8rem;}
.flab-kicker{display:inline-block;font-size:.72rem;font-weight:800;letter-spacing:.12em;
             text-transform:uppercase;color:#BBF7D0;border:1px solid rgba(187,247,208,.5);
             border-radius:4px;padding:.18rem .55rem;margin-bottom:.6rem;}
.flab-hero h3{font-family:Merriweather,serif;color:#FFF;font-size:1.5rem;margin:0 0 .5rem 0;
              line-height:1.25;letter-spacing:-.01em;}
.flab-hero p{color:#E2E8F0;font-size:.95rem;margin:0;max-width:860px;line-height:1.55;}
.flab-badges{display:flex;flex-wrap:wrap;gap:7px;margin-top:.9rem;}
.flab-badges span{font-size:.73rem;font-weight:700;color:#DCFCE7;background:rgba(21,128,61,.45);
                  border:1px solid rgba(187,247,208,.38);border-radius:20px;padding:.22rem .65rem;}
.flab-acoes{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:.9rem;}
.flab-palco{background:#060D08;border:1.5px solid #14532D;border-radius:12px;padding:5px;
            box-shadow:0 6px 20px rgba(6,32,16,.18);
            margin-left:-2rem;margin-right:-2rem;}
.flab-palco:fullscreen{padding:0;border:none;border-radius:0;margin:0;}
.flab-palco:fullscreen .flab-frame{height:100vh;border-radius:0;}
.flab-frame{display:block;width:100%;height:min(88vh,1040px);min-height:620px;border:none;
            border-radius:8px;background:#0B1220;}
html.flab-amplo .sidebar{display:none;}
html.flab-amplo .shell{max-width:none;}
html.flab-amplo .main{padding-left:0;padding-right:0;}
html.flab-amplo .flab-hero,html.flab-amplo .flab-acoes,html.flab-amplo .banner,
html.flab-amplo .tabs,html.flab-amplo .caption,html.flab-amplo .rule,
html.flab-amplo .cite-card{margin-left:1rem;margin-right:1rem;}
html.flab-amplo .flab-palco{margin-left:0;margin-right:0;border-radius:0;
                            border-left:none;border-right:none;}
html.flab-amplo .flab-frame{height:calc(100vh - 74px);min-height:420px;border-radius:0;}
.flab-galeria{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:14px;
              margin-top:.5rem;}
.flab-shot{margin:0;background:#FFF;border:1.5px solid #CBD5E1;border-radius:10px;overflow:hidden;
           box-shadow:0 2px 6px rgba(0,0,0,.04);}
.flab-shot img{display:block;width:100%;height:auto;background:#0B1220;}
.flab-shot figcaption{font-size:.82rem;color:#475569;line-height:1.5;padding:.7rem .9rem;}
.flab-shot figcaption b{color:#0F172A;}

.share-card{background:#FFF;border:1.5px solid #CBD5E1;border-left:6px solid #0284C7;border-radius:10px;
            padding:1.1rem 1.4rem;margin-top:1.4rem;box-shadow:0 2px 6px rgba(0,0,0,.03);}
.share-head{font-family:Merriweather,serif;font-weight:800;color:#0F172A;font-size:1.02rem;
            margin-bottom:.75rem;}
.share-row{display:flex;flex-wrap:wrap;gap:8px;}
.share-btn{display:inline-block;padding:.5rem 1rem;border-radius:8px;border:1.5px solid #CBD5E1;
           background:#FFF;color:#334155;font-weight:700;font-size:.85rem;cursor:pointer;
           font-family:inherit;text-decoration:none;transition:all .16s ease;}
.share-btn:hover{transform:translateY(-2px);box-shadow:0 4px 10px rgba(15,23,42,.10);}
.share-btn.wa:hover{border-color:#25D366;color:#0F7A3D;}
.share-btn.li:hover{border-color:#0A66C2;color:#0A66C2;}
.share-btn.em:hover{border-color:#64748B;color:#0F172A;}
.share-btn.cp:hover{border-color:#15803D;color:#15803D;}
.share-btn.copiado{background:#15803D;border-color:#15803D;color:#FFF;}
.share-nota{font-size:.79rem;color:#64748B;line-height:1.5;margin:.75rem 0 0 0;}

.est-destaque{background:linear-gradient(135deg,#0C4A6E 0%,#075985 55%,#0369A1 100%);
              border-radius:12px;padding:1.5rem 1.8rem;color:#E0F2FE;margin-bottom:.4rem;
              display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:14px;
              box-shadow:0 4px 16px rgba(3,105,161,.18);}
.est-numero{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;}
.est-valor{font-family:Merriweather,serif;font-size:2.8rem;font-weight:900;color:#FFF;line-height:1;
           letter-spacing:-.02em;}
.est-rotulo{font-size:.95rem;color:#BAE6FD;font-weight:600;}
.est-nota{font-size:.8rem;color:#BAE6FD;max-width:330px;line-height:1.5;text-align:right;}
.est-destaque[data-estado="erro"]{background:linear-gradient(135deg,#334155 0%,#1E293B 100%);}
.est-destaque[data-estado="desligado"]{background:linear-gradient(135deg,#44403C 0%,#292524 100%);}

.est-tabela .num{text-align:right;font-weight:800;color:#0369A1;font-variant-numeric:tabular-nums;}
.est-tabela .barra{padding-right:1rem;}
.est-tabela .barra span{display:block;height:9px;border-radius:5px;background:#0284C7;
                        transition:width .5s ease;}

.est-grade{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:12px;
           margin-top:.6rem;}
.est-item{display:flex;gap:11px;background:#FFF;border:1px solid #E2E8F0;border-radius:9px;
          padding:.9rem 1.05rem;box-shadow:0 2px 4px rgba(0,0,0,.03);}
.est-ico{font-size:1.25rem;line-height:1.2;flex-shrink:0;}
.est-item b{display:block;font-size:.92rem;color:#0F172A;font-family:Merriweather,serif;
            margin-bottom:.25rem;}
.est-item p{font-size:.83rem;color:#475569;line-height:1.5;margin:0;}

.est-painel{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:14px;
            background:#F8FAFC;border:1.5px solid #CBD5E1;border-radius:10px;padding:1.1rem 1.4rem;
            margin-top:1.4rem;}
.est-painel b{font-family:Merriweather,serif;color:#0F172A;font-size:1rem;}
.est-painel p{font-size:.84rem;color:#475569;line-height:1.5;margin:.25rem 0 0 0;max-width:620px;}

@media (max-width:980px){
  .shell{flex-direction:column;}
  .sidebar{width:100%;flex:none;position:static;max-height:none;min-height:0;
           border-right:none;border-bottom:1.5px solid #D1E0D5;}
  .main{padding:1rem 1rem 2rem 1rem;width:100%;}
  .split{grid-template-columns:1fr;}
  .hero-title{font-size:1.6rem;}
  .hero-magazine{padding:1.2rem 1.2rem;}
  .fig-nav{grid-template-columns:1fr;}
  .sig-frame{height:600px;}
  .flab-frame{height:min(80vh,640px);}
  .flab-palco{margin-left:-1rem;margin-right:-1rem;}
  .est-nota{text-align:left;max-width:none;}
  .est-valor{font-size:2.1rem;}
  .flab-hero h3{font-size:1.2rem;}
}
@media (max-width:640px){
  .tl::before{display:none;}
  .tl-item{grid-template-columns:1fr;}
  .tl-mark{display:none;}
  .tl-when{text-align:left;padding:0 0 .2rem .1rem;}
  .traj-hero h2{font-size:1.4rem;}
  .flab-frame{height:min(78vh,560px);}
}
"""

JS = """
(function(){
  function todos(sel, raiz){
    return Array.prototype.slice.call((raiz || document).querySelectorAll(sel));
  }

  // Imagem ou iframe com loading="lazy" dentro de um container display:none nao e observado;
  // ao exibi-lo, trocamos para eager para garantir o carregamento imediato.
  function despertar(raiz){
    todos('img[loading="lazy"],iframe[loading="lazy"]', raiz).forEach(function(el){
      if (el.offsetParent !== null) el.setAttribute('loading', 'eager');
    });
  }

  // ------------------------------------------------------------- medicao
  // Camada de medicao anonima. Sem cookies: o GoatCounter nao usa nenhum, e o
  // que fica no localStorage serve so para o painel "Esta visita" deste aparelho.
  var CODIGO = document.documentElement.dataset.gc || '';
  var fila = [];

  function medir(caminho, titulo, evento){
    if (!CODIGO) return;
    var gc = window.goatcounter;
    if (!gc || typeof gc.count !== 'function'){
      if (fila.length < 30) fila.push([caminho, titulo, evento]);
      return;
    }
    try {
      gc.count({path: caminho, title: titulo || caminho, event: !!evento});
    } catch (e) { /* bloqueador de anuncios: a pagina segue funcionando */ }
  }

  function escoarFila(){
    var pendentes = fila.splice(0, fila.length);
    pendentes.forEach(function(a){ medir(a[0], a[1], a[2]); });
  }
  window.addEventListener('load', escoarFila);
  setTimeout(escoarFila, 2500);

  var CANAIS = [
    [/(^|\\.)linkedin\\.|lnkd\\.in/, 'linkedin', 'LinkedIn'],
    [/(^|\\.)google\\.[a-z.]+$/, 'google', 'Google'],
    [/scholar\\.google/, 'google-academico', 'Google Acadêmico'],
    [/(^|\\.)bing\\./, 'bing', 'Bing'],
    [/duckduckgo/, 'duckduckgo', 'DuckDuckGo'],
    [/whatsapp|wa\\.me/, 'whatsapp', 'WhatsApp'],
    [/t\\.me|telegram/, 'telegram', 'Telegram'],
    [/(^|\\.)facebook\\.|fb\\.me/, 'facebook', 'Facebook'],
    [/instagram/, 'instagram', 'Instagram'],
    [/t\\.co$|twitter\\.com|x\\.com$/, 'twitter', 'X / Twitter'],
    [/researchgate/, 'researchgate', 'ResearchGate'],
    [/orcid\\.org/, 'orcid', 'ORCID'],
    [/zenodo\\.org|doi\\.org/, 'zenodo', 'Zenodo / DOI'],
    [/lattes\\.cnpq/, 'lattes', 'Lattes'],
    [/github\\.|github\\.io/, 'github', 'GitHub'],
    [/mail\\.google|outlook\\.|mail\\.yahoo|webmail/, 'email', 'E-mail']
  ];

  function origem(){
    var utm = null;
    try { utm = new URLSearchParams(location.search).get('utm_source'); } catch (e) { utm = null; }
    if (utm) return {chave: utm.toLowerCase().slice(0, 40), nome: utm + ' (campanha etiquetada)'};
    var ref = document.referrer;
    if (!ref) return {chave: 'direto', nome: 'Acesso direto, favorito ou aplicativo de mensagens'};
    var host;
    try { host = new URL(ref).hostname.replace(/^www\\./, ''); } catch (e) {
      return {chave: 'desconhecido', nome: 'Origem não identificada'};
    }
    if (host === location.hostname) return {chave: 'interno', nome: 'Navegação dentro do próprio site'};
    for (var i = 0; i < CANAIS.length; i++){
      if (CANAIS[i][0].test(host)) return {chave: CANAIS[i][1], nome: CANAIS[i][2]};
    }
    return {chave: host.slice(0, 40), nome: host};
  }

  function guardar(chave, valor){
    try { localStorage.setItem(chave, valor); } catch (e) { /* modo privado */ }
  }
  function ler(chave, padrao){
    try { var v = localStorage.getItem(chave); return v === null ? padrao : v; }
    catch (e) { return padrao; }
  }

  var ORIGEM = origem();
  var visitas = parseInt(ler('jcas_visitas', '0'), 10) + 1;
  var primeira = ler('jcas_primeira', '') || new Date().toISOString();
  guardar('jcas_visitas', String(visitas));
  guardar('jcas_primeira', primeira);

  // uma vez por sessao, registra por onde a pessoa chegou
  try {
    if (!sessionStorage.getItem('jcas_origem')){
      sessionStorage.setItem('jcas_origem', ORIGEM.chave);
      medir('origem-' + ORIGEM.chave, 'Origem: ' + ORIGEM.nome, true);
    }
  } catch (e) { /* sessionStorage indisponivel */ }

  function rotuloLink(el){
    var r = (el.dataset.medir || el.getAttribute('aria-label') || el.textContent || '').trim();
    if (!r){ try { r = new URL(el.href).hostname; } catch (e) { r = 'link'; } }
    return r.replace(/\\s+/g, ' ').slice(0, 60);
  }

  // ------------------------------------------------- painel de estatisticas
  function formatar(n){
    return String(n).replace(/\\B(?=(\\d{3})+(?!\\d))/g, '.');
  }

  function textoVisita(){
    var nav = navigator;
    var toque = (nav.maxTouchPoints || 0) > 1;
    var larg = window.screen ? window.screen.width : 0;
    var tipo = larg && larg < 768 ? 'Celular' : (toque && larg < 1200 ? 'Tablet' : 'Computador');
    var d = new Date(primeira);
    var dataPrimeira = isNaN(d.getTime()) ? '—' :
      d.toLocaleDateString('pt-BR', {day: '2-digit', month: 'short', year: 'numeric'});
    return [
      ['Como você chegou', ORIGEM.nome],
      ['Endereço de origem', document.referrer ? document.referrer.slice(0, 70) : 'Nenhum informado'],
      ['Acessos deste aparelho', formatar(visitas) + (visitas === 1 ? ' (primeiro)' : '')],
      ['Primeiro acesso', dataPrimeira],
      ['Tipo de aparelho', tipo],
      ['Tela', (window.screen ? window.screen.width + ' × ' + window.screen.height : '—') + ' px'],
      ['Idioma do navegador', nav.language || '—'],
      ['Fuso horário', (Intl.DateTimeFormat().resolvedOptions().timeZone || '—')],
      ['Medição ativa', CODIGO ? 'Sim, anônima e sem cookies' : 'Ainda não configurada'],
      ['Bloqueador de anúncios', (window.goatcounter && window.goatcounter.count) || !CODIGO ?
        'Não detectado' : 'Provavelmente ativo (acesso não contado)']
    ];
  }

  function montarVisita(){
    var caixa = document.querySelector('[data-visita]');
    if (!caixa || caixa.dataset.pronto) return;
    caixa.dataset.pronto = '1';
    caixa.innerHTML = textoVisita().map(function(par){
      return '<div class="metadata-item"><div class="metadata-label">' + par[0] +
             '</div><div class="metadata-val">' + String(par[1]) + '</div></div>';
    }).join('');
  }

  function numero(txt){
    var n = parseInt(String(txt).replace(/[^0-9]/g, ''), 10);
    return isNaN(n) ? 0 : n;
  }

  function contador(caminho){
    var u = 'https://' + CODIGO + '.goatcounter.com/counter/' + encodeURIComponent(caminho) + '.json';
    return fetch(u, {mode: 'cors'}).then(function(r){
      if (!r.ok) throw new Error(r.status);
      return r.json();
    }).then(function(j){ return numero(j.count != null ? j.count : j.count_unique); });
  }

  var carregouPainel = false;
  function carregarPainel(){
    if (carregouPainel) return;
    carregouPainel = true;
    montarVisita();

    var destaque = document.querySelector('.est-destaque');
    var alvoTotal = document.querySelector('[data-total]');
    var txt = document.querySelector('[data-estado-txt]');
    var link = document.querySelector('[data-painel-url]');
    var caixaLink = document.querySelector('[data-painel-link]');

    if (!CODIGO){
      if (destaque) destaque.dataset.estado = 'desligado';
      if (alvoTotal) alvoTotal.textContent = '—';
      if (txt) txt.textContent = 'O contador ainda não foi ativado. Assim que a conta de medição ' +
        'estiver criada, os números aparecem aqui automaticamente.';
      if (caixaLink) caixaLink.style.display = 'none';
      return;
    }

    if (link) link.href = 'https://' + CODIGO + '.goatcounter.com';

    contador('TOTAL').then(function(total){
      if (destaque) destaque.dataset.estado = 'ok';
      if (alvoTotal) alvoTotal.textContent = formatar(total);
      if (txt) txt.textContent = 'Visitantes únicos estimados. Bloqueadores de anúncio barram cerca ' +
        'de um terço dos acessos, então o número real é um pouco maior.';
    }).catch(function(){
      if (destaque) destaque.dataset.estado = 'erro';
      if (alvoTotal) alvoTotal.textContent = '—';
      if (txt) txt.textContent = 'Não foi possível ler o contador público agora. Verifique se a opção ' +
        '"Allow adding visitor counts on your website" está ligada nas configurações do serviço.';
    });

    var linhas = todos('[data-contador-secao]');
    Promise.all(linhas.map(function(tr){
      return contador('/secao/' + tr.dataset.contadorSecao).catch(function(){ return null; });
    })).then(function(vals){
      var validos = vals.filter(function(v){ return v !== null; });
      if (!validos.length){
        linhas.forEach(function(tr){ tr.querySelector('[data-valor]').textContent = '—'; });
        return;
      }
      var maior = Math.max.apply(null, validos.concat([1]));
      linhas.forEach(function(tr, i){
        var v = vals[i];
        tr.querySelector('[data-valor]').textContent = v === null ? '—' : formatar(v);
        if (v !== null){
          var pct = v > 0 ? Math.max(3, Math.round((v / maior) * 100)) : 0;
          tr.querySelector('[data-barra]').style.width = pct + '%';
        }
      });
    });
  }

  function irPara(alvo, empurrar){
    var achou = false;
    todos('.sec').forEach(function(s){
      var on = (s.dataset.sec === alvo);
      s.classList.toggle('on', on);
      if (on) achou = true;
    });
    if (!achou) return false;
    todos('.nav-btn').forEach(function(b){
      b.classList.toggle('on', b.dataset.goto === alvo);
    });
    if (empurrar && location.hash !== '#' + alvo){
      history.pushState({sec: alvo}, '', '#' + alvo);
    }
    despertar(document.querySelector('.sec.on'));
    medir('/secao/' + alvo, 'Seção: ' + alvo);
    if (alvo === 'estatisticas') carregarPainel();
    window.scrollTo({top: 0, behavior: 'smooth'});
    return true;
  }

  function selecionarArtigo(id){
    todos('.art-card').forEach(function(c){ c.classList.toggle('on', c.dataset.art === id); });
    todos('.dossie').forEach(function(d){ d.classList.toggle('on', d.dataset.dossie === id); });
    despertar(document.querySelector('.dossie.on'));
  }

  function mostrarFigura(id, i){
    var quadros = todos('.fig-frame[data-fig="' + id + '"]');
    quadros.forEach(function(q){ q.classList.toggle('on', parseInt(q.dataset.i, 10) === i); });
    todos('.film[data-film="' + id + '"]').forEach(function(b){
      b.classList.toggle('on', parseInt(b.dataset.i, 10) === i);
    });
    var contador = document.querySelector('[data-figcount="' + id + '"]');
    if (contador) contador.textContent = 'Figura ' + (i + 1) + ' de ' + quadros.length;
    despertar(quadros[i]);
  }

  document.addEventListener('click', function(ev){
    var ir = ev.target.closest('[data-goto]');
    if (ir){ ev.preventDefault(); irPara(ir.dataset.goto, true); return; }

    var aba = ev.target.closest('.tab');
    if (aba){
      var grupo = aba.dataset.tabs, i = aba.dataset.i;
      todos('.tab[data-tabs="' + grupo + '"]').forEach(function(b){
        b.classList.toggle('on', b.dataset.i === i);
      });
      todos('.tabpane[data-tabs="' + grupo + '"]').forEach(function(p){
        p.classList.toggle('on', p.dataset.i === i);
      });
      despertar(document.querySelector('.tabpane[data-tabs="' + grupo + '"].on'));
      medir('aba-' + grupo + '-' + i, 'Aba ' + grupo + ' n' + i, true);
      return;
    }

    var share = ev.target.closest('[data-share]');
    if (share){
      medir('compartilhar-' + share.dataset.share, 'Compartilhar: ' + share.dataset.share, true);
      if (share.dataset.copiar){
        ev.preventDefault();
        var endereco = share.dataset.copiar;
        var confirmar = function(){
          var antes = share.textContent;
          share.textContent = 'Link copiado!';
          share.classList.add('copiado');
          setTimeout(function(){
            share.textContent = antes;
            share.classList.remove('copiado');
          }, 2200);
        };
        var manual = function(){
          var cx = document.createElement('textarea');
          cx.value = endereco;
          cx.setAttribute('readonly', '');
          cx.style.cssText = 'position:fixed;top:-1000px;opacity:0;';
          document.body.appendChild(cx);
          cx.select();
          var deu = false;
          try { deu = document.execCommand('copy'); } catch (e) { deu = false; }
          document.body.removeChild(cx);
          if (deu) confirmar();
          else {
            share.textContent = 'Copie: ' + endereco;
            share.classList.add('copiado');
          }
        };
        if (navigator.clipboard && navigator.clipboard.writeText){
          navigator.clipboard.writeText(endereco).then(confirmar, manual);
        } else {
          manual();
        }
      }
      return;
    }

    var amplo = ev.target.closest('[data-amplo]');
    if (amplo){
      var ligado = document.documentElement.classList.toggle('flab-amplo');
      if (ligado) medir('simulador-modo-amplo', 'Forest Lab: modo amplo', true);
      amplo.textContent = ligado ? '⤡ Sair do modo amplo' : '⤢ Modo amplo';
      amplo.classList.toggle('btn-primary', ligado);
      document.querySelector('.flab-acoes').scrollIntoView({block: 'start'});
      return;
    }

    var tela = ev.target.closest('[data-fullscreen]');
    if (tela){
      medir('simulador-tela-cheia', 'Forest Lab: tela cheia', true);
      var palco = document.getElementById(tela.dataset.fullscreen);
      if (palco){
        if (document.fullscreenElement) document.exitFullscreen();
        else if (palco.requestFullscreen) palco.requestFullscreen();
        else if (palco.webkitRequestFullscreen) palco.webkitRequestFullscreen();
      }
      return;
    }

    var chip = ev.target.closest('.chip[data-atlas]');
    if (chip){
      var k = chip.dataset.atlas;
      todos('.chip[data-atlas]').forEach(function(b){ b.classList.toggle('on', b.dataset.atlas === k); });
      todos('.atlas-pane').forEach(function(p){ p.classList.toggle('on', p.dataset.atlas === k); });
      despertar(document.querySelector('.atlas-pane.on'));
      return;
    }

    var cartao = ev.target.closest('.art-card');
    if (cartao){
      medir('artigo-' + cartao.dataset.art, 'Artigo aberto: ' + cartao.dataset.art, true);
      selecionarArtigo(cartao.dataset.art);
      return;
    }

    var quadro = ev.target.closest('.film');
    if (quadro){ mostrarFigura(quadro.dataset.film, parseInt(quadro.dataset.i, 10)); return; }

    var externo = ev.target.closest('a[href^="http"], a[href^="mailto:"]');
    if (externo && !externo.dataset.share){
      var destino = externo.getAttribute('href') || '';
      if (destino.indexOf(location.origin) !== 0){
        var nome = rotuloLink(externo);
        medir('link-' + nome, 'Link: ' + nome, true);
      }
    }

    var passo = ev.target.closest('[data-figstep]');
    if (passo){
      var id = passo.dataset.figstep;
      var total = todos('.fig-frame[data-fig="' + id + '"]').length;
      if (!total) return;
      var atual = todos('.fig-frame[data-fig="' + id + '"].on')[0];
      var idx = atual ? parseInt(atual.dataset.i, 10) : 0;
      mostrarFigura(id, (idx + parseInt(passo.dataset.d, 10) + total) % total);
      return;
    }
  });

  window.addEventListener('popstate', function(){
    irPara((location.hash || '#inicio').slice(1), false);
  });

  var inicial = (location.hash || '#inicio').slice(1);
  if (!irPara(inicial, false)) irPara('inicio', false);
})();
"""

LINKS = [
    ("https://www.linkedin.com/in/jomil-costa/", "LinkedIn Perfil", "#0A66C2",
     '<path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 '
     '3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 '
     '1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 8.76a1.65 1.65 0 1 0-.02-3.3 1.65 1.65 0 0 0 .02 3.3m1.4 '
     '9.74V9.93H5.06v8.57h2.8z"/>'),
    ("https://orcid.org/0000-0001-8722-8398", "ORCID 0000-0001-8722-8398", "#A6CE39",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1.2 15.5H9.1V8.9h1.7v8.6z'
     'm-.85-9.6a1 1 0 1 1 0-2 1 1 0 0 1 0 2zm6.2 9.6h-3V8.9h3.1c2.4 0 4 1.7 4 4.3 0 2.6-1.7 4.3-4.1 4.3zm-.1'
     '-7.2h-1.2v5.8h1.2c1.6 0 2.5-1.1 2.5-2.9 0-1.8-.9-2.9-2.5-2.9z"/>'),
    ("http://lattes.cnpq.br/0266681173969604", "Currículo Lattes (CNPq)", "#0284C7",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2'
     'v2z"/>'),
    ("https://scholar.google.com/citations?user=3ymOKh8AAAAJ&hl=en", "Google Acadêmico", "#4285F4",
     '<path d="M12 3L1 9l4 2.18v6L12 21l7-3.82v-6l2-1.09V17h2V9L12 3zm6.82 6L12 12.72 5.18 9 12 5.28 18.82 9z'
     'M17 15.99l-5 2.73-5-2.73v-3.72L12 15l5-2.73v3.72z"/>'),
    ("https://www.researchgate.net/profile/Jomil-Sales", "ResearchGate", "#00CCBB",
     '<path d="M19.5 21a3 3 0 0 0 3-3v-4.5a3 3 0 0 0-3-3h-1.5v-3A4.5 4.5 0 0 0 13.5 3h-6A4.5 4.5 0 0 0 3 '
     '7.5v9A4.5 4.5 0 0 0 7.5 21h12zM7.5 5h6A2.5 2.5 0 0 1 16 7.5v3h-8.5A2.5 2.5 0 0 1 5 8V7.5A2.5 2.5 0 0 1 '
     '7.5 5zm-2.5 11.5v-4A2.5 2.5 0 0 1 7.5 10H16v.5A2.5 2.5 0 0 1 13.5 13H10v2h3.5A2.5 2.5 0 0 1 16 '
     '17.5v.5H7.5A2.5 2.5 0 0 1 5 16.5z"/>'),
    ("mailto:jomil.sales@usp.br", "Contato: jomil.sales@usp.br", "#15803D",
     '<path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 '
     '5-8-5V6l8 5 8-5v2z"/>'),
]


def bloco_links():
    partes = []
    for url, rotulo, cor, svg in LINKS:
        externo = "" if url.startswith("mailto:") else ' target="_blank" rel="noopener noreferrer"'
        partes.append(f'<a href="{esc(url)}"{externo}>'
                      f'<svg width="18" height="18" viewBox="0 0 24 24" fill="{cor}">{svg}</svg>'
                      f'{esc(rotulo)}</a>')
    return "".join(partes)


def script_medicao():
    """Carrega o count.js do GoatCounter, quando ha um codigo configurado."""
    if not GOATCOUNTER:
        return "<!-- medicao desligada: defina GOATCOUNTER em tools/build_site.py -->"
    return ('<script data-goatcounter="https://{0}.goatcounter.com/count" '
            'async src="//gc.zgo.at/count.js"></script>').format(GOATCOUNTER)


def bloco_compartilhar(titulo="Compartilhe este portfólio", nota=True):
    """Botoes de compartilhamento. Cada clique vira um evento medido."""
    alvo = "https://jomilc.github.io/portifolio/"
    texto = ("Portfólio científico do Dr. Jomil Costa Abreu Sales — sensoriamento remoto, "
             "WebSIG da APA de Itupararanga e o simulador 3D Forest Lab")
    wa = f"https://wa.me/?text={quote(texto + ' ' + alvo)}"
    li = f"https://www.linkedin.com/sharing/share-offsite/?url={quote(alvo)}"
    email = (f"mailto:?subject={quote('Portfolio cientifico - Dr. Jomil Costa Abreu Sales')}"
             f"&body={quote(texto + ':' + chr(10) + chr(10) + alvo)}")
    aviso = ("" if not nota else
             '<p class="share-nota">Os botões contam quantas pessoas clicaram em compartilhar. '
             'O compartilhamento em si acontece fora do site e não pode ser medido por ninguém — '
             'o que se mede é de onde chegam as visitas.</p>')
    return f"""
<div class="share-card">
  <div class="share-head"><span>\U0001f517 {titulo}</span></div>
  <div class="share-row">
    <a class="share-btn wa" href="{wa}" target="_blank" rel="noopener"
       data-share="whatsapp">WhatsApp</a>
    <a class="share-btn li" href="{li}" target="_blank" rel="noopener"
       data-share="linkedin">LinkedIn</a>
    <a class="share-btn em" href="{email}" data-share="email">E-mail</a>
    <button class="share-btn cp" data-share="copiar" data-copiar="{alvo}">Copiar link</button>
  </div>
  {aviso}
</div>"""


def secao_estatisticas():
    """Painel publico de metricas de acesso."""
    linhas_secoes = "".join(
        f'<tr data-contador-secao="{slug}"><td>{esc(rotulo)}</td>'
        f'<td class="num" data-valor>—</td>'
        f'<td class="barra"><span data-barra style="width:0%"></span></td></tr>'
        for slug, rotulo in SECOES if slug != "estatisticas")

    medidos = [
        ("\U0001f465", "Visitantes e visualizações",
         "Quantas pessoas entraram, quantas páginas viram e em que dia. O número de visitantes "
         "é uma estimativa por dispositivo: a mesma pessoa no celular e no computador conta duas vezes."),
        ("\U0001f5c2️", "Seções mais visitadas",
         "Cada seção aberta — artigos, WebSIG, IA, consultoria, trajetória — "
         "é registrada separadamente, o que mostra o que realmente interessa a quem chega."),
        ("\U0001f5b1️", "Cliques em cada link",
         "LinkedIn, ORCID, Lattes, Google Acadêmico, ResearchGate, o DOI do Forest Lab, o "
         "código no GitHub, o simulador em tela cheia e cada artigo aberto."),
        ("\U0001f9ed", "De onde vieram as visitas",
         "LinkedIn, Google, ResearchGate, Zenodo, WhatsApp, acesso direto. É a medida mais próxima "
         "de “quem compartilhou”, porque mostra o compartilhamento que trouxe gente."),
        ("\U0001f4e4", "Cliques em compartilhar",
         "Quantas pessoas clicaram nos botões de WhatsApp, LinkedIn, e-mail e copiar link. "
         "É intenção de compartilhar, não compartilhamento confirmado."),
        ("\U0001f30d", "País, navegador, sistema e tela",
         "Em que país a pessoa está, que navegador e sistema usa, e se o acesso foi por celular "
         "ou computador — útil para saber se o portfólio precisa funcionar bem no telefone."),
        ("\U0001f3f7️", "Campanhas etiquetadas",
         "Se você divulgar o link com uma etiqueta diferente por canal "
         "(<code>?utm_source=linkedin</code>, por exemplo), cada canal aparece separado, mesmo quando "
         "o navegador não informa a origem."),
    ]
    cartoes_medidos = "".join(
        f'<div class="est-item"><span class="est-ico">{i}</span>'
        f'<div><b>{t}</b><p>{d}</p></div></div>' for i, t, d in medidos)

    nao_medidos = [
        ("Quantas pessoas compartilharam de fato",
         "Copiar o endereço e colar no WhatsApp, num e-mail ou num grupo acontece inteiramente fora "
         "do site. Não existe evento para registrar nem API que informe — nenhuma ferramenta "
         "do mercado consegue isso."),
        ("Quem são as pessoas",
         "Não há nome, e-mail, login nem perfil. A medição é anônima e "
         "agregada, sem cookies, o que também dispensa aviso de consentimento."),
        ("O total exato de visitas",
         "Bloqueadores de anúncio barram cerca de um terço dos acessos. Todo número aqui "
         "é um piso — o real é sempre um pouco maior."),
        ("Visitas vindas de WhatsApp, Telegram e e-mail",
         "Esses aplicativos não informam a origem ao navegador, então aparecem como "
         "“acesso direto”. Links etiquetados com <code>utm_source</code> resolvem isso."),
    ]
    lista_nao = "".join(f"<li><b>{t}</b> — {d}</li>" for t, d in nao_medidos)

    return f"""
<div class="banner" style="border-left-color:#0284C7;">
  <h2>\U0001f4ca Estatísticas de Acesso</h2>
  <p>Medição anônima e sem cookies de quem visita este portfólio: quantas pessoas
     entram, que seções abrem, em que links clicam e por qual caminho chegaram. Esta página
     mostra também, com honestidade, o que <b>não</b> é possível medir.</p>
</div>

<div class="est-destaque" data-estado="carregando">
  <div class="est-numero">
    <span class="est-valor" data-total>—</span>
    <span class="est-rotulo">visitantes desde a publicação</span>
  </div>
  <div class="est-nota" data-estado-txt>Consultando o contador…</div>
</div>

<div class="rule">
  <h3 class="h-serif">Seções mais visitadas</h3>
  <p class="sub">Contagem de visitantes por seção. Os números são atualizados pelo
     serviço de medição a cada 30 minutos.</p>
  <div class="tbl-wrap"><table class="tbl est-tabela">
    <thead><tr><th>Seção</th><th style="width:110px;">Visitantes</th>
      <th style="width:38%;">Proporção</th></tr></thead>
    <tbody>{linhas_secoes}</tbody>
  </table></div>
</div>

<div class="rule">
  <h3 class="h-serif">Esta visita</h3>
  <p class="sub">O que o próprio navegador informa sobre o seu acesso, calculado aqui no seu
     aparelho. Nada disto sai do seu dispositivo nesta tabela — é mostrado para deixar
     transparente exatamente o que a medição enxerga.</p>
  <div class="metadata-grid" data-visita></div>
</div>

<div class="rule">
  <h3 class="h-serif">O que é medido</h3>
  <div class="est-grade">{cartoes_medidos}</div>
</div>

<div class="rule">
  <h3 class="h-serif">O que não é medido — e por quê</h3>
  <div class="notes" style="border-left:4px solid #B45309;">
    <ul>{lista_nao}</ul>
  </div>
</div>

{bloco_compartilhar()}

<div class="est-painel" data-painel-link>
  <div>
    <b>Painel completo</b>
    <p>O detalhamento dia a dia — origens, cliques, países, navegadores e campanhas — fica
       no painel do serviço de medição, visível apenas para você, com envio de um
       resumo diário por e-mail.</p>
  </div>
  <a class="btn btn-primary" data-painel-url href="#" target="_blank" rel="noopener">Abrir painel</a>
</div>
"""


def construir():
    dados = carregar_dados()
    traj = dados["professional_trajectory"]
    foto = preparar_foto() or "foto_curriculo.jpg"

    nav = "".join(
        f'<button class="nav-btn{" on" if slug == "inicio" else ""}" data-goto="{slug}">{esc(rotulo)}</button>'
        for slug, rotulo in SECOES)

    secoes_html = "".join([
        f'<section class="sec" data-sec="inicio">{secao_inicio()}</section>',
        f'<section class="sec" data-sec="artigos">{secao_artigos()}</section>',
        f'<section class="sec" data-sec="websig">{secao_websig()}</section>',
        f'<section class="sec" data-sec="ia">{secao_ia()}</section>',
        f'<section class="sec" data-sec="consultoria">{secao_consultoria()}</section>',
        f'<section class="sec" data-sec="trajetoria">{secao_trajetoria(traj)}</section>',
        f'<section class="sec" data-sec="estatisticas">{secao_estatisticas()}</section>',
    ])

    pagina = f"""<!DOCTYPE html>
<html lang="pt-BR" data-gc="{GOATCOUNTER}">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Dr. Jomil Costa Abreu Sales | Biólogo &amp; Consultoria Ambiental</title>
<meta name="description" content="Portfólio científico do Dr. Jomil Costa Abreu Sales: sensoriamento remoto, WebSIG da APA de Itupararanga, carbono florestal, licenciamento ambiental e docência." />
<meta name="author" content="Jomil Costa Abreu Sales" />
<meta property="og:title" content="Dr. Jomil Costa Abreu Sales | Biólogo e Consultoria Ambiental" />
<meta property="og:description" content="Pesquisa em sensoriamento remoto, carbono florestal e WebSIG interativo da APA de Itupararanga." />
<meta property="og:type" content="website" />
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>&#127807;</text></svg>" />
<style>{CSS}</style>
{script_medicao()}
</head>
<body>
<div class="shell">
  <aside class="sidebar">
    <div class="profile-card">
      <div style="display:flex;align-items:center;margin-bottom:.6rem;">
        <img class="avatar" src="{esc(foto)}" alt="Dr. Jomil Costa Abreu Sales" />
        <div>
          <span class="crbio-badge">CRBio nº 68816/01-D</span>
          <div style="margin-top:.2rem;">
            <b style="font-size:1.05rem;color:#0F172A;font-family:Merriweather,serif;">Dr. Jomil Costa Abreu Sales</b>
          </div>
        </div>
      </div>
      <div style="font-size:.78rem;color:#475569;line-height:1.35;border-top:1px solid #F1F5F9;padding-top:.5rem;">
        <b>Biólogo | Pós-Doutor em Ciências Florestais (ESALQ/USP)</b><br>
        Doutor em Ciências Ambientais (UNESP / TU Berlin)<br>
        <span style="color:#15803D;font-weight:700;">Geotecnologias, Sensoriamento Remoto &amp; IA</span>
      </div>
    </div>
    <p class="mini-cap">Menu Principal</p>
    {nav}
    <p class="mini-cap" style="margin-top:1.1rem;">Links &amp; Identificadores</p>
    <div class="links">{bloco_links()}</div>
  </aside>

  <main class="main">
    <div class="hero-magazine">
      <div class="hero-row">
        <img class="hero-photo" src="{esc(foto)}" alt="" />
        <div>
          <div class="hero-title">Dr. Jomil Costa Abreu Sales</div>
          <div class="hero-subtitle">Biólogo (CRBio nº 68816/01-D) &bull; Pós-Doutor em Ciências Florestais
            (ESALQ/USP) &bull; Geotecnologias, WebSIG &amp; Consultoria Ambiental</div>
        </div>
      </div>
    </div>
    {secoes_html}
    <div class="rodape">
      Dr. Jomil Costa Abreu Sales | Biólogo (CRBio nº 68816/01-D) | Pós-Doutor em Ciências Florestais (ESALQ/USP)<br>
      Portfólio Científico, WebSIG &amp; Consultoria Ambiental &copy; 2026
    </div>
  </main>
</div>
<script>{JS}</script>
</body>
</html>
"""
    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(pagina)

    # .nojekyll impede o GitHub Pages de processar o site com Jekyll
    with open(os.path.join(RAIZ, ".nojekyll"), "w", encoding="utf-8") as f:
        f.write("")

    figuras = sum(len(a["figuras"]) for a in ARTIGOS)
    print(f"index.html escrito: {os.path.getsize(SAIDA) / 1024:.0f} KB")
    print(f"artigos: {len(ARTIGOS)} | figuras referenciadas: {figuras} | foto de perfil: {foto}")


if __name__ == "__main__":
    construir()
