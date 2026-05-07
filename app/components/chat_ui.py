import streamlit as st
import pandas as pd
from src.chat_engine import ChatEngine

def render_chat(numeric_summary: pd.DataFrame, categorical_summary: pd.DataFrame) -> None:
    """
    Renders the Chat UI to interact with EDA summary in natural language.

    Args:
        numeric_summary: Numerical data info we got to know.
        categorical_summary: Categorical data info we got to know.
    """
    st.markdown('<p class="section-label">💬 Step 04 — Chat with your Data</p>', unsafe_allow_html=True)

    if "chat_engine" not in st.session_state:
        st.session_state["chat_engine"] = ChatEngine(numeric_summary, categorical_summary)

    for message in st.session_state["chat_engine"].messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Ask anything about your dataset...")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            response = st.session_state["chat_engine"].chat(user_input)
            st.write(response)






