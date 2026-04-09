"""
Test Cases 1.1-1.6: INPUT VALIDATION
Tests for valid standard input, invalid/empty input, special characters, etc.
"""

from typing import Dict, Any, List
from models.validation_schema import TestResult
from utils.helpers import is_null_or_empty


def test_valid_standard_input(company_data: Dict[str, Any]) -> List[TestResult]:
    """
    Test Case 1.1: Valid Standard Input
    Test with standard, well-formatted company names.
    """
    results = []
    
    # Check if name field is well-formatted
    name = company_data.get("name", "")
    
    if not name or is_null_or_empty(name):
        results.append(TestResult(
            test_case_id="1.1",
            test_case_description="Valid Standard Input - Company Name",
            parameter_name="name",
            passed=False,
            error_message="Company name is missing or empty",
            severity="high"
        ))
    elif len(name.strip()) < 2:
        results.append(TestResult(
            test_case_id="1.1",
            test_case_description="Valid Standard Input - Company Name",
            parameter_name="name",
            passed=False,
            error_message="Company name is too short",
            severity="high"
        ))
    else:
        results.append(TestResult(
            test_case_id="1.1",
            test_case_description="Valid Standard Input - Company Name",
            parameter_name="name",
            passed=True,
            error_message=None,
            severity="low"
        ))
    
    return results


def test_invalid_empty_input(company_data: Dict[str, Any]) -> List[TestResult]:
    """
    Test Case 1.2: Invalid/Empty Input
    Test with null, empty, or whitespace-only inputs for mandatory fields.
    """
    results = []
    
    mandatory_fields = [
        "name", "category", "incorporation_year", "overview_text",
        "nature_of_company", "headquarters_address", "employee_size",
        "focus_sectors", "offerings_description"
    ]
    
    for field in mandatory_fields:
        value = company_data.get(field)
        
        if is_null_or_empty(value):
            results.append(TestResult(
                test_case_id="1.2",
                test_case_description=f"Invalid/Empty Input - {field}",
                parameter_name=field,
                passed=False,
                error_message=f"Mandatory field '{field}' is null or empty",
                severity="high"
            ))
        else:
            results.append(TestResult(
                test_case_id="1.2",
                test_case_description=f"Invalid/Empty Input - {field}",
                parameter_name=field,
                passed=True,
                error_message=None,
                severity="low"
            ))
    
    return results


def test_special_characters_input(company_data: Dict[str, Any]) -> List[TestResult]:
    """
    Test Case 1.3: Special Characters Input
    Test with special characters and symbols in company name.
    """
    results = []
    
    name = company_data.get("name", "")
    
    # Check if name contains only invalid special characters
    if name and name.strip():
        # Allow legitimate special characters like &, ., -, ', (, ), ,
        allowed_pattern = r'^[a-zA-Z0-9\s&.,\-\(\)\'À-ÿ]+$'
        
        import re
        if not re.match(allowed_pattern, name):
            results.append(TestResult(
                test_case_id="1.3",
                test_case_description="Special Characters Input - Company Name",
                parameter_name="name",
                passed=False,
                error_message="Company name contains invalid special characters",
                severity="medium"
            ))
        else:
            results.append(TestResult(
                test_case_id="1.3",
                test_case_description="Special Characters Input - Company Name",
                parameter_name="name",
                passed=True,
                error_message=None,
                severity="low"
            ))
    
    return results


def test_case_sensitivity(company_data: Dict[str, Any]) -> List[TestResult]:
    """
    Test Case 1.6: Case Sensitivity
    Test different case variations of company names.
    """
    results = []
    
    name = company_data.get("name", "")
    
    # Check if name is all uppercase or all lowercase (potential issue)
    if name and name.strip():
        if name.isupper() and len(name) > 3:
            results.append(TestResult(
                test_case_id="1.6",
                test_case_description="Case Sensitivity - Company Name",
                parameter_name="name",
                passed=False,
                error_message="Company name is all uppercase (should be proper case)",
                severity="low"
            ))
        elif name.islower() and len(name) > 3:
            results.append(TestResult(
                test_case_id="1.6",
                test_case_description="Case Sensitivity - Company Name",
                parameter_name="name",
                passed=False,
                error_message="Company name is all lowercase (should be proper case)",
                severity="low"
            ))
        else:
            results.append(TestResult(
                test_case_id="1.6",
                test_case_description="Case Sensitivity - Company Name",
                parameter_name="name",
                passed=True,
                error_message=None,
                severity="low"
            ))
    
    return results


def run_input_validation_tests(company_data: Dict[str, Any]) -> List[TestResult]:
    """Run all input validation tests."""
    results = []
    
    results.extend(test_valid_standard_input(company_data))
    results.extend(test_invalid_empty_input(company_data))
    results.extend(test_special_characters_input(company_data))
    results.extend(test_case_sensitivity(company_data))
    
    return results
