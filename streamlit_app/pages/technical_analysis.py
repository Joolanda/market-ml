import streamlit as st

from streamlit_app.components.ta_bar import ta_bar
from streamlit_app.components.ta_indicator import ta_indicator_table
from streamlit_app.logic.ta_logic import (
    build_indicator_results,
    aggregate_overall_sentiment,
)
from streamlit_app.data.feature_loader import load_features


TIMEFRAME_LABELS = {
    "15m": "15m",
    "1h": "1H",
    "4h": "4H",
    "1d": "1D",
}

def _timeframe_selector() -> str:
    if "ta_timeframe" not in st.session_state:
        st.session_state["ta_timeframe"] = "1h"

    selected = st.radio(
        "Select timeframe",
        list(TIMEFRAME_LABELS.keys()),
        format_func=lambda x: TIMEFRAME_LABELS[x],
        horizontal=True,
        key="ta_timeframe_radio"
    )

    st.session_state["ta_timeframe"] = selected
    return selected


def render(current_price=None, price_change_24h=None):
    st.title("Technical Analysis")

    timeframe = _timeframe_selector()
    st.caption(f"Technical view for timeframe: {TIMEFRAME_LABELS[timeframe]}")

    # Load engineered features from CSVs
    features = load_features(timeframe)

   # Pak de laatste rij met indicatorwaarden
    # Gebruik de laatste rij waar RSI wél een waarde heeft
    last = features.dropna(subset=["rsi"]).iloc[-1]


    indicator_results = build_indicator_results({
        "rsi": last["rsi"],
        "macd": last["macd"],
        "macd_signal": last["macd_signal"],
        "sma_20": last["sma_20"],
        "sma_50": last["sma_50"],
        "bb_position": last["bb_position"],
        "volume_ratio": last["volume_ratio"],
    })

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
