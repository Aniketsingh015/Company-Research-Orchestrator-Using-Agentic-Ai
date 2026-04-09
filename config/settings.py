"""
Configuration settings for the Company Research Agent system.
Loads environment variables and provides centralized configuration.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys - ONLY Groq and OpenRouter
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")

    # Find the Settings class and add these fields after groq_api_key:

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys - ONLY Groq and OpenRouter
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    
    # LLM Configuration
    llm_provider: str = "groq"  # groq or openrouter ONLY
    default_model: str = "llama-3.3-70b-versatile"  # Groq's best model
    temperature: float = 0.2
    max_tokens: int = 4000
    
    # Supabase Configuration
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")
    supabase_db_url: str = os.getenv("SUPABASE_DB_URL", "")
    
    # Table names
    raw_data_table: str = "company_raw_data"
    validated_data_table: str = "company_validated_data"
    
    # File Paths
    data_dir: Path = BASE_DIR / "data"
    outputs_dir: Path = BASE_DIR / "data" / "outputs"
    metadata_params_path: Path = BASE_DIR / "data" / "metadata_params.csv"
    master_test_cases_path: Path = BASE_DIR / "data" / "master_test_cases.csv"
    
    # Agent Configuration
    max_regeneration_attempts: int = 3
    validation_batch_size: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"  # Add this line to allow extra fields


# Global settings instance
settings = Settings()


def validate_settings():
    """Validate that all required settings are properly configured."""
    errors = []
    
    # Check API key based on provider
    if settings.llm_provider == "groq":
        if not settings.groq_api_key:
            errors.append("GROQ_API_KEY is not set in .env file")
    elif settings.llm_provider == "openrouter":
        if not settings.openrouter_api_key:
            errors.append("OPENROUTER_API_KEY is not set in .env file")
    else:
        errors.append(f"Invalid llm_provider: {settings.llm_provider}. Must be 'groq' or 'openrouter'")
    
    # Check Supabase credentials
    if not settings.supabase_url:
        errors.append("SUPABASE_URL is not set in .env file")
    if not settings.supabase_key:
        errors.append("SUPABASE_KEY is not set in .env file")
    
    if not settings.metadata_params_path.exists():
        errors.append(f"Metadata params file not found at {settings.metadata_params_path}")
    
    if not settings.master_test_cases_path.exists():
        errors.append(f"Master test cases file not found at {settings.master_test_cases_path}")
    
    if not settings.outputs_dir.exists():
        settings.outputs_dir.mkdir(parents=True, exist_ok=True)
    
    if errors:
        raise ValueError(f"Configuration errors:\n" + "\n".join(f"- {e}" for e in errors))
    
    return True


if __name__ == "__main__":
    validate_settings()
    print("✅ All settings validated successfully!")
    print(f"Data directory: {settings.data_dir}")
    print(f"Outputs directory: {settings.outputs_dir}")