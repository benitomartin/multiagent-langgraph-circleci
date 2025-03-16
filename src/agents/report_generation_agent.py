from src.models.schemas import FinalReport, ResearchState
from src.utils.chain_builder import ChainBuilder
from src.utils.error_handler import ErrorHandler
from src.utils.prompt_templates import PromptTemplates


class ReportGenerationAgent:
    def __init__(self, llm):
        self.chain_builder = ChainBuilder(llm)

    def execute(self, state: ResearchState) -> ResearchState:
        summary = state.get("summarized_content")
        query = state.get("query")

        if not summary or not query:
            return {**state, "errors": ["Report generation agent error: Missing required content"]}

        chain = self.chain_builder.build(
            prompt_template=PromptTemplates.report_generation_prompt(),
            input_vars=["query", "summary"],
            model=FinalReport
        )

        try:
            final_report = chain.invoke({"query": query, "summary": summary})
            final_report = final_report.model_dump()

            # Print the final report
            print("\n======= FINAL REPORT =======\n")
            print(final_report["report"])
            print("\n============================\n")

            return {**state, "final_report": final_report["report"]}
        except Exception as e:
            return ErrorHandler.add_error(state, f"Report generation agent error: {str(e)}")
