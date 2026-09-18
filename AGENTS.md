# AGENTS.md — UCSA Hub

## Python / Streamlit

- Python 3.12+ — el CLI de streamlit usa `/usr/bin/python3` (3.12); el `python3` por defecto es linuxbrew 3.14 sin streamlit
- No añadir dependencias: `streamlit` + `pandas` cubren todo (charts con `bar_chart`/`line_chart`, sin plotly)
- Columnas de DataFrame con espacios o paréntesis: acceder SIEMPRE con `df["col name"]`, nunca con atributo
- `st.bar_chart`/`st.line_chart`: `color=` espera un color por serie (string), no una lista por barra
- `width="stretch"` reemplaza al deprecado `use_container_width=True`
- Zero deps nuevas; estilos vía CSS inline en `apps/theme.py`
- Determinismo: datos demo con `random.Random(seed)` fijo y `@st.cache_data`
- Código, identificadores y commits en inglés; UI del sitio en español (público UCSA)

## Estructura

- `app.py` — router por `?app=` + landing
- `apps/` — `theme.py` (paleta oficial UCSA), `academico.py`, `rrhh.py`, `ecommerce.py`
- `assets/logo_ucsa.png` — logo oficial de ucsa.edu.py
- `run_lan.sh` — levanta en LAN vía Tailscale (puerto por defecto 8989)

## Verificación

- Smoke test: `streamlit.testing.v1.AppTest.from_file("app.py")` para landing y cada `?app=*`
- El test cazó: `StreamlitColorLengthError` (color por serie) y `AttributeError` en columnas con espacios