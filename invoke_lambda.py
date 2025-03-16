import json
import os

import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

LAMBDA_FUNCTION_NAME = os.getenv("LAMBDA_FUNCTION_NAME")
AWS_REGION = os.getenv("AWS_REGION")


# Create a Lambda client
client = boto3.client('lambda', region_name=AWS_REGION)

# Input payload
payload = {
    "query": "What are the benefits of using AWS Cloud Services?"
}

# Invoke the Lambda function
response = client.invoke(
    FunctionName=LAMBDA_FUNCTION_NAME,
    Payload=json.dumps(payload)
)

# Read and print the response
response_payload = json.loads(response['Payload'].read().decode())
print("\n===== FINAL REPORT =====:\n\n")
print(response_payload['body']["final_report"])
