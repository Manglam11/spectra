import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from components.uploader import render_uploader

st.set_page_config(
    page_title="Spectra | EDA Platform",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Global styles ────────────────────────────────────────────────────────────
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("## 🔬 Spectra")
st.caption("Automated Exploratory Data Analysis — upload a dataset and let Spectra do the rest.")
st.divider()

# ── Upload stage ─────────────────────────────────────────────────────────────
df = render_uploader()

if df is not None:
    st.session_state["df"] = df