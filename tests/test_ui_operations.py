import re
import time

import pytest
from playwright.sync_api import expect
from selenium.webdriver.common.devtools.v137.debugger import pause

from conftest import logged_in_page
from logger_config import logger
from pages.repository_page import RepositoryPage, RepositoryPage
from helpers import login, test_data

# ========================= Test 1: Create Repository =========================

# ========================= Test 1: Create Repository =========================

@pytest.mark.order(1)
def test_create_repository(page):
    logger.info("🚀 Test 1: Starting repository creation flow")
    login(page)
    repo_name, desc = test_data(page)

    repo_page = RepositoryPage(page)
    logger.info("🌐 Navigating to repository creation page")
    repo_page.navigate_to_creation_page()

    logger.info("📝 Filling repository details")
    repo_page.fill_repository_details(repo_name, desc)

    logger.info("📤 Submitting repository creation form")
    repo_page.submit_creation()

    logger.info("🔍 Verifying repository creation success")
    repo_page.verify_creation_success(repo_name)

    logger.info(f"✅ Repository created successfully: {repo_name}")
    logger.info("🏁 Test 1: Repository creation flow completed")


# ========================= Test 2: Update Repository Settings =========================

@pytest.mark.order(2)
def test_repository_settings(page):
    logger.info("⚙️ Test 2: Starting repository settings update flow")
    login(page)
    repo_name, desc = test_data(page)

    repo_page = RepositoryPage(page)
    logger.info("🌐 Navigating to repository creation page")
    repo_page.navigate_to_creation_page()

    logger.info("📝 Filling repository details")
    repo_page.fill_repository_details(repo_name, desc)

    logger.info("📤 Submitting repository creation form")
    repo_page.submit_creation()

    logger.info("🔧 Navigating to repository settings")
    repo_page.navigate_to_settings()

    logger.info("🔒 Updating visibility to private")
    repo_page.update_visibility_to_private()

    logger.info(f"✅ Repository visibility updated to private: {repo_name}")
    logger.info("🏁 Test 2: Repository settings update completed")


# ========================= Test 3: Delete Matching Repositories =========================

@pytest.mark.order(3)
def test_delete_repository(page):
    logger.info("🗑️ Test 3: Starting repository deletion flow")
    login(page)

    repo_page = RepositoryPage(page)
    pattern = r"ui-repo-(175984[2-9]\d*|175985\d+|\d{7,})"
    deleted_count = repo_page.delete_matching_repositories(pattern)

    logger.info(f"✅ Total repositories deleted: {deleted_count}")
    logger.info("🏁 Test 3: Repository deletion flow completed")


# ========================= Test 4: File Upload =========================

@pytest.mark.order(4)
def test_file_upload(page):
    logger.info("📦 Test 4: Starting file upload flow")
    login(page)
    repo_name, desc = test_data(page)
    logger.info(f"📝 Repo name: {repo_name}, Description: {desc}")

    repo_page = RepositoryPage(page)
    logger.info("🌐 Navigating to repository creation page")
    repo_page.navigate_to_creation_page()

    logger.info("📝 Filling repository details")
    repo_page.fill_repository_details(repo_name, desc)

    logger.info("📤 Submitting repository creation form")
    repo_page.submit_creation()
    logger.info("✅ Repository created successfully")

    logger.info("📁 Uploading file and committing")
    file_path = "utils/Uploadable File/Test.txt"
    summary = "Test File Upload"
    description = "Test.txt file for UI validation"
    returned_summary = repo_page.upload_and_commit_file(file_path, summary, description)
    logger.info(f"🧾 Returned commit summary: {returned_summary}")

    logger.info("🔍 Validating commit summary")
    assert returned_summary == summary, f"Commit summary mismatch: expected '{summary}', got '{returned_summary}'"
    logger.info("✅ Commit summary validated")

    logger.info("📂 Verifying uploaded file in repository")
    filename = "Test.txt"
    result = repo_page.verify_uploaded_file(filename)
    assert result == filename, f"Expected file '{filename}' to be visible, but got: {result}"
    logger.info(f"✅ File upload verification successful: {result}")

    logger.info("🏁 Test 4: File upload flow completed")


