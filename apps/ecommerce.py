"""Stub: Ecommerce UCSA — tienda oficial de la comunidad académica (datos demo)."""
from __future__ import annotations

import random

import pandas as pd
import streamlit as st

from apps.theme import NAVY, STEEL, TEAL, render_topbar

PRODUCTOS = [
    ("Remera UCSA", 150_000),
    ("Buzo institucional", 320_000),
    ("Mochila universitaria", 280_000),
    ("Termo + mate", 190_000),
    ("Llavero UCSA", 35_000),
    ("Cuaderno técnico", 45_000),
    ("Pack bibliografía digital", 120_000),
    ("Botella térmica", 110_000),
]


@st.cache_data(show_spinner=False)
def _ventas() -> pd.DataFrame:
    rng = random.Random(21)
    days = pd.date_range("2026-08-01", periods=60, freq="D")
    rows = []
    for d in days:
        for nombre, precio in PRODUCTOS:
            qty = rng.randint(0, 25)
            rows.append(
                {
                    "Fecha": d,
                    "Producto": nombre,
                    "Precio (Gs)": precio,
                    "Cantidad": qty,
                    "Ingresos (Gs)": qty * precio,
                }
            )
    return pd.DataFrame(rows)


def _kpi_row(ventas: pd.DataFrame) -> None:
    total = ventas["Ingresos (Gs)"].sum()
    pedidos = ventas[(ventas.Cantidad > 0)].shape[0]
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Ingresos últimos 60 días", f"₲ {total/1e6:.2f} M", "+12,4 %")
    k2.metric("Pedidos", f"{pedidos:,}".replace(",", "."), "+9,1 %")
    k3.metric("Productos activos", f"{len(PRODUCTOS)}", "—")
    k4.metric("Ticket promedio", f"₲ {total / max(pedidos, 1):,.0f}".replace(",", "."), "+2,3 %")


def run() -> None:
    render_topbar("Ecommerce UCSA")
    st.markdown(
        f"<h2 style='color:{NAVY};margin:0.4rem 0;'>🛒 Tienda Oficial de la Comunidad Académica</h2>",
        unsafe_allow_html=True,
    )
    st.caption("Demo stub — datos de ejemplo. Integración futura con pasarela de pagos y stock real.")

    ventas = _ventas()
    _kpi_row(ventas)

    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f"<b style='color:{STEEL}'>Ingresos por día</b>", unsafe_allow_html=True)
        diario = ventas.groupby("Fecha")["Ingresos (Gs)"].sum()
        st.line_chart(diario, color=TEAL)
    with c2:
        st.markdown(f"<b style='color:{STEEL}'>Catálogo</b>", unsafe_allow_html=True)
        for nombre, precio in PRODUCTOS:
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;padding:4px 0;"
                f"border-bottom:1px solid #E3E8EF;'>"
                f"<span>{nombre}</span><b>₲ {precio:,}</b></div>".replace(",", "."),
                unsafe_allow_html=True,
            )
        top = ventas.groupby("Producto").Cantidad.sum().sort_values(ascending=False).head(3)
        st.markdown(
            f"<span style='color:{NAVY};font-weight:700;'>Top ventas: "
            f"{', '.join(top.index)}</span>",
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    run()