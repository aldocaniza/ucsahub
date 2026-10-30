"""UCSA Hub — design system (referencia.html)."""
from __future__ import annotations

import re

ref = open("design/UCSA Hub — Referencia de diseño.html").read() if False else None

# SVG sprite (17 symbols) from referencia.html
import re as _re
_ref_html = open("design/UCSA Hub — Referencia de diseño.html").read()
_svg_m = _re.search(r"<svg width=\"0\" height=\"0\" style=\"position:absolute\"><defs>.*?</defs></svg>", _ref_html, _re.S)
SVG_SPRITE = _svg_m.group(0)

_css_m = _re.search(r"<style>(.*?)</style>", _ref_html, _re.S)
_REF_CSS = _css_m.group(1).strip()

# Adapt: body -> .stApp ; remove .wrap usage later; keep .hdr fixed
_REF_CSS = _REF_CSS.replace(
    "body{margin:0;background:var(--bg);color:var(--navy);font-family:Inter,system-ui,sans-serif}",
    ".stApp{background:#F3F6FB;font-family:Inter,system-ui,sans-serif;color:#0F1C3F}",
)

# Append native Streamlit adaptations
_EXTRA_CSS = """
.block-container{max-width:1280px !important;padding:72px 32px 40px !important}
[data-testid="stMarkdownContainer"] a{text-decoration:none !important}
header[data-testid="stHeader"],#MainMenu,footer,[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none !important}
/* pills -> tabs */
[data-testid="stButtonGroup"]{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:6px}
[data-testid="stBaseButton-pills"],[data-testid="stBaseButton-pillsActive"]{display:flex;align-items:center;gap:8px;padding:8px 14px;border-radius:12px;border:1px solid transparent;background:transparent;font:inherit;font-size:14px;font-weight:500;color:#5B6780;cursor:pointer}
[data-testid="stBaseButton-pills"]:hover{background:rgba(11,102,195,.06)}
[data-testid="stBaseButton-pillsActive"]{background:#E6F0FB;border-color:#B9D4F1;color:#0B66C3;font-weight:700}
/* hide labels */
[data-testid="stTextInput"] label{display:none}
[data-testid="stButtonGroup"] label{display:none}
"""

FULL_CSS = _REF_CSS + "\n" + _EXTRA_CSS


def icon(name: str) -> str:
    return f'<svg class="i"><use href="#{name}"/></svg>'


def render_header(user: str = "acaniza") -> None:
    """Barra azul fija; 'UCSA Hub' es link a la landing."""
    import streamlit as st

    # inject sprite once
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
        f'<a href="#"><svg class="i"><use href="#dl"/></svg><span>Instalar App</span></a>'
        f'<a href="#"><svg class="i"><use href="#plus"/></svg><span>Más info</span></a>'
        f'<a href="#"><svg class="i"><use href="#user"/></svg><span>{user}</span>'
        f'{icon("chev")}</a>'
        '</nav>'
        '</header>',
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    return None


def inject_global_css() -> None:
    import streamlit as st

    st.markdown(f"<style>{FULL_CSS}</style>", unsafe_allow_html=True)


# ── Paleta / meta ────────────────────────────────────────────────────
BLUE = "#0B66C3"
BLUE_DARK = "#0954A0"
BLUE_SOFT = "#E6F0FB"
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
        f'<a class="ucsa-appbar-back" href="/">← Volver al Hub</a></div>'
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
