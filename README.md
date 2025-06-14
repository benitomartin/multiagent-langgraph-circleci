# Multi-Agent LangGraph Research System

<div align="center">
    <img src="images/collaborative _multi_agent_ai_system_with_langgraph.png" alt="Multi-Agent LangGraph Architecture">
</div>

<div align="center">
    <a href="https://www.python.org/downloads/release/python-3120/"><img src="https://img.shields.io/badge/python-3.12+-blue.svg"/></a>
    <a href="https://github.com/astral-sh/uv"><img src="https://img.shields.io/badge/uv-Package%20Manager-blue"/></a>
    <a href="https://langchain-ai.github.io/langgraph/"><img src="https://img.shields.io/badge/LangGraph-Multi%20Agent-ff6b6b"/></a>
    <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-Containerized-blue"/></a>
    <a href="https://aws.amazon.com/lambda/"><img src="https://img.shields.io/badge/AWS%20Lambda-Serverless-orange"/></a>
</div>
<div align="center">
    <a href="https://pydantic.dev/"><img src="https://img.shields.io/badge/Pydantic-Data%20Validation-e92063"/></a>
    <a href="https://github.com/features/actions"><img src="https://img.shields.io/badge/GitHub%20Actions-CI%20CD-2088ff"/></a>
    <a href="http://mypy-lang.org/"><img src="http://www.mypy-lang.org/static/mypy_badge.svg"/></a>
    <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/badge/Ruff-Linting%20Formatting-red"/></a>
    <a href="https://docs.pytest.org/"><img src="https://img.shields.io/badge/pytest-enabled-brightgreen"/></a>
    <a href="https://github.com/pre-commit/pre-commit"><img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen"/></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg"/></a>
</div>
<p align="center">
    <em>A multi-agent research system using LangGraph for automated research and report generation</em>
</p>

---

Build, test, and deploy a multi-agent AI system using LangGraph, Docker, AWS Lambda, and CircleCI. The system uses a research-driven AI workflow where different agents,such as fact-checking, summarization, and search agents, work together seamlessly. This application is packaged into a Docker container, deployed to AWS Lambda, and the entire pipeline is run using CircleCI.

The project has been developed as part of the following [blog](https://circleci.com/blog/end-to-end-testing-and-deployment-of-a-multi-agent-ai-system/)

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Configuration](#configuration)
  - [Local Execution](#local-execution)
  - [AWS Lambda Deployment](#aws-lambda-deployment)
  - [AWS Lambda Invocation](#aws-lambda-invocation)
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

### Configuration

The following parameters can be adjusted in `config/settings.py`:

- `CONFIDENCE_THRESHOLD`: Threshold for confidence in fact-checking
- `MAX_RETRIES`: Maximum number of retries for the search agent
- `ADD_MAX_RESULTS`: Number of search results to add in each retry
- `FACT_CHECK_MODEL`: Model used for fact-checking (default: "gpt-4-mini")
- `SUMMARIZATION_MODEL`: Model used for summarization (default: "anthropic.claude-3-haiku")

### Local Execution

To run the research graph locally:

```bash
uv run src/graph/research_graph.py \
   --query "What are the benefits of using AWS Cloud Services?" \
   --confidence-threshold 0.85 \
   --max-retries 3 \
   --add-max-results 2
```

### AWS Lambda Deployment

Build and deploy the Docker image with the lambda function:

```bash
chmod +x build_deploy.sh
./build_deploy.sh
```

### AWS Lambda Invocation

To invoke the deployed Lambda function add your region and run the following command:

```bash
aws lambda invoke \
    --function-name langgraph-lambda-function \
    --payload '{"query": "What are the benefits of using CircleCI?"}' \
    --region <your_region> \
    --cli-binary-format raw-in-base64-out \
    response.json && \
    cat response.json | jq
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
