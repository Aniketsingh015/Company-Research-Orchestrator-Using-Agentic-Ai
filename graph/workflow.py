"""
LangGraph workflow for orchestrating the multi-agent system.
Includes Agent 3 for Supabase integration.
"""

from typing import Dict, Any
from langgraph.graph import StateGraph, END
from graph.state import AgentState, create_initial_state
from agents.agent_1_generator import data_generator_agent
from agents.agent_2_validator import validator_agent
from agents.agent_3_normalizer import supabase_normalizer
from utils.logger import main_logger
from config.settings import settings
import time


class CompanyResearchWorkflow:
    """LangGraph workflow for company research agents."""

    def __init__(self):
        self.logger = main_logger
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:

        workflow = StateGraph(AgentState)

        workflow.add_node("generate_data", self._generate_data_node)
        workflow.add_node("push_raw_data", self._push_raw_data_node)
        workflow.add_node("validate_data", self._validate_data_node)
        workflow.add_node("push_validated_data", self._push_validated_data_node)
        workflow.add_node("save_results", self._save_results_node)

        workflow.set_entry_point("generate_data")

        workflow.add_edge("generate_data", "push_raw_data")
        workflow.add_edge("push_raw_data", "validate_data")

        workflow.add_conditional_edges(
            "validate_data",
            self._should_regenerate,
            {
                "regenerate": "validate_data",
                "finalize": "push_validated_data",
                "end": END
            }
        )

        workflow.add_edge("push_validated_data", "save_results")
        workflow.add_edge("save_results", END)

        return workflow.compile()

    def _generate_data_node(self, state: AgentState) -> Dict[str, Any]:

        self.logger.info(f"📝 Node: generate_data for {state['company_name']}")

        try:
            state["status"] = "generating"
            state["workflow_start_time"] = time.time()

            start_time = time.time()

            generated_data = data_generator_agent.generate_all_parameters(
                company_name=state["company_name"]
            )

            generation_time = time.time() - start_time

            state["generated_data"] = generated_data
            state["generation_time"] = generation_time

            self.logger.info(
                f"✅ Data generation completed in {generation_time:.2f}s"
            )

        except Exception as e:
            self.logger.error(f"❌ Error in generate_data: {str(e)}")
            state["error"] = str(e)
            state["status"] = "failed"

        return state

    def _push_raw_data_node(self, state: AgentState) -> Dict[str, Any]:

        self.logger.info(f"📤 Node: push_raw_data for {state['company_name']}")

        try:

            generated = state.get("generated_data")

            if generated and generated.data:

                result = supabase_normalizer.push_raw_data(
                    company_data=generated.data,
                    company_name=state["company_name"],
                    llm_source=settings.llm_provider,
                    processing_time=state.get("generation_time", 0.0)
                )

                if result.get("success"):

                    if not state.get("raw_data_ids"):
                        state["raw_data_ids"] = []

                    state["raw_data_ids"].append(result["id"])

                    self.logger.info(
                        f"✅ Agent 3: Raw data inserted (ID: {result['id']})"
                    )

                else:
                    self.logger.warning(
                        f"⚠️ Agent 3 raw push failed: {result.get('error')}"
                    )

            else:
                self.logger.warning("⚠️ No generated data available to push")

        except Exception as e:
            self.logger.warning(f"⚠️ Agent 3 push error: {str(e)}")

        return state

    def _validate_data_node(self, state: AgentState) -> Dict[str, Any]:

        self.logger.info(f"🔍 Node: validate_data for {state['company_name']}")

        try:

            if not state.get("generated_data"):
                self.logger.error("❌ No generated data available for validation")
                state["error"] = "No generated data"
                state["status"] = "failed"
                return state

            state["status"] = "validating"

            start_time = time.time()

            validated_data = validator_agent.validate_and_regenerate(
                company_data_with_validation=state["generated_data"],
                company_name=state["company_name"]
            )

            validation_time = time.time() - start_time

            state["validated_data"] = validated_data
            state["validation_passed"] = validated_data.is_valid
            state["regeneration_count"] = validated_data.regeneration_count
            state["validation_time"] = validation_time

            total_time = state.get("generation_time", 0) + validation_time
            state["total_processing_time"] = total_time

            validation_report = validator_agent.create_validation_report(
                company_name=state["company_name"],
                test_results=validated_data.validation_results
            )

            state["validation_report"] = validation_report

            if state["regeneration_count"] >= settings.max_regeneration_attempts:
                state["max_attempts_reached"] = True

            self.logger.info(
                f"✅ Validation completed (passed: {state['validation_passed']})"
            )

        except Exception as e:
            self.logger.error(f"❌ Error in validate_data: {str(e)}")
            state["error"] = str(e)
            state["status"] = "failed"

        return state

    def _should_regenerate(self, state: AgentState) -> str:

        if state.get("error"):
            return "end"

        if state.get("validation_passed"):
            return "finalize"

        if state.get("max_attempts_reached"):
            self.logger.warning(
                "⚠️ Max regeneration attempts reached — finalizing anyway"
            )
            return "finalize"

        self.logger.info("🔄 Validation failed — retrying validation")

        state["status"] = "regenerating"

        return "regenerate"

    def _push_validated_data_node(self, state: AgentState) -> Dict[str, Any]:

        self.logger.info(
            f"📤 Node: push_validated_data for {state['company_name']}"
        )

        try:

            state["status"] = "pushing_to_supabase"

            validated = state.get("validated_data")

            if validated and validated.data:

                result = supabase_normalizer.push_validated_data(
                    company_data_with_validation=validated,
                    company_name=state["company_name"],
                    processing_time=state.get("total_processing_time", 0.0),
                    raw_data_ids=state.get("raw_data_ids", [])
                )

                state["supabase_result"] = result

                if result.get("success"):

                    self.logger.info(
                        f"✅ Agent 3: Validated data inserted (ID: {result['id']})"
                    )

                    state["supabase_success"] = True

                else:

                    state["supabase_success"] = False
                    state["supabase_error"] = result.get("error")

            else:

                self.logger.error("❌ No validated data available to push")
                state["supabase_success"] = False

        except Exception as e:

            self.logger.error(f"❌ Supabase push error: {str(e)}")

            state["supabase_success"] = False
            state["supabase_error"] = str(e)

        return state

    def _save_results_node(self, state: AgentState) -> Dict[str, Any]:

        self.logger.info(f"💾 Node: save_results for {state['company_name']}")

        try:

            state["status"] = "saving"

            data_path = validator_agent.save_validated_data(
                company_data_with_validation=state["validated_data"],
                company_name=state["company_name"]
            )

            state["data_file_path"] = str(data_path)

            report_path = validator_agent.save_validation_report(
                validation_report=state["validation_report"],
                company_name=state["company_name"]
            )

            state["report_file_path"] = str(report_path)

            total_runtime = time.time() - state.get("workflow_start_time", time.time())
            state["workflow_runtime"] = total_runtime

            if state.get("supabase_success"):
                state["status"] = "completed_with_supabase"
            else:
                state["status"] = "completed_excel_only"

            self.logger.info(
                f"✅ Workflow completed in {total_runtime:.2f}s"
            )

        except Exception as e:

            self.logger.error(f"❌ Error saving results: {str(e)}")

            state["error"] = str(e)
            state["status"] = "failed"

        return state

    def run(self, company_name: str) -> AgentState:

        self.logger.info(f"🚀 Starting workflow for company: {company_name}")

        initial_state = create_initial_state(company_name)

        final_state = self.graph.invoke(initial_state)

        self.logger.info(
            f"🏁 Workflow completed with status: {final_state['status']}"
        )

        return final_state


company_research_workflow = CompanyResearchWorkflow()