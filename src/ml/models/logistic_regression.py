from sklearn.linear_model import LogisticRegression
from .base_model import BaseModel

class LogisticRegressionModel(BaseModel):
    def __init__(self, **params):
        default_params = {
            "solver": "lbfgs",
            "max_iter": 500,
        }
        default_params.update(params)
        self.model = LogisticRegression(**default_params)

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)
