"""
Test Cases 8.1-8.6: FORMAT & STRUCTURE
Tests for data type validation, URL validity, list formatting, text length validation.
"""

from typing import Dict, Any, List
from models.validation_schema import TestResult
from utils.helpers import validate_url, is_null_or_empty, count_words


def test_data_type_validation(company_data: Dict[str, Any]) -> List[TestResult]:
    """
    Test Case 8.1: Data Type Validation
    Correct data types for each field.
    """
    results = []
    
    # Check incorporation_year is integer
    inc_year = company_data.get("incorporation_year")
    if inc_year and not is_null_or_empty(inc_year):
        try:
            int(inc_year)
            results.append(TestResult(
                test_case_id="8.1",
                test_case_description="Data Type Validation - Incorporation Year",
                parameter_name="incorporation_year",
                passed=True,
                error_message=None,
                severity="low"
            ))
        except (ValueError, TypeError):
            results.append(TestResult(
                test_case_id="8.1",
                test_case_description="Data Type Validation - Incorporation Year",
                parameter_name="incorporation_year",
                passed=False,
                error_message=f"Incorporation year must be an integer, got: {type(inc_year).__name__}",
                severity="high"
            ))
    
    # Check office_count is integer
    office_count = company_data.get("office_count")
    if office_count and not is_null_or_empty(office_count):
        try:
            int(office_count)
            results.append(TestResult(
                test_case_id="8.1",
                test_case_description="Data Type Validation - Office Count",
                parameter_name="office_count",
                passed=True,
                error_message=None,
                severity="low"
            ))
        except (ValueError, TypeError):
            results.append(TestResult(
                test_case_id="8.1",
                test_case_description="Data Type Validation - Office Count",
                parameter_name="office_count",
                passed=False,
                error_message=f"Office count must be an integer, got: {type(office_count).__name__}",
                severity="medium"
            ))
    
    return results


def test_url_validity(company_data: Dict[str, Any]) -> List[TestResult]:
    """
    Test Case 8.2: URL Validity
    Working vs broken links.
    """
    results = []
    
    url_fields = [
        "logo_url", "website_url", "linkedin_url", "facebook_url",
        "instagram_url", "marketing_video_url", "ceo_linkedin_url"
    ]
    
    for field in url_fields:
        url = company_data.get(field)
        
        if url and not is_null_or_empty(url):
            if not validate_url(str(url)):
                results.append(TestResult(
                    test_case_id="8.2",
                    test_case_description=f"URL Validity - {field}",
                    parameter_name=field,
                    passed=False,
                    error_message=f"Invalid URL format: {url}",
                    severity="medium"
                ))
            else:
                results.append(TestResult(
                    test_case_id="8.2",
                    test_case_description=f"URL Validity - {field}",
                    parameter_name=field,
                    passed=True,
                    error_message=None,
                    severity="low"
                ))
    
    return results


def test_list_formatting(company_data: Dict[str, Any]) -> List[TestResult]:
    """
    Test Case 8.5: List Formatting
    Consistent delimiters for multi-value fields.
    """
    results = []
    
    list_fields = [
        "operating_countries", "office_locations", "key_competitors",
        "key_investors", "board_members"
    ]
    
    for field in list_fields:
        value = company_data.get(field)
        
        if value and not is_null_or_empty(value):
            value_str = str(value)
            
            # Check if it looks like a list (has commas or semicolons)
            if ',' in value_str or ';' in value_str:
                # Good - has delimiters
                results.append(TestResult(
                    test_case_id="8.5",
                    test_case_description=f"List Formatting - {field}",
                    parameter_name=field,
                    passed=True,
                    error_message=None,
                    severity="low"
                ))
            elif len(value_str.split()) > 10:
                # Long text without delimiters - might be a formatting issue
                results.append(TestResult(
                    test_case_id="8.5",
                    test_case_description=f"List Formatting - {field}",
                    parameter_name=field,
                    passed=False,
                    error_message=f"List field should use comma/semicolon delimiters",
                    severity="low"
                ))
    
    return results


def test_text_length_validation(company_data: Dict[str, Any]) -> List[TestResult]:
    """
    Test Case 8.6: Text Length Validation
    Fields within reasonable character limits.
    """
    results = []
    
    # Define length constraints
    length_constraints = {
        "short_name": (2, 100),
        "name": (2, 255),
        "overview_text": (50, 5000),
        "headquarters_address": (5, 255),
        "twitter_handle": (1, 50),
    }
    
    for field, (min_len, max_len) in length_constraints.items():
        value = company_data.get(field)
        
        if value and not is_null_or_empty(value):
            value_str = str(value)
            actual_len = len(value_str)
            
            if actual_len < min_len:
                results.append(TestResult(
                    test_case_id="8.6",
                    test_case_description=f"Text Length Validation - {field}",
                    parameter_name=field,
                    passed=False,
                    error_message=f"Length {actual_len} below minimum {min_len}",
                    severity="medium"
                ))
            elif actual_len > max_len:
                results.append(TestResult(
                    test_case_id="8.6",
                    test_case_description=f"Text Length Validation - {field}",
                    parameter_name=field,
                    passed=False,
                    error_message=f"Length {actual_len} exceeds maximum {max_len}",
                    severity="medium"
                ))
            else:
                results.append(TestResult(
                    test_case_id="8.6",
                    test_case_description=f"Text Length Validation - {field}",
                    parameter_name=field,
                    passed=True,
                    error_message=None,
                    severity="low"
                ))
    
    return results


def run_format_structure_tests(company_data: Dict[str, Any]) -> List[TestResult]:
    """Run all format and structure tests."""
    results = []
    
    results.extend(test_data_type_validation(company_data))
    results.extend(test_url_validity(company_data))
    results.extend(test_list_formatting(company_data))
    results.extend(test_text_length_validation(company_data))
    
    return results
