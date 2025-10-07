# config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_PASSWORD = os.getenv("GITHUB_PASSWORD")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
TEST_REPO_NAME = "qa-automation-test-repo"
GITHUB_BASE_URL = "https://github.com"
GITHUB_API_URL = "https://api.github.com"