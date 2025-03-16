import json
import logging
import os

from config.settings import (
    ADD_MAX_RESULTS,
    CONFIDENCE_SCORE,
    MAX_RETRIES,
    OPENAI_API_KEY,
    SERPER_API_KEY,
)
from src.graph.research_graph import build_research_graph

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    # Log environment variables (masked for security)
    logger.info("SERPER_API_KEY present: %s", bool(os.getenv("SERPER_API_KEY")))
    logger.info("OPENAI_API_KEY present: %s", bool(os.getenv("OPENAI_API_KEY")))
    logger.info("AWS_ACCESS_KEY_ID present: %s", bool(os.getenv("AWS_ACCESS_KEY_ID")))
    logger.info("AWS_SECRET_ACCESS_KEY present: %s", bool(os.getenv("AWS_SECRET_ACCESS_KEY")))

    # Extract parameters from event with defaults
    query = event.get("query", "What are the benefits of using AWS Cloud Services?")
    confidence_score = event.get("confidence_score", CONFIDENCE_SCORE)
    max_retries = event.get("max_retries", MAX_RETRIES)
    add_max_results = event.get("add_max_results", ADD_MAX_RESULTS)

    # Validate parameters
    if not 0 <= confidence_score <= 1:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Confidence score must be between 0 and 1"})
        }
    if max_retries < 0:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Max retries must be non-negative"})
        }
    if add_max_results < 1:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Additional max results must be positive"})
        }

    # Build the research graph with custom parameters
    graph = build_research_graph(
        SERPER_API_KEY,
        OPENAI_API_KEY,
        confidence_score=confidence_score,
        max_retries=max_retries,
        add_max_results=add_max_results
    )

    # Run the graph
    result = graph.invoke({
        "query": query,
        "search_results": [],
        "summarized_content": "",
        "fact_checked_results": {},
        "final_report": "",
        "errors": [],
        "fact_check_attempts": 0,
        "summarization_attempts": 0,
        "max_results": 3,
        "search_retries": 0
    })

    return {
        "statusCode": 200,
        "body": {
            "final_report": result.get("final_report", ""),
            "errors": result.get("errors", [])
        }
    }
