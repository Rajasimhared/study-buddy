"""Database models and operations."""
from typing import List, Optional, Dict
from app.database.db import get_db_connection


def save_message(session_id: str, role: str, message: str) -> int:
    """
    Save a message to the database.
    
    Args:
        session_id: Unique identifier for the conversation session
        role: Either 'user' or 'assistant'
        message: The message content
        
    Returns:
        The ID of the saved message
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO conversations (session_id, role, message)
            VALUES (?, ?, ?)
        """, (session_id, role, message))
        return cursor.lastrowid


def get_conversation_history(session_id: str, limit: Optional[int] = None) -> List[Dict]:
    """
    Retrieve conversation history for a session.
    
    Args:
        session_id: The session identifier
        limit: Optional limit on number of messages to retrieve
        
    Returns:
        List of message dictionaries with 'role' and 'message' keys
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT role, message, created_at
            FROM conversations
            WHERE session_id = ?
            ORDER BY created_at ASC
        """
        
        if limit:
            query += f" LIMIT {limit}"
            
        cursor.execute(query, (session_id,))
        rows = cursor.fetchall()
        
        return [
            {
                "role": row["role"],
                "message": row["message"],
                "created_at": row["created_at"]
            }
            for row in rows
        ]


def get_all_sessions() -> List[str]:
    """Get all unique session IDs."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT session_id FROM conversations")
        return [row["session_id"] for row in cursor.fetchall()]

