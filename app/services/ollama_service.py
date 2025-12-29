"""Ollama API service."""
from typing import AsyncGenerator
from fastapi import HTTPException
import json
import httpx
from app.config import OLLAMA_URL, MODEL_NAME


async def call_ollama_api(prompt: str, temperature: float = 0.7) -> str:
    """
    Call Ollama API and return the response text (non-streaming).
    
    Args:
        prompt: The prompt to send to the model
        temperature: Temperature setting (default: 0.7)
        
    Returns:
        The AI response text
        
    Raises:
        HTTPException if the API call fails
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "temperature": temperature,
        "stream": False,
    }
    
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            
            lines = response.text.strip().splitlines()
            final_chunk = json.loads(lines[-1])
            return final_chunk.get("response", "").strip()
            
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Ollama API error: {str(e)}")


async def stream_ollama_api(prompt: str, temperature: float = 0.7) -> AsyncGenerator[str, None]:
    """
    Stream tokens from Ollama API one by one.
    
    Args:
        prompt: The prompt to send to the model
        temperature: Temperature setting (default: 0.7)
        
    Yields:
        Token strings as they arrive
        
    Raises:
        HTTPException if the API call fails
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "temperature": temperature,
        "stream": True,
    }
    
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", OLLAMA_URL, json=payload) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.strip():
                        try:
                            chunk = json.loads(line)
                            token = chunk.get("response", "")
                            if token:
                                yield token
                        except json.JSONDecodeError:
                            continue
                            
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Ollama API error: {str(e)}")

