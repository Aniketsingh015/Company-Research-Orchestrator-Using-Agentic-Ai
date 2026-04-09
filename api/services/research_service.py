"""
Research Service
Runs the multi-agent workflow.
"""

import logging
import uuid
from typing import Dict, Any

from graph.workflow import company_research_workflow

logger = logging.getLogger(__name__)


class ResearchService:

    async def start_research(
    self,
    company_name: str,
    llm_provider: str = "groq",
    async_mode: bool = False
) -> Dict[str, Any]:

        try:

            task_id = str(uuid.uuid4())

            logger.info(
                f"🚀 Starting research for {company_name} (task: {task_id})"
            )

            # Call the workflow
            result = company_research_workflow.run(company_name)

            logger.info(f"✅ Research completed for {company_name}")

            return {
                "task_id": task_id,
                "company": company_name,
                "status": "completed",
                "result": result
            }

        except Exception as e:

            logger.error(f"Research failed for {company_name}: {str(e)}")

            return {
                "company": company_name,
                "status": "failed",
                "error": str(e)
            }


research_service = ResearchService()