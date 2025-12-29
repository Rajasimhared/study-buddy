"""Service layer."""
from app.services.ollama_service import call_ollama_api, stream_ollama_api
from app.services.conversation_service import build_conversation_prompt, stream_chat_response

__all__ = [
    "call_ollama_api",
    "stream_ollama_api",
    "build_conversation_prompt",
    "stream_chat_response",
]

