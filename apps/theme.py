"""UCSA Hub — design system "Portal Institucional Corporativo".

Paleta corporativa (azul institucional + acentos dorado/verde/teal), CSS global
y helpers HTML compartidos por la landing y las apps stub.
"""
from __future__ import annotations

# ── Paleta corporativa ────────────────────────────────────────────────
PRIMARY = "#1565C0"        # azul primario (botones, acentos)
PRIMARY_DARK = "#0D47A1"   # azul oscuro (header, gradiente)
BG = "#EEF2F7"             # fondo general (gris azulado claro)
TEXT = "#1A1A2E"           # texto principal
MUTED = "#6B7280"          # texto secundario
GOLD = "#F5A623"           # acento dorado (cards destacadas)
GOLD_LIGHT = "#FDE68A"     # dorado pastel (badges)
GOLD_DARK = "#B45309"      # texto sobre dorado pastel
GREEN = "#2E7D32"          # seguridad / confirmación / deltas positivos
RED = "#D32F2F"            # deltas negativos
WHITE = "#FFFFFF"
BORDER = "#E3E8EF"

# Acentos heredados de la paleta oficial ucsa.edu.py (charts y compat)
NAVY = PRIMARY_DARK
STEEL = "#2b5672"
SKY = "#5E97FF"
TEAL = "#4FBFB7"

# Variantes pastel para badges pill: (fondo claro, texto del mismo tono)
PILLS = {
    "blue": ("#E3EDFB", PRIMARY),
    "gold": (GOLD_LIGHT, GOLD_DARK),
    "green": ("#E4F2E5", GREEN),
    "teal": ("#E0F4F2", "#0F7A6F"),
    "gray": ("#ECEFF3", "#4B5563"),
}

APP_META = {
    "academico": {
        "icon": "🎓",
        "title": "Panel Académico",
        "subtitle": "Gestión de informaciones académicas",
        "tag": "Docencia",
        "pill": "blue",
        "featured": True,
    },
    "rrhh": {
        "icon": "👥",
        "title": "Gestión RRHH",
        "subtitle": "Administración de capital humano",
        "tag": "Institucional",
        "pill": "teal",
        "featured": False,
    },
    "ecommerce": {
        "icon": "🛒",
        "title": "Ecommerce UCSA",
        "subtitle": "Tienda oficial de la comunidad académica",
        "tag": "Comercial",
        "pill": "gold",
        "featured": False,
    },
}


def badge_html(text: str, variant: str = "blue") -> str:
    """Badge tipo pill: fondo pastel + texto del mismo tono oscurecido."""
    bg, fg = PILLS[variant]
    return f'<span class="ucsa-badge" style="background:{bg};color:{fg};">{text}</span>'


def kpi_card_html(label: str, value: str, delta: str | None = None, good: bool = True) -> str:
    """Card blanca con metric: número grande, label capitalizado, delta coloreado.

    Flecha según signo del delta (▲ sube / ▼ baja); color verde si `good`. """
    delta_html = ""
    if delta:
        cls = "ucsa-kpi-delta--up" if good else "ucsa-kpi-delta--down"
        arrow = "▼" if delta.lstrip().startswith("-") else "▲"
        delta_html = f'<div class="ucsa-kpi-delta {cls}">{arrow} {delta}</div>'
    return (
        f'<div class="ucsa-kpi"><div class="ucsa-kpi-value">{value}</div>'
        f'<div class="ucsa-kpi-label">{label}</div>{delta_html}</div>'
    )


