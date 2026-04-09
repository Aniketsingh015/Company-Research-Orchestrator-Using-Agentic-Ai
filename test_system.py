"""
Quick system test to verify all components work together.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all critical imports work."""
    print("Testing imports...")
    
    try:
        from config.settings import settings, validate_settings
        print("✅ Config imports successful")
        
        from config.parameters import COMPANY_PARAMETERS, MANDATORY_PARAMETERS
        print(f"✅ Parameters loaded: {len(COMPANY_PARAMETERS)} total, {len(MANDATORY_PARAMETERS)} mandatory")
        
        from models.company_schema import CompanyData, ValidationResult
        print("✅ Models imports successful")
        
        from agents.agent_1_generator import data_generator_agent
        print("✅ Agent 1 (Generator) loaded")
        
        from agents.agent_2_validator import validator_agent
        print("✅ Agent 2 (Validator) loaded")
        
        from utils.llm_client import llm_client
        print("✅ LLM Client loaded")
        
        from utils.excel_handler import excel_handler
        print("✅ Excel Handler loaded")
        
        from graph.workflow import company_research_workflow
        print("✅ LangGraph Workflow loaded")
        
        return True
    
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_settings():
    """Test that settings are properly configured."""
    print("\nTesting settings...")
    
    try:
        from config.settings import settings, validate_settings
        
        # Validate settings
        validate_settings()
        print("✅ Settings validated successfully")
        
        # Check API key is present based on provider
        if settings.llm_provider == "groq":
            if settings.groq_api_key and len(settings.groq_api_key) > 10:
                print("✅ Groq API key found")
            else:
                print("⚠️  Groq API key not configured")
        elif settings.llm_provider == "openrouter":
            if settings.openrouter_api_key and len(settings.openrouter_api_key) > 10:
                print("✅ OpenRouter API key found")
            else:
                print("⚠️  OpenRouter API key not configured")
        
        # Check data files
        if settings.metadata_params_path.exists():
            print(f"✅ Metadata params file found: {settings.metadata_params_path}")
        else:
            print(f"❌ Metadata params file not found: {settings.metadata_params_path}")
        
        if settings.master_test_cases_path.exists():
            print(f"✅ Master test cases file found: {settings.master_test_cases_path}")
        else:
            print(f"❌ Master test cases file not found: {settings.master_test_cases_path}")
        
        return True
    
    except Exception as e:
        print(f"❌ Settings error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    except Exception as e:
        print(f"❌ Settings error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_parameters():
    """Test parameter definitions."""
    print("\nTesting parameters...")
    
    try:
        from config.parameters import (
            COMPANY_PARAMETERS,
            MANDATORY_PARAMETERS,
            PARAMETER_CATEGORIES,
            validate_parameters
        )
        
        # Validate parameters
        validate_parameters()
        
        print(f"✅ All {len(COMPANY_PARAMETERS)} parameters validated")
        print(f"✅ {len(MANDATORY_PARAMETERS)} mandatory parameters defined")
        print(f"✅ {len(PARAMETER_CATEGORIES)} parameter categories")
        
        return True
    
    except Exception as e:
        print(f"❌ Parameters error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_csv_loading():
    """Test loading CSV files."""
    print("\nTesting CSV file loading...")
    
    try:
        from utils.excel_handler import excel_handler
        from config.settings import settings
        
        # Load metadata params
        metadata_df = excel_handler.load_csv(settings.metadata_params_path)
        print(f"✅ Loaded {len(metadata_df)} metadata parameters")
        
        # Load test cases
        test_cases_df = excel_handler.load_csv(settings.master_test_cases_path)
        print(f"✅ Loaded {len(test_cases_df)} master test cases")
        
        return True
    
    except Exception as e:
        print(f"❌ CSV loading error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_pydantic_models():
    """Test Pydantic model creation."""
    print("\nTesting Pydantic models...")
    
    try:
        from models.company_schema import CompanyData
        
        # Create a test company data object
        test_data = {
            "name": "Test Company Inc.",
            "category": "Startup",
            "incorporation_year": 2020,
            "overview_text": "A test company for validation purposes.",
            "nature_of_company": "Private",
            "headquarters_address": "123 Test St, Test City, TC",
            "employee_size": "50-100",
            "focus_sectors": "Technology, Software",
            "offerings_description": "Software as a Service",
            "pain_points_addressed": "Efficiency and automation"
        }
        
        company = CompanyData(**test_data)
        print(f"✅ Created CompanyData model: {company.name}")
        
        return True
    
    except Exception as e:
        print(f"❌ Pydantic model error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("COMPANY RESEARCH AGENT - SYSTEM TEST")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Settings", test_settings),
        ("Parameters", test_parameters),
        ("CSV Loading", test_csv_loading),
        ("Pydantic Models", test_pydantic_models)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {str(e)}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All systems operational!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
