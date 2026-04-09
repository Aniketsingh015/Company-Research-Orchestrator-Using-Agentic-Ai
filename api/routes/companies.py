from fastapi import APIRouter, HTTPException
from api.services.company_service import company_service

router = APIRouter()


@router.get("/companies/{company_name}")
async def get_company(company_name: str):
    """
    Get company research data.
    If not found in DB, the research pipeline will run.
    """

    result = await company_service.get_company(company_name)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"{company_name} not found"
        )

    return result