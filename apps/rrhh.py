"""Gestión RRHH UCSA — Panel funcional para demostración."""
from __future__ import annotations

import random
from datetime import date

import pandas as pd
import streamlit as st

from apps.theme import render_header, STEEL, TEAL, PRIMARY, kpi_card_html, render_app_header

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
    "Ana López", "Carlos Ramírez", "Pedro González", "Laura Méndez", "José Aquino",
]

@st.cache_data(show_spinner=False)
def _empleados() -> pd.DataFrame:
    rng = random.Random(123)
    rows = []
    for i in range(55):
        depto = rng.choice(DEPARTAMENTOS)
        cargo = rng.choice(CARGOS[depto])
        rows.append(
            {
                "Legajo": f"L-{i+1001:04d}",
                "CI": f"{rng.randint(1,5)}.{rng.randint(100,999)}.{rng.randint(100,999)}",
                "Nombre y Apellido": rng.choice(NOMBRES) + f" {rng.randint(1, 99)}",
                "Departamento": depto,
                "Cargo": cargo,
                "Fecha Ingreso": date(2018 + rng.randint(0, 7), rng.randint(1, 12), rng.randint(1, 28)).strftime("%d/%m/%Y"),
                "Antigüedad (años)": rng.randint(0, 12),
                "Salario (Gs)": rng.randint(4_000_000, 14_000_000),
                "Estado": rng.choices(["Activo", "Vacaciones", "Licencia"], weights=[90, 7, 3])[0],
                "Asistencias mes": rng.randint(18, 26),
                "Faltas mes": rng.randint(0, 3),
            }
        )
    return pd.DataFrame(rows)


def _kpi_row(df: pd.DataFrame) -> None:
    activos = (df["Estado"] == "Activo").sum()
    ausentismo = (df["Faltas mes"].sum() / (df["Asistencias mes"].sum() + df["Faltas mes"].sum()) * 100) if (df["Asistencias mes"].sum() + df["Faltas mes"].sum()) else 0
    nomina = df[df["Estado"] == "Activo"]["Salario (Gs)"].sum()
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi_card_html("Colaboradores activos", f"{activos}", "+8"), unsafe_allow_html=True)
    k2.markdown(kpi_card_html("Ausentismo mensual", f"{ausentismo:.1f} %", "-0,8 %"), unsafe_allow_html=True)
    k3.markdown(kpi_card_html("Nómina mensual", f"₲ {nomina/1e9:.2f} MM", "+4,1 %"), unsafe_allow_html=True)
    k4.markdown(kpi_card_html("Evaluación promedio", "4,3 / 5", "+0,1"), unsafe_allow_html=True)


