from typing import Optional, Dict, Any
from dataclasses import dataclass
import numpy as np
from sklearn.model_selection import train_test_split


@dataclass
class TrainResult:
    y_test: np.ndarray
    y_pred: np.ndarray
    y_proba: Optional[np.ndarray]
    meta: Dict[str, Any]


def train_model_v2(
    model,
    X: np.ndarray,
    y: np.ndarray,
    test_size: float = 0.2,
    random_state: int = 42,
    mode: str = "multiclass",   # "binary" or "multiclass"
    threshold: float = 0.5,
) -> TrainResult:
    """
    Modern trainer supporting both binary and multiclass classification.
    Returns predictions, probabilities (if available), and metadata.
    """

    # 1. Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, shuffle=False
    )

    # 2. Train model
    model.train(X_train, y_train)

    # 3. Predict classes
    y_pred = model.predict(X_test)

    # 4. Predict probabilities (if supported)
    y_proba = None
    if hasattr(model, "predict_proba"):
        try:
            y_proba = model.predict_proba(X_test)
        except Exception:
            y_proba = None

    # 5. Binary mode handling
    if mode == "binary":
        if y_proba is not None:
            # probability of class 1
            if y_proba.ndim == 2 and y_proba.shape[1] == 2:
                pos_proba = y_proba[:, 1]
            else:
                pos_proba = y_proba.squeeze()

            y_pred = (pos_proba >= threshold).astype(int)
        else:
            # fallback: assume y_pred is already 0/1
            y_pred = np.array(y_pred)

    # 6. Multiclass mode → leave predictions as-is
    elif mode == "multiclass":
        y_pred = np.array(y_pred)

    else:
        raise ValueError(f"Unknown mode: {mode}. Use 'binary' or 'multiclass'.")

    meta = {
        "mode": mode,
        "threshold": threshold,
        "test_size": test_size,
        "random_state": random_state,
        "model_name": model.__class__.__name__,
    }

    return TrainResult(
        y_test=y_test,
        y_pred=y_pred,
        y_proba=y_proba,
        meta=meta,
    )
