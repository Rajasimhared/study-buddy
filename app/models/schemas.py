"""Pydantic request/response schemas."""
from typing import Optional, List
from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Request model for conversational chat endpoint."""
    message: str
    session_id: Optional[str] = None  # If not provided, a new session will be created
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False  # Enable streaming responses (ChatGPT-like)


class PromptRequest(BaseModel):
    """Request model for one-off text generation (without conversation context)."""
    prompt: str
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    session_id: str
    message: str
    conversation_length: int


class GenerateResponse(BaseModel):
    """Response model for generate endpoint."""
    model: str
    response: str


class Message(BaseModel):
    """Message model for conversation history."""
    role: str
    message: str
    created_at: str


class ConversationResponse(BaseModel):
    """Response model for conversation history."""
    session_id: str
    messages: List[Message]
    message_count: int


class ConversationsListResponse(BaseModel):
    """Response model for listing all conversations."""
    sessions: List[str]
    count: int

