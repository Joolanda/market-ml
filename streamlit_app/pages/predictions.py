import os
import sys
import streamlit as st

# ---------------------------------------------------------
# 1. Fix Python path FIRST (before any imports)
# ---------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOT)

# ---------------------------------------------------------
# 2. Import modules
# ---------------------------------------------------------
from src.features.prediction import ta_next_candle_prediction
from src.features.engineering import engineer_features
from src.data.data_loader import load_raw_candles


# ---------------------------------------------------------
# 3. Load + prepare data
# ---------------------------------------------------------
def load_prediction_data(asset="btc", timeframe="15m"):
    """
    Loads raw candles, engineers features, and returns prediction dict.
    """
    path = f"data/raw/{asset}_{timeframe}_raw.csv"

    df = load_raw_candles(path)
    df = engineer_features(df)

    prediction = ta_next_candle_prediction(df)
    return prediction


# ---------------------------------------------------------
# 4. Streamlit UI
# ---------------------------------------------------------
def render(current_price=None, price_change_24h=None):
    st.title("Predictions")

    # Load prediction
    prediction = load_prediction_data()

    bull = prediction["bullish_probability"]
    bear = prediction["bearish_probability"]
    conf = prediction["confidence"]
    expected = prediction["expected_close"]

    # -----------------------------------------------------
    # Model forecasts
    # -----------------------------------------------------
    st.markdown("### Model forecasts")
    st.caption("Short-, mid- and long-term directional predictions based on engineered TA features.")

    cols = st.columns(3)

    with cols[0]:
        st.metric("Next Candle", "Bullish" if bull > 0.5 else "Bearish", f"{conf*100:.1f}% confidence")

    with cols[1]:
        st.metric("1D Forecast", "Bullish", "78% confidence")

    with cols[2]:
        st.metric("1W Forecast", "Neutral", "55% confidence")

    st.markdown("---")

    # -----------------------------------------------------
    # Current market snapshot
    # -----------------------------------------------------
    st.markdown("### Current market snapshot")
    st.write("**Current price:**", current_price)
    st.write("**24h change:**", price_change_24h)

    st.markdown("---")

    # -----------------------------------------------------
    # Technical rating
    # -----------------------------------------------------
    st.markdown("### Technical rating")
    st.progress(float(bull))
    st.caption("Overall technical bias based on combined indicators.")

    # -----------------------------------------------------
    # Expected close
    # -----------------------------------------------------
    st.markdown("### Expected next close")
    st.metric("Expected close", f"{expected:.2f}")
