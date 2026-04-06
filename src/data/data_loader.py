from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")

def load_raw_candles(asset: str, timeframe: str) -> pd.DataFrame:
    """
    Load raw OHLCV data for a given asset and timeframe.
    """
    file = RAW_DIR / f"{asset.lower()}_{timeframe}_raw.csv"
    df = pd.read_csv(file)

    # Detect timestamp format
    sample = str(df["open_time"].iloc[0])

    if sample.isdigit():
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    else:
        df["open_time"] = pd.to_datetime(df["open_time"], utc=True)

    # Optional close_time
    if "close_time" in df.columns:
        sample_close = str(df["close_time"].iloc[0])
        if sample_close.isdigit():
            df["close_time"] = pd.to_datetime(df["close_time"], unit="ms", utc=True)
        else:
            df["close_time"] = pd.to_datetime(df["close_time"], utc=True)
    else:
        df["close_time"] = df["open_time"].shift(-1)

    # Convert numeric columns
    numeric_cols = ["open", "high", "low", "close", "volume"]
    df[numeric_cols] = df[numeric_cols].astype(float)

    return df.sort_values("open_time")
