"""
Prompt templates for validation feedback and regeneration guidance.
"""

from typing import Dict, List


def get_validation_feedback_prompt(
    parameter: str,
    current_value: any,
    validation_errors: List[str]
) -> str:
    """
    Get feedback prompt for explaining validation failures.
    
    Args:
        parameter: Parameter name
        current_value: Current value that failed
        validation_errors: List of validation error messages
    
    Returns:
        Feedback prompt
    """
    errors_text = "\n".join(f"  - {error}" for error in validation_errors)
    
    return f"""Parameter '{parameter}' failed validation.

CURRENT VALUE: {current_value}

VALIDATION ERRORS:
{errors_text}

To fix this, the value should:
1. Match the expected format and data type
2. Be factually accurate and verifiable
3. Be consistent with related fields
4. Follow the business rules specified

Please regenerate this parameter with a corrected value."""


def get_batch_regeneration_prompt(
    company_name: str,
    failed_parameters: Dict[str, str]
) -> str:
    """
    Get prompt for regenerating multiple failed parameters.
    
    Args:
        company_name: Company name
        failed_parameters: Dict mapping parameter to error message
    
    Returns:
        Batch regeneration prompt
    """
    params_text = "\n".join(
        f"  - {param}: {error}"
        for param, error in failed_parameters.items()
    )
    
    return f"""The following parameters for {company_name} failed validation and need to be regenerated:

FAILED PARAMETERS:
{params_text}

Please generate corrected values for ALL these parameters in a single JSON object.

Requirements:
- Fix each validation error
- Maintain consistency across all parameters
- Use factual, verifiable data
- Return valid JSON with corrected values

Return format:
{{
  "parameter1": "corrected_value1",
  "parameter2": "corrected_value2",
  ...
}}

Generate the corrections now:"""


VALIDATION_GUIDELINES = """
VALIDATION ERROR TYPES:

1. FORMAT ERRORS:
   - Use correct data types (string, number, boolean)
   - Follow specified formats (dates, URLs, emails)
   - Match regex patterns where specified

2. BUSINESS RULE VIOLATIONS:
   - Ensure logical consistency (e.g., profitable companies have positive profit)
   - Respect dependencies (e.g., if CEO exists, CEO name should too)
   - Follow temporal rules (incorporation year < current year)

3. DATA QUALITY ISSUES:
   - Avoid hallucination - use null for unknown data
   - Be specific and factual
   - Provide recent, verifiable information
   - Avoid vague or generic descriptions

4. CONSISTENCY ERRORS:
   - Related fields must align (revenue mix should sum to 100%)
   - Cross-field validation (YoY growth requires revenue data)
   - Timeline consistency (events in chronological order)

5. COMPLETENESS ISSUES:
   - Mandatory fields cannot be null
   - Provide adequate detail (not just "Yes" or "No")
   - Include context where appropriate
"""


def get_validation_guidelines() -> str:
    """Get validation guidelines for LLM context."""
    return VALIDATION_GUIDELINES
