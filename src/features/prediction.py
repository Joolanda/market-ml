import numpy as np

def safe(x):
    """Convert None/NaN to 0 for safety."""
    try:
        if x is None or np.isnan(x):
            return 0
        return float(x)
    except:
        return 0


def extract_latest_features(df):
    """
    Extract the last row of engineered features in a safe way.
    Ensures no KeyErrors and no NaN explosions.
    """

    last = df.iloc[-1]

    features = {
        # Basic structure
        "body": safe(last.get("body")),
        "upper_wick": safe(last.get("upper_wick")),
        "lower_wick": safe(last.get("lower_wick")),
        "return": safe(last.get("return")),
        "hl_range": safe(last.get("hl_range")),

        # Trend
        "ema_10": safe(last.get("ema_10")),
        "ema_20": safe(last.get("ema_20")),
        "trend_strength": safe(last.get("trend_strength")),
        "trend_slope": safe(last.get("trend_slope")),

        # Momentum
        "rsi": safe(last.get("rsi")),
        "macd": safe(last.get("macd")),
        "macd_signal": safe(last.get("macd_signal")),
        "macd_hist": safe(last.get("macd_hist")),

        # Volatility
        "atr": safe(last.get("atr")),
        "volatility_10": safe(last.get("volatility_10")),
        "volatility_20": safe(last.get("volatility_20")),

        # Volume
        "volume_ma": safe(last.get("volume_ma")),
        "vol_ratio": safe(last.get("vol_ratio")),
    }

    return features


def ta_next_candle_prediction(df, asset="btc", timeframe="15m"):
    """
    Lightweight rule-based prediction using engineered features.
    No ML yet — but structured so ML can be plugged in later.
    """

    if df is None or len(df) < 5:
        raise ValueError("Not enough rows for prediction")

    features = extract_latest_features(df)

    # ---------------------------------------------------------
    # Simple rule-based directional logic
    # ---------------------------------------------------------

    # Trend bias
    trend = features["trend_strength"]
    macd_hist = features["macd_hist"]
    rsi = features["rsi"]

    bullish_score = 0
    bearish_score = 0

    # Trend strength
    if trend > 0:
        bullish_score += 1
    else:
        bearish_score += 1

    # MACD histogram
    if macd_hist > 0:
        bullish_score += 1
    else:
        bearish_score += 1

    # RSI
    if rsi < 30:
        bullish_score += 1
    elif rsi > 70:
        bearish_score += 1

    # ---------------------------------------------------------
    # Convert to probabilities
    # ---------------------------------------------------------
    total = bullish_score + bearish_score
    if total == 0:
        bullish_prob = 0.5
        bearish_prob = 0.5
    else:
        bullish_prob = bullish_score / total
        bearish_prob = bearish_score / total

    confidence = abs(bullish_prob - bearish_prob)

    # Expected next close (very naive placeholder)
    last_close = df["close"].iloc[-1]
    expected_close = last_close * (1 + (bullish_prob - bearish_prob) * 0.002)

    return {
        "bullish_probability": bullish_prob,
        "bearish_probability": bearish_prob,
        "confidence": confidence,
        "expected_close": expected_close,
        "features": features,
    }
