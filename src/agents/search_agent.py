from langchain_community.utilities import GoogleSerperAPIWrapper


class SearchAgent:
    def __init__(self, serper_api_key: str):
        self.search = GoogleSerperAPIWrapper(serper_api_key=serper_api_key, k=3)

    def execute(self, state: dict, k: int = 3) -> dict:
        query = state.get("query")
        max_results = state.get("max_results", k)

        if not query:
            return {**state, "errors": ["Search agent error: No query provided"]}

        try:
            self.search.k = max_results
            raw_results = self.search.results(query=query)

            results = [
                {
                    "title": r.get("title", ""),
                    "url": r.get("link", ""),
                    "snippet": r.get("snippet", ""),
                }
                for r in raw_results.get("organic", [])
            ]
            print(f"Search agent found {len(results)} results with max results equal to {max_results}")
            print(f"Search Results: {results}")

            return {**state, "search_results": results}
        except Exception as e:
            return {**state, "errors": [f"Search agent error: {str(e)}"]}
