import streamlit as st
from typing import Literal

Sentiment = Literal["bullish", "neutral", "bearish"]


def _sentiment_color(sentiment: Sentiment) -> str:
    if sentiment == "bullish":
        return "#16c784"   # groen
    if sentiment == "bearish":
        return "#ea3943"   # rood
    return "#f4c542"       # geel (neutral)


def _sentiment_label(sentiment: Sentiment) -> str:
    if sentiment == "bullish":
        return "Bullish"
    if sentiment == "bearish":
        return "Bearish"
    return "Neutral"


def ta_gauge(sentiment: Sentiment, confidence: float, label: str = "Market Sentiment"):
    """
    TradingView-style sentiment gauge.
    - sentiment: bullish / bearish / neutral
    - confidence: 0.0 → 1.0
    """

    color = _sentiment_color(sentiment)
    sentiment_text = _sentiment_label(sentiment)
    pct = int(confidence * 100)

    st.markdown(
        f"""
        <style>
        .gauge-container {{
            width: 100%;
            text-align: center;
            margin-top: 10px;
            margin-bottom: 20px;
        }}

        .gauge-label {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 6px;
        }}

        .gauge-circle {{
            width: 140px;
            height: 140px;
            border-radius: 50%;
            border: 10px solid {color};
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            font-size: 1.4rem;
            font-weight: 700;
            color: {color};
        }}

        .gauge-subtext {{
            margin-top: 6px;
            font-size: 0.9rem;
            color: #888;
        }}
        </style>

        <div class="gauge-container">
            <div class="gauge-label">{label}</div>
            <div class="gauge-circle">{pct}%</div>
            <div class="gauge-subtext">{sentiment_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
