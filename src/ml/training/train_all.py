from src.ml.training.candle_regression import train_candle_regression
from src.ml.horizons import MODEL_MAP

RAW_DIR = "data/raw"


def train_all_models():
    """
    Train one model per horizon defined in MODEL_MAP.
    """
    for horizon, model_name in MODEL_MAP.items():
        raw_path = f"{RAW_DIR}/btc_{horizon}_raw.csv"

        print(f"🚀 Training model for horizon {horizon} using {raw_path}")

        train_candle_regression(
            raw_path=raw_path,
            model_name=model_name
        )

    print("🎉 All models trained successfully!")
