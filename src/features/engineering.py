import pandas as pd
import numpy as np


# ============================================================
# 1. RAW LOADER
# ============================================================

import pandas as pd

def load_raw_candles(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Detect timestamp format
    sample = str(df["open_time"].iloc[0])

    if sample.isdigit():
        # Milliseconds since epoch
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
        df["close_time"] = pd.to_datetime(df["close_time"], unit="ms", utc=True)
    else:
        # ISO datetime string
        df["open_time"] = pd.to_datetime(df["open_time"], utc=True)
        df["close_time"] = pd.to_datetime(df["close_time"], utc=True)

    # Convert numeric columns
    numeric_cols = ["open", "high", "low", "close", "volume"]
    df[numeric_cols] = df[numeric_cols].astype(float)

    return df

# ============================================================
# 2. BASIC FEATURES
# ============================================================

def add_basic_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add simple, robust features that always work.
    """
    df = df.copy()

    # Candle body
    df["body"] = df["close"] - df["open"]

    # Upper and lower wick
    df["upper_wick"] = df["high"] - df[["open", "close"]].max(axis=1)
    df["lower_wick"] = df[["open", "close"]].min(axis=1) - df["low"]

    # Returns
    df["return"] = df["close"].pct_change()

    # High-low range
    df["hl_range"] = df["high"] - df["low"]

    return df


# ============================================================
# 3. TECHNICAL INDICATORS
# ============================================================

def add_sma(df: pd.DataFrame, periods=[20, 50, 200]) -> pd.DataFrame:
    df = df.copy()
    for p in periods:
        df[f"sma_{p}"] = df["close"].rolling(p).mean()
    return df


def add_ema(df: pd.DataFrame, periods=[20, 50, 200]) -> pd.DataFrame:
    df = df.copy()
    for p in periods:
        df[f"ema_{p}"] = df["close"].ewm(span=p, adjust=False).mean()
    return df


def add_rsi(df: pd.DataFrame, period=14) -> pd.DataFrame:
    df = df.copy()
    delta = df["close"].diff()

    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain).rolling(period).mean()
    avg_loss = pd.Series(loss).rolling(period).mean()

    rs = avg_gain / avg_loss
    df["rsi"] = 100 - (100 / (1 + rs))

    return df


def add_macd(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()

    df["macd"] = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]

    return df


def add_bollinger(df: pd.DataFrame, period=20, std_factor=2) -> pd.DataFrame:
    df = df.copy()

    sma = df["close"].rolling(period).mean()
    std = df["close"].rolling(period).std()

    df["bb_mid"] = sma
    df["bb_upper"] = sma + std_factor * std
    df["bb_lower"] = sma - std_factor * std
    df["bb_width"] = df["bb_upper"] - df["bb_lower"]

    return df


def add_atr(df: pd.DataFrame, period=14) -> pd.DataFrame:
    df = df.copy()

    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["atr"] = tr.rolling(period).mean()

    return df


def add_volume_ma(df: pd.DataFrame, period=20) -> pd.DataFrame:
    df = df.copy()
    df["volume_ma"] = df["volume"].rolling(period).mean()
    return df


def add_trend_slope(df: pd.DataFrame, period=20) -> pd.DataFrame:
    df = df.copy()
    df["trend_slope"] = df["close"].diff(period)
    return df


# ============================================================
# 4. FULL PIPELINE
# ============================================================

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full feature engineering pipeline.
    """
    df = add_basic_features(df)
    df = add_sma(df)
    df = add_ema(df)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_bollinger(df)
    df = add_atr(df)
    df = add_volume_ma(df)
    df = add_trend_slope(df)

    # Drop NaN rows created by rolling windows
    df = df.dropna()

    return df
