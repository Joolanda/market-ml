import pandas as pd

def load_raw_candles(asset: str, timeframe: str) -> pd.DataFrame:
    """
    Load raw candle data for a given asset and timeframe.
    Expects files in: data/raw/{asset}_{timeframe}_raw.csv
    """
    path = f"data/raw/{asset}_{timeframe}_raw.csv"
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
