import streamlit as st
import pandas as pd
from src.data_loader import DataLoader


def render_uploader() -> pd.DataFrame | None:
    """
    Renders the Streamlit upload UI.
    Validates and loads the CSV via DataLoader, then shows basic profile.

    Returns:
        pd.DataFrame: Loaded DataFrame if upload is valid.
        None: If no file uploaded or file is invalid.
    """
    st.markdown('<p class="section-label">⬆ Step 01 — Load Dataset</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        label="Drop your CSV file here",
        type="csv",
        help="Upload any CSV file to begin analysis. Max 200 MB."
    )

    if uploaded_file is None:
        return None

    data_loader = DataLoader(uploaded_file)

    with st.spinner("⚙  Reading file and profiling columns..."):
        import time
        time.sleep(2)
        df = data_loader.load()

    if df is None:
        st.error("❌ Failed to load file. Make sure it's a valid, non-empty CSV.")
        return None

    st.success(f"✅ **{uploaded_file.name}** loaded — {df.shape[0]:,} rows × {df.shape[1]} columns")

    # ── Basic profile ──────────────────────────────────────────────────────────
    with st.expander("🔍 Basic Profile", expanded=True):
        basic_profile = data_loader.get_basic_profile()

        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            st.metric("Rows", f"{basic_profile['shape'][0]:,}")
        with col2:
            st.metric("Columns", basic_profile["shape"][1])
        with col3:
            missing_df = pd.DataFrame({
                "Missing Count": basic_profile["null_counts"],
                "Missing %": basic_profile["null_pct"]
            })
            st.dataframe(missing_df, use_container_width=True)

    # ── Column types ───────────────────────────────────────────────────────────
    with st.expander("🧬 Column Types"):
        dtype_df = pd.DataFrame(
            data_loader.get_dtype_summary().items(),
            columns=["Column", "Dtype"]
        )
        st.dataframe(dtype_df, use_container_width=True)

    return data_loader.df