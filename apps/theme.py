"""UCSA Hub — design system (referencia.html)."""
from __future__ import annotations

SVG_SPRITE = '<svg width="0" height="0" style="position:absolute"><defs>\n<symbol id="menu" viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16"/></symbol>\n<symbol id="dl" viewBox="0 0 24 24"><path d="M20 16.5A4.5 4.5 0 0 0 17.5 8h-1A6 6 0 1 0 4 14.5M12 12v9m0 0-3-3m3 3 3-3"/></symbol>\n<symbol id="plus" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M12 8v8M8 12h8"/></symbol>\n<symbol id="user" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></symbol>\n<symbol id="chev" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></symbol>\n<symbol id="search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></symbol>\n<symbol id="shield" viewBox="0 0 24 24"><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/></symbol>\n<symbol id="grid" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></symbol>\n<symbol id="cap" viewBox="0 0 24 24"><path d="m2 9 10-5 10 5-10 5z"/><path d="M6 11v5c0 1.5 3 3 6 3s6-1.5 6-3v-5"/></symbol>\n<symbol id="cart" viewBox="0 0 24 24"><circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.7 12.4a1 1 0 0 0 1 .6H18a1 1 0 0 0 1-.8L21 7H6"/></symbol>\n<symbol id="brief" viewBox="0 0 24 24"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V4h6v3M3 13h18"/></symbol>\n<symbol id="star" viewBox="0 0 24 24"><path fill="currentColor" d="m12 2.5 2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4 6.1 20.5l1.2-6.5L2.5 9.4l6.6-.9z"/></symbol>\n<symbol id="ext" viewBox="0 0 24 24"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></symbol>\n<symbol id="info" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="currentColor" stroke="none"/><path d="M12 11v6M12 7.5v.5" stroke="#fff" stroke-width="2.4"/></symbol>\n<symbol id="link" viewBox="0 0 24 24"><path d="M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/></symbol>\n<symbol id="lock" viewBox="0 0 24 24"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></symbol>\n<symbol id="phone" viewBox="0 0 24 24"><rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/></symbol>\n</defs></svg>'

def icon(name):
    return f'<svg class="i"><use href="#{name}"/></svg>'

_RENDER_HEADER = None

def render_header(user="acaniza"):
    return (
        '<header class="hdr">'
        '<div class="hdr-l">'
        f'<button class="burger" aria-label="Menú">{icon("menu")}</button>UCSA Hub'
        '</div>'
        '<nav class="hdr-r">'
        f'<a href="#"><svg class="i"><use href="#dl"/></svg><span>Instalar App</span></a>'
        f'<a href="#"><svg class="i"><use href="#plus"/></svg><span>Más info</span></a>'
        f'<a href="#"><svg class="i"><use href="#user"/></svg><span>{user}</span>'
        f'{icon("chev")}</a>'
        '</nav>'
        '</header>'
    )

def render_sidebar():
    return None

def inject_global_css():
    import streamlit as st
    st.markdown(
        "<style>"
        "#MainMenu, footer, header[data-testid=\"stHeader\"], [data-testid=\"stToolbar\"],"
        " [data-testid=\"stDecoration\"], [data-testid=\"stSidebar\"], [data-testid=\"stSidebarCollapsedControl\"]"
        " {display:none !important}"
        ".stApp {background:#F3F6FB !important}"
        ".block-container {max-width:100% !important; padding:0 !important}"
        "[data-testid=\"stMarkdownContainer\"] a {text-decoration:none}"
        "</style>",
        unsafe_allow_html=True,
    )

