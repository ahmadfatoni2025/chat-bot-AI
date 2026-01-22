from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from fastapi.responses import FileResponse


app = FastAPI()

class ChatRequest(BaseModel):
    message: str

OPENROUTER_API_KEY = os.getenv("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")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "google/gemma-2-9b-it"

@app.get("/")
def serve_html():
    return FileResponse("index.html")

@app.post("/chat")
def chat(req: ChatRequest):
    if not OPENROUTER_API_KEY:
        return {"reply": "API key OpenRouter tidak ditemukan"}

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Chat Bot"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "Jawab singkat dalam Bahasa Indonesia."},
            {"role": "user", "content": req.message}
        ]
    }

    try:
        res = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        res.raise_for_status()
        data = res.json()

        print("RAW RESPONSE:", data)  # DEBUG

        return {
            "reply": data["choices"][0]["message"]["content"]
        }

    except Exception as e:
        return {
            "reply": f"Terjadi error: {str(e)}"
        }
