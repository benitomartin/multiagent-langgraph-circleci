class PromptTemplates:
    """Centralized class for all prompt templates used in the research workflow."""

    @staticmethod
    def summarization_prompt():
        return (
            "You are a summarization agent. Summarize the following search results:\n\n"
            "{results}\n\n"
            "Provide a structured summary of the key information about the benefits "
            "and main points.\n"
        )

    @staticmethod
    def fact_checking_prompt():
        return (
            "You are a fact-checking agent. Review the following summary and verify it "
            "against the original search results:\n\n"
            "Summary: {summary}\n\n"
            "Original results: {original_results}\n\n"
            "Identify any inaccuracies or inconsistencies. Provide a confidence score "
            "indicating how reliable your fact check is."
        )

    @staticmethod
    def report_generation_prompt():
        return (
            "You are a report generation agent. Create a comprehensive research report "
            "based on the following information:\n\n"
            "Original query: {query}\n\n"
            "Content summary: {summary}\n\n"
            "Format the report with markdown, including appropriate headings, bullet "
            "points, and sections. The report should be informative, well-structured, "
            "and directly address the original query.\n"
        )
