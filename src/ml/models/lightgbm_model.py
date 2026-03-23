from lightgbm import LGBMClassifier
from .base_model import BaseModel

class LightGBMModel(BaseModel):
    def __init__(self, **params):
        default_params = {
            "n_estimators": 300,
            "learning_rate": 0.05,
            "num_leaves": 31,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "objective": "binary",
        }
        default_params.update(params)
        self.model = LGBMClassifier(**default_params)

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)
