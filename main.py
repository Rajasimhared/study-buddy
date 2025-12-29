from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
def read_root():
    return { "status": "ok" }

@app.post("/chat")
async def chat(request: ChatRequest):
    return { "message": "AI received your message: " + request.message }