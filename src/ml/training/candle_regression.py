import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor

from src.features.engineering import engineer_features
from src.features.validation import validate_candles


MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)


def load_feature_data(path: str) -> pd.DataFrame:
    """
    Load raw candles, validate them, and engineer features.
    """
    df = pd.read_csv(path)

    # Validate raw candles
    validate_candles(df)

    # Convert timestamps
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms", utc=True)

    # Convert numeric columns
    numeric_cols = ["open", "high", "low", "close", "volume"]
    df[numeric_cols] = df[numeric_cols].astype(float)

    # Add features
    df = engineer_features(df)

    return df


def create_targets(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create next-candle regression targets.
    """
    df = df.copy()

    df["open_next"] = df["open"].shift(-1)
    df["high_next"] = df["high"].shift(-1)
    df["low_next"] = df["low"].shift(-1)
    df["close_next"] = df["close"].shift(-1)

    df = df.dropna()

    return df


def train_candle_regression(raw_path: str, model_name: str = "candle_regressor"):
    """
    Train a regression model to predict next OHLC values.
    """
    df = load_feature_data(raw_path)
    df = create_targets(df)

    # Features = all engineered columns except timestamps + targets
    target_cols = ["open_next", "high_next", "low_next", "close_next"]
    drop_cols = ["open_time", "close_time"] + target_cols

    feature_df = df.drop(columns=drop_cols)
    target_df = df[target_cols]

    # Train a simple baseline model
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )

    model.fit(feature_df, target_df)

    # Save model + feature names
    out_path = MODEL_DIR / f"{model_name}.pkl"
    joblib.dump({
        "model": model,
        "feature_names": list(feature_df.columns)
    }, out_path)

    print(f"📦 Model saved to {out_path}")