_REF_CSS = '@import url(\'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap\');\n:root{color-scheme:light;--blue:#0B66C3;--blue-dark:#0954A0;--blue-soft:#E6F0FB;--navy:#0F1C3F;--muted:#5B6780;--placeholder:#94A0B8;--bg:#F3F6FB;--card:#fff;--border:#E3E9F3;--gold:#F2B632;--gold-soft:#FDF1CF;--gold-text:#8A5A00;--green:#2E9B5A;--green-soft:#E8F6EE;--green-text:#1F6B3F;--shadow:0 4px 14px rgba(15,40,90,.08);--shadow-hover:0 10px 26px rgba(15,40,90,.14);box-sizing:border-box;padding-top:env(safe-area-inset-top,0px)}\n*,*::before,*::after{box-sizing:inherit}\nbody{margin:0;background:var(--bg);color:var(--navy);font-family:Inter,system-ui,sans-serif}\na{text-decoration:none;color:inherit}\nsvg.i{width:1em;height:1em;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;flex:none}\n/* HEADER */\n.hdr{position:fixed;top:0;left:0;right:0;z-index:10;height:48px;background:linear-gradient(90deg,var(--blue),var(--blue-dark));color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 12px}\n.hdr-l{display:flex;align-items:center;gap:8px;font-weight:700;font-size:18px}\n.burger{width:36px;height:36px;border-radius:8px;background:rgba(255,255,255,.18);display:grid;place-items:center;font-size:20px;border:0;color:#fff;cursor:pointer}\n.hdr-r{display:flex;gap:20px;font-size:13px;font-weight:500}\n.hdr-r a{display:flex;align-items:center;gap:6px;font-size:13px}\n.hdr-r svg{font-size:16px}\n/* LAYOUT */\n.wrap{max-width:1280px;margin:0 auto;padding:72px 32px 40px}\n/* HERO */\n.hero{background:linear-gradient(135deg,#fff 0%,#EEF4FC 100%);border:1px solid var(--border);border-radius:28px;box-shadow:var(--shadow);padding:32px 36px;display:grid;grid-template-columns:2.2fr 1.1fr .9fr;gap:24px;align-items:center;margin-bottom:20px}\n.brand{display:flex;align-items:center;gap:22px}\n.logo{width:96px;height:96px;border-radius:22px;background:#fff;box-shadow:0 6px 16px rgba(15,40,90,.18);display:grid;place-items:center;flex:none}\n.logo b{width:72px;height:72px;border-radius:14px;background:linear-gradient(160deg,var(--blue),var(--blue-dark));color:#fff;display:grid;place-items:center;font-size:22px;font-weight:800;letter-spacing:.5px}\n.vline{width:3px;height:80px;border-radius:3px;background:linear-gradient(180deg,var(--blue),#8FC1F2);flex:none}\n.hero h1{margin:0;font-size:28px;font-weight:800;line-height:1.15}\n.hero p{margin:6px 0 0;font-size:15px;color:var(--muted)}\n.search{position:relative}\n.search svg{position:absolute;left:18px;top:50%;transform:translateY(-50%);color:#7C889F;font-size:18px}\n.search input{width:100%;height:54px;border-radius:999px;border:1px solid #D5DCE8;background:#fff;padding:0 18px 0 48px;font:inherit;font-size:15px;color:var(--navy);outline:0}\n.search input::placeholder{color:var(--placeholder)}\n.search input:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(11,102,195,.15)}\n.secure{display:flex;align-items:center;gap:12px;background:var(--green-soft);border:1px solid #BFE3CD;border-radius:999px;padding:10px 18px}\n.secure i{width:36px;height:36px;border-radius:50%;background:var(--green);color:#fff;display:grid;place-items:center;font-size:18px;flex:none}\n.secure strong{display:block;font-size:13px;color:var(--green-text)}\n.secure span{font-size:11px;color:var(--muted)}\n/* TABS */\n.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:6px}\n.tab{display:flex;align-items:center;gap:8px;padding:8px 14px;border-radius:12px;border:1px solid transparent;background:transparent;font:inherit;font-size:14px;font-weight:500;color:var(--muted);cursor:pointer}\n.tab:hover{background:rgba(11,102,195,.06)}\n.tab.on{background:var(--blue-soft);border-color:#B9D4F1;color:var(--blue);font-weight:700}\n/* SECTION HEAD */\n.sec{display:flex;align-items:center;gap:14px;margin:22px 0 14px}\n.sec-ic{width:46px;height:46px;border-radius:14px;background:var(--gold-soft);border:1px solid #F2D98A;display:grid;place-items:center;color:#F2A900;font-size:22px}\n.sec-ic.blue{background:var(--blue-soft);border-color:#B9D4F1;color:var(--blue)}\n.sec h2{margin:0;font-size:22px;font-weight:800}\n.sec small{display:block;font-size:13px;color:var(--muted);margin-top:2px}\n.pill{margin-left:auto;background:var(--gold-soft);color:var(--gold-text);font-size:12px;font-weight:700;padding:6px 14px;border-radius:999px}\n/* CARDS */\n.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}\n.card{position:relative;overflow:hidden;background:var(--card);border:1px solid var(--border);border-radius:16px;box-shadow:var(--shadow);padding:20px;min-height:170px;display:flex;flex-direction:column;justify-content:space-between;transition:transform .2s,box-shadow .2s}\n.card:hover{transform:translateY(-3px);box-shadow:var(--shadow-hover)}\n.card.feat::before{content:"";position:absolute;left:0;right:0;top:0;height:4px;background:linear-gradient(90deg,#F2B632,#F8DC8A)}\n.c-top{display:flex;gap:16px;align-items:flex-start;padding-right:96px}\n.tile{width:64px;height:64px;border-radius:16px;display:grid;place-items:center;font-size:32px;flex:none}\n.t-doc{background:linear-gradient(135deg,#E6F0FB,#CFE2F8)}.t-com{background:linear-gradient(135deg,#FDF1CF,#FBE3A0)}.t-ins{background:linear-gradient(135deg,#E8F6EE,#CBEBD8)}\n.c-title{font-size:16px;font-weight:700;line-height:1.25}\n.c-desc{font-size:13px;color:var(--muted);margin-top:4px}\n.badge{position:absolute;top:18px;right:18px;font-size:11px;font-weight:700;padding:4px 12px;border-radius:999px}\n.b-doc{background:var(--blue-soft);color:var(--blue)}.b-com{background:var(--gold-soft);color:var(--gold-text)}.b-ins{background:var(--green-soft);color:var(--green-text)}\n.c-bot{display:flex;justify-content:space-between;align-items:center;margin-top:14px}\n.more{display:flex;align-items:center;gap:6px;font-size:13px;font-weight:600;color:var(--blue);padding-left:80px}\n.more:hover{text-decoration:underline}\n.open{display:flex;align-items:center;gap:8px;background:var(--blue);color:#fff;font-size:14px;font-weight:700;padding:10px 18px;border-radius:12px;box-shadow:0 3px 8px rgba(11,102,195,.35)}\n.open:hover{background:var(--blue-dark);transform:translateY(-1px)}\n/* FEATURES + FOOTER */\n.feats{margin-top:32px}\n.feat-t{background:#fff;border:1px solid var(--border);border-radius:16px;box-shadow:var(--shadow);padding:20px}\n.feat-t i{width:44px;height:44px;border-radius:12px;background:var(--blue-soft);color:var(--blue);display:grid;place-items:center;font-size:22px;margin-bottom:12px}\n.feat-t b{font-size:15px;display:block}.feat-t span{font-size:13px;color:var(--muted);display:block;margin-top:4px}\n.foot{text-align:center;font-size:12px;color:var(--muted);padding:24px 0 0}.foot a{color:var(--blue)}\n.empty{display:none;font-size:13px;color:var(--muted);padding:8px 2px}\n@media(max-width:992px){.grid{grid-template-columns:repeat(2,1fr)}.hero{grid-template-columns:1fr}}\n@media(max-width:700px){.hdr-r span{display:none}.hdr-r{gap:14px}.wrap{padding:68px 16px 32px}.hero{padding:22px}.hero h1{font-size:22px}.brand{gap:14px}.logo{width:72px;height:72px}.logo b{width:54px;height:54px;font-size:16px}.vline{height:60px}}\n@media(max-width:640px){.grid{grid-template-columns:1fr}}'

