import os
import sys
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------
from src.data.live_data import fetch_live_candles, candles_to_dataframe
from streamlit_app.logic.ta_logic import build_indicator_results, aggregate_overall_sentiment


# ---------------------------------------------------------
# Page render
# ---------------------------------------------------------
def render():

    st.title("Historical Analysis")
    st.write("Explore long‑term trends, volatility and technical signals.")

    # -----------------------------------------------------
    # Fetch historical candles
    # -----------------------------------------------------
    raw = fetch_live_candles("BTCUSDT", "1d", limit=500)
    df = candles_to_dataframe(raw)

    # -----------------------------------------------------
    # Ensure datetime index exists
    # -----------------------------------------------------
    if not isinstance(df.index, pd.DatetimeIndex):
        st.error("DataFrame heeft geen datetime‑index. Controleer candles_to_dataframe().")
        st.write("Index:", df.index)
        st.write("Columns:", list(df.columns))
        return

    # -----------------------------------------------------
    # Compute indicators
    # -----------------------------------------------------
    df["ema10"] = df["close"].ewm(span=10).mean()
    df["ema20"] = df["close"].ewm(span=20).mean()

    df["returns"] = df["close"].pct_change()
    df["volatility"] = df["returns"].rolling(20).std()

    df["trend_strength"] = df["ema10"] - df["ema20"]

    # -----------------------------------------------------
    # EMA Trend Chart
    # -----------------------------------------------------
    st.subheader("EMA10 vs EMA20 Trend")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["close"],
        mode="lines",
        name="Close",
        line=dict(color="#4c8bf5", width=1.5)
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["ema10"],
        mode="lines",
        name="EMA10",
        line=dict(color="#16c784", width=1.2)
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["ema20"],
        mode="lines",
        name="EMA20",
        line=dict(color="#f4c542", width=1.2)
    ))

    fig.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=30, b=10),
        template="plotly_dark"
    )

    st.plotly_chart(fig, width="stretch")

    # -----------------------------------------------------
    # Volatility + Trend Strength
    # -----------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Volatility (20‑period)")
        st.line_chart(df["volatility"], height=200)

    with col2:
        st.subheader("Trend Strength (EMA10 − EMA20)")
        st.line_chart(df["trend_strength"], height=200)

    # -----------------------------------------------------
    # TA Indicator Table
    # -----------------------------------------------------
    st.subheader("Technical Indicator Summary")

    last_features = {
        "rsi": df["rsi"].iloc[-1] if "rsi" in df else None,
        "macd": df["macd"].iloc[-1] if "macd" in df else None,
        "macd_signal": df["macd_signal"].iloc[-1] if "macd_signal" in df else None,
        "ema_10": df["ema10"].iloc[-1],
        "ema_20": df["ema20"].iloc[-1],
        "bb_width": df["bb_width"].iloc[-1] if "bb_width" in df else None,
        "vol_ratio": (
            df["volume"].iloc[-1] / df["volume"].rolling(20).mean().iloc[-1]
            if "volume" in df else None
        ),
    }

    indicators = build_indicator_results(last_features)
    overall_sentiment = aggregate_overall_sentiment(indicators)

    rows = []
    for ind in indicators:
        rows.append({
            "Indicator": ind.name,
            "Status": ind.status,
            "Trend Support": ind.trend_support,
        })

    st.table(rows)

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------
    st.markdown(f"### Overall sentiment: **{overall_sentiment.upper()}**")
