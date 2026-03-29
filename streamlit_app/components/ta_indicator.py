# streamlit_app/components/ta_indicator.py

import streamlit as st
from typing import List
from streamlit_app.logic.ta_logic import IndicatorResult


def ta_indicator_table(indicators: List[IndicatorResult]) -> None:
    st.markdown("### Key technical indicators")

    rows = []
    for ind in indicators:
        rows.append(
            {
                "Indicator": ind.name,
                "Status": ind.status,
                "Trend support": ind.trend_support,
            }
        )

    st.table(rows)
