"""UCSA Hub — landing (nativa, sin iframe)."""
from __future__ import annotations

import base64
import html as _html
from pathlib import Path

import streamlit as st

from apps import academico, ecommerce, rrhh
from apps.theme import (
    APP_META,
    SVG_SPRITE,
    icon,
    inject_global_css,
    render_header,
)

st.set_page_config(
    page_title="UCSA Hub — Proyectos Académicos",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"Get help": None, "Report a bug": None},
)

inject_global_css()

_APP_ROUTES = {"academico": academico, "rrhh": rrhh, "ecommerce": ecommerce}


def _logo_b64() -> str | None:
    logo = Path(__file__).resolve().parent / "assets" / "logo_ucsa.png"
    if not logo.exists():
        return None
    return base64.b64encode(logo.read_bytes()).decode()


def _visible(meta, cat, q):
    # cat is internal: "all", "doc", "com", "ins"
    ok_cat = cat == "all" or meta["cat"] == cat
    texto = f'{meta["title"]} {meta["subtitle"]} {meta["tag"]}'.lower()
    return ok_cat and (not q or q in texto)


def _card(app_id, meta):
    featured = bool(meta["featured"])
    cls = "card feat" if featured else "card"
    cat = meta["cat"]
    tile = meta["tile"]
    emoji = meta["emoji"]
    title = _html.escape(meta["title"])
    subtitle = _html.escape(meta["subtitle"])
    tag = _html.escape(meta["tag"])
    data_t = f"{meta['title']} {meta['subtitle']} {meta['tag']}".lower()
    badge_cls = meta["badge"]
    return (
        f'<article class="{cls}" data-cat="{cat}" data-t="{_html.escape(data_t)}">'
        f'<div class="c-top"><div class="tile {tile}">{emoji}</div>'
        f'<div><div class="c-title">{title}</div>'
        f'<div class="c-desc">{subtitle}</div></div></div>'
        f'<span class="badge {badge_cls}">{tag}</span>'
        f'<div class="c-bot">'
        f'<a class="more" href="javascript:void(0)">{icon("info")}Más información</a>'
        f'<a class="open" href="?app={app_id}" target="_self">{icon("ext")}Abrir</a>'
        f'</div></article>'
    )


def _landing():
    if not st.session_state.get("_sprite_injected"):
        st.markdown(SVG_SPRITE, unsafe_allow_html=True)
        st.session_state["_sprite_injected"] = True

    render_header()

    logo_b64 = _logo_b64()
    LOGO_HTML = f'<img src="data:image/png;base64,{logo_b64}" alt="UCSA">' if logo_b64 else '<div class="logo-placeholder">UCSA</div>'

    # ── HERO ──────────────────────────────────────────────────────────
    BRAND_HTML = (
        f'<div class="brand">'
        f'<div class="logo">{LOGO_HTML}</div>'
        f'<div class="vline"></div>'
        f'<div><span class="kicker">Portal institucional</span>'
        f'<h1>UCSA Hub - Portal de Proyectos Académicos</h1>'
        f'<p>Todos tus proyectos en un solo lugar.</p></div>'
        f'</div>'
    )
    SECURE_HTML = (
        '<div class="secure">'
        f'<i>{icon("shield")}</i>'
        '<div><strong>Acceso Institucional</strong><span>Según tu rol</span></div>'
        '</div>'
    )

    with st.container(key="hero"):
        c1, c2, c3 = st.columns([2.2, 1.1, 0.9], vertical_alignment="center")
        with c1:
            st.markdown(BRAND_HTML, unsafe_allow_html=True)
        with c2:
            q = st.text_input("Buscar", placeholder="Buscar proyectos",
                              label_visibility="collapsed", key="hero_q").strip().lower()
        with c3:
            st.markdown(SECURE_HTML, unsafe_allow_html=True)

    # ── TABS ──────────────────────────────────────────────────────────
    cat = st.pills(
        "Categoría",
        ["Todas", "Docencia", "Comercial", "Institucional"],
        default="Todas",
        label_visibility="collapsed",
        key="cat",
    ) or "Todas"

    # Map display names to internal cat values
    cat_map = {"Todas": "all", "Docencia": "doc", "Comercial": "com", "Institucional": "ins"}
    cat_val = cat_map.get(cat, "all")

    featured_ids = [aid for aid, m in APP_META.items() if m["featured"] and _visible(m, cat_val, q)]
    other_ids = [aid for aid, m in APP_META.items() if not m["featured"] and _visible(m, cat_val, q)]

    if not (featured_ids or other_ids):
        st.markdown('<div class="empty" style="display:block">Sin resultados. Probá con otro término o categoría.</div>',
                    unsafe_allow_html=True)
        _features_footer(logo_b64)
        return

    # Featured section
    if featured_ids:
        st.markdown(
            '<div class="sec"><div class="sec-ic"><svg class="i"><use href="#star"/></svg></div>'
            '<div><h2>Aplicaciones destacadas</h2><small>Accesos recomendados para tu trabajo</small></div>'
            '<span class="pill">Recomendadas</span></div>',
            unsafe_allow_html=True,
        )
        cards = "".join(_card(aid, APP_META[aid]) for aid in featured_ids)
        st.markdown(f'<div class="grid">{cards}</div>', unsafe_allow_html=True)

    # All projects section with count pill
    if other_ids:
        pill_html = f'<span class="pill" style="background:#E8ECF5;color:#1e3461">{len(other_ids)} proyectos</span>'
        st.markdown(
            f'<div class="sec"><div class="sec-ic blue"><svg class="i"><use href="#grid"/></svg></div>'
            f'<div><h2>Todos los proyectos</h2><small>Resto de aplicaciones disponibles</small></div>'
            f'{pill_html}</div>',
            unsafe_allow_html=True,
        )
        cards = "".join(_card(aid, APP_META[aid]) for aid in other_ids)
        st.markdown(f'<div class="grid">{cards}</div>', unsafe_allow_html=True)

    _features_footer(logo_b64)


