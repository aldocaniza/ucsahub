"""Ecommerce UCSA — Tienda oficial funcional."""
from __future__ import annotations

import random
from datetime import date, timedelta

import pandas as pd
import streamlit as st

from apps.theme import TEAL, PRIMARY, kpi_card_html, render_app_header

PRODUCTOS = [
    {"id": "P-001", "nombre": "Remera UCSA", "categoria": "Indumentaria", "precio": 150_000, "stock": 245, "img": "👕"},
    {"id": "P-002", "nombre": "Buzo institucional", "categoria": "Indumentaria", "precio": 320_000, "stock": 128, "img": "🧥"},
    {"id": "P-003", "nombre": "Mochila universitaria", "categoria": "Accesorios", "precio": 280_000, "stock": 87, "img": "🎒"},
    {"id": "P-004", "nombre": "Termo + mate", "categoria": "Accesorios", "precio": 190_000, "stock": 156, "img": "🧉"},
    {"id": "P-005", "nombre": "Llavero UCSA", "categoria": "Souvenirs", "precio": 35_000, "stock": 542, "img": "🔑"},
    {"id": "P-006", "nombre": "Cuaderno técnico", "categoria": "Papelería", "precio": 45_000, "stock": 324, "img": "📓"},
    {"id": "P-007", "nombre": "Pack bibliografía digital", "categoria": "Digital", "precio": 120_000, "stock": 999, "img": "💾"},
    {"id": "P-008", "nombre": "Botella térmica", "categoria": "Accesorios", "precio": 110_000, "stock": 198, "img": "🍶"},
    {"id": "P-009", "nombre": "Gorra UCSA", "categoria": "Indumentaria", "precio": 85_000, "stock": 167, "img": "🧢"},
    {"id": "P-010", "nombre": "Agenda universitaria", "categoria": "Papelería", "precio": 65_000, "stock": 276, "img": "📅"},
]

@st.cache_data(show_spinner=False)
def _ventas() -> pd.DataFrame:
    rng = random.Random(77)
    days = pd.date_range(date.today() - timedelta(days=59), periods=60, freq="D")
    rows = []
    for d in days:
        for p in PRODUCTOS:
            qty = rng.randint(0, 18)
            if qty:
                rows.append(
                    {
                        "Fecha": d,
                        "ID": p["id"],
                        "Producto": p["nombre"],
                        "Categoria": p["categoria"],
                        "Precio (Gs)": p["precio"],
                        "Cantidad": qty,
                        "Ingresos (Gs)": qty * p["precio"],
                    }
                )
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def _pedidos() -> pd.DataFrame:
    rng = random.Random(88)
    estados = ["Pendiente", "Confirmado", "En preparación", "Enviado", "Entregado"]
    rows = []
    for i in range(24):
        p = rng.choice(PRODUCTOS)
        qty = rng.randint(1, 3)
        rows.append(
            {
                "N° Pedido": f"PED-{i+1001:04d}",
                "Cliente": rng.choice(["Ana López", "Carlos Ramírez", "María Benítez", "Jorge Acosta", "Lucía Giménez"]),
                "Producto": p["nombre"],
                "Cantidad": qty,
                "Total (Gs)": qty * p["precio"],
                "Fecha": (date.today() - timedelta(days=rng.randint(0, 30))).strftime("%d/%m/%Y"),
                "Estado": rng.choices(estados, weights=[10,15,15,20,40])[0],
                "Método pago": rng.choice(["Efectivo", "Transferencia", "Tarjeta"]),
            }
        )
    return pd.DataFrame(rows)


def _kpi_row(ventas: pd.DataFrame, pedidos: pd.DataFrame) -> None:
    total = ventas["Ingresos (Gs)"].sum()
    entregados = (pedidos["Estado"] == "Entregado").sum()
    pendientes = (pedidos["Estado"].isin(["Pendiente", "Confirmado", "En preparación"])).sum()
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi_card_html("Ingresos 60 días", f"₲ {total/1e6:.2f} M", "+15,2 %"), unsafe_allow_html=True)
    k2.markdown(kpi_card_html("Pedidos totales", f"{len(pedidos)}", "+12"), unsafe_allow_html=True)
    k3.markdown(kpi_card_html("Entregados", f"{entregados}", "+18 %"), unsafe_allow_html=True)
    k4.markdown(kpi_card_html("Pendientes", f"{pendientes}"), unsafe_allow_html=True)


