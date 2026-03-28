# streamlit_app/components/ta_bar.py

import streamlit as st
from typing import Literal

Sentiment = Literal["bearish", "neutral", "bullish"]


def _sentiment_to_label(sentiment: Sentiment) -> str:
    if sentiment == "bullish":
        return "Buy"
    if sentiment == "bearish":
        return "Sell"
    return "Neutral"


def _sentiment_to_class(sentiment: Sentiment) -> str:
    if sentiment == "bullish":
        return "ta-bar-bullish"
    if sentiment == "bearish":
        return "ta-bar-bearish"
    return "ta-bar-neutral"


def ta_bar(label: str, sentiment: Sentiment, key: str | None = None) -> None:
    css_class = _sentiment_to_class(sentiment)
    sentiment_label = _sentiment_to_label(sentiment)

    st.markdown(
        f"""
        <div class="ta-bar">
            <div class="ta-bar-label">{label}</div>
            <div class="ta-bar-track">
                <div class="ta-bar-fill {css_class}"></div>
            </div>
            <div class="ta-bar-sentiment">{sentiment_label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
