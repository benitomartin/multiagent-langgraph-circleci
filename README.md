# Multi-Agent LangGraph Research System

A multi-agent research system using LangGraph for automated research and report generation. The system uses multiple AI agents to search, summarize, fact-check, and generate comprehensive research reports on any given topic.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [AWS Lambda Deployment](#aws-lambda-deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- Multi-agent architecture using LangGraph
- Automated web search using Serper API
- Fact-checking and verification
- Report generation with structured summaries
- AWS Lambda deployment support
- Configurable confidence scores and retry mechanisms

## Prerequisites

- Python 3.12
- AWS CLI (for Lambda deployment)
- Serper API key
- OpenAI API key
- AWS Credentials (for Lambda deployment)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/benitomartin/multiagent-langgraph-circleci.git
   cd multiagent-langgraph-circleci
   ```

2. Create a virtual environment:
   ```bash
   uv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On Unix or MacOS:
     ```bash
     source .venv/bin/activate
     ```

4. Install the required packages:
   ```bash
   uv sync --all-extras
   ```

5. Create a `.env` file in the root directory:
   ```plaintext
   # API Keys
   SERPER_API_KEY=your_serper_key_here                
   OPENAI_API_KEY=your_openai_key_here                

   # AWS Configuration
   AWS_REGION=your_aws_region                          
   AWS_ACCESS_KEY_ID=your_aws_access_key              
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key          
   AWS_ACCOUNT_ID=your_aws_account_id                 
   
   # Repository and Image Configuration
   REPOSITORY_NAME=langgraph-ecr-docker-repo          
   IMAGE_NAME=langgraph-lambda-image                  
   
   # Lambda Configuration
   LAMBDA_FUNCTION_NAME=langgraph-lambda-function     
   ROLE_NAME=lambda-bedrock-role                      
   ROLE_POLICY_NAME=LambdaBedrockPolicy              
   ```

   To obtain the required API keys:
   - Serper API Key: Sign up at [Serper.dev](https://serper.dev)
   - OpenAI API Key: Sign up at [OpenAI Platform](https://platform.openai.com)
   - AWS Credentials: Create through [AWS IAM Console](https://console.aws.amazon.com/iam)

## Usage

### Local Execution

To run the research graph locally:
```bash
uv run src/graph/research_graph.py \
   --query "What are the benefits of using AWS Cloud Services?" \
   --confidence-threshold 0.85 \
   --max-retries 3 \
   --add-max-results 2
```

### Lambda Invocation

To invoke the deployed Lambda function:
```bash
aws lambda invoke \
    --function-name langgraph-lambda-function \
    --payload '{"query": "What are the benefits of using CircleCI?"}' \
    --region eu-central-1 \
    --cli-binary-format raw-in-base64-out \
    response.json && \
    cat response.json | jq
```

## Configuration

The following parameters can be adjusted in `config/settings.py`:

- `CONFIDENCE_SCORE`: Threshold for confidence in fact-checking (default: 0.8)
- `MAX_RETRIES`: Maximum number of retries for the search agent (default: 2)
- `ADD_MAX_RESULTS`: Number of search results to add in each retry (default: 2)
- `FACT_CHECK_MODEL`: Model used for fact-checking (default: "gpt-4-mini")
- `SUMMARIZATION_MODEL`: Model used for summarization (default: "anthropic.claude-3-haiku")

## AWS Lambda Deployment

Build and deploy the Docker image with the lambda function:

```bash
chmod +x build_deploy.sh
./build_deploy.sh
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
