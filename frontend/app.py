
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Sentiment Analyzer",
    page_icon="💬"
)

st.title("💬 AI Sentiment Analyzer")
st.write(
    "Analyze text sentiment using a hosted AI model."
)

text = st.text_area(
    "Enter your text:",
    placeholder="I love learning new things!",
    height=150
)

if st.button("Analyze Sentiment"):
    if not text.strip():
        st.warning("Please enter some text first.")

    elif "GROQ_API_KEY" not in st.secrets:
        st.error(
            "API key missing. Add GROQ_API_KEY "
            "in your Streamlit Cloud Secrets settings."
        )

    else:
        try:
            client = Groq(
                api_key=st.secrets["GROQ_API_KEY"]
            )

            with st.spinner("Analyzing sentiment..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Classify the user's text as "
                                "Positive, Negative, or Neutral. "
                                "Return exactly one of those labels."
                            )
                        },
                        {
                            "role": "user",
                            "content": text
                        }
                    ],
                    temperature=0
                )

            result = (
                response.choices[0].message.content.strip()
            )

            if result not in ["Positive", "Negative", "Neutral"]:
                st.error("The model returned an unexpected result.")
            else:
                st.subheader("Result")
                st.success(result)

        except Exception as e:
            st.error(f"Analysis failed: {e}")
            
