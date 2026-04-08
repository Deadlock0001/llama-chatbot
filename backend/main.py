import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from openai import OpenAI

app = FastAPI()

# 🔥 Single Source of Truth
MODEL_CONFIG = {
    "gpt-oss": {
        "base_url": "http://172.31.21.186:8004/v1",
        "model_name": "openai/gpt-oss-20b",
    },
    "llama": {
        "base_url": "http://172.31.21.186:8000/v1",
        "model_name": "./meta-llama/Llama-3.1-8B-Instruct-awq",
    },
    "deepseek": {
        "base_url": "http://172.31.21.186:8002/v1",
        "model_name": "./DeepSeek-Coder-V2-Lite-Instruct-awq",
    },
    
}

class ChatRequest(BaseModel):
    model: str
    messages: List[Dict]

@app.get("/")
def root():
    return {"message": "✅ vLLM Backend Running"}


# 🔥 Endpoint to fetch available models dynamically
@app.get("/models")
def get_models():
    return {"models": list(MODEL_CONFIG.keys())}


# 🔥 Final dynamic routing
@app.post("/vllmchat")
def vllm_chat(req: ChatRequest):
    try:
        config = MODEL_CONFIG.get(req.model)

        if not config:
            return {"reply": f"Invalid model selected: {req.model}"}

        client = OpenAI(
            base_url=config["base_url"],
            api_key="token-abc123",
        )

        completion = client.chat.completions.create(
            model=config["model_name"],
            messages=req.messages,
            temperature=0.7,
            max_tokens=2048,
        )

        reply = completion.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        print("❌ LLM ERROR:", str(e))
        return {"reply": f"LLM Error: {str(e)}"}
