"""
Agent 3: Supabase Normalizer
Pushes data to Supabase database.
"""

import json
from typing import Dict, Any, Optional, List
from supabase import create_client, Client

from models.company_schema import CompanyData, CompanyDataWithValidation
from config.settings import settings
from utils.logger import agent_logger


class SupabaseNormalizer:

    def __init__(self):
        self.logger = agent_logger

        self.supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )

        self.raw_table = settings.raw_data_table
        self.validated_table = settings.validated_data_table


    # --------------------------------------------------
    # helper
    # --------------------------------------------------

    def _prepare_data_for_insert(self, data_dict: Dict[str, Any]) -> Dict[str, Any]:

        prepared = {}

        for key, value in data_dict.items():

            if value is None:
                prepared[key] = None
                continue

            if isinstance(value, (list, dict)):
                prepared[key] = json.dumps(value)
                continue

            if isinstance(value, bool):
                prepared[key] = value
                continue

            if isinstance(value, str):

                digits = "".join(c for c in value if c.isdigit())

                if digits:
                    number = int(digits)

                    if number > 2147483647:
                        prepared[key] = value
                    else:
                        prepared[key] = number

                else:
                    prepared[key] = value

                continue

            prepared[key] = value

        return prepared


    # --------------------------------------------------
    # RAW DATA INSERT
    # --------------------------------------------------

    def push_raw_data(
        self,
        company_data: CompanyData,
        company_name: str,
        llm_source: str = "groq",
        processing_time: float = 0.0
    ):

        try:

            data_dict = company_data.model_dump()
            insert_data = self._prepare_data_for_insert(data_dict)

            insert_data.update({
                "company_name": company_name,
                "llm_source": llm_source,
                "processing_time_seconds": processing_time,
                "status": "raw"
            })

            result = self.supabase.table(self.raw_table).insert(insert_data).execute()

            return result.data

        except Exception as e:
            self.logger.error(f"Raw insert failed: {str(e)}")
            return None


    # --------------------------------------------------
    # VALIDATED DATA INSERT
    # --------------------------------------------------

    def push_validated_data(
        self,
        company_data_with_validation: CompanyDataWithValidation,
        company_name: str,
        processing_time: float = 0.0,
        raw_data_ids: Optional[List[str]] = None
    ):

        try:

            data_dict = company_data_with_validation.data.model_dump()

            insert_data = self._prepare_data_for_insert(data_dict)

            insert_data.update({
                "company_name": company_name,
                "validation_passed": company_data_with_validation.is_valid,
                "regeneration_count": company_data_with_validation.regeneration_count,
                "processing_time_seconds": processing_time,
            })

            result = (
                self.supabase
                .table(self.validated_table)
                .upsert(insert_data, on_conflict="company_name")
                .execute()
            )

            return result.data

        except Exception as e:
            self.logger.error(f"Validated insert failed: {str(e)}")
            return None


    # --------------------------------------------------
    # DB READ
    # --------------------------------------------------

    def get_validated_data_by_company(self, company_name: str):

        try:

            result = (
                self.supabase
                .table(self.validated_table)
                .select("*")
                .eq("company_name", company_name)
                .execute()
            )

            if result.data:
                return result.data[0]

            return None

        except Exception as e:
            self.logger.error(f"Fetch error: {str(e)}")
            return None


supabase_normalizer = SupabaseNormalizer()