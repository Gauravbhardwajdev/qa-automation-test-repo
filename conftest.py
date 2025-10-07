import pytest
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import logger from config
from logger_config import logger

@pytest.fixture(scope="session")
def env_config():
    return {
        "username": os.getenv("GITHUB_USERNAME"),
        "token": os.getenv("GITHUB_TOKEN"),
        "repo_name": "qa-automation-test-repo",
        "base_url": "https://github.com",
        "api_url": "https://api.github.com"
    }

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(scope="function")
def logged_in_page(browser):
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()
    yield page
    context.close()