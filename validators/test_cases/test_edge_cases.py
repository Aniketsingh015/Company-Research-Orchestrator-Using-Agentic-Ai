"""
Test Cases 6.1-6.3: Edge Cases
Tests for very new companies, very large companies, and private companies.
"""

import pytest
from typing import Dict, Any
from models.validation_schema import TestResult


class TestEdgeCases:
    """Test edge cases like very new/large companies and private entities."""
    
    def test_6_1_very_new_companies(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test Case 6.1: Very New Companies
        Startups with minimal public information.
        """
        test_id = "6.1"
        description = "Very New Companies - Startups with minimal public information"
        
        try:
            incorporation_year = company_data.get("incorporation_year")
            
            if not incorporation_year:
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    parameter_name="incorporation_year",
                    passed=False,
                    error_message="Incorporation year missing for new company validation"
                )
            
            current_year = 2026  # Based on conversation date
            company_age = current_year - int(incorporation_year)
            
            # If company is very new (< 2 years), check for graceful handling
            if company_age < 2:
                # Should handle limited data gracefully
                required_basics = ["name", "category", "overview_text"]
                missing = [field for field in required_basics if not company_data.get(field)]
                
                if missing:
                    return TestResult(
                        test_case_id=test_id,
                        test_case_description=description,
                        parameter_name=",".join(missing),
                        passed=False,
                        error_message=f"New company missing basic fields: {missing}"
                    )
            
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=True
            )
        
        except Exception as e:
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=False,
                error_message=f"Edge case test failed: {str(e)}"
            )
    
    def test_6_2_very_large_companies(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test Case 6.2: Very Large Companies
        Conglomerates with complex structures.
        """
        test_id = "6.2"
        description = "Very Large Companies - Conglomerates with complex structures"
        
        try:
            employee_size = company_data.get("employee_size")
            
            if not employee_size:
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    parameter_name="employee_size",
                    passed=False,
                    error_message="Employee size missing for large company validation"
                )
            
            # Check if it's a large company (basic heuristic)
            employee_str = str(employee_size).lower()
            is_large = any(indicator in employee_str for indicator in 
                          ['100,000', '100000', '1000000', 'million', 'lakhs'])
            
            if is_large:
                # Large companies should have comprehensive data
                expected_fields = [
                    "operating_countries", "office_locations", "key_competitors",
                    "annual_revenue", "top_customers"
                ]
                
                missing_critical = [field for field in expected_fields 
                                   if not company_data.get(field)]
                
                if len(missing_critical) > 3:  # Allow some missing for private companies
                    return TestResult(
                        test_case_id=test_id,
                        test_case_description=description,
                        parameter_name=",".join(missing_critical[:3]),
                        passed=False,
                        error_message=f"Large company missing critical fields: {missing_critical[:3]}"
                    )
            
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=True
            )
        
        except Exception as e:
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=False,
                error_message=f"Large company test failed: {str(e)}"
            )
    
    def test_6_3_private_companies(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test Case 6.3: Private Companies
        Limited publicly available data.
        """
        test_id = "6.3"
        description = "Private Companies - Limited publicly available data"
        
        try:
            nature = company_data.get("nature_of_company", "").lower()
            
            if "private" in nature:
                # Private companies may have null financial data - this is acceptable
                financial_fields = [
                    "annual_revenue", "annual_profit", "valuation",
                    "recent_funding_rounds"
                ]
                
                # Check that we don't have fabricated data for private companies
                suspicious_patterns = []
                for field in financial_fields:
                    value = company_data.get(field)
                    if value:
                        value_str = str(value).lower()
                        # Check for overly specific data that's unlikely for private companies
                        if any(pattern in value_str for pattern in 
                              ['exact', 'precisely', 'confirmed']):
                            suspicious_patterns.append(field)
                
                if suspicious_patterns:
                    return TestResult(
                        test_case_id=test_id,
                        test_case_description=description,
                        parameter_name=",".join(suspicious_patterns),
                        passed=False,
                        error_message=f"Private company has suspiciously specific data: {suspicious_patterns}",
                        severity="medium"
                    )
            
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=True
            )
        
        except Exception as e:
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=False,
                error_message=f"Private company test failed: {str(e)}"
            )


def run_edge_case_tests(company_data: Dict[str, Any]) -> list:
    """Run all edge case tests."""
    test_suite = TestEdgeCases()
    
    return [
        test_suite.test_6_1_very_new_companies(company_data),
        test_suite.test_6_2_very_large_companies(company_data),
        test_suite.test_6_3_private_companies(company_data)
    ]
