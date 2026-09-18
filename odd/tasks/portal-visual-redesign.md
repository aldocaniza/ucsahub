# UCSA Hub — Portal Institucional Corporativo (Rediseño Visual)

## Goal
Reestilizar el Hub UCSA completo (landing + 3 apps stub) con estética "Portal Institucional Corporativo" / enterprise SaaS: header azul sólido fijo, fondo gris azulado claro, tarjetas blancas con borde superior dorado de acento, badges pill pastel, tipografía sans-serif moderna, mucho whitespace. Mantener toda la funcionalidad existente (router ?app=, filtros, charts demo deterministas) y zero deps nuevas.

## Tasks
1. `T-1` Design system en `apps/theme.py`: paleta corporativa (#1565C0→#0D47A1, #EEF2F7, #1A1A2E, #6B7280, #F5A623/#FDE68A, #2E7D32) + `inject_global_css()` completo (header fijo, hero, cards, badges pill, botones, KPIs, inputs, chart wrappers) + helpers `badge_html`, `card_html`, `kpi_card_html`, `render_header`, `render_app_header`
2. `T-2` Landing `app.py`: header azul sólido fijo (logo+nombre izq, hamburger/sidebar, acciones der: "Instalar App", "Más info", usuario), hero blanco (logo izq, título+desc centro, búsqueda + botón der con filtrado live), pills de categoría, cards con borde superior dorado + badge "Recomendada" en card destacada, tiles de features, footer
3. `T-3` Apps (`academico.py`, `rrhh.py`, `ecommerce.py`): header corporativo, jerarquía título/subtítulo, KPIs en cards blancas, charts y tablas dentro de cards blancas, badges tag pill
4. `T-4` Smoke test AppTest (AppTest.from_file) en las 4 rutas: landing, academico, rrhh, ecommerce
5. `T-5` Commit work-unit en `feature/ucsa-landing` (Conventional Commit)

## Decisions
- Paleta corporativa del prompt (azul #1565C0→#0D47A1, oro #F5A623) reemplaza la navy/teal anterior como look principal; se mantienen acentos institucionales heredados donde encajan (teal en charts)
- Header fijo vía CSS position:fixed + padding-top en .block-container; menú hamburger = sidebar nativo de Streamlit reestilizado en azul (menu de apps + volver al Hub)
- Hero con búsqueda live: st.container(key=...) reestilizado por CSS (permite st.text_input real); cards estáticas en HTML puro (control total de estilo)
- "Instalar App" y "Más info" = anchors estilizados (repo GitHub / ucsa.edu.py), sin JS fake; chip de usuario estático "AC"
- UI siempre en español; código/identificadores en inglés

## Constraints (AGENTS.md)
- Zero deps nuevas: streamlit + pandas; charts bar_chart/line_chart (sin plotly), color= string por serie
- Columnas con espacios/paréntesis: df["col"] siempre
- width="stretch" (no use_container_width); st.pills verificar con hasattr (1.58 lo tiene)
- Datos demo deterministas: random.Random(seed) + @st.cache_data
- Smoke test: AppTest con /usr/bin/python3 (3.12), no python3 linuxbrew

## Evidencia de commits
- 9af76d4 feat: corporate institutional portal redesign for UCSA Hub (5 archivos + feature doc + mirror)

## Fallback delegación
- gentle-ai-worker intentado 2× para T-1..T-3 (surfaces 5 archivos, spec detallada): falló en ambos intentos con "assistant returned no final report" sin tocar archivos. Role inusable en esta sesión → implementación inline en el parent con las mismas surfaces (fallback permitido por el Work Routing Ladder).

## Resultado smoke test (AppTest)
- landing: PASS (1 text_input hero_search, 3 botones Abrir)
- ?app=academico / rrhh / ecommerce: PASS sin excepciones
- Bug cazado por el test: st.page_link("app.py") rompe en AppTest bare (KeyError 'url_pathname') → sidebar navega con anchors HTML (.ucsa-sidenav)