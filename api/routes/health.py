"""Health check endpoints."""

from fastapi import APIRouter
from datetime import datetime
from config.settings import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "llm_provider": settings.llm_provider,
        "model": settings.default_model,
        "supabase_connected": bool(settings.supabase_url)
    }


@router.get("/ping")
async def ping():
    """Simple ping endpoint."""
    return {"message": "pong"}
