import sys
import os
import uuid
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from components.uploader import render_uploader
from components.eda_display import render_eda
from components.viz_display import render_visuals
from components.chat_ui import render_chat

st.set_page_config(
    page_title="Spectra | EDA Platform",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Session ID generation
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

# ── Global styles ─────────────────────────────────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

        :root {
            --accent:    #00D4AA;
            --accent-2:  #FFB347;
            --surface:   rgba(0, 212, 170, 0.06);
            --border:    rgba(0, 212, 170, 0.2);
        }

        #MainMenu, footer, header { visibility: hidden; }

        .block-container {
            padding-top: 2.5rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        /* ── Hero header ─────────────────────────────────────────────── */
        .spectra-hero {
            display: flex;
            align-items: baseline;
            gap: 1rem;
            margin-bottom: 0.25rem;
        }

        .spectra-wordmark {
            font-family: 'Space Mono', monospace;
            font-size: 2.6rem;
            font-weight: 700;
            background: linear-gradient(90deg, #00D4AA 0%, #00A8FF 60%, #FFB347 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -1px;
        }

        .spectra-badge {
            font-family: 'Space Mono', monospace;
            font-size: 0.65rem;
            color: var(--accent);
            border: 1px solid var(--border);
            padding: 2px 8px;
            border-radius: 3px;
            letter-spacing: 2px;
            text-transform: uppercase;
            vertical-align: middle;
        }

        .spectra-tagline {
            font-family: 'DM Sans', sans-serif;
            font-size: 0.95rem;
            color: #888;
            margin-bottom: 1.5rem;
            font-weight: 300;
        }

        /* ── Section headings ────────────────────────────────────────── */
        .section-label {
            font-family: 'Space Mono', monospace;
            font-size: 0.7rem;
            letter-spacing: 3px;
            color: var(--accent);
            text-transform: uppercase;
            margin-bottom: 0.75rem;
        }

        /* ── Metric cards ────────────────────────────────────────────── */
        [data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1rem 1.2rem;
        }

        [data-testid="stMetricLabel"] {
            font-family: 'Space Mono', monospace;
            font-size: 0.7rem;
            letter-spacing: 1px;
            color: #888 !important;
            text-transform: uppercase;
        }

        [data-testid="stMetricValue"] {
            font-family: 'Space Mono', monospace;
            color: var(--accent) !important;
            font-size: 1.8rem !important;
        }

        /* ── Expander ────────────────────────────────────────────────── */
        [data-testid="stExpander"] {
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            background: var(--surface) !important;
        }

        /* ── Divider ─────────────────────────────────────────────────── */
        hr {
            border-color: var(--border) !important;
            margin: 1.5rem 0 !important;
        }

        /* ── Dataframe ───────────────────────────────────────────────── */
        [data-testid="stDataFrame"] {
            border: 1px solid var(--border);
            border-radius: 6px;
        }

        /* ── Success / Error / Spinner text ──────────────────────────── */
        [data-testid="stSpinner"] p {
            font-family: 'Space Mono', monospace;
            font-size: 0.8rem;
            color: var(--accent);
        }
    </style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
    <div class="spectra-hero">
        <span class="spectra-wordmark">Spectra</span>
        <span class="spectra-badge">EDA v1.0</span>
    </div>
    <p class="spectra-tagline">Automated Exploratory Data Analysis — upload a dataset and let Spectra do the rest.</p>
""", unsafe_allow_html=True)

st.divider()

# ── Upload stage ───────────────────────────────────────────────────────────────
df = render_uploader()

if df is not None:
# ── EDA stage ─────────────────────────────────────────────────────────────────
    st.session_state["df"] = df
    st.divider()
    numeric_summary, categorical_summary = render_eda(df)

# ── Visualisation stage ────────────────────────────────────────────────────────
    st.divider()
    render_visuals(df)

# ── Chat stage ────────────────────────────────────────────────────────
    st.divider()
    render_chat(numeric_summary, categorical_summary)

