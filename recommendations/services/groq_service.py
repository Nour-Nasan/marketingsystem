import os
import requests

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_groq(prompt: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing. Add it to .env")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 300,
    }

    response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)

    if response.status_code != 200:
        raise RuntimeError(response.text)

    data = response.json()
    return data["choices"][0]["message"]["content"]
