import streamlit as st
from pathlib import Path
import sys
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)


# Import pages
from streamlit_app.pages import (
    overview,
    predictions,
    historical,
    scenarios,
    technical_analysis
)

# Import the REAL get_live_price from your data module
from streamlit_app.data.live_features import get_live_price


def load_css(file_path: str):
    css_path = Path(file_path)
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Streamlit page config
st.set_page_config(
    page_title="Market ML Dashboard",
    page_icon="📈",
    layout="wide"
)

# Load custom CSS
load_css("streamlit_app/assets/style.css")


# Page registry
PAGES = {
    "📊 Overview": overview,
    "🤖 Predictions": predictions,
    "📈 Technical Analysis": technical_analysis,
    "📜 Historical Analysis": historical,
    "🧠 Scenario AI": scenarios,
}


def main():
    # Sidebar navigation
    with st.sidebar:
        st.markdown('<div class="sidebar-title">Navigation</div>', unsafe_allow_html=True)

        selected_page = st.radio(
            "Navigation",
            list(PAGES.keys()),
            index=list(PAGES.keys()).index(st.session_state.get("page", "📊 Overview")),
            key="nav_selector"
        )

        st.session_state["page"] = selected_page

    # Determine active page
    active_page = st.session_state.get("page", "📊 Overview")
    page = PAGES[active_page]

    # Load live data once per page render
    # This now ALWAYS returns floats (never None)
    current_price, price_change_24h = get_live_price("BTCUSDT")

    # Render selected page
    page.render(current_price, price_change_24h)


if __name__ == "__main__":
    main()
