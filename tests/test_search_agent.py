from src.agents.search_agent import SearchAgent
from config.settings import SERPER_API_KEY

def test_search_agent():
    """
    Tests the SearchAgent with a mock query.
    """

    # Initialize the agent
    agent = SearchAgent(SERPER_API_KEY)

    # Test search execution
    results = agent.execute({"query": "What is CircleCI?"})

    # Assertions
    assert isinstance(results, dict)
    assert "search_results" in results
    assert isinstance(results["search_results"], list)
