
import streamlit as st
import requests

st.set_page_config(
    page_title="Sentiment Analyzer",
    page_icon="💬"
)

st.title("💬 AI Sentiment Analyzer")
st.write("Enter text below to analyze its sentiment using Mistral AI.")

text = st.text_area(
    "Enter your text:",
    placeholder="I love learning new things!",
    height=150
)

if st.button("Analyze Sentiment"):
    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        try:
            with st.spinner("Analyzing sentiment..."):
                response = requests.post(
                    "http://127.0.0.1:8000/analyze/",
                    data={"text": text},
                    timeout=130
                )
                response.raise_for_status()
                result = response.json()["sentiment"]

            st.subheader("Result")
            st.success(result)

        except requests.exceptions.RequestException:
            st.error(
                "Could not reach the backend. "
                "Make sure the backend server is running."
            )
