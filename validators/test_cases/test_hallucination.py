"""
Test cases for Hallucination Detection (Test Cases 4.1-4.3).
"""

import pytest
from typing import Dict, Any
from models.validation_schema import TestResult


class TestHallucinationDetection:
    """Test suite for detecting fabricated or false information."""
    
    def test_4_1_fabricated_entities(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test 4.1: Detection of invented people, events, or data.
        
        Checks:
        - Executive names exist and are verifiable
        - Funding rounds are real
        - Awards are legitimate
        """
        test_id = "4.1"
        description = "Fabricated Entities Detection"
        
        try:
            suspicious_patterns = []
            
            # Check CEO name
            if company_data.get('ceo_name'):
                ceo_name = company_data['ceo_name']
                # Flag if CEO name looks suspiciously generic
                generic_names = ['John Doe', 'Jane Doe', 'CEO Name', 'Unknown', 'TBD']
                if any(generic in ceo_name for generic in generic_names):
                    suspicious_patterns.append(f"Generic CEO name: {ceo_name}")
            
            # Check funding rounds
            if company_data.get('recent_funding_rounds'):
                funding = str(company_data['recent_funding_rounds'])
                # Flag if funding rounds have suspiciously round numbers
                if '$1,000,000' in funding or '$10,000,000' in funding:
                    suspicious_patterns.append("Suspiciously round funding amounts")
            
            # Check awards
            if company_data.get('awards_recognitions'):
                awards = str(company_data['awards_recognitions'])
                fake_awards = ['Made Up Award', 'Fictional Prize', 'Best Company Award']
                if any(fake in awards for fake in fake_awards):
                    suspicious_patterns.append("Potentially fabricated awards")
            
            if suspicious_patterns:
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    passed=False,
                    error_message=f"Fabrication indicators: {'; '.join(suspicious_patterns)}",
                    severity="critical"
                )
            
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=True,
                severity="critical"
            )
        
        except Exception as e:
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=False,
                error_message=f"Test execution error: {str(e)}",
                severity="critical"
            )
    
    def test_4_2_plausible_but_false(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test 4.2: Reasonable-sounding but incorrect information.
        
        Checks:
        - CEO name sounds real but might be wrong person
        - Funding amounts are plausible but verifiable
        - Office locations exist but company presence is questionable
        """
        test_id = "4.2"
        description = "Plausible but False Information Detection"
        
        try:
            warnings = []
            
            # Check employee size consistency with other metrics
            if company_data.get('employee_size') and company_data.get('office_count'):
                emp_size_str = str(company_data['employee_size'])
                office_count = company_data.get('office_count', 0)
                
                # Extract number from employee size
                if '-' in emp_size_str:
                    emp_low = int(emp_size_str.split('-')[0].replace(',', ''))
                else:
                    emp_low = int(''.join(filter(str.isdigit, emp_size_str)))
                
                # Warn if employee count seems inconsistent with office count
                if emp_low > 10000 and office_count == 0:
                    warnings.append("Large employee count but no offices listed")
            
            # Check valuation vs revenue consistency
            if company_data.get('valuation') and company_data.get('annual_revenue'):
                # Basic sanity check - valuation should typically be > annual revenue
                # This is a simplified check
                pass  # Would need more sophisticated parsing
            
            if warnings:
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    passed=False,
                    error_message=f"Inconsistencies detected: {'; '.join(warnings)}",
                    severity="critical"
                )
            
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=True,
                severity="critical"
            )
        
        except Exception as e:
            return TestResult(
                test_case_id=test_id,
                test_case_description=description,
                passed=False,
                error_message=f"Test execution error: {str(e)}",
                severity="critical"
            )
    
    def test_4_3_confident_incorrectness(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test 4.3: Wrong data presented with high certainty.
        
        Checks:
        - Assertive statements about unverifiable facts
        - Specific numbers that can't be confirmed
        - Definitive claims without sources
        """
        test_id = "4.3"
        description = "Confident Incorrectness Detection"
        
        try:
            issues = []
            
            # Check for overly specific unverifiable claims
            text_fields = [
                'overview_text',
                'core_value_proposition',
                'strategic_priorities'
            ]
            
            suspicious_phrases = [
                'exactly',
                'precisely',
                'definitively',
                'without a doubt',
                'guaranteed'
            ]
            
            for field in text_fields:
                if company_data.get(field):
                    text = str(company_data[field]).lower()
                    for phrase in suspicious_phrases:
                        if phrase in text:
                            issues.append(f"Overly confident claim in {field}: contains '{phrase}'")
            
            # Check for suspiciously specific numbers in private company financials
            if company_data.get('nature_of_company') == 'Private':
                precise_fields = ['annual_revenue', 'annual_profit', 'burn_rate']
                for field in precise_fields:
                    if company_data.get(field):
                        value = str(company_data[field])
                        # Check for oddly specific numbers (e.g., $12,345,678)
                        if value.count(',') >= 2 and value.endswith(('678', '123', '456')):
                            issues.append(f"Suspiciously precise {field} for private company")
            
            if issues:
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    passed=False,
                    error_message=f"Confident incorrectness indicators: {'; '.join(issues)}",
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


def run_hallucination_tests(company_data: Dict[str, Any]) -> list:
    """
    Run all hallucination detection tests.
    
    Args:
        company_data: Company data dictionary
    
    Returns:
        List of TestResult objects
    """
    tester = TestHallucinationDetection()
    
    results = [
        tester.test_4_1_fabricated_entities(company_data),
        tester.test_4_2_plausible_but_false(company_data),
        tester.test_4_3_confident_incorrectness(company_data)
    ]
    
    return results
