import time
import streamlit as st
import pandas as pd
from src.eda_engine import EDAEngine


def render_eda(df: pd.DataFrame) -> None:
    """
    Renders the EDA summary UI for the uploaded DataFrame.
    Displays numeric and categorical statistical summaries.

    Args:
        df (pd.DataFrame): The DataFrame to analyse.
    """
    st.markdown('<p class="section-label">📊 Step 02 — Statistical Profile</p>', unsafe_allow_html=True)

    eda_engine = EDAEngine(df)

    with st.spinner("🧮  Running statistical engine — computing distributions, skewness, kurtosis..."):
        time.sleep(2)
        numeric_summary = eda_engine.get_numeric_summary()
        categorical_summary = eda_engine.get_categorical_summary()

    # ── Numeric summary ────────────────────────────────────────────────────────
    with st.expander("📐 Numeric Summary", expanded=True):
        if numeric_summary.empty:
            st.caption("No numeric columns found in this dataset.")
        else:
            st.caption(f"{len(numeric_summary)} numeric column(s) detected")
            st.dataframe(
                numeric_summary.style.format(precision=4),
                use_container_width=True
            )

    # ── Categorical summary ────────────────────────────────────────────────────
    with st.expander("🏷️ Categorical Summary", expanded=True):
        if categorical_summary.empty:
            st.caption("No categorical columns found in this dataset.")
        else:
            st.caption(f"{len(categorical_summary)} categorical column(s) detected")
            st.dataframe(
                categorical_summary,
                use_container_width=True
            )