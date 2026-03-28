import streamlit as st

def live_price_header(symbol: str, price: float, change_pct: float):
    color = "green" if change_pct >= 0 else "red"
    arrow = "▲" if change_pct >= 0 else "▼"

    st.markdown(
        f"""
        <div class="live-header">
            <div class="live-header-left">
                <span class="live-symbol">{symbol}</span>
                <span class="live-price">${price:,.2f}</span>
            </div>
            <div class="live-header-right">
                <span class="live-change" style="color:{color};">
                    {arrow} {change_pct:.2f}%
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
