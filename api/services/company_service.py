"""
Company Service
Triggers research pipeline and returns company data.
"""

from typing import Dict, Any, Optional
from agents.agent_3_normalizer import supabase_normalizer
from api.services.research_service import research_service
import logging

logger = logging.getLogger(__name__)


class CompanyService:

    async def get_company(self, company_name: str) -> Optional[Dict[str, Any]]:

        try:

            # ALWAYS run research pipeline
            logger.info(f"Running research pipeline for {company_name}")

            await research_service.run_research(company_name)

            # AFTER pipeline completes → fetch DB
            result = supabase_normalizer.get_validated_data_by_company(company_name)

            return result

        except Exception as e:

            logger.error(f"Error fetching company {company_name}: {str(e)}")
            return None


company_service = CompanyService()