"""
Defines which prediction horizon belongs to each timeframe.
"""

# 1. Mapping: timeframe → prediction horizon
HORIZON_MAP = {
    "5m": "15m",
    "15m": "1h",
    "1h": "4h",
    "4h": "1d",
}

# 2. Mapping: horizon → model filename
MODEL_MAP = {
    "15m": "model_15m",
    "1h": "model_1h",
    "4h": "model_4h",
    "1d": "model_1d",
}


def get_horizon(timeframe: str) -> str:
    """
    Return the prediction horizon for a given timeframe.
    """
    if timeframe not in HORIZON_MAP:
        raise ValueError(f"No horizon defined for timeframe: {timeframe}")
    return HORIZON_MAP[timeframe]


def get_model_name_for_horizon(horizon: str) -> str:
    """
    Return the model name associated with a prediction horizon.
    """
    if horizon not in MODEL_MAP:
        raise ValueError(f"No model defined for horizon: {horizon}")
    return MODEL_MAP[horizon]
