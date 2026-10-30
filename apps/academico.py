"""Portal Académico UCSA — Portal del Estudiante (demo funcional)."""
from __future__ import annotations

import random
from datetime import date, timedelta

import pandas as pd
import streamlit as st

from apps.theme import render_header, PRIMARY, TEAL, kpi_card_html, render_app_header

ALUMNOS_DEMO = [
    {"id": "A-00123", "cedula": "4.567.890", "nombre": "Ana López", "carrera": "Ingeniería Informática", "facultad": "Ingeniería y Tecnología", "curso": 4, "correo": "ana.lopez@ucsa.edu.py"},
    {"id": "A-00456", "cedula": "3.456.123", "nombre": "Carlos Ramírez", "carrera": "Administración", "facultad": "Ciencias Empresariales", "curso": 3, "correo": "carlos.ramirez@ucsa.edu.py"},
    {"id": "A-00789", "cedula": "5.678.234", "nombre": "María Benítez", "carrera": "Derecho", "facultad": "Ciencias Jurídicas", "curso": 5, "correo": "maria.benitez@ucsa.edu.py"},
]

MATERIAS = [
    {"codigo": "INF401", "materia": "Ingeniería de Software", "docente": "Lic. Diego Villalba", "aula": "A-204", "creditos": 4},
    {"codigo": "INF402", "materia": "Base de Datos II", "docente": "Ing. Sofía Duarte", "aula": "Lab-3", "creditos": 4},
    {"codigo": "INF403", "materia": "Redes de Computadoras", "docente": "Ing. Martín Cardozo", "aula": "B-105", "creditos": 3},
    {"codigo": "INF404", "materia": "Inteligencia Artificial", "docente": "Dra. Valentina Ortiz", "aula": "A-310", "creditos": 3},
    {"codigo": "LEG301", "materia": "Derecho Constitucional", "docente": "Abg. Andrés Rojas", "aula": "C-101", "creditos": 4},
    {"codigo": "ADM302", "materia": "Finanzas Empresariales", "docente": "MSc. Camila Torres", "aula": "D-202", "creditos": 3},
]

HORARIO = [
    {"dia": "Lunes", "hora": "07:00 - 09:00", "materia": "Ingeniería de Software", "aula": "A-204"},
    {"dia": "Lunes", "hora": "09:15 - 11:15", "materia": "Base de Datos II", "aula": "Lab-3"},
    {"dia": "Martes", "hora": "07:00 - 09:00", "materia": "Redes de Computadoras", "aula": "B-105"},
    {"dia": "Miércoles", "hora": "14:00 - 16:00", "materia": "Inteligencia Artificial", "aula": "A-310"},
    {"dia": "Jueves", "hora": "09:15 - 11:15", "materia": "Base de Datos II", "aula": "Lab-3"},
    {"dia": "Viernes", "hora": "07:00 - 09:00", "materia": "Ingeniería de Software", "aula": "A-204"},
]

CALIFICACIONES = [
    {"materia": "Ingeniería de Software", "parcial1": 4.5, "parcial2": 4.8, "final": 5.0, "estado": "Aprobado"},
    {"materia": "Base de Datos II", "parcial1": 4.0, "parcial2": 4.2, "final": 4.5, "estado": "Aprobado"},
    {"materia": "Redes de Computadoras", "parcial1": 3.8, "parcial2": 4.0, "final": 4.0, "estado": "Aprobado"},
    {"materia": "Inteligencia Artificial", "parcial1": 4.7, "parcial2": 4.9, "final": 4.8, "estado": "Aprobado"},
]

TRAMITES = [
    {"tramite": "Constancia de alumno regular", "estado": "Disponible", "fecha": "2026-10-01"},
    {"tramite": "Certificado de materias cursadas", "estado": "En trámite", "fecha": "2026-10-08"},
    {"tramite": "Solicitud de equivalencia", "estado": "Pendiente", "fecha": "2026-10-10"},
]

PAGOS = [
    {"concepto": "Matrícula 2do semestre 2026", "monto": "₲ 1.850.000", "vencimiento": "2026-10-15", "estado": "Pendiente"},
    {"concepto": "Cuota Septiembre 2026", "monto": "₲ 950.000", "vencimiento": "2026-09-30", "estado": "Pagado"},
    {"concepto": "Cuota Octubre 2026", "monto": "₲ 950.000", "vencimiento": "2026-10-31", "estado": "Pendiente"},
]