def _features_footer(logo_b64):
    LOGO_FOOTER = f'<img src="data:image/png;base64,{logo_b64}" alt="UCSA Universidad">' if logo_b64 else ''
    st.markdown(
        '<div class="grid feats">'
        f'<div class="feat-t"><i>{icon("link")}</i>'
        '<b>Integración multiplataforma</b>'
        '<span>Cada proyecto vive en su propia plataforma. El Hub los unifica bajo un único acceso.</span></div>'
        f'<div class="feat-t"><i>{icon("lock")}</i>'
        '<b>Acceso institucional</b>'
        '<span>Preparado para autenticación única UCSA y roles por facultad o dependencia.</span></div>'
        f'<div class="feat-t"><i>{icon("phone")}</i>'
        '<b>Accesible desde cualquier dispositivo</b>'
        '<span>Sitio responsive. Accedé desde cualquier dispositivo, donde estés.</span></div>'
        '</div>',
        unsafe_allow_html=True,
    )
    # Institutional footer
    st.markdown(
        f'<footer class="foot">'
        f'<div class="foot-g">'
        f'{LOGO_FOOTER}'
        f'<div>'
        f'<p><b>Universidad del Cono Sur de las Américas</b></p>'
        f'<p>Sgto. Gauto 972 casi Venezuela, Asunción</p>'
        f'<p>Lunes a Viernes: 08:00 - 21:00 h</p>'
        f'</div>'
        f'<div class="foot-s">'
        f'<a href="https://www.ucsa.edu.py" target="_blank" rel="noopener">ucsa.edu.py</a>'
        f'<a href="https://www.instagram.com/universidaducsa/" target="_blank" rel="noopener">Instagram</a>'
        f'<a href="https://www.facebook.com/universidaducsa" target="_blank" rel="noopener">Facebook</a>'
        f'<a href="https://www.linkedin.com/school/ucsapy/" target="_blank" rel="noopener">LinkedIn</a>'
        f'<a href="https://www.youtube.com/@UniversidadUCSA" target="_blank" rel="noopener">YouTube</a>'
        f'</div>'
        f'</div>'
        f'<div class="foot-b">UCSA Hub · Demo con datos de ejemplo</div>'
        f'</footer>',
        unsafe_allow_html=True,
    )


def main():
    app_id = st.query_params.get("app")
    if app_id in _APP_ROUTES:
        render_header()
        _APP_ROUTES[app_id].run()
    else:
        _landing()


main()
