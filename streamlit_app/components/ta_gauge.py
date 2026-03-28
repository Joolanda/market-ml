import streamlit as st

def ta_gauge(title: str, label: str, score: float):
    pct = max(0, min(1, score)) * 100

    html = f"""
    <div class="gauge">
      <div class="gauge-title">{title}</div>

      <div class="gauge-bar">
        <div class="gauge-pointer" style="left:{pct:.0f}%;"></div>
      </div>

      <div class="gauge-pill">
        {label}
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
