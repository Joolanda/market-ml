import pandas as pd


REQUIRED_COLUMNS = [
    "open_time", "open", "high", "low", "close",
    "volume", "close_time"
]


def validate_columns(df: pd.DataFrame):
    """
    Ensure all required columns exist.
    """
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def validate_timestamps(df: pd.DataFrame):
    """
    Ensure timestamps are valid and strictly increasing.
    """
    if not pd.api.types.is_datetime64_any_dtype(df["open_time"]):
        raise ValueError("open_time must be a datetime64 column")

    if df["open_time"].isna().any():
        raise ValueError("open_time contains NaN values")

    if not df["open_time"].is_monotonic_increasing:
        raise ValueError("open_time must be strictly increasing")


def validate_numeric(df: pd.DataFrame):
    """
    Ensure numeric columns contain valid floats.
    """
    numeric_cols = ["open", "high", "low", "close", "volume"]

    for col in numeric_cols:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Column {col} must be numeric")

        if df[col].isna().any():
            raise ValueError(f"Column {col} contains NaN values")


def validate_candles(df: pd.DataFrame):
    """
    Run all validation checks.
    """
    validate_columns(df)
    validate_timestamps(df)
    validate_numeric(df)

    return True
