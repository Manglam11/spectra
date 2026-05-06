import time
import streamlit as st
import pandas as pd

from src.viz_engine import VisualizationEngine


def render_visuals(df: pd.DataFrame) -> None:
    """
    Renders the visualization UI for the uploaded DataFrame.
    Lets user select chart type and relevant columns, then plots on demand.

    Args:
        df (pd.DataFrame): The DataFrame to visualise.
    """
    st.markdown('<p class="section-label">📈 Step 03 — Visualise</p>', unsafe_allow_html=True)

    viz_engine = VisualizationEngine(df)
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()

    available_plots = [
        "Histogram",
        "Bar Plot",
        "Scatter Plot",
        "Violin Plot",
        "Correlation Heatmap"
    ]

    col_select, col_plot = st.columns([2, 1], vertical_alignment="bottom")

    with col_select:
        chart_type = st.selectbox("Select chart type", options=available_plots)

    # ── Column selectors ───────────────────────────────────────────────────────
    if chart_type == "Histogram":
        col = st.selectbox("Numeric column", options=numeric_cols)

    elif chart_type == "Bar Plot":
        col = st.selectbox("Categorical column", options=categorical_cols)

    elif chart_type == "Scatter Plot":
        c1, c2 = st.columns(2)
        with c1:
            col1 = st.selectbox("X — Numeric column", options=numeric_cols)
        with c2:
            col2 = st.selectbox("Y — Numeric column", options=numeric_cols)

    elif chart_type == "Violin Plot":
        c1, c2 = st.columns(2)
        with c1:
            col1 = st.selectbox("Categorical column", options=categorical_cols)
        with c2:
            col2 = st.selectbox("Numeric column", options=numeric_cols)

    elif chart_type == "Correlation Heatmap":
        st.caption(f"Will use all {len(numeric_cols)} numeric column(s) — no selection needed.")

    # ── Generate button ────────────────────────────────────────────────────────
    with col_plot:
        generate = st.button("⚡ Generate Plot", use_container_width=True)

    if generate:
        with st.spinner("🎨  Rendering plot..."):
            time.sleep(1)

            if chart_type == "Histogram":
                fig = viz_engine.plot_histogram(col)
            elif chart_type == "Bar Plot":
                fig = viz_engine.plot_bar(col)
            elif chart_type == "Scatter Plot":
                fig = viz_engine.plot_scatter(col1, col2)
            elif chart_type == "Violin Plot":
                fig = viz_engine.plot_violin(col1, col2)
            elif chart_type == "Correlation Heatmap":
                fig = viz_engine.plot_correlation_heatmap()

        st.pyplot(fig)