def run() -> None:
    render_header()
    render_app_header(
        "Gestión RRHH",
        "Módulo RRHH UCSA — Legajo, asistencias, nómina, evaluaciones y solicitudes",
    )
    df = _empleados()
    _kpi_row(df)

    tab = st.tabs(["Dashboard", "Legajo", "Asistencias", "Nómina", "Evaluaciones", "Solicitudes"])

    with tab[0]:
        c1,c2 = st.columns([2,1])
        with c1:
            with st.container(border=True):
                st.markdown("### Colaboradores por departamento")
                dist = df["Departamento"].value_counts()
                st.bar_chart(dist, color=STEEL)
        with c2:
            with st.container(border=True):
                st.markdown("### Estado laboral")
                est = df["Estado"].value_counts()
                st.dataframe(est.rename_axis("Estado").reset_index(name="Cantidad"), width="stretch", hide_index=True)
        with st.container(border=True):
            st.markdown("### Cumpleaños del mes")
            st.info("Próximos cumpleaños: María Benítez (15/10), Jorge Acosta (22/10), Lucía Giménez (28/10)")

    with tab[1]:
        with st.container(border=True):
            st.markdown("### Legajo de colaboradores")
            depto = st.selectbox("Filtrar por departamento", ["Todos"] + sorted(df["Departamento"].unique().tolist()))
            filt = df if depto == "Todos" else df[df["Departamento"] == depto]
            st.dataframe(filt, width="stretch", hide_index=True)
        with st.container(border=True):
            st.markdown("### Alta de colaborador")
            c1,c2,c3 = st.columns(3)
            with c1: st.text_input("Nombre y Apellido")
            with c2: st.text_input("CI/N° Documento")
            with c3: st.selectbox("Departamento", DEPARTAMENTOS)
            c4,c5,c6 = st.columns(3)
            with c4: st.selectbox("Cargo", sum(CARGOS.values(), []))
            with c5: st.number_input("Salario (Gs)", min_value=0, value=6000000, step=100000)
            with c6: st.date_input("Fecha de ingreso")
            if st.button("Registrar colaborador", type="primary"):
                st.success("Colaborador registrado correctamente (demo).")

    with tab[2]:
        with st.container(border=True):
            st.markdown("### Control de asistencias - Octubre 2026")
            asist = df[["Legajo","Nombre y Apellido","Departamento","Asistencias mes","Faltas mes","Estado"]].copy()
            asist["% Asistencia"] = (asist["Asistencias mes"] / (asist["Asistencias mes"] + asist["Faltas mes"]) * 100).round(1)
            st.dataframe(asist, width="stretch", hide_index=True)
        with st.container(border=True):
            st.markdown("### Registrar marcación")
            c1,c2,c3 = st.columns(3)
            with c1: st.selectbox("Legajo", df["Legajo"].tolist()[:10])
            with c2: st.selectbox("Tipo", ["Entrada", "Salida", "Justificación"])
            with c3: st.time_input("Hora")
            if st.button("Guardar marcación", type="primary"):
                st.success("Marcación registrada correctamente.")

    with tab[3]:
        with st.container(border=True):
            st.markdown("### Nómina Octubre 2026")
            nom = df[df["Estado"] == "Activo"][["Legajo","Nombre y Apellido","Cargo","Departamento","Salario (Gs)"]].copy()
            nom["Bonificación"] = (nom["Salario (Gs)"] * 0.05).astype(int)
            nom["Descuentos"] = (nom["Salario (Gs)"] * 0.09).astype(int)
            nom["Neto a cobrar (Gs)"] = nom["Salario (Gs)"] + nom["Bonificación"] - nom["Descuentos"]
            st.dataframe(nom, width="stretch", hide_index=True)
            total = nom["Neto a cobrar (Gs)"].sum()
            st.metric("Total neto a pagar", f"₲ {total:,.0f}".replace(",", "."))
        with st.container(border=True):
            st.markdown("### Generar recibos")
            if st.button("Generar recibos de sueldo (PDF)", type="primary"):
                st.success("Recibos generados. Listos para impresión/envío por correo.")

    with tab[4]:
        with st.container(border=True):
            st.markdown("### Evaluación de desempeño 2026")
            ev = df[["Legajo","Nombre y Apellido","Departamento","Cargo"]].copy().head(12)
            ev["Calificación"] = [4.5,4.0,4.8,4.2,4.6,4.1,4.9,4.3,4.7,4.4,4.0,4.6]
            ev["Observación"] = ["Muy bueno","Bueno","Destacado","Bueno","Muy bueno","Bueno","Destacado","Bueno","Muy bueno","Bueno","Satisfactorio","Muy bueno"]
            st.dataframe(ev, width="stretch", hide_index=True)
        with st.container(border=True):
            st.markdown("### Nueva evaluación")
            c1,c2 = st.columns(2)
            with c1: st.selectbox("Colaborador", df["Nombre y Apellido"].tolist()[:15])
            with c2: st.slider("Calificación (1-5)", 1.0, 5.0, 4.0, 0.1)
            st.text_area("Fortalezas / Oportunidades de mejora")
            if st.button("Guardar evaluación", type="primary"):
                st.success("Evaluación guardada correctamente.")

    with tab[5]:
        with st.container(border=True):
            st.markdown("### Solicitudes de RRHH")
            sol = pd.DataFrame([
                {"ID": "SOL-001", "Solicitante": "María Benítez", "Tipo": "Certificado laboral", "Fecha": "08/10/2026", "Estado": "Aprobado"},
                {"ID": "SOL-002", "Solicitante": "Jorge Acosta", "Tipo": "Vacaciones", "Fecha": "09/10/2026", "Estado": "En proceso"},
                {"ID": "SOL-003", "Solicitante": "Lucía Giménez", "Tipo": "Permiso", "Fecha": "10/10/2026", "Estado": "Pendiente"},
                {"ID": "SOL-004", "Solicitante": "Diego Villalba", "Tipo": "Constancia", "Fecha": "10/10/2026", "Estado": "Pendiente"},
            ])
            st.dataframe(sol, width="stretch", hide_index=True)
        with st.container(border=True):
            st.markdown("### Gestionar solicitud")
            c1,c2 = st.columns(2)
            with c1: st.selectbox("Seleccionar solicitud", ["SOL-001","SOL-002","SOL-003","SOL-004"])
            with c2: st.selectbox("Acción", ["Aprobar", "Rechazar", "Derivar", "Marcar en proceso"])
            st.text_input("Observación / Motivo")
            if st.button("Aplicar acción", type="primary"):
                st.success("Acción aplicada correctamente.")


if __name__ == "__main__":
    run()