def run() -> None:
    render_app_header(
        "Ecommerce UCSA",
        "Tienda oficial de la comunidad académica UCSA — Catálogo, carrito, pedidos y ventas",
    )
    if "carrito" not in st.session_state:
        st.session_state["carrito"] = []

    ventas = _ventas()
    pedidos = _pedidos()
    _kpi_row(ventas, pedidos)

    tab = st.tabs(["Tienda", "Catálogo", "Carrito", "Pedidos", "Ventas", "Stock"])

    with tab[0]:
        st.markdown("## Tienda Online")
        st.markdown("Productos destacados para la comunidad universitaria")
        cols = st.columns(4)
        for i,p in enumerate(PRODUCTOS[:8]):
            with cols[i % 4]:
                with st.container(border=True):
                    st.markdown(f"### {p['img']} {p['nombre']}")
                    st.caption(f"{p['categoria']} | Stock: {p['stock']} u.")
                    st.markdown(f"**₲ {p['precio']:,}**".replace(",", "."))
                    if st.button("Agregar al carrito", key=f"add_{p['id']}", width="stretch"):
                        st.session_state["carrito"].append(p)
                        st.success(f"{p['nombre']} agregado al carrito")
        if st.session_state["carrito"]:
            st.info(f"Carrito: {len(st.session_state['carrito'])} producto(s)")

    with tab[1]:
        with st.container(border=True):
            st.markdown("### Catálogo completo")
            df_cat = pd.DataFrame(PRODUCTOS)[["id","nombre","categoria","precio","stock"]]
            df_cat["Precio (Gs)"] = df_cat["precio"].apply(lambda x: f"₲ {x:,}".replace(",", "."))
            st.dataframe(df_cat[["id","nombre","categoria","Precio (Gs)","stock"]], width="stretch", hide_index=True)
        c1,c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("### Filtrar por categoría")
                cat = st.selectbox("Categoría", ["Todas"] + sorted(set(p["categoria"] for p in PRODUCTOS)))
                filt = PRODUCTOS if cat == "Todas" else [p for p in PRODUCTOS if p["categoria"] == cat]
                for p in filt:
                    st.write(f"{p['img']} **{p['nombre']}** - ₲ {p['precio']:,}".replace(",", "."))
        with c2:
            with st.container(border=True):
                st.markdown("### Nuevo producto")
                st.text_input("Código")
                st.text_input("Nombre del producto")
                st.selectbox("Categoría", ["Indumentaria","Accesorios","Souvenirs","Papelería","Digital"])
                st.number_input("Precio (Gs)", min_value=0, value=100000, step=5000)
                st.number_input("Stock inicial", min_value=0, value=50)
                if st.button("Agregar producto", type="primary"):
                    st.success("Producto agregado al catálogo (demo).")

    with tab[2]:
        st.markdown("## Carrito de Compras")
        if not st.session_state["carrito"]:
            st.info("Tu carrito está vacío. Agregá productos desde la Tienda.")
        else:
            total_carrito = sum(p["precio"] for p in st.session_state["carrito"])
            for i,p in enumerate(st.session_state["carrito"]):
                c1,c2,c3 = st.columns([4,2,1])
                with c1: st.write(f"{p['img']} **{p['nombre']}**")
                with c2: st.write(f"₲ {p['precio']:,}".replace(",", "."))
                with c3:
                    if st.button("Quitar", key=f"rm_{i}"):
                        st.session_state["carrito"].pop(i)
                        st.rerun()
            st.divider()
            st.markdown(f"### Total: ₲ {total_carrito:,}".replace(",", "."))
            with st.container(border=True):
                st.markdown("### Datos de entrega")
                c1,c2 = st.columns(2)
                with c1: st.text_input("Nombre completo")
                with c2: st.text_input("Teléfono / Celular")
                st.text_input("Dirección de entrega")
                st.selectbox("Método de pago", ["Efectivo", "Transferencia bancaria", "Tarjeta de débito/crédito"])
                if st.button("Confirmar pedido", type="primary", width="stretch"):
                    st.session_state["carrito"] = []
                    st.success("¡Pedido confirmado! Te enviaremos la confirmación por correo. N° de pedido: PED-2001")

    with tab[3]:
        with st.container(border=True):
            st.markdown("### Gestión de pedidos")
            df_p = _pedidos()
            estado = st.selectbox("Filtrar por estado", ["Todos"] + sorted(df_p["Estado"].unique().tolist()))
            filt_p = df_p if estado == "Todos" else df_p[df_p["Estado"] == estado]
            st.dataframe(filt_p, width="stretch", hide_index=True)
        with st.container(border=True):
            st.markdown("### Actualizar estado de pedido")
            c1,c2,c3 = st.columns(3)
            with c1: st.selectbox("N° Pedido", _pedidos()["N° Pedido"].tolist())
            with c2: st.selectbox("Nuevo estado", ["Confirmado", "En preparación", "Enviado", "Entregado", "Cancelado"])
            with c3: st.text_input("Seguimiento / Tracking")
            if st.button("Actualizar pedido", type="primary"):
                st.success("Estado de pedido actualizado correctamente.")

    with tab[4]:
        c1,c2 = st.columns([2,1])
        with c1:
            with st.container(border=True):
                st.markdown("### Ingresos por día - Últimos 60 días")
                diario = ventas.groupby("Fecha")["Ingresos (Gs)"].sum()
                st.line_chart(diario, color=TEAL)
        with c2:
            with st.container(border=True):
                st.markdown("### Ventas por categoría")
                cat_v = ventas.groupby("Categoria")["Ingresos (Gs)"].sum().sort_values(ascending=False)
                st.bar_chart(cat_v, color=PRIMARY)
        with st.container(border=True):
            st.markdown("### Detalle de ventas")
            st.dataframe(ventas.sort_values("Fecha", ascending=False).head(40), width="stretch", hide_index=True)

    with tab[5]:
        with st.container(border=True):
            st.markdown("### Control de stock")
            df_s = pd.DataFrame(PRODUCTOS)[["id","nombre","categoria","stock","precio"]]
            df_s["Valor stock (Gs)"] = df_s["stock"] * df_s["precio"]
            st.dataframe(df_s, width="stretch", hide_index=True)
        c1,c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("### Ajuste de stock")
                c1a,c2a,c3a = st.columns(3)
                with c1a: st.selectbox("Producto", [p["nombre"] for p in PRODUCTOS])
                with c2a: st.selectbox("Movimiento", ["Entrada", "Salida", "Ajuste"])
                with c3a: st.number_input("Cantidad", min_value=0, value=10)
                if st.button("Aplicar ajuste", type="primary"):
                    st.success("Ajuste de stock aplicado correctamente.")
        with c2:
            with st.container(border=True):
                st.markdown("### Alertas de stock bajo")
                bajos = [p for p in PRODUCTOS if p["stock"] < 100]
                for p in bajos:
                    st.warning(f"{p['img']} **{p['nombre']}** - Stock: {p['stock']} (Bajo)")


if __name__ == "__main__":
    run()
