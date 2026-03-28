import streamlit as st
from pathlib import Path

from streamlit_app.pages import overview, predictions, historical, scenarios, technical_analysis
from streamlit_app.data.loaders import get_live_price


def load_css(file_path: str):
    css_path = Path(file_path)
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.set_page_config(
    page_title="Market ML Dashboard",
    page_icon="📈",
    layout="wide"
)

load_css("streamlit_app/assets/style.css")

PAGES = {
    "📊 Overview": overview,
    "🤖 Predictions": predictions,
    "📈 Technical Analysis": technical_analysis,
    "📜 Historical Analysis": historical,
    "🧠 Scenario AI": scenarios,
}


def main():
    with st.sidebar:
        st.markdown('<div class="sidebar-title">Navigation</div>', unsafe_allow_html=True)

        def nav_item(label):
            active = st.session_state.get("page", "📊 Overview") == label
            css_class = "sidebar-item-active" if active else "sidebar-item"

            # Render the styled button
            if st.button(label, key=label):
                st.session_state["page"] = label

            # Apply custom CSS class
            st.markdown(
                f"""
                <style>
                div[data-testid="stButton"] button[key="{label}"] {{
                    all: unset;
                    display: block;
                    width: 100%;
                    padding: 0.6rem 1rem;
                    margin: 0.2rem 0;
                    border-radius: 6px;
                    font-size: 1rem;
                    cursor: pointer;
                    background: {"#2563eb" if active else "transparent"};
                    color: {"white" if active else "#d1d5db"};
                    transition: background 0.2s ease;
                }}
                div[data-testid="stButton"] button[key="{label}"]:hover {{
                    background: {"#1f2937" if not active else "#2563eb"};
                }}
                </style>
                """,
                unsafe_allow_html=True,
            )

        for label in PAGES.keys():
            nav_item(label)

    # Determine active page
    active_page = st.session_state.get("page", "📊 Overview")
    page = PAGES[active_page]

    current_price, price_change_24h = get_live_price("BTC")
    page.render(current_price, price_change_24h)


    # Determine active page
    active_page = st.session_state.get("page", "📊 Overview")
    page = PAGES[active_page]

    # Load live data once per page render
    current_price, price_change_24h = get_live_price("BTC")

    # Render selected page
    page.render(current_price, price_change_24h)


if __name__ == "__main__":
    main()
