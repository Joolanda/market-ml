import joblib
import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger("PredictionService")

MODEL_DIR = Path("models")


class PredictionService:
    """
    Loads ML models and performs predictions on engineered features.
    """

    def __init__(self, model_name: str):
        self.model_path = MODEL_DIR / f"{model_name}.pkl"
        self.model = None
        self.feature_names = None

        self._load_model()

    def _load_model(self):
        """
        Load model from disk and cache it in memory.
        """
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found: {self.model_path}")

        data = joblib.load(self.model_path)

        self.model = data["model"]
        self.feature_names = data["feature_names"]

        logger.info(f"📦 Loaded model: {self.model_path}")

    def align_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Ensure the input features match the model's expected feature order.
        Missing features → fill with 0
        Extra features → drop
        """
        df = df.copy()

        for col in self.feature_names:
            if col not in df.columns:
                df[col] = 0.0

        df = df[self.feature_names]

        return df

    def predict(self, df: pd.DataFrame):
        """
        Run model prediction on a single row of features.
        """
        df = self.align_features(df)

        pred = self.model.predict(df)[0]

        return pred
