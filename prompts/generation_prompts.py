"""
Prompts for Agent 1 (Data Generation).
"""

from typing import List
import json


def get_system_prompt() -> str:
    """Get system prompt for data generation."""
    return """You are an expert company research analyst with deep knowledge of businesses, industries, and market dynamics.

Your task is to generate comprehensive, accurate company data based on publicly available information.

CRITICAL RULES:
1. Return ONLY valid JSON with no additional text before or after
2. Use the exact parameter names provided in the request
3. For unknown/unavailable data, use null instead of fabricating information
4. Ensure all mandatory fields are populated with real data
5. Be factual and avoid hallucination - if you don't know, use null
6. Maintain consistency across related fields
7. Use proper data types (strings for text, numbers for numeric values)
8. Follow standard formatting conventions (dates, URLs, emails, etc.)

DATA QUALITY STANDARDS:
- Names: Use official legal names from government registrations
- URLs: Ensure they are valid and accessible
- Numbers: Use realistic ranges and proper formatting
- Dates: Use YYYY format for years, proper date formats
- Consistency: Related fields must align (e.g., CEO tenure < company age)

AVOID:
- Making up specific names, dates, or numbers when unknown
- Inventing awards, partnerships, or events
- Providing outdated information as current
- Hallucinating details about people or financial metrics"""


def get_generation_prompt(company_name: str, parameters: List[str]) -> str:
    """
    Get user prompt for generating company data.
    
    Args:
        company_name: Name of the company
        parameters: List of parameters to generate
    
    Returns:
        Formatted prompt string
    """
    return f"""Generate comprehensive data for the company: {company_name}

Return a JSON object with these exact keys (use null for unavailable data):
{json.dumps(parameters, indent=2)}

MANDATORY FIELDS (must be populated):
- name
- category
- incorporation_year
- overview_text
- nature_of_company
- headquarters_address
- employee_size
- focus_sectors
- offerings_description

GUIDELINES:
1. Research the company thoroughly
2. Use real, verifiable information when available
3. For private/unavailable data (e.g., financials for private companies), use null
4. Ensure consistency:
   - If public company → must have valuation, revenue data
   - If startup → may not have all financial metrics
   - If VC/Investor → focus on investment data, not products
5. Maintain logical relationships:
   - incorporation_year must be before current year
   - employee_size should align with office_count and operating_countries
   - Financial metrics should be consistent (revenue > profit for profitable companies)

Return ONLY the JSON object. Do not include any explanatory text."""


def get_regeneration_prompt(
    company_name: str,
    parameter: str,
    current_value: any,
    validation_error: str,
    context: dict
) -> str:
    """
    Get prompt for regenerating a failed parameter.
    
    Args:
        company_name: Name of the company
        parameter: Parameter to regenerate
        current_value: Current value that failed
        validation_error: Error message from validation
        context: Existing company data for context
    
    Returns:
        Formatted prompt string
    """
    context_snippet = {k: v for k, v in list(context.items())[:10]}  # First 10 for context
    
    return f"""Regenerate the parameter "{parameter}" for company: {company_name}

CURRENT VALUE (FAILED): {json.dumps(current_value)}

VALIDATION ERROR: {validation_error}

CONTEXT (other company data for consistency):
{json.dumps(context_snippet, indent=2)}

INSTRUCTIONS:
1. Fix the validation error
2. Ensure the new value is accurate and verifiable
3. Maintain consistency with the context provided
4. Use null if data is truly unavailable (don't fabricate)
5. Return ONLY a JSON object with the parameter name and corrected value

Example response format:
{{"{parameter}": "corrected value"}}

Return ONLY the JSON object."""


def get_batch_generation_prompt(company_name: str, parameters: List[str], batch_size: int = 20) -> List[str]:
    """
    Generate prompts for batch processing (if needed for large parameter sets).
    
    Args:
        company_name: Name of the company
        parameters: List of all parameters
        batch_size: Number of parameters per batch
    
    Returns:
        List of prompts for each batch
    """
    prompts = []
    for i in range(0, len(parameters), batch_size):
        batch = parameters[i:i + batch_size]
        prompts.append(get_generation_prompt(company_name, batch))
    return prompts
