import streamlit as st

def _sentiment_color(value: str) -> str:
    value = value.lower()
    if value == "bullish":
        return "#16c784"   # groen
    if value == "bearish":
        return "#ea3943"   # rood
    return "#f4c542"       # geel (neutral)


def _sentiment_label(value: str) -> str:
    value = value.lower()
    if value == "bullish":
        return "Bullish"
    if value == "bearish":
        return "Bearish"
    return "Neutral"


def prediction_card(title: str, value: str, confidence: float):
    color = _sentiment_color(value)
    label = _sentiment_label(value)

    st.markdown(
        f"""
        <style>
        .prediction-card {{
            background: #111;
            border-radius: 10px;
            padding: 14px 18px;
            border: 1px solid #222;
            text-align: center;
            margin-bottom: 10px;
        }}

        .prediction-title {{
            font-size: 0.9rem;
            color: #aaa;
            margin-bottom: 6px;
        }}

        .prediction-value {{
            font-size: 1.4rem;
            font-weight: 700;
            color: {color};
            margin-bottom: 4px;
        }}

        .prediction-confidence {{
            font-size: 0.85rem;
            color: #888;
        }}
        </style>

        <div class="prediction-card">
            <div class="prediction-title">{title}</div>
            <div class="prediction-value">{label}</div>
            <div class="prediction-confidence">Confidence: {confidence:.0%}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def prediction_row(predictions: list):
    """
    predictions = [
        {"title": "1D Forecast", "value": "bullish", "confidence": 0.78},
        {"title": "1W Forecast", "value": "neutral", "confidence": 0.55},
        {"title": "1M Forecast", "value": "bearish", "confidence": 0.32},
    ]
    """
    cols = st.columns(len(predictions))

    for col, pred in zip(cols, predictions):
        with col:
            prediction_card(
                title=pred["title"],
                value=pred["value"],
                confidence=pred["confidence"],
            )
