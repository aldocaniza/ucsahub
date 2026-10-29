"""UCSA Hub — landing que integra proyectos académicos UCSA.

Router por query param `?app=<id>`. La landing se renderiza dentro de un iframe
(coplando el HTML y el CSS de `design/UCSA Hub — Referencia de diseño.html`).
"""
from __future__ import annotations

import base64
import html as _html
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from apps import academico, ecommerce, rrhh
from apps.theme import (
    APP_META,
    SVG_SPRITE,
    _REF_CSS as REF_CSS,
    icon,
    render_header,
)

st.set_page_config(
    page_title="UCSA Hub — Proyectos Académicos",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"Get help": None, "Report a bug": None},
)

from apps.theme import inject_global_css

inject_global_css()

_APP_ROUTES = {"academico": academico, "rrhh": rrhh, "ecommerce": ecommerce}


def _logo_b64() -> str | None:
    logo = Path(__file__).resolve().parent / "assets" / "logo_ucsa.png"
    if not logo.exists():
        return None
    return base64.b64encode(logo.read_bytes()).decode()


def _card(app_id: str, meta: dict) -> str:
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
        f'<a class="more" href="#">{icon("info")}Más información</a>'
        f'<a class="open" href="?app={app_id}" target="_top">{icon("ext")}Abrir</a>'
        f"</div></article>"
    )


def _landing() -> str:
    logo_b64 = _logo_b64()
    if logo_b64:
        logo_html = (
            f'<img src="data:image/png;base64,{logo_b64}" '
            f'style="width:72px;height:72px;object-fit:contain" alt="UCSA"/>'
        )
    else:
        logo_html = "<b>UCSA</b>"

    featured_ids = [aid for aid, m in APP_META.items() if m["featured"]]
    other_ids = [aid for aid, m in APP_META.items() if not m["featured"]]

    featured_cards = "".join(_card(aid, APP_META[aid]) for aid in featured_ids)
    other_cards = "".join(_card(aid, APP_META[aid]) for aid in other_ids)

    featured_section = ""
    if featured_ids:
        featured_section = (
            '<div class="sec"><div class="sec-ic"><svg class="i"><use href="#star"/></svg></div>'
            '<div><h2>Aplicaciones destacadas</h2><small>Accesos recomendados para tu trabajo</small></div>'
            '<span class="pill">Recomendadas</span></div>'
            f'<div class="grid">{featured_cards}</div>'
        )

    other_section = ""
    if other_ids:
        other_section = (
            '<div class="sec"><div class="sec-ic blue"><svg class="i"><use href="#grid"/></svg></div>'
            '<div><h2>Todos los proyectos</h2><small>Resto de aplicaciones disponibles</small></div></div>'
            f'<div class="grid">{other_cards}</div>'
        )

    return f"""
<main class="wrap">
  <section class="hero">
    <div class="brand">
      <div class="logo">{logo_html}</div>
      <div class="vline"></div>
      <div><h1>UCSA Hub - Portal de Proyectos Académicos</h1><p>Todos tus proyectos en un solo lugar.</p></div>
    </div>
    <div class="search"><svg class="i"><use href="#search"/></svg><input id="q" type="text" placeholder="Buscar proyectos"></div>
    <div class="secure"><i><svg class="i"><use href="#shield"/></svg></i><div><strong>Acceso Institucional</strong><span>Según tu rol</span></div></div>
  </section>

  <div class="tabs" id="tabs">
    <button class="tab on" data-cat="all"><svg class="i"><use href="#grid"/></svg>Todas</button>
    <button class="tab" data-cat="doc"><svg class="i"><use href="#cap"/></svg>Docencia</button>
    <button class="tab" data-cat="com"><svg class="i"><use href="#cart"/></svg>Comercial</button>
    <button class="tab" data-cat="ins"><svg class="i"><use href="#brief"/></svg>Institucional</button>
  </div>

  {featured_section}
  {other_section}
  <div class="empty" id="empty">Sin resultados. Probá con otro término o categoría.</div>

  <div class="grid feats">
    <div class="feat-t"><i><svg class="i"><use href="#link"/></svg></i><b>Integración multiplataforma</b><span>Cada proyecto vive en su propia plataforma. El Hub los unifica bajo un único acceso.</span></div>
    <div class="feat-t"><i><svg class="i"><use href="#lock"/></svg></i><b>Acceso institucional</b><span>Preparado para autenticación única UCSA y roles por facultad o dependencia.</span></div>
    <div class="feat-t"><i><svg class="i"><use href="#phone"/></svg></i><b>Accesible desde cualquier dispositivo</b><span>Sitio responsive. Accedé desde cualquier dispositivo, donde estés.</span></div>
  </div>
  <div class="foot">Universidad del Cono Sur de las Américas — UCSA · <a href="https://ucsa.edu.py">ucsa.edu.py</a> · Demo con datos de ejemplo</div>
</main>
"""


def _landing_page() -> None:
    header = render_header("acaniza")
    script = """<script>
(function(){
  var cat="all",q=document.getElementById("q"),cards=[].slice.call(document.querySelectorAll(".card"));
  function run(){
    var t=q.value.trim().toLowerCase(),n=0;
    cards.forEach(function(c){var ok=(cat==="all"||c.dataset.cat===cat)&&(!t||c.dataset.t.indexOf(t)>-1);c.style.display=ok?"":"none";if(ok)n++;});
    document.getElementById("empty").style.display=n?"none":"block";
  }
  document.getElementById("tabs").addEventListener("click",function(e){
    var b=e.target.closest(".tab");if(!b)return;
    [].forEach.call(document.querySelectorAll(".tab"),function(x){x.classList.remove("on")});
    b.classList.add("on");cat=b.dataset.cat;run();
  });
  q.addEventListener("input",run);
})();
</script>"""
    full = (
        "<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1, viewport-fit=cover'>"
        "<title>UCSA Hub</title>"
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">'
        f"<style>{REF_CSS}</style></head><body>"
        f"{SVG_SPRITE}{header}{_landing()}{script}</body></html>"
    )
    components.html(full, height=1500, scrolling=True)


def main() -> None:
    app_id = st.query_params.get("app")
    if app_id in _APP_ROUTES:
        _APP_ROUTES[app_id].run()
    else:
        _landing_page()


main()
