from lambda_function.lambda_handler import lambda_handler


def test_lambda_handler():
    # Create a mock event to simulate an AWS Lambda invocation
    event = {
        "query": "What is the capital of France?"
    }

    # Call the lambda_handler function
    response = lambda_handler(event, None)

    # Print the response for testing
    print("\nResponse:\n\n", response["body"]["final_report"])


    # Assertions to validate the response
    assert response["statusCode"] == 200
    assert "final_report" in response["body"]
    assert "errors" in response["body"]
    assert isinstance(response["body"]["final_report"], str)
    assert isinstance(response["body"]["errors"], list)

