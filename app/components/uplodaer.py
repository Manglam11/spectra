import streamlit as st
import pandas as pd
from src.data_loader import DataLoader



def render_uploader() -> pd.DataFrame | None:
    """
    Shows the Streamlit UI for user to upload his file.
    Uploaded file is being rendered in main.py to be used further.

    Returns:

        pd.Dataframe: Loaded DataFrame if upload is valid.

        None: if not valid.
    """
    st.markdown("### 📂 Upload Your Dataset")
    st.caption("Supports CSV files only. Max size 200MB")

    uploaded_file = st.file_uploader(
        label="Drop your CSV file here",
        type="csv",
        help="Upload any CSV file to begin analysis"
    )
    if uploaded_file is None:
        return None

    data_loader = DataLoader(uploaded_file)
    with st.spinner("Analysing your dataset..."):
        df = data_loader.load()

    if df is None:
        st.error("❌ Failed to load file. Make sure it's a valid CSV.")
        return None
    st.success(f"✅ `{uploaded_file.name}` loaded — {df.shape[0]} rows × {df.shape[1]} columns")

    with st.expander("🔍 Basic Profile", expanded=True):
        basic_profile = data_loader.get_basic_profile()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rows", basic_profile["shape"][0])
            st.metric("Columns", basic_profile["shape"][1])
        with col2:
            st.dataframe(
                pd.DataFrame({
                    "Missing Count": basic_profile["null_counts"],
                    "Missing %": basic_profile["null_pct"]
                }),
                use_container_width=True
            )

    with st.expander("🧬 Column Types"):
        dtype_df = pd.DataFrame(
            data_loader.get_dtype_summary().items(),
            columns=["Column", "Dtype"]
        )
        st.dataframe(dtype_df, use_container_width=True)

    return data_loader.df

