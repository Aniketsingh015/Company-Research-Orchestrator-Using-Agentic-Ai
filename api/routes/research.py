"""Research execution endpoints."""

from fastapi import APIRouter, HTTPException
from api.schemas.research import ResearchRequest, ResearchStatusResponse, ResearchListResponse
from api.services.research_service import research_service

router = APIRouter()


@router.post("/research/start", response_model=ResearchStatusResponse)
async def start_research(request: ResearchRequest):
    """Start company research."""
    result = await research_service.start_research(
        company_name=request.company_name,
        llm_provider=request.llm_provider,
        async_mode=request.async_mode
    )
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error"))
    return result


@router.get("/research/status/{task_id}", response_model=ResearchStatusResponse)
async def get_research_status(task_id: str):
    """Get status of a research task."""
    result = research_service.get_task_status(task_id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail="Task not found")
    return result


@router.get("/research/tasks", response_model=ResearchListResponse)
async def list_research_tasks():
    """List all research tasks."""
    return research_service.list_all_tasks()
