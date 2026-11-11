"""
Asset registry: one place that defines which markets the project covers.

Adding a market = adding one entry here. Everything else (data download,
features, models, weekly report, Streamlit selector) reads from this list.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class Asset:
    key: str                 # file-safe id, e.g. "eurusd"
    name: str                # display name, e.g. "EUR/USD"
    yf_ticker: str           # Yahoo Finance ticker used for daily data
    kind: str                # "fx" or "crypto"
    decimals: int            # how many decimals to show for prices
    base_ccy: Optional[str] = None   # FX only: currency whose rate is "base"
    quote_ccy: Optional[str] = None  # FX only: currency whose rate is "quote"
    binance_symbol: Optional[str] = None  # crypto only: live price source
    note: str = ""           # one line of context shown in the weekly report


ASSETS: Dict[str, Asset] = {
    "eurusd": Asset(
        key="eurusd", name="EUR/USD", yf_ticker="EURUSD=X", kind="fx", decimals=4,
        base_ccy="EUR", quote_ccy="USD",
        note="The most traded currency pair; driven by ECB vs. Fed policy.",
    ),
    "eurchf": Asset(
        key="eurchf", name="EUR/CHF", yf_ticker="EURCHF=X", kind="fx", decimals=4,
        base_ccy="EUR", quote_ccy="CHF",
        note="Safe-haven barometer for the DACH region; SNB policy matters.",
    ),
    "eurpln": Asset(
        key="eurpln", name="EUR/PLN", yf_ticker="EURPLN=X", kind="fx", decimals=4,
        base_ccy="EUR", quote_ccy="PLN",
        note="Largest CEE currency; relevant for banks active in Central & Eastern Europe.",
    ),
    "btcusd": Asset(
        key="btcusd", name="BTC/USD", yf_ticker="BTC-USD", kind="crypto", decimals=0,
        binance_symbol="BTCUSDT",
        note="Since Oct 2026 Sparkassen offer crypto trading in their app; RBI is rolling out "
             "crypto via Bitpanda across its CEE network banks.",
    ),
}

# Monthly 3-month interbank rates (OECD, via FRED – no API key needed).
# Used to build the interest-rate differential for FX pairs.
RATE_SERIES: Dict[str, str] = {
    "EUR": "IR3TIB01EZM156N",
    "USD": "IR3TIB01USM156N",
    "CHF": "IR3TIB01CHM156N",
    "PLN": "IR3TIB01PLM156N",
}

DEFAULT_ASSET = "eurusd"


def get_asset(key: str) -> Asset:
    key = key.lower()
    if key not in ASSETS:
        raise KeyError(f"Unknown asset '{key}'. Known: {', '.join(ASSETS)}")
    return ASSETS[key]
