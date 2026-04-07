import os
import sys
import streamlit as st
from pathlib import Path

# ---------------------------------------------------------
# Ensure src/ is on the Python path
# ---------------------------------------------------------
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")

if SRC not in sys.path:
    sys.path.insert(0, SRC)

# ---------------------------------------------------------
# Import pages (new architecture)
# ---------------------------------------------------------
from streamlit_app.pages import (
    overview,
    predictions,
    historical,
    scenarios,
)

# ---------------------------------------------------------
# Import live price function (new architecture)
# ---------------------------------------------------------
from src.data.live_data import fetch_live_price


# ---------------------------------------------------------
# CSS loader
# ---------------------------------------------------------
def load_css(file_path: str):
    css_path = Path(file_path)
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ---------------------------------------------------------
# Streamlit config
# ---------------------------------------------------------
st.set_page_config(
    page_title="Market ML Dashboard",
    page_icon="📈",
    layout="wide"
)

load_css("streamlit_app/assets/style.css")


# ---------------------------------------------------------
# Page registry
# ---------------------------------------------------------
PAGES = {
    "📊 Overview": overview,
    "🤖 Predictions": predictions,
    "📜 Historical Analysis": historical,
    "🧠 Scenario AI": scenarios,
}


# ---------------------------------------------------------
# Main app
# ---------------------------------------------------------
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

    # Fetch live price once per render
    current_price = fetch_live_price("BTCUSDT")
    price_change_24h = None  # later toevoegen

    # Render selected page
    page.render()



if __name__ == "__main__":
    main()
