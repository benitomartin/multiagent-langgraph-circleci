import json

from lambda_function.lambda_handler import lambda_handler


def test_lambda_handler():
    # Create a mock event to simulate an AWS Lambda invocation
    event = {
        "query": "What is the capital of France?"
    }

    # Call the lambda_handler function
    response = lambda_handler(event, None)

    # Print the response for testing
    print("\nResponse:\n\n", json.loads(response["body"])["final_report"])


    # Assertions to validate the response
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "final_report" in body
    assert "errors" in body

if __name__ == "__main__":
    test_lambda_handler()
