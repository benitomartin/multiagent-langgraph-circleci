from src.models.schemas import ResearchState


class StopWorkflowAgent:
    def execute(self, state: ResearchState) -> ResearchState:
        """Stops the workflow and displays the final confidence score"""
        state.get("fact_checked_results", {}).get("confidence_score", "N/A")

        # Add the message to the errors list
        errors = state.get("errors", [])

        return {**state, "errors": errors}
