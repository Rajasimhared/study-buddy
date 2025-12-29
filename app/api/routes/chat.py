"""Chat endpoints."""
import uuid
import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.models.schemas import ChatRequest, ChatResponse, PromptRequest, GenerateResponse
from app.services.ollama_service import call_ollama_api
from app.services.conversation_service import build_conversation_prompt, stream_chat_response
from app.database.models import save_message, get_conversation_history
from app.config import MODEL_NAME

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("")
async def chat(request: ChatRequest):
    """
    Main conversational endpoint - always saves messages and maintains conversation context.
    
    Usage flow:
    1. First call: POST /chat with {"message": "Hello"} -> returns session_id
    2. Continue: POST /chat with {"message": "How are you?", "session_id": "..."}
    3. Retrieve history: GET /conversations/{session_id}
    
    Streaming mode:
    - Set "stream": true to get tokens one by one (ChatGPT-like experience)
    - Response will be Server-Sent Events (SSE) format
    - Full message is still saved to database after streaming completes
    
    This endpoint:
    - Always creates/uses a session_id (generates new one if not provided)
    - Always saves user messages and AI replies to the database
    - Always includes conversation history in the prompt (so AI remembers context)
    
    Returns:
    - If stream=false: ChatResponse (JSON)
    - If stream=true: StreamingResponse (text/event-stream)
    """
    # Generate or use provided session_id
    session_id = request.session_id or str(uuid.uuid4())
    
    logger.info(f"Chat request - Session: {session_id}, Message: {request.message[:50]}..., Stream: {request.stream}")
    
    # Save user message first
    save_message(session_id, "user", request.message)
    
    # Build prompt with conversation history (will include all previous messages)
    full_prompt, _ = build_conversation_prompt(request.message, session_id)
    
    # Handle streaming vs non-streaming
    if request.stream:
        return StreamingResponse(
            stream_chat_response(session_id, full_prompt, request.temperature),
            media_type="text/event-stream"
        )
    else:
        # Non-streaming mode
        ai_response = await call_ollama_api(full_prompt, temperature=request.temperature)
        
        logger.info(f"AI Response - Session: {session_id}, Response: {ai_response[:100]}...")
        
        # Save AI response
        save_message(session_id, "assistant", ai_response)
        
        # Get updated history count
        history = get_conversation_history(session_id)
        
        response = ChatResponse(
            session_id=session_id,
            message=ai_response,
            conversation_length=len(history)
        )
        
        logger.info(f"Chat response - Session: {session_id}, Length: {len(history)} messages")
        
        return response


@router.post("/generate", response_model=GenerateResponse)
async def generate_text(request: PromptRequest):
    """
    One-off text generation endpoint - for standalone prompts without conversation context.
    
    Use this endpoint when you want:
    - A single generation without saving to database
    - Custom temperature/stream settings
    - No conversation history included
    
    Note: For conversational AI that remembers context, use /chat instead.
    """
    logger.info(f"Generate request - Prompt: {request.prompt[:50]}..., Temperature: {request.temperature}")
    
    # Just use the prompt as-is (no conversation history)
    ai_response = await call_ollama_api(
        request.prompt, 
        temperature=request.temperature
    )
    
    logger.info(f"Generate response - Response: {ai_response[:100]}...")
    
    return GenerateResponse(
        model=MODEL_NAME,
        response=ai_response
    )

