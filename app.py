"""UCSA Hub — landing que integra proyectos académicos UCSA.

Router por query param `?app=<id>`. Cada app es un stub demo en apps/.
Look "Portal Institucional Corporativo" (header sólido azul, hero con búsqueda
live, cards con borde dorado en la destacada, badges pill pastel).
"""
from __future__ import annotations

import streamlit as st

from apps import academico, ecommerce, rrhh
from apps.theme import (
    APP_META,
    GOLD_DARK,
    GOLD_LIGHT,
    PRIMARY,
    badge_html,
    inject_global_css,
    render_header,
    render_sidebar,
)

st.set_page_config(
    page_title="UCSA Hub — Proyectos Académicos",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"Get help": None, "Report a bug": None},
)

inject_global_css()
render_sidebar()

_APP_ROUTES = {"academico": academico, "rrhh": rrhh, "ecommerce": ecommerce}
_CATEGORIES = ["Todas"] + sorted({meta["tag"] for meta in APP_META.values()})


def _hero() -> None:
    from pathlib import Path

    logo = Path(__file__).resolve().parent / "assets" / "logo_ucsa.png"
    cta = (
        f'<a href="#ucsa-proyectos" style="display:block;text-align:center;'
        f'background:{PRIMARY};color:#fff;font-weight:700;padding:.62rem 1rem;'
        f'border-radius:10px;text-decoration:none;margin-top:.85rem;">'
        f'Explorar proyectos ↓</a>'
    )
    with st.container(key="hero"):
        c_logo, c_text, c_search = st.columns([1, 1.7, 1], vertical_alignment="center")
        with c_logo:
            st.image(str(logo), width=190)
        with c_text:
            st.markdown(
                '<div class="ucsa-hero-kicker">Portal Institucional</div>'
                '<div class="ucsa-hero-title">Ecosistema digital de la '
                'Universidad del Cono Sur de las Américas</div>'
                '<div class="ucsa-hero-sub">Un solo punto de acceso a todos '
                'nuestros proyectos académicos y servicios institucionales.</div>',
                unsafe_allow_html=True,
            )
        with c_search:
            st.text_input(
                "Buscar proyecto",
                key="hero_search",
                placeholder="Buscar proyecto…",
                label_visibility="collapsed",
            )
            st.markdown(cta, unsafe_allow_html=True)


def _projects() -> None:
    st.markdown(
        '<div id="ucsa-proyectos" style="scroll-margin-top:150px;"></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="ucsa-section-title">Proyectos académicos</div>', unsafe_allow_html=True)

    pills = st.pills("Categoría", _CATEGORIES, key="hero_cat", default="Todas") if hasattr(st, "pills") else None
    categoria = pills or "Todas"
    query = st.session_state.get("hero_search", "").strip().lower()

    shown = []
    for app_id, meta in APP_META.items():
        if categoria != "Todas" and meta["tag"] != categoria:
            continue
        haystack = f'{meta["title"]} {meta["subtitle"]} {meta["tag"]}'.lower()
        if query and query not in haystack:
            continue
        shown.append(app_id)

    st.markdown(
        f'<div class="ucsa-section-caption">Mostrando {len(shown)} de {len(APP_META)} '
        f'proyectos — usá la búsqueda o filtrá por categoría.</div>',
        unsafe_allow_html=True,
    )

    if not shown:
        st.markdown(
            f'<div class="ucsa-section-caption">Sin resultados para "{query}". '
            f'Probá con otro término.</div>',
            unsafe_allow_html=True,
        )
        return

    cols = st.columns(3)
    for col, app_id in zip(cols, shown):
        meta = APP_META[app_id]
        with col:
            st.markdown(_card_html(app_id, meta), unsafe_allow_html=True)
            if st.button(
                f"Abrir {meta['title']}",
                key=f"open_{app_id}",
                width="stretch",
                type="primary",
            ):
                st.query_params["app"] = app_id
                st.rerun()
            st.markdown(
                f'<a class="ucsa-card-link" href="?app={app_id}">↗ Abrir en pestaña nueva</a>',
                unsafe_allow_html=True,
            )


def _card_html(app_id: str, meta: dict) -> str:
    featured = bool(meta["featured"])
    cls = "ucsa-card ucsa-card--featured" if featured else "ucsa-card"
    corner = badge_html(meta["tag"], meta["pill"])
    if featured:
        corner = (
            f'<span class="ucsa-badge" style="background:{GOLD_LIGHT};color:{GOLD_DARK};">'
            f'★ Recomendada</span>'
        )
    return f"""
    <div class="{cls}">
      <div class="ucsa-card-top">
        <div class="ucsa-card-icon">{meta["icon"]}</div>
        <div style="display:flex;flex-direction:column;align-items:flex-end;gap:.3rem;">{corner}</div>
      </div>
      <div class="ucsa-card-title">{meta["title"]}</div>
      <div class="ucsa-card-desc">{meta["subtitle"]}.</div>
      <div class="ucsa-card-open"></div>
    </div>
    """


def _features() -> None:
    tiles = [
        ("🔗", "Integración multiplataforma",
         "Cada proyecto vive en su propia plataforma. El Hub los unifica bajo un único acceso."),
        ("🔐", "Acceso institucional",
         "Preparado para autenticación única UCSA y roles por facultad o dependencia."),
        ("📱", "Accesible desde cualquier dispositivo",
         "Sitio responsive. En red local o vía Tailscale desde cualquier ubicación."),
    ]
    cols = st.columns(3)
    for col, (icon, title, desc) in zip(cols, tiles):
        with col:
            st.markdown(
                f'<div class="ucsa-tile"><div class="ucsa-tile-icon">{icon}</div>'
                f'<div class="ucsa-tile-title">{title}</div>'
                f'<div class="ucsa-tile-desc">{desc}</div></div>',
                unsafe_allow_html=True,
            )


def _footer() -> None:
    st.markdown(
        '<div class="ucsa-footer">Universidad del Cono Sur de las Américas — UCSA · '
        '<a href="https://ucsa.edu.py">ucsa.edu.py</a> · Demo con datos de ejemplo</div>',
        unsafe_allow_html=True,
    )


def main() -> None:
    app_id = st.query_params.get("app")
    if app_id in _APP_ROUTES:
        _APP_ROUTES[app_id].run()
    else:
        render_header()
        _hero()
        _projects()
        _features()
        _footer()


main()