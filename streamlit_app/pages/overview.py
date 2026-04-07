import os
import sys
import streamlit as st

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

# ---------------------------------------------------------
# Imports (new architecture)
# ---------------------------------------------------------
from streamlit_app.components.live_price_header import live_price_header
from streamlit_app.components.ta_gauge import ta_gauge
from streamlit_app.components.prediction_row import prediction_row
from streamlit_app.components.charts import render_sparkline
from streamlit_app.components.ta_indicator import ta_indicator_table

from streamlit_app.logic.ta_logic import (
    build_indicator_results,
    aggregate_overall_sentiment
)

from src.data.live_data import (
    fetch_live_candles,
    candles_to_dataframe,
    fetch_24h_stats
)

from src.features.prediction import ta_next_candle_prediction


# ---------------------------------------------------------
# Page render
# ---------------------------------------------------------
def render(current_price=None, price_change_24h=None):

    st.title("Market Overview")

    # -----------------------------------------------------
    # Live Price Header
    # -----------------------------------------------------
    live_price_header(
        symbol="BTC",
        price=current_price,
        change_pct=price_change_24h
    )

    # -----------------------------------------------------
    # Fetch candles + prediction + TA features
    # -----------------------------------------------------
    raw = fetch_live_candles("BTCUSDT", "1h", limit=200)
    df = candles_to_dataframe(raw)

    prediction = ta_next_candle_prediction(df, "BTC", "1h")
    features = prediction["features"]

    indicators = build_indicator_results(features)
    overall_sentiment = aggregate_overall_sentiment(indicators)

    # -----------------------------------------------------
    # Sentiment Gauge
    # -----------------------------------------------------
    ta_gauge(
        sentiment=overall_sentiment,
        confidence=prediction["confidence"],
        label="Overall Market Sentiment"
    )

    # -----------------------------------------------------
    # 24h Stats
    # -----------------------------------------------------
    st.subheader("24h Market Stats")

    stats = fetch_24h_stats("BTCUSDT")

    high_24h = float(stats["highPrice"])
    low_24h = float(stats["lowPrice"])
    volume_24h = float(stats["volume"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("24h High", f"${high_24h:,.2f}")
    with col2:
        st.metric("24h Low", f"${low_24h:,.2f}")
    with col3:
        st.metric("24h Volume", f"{volume_24h:,.2f} BTC")

    # -----------------------------------------------------
    # Sparkline + Volatility + Trend Strength
    # -----------------------------------------------------
    st.subheader("Short‑Term Price Action")

    render_sparkline(df)

    df["returns"] = df["close"].pct_change()
    volatility = df["returns"].rolling(20).std().iloc[-1]

    df["ema10"] = df["close"].ewm(span=10).mean()
    df["ema20"] = df["close"].ewm(span=20).mean()
    trend_strength = df["ema10"].iloc[-1] - df["ema20"].iloc[-1]

    col4, col5 = st.columns(2)
    with col4:
        st.metric("Volatility (20‑period)", f"{volatility:.4f}")
    with col5:
        st.metric("Trend Strength", f"{trend_strength:.2f}")

    # -----------------------------------------------------
    # Technical Indicator Table
    # -----------------------------------------------------
    st.subheader("Technical Indicator Summary")
    ta_indicator_table(indicators)

    # -----------------------------------------------------
    # Predictions Row (multi‑horizon)
    # -----------------------------------------------------
    st.subheader("Forecasts")

    predictions = [
        {
            "title": "Next Candle (1h)",
            "value": "bullish" if prediction["bullish_probability"] > 0.5 else "bearish",
            "confidence": prediction["confidence"],
        },
        {
            "title": "1D Forecast",
            "value": "neutral",
            "confidence": 0.55,
        },
        {
            "title": "1W Forecast",
            "value": "bearish",
            "confidence": 0.32,
        },
    ]

    prediction_row(predictions)
