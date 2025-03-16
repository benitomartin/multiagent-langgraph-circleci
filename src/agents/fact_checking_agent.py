import json

from config.settings import ADD_MAX_RESULTS, CONFIDENCE_SCORE, MAX_RETRIES
from src.models.schemas import FactCheckResult, ResearchState
from src.utils.chain_builder import ChainBuilder
from src.utils.error_handler import ErrorHandler
from src.utils.prompt_templates import PromptTemplates


class FactCheckingAgent:
    def __init__(self, llm):
        self.chain_builder = ChainBuilder(llm)

    def execute(self, state: ResearchState) -> ResearchState:
        summary = state.get("summarized_content")
        search_results = state.get("search_results", [])

        # Increment fact-checking attempt counter
        fact_check_attempts = state.get("fact_check_attempts", 0)
        state["fact_check_attempts"] = fact_check_attempts + 1

        if not summary or not search_results:
            return {**state, "errors": ["Fact-checking agent error: Missing data"]}

        fact_check_chain = self.chain_builder.build(
            prompt_template=PromptTemplates.fact_checking_prompt(),
            input_vars=["summary", "original_results"],
            model=FactCheckResult
        )
        try:
            results_text = json.dumps(search_results, indent=2)
            fact_check_results = fact_check_chain.invoke({
                "summary": summary,
                "original_results": results_text,
            })

            print(f"Fact-checking agent completed review. Accurate: {fact_check_results.is_accurate}")
            print(f"Confidence score: {fact_check_results.confidence_score}")

            fact_check_results = fact_check_results.model_dump()

            confidence_score = fact_check_results.get("confidence_score", 1.0)
            retry_count = state.get("search_retries", 0)
            max_results = state.get("max_results", 3)
            print("Retry Count:", retry_count)
            print("Max Results:", max_results)

            if confidence_score < CONFIDENCE_SCORE:
                if retry_count < MAX_RETRIES:
                    state["search_retries"] = retry_count + 1

                    # Only increase max_results if we're NOT about to hit the retry cap
                    if state["search_retries"] < MAX_RETRIES:
                        print(f"Retrying search number {state['search_retries']}")

                        state["max_results"] = max_results + ADD_MAX_RESULTS
                        print(f"Increasing max_results to: {state['max_results']}")

            state["fact_checked_results"] = fact_check_results
            return state

        except Exception as e:
            return ErrorHandler.add_error(state, f"Fact-checking agent error: {str(e)}")
