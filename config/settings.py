import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

# Model Settings
FACT_CHECK_MODEL = "gpt-4o-mini"
SUMMARIZATION_MODEL = "anthropic.claude-3-haiku-20240307-v1:0"

# Workflow Settings
CONFIDENCE_THRESHOLD = 0.95
MAX_RETRIES = 1
ADD_MAX_RESULTS = 2

# Validate required environment variables
if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY environment variable is not set")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
