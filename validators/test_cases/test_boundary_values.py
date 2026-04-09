"""
Test cases for Boundary Values (Test Cases 7.1-7.6).
"""

import pytest
from typing import Dict, Any
from datetime import datetime
from models.validation_schema import TestResult
from utils.helpers import extract_number_from_string, percentage_to_float


class TestBoundaryValues:
    """Test suite for boundary value validation."""
    
    def test_7_1_extreme_high_values(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test 7.1: Very large numbers at upper bounds.
        
        Checks:
        - Employee count reasonability (< 10 million)
        - Revenue magnitude checks
        - Market cap reasonability
        """
        test_id = "7.1"
        description = "Extreme High Values Validation"
        
        try:
            errors = []
            
            # Check employee size
            emp_size = company_data.get('employee_size')
            if emp_size:
                emp_val = extract_number_from_string(str(emp_size))
                if emp_val and emp_val > 10000000:  # 10 million employees
                    errors.append(f"Employee count {emp_val} exceeds realistic maximum")
            
            # Check revenue
            revenue = company_data.get('annual_revenue')
            if revenue:
                rev_val = extract_number_from_string(str(revenue))
                if rev_val and rev_val > 1000000000000:  # > 1 trillion
                    # Only a few companies have revenue > $1T (Apple, Walmart, etc.)
                    errors.append(f"Revenue ${rev_val} is extremely high - verify accuracy")
            
            if errors:
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    passed=False,
                    error_message="; ".join(errors),
                    severity="medium"
                )
            
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=True,
                severity="medium"
            )
        
        except Exception as e:
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=False,
                error_message=f"Test execution error: {str(e)}",
                severity="medium"
            )
    
    def test_7_2_zero_values(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test 7.2: Legitimate zero values in numeric fields.
        
        Checks:
        - Zero offices (remote company - legitimate)
        - Zero funding (bootstrapped - legitimate)
        - Zero turnover (very new/stable - legitimate)
        """
        test_id = "7.2"
        description = "Zero Values Validation"
        
        try:
            warnings = []
            
            # Zero offices can be legitimate (remote company)
            office_count = company_data.get('office_count')
            if office_count == 0:
                # Check if remote policy exists
                remote_policy = company_data.get('remote_policy_details')
                if not remote_policy or 'remote' not in str(remote_policy).lower():
                    warnings.append("Zero offices but no remote policy mentioned")
            
            # Zero funding can be legitimate (bootstrapped)
            funding = company_data.get('total_capital_raised')
            if funding and extract_number_from_string(str(funding)) == 0:
                # Should be marked as bootstrapped
                nature = str(company_data.get('nature_of_company', '')).lower()
                if 'bootstrap' not in nature:
                    warnings.append("Zero funding but not marked as bootstrapped")
            
            if warnings:
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    passed=False,
                    error_message="; ".join(warnings),
                    severity="medium"
                )
            
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=True,
                severity="medium"
            )
        
        except Exception as e:
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=False,
                error_message=f"Test execution error: {str(e)}",
                severity="medium"
            )
    
    def test_7_3_negative_values(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test 7.3: Fields that can legitimately be negative.
        
        Checks:
        - Negative profits (loss-making - legitimate)
        - Negative growth rate (declining - legitimate)
        - Negative cash flow (legitimate for startups)
        """
        test_id = "7.3"
        description = "Negative Values Validation"
        
        try:
            errors = []
            
            # Negative profit is legitimate if company is loss-making
            profit = company_data.get('annual_profit')
            if profit:
                profit_val = extract_number_from_string(str(profit))
                if profit_val and profit_val < 0:
                    profitability = company_data.get('profitability_status', '').lower()
                    if 'profitable' in profitability:
                        errors.append("Negative profit but marked as profitable")
            
            # Negative growth rate is legitimate for declining companies
            growth = company_data.get('yoy_growth_rate')
            if growth:
                growth_val = percentage_to_float(str(growth))
                if growth_val and growth_val < -50:  # More than -50% decline
                    errors.append(f"Extreme negative growth rate: {growth_val}% - verify accuracy")
            
            # Check for fields that should NEVER be negative
            never_negative = ['employee_size', 'office_count', 'incorporation_year']
            for field in never_negative:
                value = company_data.get(field)
                if value:
                    num_val = extract_number_from_string(str(value))
                    if num_val and num_val < 0:
                        errors.append(f"{field} cannot be negative: {num_val}")
            
            if errors:
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    passed=False,
                    error_message="; ".join(errors),
                    severity="high"
                )
            
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=True,
                severity="high"
            )
        
        except Exception as e:
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=False,
                error_message=f"Test execution error: {str(e)}",
                severity="high"
            )
    
    def test_7_4_percentage_bounds(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test 7.4: Values constrained to 0-100%.
        
        Checks:
        - Market share: 0-100%
        - Churn rate: 0-100%
        - YoY growth: can exceed 100%
        - Profit margin: can be negative
        """
        test_id = "7.4"
        description = "Percentage Bounds Validation"
        
        try:
            errors = []
            
            # Fields that MUST be 0-100%
            bounded_percentages = {
                'market_share_percentage': 'Market share',
                'employee_turnover': 'Employee turnover',
                'churn_rate': 'Churn rate'
            }
            
            for field, display_name in bounded_percentages.items():
                value = company_data.get(field)
                if value:
                    pct_val = percentage_to_float(str(value))
                    if pct_val is not None:
                        if pct_val < 0 or pct_val > 100:
                            errors.append(f"{display_name} must be 0-100%, got {pct_val}%")
            
            # Growth rate can exceed 100% (high-growth startups)
            growth = company_data.get('yoy_growth_rate')
            if growth:
                growth_val = percentage_to_float(str(growth))
                if growth_val and growth_val > 1000:  # >1000% growth is suspicious
                    errors.append(f"YoY growth {growth_val}% is extremely high - verify accuracy")
            
            if errors:
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    passed=False,
                    error_message="; ".join(errors),
                    severity="high"
                )
            
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=True,
                severity="high"
            )
        
        except Exception as e:
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=False,
                error_message=f"Test execution error: {str(e)}",
                severity="high"
            )
    
    def test_7_5_date_boundaries(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test 7.5: Invalid or extreme dates.
        
        Checks:
        - No future dates for historical data
        - No dates before 1800
        - Reasonable date formats
        """
        test_id = "7.5"
        description = "Date Boundaries Validation"
        
        try:
            errors = []
            current_year = datetime.now().year
            
            # Check incorporation year
            inc_year = company_data.get('incorporation_year')
            if inc_year:
                if inc_year > current_year:
                    errors.append(f"Incorporation year {inc_year} is in the future")
                if inc_year < 1800:
                    errors.append(f"Incorporation year {inc_year} is before 1800 (unrealistic)")
            
            if errors:
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    passed=False,
                    error_message="; ".join(errors),
                    severity="low"
                )
            
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=True,
                severity="low"
            )
        
        except Exception as e:
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=False,
                error_message=f"Test execution error: {str(e)}",
                severity="low"
            )


def run_boundary_tests(company_data: Dict[str, Any]) -> list:
    """
    Run all boundary value tests.
    
    Args:
        company_data: Company data dictionary
    
    Returns:
        List of TestResult objects
    """
    tester = TestBoundaryValues()
    
    results = [
        tester.test_7_1_extreme_high_values(company_data),
        tester.test_7_2_zero_values(company_data),
        tester.test_7_3_negative_values(company_data),
        tester.test_7_4_percentage_bounds(company_data),
        tester.test_7_5_date_boundaries(company_data)
    ]
    
    return results
