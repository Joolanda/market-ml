import streamlit as st
from streamlit_app.components.ta_gauge import ta_gauge
from streamlit_app.components.live_price_header import live_price_header
from streamlit_app.components.prediction_row import prediction_row
from streamlit_app.data.live_features import fetch_live_candles, render_sparkline


def render(current_price=None, price_change_24h=None):

    # Debug info (optioneel)
    st.write("Current price:", current_price)
    st.write("24h change:", price_change_24h)

    # --- Live Price Header ---
    live_price_header(
        symbol="BTC",
        price=current_price,
        change_pct=price_change_24h
    )

    # --- Sparkline ---
    df = fetch_live_candles("BTCUSDT", "1m", limit=50)

    st.write("Sparkline wordt aangeroepen")
    st.write(df.head())

    st.subheader("BTC Sparkline")
    render_sparkline(df)

    # --- Page content ---
    st.title("Market Overview")
    st.write("This is the overview page. Add charts, summaries, and market data here.")

    # --- Predictions Row ---
    predictions = [
        {"title": "1D Forecast", "value": "Bullish", "confidence": 0.78, "color": "#4caf50"},
        {"title": "1W Forecast", "value": "Neutral", "confidence": 0.55, "color": "#ffb300"},
        {"title": "1M Forecast", "value": "Bearish", "confidence": 0.32, "color": "#e53935"},
    ]

    prediction_row(predictions)

    # --- Technical Analysis Gauge ---
    ta_gauge("Technical rating", "Buy", 0.72)
