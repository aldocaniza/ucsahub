# UCSA Hub 🎓

Landing page (Streamlit) que integra proyectos académicos de la **Universidad del Cono Sur de las Américas** (UCSA). Branding oficial: logo y paleta extraídos de [ucsa.edu.py](https://ucsa.edu.py).

## Incluye

| Ruta | App | Descripción |
|------|-----|-------------|
| `/` | Landing | Hub con cards de acceso a cada proyecto |
| `/?app=academico` | Panel Académico | KPIs, alumnos por facultad, tabla filtrable |
| `/?app=rrhh` | Gestión RRHH | KPIs, colaboradores por departamento, nómina |
| `/?app=ecommerce` | Ecommerce UCSA | Ingresos, catálogo en ₲, top ventas |

Las 3 apps son **stubs funcionales** con datos de ejemplo (seed determinista). Reemplazables por las aplicaciones reales de cada plataforma.

## Requisitos

- Python 3.12+ con `streamlit` y `pandas` (ya instalados: `.local` / sistema)
- `tailscale` opcional (para acceso remoto)

## Levantar en LAN (Tailscale)

```bash
./run_lan.sh          # puerto por defecto 8989
./run_lan.sh 9090     # puerto custom
```

El script detecta la IP de Tailscale (`tailscale ip -4`), hace fallback a la IP LAN si no, y busca puerto libre. Imprime la URL lista para compartir: `http://100.xx.xx.xx:8989`.

## Estructura

```
app.py               # router + landing (query param ?app=)
apps/theme.py        # paleta UCSA, CSS global, topbar
apps/academico.py    # stub panel académico
apps/rrhh.py         # stub gestión RRHH
apps/ecommerce.py    # stub ecommerce
assets/logo_ucsa.png # logo oficial
run_lan.sh           # levanta en LAN/Tailscale
```

## Conectar las apps reales

En `app.py` el router usa `_APP_ROUTES`. Cuando tengas las URLs reales de cada plataforma, apostá cada card a su enlace externo (ver `APP_META` en `apps/theme.py`) o reemplazá cada stub por la app final.

```bash
streamlit run app.py   # desarrollo local
```