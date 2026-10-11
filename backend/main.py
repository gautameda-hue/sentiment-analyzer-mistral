
from fastapi import FastAPI, Form, HTTPException
import requests

app = FastAPI(title="Sentiment Analyzer API")


@app.get("/")
def home():
    return {"message": "Sentiment Analyzer API is running"}


@app.post("/analyze/")
def analyze_sentiment(text: str = Form(...)):
    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter some text."
        )

    prompt = f"""
Classify the sentiment of the text below.

Choose exactly one label: Positive, Negative, or Neutral.
Return only the label.

Text:
{text}

Sentiment:
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        result = response.json()["response"].strip()

        return {"sentiment": result}

    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to Ollama. Make sure Ollama is running."
        )
