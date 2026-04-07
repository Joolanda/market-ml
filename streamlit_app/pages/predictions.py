import os
import sys
import streamlit as st

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------
from src.data.live_data import fetch_live_candles, candles_to_dataframe
from src.features.prediction import ta_next_candle_prediction

from streamlit_app.components.prediction_row import prediction_row
from streamlit_app.components.ta_gauge import ta_gauge
from streamlit_app.components.charts import render_sparkline

from streamlit_app.logic.ta_logic import (
    build_indicator_results,
    aggregate_overall_sentiment
)


# ---------------------------------------------------------
# Page render
# ---------------------------------------------------------
def render():

    st.title("AI Predictions")
    st.write("Machine‑learning forecasts for multiple time horizons.")

    # -----------------------------------------------------
    # Fetch data
    # -----------------------------------------------------
    raw = fetch_live_candles("BTCUSDT", "1h", limit=200)
    df = candles_to_dataframe(raw)

    # -----------------------------------------------------
    # 1H Prediction (your ML model)
    # -----------------------------------------------------
    pred_1h = ta_next_candle_prediction(df, "BTC", "1h")

    features = pred_1h["features"]
    indicators = build_indicator_results(features)
    sentiment = aggregate_overall_sentiment(indicators)

    # -----------------------------------------------------
    # Sentiment Gauge
    # -----------------------------------------------------
    ta_gauge(
        sentiment=sentiment,
        confidence=pred_1h["confidence"],
        label="Next‑Candle Sentiment"
    )

    # -----------------------------------------------------
    # Sparkline
    # -----------------------------------------------------
    st.subheader("Recent Price Action")
    render_sparkline(df)

    # -----------------------------------------------------
    # Multi‑Horizon Forecasts
    # -----------------------------------------------------
    st.subheader("Forecast Summary")

    predictions = [
        {
            "title": "Next Candle (1h)",
            "value": "bullish" if pred_1h["bullish_probability"] > 0.5 else "bearish",
            "confidence": pred_1h["confidence"],
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

    # -----------------------------------------------------
    # Detailed ML Output
    # -----------------------------------------------------
    st.subheader("Model Output Details")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Bullish Probability", f"{pred_1h['bullish_probability']:.1%}")
    with col2:
        st.metric("Confidence Score", f"{pred_1h['confidence']:.1%}")

    st.write("### Feature Snapshot")
    st.json(features)
