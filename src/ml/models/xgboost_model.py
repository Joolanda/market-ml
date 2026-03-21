from xgboost import XGBClassifier
from .base_model import BaseModel

class XGBoostModel(BaseModel):
    def __init__(self, **params):
        default_params = {
            "n_estimators": 200,
            "max_depth": 5,
            "learning_rate": 0.05,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "objective": "binary:logistic",
            "eval_metric": "logloss",
        }
        default_params.update(params)
        self.model = XGBClassifier(**default_params)

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)
