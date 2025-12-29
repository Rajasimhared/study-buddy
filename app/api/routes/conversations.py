"""Conversation history endpoints."""
import logging
from fastapi import APIRouter

from app.models.schemas import ConversationResponse, ConversationsListResponse, Message
from app.database.models import get_conversation_history, get_all_sessions

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{session_id}", response_model=ConversationResponse)
async def get_conversation(session_id: str):
    """Retrieve conversation history for a session."""
    logger.info(f"Retrieving conversation history for session: {session_id}")
    history = get_conversation_history(session_id)
    
    messages = [
        Message(
            role=msg["role"],
            message=msg["message"],
            created_at=msg["created_at"]
        )
        for msg in history
    ]
    
    logger.info(f"Found {len(messages)} messages for session: {session_id}")
    
    return ConversationResponse(
        session_id=session_id,
        messages=messages,
        message_count=len(messages)
    )


@router.get("", response_model=ConversationsListResponse)
async def list_conversations():
    """List all conversation sessions."""
    sessions = get_all_sessions()
    logger.info(f"Listing all conversations - Found {len(sessions)} sessions")
    return ConversationsListResponse(
        sessions=sessions,
        count=len(sessions)
    )

