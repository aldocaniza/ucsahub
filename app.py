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
    ok_cat = cat == "Todas" or meta["tag"] == cat
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
    # sprite once
    if not st.session_state.get("_sprite_injected"):
        st.markdown(SVG_SPRITE, unsafe_allow_html=True)
        st.session_state["_sprite_injected"] = True
    render_header("acaniza")

    logo_b64 = _logo_b64()
    logo_html = (f'<img src="data:image/png;base64,{logo_b64}" '
                 f'style="width:72px;height:72px;object-fit:contain" alt="UCSA"/>'
                 if logo_b64 else "<b>UCSA</b>")

    # hero
    st.markdown(
        f'<section class="hero">'
        f'<div class="brand">'
        f'<div class="logo">{logo_html}</div>'
        f'<div class="vline"></div>'
        f'<div><h1>UCSA Hub - Portal de Proyectos Académicos</h1>'
        f'<p>Todos tus proyectos en un solo lugar.</p></div>'
        f'</div>'
        f'<div class="search"><svg class="i"><use href="#search"/></svg>'
        f'<input id="q" type="text" placeholder="Buscar proyectos" disabled></div>'
        f'<div class="secure"><i><svg class="i"><use href="#shield"/></svg></i>'
        f'<div><strong>Acceso Institucional</strong><span>Según tu rol</span></div></div>'
        f'</section>',
        unsafe_allow_html=True,
    )

    # native pills + search
    c1, c2 = st.columns([3, 1.2])
    with c1:
        cat = st.pills("Categoría", ["Todas", "Docencia", "Comercial", "Institucional"],
                       default="Todas", label_visibility="collapsed", key="cat") or "Todas"
    with c2:
        q = st.text_input("Buscar", placeholder="Buscar proyectos",
                          label_visibility="collapsed", key="q").strip().lower()

    featured_ids = [aid for aid, m in APP_META.items() if m["featured"] and _visible(m, cat, q)]
    other_ids = [aid for aid, m in APP_META.items() if not m["featured"] and _visible(m, cat, q)]

    if not (featured_ids or other_ids):
        st.markdown('<div class="empty" style="display:block">Sin resultados. Probá con otro término o categoría.</div>',
                    unsafe_allow_html=True)
        # features + footer
        _features_footer()
        return

    if featured_ids:
        st.markdown(
            '<div class="sec"><div class="sec-ic"><svg class="i"><use href="#star"/></svg></div>'
            '<div><h2>Aplicaciones destacadas</h2><small>Accesos recomendados para tu trabajo</small></div>'
            '<span class="pill">Recomendadas</span></div>',
            unsafe_allow_html=True,
        )
        cards = "".join(_card(aid, APP_META[aid]) for aid in featured_ids)
        st.markdown(f'<div class="grid">{cards}</div>', unsafe_allow_html=True)

    if other_ids:
        st.markdown(
            '<div class="sec"><div class="sec-ic blue"><svg class="i"><use href="#grid"/></svg></div>'
            '<div><h2>Todos los proyectos</h2><small>Resto de aplicaciones disponibles</small></div></div>',
            unsafe_allow_html=True,
        )
        cards = "".join(_card(aid, APP_META[aid]) for aid in other_ids)
        st.markdown(f'<div class="grid">{cards}</div>', unsafe_allow_html=True)

    _features_footer()


def _features_footer():
    st.markdown(
        '<div class="grid feats">'
        '<div class="feat-t"><i><svg class="i"><use href="#link"/></svg></i>'
        '<b>Integración multiplataforma</b>'
        '<span>Cada proyecto vive en su propia plataforma. El Hub los unifica bajo un único acceso.</span></div>'
        '<div class="feat-t"><i><svg class="i"><use href="#lock"/></svg></i>'
        '<b>Acceso institucional</b>'
        '<span>Preparado para autenticación única UCSA y roles por facultad o dependencia.</span></div>'
        '<div class="feat-t"><i><svg class="i"><use href="#phone"/></svg></i>'
        '<b>Accesible desde cualquier dispositivo</b>'
        '<span>Sitio responsive. Accedé desde cualquier dispositivo, donde estés.</span></div>'
        '</div>'
        '<div class="foot">Universidad del Cono Sur de las Américas — UCSA · '
        '<a href="https://ucsa.edu.py">ucsa.edu.py</a> · Demo con datos de ejemplo</div>',
        unsafe_allow_html=True,
    )


def main():
    app_id = st.query_params.get("app")
    if app_id in _APP_ROUTES:
        render_header("acaniza")
        _APP_ROUTES[app_id].run()
    else:
        _landing()


main()
