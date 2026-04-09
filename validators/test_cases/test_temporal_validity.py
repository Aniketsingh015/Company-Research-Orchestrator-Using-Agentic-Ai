"""
Test Cases 10.1-10.5: Temporal Validity
Tests for knowledge cutoff events, recent changes, and crisis events.
"""

import pytest
from typing import Dict, Any
from datetime import datetime
from models.validation_schema import TestResult


class TestTemporalValidity:
    """Test temporal validity of company data."""
    
    def test_10_1_knowledge_cutoff_events(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test Case 10.1: Knowledge Cutoff Events
        Events after LLM training data cutoff.
        """
        test_id = "10.1"
        description = "Knowledge Cutoff Events - Recent events validation"
        
        try:
            recent_news = company_data.get("recent_news")
            ceo_name = company_data.get("ceo_name")
            recent_funding = company_data.get("recent_funding_rounds")
            
            # Check if recent data is marked as such or properly null
            current_year = 2026
            
            # Recent news should either be null or contain recent years
            if recent_news:
                news_str = str(recent_news).lower()
                # Check for plausible recency indicators
                has_recent_indicator = any(year in news_str for year in 
                                          ['2024', '2025', '2026', 'recent', 'latest'])
                
                # Warning if claiming very recent events without proper sourcing
                if 'january 2026' in news_str or 'february 2026' in news_str or 'march 2026' in news_str:
                    return TestResult(
                        test_case_id=test_id,
                        test_case_description=description,
                        parameter_name="recent_news",
                        passed=False,
                        error_message="Claims events beyond knowledge cutoff without verification",
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
                error_message=f"Knowledge cutoff test failed: {str(e)}"
            )
    
    def test_10_2_recent_structural_changes(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test Case 10.2: Recent Structural Changes
        M&A, restructuring post-cutoff.
        """
        test_id = "10.2"
        description = "Recent Structural Changes - M&A and restructuring validation"
        
        try:
            history = company_data.get("history_timeline", "")
            recent_news = company_data.get("recent_news", "")
            
            combined_text = f"{history} {recent_news}".lower()
            
            # Check for M&A language
            merger_keywords = ['acquired', 'merger', 'acquisition', 'spin-off', 'restructuring']
            has_recent_ma = any(keyword in combined_text for keyword in merger_keywords)
            
            if has_recent_ma:
                # If claiming recent M&A, should have specific details
                year_mentioned = any(str(year) in combined_text for year in [2024, 2025, 2026])
                
                if not year_mentioned:
                    return TestResult(
                        test_case_id=test_id,
                        test_case_description=description,
                        parameter_name="history_timeline",
                        passed=False,
                        error_message="M&A mentioned without specific timeline",
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
                error_message=f"Structural changes test failed: {str(e)}"
            )
    
    def test_10_3_market_position_changes(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test Case 10.3: Market Position Changes
        Shifted competitive landscape.
        """
        test_id = "10.3"
        description = "Market Position Changes - Competitive landscape validation"
        
        try:
            market_share = company_data.get("market_share_percentage")
            competitors = company_data.get("key_competitors")
            
            # Check for overly confident market position claims
            if market_share:
                share_str = str(market_share).lower()
                # Suspicious if claiming exact current market share
                if any(word in share_str for word in ['exactly', 'precisely', 'as of 2026']):
                    return TestResult(
                        test_case_id=test_id,
                        test_case_description=description,
                        parameter_name="market_share_percentage",
                        passed=False,
                        error_message="Overly confident current market share claim",
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
                error_message=f"Market position test failed: {str(e)}"
            )
    
    def test_10_4_regulatory_updates(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test Case 10.4: Regulatory Updates
        Changed compliance requirements.
        """
        test_id = "10.4"
        description = "Regulatory Updates - Compliance changes validation"
        
        try:
            regulatory_status = company_data.get("regulatory_status")
            
            if regulatory_status:
                status_str = str(regulatory_status).lower()
                
                # Check for recent regulatory claims
                recent_reg_keywords = ['new regulation', 'updated compliance', '2026 regulation']
                has_recent_claim = any(keyword in status_str for keyword in recent_reg_keywords)
                
                if has_recent_claim:
                    return TestResult(
                        test_case_id=test_id,
                        test_case_description=description,
                        parameter_name="regulatory_status",
                        passed=False,
                        error_message="Claims recent regulatory changes beyond knowledge",
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
                error_message=f"Regulatory updates test failed: {str(e)}"
            )
    
    def test_10_5_crisis_events(self, company_data: Dict[str, Any]) -> TestResult:
        """
        Test Case 10.5: Crisis Events
        Recent disruptions or scandals.
        """
        test_id = "10.5"
        description = "Crisis Events - Recent disruptions validation"
        
        try:
            layoff_history = company_data.get("layoff_history")
            legal_issues = company_data.get("legal_issues")
            crisis_behavior = company_data.get("crisis_behavior")
            
            crisis_fields = [layoff_history, legal_issues, crisis_behavior]
            
            for idx, field_value in enumerate(crisis_fields):
                if field_value:
                    value_str = str(field_value).lower()
                    
                    # Check for very recent crisis claims
                    very_recent = any(term in value_str for term in 
                                    ['march 2026', 'february 2026', 'this month', 'last week'])
                    
                    if very_recent:
                        field_names = ["layoff_history", "legal_issues", "crisis_behavior"]
                        return TestResult(
                            test_case_id=test_id,
                            test_case_description=description,
                            parameter_name=field_names[idx],
                            passed=False,
                            error_message="Claims very recent crisis events beyond knowledge cutoff",
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
                error_message=f"Crisis events test failed: {str(e)}"
            )


def run_temporal_validity_tests(company_data: Dict[str, Any]) -> list:
    """Run all temporal validity tests."""
    test_suite = TestTemporalValidity()
    
    return [
        test_suite.test_10_1_knowledge_cutoff_events(company_data),
        test_suite.test_10_2_recent_structural_changes(company_data),
        test_suite.test_10_3_market_position_changes(company_data),
        test_suite.test_10_4_regulatory_updates(company_data),
        test_suite.test_10_5_crisis_events(company_data)
    ]