APP_META = {
    "academico": {"cat":"doc","emoji":"🎓","tile":"t-doc","title":"Panel Académico","subtitle":"Gestión de informaciones académicas","tag":"Docencia","badge":"b-doc","featured":True},
    "rrhh": {"cat":"ins","emoji":"👥","tile":"t-ins","title":"Gestión RRHH","subtitle":"Administración de capital humano","tag":"Institucional","badge":"b-ins","featured":False},
    "ecommerce": {"cat":"com","emoji":"🛒","tile":"t-com","title":"Ecommerce UCSA","subtitle":"Tienda oficial de la comunidad académica","tag":"Comercial","badge":"b-com","featured":False},
}

BLUE="#0B66C3"; BLUE_DARK="#0954A0"; BLUE_SOFT="#E6F0FB"; NAVY="#0F1C3F"; MUTED="#5B6780"; PLACEHOLDER="#94A0B8"; BG="#F3F6FB"; CARD="#FFF"; BORDER="#E3E9F3"; GOLD="#F2B632"; GOLD_LIGHT="#FDF1CF"; GOLD_TEXT="#8A5A00"; GREEN="#2E9B5A"; GREEN_SOFT="#E8F6EE"; GREEN_TEXT="#1F6B3F"; WHITE="#FFFFFF"
PRIMARY=BLUE; PRIMARY_DARK=BLUE_DARK; TEAL="#4FBFB7"; STEEL="#2b5672"; SKY="#5E97FF"; GOLD_DARK=GOLD_TEXT

def kpi_card_html(label, value, delta=None, good=True):
    delta_html=""
    if delta:
        cls="ucsa-kpi-delta--up" if good else "ucsa-kpi-delta--down"
        arrow="▼" if str(delta).lstrip().startswith("-") else "▲"
        delta_html=f'<div class="ucsa-kpi-delta {cls}">{arrow} {delta}</div>'
    return f'<div class="ucsa-kpi"><div class="ucsa-kpi-value">{value}</div><div class="ucsa-kpi-label">{label}</div>{delta_html}</div>'

def badge_html(text, variant="blue"):
    return f'<span class="ucsa-badge b-{variant}">{text}</span>'

def render_app_header(title, subtitle):
    import streamlit as st
    st.markdown(f'<div class="ucsa-appbar"><div class="ucsa-appbar-title">{title}</div><a class="ucsa-appbar-back" href="/">← Volver al Hub</a></div><div class="ucsa-page-title">{title}</div><p class="ucsa-page-sub">{subtitle}</p>', unsafe_allow_html=True)
