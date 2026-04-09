"""
State definition for LangGraph workflow.
"""

from typing import TypedDict, Optional, Dict, Any, List
from models.company_schema import CompanyDataWithValidation
from models.validation_schema import ValidationReport


class AgentState(TypedDict):
    """State for the company research workflow."""
    
    # Input
    company_name: str
    
    # Agent 1: Generation
    generated_data: Optional[CompanyDataWithValidation]
    generation_time: Optional[float]  # Time taken by Agent 1
    
    # Agent 2: Validation
    validated_data: Optional[CompanyDataWithValidation]
    validation_passed: Optional[bool]
    validation_report: Optional[ValidationReport]
    regeneration_count: int
    max_attempts_reached: Optional[bool]
    validation_time: Optional[float]  # Time taken by Agent 2
    total_processing_time: Optional[float]  # Total time (generation + validation)
    
    # Agent 3: Supabase
    raw_data_ids: Optional[List[str]]  # IDs from Table 1 (company_raw_data)
    supabase_result: Optional[Dict[str, Any]]  # Result from Table 2 push
    supabase_success: Optional[bool]  # Whether Supabase push succeeded
    supabase_error: Optional[str]  # Error message if push failed
    
    # File outputs
    data_file_path: Optional[str]  # Path to Excel data file
    report_file_path: Optional[str]  # Path to validation report
    
    # Status tracking
    status: str  # Current workflow status
    error: Optional[str]  # Error message if any


def create_initial_state(company_name: str) -> AgentState:
    """
    Create initial state for workflow.
    
    Args:
        company_name: Name of the company to research
    
    Returns:
        Initial agent state
    """
    return AgentState(
        company_name=company_name,
        generated_data=None,
        generation_time=None,
        validated_data=None,
        validation_passed=None,
        validation_report=None,
        regeneration_count=0,
        max_attempts_reached=False,
        validation_time=None,
        total_processing_time=None,
        raw_data_ids=None,
        supabase_result=None,
        supabase_success=None,
        supabase_error=None,
        data_file_path=None,
        report_file_path=None,
        status="initialized",
        error=None
    )