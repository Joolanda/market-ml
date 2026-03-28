import streamlit as st

from streamlit_app.components.ta_bar import ta_bar
from streamlit_app.components.ta_indicator import ta_indicator_table
from streamlit_app.logic.ta_logic import (
    build_indicator_results,
    aggregate_overall_sentiment,
)
from streamlit_app.data.live_features import get_live_features  # ← JUISTE IMPORT


TIMEFRAME_LABELS = {
    "15m": "15m",
    "1h": "1H",
    "4h": "4H",
    "1d": "1D",
}


def _timeframe_selector() -> str:
    cols = st.columns(len(TIMEFRAME_LABELS))
    keys = list(TIMEFRAME_LABELS.keys())

    default_idx = 1  # default 1h
    selected = st.session_state.get("ta_timeframe", keys[default_idx])

    for i, (tf, label) in enumerate(TIMEFRAME_LABELS.items()):
        with cols[i]:
            if st.button(
                label,
                key=f"ta_tf_{tf}",
                type="secondary" if tf == selected else "primary",
            ):
                selected = tf

    st.session_state["ta_timeframe"] = selected
    return selected


def render(current_price=None, price_change_24h=None):
    st.title("Technical Analysis")

    timeframe = _timeframe_selector()
    st.caption(f"Technical view for timeframe: {TIMEFRAME_LABELS[timeframe]}")

    # Load features from capstone CSVs
    features = get_live_features(timeframe=timeframe)

    indicator_results = build_indicator_results(features)
    overall_sentiment = aggregate_overall_sentiment(indicator_results)

    st.markdown("### Technical sentiment overview")

    cols = st.columns(6)
    sentiment_map = {ind.name: ind.sentiment for ind in indicator_results}

    with cols[0]:
        ta_bar("RSI", sentiment_map.get("RSI", "neutral"))
    with cols[1]:
        ta_bar("MACD", sentiment_map.get("MACD", "neutral"))
    with cols[2]:
        ta_bar("MA (20/50)", sentiment_map.get("Moving Averages", "neutral"))
    with cols[3]:
        ta_bar("Bollinger", sentiment_map.get("Bollinger Bands", "neutral"))
    with cols[4]:
        ta_bar("Volume", sentiment_map.get("Volume", "neutral"))
    with cols[5]:
        ta_bar("Overall", overall_sentiment)

    st.markdown("---")
    ta_indicator_table(indicator_results)

    st.caption(
        "Interpretation based on feature values from the capstone feature CSVs "
        "for the selected timeframe."
    )
