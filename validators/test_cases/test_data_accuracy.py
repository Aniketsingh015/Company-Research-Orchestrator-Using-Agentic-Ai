"""
Test Cases 3.1-3.5: DATA ACCURACY
Tests for factual correctness, temporal accuracy, numerical precision, cross-field consistency.
"""

from typing import Dict, Any, List
from models.validation_schema import TestResult
from utils.helpers import is_null_or_empty, validate_year, extract_number_from_string
from datetime import datetime


def test_temporal_accuracy(company_data: Dict[str, Any]) -> List[TestResult]:
    """
    Test Case 3.2: Temporal Accuracy
    Current data vs outdated information.
    """
    results = []
    
    # Check incorporation year
    inc_year = company_data.get("incorporation_year")
    if inc_year:
        if not validate_year(inc_year):
            results.append(TestResult(
                test_case_id="3.2",
                test_case_description="Temporal Accuracy - Incorporation Year",
                parameter_name="incorporation_year",
                passed=False,
                error_message=f"Invalid incorporation year: {inc_year}",
                severity="high"
            ))
        else:
            current_year = datetime.now().year
            year_int = int(inc_year)
            
            if year_int > current_year:
                results.append(TestResult(
                    test_case_id="3.2",
                    test_case_description="Temporal Accuracy - Incorporation Year",
                    parameter_name="incorporation_year",
                    passed=False,
                    error_message=f"Incorporation year {inc_year} is in the future",
                    severity="high"
                ))
            else:
                results.append(TestResult(
                    test_case_id="3.2",
                    test_case_description="Temporal Accuracy - Incorporation Year",
                    parameter_name="incorporation_year",
                    passed=True,
                    error_message=None,
                    severity="low"
                ))
    
    return results


def test_numerical_precision(company_data: Dict[str, Any]) -> List[TestResult]:
    """
    Test Case 3.3: Numerical Precision
    Accuracy of numerical values.
    """
    results = []
    
    # Check employee size format
    emp_size = company_data.get("employee_size")
    if emp_size and not is_null_or_empty(emp_size):
        # Should be either a number or a range (e.g., "10-50", "100+")
        import re
        valid_formats = [
            r'^\d+$',  # Just a number
            r'^\d+-\d+$',  # Range
            r'^\d+\+$',  # Number+
            r'^\d+K$',  # K notation
            r'^\d+,\d+$',  # Comma separated
            r'^\d+,\d+\+$'  # Comma + plus
        ]
        
        is_valid = any(re.match(pattern, str(emp_size).replace(' ', '')) for pattern in valid_formats)
        
        if not is_valid:
            results.append(TestResult(
                test_case_id="3.3",
                test_case_description="Numerical Precision - Employee Size",
                parameter_name="employee_size",
                passed=False,
                error_message=f"Invalid employee size format: {emp_size}",
                severity="medium"
            ))
    
    return results


def test_cross_field_consistency(company_data: Dict[str, Any]) -> List[TestResult]:
    """
    Test Case 3.4: Cross-Field Consistency
    Values align across related fields.
    """
    results = []
    
    # Check CAC:LTV ratio consistency
    cac = company_data.get("customer_acquisition_cost")
    ltv = company_data.get("customer_lifetime_value")
    cac_ltv_ratio = company_data.get("cac_ltv_ratio")
    
    if cac and ltv and cac_ltv_ratio and not any(is_null_or_empty(v) for v in [cac, ltv, cac_ltv_ratio]):
        cac_num = extract_number_from_string(str(cac))
        ltv_num = extract_number_from_string(str(ltv))
        ratio_num = extract_number_from_string(str(cac_ltv_ratio))
        
        if cac_num and ltv_num and ratio_num and cac_num > 0:
            expected_ratio = ltv_num / cac_num
            
            # Allow 10% tolerance
            if abs(expected_ratio - ratio_num) > (expected_ratio * 0.1):
                results.append(TestResult(
                    test_case_id="3.4",
                    test_case_description="Cross-Field Consistency - CAC:LTV Ratio",
                    parameter_name="cac_ltv_ratio",
                    passed=False,
                    error_message=f"CAC:LTV ratio inconsistent. Expected ~{expected_ratio:.2f}, got {ratio_num}",
                    severity="medium"
                ))
    
    # Check year of incorporation vs CEO tenure (if available)
    inc_year = company_data.get("incorporation_year")
    if inc_year and validate_year(inc_year):
        current_year = datetime.now().year
        company_age = current_year - int(inc_year)
        
        # Company should not be negative age
        if company_age < 0:
            results.append(TestResult(
                test_case_id="3.4",
                test_case_description="Cross-Field Consistency - Company Age",
                parameter_name="incorporation_year",
                passed=False,
                error_message="Company incorporation year is in the future",
                severity="high"
            ))
    
    return results


def run_data_accuracy_tests(company_data: Dict[str, Any]) -> List[TestResult]:
    """Run all data accuracy tests."""
    results = []
    
    results.extend(test_temporal_accuracy(company_data))
    results.extend(test_numerical_precision(company_data))
    results.extend(test_cross_field_consistency(company_data))
    
    return results
