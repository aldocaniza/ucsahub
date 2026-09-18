"""Stub: Gestión RRHH UCSA — capital humano (datos demo)."""
from __future__ import annotations

import random

import pandas as pd
import streamlit as st

from apps.theme import STEEL, TEAL, kpi_card_html, render_app_header

DEPARTAMENTOS = ["Docencia", "Administración", "Tecnología", "Mantenimiento", "Servicios"]
CARGOS = {
    "Docencia": ["Profesor", "Coordinador", "Decano"],
    "Administración": ["Asistente", "Analista", "Jefe de Sección"],
    "Tecnología": ["Soporte Técnico", "Desarrollador", "Administrador de Red"],
    "Mantenimiento": ["Operario", "Electricista"],
    "Servicios": ["Recepcionista", "Portero", "Auxiliar de Biblioteca"],
}
NOMBRES = [
    "María Benítez", "Jorge Acosta", "Lucía Giménez", "Diego Villalba", "Sofía Duarte",
    "Martín Cardozo", "Valentina Ortiz", "Andrés Rojas", "Camila Torres", "Fabio Vera",
]


@st.cache_data(show_spinner=False)
def _empleados() -> pd.DataFrame:
    rng = random.Random(7)
    rows = []
    for i in range(48):
        depto = rng.choice(DEPARTAMENTOS)
        cargo = rng.choice(CARGOS[depto])
        rows.append(
            {
                "Cédula": f"{rng.randint(1, 4)}.{rng.randint(100, 999)}.{rng.randint(100, 999)}",
                "Nombre": rng.choice(NOMBRES) + f" {rng.randint(1, 99)}",
                "Departamento": depto,
                "Cargo": cargo,
                "Antigüedad (años)": rng.randint(0, 25),
                "Salario (Gs)": rng.randint(4_000_000, 12_000_000),
                "Asistencias mes": rng.randint(15, 26),
            }
        )
    return pd.DataFrame(rows)


def _kpi_row() -> None:
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi_card_html("Colaboradores", "387", "+12"), unsafe_allow_html=True)
    # Baja de ausentismo es buena noticia: flecha ▼ pero en verde
    k2.markdown(kpi_card_html("Ausentismo mensual", "3,4 %", "-0,6 %"), unsafe_allow_html=True)
    k3.markdown(kpi_card_html("Nómina mensual", "₲ 2,84 MM", "+4,1 %"), unsafe_allow_html=True)
    k4.markdown(kpi_card_html("Evaluación desempeño", "4,1 / 5", "+0,2"), unsafe_allow_html=True)


def run() -> None:
    render_app_header(
        "Gestión RRHH",
        "Demo stub — datos de ejemplo. Conexión futura al sistema de RRHH institucional.",
    )

    _kpi_row()
    df = _empleados()

    c1, c2 = st.columns([1, 2])
    with c1:
        with st.container(key="panel_tabla", border=False):
            st.markdown('<div class="ucsa-panel-title">Empleados — tabla</div>', unsafe_allow_html=True)
            depto = st.selectbox("Filtrar por departamento", ["Todos"] + DEPARTAMENTOS)
            filt = df if depto == "Todos" else df[df.Departamento == depto]
            st.dataframe(
                filt[["Cédula", "Nombre", "Cargo", "Salario (Gs)", "Asistencias mes"]].head(15),
                width="stretch",
                hide_index=True,
            )
    with c2:
        with st.container(key="panel_chart", border=False):
            st.markdown('<div class="ucsa-panel-title">Colaboradores por departamento</div>', unsafe_allow_html=True)
            st.bar_chart(filt.Departamento.value_counts(), color=STEEL)
            n_dias = 26
            asistencia = (filt["Asistencias mes"] / n_dias * 100).mean() if len(filt) else 0
            st.markdown(
                f'<div class="ucsa-panel-note" style="color:{TEAL};">'
                f'Asistencia promedio del filtro: {asistencia:.1f} %</div>',
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    run()