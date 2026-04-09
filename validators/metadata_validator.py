"""
Metadata Parameter Validator
Validates company data against 22 metadata parameter rules from CSV.
"""

import pandas as pd
import re
from typing import Dict, Any, List, Optional
from pathlib import Path
from models.validation_schema import MetadataParameter, TestResult
from utils.logger import validation_logger
from utils.helpers import (
    validate_url, validate_email, validate_year, 
    validate_phone, is_null_or_empty, validate_regex_pattern,
    percentage_to_float, count_words
)
from config.settings import settings


class MetadataValidator:
    """Validates company data against metadata parameter rules."""
    
    def __init__(self):
        """Initialize metadata validator."""
        self.logger = validation_logger
        self.metadata_params = self._load_metadata_params()
        self.logger.info(f"✅ Loaded {len(self.metadata_params)} metadata parameters")
    
    def _load_metadata_params(self) -> List[MetadataParameter]:
        """Load metadata parameters from CSV."""
        try:
            # Try different encodings
            for encoding in ['utf-8', 'latin-1', 'ISO-8859-1', 'cp1252']:
                try:
                    df = pd.read_csv(settings.metadata_params_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError("Could not decode CSV with any standard encoding")
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            metadata_params = []
            for _, row in df.iterrows():
                try:
                    param = MetadataParameter(
                        sr_no=int(row['sr_no']) if pd.notna(row['sr_no']) else 0,
                        validator=str(row['Validator']) if pd.notna(row['Validator']) else "",
                        column_name=str(row['column_name']) if pd.notna(row['column_name']) else "",
                        category=str(row['category']) if pd.notna(row['category']) else "",
                        description=str(row['description']) if pd.notna(row['description']) else "",
                        content_type=str(row['content_type']) if pd.notna(row['content_type']) else "",
                        granularity=str(row['granularity']) if pd.notna(row['granularity']) else "",
                        minimum_element=int(row['minimum_element']) if pd.notna(row['minimum_element']) else 0,
                        maximum_element=int(row['maximum_element']) if pd.notna(row['maximum_element']) else 1000,
                        data_owner=str(row['data_owner']) if pd.notna(row['data_owner']) else "",
                        confidence_level=str(row['confidence_level']) if pd.notna(row['confidence_level']) else "",
                        criticality=str(row['criticality']) if pd.notna(row['criticality']) else "",
                        data_volatility=str(row['data_volatility']) if pd.notna(row['data_volatility']) else "",
                        update_frequency=str(row['update_frequency']) if pd.notna(row['update_frequency']) else "",
                        data_type=str(row['data_type']) if pd.notna(row['data_type']) else "",
                        format_constraints=str(row['format_constraints']) if pd.notna(row['format_constraints']) else None,
                        regex_pattern=str(row['regex_pattern']) if pd.notna(row['regex_pattern']) else None,
                        nullability=str(row['nullability']) if pd.notna(row['nullability']) else "",
                        business_rules=str(row['business_rules']) if pd.notna(row['business_rules']) else None,
                        data_rules=str(row['data_rules']) if pd.notna(row['data_rules']) else None,
                        data_source=str(row['data_source']) if pd.notna(row['data_source']) else None,
                        validation_mode=str(row['validation_mode']) if pd.notna(row['validation_mode']) else "",
                        test_cases=str(row['test_cases']) if pd.notna(row['test_cases']) else None,
                        is_derived_from=str(row['is_dervied_from']) if pd.notna(row['is_dervied_from']) else None,
                        derivation_method=str(row['derivation_method']) if pd.notna(row['derivation_method']) else None
                    )
                    metadata_params.append(param)
                except Exception as e:
                    self.logger.warning(f"Error parsing row {row.get('sr_no', 'unknown')}: {str(e)}")
                    continue
            
            return metadata_params
        
        except Exception as e:
            self.logger.error(f"Error loading metadata params: {str(e)}")
            raise
    
    def validate_all(self, company_data: Dict[str, Any]) -> List[TestResult]:
        """
        Validate all metadata parameters.
        
        Args:
            company_data: Company data dictionary
        
        Returns:
            List of TestResult objects
        """
        results = []
        
        for param in self.metadata_params:
            result = self._validate_parameter(param, company_data)
            if result:
                results.append(result)
        
        return results
    
    def _validate_parameter(
        self, 
        metadata_param: MetadataParameter, 
        company_data: Dict[str, Any]
    ) -> Optional[TestResult]:
        """
        Validate a single parameter against its metadata rules.
        
        Args:
            metadata_param: Metadata parameter definition
            company_data: Company data dictionary
        
        Returns:
            TestResult or None if parameter not in data
        """
        # Map column name to actual parameter name (convert to snake_case)
        param_name = self._map_column_name(metadata_param.column_name)
        
        # Get value from company data
        value = company_data.get(param_name)
        
        # Check nullability
        if metadata_param.nullability == "Not Null":
            if is_null_or_empty(value):
                return TestResult(
                    test_case_id=f"META_{metadata_param.sr_no}",
                    test_case_description=f"Nullability check for {metadata_param.column_name}",
                    parameter_name=param_name,
                    passed=False,
                    error_message=f"Field is mandatory but got null/empty value",
                    severity="high"
                )
        
        # If value is null and nullable, skip other validations
        if is_null_or_empty(value) and metadata_param.nullability == "Nullable":
            return TestResult(
                test_case_id=f"META_{metadata_param.sr_no}",
                test_case_description=f"Validation for {metadata_param.column_name}",
                parameter_name=param_name,
                passed=True,
                error_message=None,
                severity="low"
            )
        
        # Length validation
        if value and isinstance(value, str):
            value_len = len(value)
            if value_len < metadata_param.minimum_element:
                return TestResult(
                    test_case_id=f"META_{metadata_param.sr_no}",
                    test_case_description=f"Length check for {metadata_param.column_name}",
                    parameter_name=param_name,
                    passed=False,
                    error_message=f"Length {value_len} is below minimum {metadata_param.minimum_element}",
                    severity="medium"
                )
            
            if value_len > metadata_param.maximum_element:
                return TestResult(
                    test_case_id=f"META_{metadata_param.sr_no}",
                    test_case_description=f"Length check for {metadata_param.column_name}",
                    parameter_name=param_name,
                    passed=False,
                    error_message=f"Length {value_len} exceeds maximum {metadata_param.maximum_element}",
                    severity="medium"
                )
        
        # Regex pattern validation
        if metadata_param.regex_pattern and value:
            if not validate_regex_pattern(str(value), metadata_param.regex_pattern):
                return TestResult(
                    test_case_id=f"META_{metadata_param.sr_no}",
                    test_case_description=f"Regex pattern check for {metadata_param.column_name}",
                    parameter_name=param_name,
                    passed=False,
                    error_message=f"Value does not match regex pattern: {metadata_param.regex_pattern}",
                    severity="high"
                )
        
        # Data type validation
        if not self._validate_data_type(value, metadata_param.data_type, param_name):
            return TestResult(
                test_case_id=f"META_{metadata_param.sr_no}",
                test_case_description=f"Data type check for {metadata_param.column_name}",
                parameter_name=param_name,
                passed=False,
                error_message=f"Invalid data type. Expected: {metadata_param.data_type}",
                severity="high"
            )
        
        # Specific validations based on content type
        error = self._validate_content_type(value, metadata_param.content_type, param_name)
        if error:
            return TestResult(
                test_case_id=f"META_{metadata_param.sr_no}",
                test_case_description=f"Content type check for {metadata_param.column_name}",
                parameter_name=param_name,
                passed=False,
                error_message=error,
                severity="medium"
            )
        
        # If all validations pass
        return TestResult(
            test_case_id=f"META_{metadata_param.sr_no}",
            test_case_description=f"Validation for {metadata_param.column_name}",
            parameter_name=param_name,
            passed=True,
            error_message=None,
            severity="low"
        )
    
    def _validate_data_type(self, value: Any, data_type: str, param_name: str) -> bool:
        """Validate data type."""
        if is_null_or_empty(value):
            return True
        
        if "INTEGER" in data_type:
            try:
                int(value)
                return True
            except (ValueError, TypeError):
                return False
        
        if "VARCHAR" in data_type or "TEXT" in data_type:
            return isinstance(value, str)
        
        return True
    
    def _validate_content_type(self, value: Any, content_type: str, param_name: str) -> Optional[str]:
        """Validate based on content type."""
        if is_null_or_empty(value):
            return None
        
        value_str = str(value)
        
        # URL validation
        if "URL" in content_type:
            if not validate_url(value_str):
                return "Invalid URL format"
        
        # Email validation
        if "email" in param_name.lower() or "Email" in content_type:
            if not validate_email(value_str):
                return "Invalid email format"
        
        # Year validation
        if "Year" in content_type or "year" in param_name.lower():
            if not validate_year(value):
                return "Invalid year"
        
        # Phone validation
        if "phone" in param_name.lower():
            if not validate_phone(value_str):
                return "Invalid phone number format"
        
        # Percentage validation
        if "Percentage" in content_type:
            pct = percentage_to_float(value_str)
            if pct is None or pct < 0 or pct > 100:
                return "Invalid percentage (must be 0-100)"
        
        return None
    
    def _map_column_name(self, column_name: str) -> str:
        """Map column name from CSV to parameter name."""
        # Simple mapping - convert to lowercase with underscores
        mapped = column_name.lower().replace(" ", "_").replace("/", "_")
        mapped = re.sub(r'[^\w\s_]', '', mapped)
        mapped = re.sub(r'_+', '_', mapped)
        
        # Handle specific mappings
        mapping = {
            "company_name": "name",
            "short_name": "short_name",
            "logo": "logo_url",
            "year_of_incorporation": "incorporation_year",
            "overview_of_the_company": "overview_text",
            "company_headquarters": "headquarters_address",
            "countries_operating_in": "operating_countries",
            "number_of_offices_beyond_hq": "office_count",
            "pain_points_being_addressed": "pain_points_addressed",
            "focus_sectors_industries": "focus_sectors",
            "services_offerings_products": "offerings_description",
            "r_and_d_investment": "r_and_d_investment",
            "ai_ml_adoption_level": "ai_ml_adoption_level"
        }
        
        return mapping.get(mapped, mapped)


# Global validator instance
metadata_validator = MetadataValidator()
