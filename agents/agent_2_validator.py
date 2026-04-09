"""
Agent 2: Validator
Validates company data and triggers regeneration for failed parameters.
"""

from typing import Dict, Any, List, Tuple
from models.company_schema import CompanyDataWithValidation, CompanyData
from models.validation_schema import TestResult, ValidationReport
from validators.test_runner import test_runner
from agents.agent_1_generator import data_generator_agent
from utils.logger import agent_logger
from utils.excel_handler import excel_handler
from config.settings import settings
from pathlib import Path


class ValidatorAgent:
    """Agent 2: Validates data and manages regeneration loop."""
    
    def __init__(self):
        """Initialize the validator agent."""
        self.logger = agent_logger
        self.max_regeneration_attempts = settings.max_regeneration_attempts
    
    def validate_and_regenerate(
        self, 
        company_data_with_validation: CompanyDataWithValidation,
        company_name: str
    ) -> CompanyDataWithValidation:
        """
        Validate company data and regenerate failed parameters.
        
        Args:
            company_data_with_validation: Company data with validation container
            company_name: Name of the company
        
        Returns:
            Validated and regenerated company data
        """
        self.logger.info(f"🔍 Agent 2: Starting validation for {company_name}")
        
        attempt = 0
        
        while attempt < self.max_regeneration_attempts:
            attempt += 1
            self.logger.info(f"📊 Validation attempt {attempt}/{self.max_regeneration_attempts}")
            
            # Convert CompanyData to dict
            company_data_dict = company_data_with_validation.data.model_dump()
            
            # Run all validation tests
            test_results = test_runner.run_all_tests(company_data_dict)
            
            # Get failed parameters
            failed_params = test_runner.get_failed_parameter_list(test_results)
            failed_param_errors = test_runner.get_failed_parameters(test_results)
            
            if not failed_params:
                self.logger.info(f"✅ Agent 2: All validations passed for {company_name}")
                company_data_with_validation.validation_results = test_results
                company_data_with_validation.is_valid = True
                return company_data_with_validation
            
            self.logger.warning(f"❌ Agent 2: {len(failed_params)} parameters failed validation")
            self.logger.warning(f"   Failed parameters: {', '.join(failed_params[:10])}")
            
            if attempt >= self.max_regeneration_attempts:
                self.logger.error(f"⚠️ Maximum regeneration attempts reached")
                company_data_with_validation.validation_results = test_results
                company_data_with_validation.is_valid = False
                company_data_with_validation.regeneration_count = attempt
                return company_data_with_validation
            
            # Regenerate failed parameters
            self.logger.info(f"🔄 Agent 2: Requesting regeneration for {len(failed_params)} parameters")
            
            regenerated_data = data_generator_agent.regenerate_parameters(
                company_name=company_name,
                failed_parameters=failed_params,
                current_data=company_data_dict,
                validation_errors=failed_param_errors
            )
            
            
            # Convert model to dictionary
            data_dict = company_data_with_validation.data.model_dump()
                # Update regenerated values
            for param, new_value in regenerated_data.items():
                if new_value is not None:
                    data_dict[param] = new_value

            # Recreate the CompanyData model
            company_data_with_validation.data = CompanyData(**data_dict)
            
            company_data_with_validation.regeneration_count = attempt
        
        # If we exit the loop, validation failed
        company_data_with_validation.validation_results = test_results
        company_data_with_validation.is_valid = False
        return company_data_with_validation
    
    def create_validation_report(
        self,
        company_name: str,
        test_results: List[TestResult]
    ) -> ValidationReport:
        """
        Create validation report.
        
        Args:
            company_name: Company name
            test_results: List of test results
        
        Returns:
            ValidationReport object
        """
        passed_tests = sum(1 for r in test_results if r.passed)
        failed_tests = len(test_results) - passed_tests
        
        report = ValidationReport(
            company_name=company_name,
            total_tests=len(test_results),
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            test_results=test_results,
            overall_status="unknown"
        )
        
        report.calculate_status()
        return report
    
    def save_validated_data(
        self,
        company_data_with_validation: CompanyDataWithValidation,
        company_name: str
    ) -> Path:
        """
        Save validated data to Excel file.
        
        Args:
            company_data_with_validation: Validated company data
            company_name: Company name
        
        Returns:
            Path to saved Excel file
        """
        # Convert to dictionary
        data_dict = company_data_with_validation.data.model_dump()
        
        # Generate output filename
        filename = excel_handler.generate_output_filename(company_name, suffix="validated")
        output_path = settings.outputs_dir / filename
        
        # Save to Excel
        excel_handler.save_to_excel(data_dict, output_path, sheet_name="Company Data")
        
        self.logger.info(f"💾 Saved validated data to {output_path}")
        
        return output_path
    
    def save_validation_report(
        self,
        validation_report: ValidationReport,
        company_name: str
    ) -> Path:
        """
        Save validation report to Excel.
        
        Args:
            validation_report: Validation report
            company_name: Company name
        
        Returns:
            Path to saved report file
        """
        # Convert test results to dicts
        results_data = [
            {
                "Test ID": r.test_case_id,
                "Description": r.test_case_description,
                "Parameter": r.parameter_name or "N/A",
                "Passed": "✅ Yes" if r.passed else "❌ No",
                "Error Message": r.error_message or "",
                "Severity": r.severity,
                "Timestamp": r.timestamp
            }
            for r in validation_report.test_results
        ]
        
        # Generate filename
        filename = excel_handler.generate_output_filename(company_name, suffix="validation_report")
        output_path = settings.outputs_dir / filename
        
        # Save report
        excel_handler.create_validation_report_excel(
            company_name=company_name,
            validation_results=results_data,
            output_path=output_path
        )
        
        self.logger.info(f"📋 Saved validation report to {output_path}")
        
        return output_path


# Global validator agent instance
validator_agent = ValidatorAgent()
