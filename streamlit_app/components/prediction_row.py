import streamlit as st

def prediction_card(title: str, value: str, confidence: float, color: str):
    st.markdown(
        f"""
        <div class="prediction-card">
            <div class="prediction-title">{title}</div>
            <div class="prediction-value" style="color:{color};">{value}</div>
            <div class="prediction-confidence">Confidence: {confidence:.0%}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def prediction_row(predictions: list):
    """
    predictions = [
        {"title": "1D Forecast", "value": "Bullish", "confidence": 0.78, "color": "#4caf50"},
        {"title": "1W Forecast", "value": "Neutral", "confidence": 0.55, "color": "#ffb300"},
        {"title": "1M Forecast", "value": "Bearish", "confidence": 0.32, "color": "#e53935"},
    ]
    """
    cols = st.columns(len(predictions))

    for col, pred in zip(cols, predictions):
        with col:
            prediction_card(
                title=pred["title"],
                value=pred["value"],
                confidence=pred["confidence"],
                color=pred["color"]
            )