@st.cache_data(show_spinner=False)
def _notificaciones():
    return [
        {"fecha": (date.today() - timedelta(days=1)).strftime("%d/%m/%Y"), "titulo": "Nota publicada", "detalle": "Ingeniería de Software - Parcial 2"},
        {"fecha": (date.today() - timedelta(days=2)).strftime("%d/%m/%Y"), "titulo": "Horario actualizado", "detalle": "Base de Datos II pasa a Lab-3"},
        {"fecha": (date.today() - timedelta(days=5)).strftime("%d/%m/%Y"), "titulo": "Trámite", "detalle": "Constancia de alumno regular disponible para descarga"},
    ]


def _login() -> None:
    st.markdown('<div class="ucsa-page-title">Portal del Estudiante</div>', unsafe_allow_html=True)
    st.markdown('<p class="ucsa-page-sub">Acceso al portal académico UCSA</p>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### Iniciar sesión")
        col1, col2 = st.columns(2)
        with col1:
            usuario = st.text_input("Usuario / N° de matrícula", value="A-00123")
        with col2:
            clave = st.text_input("Contraseña", type="password", value="demo")
        if st.button("Ingresar al Portal", type="primary", width="stretch"):
            alumno = next((a for a in ALUMNOS_DEMO if a["id"] == usuario), None)
            if alumno and clave:
                st.session_state["portal_alumno"] = alumno
                st.session_state["portal_tab"] = "Inicio"
                st.rerun()
            else:
                st.error("Credenciales inválidas. Usá A-00123 / demo para probar.")


def _nav() -> None:
    alumno = st.session_state["portal_alumno"]
    with st.container(border=True):
        c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)
        tabs = ["Inicio", "Mis Materias", "Horario", "Calificaciones", "Inscripciones", "Trámites", "Pagos", "Mi Perfil"]
        for i, t in enumerate(tabs):
            if c1 if i==0 else c2 if i==1 else c3 if i==2 else c4 if i==3 else c5 if i==4 else c6 if i==5 else c7 if i==6 else c8:
                if st.button(t, width="stretch"):
                    st.session_state["portal_tab"] = t
        st.caption(f"Conectado como: {alumno['nombre']} | {alumno['carrera']} | Curso {alumno['curso']}")


def _inicio(alumno: dict) -> None:
    st.markdown("## Inicio")
    k1,k2,k3,k4 = st.columns(4)
    k1.markdown(kpi_card_html("Materias cursando", "4", "+0"), unsafe_allow_html=True)
    k2.markdown(kpi_card_html("Promedio general", "4.58 / 5.00", "+0.12"), unsafe_allow_html=True)
    k3.markdown(kpi_card_html("Créditos aprobados", "92", "+12"), unsafe_allow_html=True)
    k4.markdown(kpi_card_html("Asistencia", "96 %", "+2 %"), unsafe_allow_html=True)

    c1,c2 = st.columns([2,1])
    with c1:
        with st.container(border=True):
            st.markdown("### Próximas clases")
            hoy = date.today()
            df_h = pd.DataFrame(HORARIO)
            st.dataframe(df_h, width="stretch", hide_index=True)
    with c2:
        with st.container(border=True):
            st.markdown("### Notificaciones")
            for n in _notificaciones():
                st.markdown(f"**{n['titulo']}** · {n['fecha']}  \n{n['detalle']}")
                st.divider()


def _materias() -> None:
    st.markdown("## Mis Materias")
    df = pd.DataFrame(MATERIAS)
    st.dataframe(df, width="stretch", hide_index=True)


def _horario() -> None:
    st.markdown("## Horario Semanal")
    df = pd.DataFrame(HORARIO)
    pivot = df.pivot_table(index="hora", columns="dia", values="materia", aggfunc="first")
    st.dataframe(pivot, width="stretch")
    with st.container(border=True):
        st.markdown("### Detalle por clase")
        st.dataframe(df, width="stretch", hide_index=True)