def render_header() -> None:
    """Barra corporativa del portal (sticky bajo el chrome nativo de Streamlit)."""
    import streamlit as st
    from pathlib import Path

    logo = Path(__file__).resolve().parent.parent / "assets" / "logo_ucsa.png"
    logo_html = f'<img src="data:image/png;base64,{_b64(logo)}" alt="UCSA"/>' if logo.exists() else ""
    st.markdown(
        f"""
        <div class="ucsa-header">
          <div class="ucsa-header-brand">
            {logo_html} UCSA Hub
          </div>
          <div class="ucsa-header-actions">
            <a class="ucsa-btn" href="https://github.com/aldocaniza/ucsahub" target="_blank">⬇ Instalar App</a>
            <a class="ucsa-btn" href="https://ucsa.edu.py" target="_blank">ℹ Más info</a>
            <span class="ucsa-avatar">AC</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    """Menú lateral corporativo: brand + enlaces a las apps (hamburger nativo)."""
    import streamlit as st
    from pathlib import Path

    logo = Path(__file__).resolve().parent.parent / "assets" / "logo_ucsa.png"
    logo_html = f'<img src="data:image/png;base64,{_b64(logo)}" alt="UCSA"/>' if logo.exists() else ""
    st.markdown(
        f'<div class="ucsa-sidebar-brand">{logo_html} UCSA Hub</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="ucsa-sidebar-label">Navegación</div>', unsafe_allow_html=True)
    nav = [
        ("/", "🏠", "Inicio — Landing"),
        ("/?app=academico", "🎓", "Panel Académico"),
        ("/?app=rrhh", "👥", "Gestión RRHH"),
        ("/?app=ecommerce", "🛒", "Ecommerce UCSA"),
    ]
    for href, icon, label in nav:
        st.markdown(
            f'<a class="ucsa-sidenav" href="{href}">{icon} {label}</a>',
            unsafe_allow_html=True,
        )


def render_app_header(title: str, subtitle: str) -> None:
    """Barra corporativa + título de página para las apps."""
    import streamlit as st

    st.markdown(
        f"""
        <div class="ucsa-appbar">
          <div class="ucsa-appbar-title">{title}</div>
          <a class="ucsa-appbar-back" href="/">← Volver al Hub</a>
        </div>
        <div class="ucsa-page-title">{title}</div>
        <p class="ucsa-page-sub">{subtitle}</p>
        """,
        unsafe_allow_html=True,
    )


def _b64(path) -> str:
    import base64

    with open(path, "rb") as fh:
        return base64.b64encode(fh.read()).decode()


# CSS del design system (inyectado una vez por sesión)
_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {{ font-family: 'Inter', system-ui, 'Segoe UI', sans-serif; }}
.stApp, [data-testid="stAppViewContainer"] {{ background-color: {BG}; }}

/* Chrome nativo -> azul corporativo (mantiene el hamburger real del sidebar) */
header[data-testid="stHeader"] {{
    background: linear-gradient(90deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%);
    border-bottom: 1px solid rgba(255, 255, 255, 0.18);
}}
header[data-testid="stHeader"] [data-testid="stToolbar"] {{ display: none; }}
header[data-testid="stHeader"] [data-testid="stMainMenu"] {{ color: #fff; }}
header[data-testid="stHeader"] [data-testid="stSidebarCollapsedControl"],
header[data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] {{ color: #fff; }}

[data-testid="stMainBlockContainer"], .block-container {{ max-width: 1180px; padding-top: 1.1rem; }}

/* Sidebar corporativo */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #FFFFFF 0%, #F6F9FE 100%);
    border-right: 1px solid {BORDER};
}}
.ucsa-sidebar-brand {{
    display: flex; align-items: center; gap: 0.55rem;
    background: linear-gradient(90deg, {PRIMARY}, {PRIMARY_DARK});
    color: #fff; font-weight: 800; font-size: 0.95rem;
    padding: 0.65rem 0.9rem; border-radius: 12px; margin-bottom: 0.8rem;
}}
.ucsa-sidebar-brand img {{ height: 26px; border-radius: 6px; }}
.ucsa-sidebar-label {{
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; color: {MUTED}; margin: 0.4rem 0 0.35rem;
}}
.ucsa-sidenav {{
    display: flex; align-items: center; gap: 0.5rem; text-decoration: none;
    color: {TEXT}; font-weight: 600; font-size: 0.9rem;
    padding: 0.5rem 0.7rem; border-radius: 10px; margin: 0.15rem 0;
}}
.ucsa-sidenav:hover {{ background: #EDF3FB; color: {PRIMARY}; text-decoration: none; }}

/* Botones e inputs */
.stButton > button {{ border-radius: 10px; font-weight: 600; border: none;
    transition: filter .15s ease; }}
.stButton > button:hover {{ border: none; filter: brightness(1.08); }}
.stButton > button[kind="primary"] {{ background: {PRIMARY}; }}
.stLinkButton > a {{ border-radius: 10px; font-weight: 600; }}
[data-testid="stTextInput"] > div > div {{ border-radius: 10px; border-color: {BORDER}; }}
[data-testid="stTextInput"] > div > div:focus-within {{ border-color: {PRIMARY}; }}
[data-testid="stPills"] button {{ border-radius: 999px; font-weight: 600; }}

/* Barra corporativa del portal (sticky bajo el chrome nativo) */
.ucsa-header {{
    position: sticky; top: 3.45rem; z-index: 90;
    display: flex; align-items: center; justify-content: space-between; gap: 1rem;
    background: linear-gradient(90deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%);
    color: #fff; padding: 0.65rem 1.2rem; border-radius: 14px;
    box-shadow: 0 4px 16px rgba(13, 71, 161, 0.22);
}}
.ucsa-header-brand {{ display: flex; align-items: center; gap: 0.6rem;
    font-weight: 800; font-size: 1.05rem; }}
.ucsa-header-brand img {{ height: 34px; border-radius: 8px; }}
.ucsa-header-actions {{ display: flex; align-items: center; gap: 0.5rem; }}
.ucsa-btn {{
    display: inline-flex; align-items: center; gap: 0.4rem; text-decoration: none;
    font-weight: 700; font-size: 0.82rem; padding: 0.42rem 0.9rem; border-radius: 999px;
    border: 1.5px solid rgba(255, 255, 255, 0.55); color: #fff;
    background: rgba(255, 255, 255, 0.08); transition: background .15s ease;
}}
.ucsa-btn:hover {{ background: rgba(255, 255, 255, 0.18); color: #fff; }}
.ucsa-avatar {{
    width: 32px; height: 32px; border-radius: 50%;
    background: rgba(255, 255, 255, 0.22); border: 1.5px solid #fff;
    display: inline-flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 0.78rem; color: #fff;
}}

/* Hero */
.st-key-hero {{
    background: {WHITE}; border-radius: 20px;
    box-shadow: 0 10px 30px rgba(21, 101, 192, 0.10);
    padding: 2rem 2.2rem;
}}
.ucsa-hero-kicker {{ display: inline-block; font-size: 0.7rem; font-weight: 800;
    letter-spacing: 0.09em; text-transform: uppercase; color: {GOLD_DARK};
    background: {GOLD_LIGHT}; padding: 0.2rem 0.7rem; border-radius: 999px; margin-bottom: 0.6rem; }}
.ucsa-hero-title {{ font-size: 1.55rem; font-weight: 800; color: {TEXT};
    margin: 0 0 0.35rem; line-height: 1.25; }}
.ucsa-hero-sub {{ font-size: 0.95rem; color: {MUTED}; margin: 0; line-height: 1.55; }}

/* Secciones */
.ucsa-section-title {{ font-size: 1.25rem; font-weight: 800; color: {TEXT};
    margin: 1.7rem 0 0.3rem; }}
.ucsa-section-caption {{ font-size: 0.9rem; color: {MUTED}; margin: 0 0 1rem; }}

/* Cards de apps y tiles */
.ucsa-card {{
    background: {WHITE}; border: 1px solid {BORDER}; border-radius: 16px;
    padding: 1.5rem 1.4rem; height: 100%; display: flex; flex-direction: column; gap: 0.55rem;
    box-shadow: 0 4px 16px rgba(21, 101, 192, 0.06);
    transition: box-shadow .15s ease, transform .15s ease;
}}
.ucsa-card:hover {{ box-shadow: 0 10px 28px rgba(21, 101, 192, 0.12);
    transform: translateY(-2px); }}
.ucsa-card--featured {{ border-top: 4px solid {GOLD}; }}
.ucsa-card-top {{ display: flex; align-items: center; justify-content: space-between; }}
.ucsa-card-icon {{ font-size: 1.9rem; line-height: 1; }}
.ucsa-card-title {{ font-size: 1.15rem; font-weight: 800; color: {TEXT}; margin: 0; }}
.ucsa-card-desc {{ font-size: 0.9rem; color: {MUTED}; margin: 0; line-height: 1.5; flex: 1; }}
.ucsa-card-open {{ margin-top: 0.85rem; }}
.ucsa-card-link {{ text-decoration: none; color: {PRIMARY}; font-weight: 600;
    font-size: 0.85rem; display: inline-block; margin-top: 0.55rem; }}
.ucsa-card-link:hover {{ text-decoration: underline; }}

.ucsa-tile {{ background: {WHITE}; border: 1px solid {BORDER}; border-radius: 16px;
    padding: 1.3rem 1.2rem; height: 100%;
    box-shadow: 0 2px 10px rgba(21, 101, 192, 0.05); }}
.ucsa-tile-icon {{ font-size: 1.4rem; }}
.ucsa-tile-title {{ font-size: 0.98rem; font-weight: 800; color: {TEXT}; margin: 0.5rem 0 0.3rem; }}
.ucsa-tile-desc {{ font-size: 0.85rem; color: {MUTED}; margin: 0; line-height: 1.5; }}

/* Badges pill */
.ucsa-badge {{ display: inline-flex; align-items: center; gap: 0.25rem;
    font-size: 0.7rem; font-weight: 700; padding: 0.22rem 0.7rem;
    border-radius: 999px; letter-spacing: 0.02em; }}

/* KPIs */
.ucsa-kpi {{ background: {WHITE}; border: 1px solid {BORDER}; border-radius: 14px;
    padding: 1rem 1.1rem; box-shadow: 0 2px 10px rgba(21, 101, 192, 0.05); }}
.ucsa-kpi-value {{ font-size: 1.65rem; font-weight: 800; color: {TEXT}; line-height: 1.1; }}
.ucsa-kpi-label {{ font-size: 0.72rem; font-weight: 700; color: {MUTED};
    letter-spacing: 0.05em; text-transform: uppercase; margin-top: 0.3rem; }}
.ucsa-kpi-delta {{ font-size: 0.78rem; font-weight: 700; margin-top: 0.35rem; }}
.ucsa-kpi-delta--up {{ color: {GREEN}; }}
.ucsa-kpi-delta--down {{ color: {RED}; }}

/* Paneles blancos para charts/tablas (contenedores con key="panel_*") */
div[class*="st-key-panel"] {{
    background: {WHITE}; border: 1px solid {BORDER}; border-radius: 16px;
    padding: 0.9rem 1.3rem 0.4rem; box-shadow: 0 4px 16px rgba(21, 101, 192, 0.06);
    margin: 0.2rem 0 1.4rem;
}}
.ucsa-panel-title {{ font-size: 1rem; font-weight: 800; color: {TEXT};
    margin: 0 0 0.9rem; }}
.ucsa-panel-note {{ font-size: 0.85rem; font-weight: 700; margin-top: 0.9rem; }}

/* Barra de app */
.ucsa-appbar {{
    display: flex; align-items: center; justify-content: space-between; gap: 1rem;
    background: linear-gradient(90deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%);
    color: #fff; padding: 0.7rem 1.2rem; border-radius: 14px; margin-bottom: 1.1rem;
    box-shadow: 0 4px 16px rgba(13, 71, 161, 0.22);
}}
.ucsa-appbar-title {{ font-weight: 800; font-size: 1.02rem; }}
.ucsa-appbar-back {{ color: #fff; text-decoration: none; font-weight: 700; font-size: 0.85rem;
    padding: 0.35rem 0.8rem; border-radius: 999px;
    border: 1.5px solid rgba(255, 255, 255, 0.55); background: rgba(255, 255, 255, 0.08); }}
.ucsa-appbar-back:hover {{ color: #fff; background: rgba(255, 255, 255, 0.18); }}

/* Título de página en apps */
.ucsa-page-title {{ font-size: 1.55rem; font-weight: 800; color: {TEXT}; margin: 0.2rem 0 0.2rem; }}
.ucsa-page-sub {{ font-size: 0.9rem; color: {MUTED}; margin: 0 0 1.1rem; }}

/* Footer */
.ucsa-footer {{ text-align: center; color: #8b9aad; font-size: 0.82rem;
    margin: 2.8rem 0 1rem; }}
.ucsa-footer a {{ color: {PRIMARY}; text-decoration: none; }}
.ucsa-footer a:hover {{ text-decoration: underline; }}
</style>
"""


def inject_global_css() -> None:
    """Tipografía, paleta y componentes del design system (una sola inyección)."""
    import streamlit as st

    st.markdown(_CSS, unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )