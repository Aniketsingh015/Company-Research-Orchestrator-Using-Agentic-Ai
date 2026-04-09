"""Pydantic schemas for Research API endpoints."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class ResearchRequest(BaseModel):
    """Request schema for starting research."""
    company_name: str = Field(..., description="Company name to research")
    llm_provider: Optional[str] = Field("groq", description="LLM provider (groq/openrouter)")
    async_mode: Optional[bool] = Field(True, description="Run asynchronously in background")


class ResearchStatusResponse(BaseModel):
    """Response schema for research status."""
    success: bool
    task_id: Optional[str] = None
    status: str
    company_name: str
    message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    processing_time: Optional[float] = None


class ResearchResultResponse(BaseModel):
    """Response schema for completed research."""
    success: bool
    company_name: str
    status: str
    validation_passed: bool
    regeneration_count: int
    supabase_pushed: bool
    excel_file_path: Optional[str] = None
    report_file_path: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    processing_time: float
    created_at: datetime


class ResearchListResponse(BaseModel):
    """Response schema for list of research tasks."""
    success: bool
    total: int
    tasks: List[Dict[str, Any]]
