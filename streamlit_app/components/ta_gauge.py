import streamlit as st

def ta_gauge(title: str, label: str, score: float):
    # Handle None gracefully
    if score is None:
        pct = 50
    else:
        pct = max(0, min(1, score)) * 100

    # Color logic
    if pct < 33:
        color = "#e53935"   # red
    elif pct < 66:
        color = "#ffb300"   # yellow
    else:
        color = "#4caf50"   # green

    # Build HTML
    html = f"""
    <div class="gauge">
      <div class="gauge-title">{title}</div>

      <div class="gauge-bar">
        <div class="gauge-pointer" style="left:{pct:.0f}%; background:{color};"></div>
      </div>

      <div class="gauge-pill">
        {label}
      </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)
