from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


def evaluate_classification_v2(y_true, y_pred, mode="multiclass"):
    """
    Unified evaluator for binary and multiclass classification.
    Returns accuracy + precision/recall/F1 depending on mode.
    """

    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
    }

    if mode == "binary":
        metrics.update({
            "precision": precision_score(y_true, y_pred, average="binary", zero_division=0),
            "recall": recall_score(y_true, y_pred, average="binary", zero_division=0),
            "f1": f1_score(y_true, y_pred, average="binary", zero_division=0),
            "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        })

    elif mode == "multiclass":
        metrics.update({
            "precision_macro": precision_score(y_true, y_pred, average="macro", zero_division=0),
            "recall_macro": recall_score(y_true, y_pred, average="macro", zero_division=0),
            "f1_macro": f1_score(y_true, y_pred, average="macro", zero_division=0),

            "precision_weighted": precision_score(y_true, y_pred, average="weighted", zero_division=0),
            "recall_weighted": recall_score(y_true, y_pred, average="weighted", zero_division=0),
            "f1_weighted": f1_score(y_true, y_pred, average="weighted", zero_division=0),

            "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        })

    else:
        raise ValueError("mode must be 'binary' or 'multiclass'")

    return metrics
