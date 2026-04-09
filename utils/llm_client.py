"""
LLM Client for Groq and OpenRouter APIs ONLY.
Handles all LLM calls with retry logic and error handling.
"""

import json
from typing import Dict, Any, Optional, List
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from config.settings import settings


class LLMClient:
    """Wrapper for Groq/OpenRouter APIs with retry logic."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize LLM client.
        
        Args:
            api_key: API key (defaults to settings based on provider)
            model: Model name (defaults to settings)
        """
        self.provider = settings.llm_provider
        self.model = model or settings.default_model
        self.temperature = settings.temperature
        self.max_tokens = settings.max_tokens
        
        # Configure client based on provider (ONLY Groq or OpenRouter)
        if self.provider == "groq":
            self.api_key = api_key or settings.groq_api_key
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.groq.com/openai/v1"
            )
        elif self.provider == "openrouter":
            self.api_key = api_key or settings.openrouter_api_key
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1"
            )
        else:
            raise ValueError(f"Invalid provider: {self.provider}. Must be 'groq' or 'openrouter'")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def generate_completion(
        self, 
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Generate completion from LLM API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            response_format: Response format (e.g., {"type": "json_object"})
        
        Returns:
            Generated text content
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                response_format=response_format
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"❌ Error in LLM generation: {str(e)}")
            raise
    
    def generate_json_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate JSON completion from LLM API.
        
        Args:
            messages: List of message dictionaries
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
        
        Returns:
            Parsed JSON dictionary
        """
        response_text = self.generate_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON response: {str(e)}")
            print(f"Response text: {response_text[:500]}")
            raise
    
    def generate_company_data(self, company_name: str, parameters: List[str]) -> Dict[str, Any]:
        """
        Generate company data for specified parameters.
        
        Args:
            company_name: Name of the company
            parameters: List of parameters to generate
        
        Returns:
            Dictionary with generated company data
        """
        system_prompt = """You are an expert company research analyst. Generate accurate, comprehensive company data based on publicly available information. 
        
CRITICAL INSTRUCTIONS:
1. Return ONLY valid JSON with no additional text
2. Use the exact parameter names provided
3. For unknown/unavailable data, use null instead of making up information
4. Ensure all mandatory fields are populated
5. Be factual and avoid hallucination
6. Use proper data types (strings, numbers, etc.)"""
        
        user_prompt = f"""Generate comprehensive data for the company: {company_name}

Return a JSON object with these exact keys:
{json.dumps(parameters, indent=2)}

Requirements:
- Use real, verifiable information when available
- Use null for unavailable data (don't fabricate)
- Ensure data consistency across related fields
- Follow standard formatting (dates, URLs, etc.)
- Return ONLY the JSON object, no additional text"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return self.generate_json_completion(messages, max_tokens=4000)
    
    def regenerate_parameter(
        self, 
        company_name: str, 
        parameter: str,
        context: Dict[str, Any],
        validation_error: str
    ) -> Any:
        """
        Regenerate a specific parameter that failed validation.
        
        Args:
            company_name: Name of the company
            parameter: Parameter name to regenerate
            context: Existing company data context
            validation_error: Error message from validation
        
        Returns:
            Regenerated parameter value
        """
        system_prompt = """You are an expert company research analyst. Regenerate ONLY the requested parameter with accurate information.

CRITICAL:
- Return ONLY valid JSON with the single parameter
- Fix the validation error mentioned
- Ensure consistency with provided context
- Be factual and avoid hallucination"""
        
        user_prompt = f"""Company: {company_name}
Parameter to regenerate: {parameter}
Validation Error: {validation_error}

Existing Context (for consistency):
{json.dumps(context, indent=2)[:1000]}

Generate ONLY this parameter with correct, validated data.
Return JSON format: {{"{parameter}": "value"}}"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        result = self.generate_json_completion(messages, max_tokens=500)
        return result.get(parameter) or result.get("parameter_name")


# Global LLM client instance
llm_client = LLMClient()