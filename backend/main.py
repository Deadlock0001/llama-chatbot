from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class ChatRequest(BaseModel):
    messages: list

@app.post("/chat")
def chat(req: ChatRequest):
    response = requests.post(
        "http://ollama:11434/api/chat",
        json={
            "model": "llama3.1",
            "messages": req.messages,
            "stream": False
        }
    )

    return {"reply": response.json()["message"]["content"]}
