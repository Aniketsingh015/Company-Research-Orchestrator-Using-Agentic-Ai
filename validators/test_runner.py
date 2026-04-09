"""
Test Runner - Consolidates all test cases
Runs metadata validation + all master test cases
"""

from typing import Dict, Any, List
from models.validation_schema import TestResult
from validators.metadata_validator import metadata_validator
from validators.test_cases.test_input_validation import run_input_validation_tests
from validators.test_cases.test_data_completeness import run_data_completeness_tests
from validators.test_cases.test_data_accuracy import run_data_accuracy_tests
from validators.test_cases.test_format_structure import run_format_structure_tests
from utils.logger import validation_logger


class TestRunner:
    """Runs all validation tests on company data."""
    
    def __init__(self):
        """Initialize test runner."""
        self.logger = validation_logger
    
    def run_all_tests(self, company_data: Dict[str, Any]) -> List[TestResult]:
        """
        Run all validation tests.
        
        Args:
            company_data: Company data dictionary
        
        Returns:
            List of all test results
        """
        all_results = []
        
        self.logger.info("🧪 Running metadata parameter validation...")
        metadata_results = metadata_validator.validate_all(company_data)
        all_results.extend(metadata_results)
        
        self.logger.info("🧪 Running input validation tests...")
        all_results.extend(run_input_validation_tests(company_data))
        
        self.logger.info("🧪 Running data completeness tests...")
        all_results.extend(run_data_completeness_tests(company_data))
        
        self.logger.info("🧪 Running data accuracy tests...")
        all_results.extend(run_data_accuracy_tests(company_data))
        
        self.logger.info("🧪 Running format & structure tests...")
        all_results.extend(run_format_structure_tests(company_data))
        
        # Calculate statistics
        total_tests = len(all_results)
        passed_tests = sum(1 for r in all_results if r.passed)
        failed_tests = total_tests - passed_tests
        
        self.logger.info(f"✅ Tests Passed: {passed_tests}/{total_tests}")
        self.logger.info(f"❌ Tests Failed: {failed_tests}/{total_tests}")
        
        return all_results
    
    def get_failed_parameters(self, test_results: List[TestResult]) -> Dict[str, str]:
        """
        Extract failed parameters and their error messages.
        
        Args:
            test_results: List of test results
        
        Returns:
            Dictionary of parameter -> error message
        """
        failed_params = {}
        
        for result in test_results:
            if not result.passed and result.parameter_name:
                # Keep the first error for each parameter
                if result.parameter_name not in failed_params:
                    failed_params[result.parameter_name] = result.error_message or "Validation failed"
        
        return failed_params
    
    def get_failed_parameter_list(self, test_results: List[TestResult]) -> List[str]:
        """
        Get list of unique failed parameters.
        
        Args:
            test_results: List of test results
        
        Returns:
            List of failed parameter names
        """
        return list(set([
            r.parameter_name for r in test_results 
            if not r.passed and r.parameter_name and r.parameter_name != "all"
        ]))


# Global test runner instance
test_runner = TestRunner()
