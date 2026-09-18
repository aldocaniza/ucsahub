"""Branding compartido UCSA — paleta oficial de ucsa.edu.py."""
from __future__ import annotations

# Paleta extraída del sitio oficial (Wix): azules institucionales + teal
NAVY = "#1F3665"        # azul marino principal
STEEL = "#2b5672"       # azul acero
SKY = "#5E97FF"         # celeste
TEAL = "#4FBFB7"        # teal de acento
DARK = "#0F1E38"        # fondo oscuro de hero
LIGHT = "#F5F7FA"       # fondo claro

APP_META = {
    "academico": {
        "icon": "🎓",
        "title": "Panel Académico",
        "subtitle": "Gestión de informaciones académicas",
        "tag": "Docencia",
        "color": NAVY,
    },
    "rrhh": {
        "icon": "👥",
        "title": "Gestión RRHH",
        "subtitle": "Administración de capital humano",
        "tag": "Institucional",
        "color": STEEL,
    },
    "ecommerce": {
        "icon": "🛒",
        "title": "Ecommerce UCSA",
        "subtitle": "Tienda oficial de la comunidad académica",
        "tag": "Comercial",
        "color": TEAL,
    },
}


def inject_global_css() -> None:
    """Tipografía y reset visual compartidos (una sola inyección por sesión)."""
    import streamlit as st

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}
        .stApp {{ background-color: {LIGHT}; }}
        /* header nativo oculto: escondemos sidebar y chrome */
        #MainMenu, footer, header {{ visibility: hidden; }}
        .block-container {{ padding-top: 2rem; max-width: 1100px; }}
        /* baseline fijo para no saltar al navegar entre apps */
        .stButton > button, .stLinkButton > a {{
            border-radius: 10px; font-weight: 600; border: none;
        }}
        .stButton > button:hover {{ border: none; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_topbar(title: str | None = None) -> None:
    """Barra superior con logo UCSA y título opcional."""
    import streamlit as st
    from pathlib import Path

    logo = Path(__file__).resolve().parent.parent / "assets" / "logo_ucsa.png"
    col_logo, col_title, col_back = st.columns([1, 3, 1], vertical_alignment="center")
    with col_logo:
        st.image(str(logo), width=150)
    with col_title:
        if title:
            st.markdown(
                f"<div style='color:{NAVY};font-size:1.15rem;font-weight:800;'>"
                f"{title}</div>",
                unsafe_allow_html=True,
            )
    with col_back:
        st.link_button("← Volver al Hub", "/", width="stretch")