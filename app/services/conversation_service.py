"""Conversation service for building prompts and handling streaming."""
from typing import Optional, Tuple, AsyncGenerator
import json
import logging
from app.database.models import get_conversation_history, save_message
from app.services.ollama_service import stream_ollama_api

logger = logging.getLogger(__name__)


def build_conversation_prompt(user_message: str, session_id: Optional[str] = None) -> Tuple[str, Optional[str]]:
    """
    Build a prompt with conversation history if session_id is provided.
    
    Args:
        user_message: The current user message
        session_id: Optional session ID to include conversation history
        
    Returns:
        Tuple of (formatted_prompt, session_id)
        If session_id is None, a new one is generated
    """
    if session_id:
        history = get_conversation_history(session_id)
        if history:
            context = "\n".join([
                f"{msg['role']}: {msg['message']}" 
                for msg in history
            ])
            return f"{context}\nuser: {user_message}\nassistant:", session_id
    
    # No session or no history - just use the current message
    return f"user: {user_message}\nassistant:", session_id


async def stream_chat_response(session_id: str, prompt: str, temperature: float) -> AsyncGenerator[str, None]:
    """
    Stream chat response and save to database after completion.
    
    Yields tokens in SSE format: "data: {token}\n\n"
    """
    full_response = ""
    
    try:
        # Send session_id first as metadata
        yield f"data: {json.dumps({'type': 'session_id', 'session_id': session_id})}\n\n"
        
        # Stream tokens from Ollama
        async for token in stream_ollama_api(prompt, temperature):
            full_response += token
            # Send token in SSE format
            yield f"data: {json.dumps({'type': 'token', 'token': token})}\n\n"
        
        # Send completion signal
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
        
        # Save complete response to database
        save_message(session_id, "assistant", full_response)
        
        # Get updated history count
        history = get_conversation_history(session_id)
        
        # Send final metadata
        yield f"data: {json.dumps({'type': 'metadata', 'conversation_length': len(history)})}\n\n"
        
        logger.info(f"Streaming complete - Session: {session_id}, Length: {len(history)} messages, Response length: {len(full_response)} chars")
        
    except Exception as e:
        logger.error(f"Error during streaming - Session: {session_id}, Error: {str(e)}")
        yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"

