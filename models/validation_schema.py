"""
Pydantic models for validation schemas.
Maps to metadata parameters and test cases from CSV files.
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class DataType(str, Enum):
    """Data type enumeration."""
    VARCHAR = "VARCHAR"
    INTEGER = "INTEGER"
    TEXT = "TEXT"
    PERCENTAGE = "Percentage"
    DURATION = "Duration"
    URL = "URL"


class Nullability(str, Enum):
    """Nullability options."""
    NOT_NULL = "Not Null"
    NULLABLE = "Nullable"


class ValidationMode(str, Enum):
    """Validation mode options."""
    AUTOMATED = "Automated"
    MANUAL = "Manual"
    AUTOMATED_AND_MANUAL = "Automated & Manual"


class MetadataParameter(BaseModel):
    """Metadata parameter validation rule."""
    sr_no: int
    validator: str
    column_name: str
    category: str
    description: str
    content_type: str
    granularity: str
    minimum_element: int
    maximum_element: int
    data_owner: str
    confidence_level: str
    criticality: str
    data_volatility: str
    update_frequency: str
    data_type: str
    format_constraints: Optional[str] = None
    regex_pattern: Optional[str] = None
    nullability: str
    business_rules: Optional[str] = None
    data_rules: Optional[str] = None
    data_source: Optional[str] = None
    validation_mode: str
    test_cases: Optional[str] = None
    is_derived_from: Optional[str] = None
    derivation_method: Optional[str] = None
    
    class Config:
        use_enum_values = True


class TestCaseCategory(str, Enum):
    """Test case categories."""
    INPUT_VALIDATION = "INPUT VALIDATION"
    DATA_COMPLETENESS = "DATA COMPLETENESS"
    DATA_ACCURACY = "DATA ACCURACY"
    HALLUCINATION_DETECTION = "HALLUCINATION DETECTION"
    INTERNAL_CONSISTENCY = "INTERNAL CONSISTENCY"
    EDGE_CASES = "EDGE CASES"
    BOUNDARY_VALUES = "BOUNDARY VALUES"
    FORMAT_STRUCTURE = "FORMAT & STRUCTURE"
    ADVERSARIAL_TESTS = "ADVERSARIAL TESTS"
    TEMPORAL_VALIDITY = "TEMPORAL VALIDITY"
    AMBIGUITY_RESOLUTION = "AMBIGUITY RESOLUTION"
    CLASSIFICATION_CATEGORIZATION = "CLASSIFICATION & CATEGORIZATION"
    SCALE_PERFORMANCE = "SCALE & PERFORMANCE"
    NULL_NA_HANDLING = "NULL/NA HANDLING"
    QUALITY_THRESHOLDS = "QUALITY THRESHOLDS"


class TestCaseType(str, Enum):
    """Applicable to types."""
    SPECIFIC_PARAMETERS = "Specific-Parameters"
    PER_PARAMETER = "Per-Parameter"
    ALL_PARAMETERS = "All-Parameters"


class Priority(str, Enum):
    """Test case priority."""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class MasterTestCase(BaseModel):
    """Master test case definition."""
    assigned: str
    id: str
    applicable_to: str
    test_case_category: str
    test_case_type: str
    description: str
    example_test_scenarios: str
    priority: str
    
    class Config:
        use_enum_values = True


class TestResult(BaseModel):
    """Individual test result."""
    test_case_id: str
    test_case_description: str
    parameter_name: Optional[str] = None
    passed: bool
    error_message: Optional[str] = None
    severity: str = "high"
    timestamp: str = Field(default_factory=lambda: __import__('datetime').datetime.now().isoformat())


class ValidationReport(BaseModel):
    """Complete validation report for a company."""
    company_name: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    test_results: List[TestResult]
    overall_status: str  # "passed", "failed", "partial"
    failed_parameters: List[str] = []
    
    def calculate_status(self):
        """Calculate overall validation status."""
        if self.failed_tests == 0:
            self.overall_status = "passed"
        elif self.passed_tests == 0:
            self.overall_status = "failed"
        else:
            self.overall_status = "partial"
        
        # Extract unique failed parameters
        self.failed_parameters = list(set([
            r.parameter_name for r in self.test_results 
            if not r.passed and r.parameter_name
        ]))
