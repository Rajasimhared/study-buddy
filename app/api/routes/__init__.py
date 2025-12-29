"""API route handlers."""
from fastapi import APIRouter
from app.api.routes import chat, conversations, health

# Create main router
api_router = APIRouter()

# Include all route modules with proper prefixes
api_router.include_router(health.router, tags=["health"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])

