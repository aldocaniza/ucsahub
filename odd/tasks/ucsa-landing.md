# UCSA Hub — Landing Page

## Goal
Landing page Streamlit que integra proyectos académicos UCSA (Universidad del Cono Sur de las Américas). Demo con 3 apps stub funcionales + script para levantar en LAN vía Tailscale.

## Tasks
1. `T-1` Landing page con branding UCSA (logo oficial, paleta navy #1F3665 / #2b5672 / #5E97FF / teal #4FBFB7) y hero con las 3 cards
2. `T-2` App stub: Panel Académico (KPIs, tabla alumnos, chart por facultad)
3. `T-3` App stub: Gestión RRHH (KPIs, tabla empleados, chart por departamento)
4. `T-4` App stub: Ecommerce UCSA (KPIs ventas, catálogo en PYG, chart ventas)
5. `T-5` Router app.py (query param `?app=`) + diseño institucional CSS
6. `T-6` Script run_lan.sh: Tailscale IP + Streamlit en puerto 8989
7. `T-7` Smoke test headless (streamlit run con timeout)

## Decisions
- Demo apps = stubs funcionales con datos de ejemplo (decisión usuario)
- Colores y logo oficiales de ucsa.edu.py (Wix; extensión azul/navy institucional)
- Zero deps nuevas: pandas nativo para charts (sin plotly), estilos vía CSS inline
- Idioma del sitio: español (público UCSA Paraguay)

## Evidencia de commits
- (pendiente)

## Resultado smoke test (AppTest)
- landing / academico / rrhh / ecommerce: todos renderizan sin excepción
- Bugs cazados por test: StreamlitColorLengthError (color por serie, no por barra) y AttributeError en columnas con espacio ("Asistencias mes", "Ingresos (Gs)") → bracket access
- streamlit CLI usa /usr/bin/python3 (3.12); python3 por defecto es linuxbrew 3.14 sin streamlit