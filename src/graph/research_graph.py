import argparse

from langchain_aws import ChatBedrock
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from config.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_REGION,
    AWS_SECRET_ACCESS_KEY,
    FACT_CHECK_MODEL,
    SUMMARIZATION_MODEL,
    CONFIDENCE_THRESHOLD,
    MAX_RETRIES,
    ADD_MAX_RESULTS,
    OPENAI_API_KEY,
    SERPER_API_KEY,

)
from src.agents.fact_checking_agent import FactCheckingAgent
from src.agents.report_generation_agent import ReportGenerationAgent
from src.agents.search_agent import SearchAgent
from src.agents.stop_workflow_agent import StopWorkflowAgent
from src.agents.summarization_agent import SummarizationAgent
from src.models.schemas import ResearchState


def build_research_graph(serper_api_key: str = SERPER_API_KEY, 
                         openai_api_key: str = OPENAI_API_KEY,
                         confidence_threshold: float = CONFIDENCE_THRESHOLD,
                         max_retries: int = MAX_RETRIES,
                         add_max_results: int = ADD_MAX_RESULTS):
    
    # Initialize different models for Summarization and Fact-Checking agents
    fact_check_llm = ChatOpenAI(model=FACT_CHECK_MODEL, api_key=openai_api_key)
    summarization_llm = ChatBedrock(
        model_id=SUMMARIZATION_MODEL,
        model_kwargs=dict(temperature=0),
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

    # Initialize agents
    search_agent = SearchAgent(serper_api_key)
    summarization_agent = SummarizationAgent(summarization_llm)
    fact_checking_agent = FactCheckingAgent(fact_check_llm, confidence_threshold, max_retries, add_max_results)
    report_generation_agent = ReportGenerationAgent(summarization_llm)
    stop_workflow_agent = StopWorkflowAgent()

    # Define graph state
    builder = StateGraph(ResearchState)

    # Set entry point
    builder.set_entry_point("Search")

    # Add nodes
    builder.add_node("Search", search_agent.execute)
    builder.add_node("Summarize", summarization_agent.execute)
    builder.add_node("Fact Check", fact_checking_agent.execute)
    builder.add_node("Report", report_generation_agent.execute)
    builder.add_node("Stop Workflow", stop_workflow_agent.execute)

    def on_search_complete(state: ResearchState) -> str:
        return "Stop Workflow" if state.get("errors") else "Summarize"

    def on_summarization_complete(state: ResearchState) -> str:
        return "Stop Workflow" if state.get("errors") else "Fact Check"

    def on_fact_check_complete(state: ResearchState) -> str:
        fact_check_result = state.get("fact_checked_results", {})
        confidence_score = fact_check_result.get("confidence_score", 1.0)
        count = state.get("search_retries", 0)

        if state.get("errors"):
            return "Stop Workflow"

        if confidence_score < confidence_threshold:
            if count >= max_retries:
                print(f"Maximum retry attempts ({max_retries}) reached. Stopping workflow.")
                return "Stop Workflow"
            return "Search"  # Go back to search if retries are available

        return "Report"  # Proceed to report generation

    def on_report_complete(state: ResearchState) -> str:
        return "Stop Workflow" if state.get("errors") else END

    def on_stop_workflow(_state: ResearchState) -> str:
        return END

    builder.add_conditional_edges("Search", on_search_complete, {
        "Stop Workflow": "Stop Workflow",
        "Summarize": "Summarize",
    })

    builder.add_conditional_edges("Summarize", on_summarization_complete, {
        "Stop Workflow": "Stop Workflow",
        "Fact Check": "Fact Check",
    })

    builder.add_conditional_edges("Fact Check", on_fact_check_complete, {
        "Stop Workflow": "Stop Workflow",
        "Report": "Report",
        "Search": "Search",
    })

    builder.add_conditional_edges("Report", on_report_complete, {
        "Stop Workflow": "Stop Workflow",
        END: END,
    })

    builder.add_conditional_edges("Stop Workflow", on_stop_workflow, {
        END: END
    })

    return builder.compile()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Run research graph with custom parameters')
    parser.add_argument('--query', type=str, default="What are the benefits of using AWS Cloud Services?",
                      help='Research query')
    parser.add_argument('--confidence-threshold', type=float, default=CONFIDENCE_THRESHOLD,
                      help='Confidence score threshold (0-1)')
    parser.add_argument('--max-retries', type=int, default=MAX_RETRIES,
                      help='Maximum number of retries')
    parser.add_argument('--add-max-results', type=int, default=ADD_MAX_RESULTS,
                      help='Number of additional results per retry')

    args = parser.parse_args()

    graph = build_research_graph(
        SERPER_API_KEY,
        OPENAI_API_KEY,
        confidence_threshold=args.confidence_threshold,
        max_retries=args.max_retries,
        add_max_results=args.add_max_results
    )

    result = graph.invoke({"query": args.query})
    print(f"Research completed. Final report:\n{result.get('final_report', '')}")
