
import time
import pytest
from logger_config import logger
from helpers import login
from pages.repository_page import RepositoryPage, RepositoryPage
from config import GITHUB_USERNAME, GITHUB_PASSWORD, GITHUB_BASE_URL
from playwright.sync_api import expect
import re
from helpers import login, test_data


# ========================= Test 1: Create Repository =========================

@pytest.mark.order(1)
def test_create_repository(page):
    login(page)
    repo_name, desc = test_data(page)

    logger.info("========================= Test 1: Create Repository Started =========================")

    repo_page = RepositoryPage(page)
    repo_page.navigate_to_creation_page()
    repo_page.fill_repository_details(repo_name, desc)
    repo_page.submit_creation()
    repo_page.verify_creation_success(repo_name)

    logger.info(f"✅ Repository created: {repo_name}")
    logger.info("========================= Test 1: Create Repository Completed =========================")
# ========================= Test 2: Update Repository Settings =========================

@pytest.mark.order(2)
def test_repository_settings(page):
    login(page)
    repo_name, desc = test_data(page)

    logger.info("🔧 Starting repository settings update flow")
    repo_page = RepositoryPage(page)
    repo_page.navigate_to_creation_page()
    logger.info("Naviagted to repository creation flow page")
    repo_page.fill_repository_details(repo_name, desc)
    logger.info("Added repo name and description")
    repo_page.submit_creation()
    logger.info("clicked on create repository button")
    repo_page.navigate_to_settings()
    logger.info("Navigated to settings page")
    repo_page.update_visibility_to_private()
    logger.info("Updated repository settings from Public to Private")

    logger.info(f"✅ Repository visibility updated: {repo_name}")
    logger.info("✅ test_repository_settings completed")

# ========================= Test 3: Delete Matching Repositories =========================


@pytest.mark.order(3)
def test_delete_repository(page):
    login(page)
    logger.info("🗑️ Starting repository deletion flow")

    repo_page = RepositoryPage(page)
    pattern = r"ui-repo-(175984[2-9]\d*|175985\d+|\d{7,})"
    deleted_count = repo_page.delete_matching_repositories(pattern)

    logger.info(f"🧹 Total repositories deleted: {deleted_count}")
    logger.info("✅ test_delete_repository completed")
