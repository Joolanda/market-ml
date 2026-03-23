import pandas as pd
from typing import Dict, Any, List
from sklearn.metrics import roc_auc_score
from src.ml.training.trainer import train_model_v2 as train_model
from src.ml.evaluation.metrics import evaluate_classification_v2

def compare_models_v2(
    models: Dict[str, Any],
    X,
    y,
    mode: str = "multiclass",
    sort_by: str = "accuracy",
    return_df: bool = True
):
    """
    Clean, modern model comparison.
    Supports:
    - binary + multiclass
    - probabilities (if model supports predict_proba)
    - ROC-AUC (binary + multiclass)
    - optional DataFrame export
    """

    results = []

    for name, model in models.items():
        # Train using modern trainer
        train_result = train_model(
            model=model,
            X=X,
            y=y,
            mode=mode
        )

        # Evaluate predictions
        metrics = evaluate_classification_v2(
            y_true=train_result.y_test,
            y_pred=train_result.y_pred,
            mode=mode
        )

        # Add ROC-AUC if probabilities exist
        if train_result.y_proba is not None:
            try:
                if mode == "binary":
                    metrics["roc_auc"] = roc_auc_score(
                        train_result.y_test,
                        train_result.y_proba[:, 1] if train_result.y_proba.ndim == 2 else train_result.y_proba
                    )
                else:
                    metrics["roc_auc_macro"] = roc_auc_score(
                        train_result.y_test,
                        train_result.y_proba,
                        multi_class="ovr",
                        average="macro"
                    )
            except Exception:
                metrics["roc_auc"] = None

        results.append({
            "model": name,
            **metrics,
            **train_result.meta
        })

    # Convert to DataFrame
    df = pd.DataFrame(results)

    # Sort
    df = df.sort_values(sort_by, ascending=False)

    return df if return_df else results
