import streamlit as st
from streamlit_app.components.ta_gauge import ta_gauge
from streamlit_app.components.live_price_header import live_price_header


def render(current_price, price_change_24h):
    st.title("📊 Market Overview")

    # --- Live Price Header ---
    live_price_header(
        symbol="BTC",
        price=current_price,
        change_pct=price_change_24h
    )

    st.write("This is the overview page. Add charts, summaries, and market data here.")

    # --- Technical Analysis Gauge ---
    ta_gauge("Technical rating", "Buy", 0.72)
