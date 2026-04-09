"""
Integration tests for the complete workflow.
Tests end-to-end functionality of the multi-agent system.
"""

import pytest
from pathlib import Path
from graph.workflow import company_research_workflow
from agents.agent_1_generator import data_generator_agent
from agents.agent_2_validator import data_validator_agent


@pytest.mark.integration
class TestFullWorkflow:
    """Integration tests for the complete company research workflow."""
    
    def test_workflow_initialization(self):
        """Test that workflow initializes correctly."""
        assert company_research_workflow is not None
        assert hasattr(company_research_workflow, 'run')
    
    @pytest.mark.slow
    def test_small_company_generation(self):
        """Test generation for a small, well-known company."""
        company_name = "Stripe"
        
        # Generate data
        data = data_generator_agent.generate_all_parameters(company_name)
        
        # Basic assertions
        assert data is not None
        assert isinstance(data, dict)
        assert len(data) > 0
        
        # Check mandatory fields
        assert data.get("name") is not None
        assert data.get("category") is not None
        assert data.get("incorporation_year") is not None
    
    @pytest.mark.slow
    def test_data_validation(self, sample_company_data):
        """Test validation of company data."""
        # This test uses the sample data fixture
        validation_result = data_validator_agent.validate(sample_company_data)
        
        assert validation_result is not None
        assert hasattr(validation_result, 'is_valid')
        assert hasattr(validation_result, 'failed_parameters')
    
    @pytest.mark.slow
    def test_regeneration_logic(self, sample_company_data, sample_validation_errors):
        """Test parameter regeneration logic."""
        failed_param = list(sample_validation_errors.keys())[0]
        error_msg = sample_validation_errors[failed_param]
        
        # Attempt regeneration
        new_value = data_generator_agent.regenerate_parameter(
            company_name="Test Company",
            parameter=failed_param,
            context=sample_company_data,
            validation_error=error_msg
        )
        
        assert new_value is not None
    
    def test_output_directory_creation(self):
        """Test that output directory is created."""
        from config.settings import settings
        
        assert settings.outputs_dir.exists()
        assert settings.outputs_dir.is_dir()
    
    def test_csv_files_exist(self, metadata_csv_path, test_cases_csv_path):
        """Test that required CSV files exist."""
        assert metadata_csv_path.exists(), "Metadata CSV not found"
        assert test_cases_csv_path.exists(), "Test cases CSV not found"


@pytest.mark.integration
class TestWorkflowSteps:
    """Test individual workflow steps."""
    
    def test_agent_1_exists(self):
        """Test that Agent 1 is properly initialized."""
        assert data_generator_agent is not None
        assert hasattr(data_generator_agent, 'generate_all_parameters')
    
    def test_agent_2_exists(self):
        """Test that Agent 2 is properly initialized."""
        assert data_validator_agent is not None
        assert hasattr(data_validator_agent, 'validate')
    
    def test_parameters_loaded(self):
        """Test that 163 parameters are loaded."""
        from config.parameters import COMPANY_PARAMETERS
        
        assert len(COMPANY_PARAMETERS) == 163
    
    def test_metadata_params_loaded(self, metadata_csv_path):
        """Test that metadata parameters can be loaded."""
        import pandas as pd
        
        df = pd.read_csv(metadata_csv_path)
        assert len(df) > 0
        assert 'column_name' in df.columns
    
    def test_test_cases_loaded(self, test_cases_csv_path):
        """Test that master test cases can be loaded."""
        import pandas as pd
        
        df = pd.read_csv(test_cases_csv_path)
        assert len(df) > 0
        assert 'ID' in df.columns or 'id' in df.columns


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
