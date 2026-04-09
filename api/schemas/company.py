"""Pydantic schemas for Company API endpoints."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class CompanyBase(BaseModel):
    """Base company schema."""
    company_name: str = Field(..., description="Company name")


class CompanyResponse(BaseModel):
    """Response schema for company data."""
    id: str
    company_name: str
    name: Optional[str] = None
    category: Optional[str] = None
    incorporation_year: Optional[int] = None
    overview_text: Optional[str] = None
    employee_size: Optional[Any] = None
    headquarters_address: Optional[str] = None
    annual_revenue: Optional[Any] = None
    validation_passed: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CompanyListResponse(BaseModel):
    """Response schema for list of companies."""
    success: bool
    total: int
    companies: List[CompanyResponse]


class CompanyDetailResponse(BaseModel):
    """Response schema for detailed company data."""
    success: bool
    company: Dict[str, Any]


class CompanyDeleteResponse(BaseModel):
    """Response schema for company deletion."""
    success: bool
    message: str
    company_name: str
