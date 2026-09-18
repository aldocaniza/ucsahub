"""Stub: Panel Académico — gestión de informaciones académicas (datos demo)."""
from __future__ import annotations

import random

import pandas as pd
import streamlit as st

from apps.theme import PRIMARY, TEAL, kpi_card_html, render_app_header

FACULTADES = [
    "Ciencias Empresariales",
    "Ingeniería y Tecnología",
    "Ciencias de la Salud",
    "Ciencias Jurídicas",
    "Humanidades y Educación",
]
CARRERAS = {
    "Ciencias Empresariales": ["Administración", "Contabilidad", "Marketing"],
    "Ingeniería y Tecnología": ["Ingeniería Informática", "Ingeniería Industrial"],
    "Ciencias de la Salud": ["Medicina", "Enfermería"],
    "Ciencias Jurídicas": ["Derecho", "Ciencias Políticas"],
    "Humanidades y Educación": ["Psicología", "Educación"],
}
NOMBRES = [
    "Ana López", "Carlos Ramírez", "María Benítez", "Jorge Acosta", "Lucía Giménez",
    "Diego Villalba", "Sofía Duarte", "Martín Cardozo", "Valentina Ortiz", "Andrés Rojas",
]


@st.cache_data(show_spinner=False)
def _alumnos() -> pd.DataFrame:
    rng = random.Random(42)
    rows = []
    for i in range(60):
        fac = rng.choice(FACULTADES)
        carrera = rng.choice(CARRERAS[fac])
        rows.append(
            {
                "Cédula": f"{rng.randint(1, 4)}.{rng.randint(100, 999)}.{rng.randint(100, 999)}",
                "Alumno": rng.choice(NOMBRES) + f" {rng.randint(1, 99)}",
                "Facultad": fac,
                "Carrera": carrera,
                "Curso": rng.randint(1, 5),
                "Promedio": round(rng.uniform(2.0, 5.0), 2),
            }
        )
    return pd.DataFrame(rows)


def _kpi_row() -> None:
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi_card_html("Alumnos activos", "12 480", "+3,1 %"), unsafe_allow_html=True)
    k2.markdown(kpi_card_html("Materias ofertadas", "214", "+8"), unsafe_allow_html=True)
    k3.markdown(kpi_card_html("Docentes", "387", "+12"), unsafe_allow_html=True)
    k4.markdown(kpi_card_html("Tasa de aprobación", "84,6 %", "+1,8 %"), unsafe_allow_html=True)


def run() -> None:
    render_app_header(
        "Panel Académico",
        "Demo stub — datos de ejemplo. Los datos reales se conectan a las plataformas académicas.",
    )

    _kpi_row()
    df = _alumnos()

    c1, c2 = st.columns([1, 2])
    with c1:
        with st.container(key="panel_tabla", border=False):
            st.markdown('<div class="ucsa-panel-title">Alumnos — tabla</div>', unsafe_allow_html=True)
            fac = st.selectbox("Filtrar por facultad", ["Todas"] + FACULTADES)
            filt = df if fac == "Todas" else df[df.Facultad == fac]
            st.dataframe(
                filt[["Cédula", "Alumno", "Carrera", "Curso", "Promedio"]].head(15),
                width="stretch",
                hide_index=True,
            )
    with c2:
        with st.container(key="panel_chart", border=False):
            st.markdown('<div class="ucsa-panel-title">Alumnos por facultad</div>', unsafe_allow_html=True)
            dist = filt.Facultad.value_counts()
            st.bar_chart(dist, color=PRIMARY)
            promedio = filt.Promedio.mean()
            st.markdown(
                f'<div class="ucsa-panel-note" style="color:{TEAL};">'
                f'Promedio general del filtro: {promedio:.2f} / 5.00</div>',
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    run()