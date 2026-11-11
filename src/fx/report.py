"""
FX Weekly report: one forecast per market plus an honest track record.

    python cli.py fx-weekly            # writes reports/fx_weekly/<date>.md and latest.md
    python cli.py fx-eval              # track record table only

For every asset in src/config/assets.py:
1. Build weekly features (src/fx/weekly.py).
2. Walk-forward evaluation over the past (src/fx/models.py) -> track record vs benchmarks.
3. Fit on all weeks whose outcome is known and forecast the next week from the
   most recent completed week.

The same `AssetOutlook` objects feed the Markdown report and the Streamlit page,
so the app and the report never disagree.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from src.config.assets import ASSETS, Asset, get_asset
from src.data.data_loader import load_daily, load_rates
from src.fx.models import WeeklyModels, evaluate, walk_forward
from src.fx.weekly import build_dataset, feature_columns

REPORT_DIR = Path("reports/fx_weekly")

# Plain-language names for the features, used in the "drivers" line.
FEATURE_LABELS = {
    "ret_1w": "last week's move",
    "ret_4w": "4-week momentum",
    "ret_12w": "12-week momentum",
    "vol_1w": "last week's volatility",
    "vol_4w": "4-week volatility",
    "vol_12w": "12-week volatility",
    "rsi_14w": "weekly RSI",
    "dist_sma_26w": "distance to 26-week average",
    "range_1w": "last week's trading range",
    "rate_diff": "interest-rate differential",
    "rate_diff_chg_3m": "change in rate differential (3m)",
}

LEAN_THRESHOLD = 0.05  # |P(up) - 0.5| below this counts as "no clear direction"


@dataclass
class AssetOutlook:
    asset: Asset
    source: str                   # "real" or "sample"
    as_of: pd.Timestamp           # Friday close the forecast is made from
    close: float
    p_up: float
    low_80: float
    high_80: float
    vol_hat: float                # predicted weekly vol (log-return std)
    vol_regime: str               # "low" / "normal" / "high"
    vol_percentile: float         # where vol_hat sits in the history of weekly vol
    drivers: List[tuple] = field(default_factory=list)  # (feature, contribution)
    track: Dict[str, float] = field(default_factory=dict)
    history: Optional[pd.DataFrame] = None  # walk-forward frame, for charts

    @property
    def direction(self) -> str:
        if self.p_up >= 0.5 + LEAN_THRESHOLD:
            return "leaning up"
        if self.p_up <= 0.5 - LEAN_THRESHOLD:
            return "leaning down"
        return "no clear direction"

    @property
    def week_ending(self) -> pd.Timestamp:
        return self.as_of + pd.Timedelta(days=7)

    def fmt(self, x: float) -> str:
        return f"{x:,.{self.asset.decimals}f}"


def _vol_regime(vol_hat: float, vol_history: pd.Series) -> tuple[str, float]:
    hist = vol_history.dropna()
    pct = float((hist < vol_hat).mean()) if len(hist) else 0.5
    if pct < 1 / 3:
        return "low", pct
    if pct > 2 / 3:
        return "high", pct
    return "normal", pct


def _drivers(model: WeeklyModels, row: pd.DataFrame, top: int = 3) -> List[tuple]:
    """Largest contributions (coefficient x standardised value) to the up/down logit."""
    scaler = model.direction.named_steps["standardscaler"]
    logit = model.direction.named_steps["logisticregression"]
    z = scaler.transform(row[model.features].to_numpy())[0]
    contrib = logit.coef_[0] * z
    order = np.argsort(-np.abs(contrib))[:top]
    return [(model.features[i], float(contrib[i])) for i in order]


def build_outlook(asset_key: str, with_history: bool = True) -> AssetOutlook:
    asset = get_asset(asset_key)
    daily = load_daily(asset.key)
    rates = load_rates()
    data = build_dataset(daily.df, rates.df, asset)
    features = feature_columns(data)

    # Track record: out-of-sample only.
    wf = walk_forward(data, features)
    track = evaluate(wf)

    # Today's forecast: train on every week with a known outcome,
    # predict from the most recent completed week.
    labelled = data.dropna(subset=features + ["y_up", "y_ret", "y_vol"])
    latest = data.dropna(subset=features).iloc[[-1]]
    model = WeeklyModels(features).fit(labelled)
    pred = model.predict(latest).iloc[0]

    regime, pct = _vol_regime(float(pred["vol_hat"]), data["vol_1w"])
    return AssetOutlook(
        asset=asset,
        source=daily.source,
        as_of=latest.index[0],
        close=float(latest["close"].iloc[0]),
        p_up=float(pred["p_up"]),
        low_80=float(pred["low_80"]),
        high_80=float(pred["high_80"]),
        vol_hat=float(pred["vol_hat"]),
        vol_regime=regime,
        vol_percentile=pct,
        drivers=_drivers(model, latest),
        track=track,
        history=wf if with_history else None,
    )


def build_all(asset_keys: Optional[List[str]] = None) -> List[AssetOutlook]:
    return [build_outlook(k) for k in (asset_keys or list(ASSETS))]


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------

def _pct(x: float, digits: int = 1) -> str:
    return f"{x * 100:.{digits}f}%"


def verdict(track: Dict[str, float]) -> str:
    """One honest sentence about whether the models add value over the benchmarks."""
    parts = []
    if track["brier"] < track["brier_benchmark"]:
        parts.append("the direction model beats the base rate")
    else:
        parts.append("the direction model does **not** beat the base rate")
    if track["theil_u"] < 1:
        parts.append("the return model edges out the random walk")
    else:
        parts.append("the random walk remains the better return forecast")
    if track["vol_rmse_ratio"] < 1:
        parts.append("the volatility model beats the 4-week average")
    else:
        parts.append("the volatility model does not beat the 4-week average")
    return "Out of sample, " + ", ".join(parts[:-1]) + " and " + parts[-1] + "."


def track_record_table(outlooks: List[AssetOutlook]) -> str:
    lines = [
        "| Market | Weeks | Hit rate (bench) | Brier (bench) | Theil's U | Vol RMSE ratio | 80% band coverage |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for o in outlooks:
        t = o.track
        lines.append(
            f"| {o.asset.name} | {t['weeks']} "
            f"| {_pct(t['hit_rate'])} ({_pct(t['hit_rate_benchmark'])}) "
            f"| {t['brier']:.3f} ({t['brier_benchmark']:.3f}) "
            f"| {t['theil_u']:.3f} | {t['vol_rmse_ratio']:.3f} | {_pct(t['band_coverage'])} |"
        )
    lines.append("")
    lines.append(
        "*Theil's U and the vol RMSE ratio are below 1 when the model beats its benchmark "
        "(random walk / 4-week average vol). Lower Brier is better. "
        "A well-calibrated 80% band contains next week's close about 80% of the time.*"
    )
    return "\n".join(lines)


def asset_section(o: AssetOutlook) -> str:
    drivers = ", ".join(
        f"{FEATURE_LABELS.get(f, f)} ({'+' if c >= 0 else '−'})" for f, c in o.drivers
    )
    t = o.track
    return "\n".join([
        f"## {o.asset.name}",
        "",
        f"*{o.asset.note}*",
        "",
        f"| | |",
        f"|---|---|",
        f"| Close {o.as_of:%a %d %b %Y} | **{o.fmt(o.close)}** |",
        f"| P(higher by {o.week_ending:%d %b}) | **{_pct(o.p_up, 0)}** — {o.direction} |",
        f"| 80% expected range | {o.fmt(o.low_80)} – {o.fmt(o.high_80)} |",
        f"| Expected weekly volatility | {_pct(o.vol_hat, 2)} — **{o.vol_regime}** "
        f"(higher than {_pct(o.vol_percentile, 0)} of past weeks) |",
        "",
        f"**What moves the signal:** {drivers} (sign = push towards up / down).",
        "",
        f"**Track record** ({t['from']} to {t['to']}, {t['weeks']} weeks): {verdict(t)}",
        "",
    ])


def render_markdown(outlooks: List[AssetOutlook], today: Optional[date] = None) -> str:
    today = today or date.today()
    sources = {o.source for o in outlooks}
    as_of = max(o.as_of for o in outlooks)

    header = [
        f"# FX Weekly — {as_of:%d %B %Y}",
        "",
        f"Generated {today:%Y-%m-%d} from the Friday close of {as_of:%d %b %Y}.",
        "",
    ]
    if "sample" in sources:
        header += [
            "> ⚠️ **Sample data.** At least one market uses synthetic data "
            "(no download available). Run `python cli.py fetch-data` for real prices.",
            "",
        ]

    summary = [
        "## At a glance",
        "",
        "| Market | Close | P(up next week) | 80% range | Volatility regime |",
        "|---|---:|---:|---|---|",
    ]
    for o in outlooks:
        summary.append(
            f"| {o.asset.name} | {o.fmt(o.close)} | {_pct(o.p_up, 0)} "
            f"| {o.fmt(o.low_80)} – {o.fmt(o.high_80)} | {o.vol_regime} |"
        )
    summary.append("")

    sections = [asset_section(o) for o in outlooks]

    footer = [
        "## Track record (walk-forward, out of sample)",
        "",
        track_record_table(outlooks),
        "",
        "## How to read this",
        "",
        "- **P(up)** comes from a logistic regression on weekly momentum, volatility, RSI, "
        "trend and (for FX) the interest-rate differential. Values near 50% mean the model "
        "sees no edge — which is the normal state of affairs in FX.",
        "- **The 80% range** is centred on today's close (random walk) and sized by the "
        "volatility forecast. It is a risk measure, not a price target.",
        "- **Validation:** every number in the track record comes from forecasts made with "
        "only past data (expanding window, refitted every 4 weeks).",
        "",
        "*Educational project — not investment advice.*",
        "",
    ]
    return "\n".join(header + summary + sections + footer)


def write_report(outlooks: List[AssetOutlook], out_dir: Path = REPORT_DIR) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    md = render_markdown(outlooks)
    as_of = max(o.as_of for o in outlooks)
    path = out_dir / f"{as_of:%Y-%m-%d}.md"
    path.write_text(md, encoding="utf-8")
    (out_dir / "latest.md").write_text(md, encoding="utf-8")
    return path
