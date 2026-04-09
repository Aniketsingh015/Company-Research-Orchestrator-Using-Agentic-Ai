"""
PyTest configuration and fixtures for testing.
"""

import pytest
import json
from pathlib import Path
from typing import Dict, Any


@pytest.fixture
def sample_company_data() -> Dict[str, Any]:
    """Sample company data for testing."""
    return {
        "name": "Test Company Inc.",
        "short_name": "TestCo",
        "logo_url": "https://example.com/logo.png",
        "category": "Startup",
        "incorporation_year": 2020,
        "overview_text": "A test company for validation testing purposes.",
        "nature_of_company": "Private",
        "headquarters_address": "San Francisco, CA, USA",
        "operating_countries": "United States, Canada",
        "office_count": 2,
        "office_locations": "San Francisco, CA; Toronto, ON",
        "employee_size": "50-100",
        "vision_statement": "To revolutionize testing",
        "mission_statement": "Making testing better for everyone",
        "core_values": "Innovation, Quality, Integrity",
        "website_url": "https://testcompany.com",
        "linkedin_url": "https://linkedin.com/company/testco",
        "primary_contact_email": "contact@testcompany.com",
        "primary_phone_number": "+1-555-0123",
        "focus_sectors": "Technology, Software",
        "offerings_description": "Enterprise software solutions",
        "pain_points_addressed": "Simplifying complex business processes",
        "employee_turnover": "10%",
        "glassdoor_rating": "4.2",
        "annual_revenue": "$5M",
        "recent_funding_rounds": "Series A: $10M (2023)",
        "key_investors": "VC Fund A, Angel Investor B"
    }


@pytest.fixture
def sample_validation_errors() -> Dict[str, str]:
    """Sample validation errors for testing."""
    return {
        "incorporation_year": "Year cannot be in the future",
        "website_url": "Invalid URL format",
        "employee_turnover": "Must be in percentage format (e.g., 15%)"
    }


@pytest.fixture
def config_path() -> Path:
    """Path to config directory."""
    return Path(__file__).parent.parent / "config"


@pytest.fixture
def data_path() -> Path:
    """Path to data directory."""
    return Path(__file__).parent.parent / "data"


@pytest.fixture
def metadata_csv_path(data_path) -> Path:
    """Path to metadata parameters CSV."""
    return data_path / "metadata_params.csv"


@pytest.fixture
def test_cases_csv_path(data_path) -> Path:
    """Path to master test cases CSV."""
    return data_path / "master_test_cases.csv"


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
