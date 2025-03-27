from typing import Any, Dict, List, TypedDict

from pydantic import BaseModel, Field


class ResearchState(TypedDict):
    query: str
    search_results: List[Dict[str, Any]]
    summarized_content: str
    fact_checked_results: Dict[str, Any]
    final_report: str
    errors: List[str]
    fact_check_attempts: int
    summarization_attempts: int
    max_results: int
    search_retries: int

class SearchResult(BaseModel):
    title: str = Field(description="The title of the search result")
    url: str = Field(description="The URL of the search result")
    snippet: str = Field(description="A brief excerpt or summary of the search result")
class Summary(BaseModel):
    main_points: str = Field(description="List of key points from the search results")
    benefits: str = Field(description="List of specific benefits of the search results")
    conclusion: str = Field(description="A concise conclusion about the search results")

class FactCheckResult(BaseModel):
    is_accurate: bool = Field(description="Whether the summary is factually accurate based on the search results")
    issues: List[str] = Field(description="List of inaccuracies or inconsistencies found in the summary")
    corrected_facts: List[str] = Field(description="List of corrections for any identified issues")
    confidence_score: float = Field(description="Confidence score from 0.0 to 1.0 indicating reliability of the fact check")

class FinalReport(BaseModel):
    report: str = Field(description="The final research report generated from the summary and fact-check results")