# ========================= Test 5: File Editing =========================

@pytest.mark.order(5)
def test_file_editing(page):
    logger.info("📝 Test 5: Starting file editing flow")
    login(page)

    page.goto("https://github.com/Gauravbhardwajdev?tab=repositories")
    page.wait_for_load_state("load")

    latest_repo = page.locator("li[itemprop='owns'] a[itemprop='name codeRepository']").first
    latest_repo_name = latest_repo.inner_text()
    latest_repo.click()
    logger.info(f"✅ Opened latest repository: {latest_repo_name}")

    repo_page = RepositoryPage(page)
    filename = "Test.txt"
    new_content = "This is an edited line for validation."
    commit_message = "Edited Test.txt for validation"

    logger.info("📂 Opening file in editor")
    repo_page.open_file_preview(filename)
    repo_page.open_file_in_editor()
    logger.info("✏️ Editing file content")

    repo_page.edit_file_content(new_content)
    logger.info("📤 Committing file changes")
    repo_page.commit_file_changes(commit_message)

    logger.info("🔍 Verifying updated file content")
    repo_page.verify_file_content(new_content)

    logger.info("🏁 Test 5: File editing flow completed successfully")


# ========================= Test 6: File Operation Errors =========================

@pytest.mark.order(6)
def test_upload_invalid_file_to_repo(page):
    logger.info("🧪 Test 11: Uploading file to GitHub repository")

    # Step 1: Login and open latest repo
    login(page)
    page.goto("https://github.com/Gauravbhardwajdev?tab=repositories")
    page.wait_for_load_state("load")

    latest_repo = page.locator("li[itemprop='owns'] a[itemprop='name codeRepository']").first
    latest_repo_name = latest_repo.inner_text()
    latest_repo.click()
    logger.info(f"✅ Opened latest repository: {latest_repo_name}")

    repo_page = RepositoryPage(page)
    file_path = "utils/Non Uploadable File/invalid_file.exe"
    summary = "Test invalid_file Upload"
    description = "invalid_file.exe file for UI validation"
    returned_summary = repo_page.upload_file_to_repo(file_path, summary, description)
    logger.info(f"🧾 Returned commit summary: {returned_summary}")

    logger.info("🔍 Validating commit summary")
    assert returned_summary == summary, f"Commit summary mismatch: expected '{summary}', got '{returned_summary}'"
    logger.info("✅ Commit summary validated")

    logger.info("📂 Verifying uploaded file in repository")
    filename = "invalid_file.exe"
    result = repo_page.verify_uploaded_file(filename)
    assert result == filename, f"Expected file '{filename}' to be visible, but got: {result}"
    logger.info(f"✅ File upload verification successful: {result}")

    logger.info("🏁 Test 4: File upload flow completed")



@pytest.mark.order(7)
def test_edit_without_permissions(page):
    logger.info("🧪 Test 13: Attempting to edit a file without write permissions")

    # Step 1: Navigate to a public repo you don't own
    page.goto("https://github.com/octocat/Hello-World")
    page.wait_for_load_state("load")

    # Step 2: Try to edit README.md
    logger.info("🔒 Attempting to edit README.md")
    page.goto("https://github.com/octocat/Hello-World/edit/main/README.md")

    # Step 3: Validate permission error or fork prompt
    fork_prompt = page.locator("text=You need to fork this repository to propose changes")
    permission_error = page.locator("text=You must be signed in to propose changes")

    assert fork_prompt.is_visible() or permission_error.is_visible(), "❌ No permission error or fork prompt detected"

    logger.info("✅ Permission restriction validated successfully")





