import pandas as pd
import numpy as np

def add_basic_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["body"] = df["close"] - df["open"]
    df["upper_wick"] = df["high"] - df[["open", "close"]].max(axis=1)
    df["lower_wick"] = df[["open", "close"]].min(axis=1) - df["low"]
    df["return"] = df["close"].pct_change()
    df["hl_range"] = df["high"] - df["low"]
    return df

def add_sma(df, periods=[20, 50, 200]):
    df = df.copy()
    for p in periods:
        df[f"sma_{p}"] = df["close"].rolling(p).mean()
    return df

def add_ema(df, periods=[20, 50, 200]):
    df = df.copy()
    for p in periods:
        df[f"ema_{p}"] = df["close"].ewm(span=p, adjust=False).mean()
    return df

def add_rsi(df, period=14):
    df = df.copy()
    delta = df["close"].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    # FIX: avoid creating a Series without index alignment
    gain = pd.Series(gain, index=df.index)
    loss = pd.Series(loss, index=df.index)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    df["rsi"] = 100 - (100 / (1 + rs))
    return df

def add_macd(df):
    df = df.copy()
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"] = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]
    return df

def add_bollinger(df, period=20, std_factor=2):
    df = df.copy()
    sma = df["close"].rolling(period).mean()
    std = df["close"].rolling(period).std()
    df["bb_mid"] = sma
    df["bb_upper"] = sma + std_factor * std
    df["bb_lower"] = sma - std_factor * std
    df["bb_width"] = df["bb_upper"] - df["bb_lower"]
    return df

def add_atr(df, period=14):
    df = df.copy()
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["atr"] = tr.rolling(period).mean()
    return df

def add_volume_ma(df, period=20):
    df = df.copy()
    df["volume_ma"] = df["volume"].rolling(period).mean()
    return df

def add_trend_slope(df, period=20):
    df = df.copy()
    df["trend_slope"] = df["close"].diff(period)
    return df

def engineer_features(df: pd.DataFrame, asset: str, timeframe: str) -> pd.DataFrame:
    df = df.copy()

    # 1. Basic features
    df = add_basic_features(df)

    # 2. Safe moving averages
    df = add_sma(df, periods=[10, 20])
    df = add_ema(df, periods=[10, 20])

    df["trend_strength"] = df["ema_10"] - df["ema_20"]

    # 3. RSI
    df = add_rsi(df, period=14)

    # 4. MACD
    df = add_macd(df)

    # 5. Bollinger
    df = add_bollinger(df, period=20, std_factor=2)

    # 6. ATR
    df = add_atr(df, period=14)

    # 7. Volume features
    df = add_volume_ma(df, period=20)
    df["vol_ratio"] = df["volume"] / df["volume_ma"]

    # 8. Trend slope
    df = add_trend_slope(df, period=10)

    # 9. Drop NaNs
    df = df.dropna()

    # 10. Safety
    if len(df) < 5:
        raise ValueError("Not enough rows after feature engineering")

    return df
