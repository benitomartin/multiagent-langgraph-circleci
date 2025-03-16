from src.models.schemas import ResearchState, Summary
from src.utils.chain_builder import ChainBuilder
from src.utils.prompt_templates import PromptTemplates


class SummarizationAgent:
    def __init__(self, llm):
        self.chain_builder = ChainBuilder(llm)

    def execute(self, state: ResearchState) -> ResearchState:
        search_results = state.get("search_results", [])

        print(f"Summarization agent executing with {len(search_results)} search results")

        # Increment the summarization attempt counter
        summarization_attempts = state.get("summarization_attempts", 0)
        state["summarization_attempts"] = summarization_attempts + 1

        if not search_results:
            errors = state.get("errors", [])
            errors.append("Summarization agent error: No search results to summarize")
            return {**state, "errors": errors}

        summary_chain = self.chain_builder.build(
            prompt_template=PromptTemplates.summarization_prompt(),
            input_vars=["results"],
            model=Summary
        )
        try:
            # Format the search results as a string for the prompt
            formatted_results = "\n\n".join([
                f"Title: {result['title']}\nURL: {result['url']}\nSnippet: {result['snippet']}"
                for result in search_results
            ])

            # Invoke the chain with the formatted results
            summary_obj = summary_chain.invoke({"results": formatted_results})

            # Format the summary object into a string
            summary_str = "# Summary\n\n"
            summary_str += f"\n\n## Key Points\n{summary_obj.main_points}\n"
            summary_str += f"\n\n## Benefits\n{summary_obj.benefits}\n"
            summary_str += f"\n\n## Conclusion\n{summary_obj.conclusion}\n"

            return {**state, "summarized_content": summary_str}

        except Exception as e:
            errors = state.get("errors", [])
            errors.append(f"Summarization agent error: {str(e)}")
            return {**state, "errors": errors}
