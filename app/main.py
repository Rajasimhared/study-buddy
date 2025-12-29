"""FastAPI application entry point."""
import logging
from fastapi import FastAPI
from app.config import LOG_LEVEL
from app.database import init_database
from app.api.routes import api_router

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create FastAPI app
app = FastAPI(
    title="Study Buddy API",
    description="AI-powered study assistant with conversation memory",
    version="1.0.0"
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_database()

# Include API routes
app.include_router(api_router)

