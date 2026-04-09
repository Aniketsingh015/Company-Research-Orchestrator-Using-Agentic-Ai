"""
Agent 1: Data Generator
Generates company data for all 163 parameters using LLM.
"""

from typing import Dict, Any, List
from models.company_schema import CompanyData, CompanyDataWithValidation
from utils.llm_client import llm_client
from utils.logger import agent_logger
from config.parameters import COMPANY_PARAMETERS
import time
import json


def normalize_for_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize LLM output to match CompanyData schema.
    Prevents Pydantic validation crashes.
    """

    normalized = {}

    for key, value in data.items():

        if value is None:
            normalized[key] = None

        # Convert dict/list → JSON string
        elif isinstance(value, (dict, list)):
            normalized[key] = json.dumps(value)

        # Convert bool → Yes/No
        elif isinstance(value, bool):
            normalized[key] = "Yes" if value else "No"

        # Convert numbers → string (safe for schema)
        elif isinstance(value, (int, float)):
            normalized[key] = str(value)

        else:
            normalized[key] = str(value)

    return normalized


class DataGeneratorAgent:
    """Agent 1: Generates company data using LLM."""

    def __init__(self):
        self.logger = agent_logger
        self.llm_client = llm_client

    def generate_all_parameters(self, company_name: str) -> CompanyDataWithValidation:

        self.logger.info(f"🚀 Agent 1: Starting data generation for {company_name}")

        start_time = time.time()

        try:

            raw_data = self.llm_client.generate_company_data(
                company_name=company_name,
                parameters=COMPANY_PARAMETERS
            )

            # Normalize output
            normalized_data = normalize_for_schema(raw_data)

            company_data = CompanyData(**normalized_data)

            self.logger.info(
                f"✅ Agent 1: Successfully created CompanyData for {company_name}"
            )

            result = CompanyDataWithValidation(
                data=company_data,
                validation_results=[],
                is_valid=True,
                regeneration_count=0
            )

            processing_time = time.time() - start_time

            self.logger.info(
                f"✅ Agent 1: Data generation completed for {company_name} "
                f"in {processing_time:.2f}s"
            )

            return result

        except Exception as e:

            self.logger.error(
                f"❌ Agent 1: Error generating data for {company_name}: {str(e)}"
            )

            raise

    def regenerate_parameters(
        self,
        company_name: str,
        failed_parameters: List[str],
        current_data: Dict[str, Any],
        validation_errors: Dict[str, str]
    ) -> Dict[str, Any]:

        self.logger.info(
            f"🔄 Agent 1: Regenerating {len(failed_parameters)} parameters for {company_name}"
        )

        regenerated = {}

        for param in failed_parameters:

            try:

                error_msg = validation_errors.get(param, "Validation failed")

                new_value = self.llm_client.regenerate_parameter(
                    company_name=company_name,
                    parameter=param,
                    context=current_data,
                    validation_error=error_msg
                )

                normalized = normalize_for_schema({param: new_value})

                regenerated[param] = normalized[param]

                self.logger.info(f"✅ Regenerated: {param}")

            except Exception as e:

                self.logger.error(
                    f"❌ Failed regenerating {param}: {str(e)}"
                )

                regenerated[param] = current_data.get(param)

        return regenerated


# Global agent instance
data_generator_agent = DataGeneratorAgent()