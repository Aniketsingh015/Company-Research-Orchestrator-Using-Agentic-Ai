"""
Test Cases 15.1-15.5: Quality Thresholds
Tests for confidence levels, source quality, recency, and overall quality.
"""

import pytest
from typing import Dict, Any
from models.validation_schema import TestResult


class TestQualityThresholds:
    """Test data quality thresholds."""
    
    def test_15_1_confidence_levels(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 15.1: Confidence Levels"""
        test_id = "15.1"
        description = "Confidence Levels - High-confidence vs speculative data"
        
        try:
            # Check for speculative language
            speculative_words = [
                'estimated', 'approximately', 'around', 'roughly', 'about',
                'believed to be', 'reported', 'alleged', 'supposedly'
            ]
            
            high_confidence_fields = [
                'name', 'incorporation_year', 'headquarters_address',
                'nature_of_company', 'category'
            ]
            
            issues = []
            for field in high_confidence_fields:
                value = company_data.get(field)
                if value:
                    value_str = str(value).lower()
                    if any(spec in value_str for spec in speculative_words):
                        issues.append(field)
            
            if issues:
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    parameter_name=",".join(issues),
                    passed=False,
                    error_message=f"High-confidence fields contain speculative language: {issues}",
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
    
    def test_15_2_source_quality_tiers(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 15.2: Source Quality Tiers"""
        test_id = "15.2"
        description = "Source Quality Tiers - Primary vs secondary sources"
        
        try:
            # Check for low-quality source indicators
            low_quality_indicators = [
                'wikipedia', 'blog', 'forum', 'reddit', 'quora',
                'according to an article', 'some sources say'
            ]
            
            # Sample some fields for source quality
            text_fields = [
                company_data.get("overview_text", ""),
                company_data.get("history_timeline", ""),
                company_data.get("recent_news", "")
            ]
            
            issues = []
            for idx, text in enumerate(text_fields):
                if text:
                    text_str = str(text).lower()
                    for indicator in low_quality_indicators:
                        if indicator in text_str:
                            issues.append(indicator)
            
            if len(issues) > 2:
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    parameter_name="overview_text,history_timeline,recent_news",
                    passed=False,
                    error_message=f"Multiple low-quality source indicators: {issues[:2]}",
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
    
    def test_15_3_recency_scoring(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 15.3: Recency Scoring"""
        test_id = "15.3"
        description = "Recency Scoring - Recent vs outdated information"
        
        try:
            recent_news = company_data.get("recent_news", "")
            
            if recent_news:
                news_str = str(recent_news).lower()
                
                # Check for very old information being passed as "recent"
                old_years = ['2020', '2019', '2018', '2017', '2016']
                old_year_count = sum(1 for year in old_years if year in news_str)
                
                # Check for actual recent years
                recent_years = ['2024', '2025', '2026']
                recent_year_count = sum(1 for year in recent_years if year in news_str)
                
                if old_year_count > recent_year_count and recent_year_count == 0:
                    return TestResult(
                        test_case_id=test_id,
                        test_case_description=description,
                        parameter_name="recent_news",
                        passed=False,
                        error_message="'Recent news' contains outdated information",
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
    
    def test_15_5_overall_quality_score(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 15.5: Overall Quality Score"""
        test_id = "15.5"
        description = "Overall Quality Score - Composite quality metric"
        
        try:
            # Calculate completeness
            total_fields = len(company_data)
            non_null_fields = sum(1 for v in company_data.values() if v is not None and str(v).strip())
            
            completeness = (non_null_fields / total_fields * 100) if total_fields > 0 else 0
            
            # Check mandatory fields
            mandatory_fields = [
                'name', 'category', 'incorporation_year', 'overview_text',
                'nature_of_company', 'headquarters_address', 'employee_size',
                'focus_sectors', 'offerings_description'
            ]
            
            missing_mandatory = [f for f in mandatory_fields if not company_data.get(f)]
            
            # Quality grade
            if missing_mandatory:
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    parameter_name=",".join(missing_mandatory),
                    passed=False,
                    error_message=f"Missing mandatory fields: {missing_mandatory}"
                )
            
            if completeness < 30:
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    passed=False,
                    error_message=f"Overall data completeness too low: {completeness:.1f}%",
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


def run_quality_threshold_tests(company_data: Dict[str, Any]) -> list:
    """Run all quality threshold tests."""
    test_suite = TestQualityThresholds()
    
    return [
        test_suite.test_15_1_confidence_levels(company_data),
        test_suite.test_15_2_source_quality_tiers(company_data),
        test_suite.test_15_3_recency_scoring(company_data),
        test_suite.test_15_5_overall_quality_score(company_data)
    ]
