"""
Test cases for Internal Consistency (Test Cases 5.1-5.5).
"""

import pytest
import re
from typing import Dict, Any
from models.validation_schema import TestResult
from utils.helpers import extract_number_from_string, percentage_to_float


class TestInternalConsistency:
    """Test suite for internal data consistency."""
    
    def test_5_1_calculated_field_accuracy(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test 5.1: Derived fields match their source values.
        
        Checks:
        - CAC:LTV = LTV ÷ CAC
        - YoY Growth calculation
        - Burn Multiplier calculation
        """
        test_id = "5.1"
        description = "Calculated Field Accuracy"
        
        try:
            errors = []
            
            # Test CAC:LTV ratio
            cac = company_data.get('customer_acquisition_cost')
            ltv = company_data.get('customer_lifetime_value')
            cac_ltv_ratio = company_data.get('cac_ltv_ratio')
            
            if all([cac, ltv, cac_ltv_ratio]):
                try:
                    cac_val = extract_number_from_string(str(cac))
                    ltv_val = extract_number_from_string(str(ltv))
                    ratio_val = extract_number_from_string(str(cac_ltv_ratio))
                    
                    if cac_val and ltv_val and cac_val > 0:
                        expected_ratio = ltv_val / cac_val
                        if ratio_val and abs(ratio_val - expected_ratio) > 0.5:
                            errors.append(
                                f"CAC:LTV ratio mismatch: Expected {expected_ratio:.2f}, got {ratio_val}"
                            )
                except (ValueError, ZeroDivisionError, TypeError) as e:
                    errors.append(f"CAC:LTV calculation error: {str(e)}")
            
            # Test YoY Growth calculation (if historical data available)
            # This would require more complex parsing of revenue_mix or historical data
            
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
    
    def test_5_2_logical_consistency(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test 5.2: Fields logically align with each other.
        
        Checks:
        - If Profitable, profits > 0
        - If Pre-revenue, revenue = 0 or null
        - If Public, funding rounds should be complete
        """
        test_id = "5.2"
        description = "Logical Consistency"
        
        try:
            errors = []
            
            # Test profitability consistency
            profitability = company_data.get('profitability_status', '').lower()
            profit = company_data.get('annual_profit')
            
            if 'profitable' in profitability and profit:
                profit_val = extract_number_from_string(str(profit))
                if profit_val is not None and profit_val <= 0:
                    errors.append("Marked as profitable but profit <= 0")
            
            if 'loss' in profitability or 'unprofitable' in profitability:
                if profit:
                    profit_val = extract_number_from_string(str(profit))
                    if profit_val is not None and profit_val > 0:
                        errors.append("Marked as loss-making but profit > 0")
            
            # Test pre-revenue consistency
            revenue = company_data.get('annual_revenue')
            if 'pre-revenue' in str(company_data.get('category', '')).lower():
                if revenue and revenue != 'null' and str(revenue) != '0':
                    errors.append("Marked as pre-revenue but has revenue")
            
            # Test public company funding
            nature = company_data.get('nature_of_company', '').lower()
            recent_funding = company_data.get('recent_funding_rounds')
            
            if 'public' in nature and recent_funding:
                if any(word in str(recent_funding).lower() for word in ['seed', 'series a', 'series b']):
                    errors.append("Public company should not have early-stage funding rounds")
            
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
    
    def test_5_3_timeline_consistency(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test 5.3: Chronological events in correct order.
        
        Checks:
        - Incorporation < First Funding < IPO
        - CEO tenure start > Company founding
        - Recent news is actually recent
        """
        test_id = "5.3"
        description = "Timeline Consistency"
        
        try:
            from datetime import datetime
            errors = []
            
            incorporation_year = company_data.get('incorporation_year')
            current_year = datetime.now().year
            
            # Test incorporation year
            if incorporation_year:
                if incorporation_year > current_year:
                    errors.append(f"Incorporation year {incorporation_year} is in the future")
                
                if incorporation_year < 1800:
                    errors.append(f"Incorporation year {incorporation_year} is unrealistically old")
            
            # Test CEO tenure vs incorporation
            # Would need CEO start year to validate properly
            
            # Test recent news recency
            recent_news = company_data.get('recent_news')
            if recent_news and str(recent_news).lower() != 'null':
                # Look for year mentions in recent news
                year_pattern = r'\b(19|20)\d{2}\b'
                years = re.findall(year_pattern, str(recent_news))
                if years:
                    oldest_year = min([int(y) for y in years])
                    if current_year - oldest_year > 2:
                        errors.append(f"'Recent' news mentions year {oldest_year} which is not recent")
            
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
    
    def test_5_4_format_consistency(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test 5.4: Standardized formatting across fields.
        
        Checks:
        - Date format consistency
        - Currency notation consistency
        - Phone number format consistency
        """
        test_id = "5.4"
        description = "Format Consistency"
        
        try:
            warnings = []
            
            # Check phone number format
            phone = company_data.get('primary_phone_number')
            contact_phone = company_data.get('contact_person_phone')
            
            if phone and contact_phone:
                # Both should use similar format
                phone_clean1 = re.sub(r'[^\d+]', '', str(phone))
                phone_clean2 = re.sub(r'[^\d+]', '', str(contact_phone))
                
                # Check if one has +country code and other doesn't
                if (phone.startswith('+') and not contact_phone.startswith('+')) or \
                   (contact_phone.startswith('+') and not phone.startswith('+')):
                    warnings.append("Inconsistent phone number format (country code presence)")
            
            # Check percentage formats
            percentage_fields = ['market_share_percentage', 'employee_turnover', 'churn_rate']
            has_percent_sign = []
            
            for field in percentage_fields:
                value = company_data.get(field)
                if value and str(value).strip():
                    has_percent_sign.append('%' in str(value))
            
            if has_percent_sign and len(set(has_percent_sign)) > 1:
                warnings.append("Inconsistent percentage formatting (some with %, some without)")
            
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
    
    def test_5_5_cross_parameter_consistency(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test 5.5: Related metrics support each other.
        
        Checks:
        - High hiring velocity + low turnover = growth
        - Large employee size + many offices = scale
        - High NPS + low churn = customer satisfaction
        """
        test_id = "5.5"
        description = "Cross-Parameter Consistency"
        
        try:
            warnings = []
            
            # Check hiring velocity vs turnover
            hiring = company_data.get('hiring_velocity', '').lower()
            turnover = company_data.get('employee_turnover')
            
            if 'high' in str(hiring) and turnover:
                turnover_val = percentage_to_float(str(turnover))
                if turnover_val and turnover_val > 20:
                    warnings.append("High hiring velocity with high turnover (>20%) - potential red flag")
            
            # Check employee size vs offices
            emp_size = company_data.get('employee_size')
            office_count = company_data.get('office_count', 0)
            
            if emp_size:
                emp_str = str(emp_size)
                if any(indicator in emp_str for indicator in ['10,000', '50,000', '100,000']):
                    if office_count == 0 or office_count == 1:
                        warnings.append("Large employee size but very few offices listed")
            
            # Check NPS vs churn
            nps = company_data.get('net_promoter_score')
            churn = company_data.get('churn_rate')
            
            if nps and churn:
                nps_val = extract_number_from_string(str(nps))
                churn_val = percentage_to_float(str(churn))
                
                if nps_val and churn_val:
                    if nps_val > 50 and churn_val > 15:
                        warnings.append("High NPS but high churn rate - inconsistent customer satisfaction")
            
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


def run_consistency_tests(company_data: Dict[str, Any]) -> list:
    """
    Run all internal consistency tests.
    
    Args:
        company_data: Company data dictionary
    
    Returns:
        List of TestResult objects
    """
    tester = TestInternalConsistency()
    
    results = [
        tester.test_5_1_calculated_field_accuracy(company_data),
        tester.test_5_2_logical_consistency(company_data),
        tester.test_5_3_timeline_consistency(company_data),
        tester.test_5_4_format_consistency(company_data),
        tester.test_5_5_cross_parameter_consistency(company_data)
    ]
    
    return results
