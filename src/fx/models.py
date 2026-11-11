"""
Weekly models and walk-forward evaluation.

Three questions per market, each with a deliberately simple, explainable model
and an honest benchmark:

| Question                         | Model                                   | Benchmark                    |
|----------------------------------|-----------------------------------------|------------------------------|
| Will next week close higher?     | Logistic regression on weekly features  | Up-share in the training set |
| How much will it move (return)?  | Ridge regression on the same features   | Random walk (0% change)      |
| How volatile will next week be?  | HAR-style regression on log volatility  | Last 4-week average vol      |

The 80% expected range = current close x exp(+/- 1.2816 x predicted weekly vol).
It is centred on the random walk on purpose: in FX the random walk is very hard
to beat (Meese & Rogoff, 1983), and the evaluation shows whether ours does.

Walk-forward: the model is refitted every `refit_every` weeks on all data before
the forecast week only (expanding window). No test week is ever used for training.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

Z80 = 1.2816  # two-sided 80% interval of a normal distribution
VOL_FEATURES = ["vol_1w", "vol_4w", "vol_12w"]


@dataclass
class WeeklyModels:
    features: list[str]
    direction: object = None
    ret: object = None
    vol: object = None
    base_rate_up: float = 0.5
    coefficients: dict = field(default_factory=dict)

    def fit(self, train: pd.DataFrame) -> "WeeklyModels":
        train = train.dropna(subset=self.features + ["y_up", "y_ret", "y_vol"])
        X = train[self.features].to_numpy()
        self.base_rate_up = float(train["y_up"].mean())

        self.direction = make_pipeline(StandardScaler(), LogisticRegression(C=0.5, max_iter=1000))
        self.direction.fit(X, train["y_up"].astype(int))

        self.ret = make_pipeline(StandardScaler(), Ridge(alpha=10.0))
        self.ret.fit(X, train["y_ret"])

        Xv = np.log(train[VOL_FEATURES].clip(lower=1e-6))
        self.vol = LinearRegression().fit(Xv, np.log(train["y_vol"].clip(lower=1e-6)))
        # Correct the log-normal bias so the vol forecast is unbiased on average.
        resid = np.log(train["y_vol"].clip(lower=1e-6)) - self.vol.predict(Xv)
        self._vol_bias = float(np.exp(resid.var() / 2))

        logit = self.direction.named_steps["logisticregression"]
        self.coefficients = dict(zip(self.features, logit.coef_[0].round(3)))
        return self

    def predict(self, rows: pd.DataFrame) -> pd.DataFrame:
        X = rows[self.features].to_numpy()
        out = pd.DataFrame(index=rows.index)
        out["p_up"] = self.direction.predict_proba(X)[:, 1]
        out["ret_hat"] = self.ret.predict(X)
        Xv = np.log(rows[VOL_FEATURES].clip(lower=1e-6))
        out["vol_hat"] = np.exp(self.vol.predict(Xv)) * self._vol_bias
        out["low_80"] = rows["close"] * np.exp(-Z80 * out["vol_hat"])
        out["high_80"] = rows["close"] * np.exp(Z80 * out["vol_hat"])
        return out


def walk_forward(data: pd.DataFrame, features: list[str], min_train: int = 156,
                 refit_every: int = 4) -> pd.DataFrame:
    """Out-of-sample forecasts for every week after the first `min_train` weeks."""
    usable = data.dropna(subset=features)
    labelled = usable.dropna(subset=["y_up", "y_ret", "y_vol"])
    if len(labelled) <= min_train + 10:
        raise ValueError(f"Not enough weekly history ({len(labelled)} weeks) for walk-forward")

    preds = []
    model = None
    test_weeks = labelled.index[min_train:]
    for i, week in enumerate(test_weeks):
        if model is None or i % refit_every == 0:
            # Only rows whose target was fully known before `week` closed.
            train = labelled[labelled.index < week]
            model = WeeklyModels(features).fit(train)
        p = model.predict(labelled.loc[[week]])
        p["base_rate_up"] = model.base_rate_up
        preds.append(p)
    out = pd.concat(preds)
    return out.join(labelled[["close", "y_up", "y_ret", "y_vol", "vol_4w"]])


def evaluate(wf: pd.DataFrame) -> dict:
    """Summary statistics of a walk-forward run, each next to its benchmark."""
    y_up = wf["y_up"]
    hit = float(((wf["p_up"] > 0.5) == (y_up == 1)).mean())
    hit_bench = float(((wf["base_rate_up"] > 0.5) == (y_up == 1)).mean())
    brier = float(((wf["p_up"] - y_up) ** 2).mean())
    brier_bench = float(((wf["base_rate_up"] - y_up) ** 2).mean())

    rmse_model = float(np.sqrt(((wf["y_ret"] - wf["ret_hat"]) ** 2).mean()))
    rmse_rw = float(np.sqrt((wf["y_ret"] ** 2).mean()))

    vol_rmse = float(np.sqrt(((wf["y_vol"] - wf["vol_hat"]) ** 2).mean()))
    vol_rmse_naive = float(np.sqrt(((wf["y_vol"] - wf["vol_4w"]) ** 2).mean()))

    next_close = wf["close"] * np.exp(wf["y_ret"])
    inside = (next_close >= wf["low_80"]) & (next_close <= wf["high_80"])

    return {
        "weeks": int(len(wf)),
        "from": wf.index[0].date().isoformat(),
        "to": wf.index[-1].date().isoformat(),
        "hit_rate": hit,
        "hit_rate_benchmark": hit_bench,
        "brier": brier,
        "brier_benchmark": brier_bench,
        "theil_u": rmse_model / rmse_rw if rmse_rw else float("nan"),
        "vol_rmse_ratio": vol_rmse / vol_rmse_naive if vol_rmse_naive else float("nan"),
        "band_coverage": float(inside.mean()),
    }
