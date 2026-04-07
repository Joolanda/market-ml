import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def placeholder_chart():
    st.line_chart(pd.DataFrame({"value": [1, 2, 3, 2, 4]}))

def render_sparkline(df):
    """
    Render a clean sparkline chart using Plotly.
    Expects a DataFrame with a 'close' column.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["close"],
        mode="lines",
        line=dict(color="#4caf50", width=2),
        hoverinfo="skip"
    ))

    fig.update_layout(
        height=60,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )

    st.plotly_chart(fig, use_container_width=True)