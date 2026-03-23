import time
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix
)
from src.ml.training.trainer_legacy import train_model


def evaluate_model(y_true, y_pred):
    """Compute a rich set of classification metrics."""
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
    }

    # ROC AUC only if predictions are binary 0/1
    try:
        metrics["roc_auc"] = roc_auc_score(y_true, y_pred)
    except Exception:
        metrics["roc_auc"] = np.nan

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    metrics["confusion_matrix"] = cm.tolist()

    return metrics


def compare_models(models: dict, X, y):
    """
    Train and evaluate multiple models.
    Returns a DataFrame with metrics and ranking.
    """
    results = []

    for name, model in models.items():
        print(f"\n🚀 Training {name}...")

        # Training time
        t0 = time.time()
        preds, y_test = train_model(model, X, y)
        train_time = time.time() - t0

        # Inference time
        t1 = time.time()
        _ = model.predict(X[:200])   # small batch for speed
        inference_time = time.time() - t1

        # Metrics
        metrics = evaluate_model(y_test, preds)

        results.append({
            "model": name,
            "train_time_sec": round(train_time, 4),
            "inference_time_sec": round(inference_time, 4),
            **metrics
        })

    # Convert to DataFrame
    df = pd.DataFrame(results)

    # Ranking by F1
    df["rank"] = df["f1"].rank(ascending=False).astype(int)
    df = df.sort_values("rank")

    return df