def _calificaciones() -> None:
    st.markdown("## Calificaciones")
    df = pd.DataFrame(CALIFICACIONES)
    df["Promedio"] = df[["parcial1","parcial2","final"]].mean(axis=1).round(2)
    st.dataframe(df, width="stretch", hide_index=True)
    with st.container(border=True):
        prom = df["Promedio"].mean()
        st.success(f"Promedio acumulado: {prom:.2f} / 5.00")


def _inscripciones() -> None:
    st.markdown("## Inscripciones")
    with st.container(border=True):
        st.markdown("### Inscripción a materias - Semestre 2/2026")
        opts = [f"{m['codigo']} - {m['materia']} ({m['creditos']} créditos)" for m in MATERIAS]
        sel = st.multiselect("Seleccioná materias", opts)
        if st.button("Confirmar pre-inscripción", type="primary"):
            if sel:
                st.session_state["preinsc"] = sel
                st.success(f"Pre-inscripción enviada: {len(sel)} materia(s). Pendiente de aprobación por Secretaría Académica.")
            else:
                st.warning("Seleccioná al menos una materia.")
    if st.session_state.get("preinsc"):
        with st.container(border=True):
            st.markdown("### Pre-inscripción en proceso")
            for s in st.session_state["preinsc"]:
                st.write(f"- {s}")


def _tramites() -> None:
    st.markdown("## Trámites")
    df = pd.DataFrame(TRAMITES)
    st.dataframe(df, width="stretch", hide_index=True)
    with st.container(border=True):
        st.markdown("### Solicitar nuevo trámite")
        t = st.selectbox("Tipo de trámite", ["Constancia de alumno regular", "Certificado de materias cursadas", "Historial académico", "Otros"])
        obs = st.text_area("Observaciones")
        if st.button("Enviar solicitud", type="primary"):
            st.success(f"Solicitud '{t}' enviada correctamente. Te notificaremos por correo cuando esté lista.")


def _pagos() -> None:
    st.markdown("## Pagos y Estado de Cuenta")
    df = pd.DataFrame(PAGOS)
    st.dataframe(df, width="stretch", hide_index=True)
    c1,c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("### Generar cupón de pago")
            if st.button("Generar cupón para cuotas pendientes", type="primary"):
                st.info("Cupón generado. Podés abonar por cajero automático, homebanking o ventanilla.")
    with c2:
        with st.container(border=True):
            st.markdown("### Estado")
            st.write("Saldo pendiente: ₲ 2.800.000")
            st.write("Último pago: Cuota Septiembre 2026 - 15/09/2026")


def _perfil(alumno: dict) -> None:
    st.markdown("## Mi Perfil")
    c1,c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("### Datos personales")
            st.write(f"**Matrícula:** {alumno['id']}")
            st.write(f"**Cédula:** {alumno['cedula']}")
            st.write(f"**Nombre y apellido:** {alumno['nombre']}")
            st.write(f"**Correo institucional:** {alumno['correo']}")
    with c2:
        with st.container(border=True):
            st.markdown("### Datos académicos")
            st.write(f"**Facultad:** {alumno['facultad']}")
            st.write(f"**Carrera:** {alumno['carrera']}")
            st.write(f"**Curso:** {alumno['curso']}°")
            st.write(f"**Modalidad:** Presencial")
    with st.container(border=True):
        st.markdown("### Seguridad")
        if st.button("Cerrar sesión"):
            for k in list(st.session_state.keys()):
                if k.startswith("portal_"):
                    del st.session_state[k]
            st.rerun()


def run() -> None:
    render_header("acaniza")
    render_app_header(
        "Portal Académico - Estudiantes",
        "Portal del Estudiante UCSA — Inscripciones, horarios, calificaciones, trámites y pagos",
    )
    if "portal_alumno" not in st.session_state:
        _login()
        return
    _nav()
    tab = st.session_state.get("portal_tab", "Inicio")
    alumno = st.session_state["portal_alumno"]
    if tab == "Inicio":
        _inicio(alumno)
    elif tab == "Mis Materias":
        _materias()
    elif tab == "Horario":
        _horario()
    elif tab == "Calificaciones":
        _calificaciones()
    elif tab == "Inscripciones":
        _inscripciones()
    elif tab == "Trámites":
        _tramites()
    elif tab == "Pagos":
        _pagos()
    elif tab == "Mi Perfil":
        _perfil(alumno)


if __name__ == "__main__":
    run()
