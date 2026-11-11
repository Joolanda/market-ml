"""
Live price helpers for the Streamlit header and sparkline.

Tries the public Binance REST API first (no key needed). When that is not
reachable (offline, firewall, CI), it falls back to the latest daily data
from src/data/data_loader.py, so the app always renders.
"""

from __future__ import annotations

import logging
from typing import Tuple

import pandas as pd
import requests
import streamlit as st

from src.config.assets import ASSETS
from src.data.data_loader import load_daily

log = logging.getLogger("market_ml.live")

BINANCE_KLINES = "https://api.binance.com/api/v3/klines"
BINANCE_TICKER = "https://api.binance.com/api/v3/ticker/24hr"
TIMEOUT = 3


def _asset_for_symbol(symbol: str) -> str:
    symbol = symbol.upper()
    for key, asset in ASSETS.items():
        if asset.binance_symbol == symbol or asset.key.upper() == symbol:
            return key
    return "btcusd"


@st.cache_data(ttl=60, show_spinner=False)
def get_live_price(symbol: str = "BTCUSDT") -> Tuple[float, float]:
    """Return (last price, 24h change in %). Always floats, never None."""
    try:
        r = requests.get(BINANCE_TICKER, params={"symbol": symbol}, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        return float(data["lastPrice"]), float(data["priceChangePercent"])
    except Exception as exc:
        log.info("Live price unavailable (%s); using latest daily close", exc)
    daily = load_daily(_asset_for_symbol(symbol)).df
    last, prev = daily["close"].iloc[-1], daily["close"].iloc[-2]
    return float(last), float((last / prev - 1) * 100)


@st.cache_data(ttl=60, show_spinner=False)
def fetch_live_candles(symbol: str = "BTCUSDT", interval: str = "1m", limit: int = 50) -> pd.DataFrame:
    """Recent candles with columns open_time, open, high, low, close, volume."""
    try:
        r = requests.get(BINANCE_KLINES, params={"symbol": symbol, "interval": interval, "limit": limit},
                         timeout=TIMEOUT)
        r.raise_for_status()
        rows = r.json()
        df = pd.DataFrame(rows).iloc[:, :6]
        df.columns = ["open_time", "open", "high", "low", "close", "volume"]
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
        return df
    except Exception as exc:
        log.info("Live candles unavailable (%s); using daily data", exc)
    daily = load_daily(_asset_for_symbol(symbol)).df.tail(limit)
    return daily.reset_index().rename(columns={"date": "open_time"})


def render_sparkline(df: pd.DataFrame) -> None:
    if df is None or df.empty:
        st.info("No price data available.")
        return
    st.line_chart(df.set_index("open_time")["close"], height=140)
