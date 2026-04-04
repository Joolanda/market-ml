import numpy as np
import pandas as pd


def ta_next_candle_prediction(df: pd.DataFrame) -> dict:
    """
    Simple but effective TA-based next-candle predictor.
    Uses engineered features to estimate direction and confidence.
    """

    latest = df.iloc[-1]

    # -------------------------
    # 1. Feature scoring
    # -------------------------

    score = 0
    max_score = 0

    # RSI
    if latest["rsi"] > 55:
        score += 1
    elif latest["rsi"] < 45:
        score -= 1
    max_score += 1

    # MACD histogram
    if latest["macd_hist"] > 0:
        score += 1
    else:
        score -= 1
    max_score += 1

    # SMA20 vs SMA50
    if latest["sma_20"] > latest["sma_50"]:
        score += 1
    else:
        score -= 1
    max_score += 1

    # Bollinger position
    if latest["close"] < latest["bb_lower"]:
        score += 1  # oversold → bullish
    elif latest["close"] > latest["bb_upper"]:
        score -= 1  # overextended → bearish
    max_score += 1

    # Volume confirmation
    if latest["volume"] > latest["volume_ma"]:
        score += 1
    else:
        score -= 1
    max_score += 1

    # Trend slope
    if latest["trend_slope"] > 0:
        score += 1
    else:
        score -= 1
    max_score += 1

    # -------------------------
    # 2. Convert score → probabilities
    # -------------------------

    bullish_prob = (score + max_score) / (2 * max_score)
    bearish_prob = 1 - bullish_prob

    # -------------------------
    # 3. Expected close
    # -------------------------

    expected_move = latest["atr"] * (bullish_prob - bearish_prob)
    expected_close = latest["close"] + expected_move

    # -------------------------
    # 4. Confidence
    # -------------------------

    confidence = abs(score) / max_score

    return {
        "bullish_probability": float(bullish_prob),
        "bearish_probability": float(bearish_prob),
        "expected_close": float(expected_close),
        "expected_range": float(latest["atr"]),
        "confidence": float(confidence),
        "raw_score": int(score),
    }
