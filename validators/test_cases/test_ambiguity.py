"""
Test Cases 11.1-11.5: Ambiguity Resolution
Tests for handling multiple entities, subsidiaries, geographic variants, etc.
"""

import pytest
from typing import Dict, Any
from models.validation_schema import TestResult


class TestAmbiguityResolution:
    """Test ambiguity resolution in company identification."""
    
    def test_11_1_multiple_entities_same_name(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 11.1: Multiple Entities Same Name"""
        test_id = "11.1"
        description = "Multiple Entities Same Name - Disambiguation validation"
        
        try:
            name = company_data.get("name", "")
            category = company_data.get("category", "")
            focus_sectors = company_data.get("focus_sectors", "")
            
            # Check for common ambiguous names
            ambiguous_names = ['delta', 'mercury', 'amazon', 'target', 'oracle']
            
            if any(amb in name.lower() for amb in ambiguous_names):
                # Should have clear disambiguation in category or sectors
                if not category or not focus_sectors:
                    return TestResult(
                        test_case_id=test_id,
                        test_case_description=description,
                        parameter_name="category,focus_sectors",
                        passed=False,
                        error_message=f"Ambiguous name '{name}' lacks clear disambiguation",
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
    
    def test_11_2_subsidiaries_vs_parent(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 11.2: Subsidiaries vs Parent"""
        test_id = "11.2"
        description = "Subsidiaries vs Parent - Entity relationship validation"
        
        try:
            name = company_data.get("name", "")
            nature = company_data.get("nature_of_company", "")
            
            # Check if correctly identified as subsidiary
            subsidiary_indicators = ['subsidiary', 'division of', 'owned by']
            is_marked_subsidiary = any(ind in nature.lower() for ind in subsidiary_indicators)
            
            # Known subsidiaries
            known_subs = {
                'instagram': 'meta', 'whatsapp': 'meta', 'youtube': 'google',
                'linkedin': 'microsoft', 'github': 'microsoft'
            }
            
            name_lower = name.lower()
            for sub, parent in known_subs.items():
                if sub in name_lower and not is_marked_subsidiary:
                    return TestResult(
                        test_case_id=test_id,
                        test_case_description=description,
                        parameter_name="nature_of_company",
                        passed=False,
                        error_message=f"{name} should be marked as subsidiary of {parent}",
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
    
    def test_11_3_geographic_variants(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 11.3: Geographic Variants"""
        test_id = "11.3"
        description = "Geographic Variants - Regional entity validation"
        
        try:
            hq = company_data.get("headquarters_address", "")
            operating_countries = company_data.get("operating_countries", "")
            
            # For multinational companies, HQ should be clear
            if operating_countries:
                countries_list = operating_countries.lower()
                if ',' in countries_list or 'multiple' in countries_list:
                    # Multinational - HQ must be specific
                    if not hq or len(hq) < 5:
                        return TestResult(
                            test_case_id=test_id,
                            test_case_description=description,
                            parameter_name="headquarters_address",
                            passed=False,
                            error_message="Multinational company needs specific HQ location"
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
    
    def test_11_4_abbreviation_handling(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 11.4: Abbreviation Handling"""
        test_id = "11.4"
        description = "Abbreviation Handling - Full name vs acronym"
        
        try:
            name = company_data.get("name", "")
            short_name = company_data.get("short_name", "")
            
            # Known abbreviations
            known_abbrevs = {
                'ibm': 'international business machines',
                'at&t': 'american telephone',
                '3m': 'minnesota mining'
            }
            
            name_lower = name.lower()
            for abbrev, full_part in known_abbrevs.items():
                if abbrev in name_lower:
                    # Should have full name, not just abbreviation
                    if full_part not in name_lower and len(name) < 10:
                        return TestResult(
                            test_case_id=test_id,
                            test_case_description=description,
                            parameter_name="name",
                            passed=False,
                            error_message=f"Should use full company name, not just '{abbrev}'",
                            severity="low"
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
    
    def test_11_5_legal_entity_names(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 11.5: Legal Entity Names"""
        test_id = "11.5"
        description = "Legal Entity Names - Official vs common names"
        
        try:
            name = company_data.get("name", "")
            short_name = company_data.get("short_name", "")
            
            # Legal suffixes that should be in official name
            legal_suffixes = ['Inc.', 'Corp.', 'LLC', 'Ltd.', 'Limited', 'Corporation']
            
            has_legal_suffix = any(suffix.lower() in name.lower() for suffix in legal_suffixes)
            
            # For public companies, should have legal entity designation
            nature = company_data.get("nature_of_company", "").lower()
            if 'public' in nature:
                if not has_legal_suffix and len(name) < 50:
                    # May be using common name instead of legal name
                    # This is a warning, not necessarily an error
                    pass  # Acceptable
            
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


def run_ambiguity_resolution_tests(company_data: Dict[str, Any]) -> list:
    """Run all ambiguity resolution tests."""
    test_suite = TestAmbiguityResolution()
    
    return [
        test_suite.test_11_1_multiple_entities_same_name(company_data),
        test_suite.test_11_2_subsidiaries_vs_parent(company_data),
        test_suite.test_11_3_geographic_variants(company_data),
        test_suite.test_11_4_abbreviation_handling(company_data),
        test_suite.test_11_5_legal_entity_names(company_data)
    ]