from src.ml.models.random_forest import RandomForestModel
from src.ml.models.logistic_regression import LogisticRegressionModel
from src.ml.models.xgboost_model import XGBoostModel
from src.ml.comparison.compare_legacy import compare_models

# TODO: load your dataset here
X, y = ...

models = {
    "RandomForest": RandomForestModel(),
    "LogisticRegression": LogisticRegressionModel(),
    "XGBoost": XGBoostModel(),
}

df = compare_models(models, X, y)
print(df)
