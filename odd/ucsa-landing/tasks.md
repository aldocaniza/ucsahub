# UCSA Hub — Landing (mirror Engram)

Cmd: Reconciliar este mirror con `odd/tasks/ucsa-landing.md` en cada transición de tarea.

## Feature: ucsahub-landing
Objetivo: landing Streamlit con branding oficial UCSA (colores de ucsa.edu.py: navy #1F3665, azul acero #2b5672, celeste #5E97FF, teal #4FBFB7; logo oficial en assets/) que integra 3 proyectos demo (panel académico, RRHH, ecommerce). Script run_lan.sh para Tailscale en puerto 8989. Zero deps nuevas (pandas nativo).

## Tasks
| Id | Descripción | Estado |
|----|-------------|--------|
| T-1 | Landing branding + 3 cards | done |
| T-2 | Stub Panel Académico | done |
| T-3 | Stub Gestión RRHH | done |
| T-4 | Stub Ecommerce | done |
| T-5 | Router app.py + CSS institucional | done |
| T-6 | run_lan.sh (Tailscale, puerto 8989) | done |
| T-7 | Smoke test headless | done |

## Evidencia de commits
## Evidencia de commits
- `8d66504` chore: scaffold · `7c7b408` feat: landing + 3 apps stub · `bb7a230` feat: run_lan.sh