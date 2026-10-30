"""UCSA Hub — design system (referencia-v2.html)."""
from __future__ import annotations

import re

_ref_html = open("design/UCSA Hub — Referencia de diseño v2.html").read()
_svg_m = re.search(r"<svg width=\"0\" height=\"0\" style=\"position:absolute\"><defs>.*?</defs></svg>", _ref_html, re.S)
SVG_SPRITE = _svg_m.group(0)

_css_m = re.search(r"<style>(.*?)</style>", _ref_html, re.S)
_REF_CSS = _css_m.group(1).strip()

# Adapt CSS for Streamlit native (not iframe)
_REF_CSS = _REF_CSS.replace(
    "body{margin:0;background:var(--bg);color:var(--navy);font-family:Inter,system-ui,sans-serif}",
    ".stApp{background:#F3F6FB;font-family:Inter,system-ui,sans-serif;color:#0F1C3F}",
)

# Remove .wrap references (we use .block-container)
_REF_CSS = _REF_CSS.replace(".wrap{max-width:1280px;margin:0 auto;padding:72px 32px 40px}", "")

# Append Streamlit-specific adaptations
_EXTRA_CSS = """
/* Streamlit chrome & layout */
header[data-testid="stHeader"],#MainMenu,footer,[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none !important}
.block-container{max-width:1280px !important;padding:72px 32px 40px !important}
[data-testid="stMarkdownContainer"] a{text-decoration:none !important}

/* Hero container (st.container key="hero") */
.st-key-hero{
  background:linear-gradient(135deg,#fff 0%,#EEF1F8 100%);
  border:1px solid #E3E9F3;
  border-radius:28px;
  box-shadow:0 4px 14px rgba(15,40,90,.08);
  padding:32px 36px;
  margin-bottom:20px;
  position:relative;
  overflow:hidden;
}
.st-key-hero::after{
  content:"";
  position:absolute;
  right:-60px;
  top:-80px;
  width:260px;
  height:260px;
  border-radius:50%;
  background:radial-gradient(circle,rgba(30,52,97,.10),transparent 70%);
  pointer-events:none;
}
.st-key-hero [data-testid="stTextInput"] input{
  height:54px;
  border-radius:999px;
  background:#fff;
  border:1px solid #D5DCE8;
  padding:0 18px 0 48px;
  font-size:15px;
  color:#0F1C3F;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%237C889F' stroke-width='1.8' stroke-linecap='round'><circle cx='11' cy='11' r='7'/><path d='m21 21-4.3-4.3'/></svg>");
  background-repeat:no-repeat;
  background-position:18px center;
}
.st-key-hero [data-testid="stTextInput"] input:focus{
  border-color:#1e3461;
  box-shadow:0 0 0 3px rgba(30,52,97,.15);
}
.st-key-hero [data-testid="stTextInput"] > div > div{
  border:0;
  background:transparent;
  box-shadow:none;
}

/* Pills (st.pills) - full width tabs */
[data-testid="stButtonGroup"]{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:6px}
[data-testid="stBaseButton-pills"],[data-testid="stBaseButton-pillsActive"]{
  display:flex;align-items:center;gap:8px;padding:8px 14px;border-radius:12px;border:1px solid transparent;
  background:transparent;font:inherit;font-size:14px;font-weight:500;color:#5B6780;cursor:pointer;
}
[data-testid="stBaseButton-pills"]:hover{background:rgba(30,52,97,.06)}
[data-testid="stBaseButton-pillsActive"]{
  background:#E8ECF5;border-color:#C5CEE4;color:#1e3461;font-weight:700;
}

/* Hide labels for pills and search */
[data-testid="stTextInput"] label{display:none}
[data-testid="stButtonGroup"] label{display:none}

/* Card open/more links */
.open, .open:visited, .open:hover, .open:active,
[data-testid="stMarkdownContainer"] a.open {color:#fff !important; text-decoration:none !important}
.open svg {stroke:#fff !important}
.more, .more:visited, [data-testid="stMarkdownContainer"] a.more {color:#1e3461 !important; text-decoration:none !important}
.more:hover {text-decoration:underline !important}
.card::before {pointer-events:none}

/* Footer */
.foot{margin-top:32px;background:#1e3461;color:#fff;border-radius:20px;padding:24px 28px;box-shadow:0 4px 14px rgba(15,40,90,.08);font-size:13px}
.foot-g{display:grid;grid-template-columns:auto 1fr auto;gap:28px;align-items:center}
.foot img{height:48px;width:auto;display:block}
.foot p{margin:2px 0;color:#C9D3EA}.foot b{color:#fff}
.foot-s{display:flex;gap:14px;flex-wrap:wrap}
.foot a,[data-testid="stMarkdownContainer"] .foot a{color:#fff !important;font-weight:600;opacity:.9;text-decoration:none !important}
.foot a:hover{opacity:1;text-decoration:underline !important}
.foot-b{border-top:1px solid rgba(255,255,255,.15);margin-top:18px;padding-top:14px;font-size:12px;color:#A9B7D6;text-align:center}
@media(max-width:700px){.foot-g{grid-template-columns:1fr}}

/* Kicker tag */
.kicker{display:inline-block;background:#FDF1CF;color:#8A5A00;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;padding:3px 12px;border-radius:999px;margin-bottom:8px}

/* Section pill count */
.pill.blue{background:#E8ECF5;color:#1e3461}
"""

