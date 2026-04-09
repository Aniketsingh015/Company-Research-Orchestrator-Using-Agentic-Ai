"""
Test Cases 2.1-2.5: DATA COMPLETENESS
Tests for complete profile, partial profile, empty response, mandatory fields, field dependency.
"""

from typing import Dict, Any, List
from models.validation_schema import TestResult
from utils.helpers import is_null_or_empty
from config.parameters import COMPANY_PARAMETERS, MANDATORY_PARAMETERS


def test_complete_profile(company_data: Dict[str, Any]) -> List[TestResult]:
    """
    Test Case 2.1: Complete Profile
    All mandatory and optional fields populated.
    """
    results = []
    
    total_params = len(COMPANY_PARAMETERS)
    populated_params = sum(1 for p in COMPANY_PARAMETERS if not is_null_or_empty(company_data.get(p)))
    
    completeness_ratio = populated_params / total_params
    
    # Calculate data richness score
    if completeness_ratio >= 0.8:
        severity = "low"
        passed = True
        message = None
    elif completeness_ratio >= 0.5:
        severity = "medium"
        passed = True
        message = f"Data completeness: {completeness_ratio*100:.1f}% (could be improved)"
    else:
        severity = "high"
        passed = False
        message = f"Data completeness: {completeness_ratio*100:.1f}% (too low)"
    
    results.append(TestResult(
        test_case_id="2.1",
        test_case_description="Complete Profile - Overall Completeness",
        parameter_name="all",
        passed=passed,
        error_message=message,
        severity=severity
    ))
    
    return results


def test_partial_profile(company_data: Dict[str, Any]) -> List[TestResult]:
    """
    Test Case 2.2: Partial Profile
    Only some fields populated for lesser-known entities.
    """
    results = []
    
    # Check if at least mandatory fields are populated
    mandatory_populated = sum(
        1 for p in MANDATORY_PARAMETERS 
        if not is_null_or_empty(company_data.get(p))
    )
    
    mandatory_ratio = mandatory_populated / len(MANDATORY_PARAMETERS)
    
    if mandatory_ratio < 0.8:
        results.append(TestResult(
            test_case_id="2.2",
            test_case_description="Partial Profile - Mandatory Fields",
            parameter_name="mandatory_fields",
            passed=False,
            error_message=f"Only {mandatory_ratio*100:.0f}% of mandatory fields populated",
            severity="high"
        ))
    else:
        results.append(TestResult(
            test_case_id="2.2",
            test_case_description="Partial Profile - Mandatory Fields",
            parameter_name="mandatory_fields",
            passed=True,
            error_message=None,
            severity="low"
        ))
    
    return results


def test_mandatory_fields_only(company_data: Dict[str, Any]) -> List[TestResult]:
    """
    Test Case 2.4: Mandatory Fields Only
    Critical fields present, optional fields missing.
    """
    results = []
    
    for field in MANDATORY_PARAMETERS:
        value = company_data.get(field)
        
        if is_null_or_empty(value):
            results.append(TestResult(
                test_case_id="2.4",
                test_case_description=f"Mandatory Field Check - {field}",
                parameter_name=field,
                passed=False,
                error_message=f"Mandatory field '{field}' is missing",
                severity="high"
            ))
        else:
            results.append(TestResult(
                test_case_id="2.4",
                test_case_description=f"Mandatory Field Check - {field}",
                parameter_name=field,
                passed=True,
                error_message=None,
                severity="low"
            ))
    
    return results


def test_field_dependency(company_data: Dict[str, Any]) -> List[TestResult]:
    """
    Test Case 2.5: Field Dependency
    Related fields populated together or empty together.
    """
    results = []
    
    # Define field dependencies
    dependencies = [
        ("ceo_name", "ceo_linkedin_url"),
        ("key_investors", "total_capital_raised"),
        ("recent_funding_rounds", "key_investors"),
        ("annual_revenue", "annual_profit"),
        ("customer_acquisition_cost", "customer_lifetime_value"),
        ("contact_person_name", "contact_person_email"),
    ]
    
    for field1, field2 in dependencies:
        value1 = company_data.get(field1)
        value2 = company_data.get(field2)
        
        has_value1 = not is_null_or_empty(value1)
        has_value2 = not is_null_or_empty(value2)
        
        # If one has value, the other should too
        if has_value1 and not has_value2:
            results.append(TestResult(
                test_case_id="2.5",
                test_case_description=f"Field Dependency - {field1} ↔ {field2}",
                parameter_name=field2,
                passed=False,
                error_message=f"'{field1}' is populated but related field '{field2}' is empty",
                severity="medium"
            ))
        elif has_value2 and not has_value1:
            results.append(TestResult(
                test_case_id="2.5",
                test_case_description=f"Field Dependency - {field1} ↔ {field2}",
                parameter_name=field1,
                passed=False,
                error_message=f"'{field2}' is populated but related field '{field1}' is empty",
                severity="medium"
            ))
    
    return results


def run_data_completeness_tests(company_data: Dict[str, Any]) -> List[TestResult]:
    """Run all data completeness tests."""
    results = []
    
    results.extend(test_complete_profile(company_data))
    results.extend(test_partial_profile(company_data))
    results.extend(test_mandatory_fields_only(company_data))
    results.extend(test_field_dependency(company_data))
    
    return results
