# Study Buddy API

AI-powered study assistant with conversation memory, built with FastAPI.

## Project Structure

```
study-buddy/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py             # Configuration settings
│   │
│   ├── api/                  # API routes
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py   # Router aggregation
│   │       ├── health.py     # Health check endpoint
│   │       ├── chat.py       # Chat endpoints
│   │       └── conversations.py  # Conversation history endpoints
│   │
│   ├── models/               # Pydantic schemas
│   │   ├── __init__.py
│   │   └── schemas.py        # Request/response models
│   │
│   ├── services/             # Business logic
│   │   ├── __init__.py
│   │   ├── ollama_service.py      # Ollama API integration
│   │   └── conversation_service.py # Conversation management
│   │
│   └── database/             # Database layer
│       ├── __init__.py
│       ├── db.py             # Database connection
│       └── models.py         # Database operations
│
├── main.py                   # Application entry point
├── init_db.py                # Database initialization script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Features

- ✅ **Conversation Memory**: Saves and retrieves conversation history
- ✅ **Streaming Responses**: ChatGPT-like token-by-token streaming
- ✅ **Session Management**: Track multiple conversation sessions
- ✅ **Database Persistence**: SQLite (easily switchable to Postgres)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize database:
```bash
python init_db.py
```

3. Run the server:
```bash
uvicorn main:app --reload
```

## API Endpoints

### Health Check
- `GET /health` - Check API status

### Chat
- `POST /chat` - Send a message (with optional streaming)
- `POST /chat/generate` - One-off text generation

### Conversations
- `GET /conversations` - List all conversation sessions
- `GET /conversations/{session_id}` - Get conversation history

## Usage Examples

### Start a conversation
```bash
POST /chat
{
  "message": "Hello, my name is Alice"
}
```

### Continue conversation (with streaming)
```bash
POST /chat
{
  "message": "What's my name?",
  "session_id": "abc-123",
  "stream": true
}
```

### Get conversation history
```bash
GET /conversations/abc-123
```

## Configuration

Environment variables:
- `OLLAMA_URL` - Ollama API URL (default: http://localhost:11434/api/generate)
- `MODEL_NAME` - Model name (default: gemma3:27b)
- `DATABASE_URL` - Database connection string (default: sqlite:///conversations.db)
- `LOG_LEVEL` - Logging level (default: INFO)

## Architecture

The project follows a clean architecture pattern:

- **API Layer** (`app/api/`): HTTP endpoints and request handling
- **Service Layer** (`app/services/`): Business logic and external API calls
- **Database Layer** (`app/database/`): Data persistence and queries
- **Models** (`app/models/`): Pydantic schemas for validation

This structure makes the codebase:
- **Maintainable**: Clear separation of concerns
- **Scalable**: Easy to add new features
- **Testable**: Each layer can be tested independently