FULL_CSS = _REF_CSS + "\n" + _EXTRA_CSS


def icon(name: str) -> str:
    return f'<svg class="i"><use href="#{name}"/></svg>'


def render_header() -> None:
    """Barra azul fija; 'UCSA Hub' es link a la landing. Solo 'Más info' a la derecha."""
    import streamlit as st

    if not st.session_state.get("_sprite_injected"):
        st.markdown(SVG_SPRITE, unsafe_allow_html=True)
        st.session_state["_sprite_injected"] = True
    st.markdown(
        '<header class="hdr">'
        '<div class="hdr-l">'
        f'<button class="burger" aria-label="Menú">{icon("menu")}</button>'
        '<a href="?" target="_self" style="color:#fff;text-decoration:none;">UCSA Hub</a>'
        '</div>'
        '<nav class="hdr-r">'
        f'<a href="https://github.com/aldocaniza/ucsahub" target="_blank" rel="noopener noreferrer">'
        f'{icon("plus")}<span>Más info</span></a>'
        '</nav>'
        '</header>',
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    return None


def inject_global_css() -> None:
    import streamlit as st

    st.markdown(f"<style>{FULL_CSS}</style>", unsafe_allow_html=True)


# ── Paleta v2 ────────────────────────────────────────────────────────
BLUE = "#1e3461"
BLUE_DARK = "#152849"
BLUE_SOFT = "#E8ECF5"
NAVY = "#0F1C3F"
MUTED = "#5B6780"
PLACEHOLDER = "#94A0B8"
BG = "#F3F6FB"
CARD = "#FFF"
BORDER = "#E3E9F3"
GOLD = "#F2B632"
GOLD_LIGHT = "#FDF1CF"
GOLD_TEXT = "#8A5A00"
GREEN = "#2E9B5A"
GREEN_SOFT = "#E8F6EE"
GREEN_TEXT = "#1F6B3F"
WHITE = "#FFFFFF"

APP_META = {
    "academico": {"cat": "doc", "emoji": "🎓", "tile": "t-doc", "title": "Panel Académico",
                  "subtitle": "Gestión de informaciones académicas", "tag": "Docencia", "badge": "b-doc", "featured": True},
    "rrhh": {"cat": "ins", "emoji": "👥", "tile": "t-ins", "title": "Gestión RRHH",
             "subtitle": "Administración de capital humano", "tag": "Institucional", "badge": "b-ins", "featured": False},
    "ecommerce": {"cat": "com", "emoji": "🛒", "tile": "t-com", "title": "Ecommerce UCSA",
                  "subtitle": "Tienda oficial de la comunidad académica", "tag": "Comercial", "badge": "b-com", "featured": False},
}


def kpi_card_html(label, value, delta=None, good=True):
    delta_html = ""
    if delta:
        cls = "ucsa-kpi-delta--up" if good else "ucsa-kpi-delta--down"
        arrow = "▼" if str(delta).lstrip().startswith("-") else "▲"
        delta_html = f'<div class="ucsa-kpi-delta {cls}">{arrow} {delta}</div>'
    return (f'<div class="ucsa-kpi"><div class="ucsa-kpi-value">{value}</div>'
            f'<div class="ucsa-kpi-label">{label}</div>{delta_html}</div>')


def badge_html(text, variant="blue"):
    return f'<span class="ucsa-badge b-{variant}">{text}</span>'


def render_app_header(title, subtitle):
    import streamlit as st

    st.markdown(
        f'<div class="ucsa-appbar"><div class="ucsa-appbar-title">{title}</div>'
        f'<a class="ucsa-appbar-back" href="?">← Volver al Hub</a></div>'
        f'<div class="ucsa-page-title">{title}</div>'
        f'<p class="ucsa-page-sub">{subtitle}</p>',
        unsafe_allow_html=True,
    )


# compat constants used by apps
PRIMARY = BLUE
PRIMARY_DARK = BLUE_DARK
TEAL = "#4FBFB7"
STEEL = "#2b5672"
SKY = "#5E97FF"
GOLD_DARK = GOLD_TEXT
