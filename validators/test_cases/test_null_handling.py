"""
Test Cases 14.1-14.5: NULL/NA Handling
Tests for handling unavailable data, N/A fields, and default values.
"""

import pytest
from typing import Dict, Any
from models.validation_schema import TestResult


class TestNullHandling:
    """Test proper NULL/NA handling."""
    
    def test_14_1_unavailable_data(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 14.1: Unavailable Data - Graceful handling"""
        test_id = "14.1"
        description = "Unavailable Data - Graceful null handling"
        
        try:
            # Private company financials should be null or marked as unavailable
            nature = company_data.get("nature_of_company", "").lower()
            annual_revenue = company_data.get("annual_revenue")
            annual_profit = company_data.get("annual_profit")
            
            if "private" in nature:
                # Check that we're not fabricating precise financial data
                if annual_revenue:
                    revenue_str = str(annual_revenue).lower()
                    suspicious = any(word in revenue_str for word in 
                                   ['precisely', 'exactly', 'confirmed to be'])
                    
                    if suspicious:
                        return TestResult(
                            test_case_id=test_id,
                            test_case_description=description,
                            parameter_name="annual_revenue",
                            passed=False,
                            error_message="Suspiciously precise data for private company",
                            severity="high"
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
                error_message=f"Test failed: {str(e)}"
            )
    
    def test_14_2_not_applicable_fields(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 14.2: Not Applicable Fields"""
        test_id = "14.2"
        description = "Not Applicable Fields - Fields that don't apply to entity type"
        
        try:
            category = company_data.get("category", "").lower()
            
            # VC firms shouldn't have "products"
            if 'vc' in category or 'investor' in category:
                products = company_data.get("offerings_description", "")
                if products and 'fund' not in products.lower():
                    # VCs offer funds, not products
                    if any(word in products.lower() for word in 
                          ['product', 'software', 'hardware', 'saas']):
                        return TestResult(
                            test_case_id=test_id,
                            test_case_description=description,
                            parameter_name="offerings_description",
                            passed=False,
                            error_message="VC firm incorrectly described as having products",
                            severity="medium"
                        )
            
            # Bootstrapped companies shouldn't have investors
            funding = company_data.get("recent_funding_rounds", "")
            investors = company_data.get("key_investors", "")
            
            if funding:
                funding_str = str(funding).lower()
                if 'bootstrap' in funding_str or 'self-funded' in funding_str:
                    if investors and 'none' not in str(investors).lower():
                        return TestResult(
                            test_case_id=test_id,
                            test_case_description=description,
                            parameter_name="key_investors",
                            passed=False,
                            error_message="Bootstrapped company shouldn't have external investors",
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
                error_message=f"Test failed: {str(e)}"
            )
    
    def test_14_3_ambiguous_availability(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 14.3: Ambiguous Availability"""
        test_id = "14.3"
        description = "Ambiguous Availability - Unclear if data exists or not found"
        
        try:
            # Check for suspicious "unknown" or "not available" patterns
            suspicious_values = [
                'unknown', 'not available', 'n/a', 'data not found',
                'information unavailable', 'not disclosed'
            ]
            
            issues = []
            for key, value in company_data.items():
                if value:
                    value_str = str(value).lower().strip()
                    # Exact match to suspicious values is OK (proper null handling)
                    # But embedded in longer text is suspicious
                    if any(susp in value_str for susp in suspicious_values):
                        if len(value_str) > 20:  # Embedded in description
                            issues.append(key)
            
            if len(issues) > 5:  # Too many "unknown" fields
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    parameter_name=",".join(issues[:3]),
                    passed=False,
                    error_message=f"Too many ambiguous availability markers: {len(issues)} fields",
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
                error_message=f"Test failed: {str(e)}"
            )
    
    def test_14_4_default_value_handling(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 14.4: Default Value Handling"""
        test_id = "14.4"
        description = "Default Value Handling - Appropriate vs inappropriate defaults"
        
        try:
            # Revenue should not default to $0 unless explicitly stated
            revenue = company_data.get("annual_revenue")
            if revenue:
                revenue_str = str(revenue).lower()
                if revenue_str in ['0', '$0', '0.0', 'zero']:
                    # Check if this is a pre-revenue startup
                    category = company_data.get("category", "").lower()
                    funding = company_data.get("recent_funding_rounds", "")
                    
                    is_early_stage = 'startup' in category or 'seed' in str(funding).lower()
                    
                    if not is_early_stage:
                        return TestResult(
                            test_case_id=test_id,
                            test_case_description=description,
                            parameter_name="annual_revenue",
                            passed=False,
                            error_message="Revenue defaulted to $0 without justification",
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
                error_message=f"Test failed: {str(e)}"
            )
    
    def test_14_5_null_propagation(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 14.5: Null Propagation in calculated fields"""
        test_id = "14.5"
        description = "Null Propagation - Proper null handling in derived fields"
        
        try:
            # CAC:LTV ratio should be null if either CAC or LTV is null
            cac = company_data.get("customer_acquisition_cost")
            ltv = company_data.get("customer_lifetime_value")
            cac_ltv_ratio = company_data.get("cac_ltv_ratio")
            
            if (not cac or not ltv) and cac_ltv_ratio:
                # Has ratio but missing components
                ratio_str = str(cac_ltv_ratio).lower()
                if ratio_str not in ['null', 'none', 'n/a', 'not calculated']:
                    return TestResult(
                        test_case_id=test_id,
                        test_case_description=description,
                        parameter_name="cac_ltv_ratio",
                        passed=False,
                        error_message="Calculated ratio exists without source values",
                        severity="high"
                    )
            
            # YoY growth should be null for new companies
            incorporation_year = company_data.get("incorporation_year")
            yoy_growth = company_data.get("yoy_growth_rate")
            
            if incorporation_year:
                try:
                    year = int(incorporation_year)
                    if 2026 - year < 2:  # Less than 2 years old
                        if yoy_growth and str(yoy_growth).lower() not in ['null', 'none', 'n/a']:
                            # New company claiming YoY growth
                            pass  # This might be OK if they have comparison data
                except:
                    pass
            
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
                error_message=f"Test failed: {str(e)}"
            )


def run_null_handling_tests(company_data: Dict[str, Any]) -> list:
    """Run all null handling tests."""
    test_suite = TestNullHandling()
    
    return [
        test_suite.test_14_1_unavailable_data(company_data),
        test_suite.test_14_2_not_applicable_fields(company_data),
        test_suite.test_14_3_ambiguous_availability(company_data),
        test_suite.test_14_4_default_value_handling(company_data),
        test_suite.test_14_5_null_propagation(company_data)
    ]
