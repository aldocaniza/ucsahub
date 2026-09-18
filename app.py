"""UCSA Hub — landing que integra proyectos académicos UCSA.

Router por query param `?app=<id>`. Cada app es un stub demo en apps/.
"""
from __future__ import annotations

import streamlit as st

from apps import academico, ecommerce, rrhh
from apps.theme import APP_META, NAVY, STEEL, inject_global_css

st.set_page_config(
    page_title="UCSA Hub — Proyectos Académicos",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_global_css()
_APP_ROUTES = {"academico": academico, "rrhh": rrhh, "ecommerce": ecommerce}


def _landing() -> None:
    from pathlib import Path

    logo = Path(__file__).resolve().parent / "assets" / "logo_ucsa.png"
    top = st.columns([1, 2, 1])
    with top[1]:
        st.image(str(logo), width=230)
    st.markdown(
        f"""
        <div style="text-align:center;padding:0 0 1.6rem;">
          <h1 style="color:{NAVY};font-size:2.3rem;font-weight:800;margin:1rem 0 .4rem;">
            UCSA Hub</h1>
          <p style="color:{STEEL};font-size:1.15rem;max-width:720px;margin:0 auto;">
            Ecosistema digital de la <b>Universidad del Cono Sur de las Américas</b>:
            un solo punto de acceso a todos nuestros proyectos académicos y servicios.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## Proyectos")
    cols = st.columns(3)
    for col, (app_id, meta) in zip(cols, APP_META.items()):
        with col:
            card = (
                f"""<div style="background:#fff;border:1px solid #E3E8EF;border-radius:16px;
                padding:1.6rem 1.4rem;height:100%;box-shadow:0 4px 16px rgba(31,54,101,.07);">
                <div style="font-size:2.2rem;">{meta['icon']}</div>
                <span style="background:{meta['color']}22;color:{meta['color']};font-size:.75rem;
                    font-weight:700;padding:3px 10px;border-radius:999px;">
                    {meta["tag"]}</span>
                <h3 style="color:{NAVY};margin:.7rem 0 .3rem;">{meta["title"]}</h3>
                <p style="color:#5b6b7f;font-size:.95rem;min-height:2.6rem;">{meta["subtitle"]}</p>
                </div>"""
            )
            st.markdown(card, unsafe_allow_html=True)
            if st.button(f"🚀 Abrir {meta['title']}", key=f"open_{app_id}", width="stretch"):
                st.query_params["app"] = app_id
                st.rerun()
            st.markdown(
                f"<a href='?app={app_id}' style='text-decoration:none;color:{STEEL};"
                f"font-size:.85rem;'>↗ Abrir en pestaña nueva</a>",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.markdown(
        f"<h3 style='color:{NAVY};'>🔗 Integración multiplataforma</h3>"
        "<p style='color:#5b6b7f;'>Cada proyecto vive en su propia plataforma. "
        "El Hub los unifica bajo un único acceso.</p>",
        unsafe_allow_html=True,
    )
    c2.markdown(
        f"<h3 style='color:{NAVY};'>🔐 Acceso institucional</h3>"
        "<p style='color:#5b6b7f;'>Preparado para autenticación única UCSA "
        "y roles por facultad o dependencia.</p>",
        unsafe_allow_html=True,
    )
    c3.markdown(
        f"<h3 style='color:{NAVY};'>📱 Accesible desde cualquier dispositivo</h3>"
        "<p style='color:#5b6b7f;'>Sitio responsive. En red local o vía Tailscale "
        "desde cualquier ubicación.</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="margin:2.4rem 0 1rem;text-align:center;color:#8b9aad;font-size:.85rem;">
          Universidad del Cono Sur de las Américas — UCSA ·
          <a href="https://ucsa.edu.py">ucsa.edu.py</a> · Demo con datos de ejemplo
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_app(app_id: str) -> None:
    app = _APP_ROUTES[app_id]
    app.run()


def main() -> None:
    app_id = st.query_params.get("app")
    if app_id in _APP_ROUTES:
        _render_app(str(app_id))
    else:
        _landing()


main()