from typing import Union
from typing import Optional
from fastapi import FastAPI, HTTPException
import json

from pydantic import BaseModel
import httpx

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:27b"

class ChatRequest(BaseModel):
    message: str

class PromptRequest(BaseModel):
    prompt: str
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False

@app.get("/health")
def read_root():
    return { "status": "ok" }

@app.post("/chat")
async def chat(request: ChatRequest):
    return { "message": "AI received your message: " + request.message }

@app.post("/generate")
async def generate_text(request: PromptRequest):
    payload = {
        "model": MODEL_NAME,
        "prompt": request.prompt,
        "temperature": request.temperature,
        "stream": request.stream,
    }

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()

            lines = response.text.strip().splitlines()
            final_chunk = json.loads(lines[-1])

            return {
                "model": MODEL_NAME,
                "response": final_chunk.get("response", "").strip(),
            }

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=str(e))