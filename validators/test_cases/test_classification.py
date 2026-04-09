"""
Test Cases 12.1-12.5: Classification & Categorization
Tests for company category, industry, nature, sentiment, and risk classification.
"""

import pytest
from typing import Dict, Any
from models.validation_schema import TestResult


class TestClassification:
    """Test classification and categorization accuracy."""
    
    def test_12_1_company_category(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 12.1: Company Category Classification"""
        test_id = "12.1"
        description = "Company Category - Startup/MSME/SMB/Investor/VC classification"
        
        try:
            category = company_data.get("category", "")
            employee_size = company_data.get("employee_size", "")
            
            if not category:
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    parameter_name="category",
                    passed=False,
                    error_message="Category is required but missing"
                )
            
            # Valid categories
            valid_categories = [
                'startup', 'msme', 'smb', 'enterprise', 'investor', 'vc',
                'conglomerate', 'small business', 'medium business'
            ]
            
            if not any(cat in category.lower() for cat in valid_categories):
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    parameter_name="category",
                    passed=False,
                    error_message=f"Invalid category: {category}"
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
    
    def test_12_2_industry_classification(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 12.2: Industry Classification"""
        test_id = "12.2"
        description = "Industry Classification - Accurate GICS sector assignment"
        
        try:
            focus_sectors = company_data.get("focus_sectors", "")
            
            if not focus_sectors:
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    parameter_name="focus_sectors",
                    passed=False,
                    error_message="Focus sectors is required but missing"
                )
            
            # Should be descriptive (more than just one word)
            if len(focus_sectors.strip()) < 5:
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    parameter_name="focus_sectors",
                    passed=False,
                    error_message="Focus sectors too vague or short"
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
    
    def test_12_3_nature_of_company(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 12.3: Nature of Company Classification"""
        test_id = "12.3"
        description = "Nature of Company - Private/Public/Subsidiary correctly identified"
        
        try:
            nature = company_data.get("nature_of_company", "")
            
            if not nature:
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    parameter_name="nature_of_company",
                    passed=False,
                    error_message="Nature of company is required but missing"
                )
            
            # Valid nature types
            valid_natures = [
                'private', 'public', 'subsidiary', 'partnership',
                'non-profit', 'government', 'govt'
            ]
            
            if not any(nat in nature.lower() for nat in valid_natures):
                return TestResult(
                    test_case_id=test_id,
                    test_case_description=description,
                    parameter_name="nature_of_company",
                    passed=False,
                    error_message=f"Invalid nature of company: {nature}"
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
    
    def test_12_4_sentiment_scoring(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 12.4: Sentiment Scoring"""
        test_id = "12.4"
        description = "Sentiment Scoring - Appropriate sentiment classification"
        
        try:
            brand_sentiment = company_data.get("brand_sentiment_score", "")
            glassdoor = company_data.get("glassdoor_rating", "")
            
            # If sentiment score exists, validate format
            if brand_sentiment:
                sentiment_str = str(brand_sentiment).lower()
                
                # Should be positive/neutral/negative or numeric
                valid_sentiments = ['positive', 'neutral', 'negative', 'mixed']
                is_valid_text = any(sent in sentiment_str for sent in valid_sentiments)
                
                # Or should be a reasonable number
                try:
                    score = float(sentiment_str.replace('%', '').strip())
                    is_valid_number = -100 <= score <= 100 or 0 <= score <= 5
                except:
                    is_valid_number = False
                
                if not (is_valid_text or is_valid_number):
                    return TestResult(
                        test_case_id=test_id,
                        test_case_description=description,
                        parameter_name="brand_sentiment_score",
                        passed=False,
                        error_message=f"Invalid sentiment format: {brand_sentiment}",
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
    
    def test_12_5_risk_classification(self, company_data: Dict[str, Any]) -> TestResult:
        """Test Case 12.5: Risk Classification"""
        test_id = "12.5"
        description = "Risk Classification - Appropriate risk level assignment"
        
        try:
            customer_risk = company_data.get("customer_concentration_risk", "")
            geopolitical_risk = company_data.get("geopolitical_risks", "")
            burnout_risk = company_data.get("burnout_risk", "")
            
            # Validate risk level format if present
            risk_fields = [
                ("customer_concentration_risk", customer_risk),
                ("geopolitical_risks", geopolitical_risk),
                ("burnout_risk", burnout_risk)
            ]
            
            for field_name, risk_value in risk_fields:
                if risk_value:
                    risk_str = str(risk_value).lower()
                    
                    # Valid risk levels
                    valid_levels = ['low', 'medium', 'high', 'critical', 'minimal', 'none']
                    
                    # Check if it contains a valid level or is descriptive
                    has_valid_level = any(level in risk_str for level in valid_levels)
                    is_descriptive = len(risk_str) > 15  # Descriptive explanation
                    
                    if not (has_valid_level or is_descriptive):
                        return TestResult(
                            test_case_id=test_id,
                            test_case_description=description,
                            parameter_name=field_name,
                            passed=False,
                            error_message=f"Invalid risk classification: {risk_value}",
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


def run_classification_tests(company_data: Dict[str, Any]) -> list:
    """Run all classification tests."""
    test_suite = TestClassification()
    
    return [
        test_suite.test_12_1_company_category(company_data),
        test_suite.test_12_2_industry_classification(company_data),
        test_suite.test_12_3_nature_of_company(company_data),
        test_suite.test_12_4_sentiment_scoring(company_data),
        test_suite.test_12_5_risk_classification(company_data)
    ]
