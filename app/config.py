"""Application configuration."""
import os

# Ollama Configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "gemma3:27b")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///conversations.db")

# For SQLite, extract the file path
if DATABASE_URL.startswith("sqlite:///"):
    DATABASE_FILE = DATABASE_URL.replace("sqlite:///", "")
else:
    DATABASE_FILE = "conversations.db"

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

