import re
import time
import pytest
from loguru import logger
from playwright.sync_api import expect
from selenium.webdriver.common.devtools.v139.debugger import pause

from helpers import login
from config import GITHUB_USERNAME, GITHUB_PASSWORD, GITHUB_BASE_URL


# def test_github_login_flow(page):
#     login(page)
#     logger.info("Starting GitHub login flow test")

    #  # Navigate to GitHub login
    # logger.info("Navigating to GitHub login page")
    # page.goto(f"{GITHUB_BASE_URL}/login")
    # page.click("(//a[@class='color-fg-default lh-0 mb-2 markdown-title'])[6]")
    # page.click("//span[normalize-space()='Settings']")
    # page.locator("button[id='visibility_menu-button'] span[class='Button-label']").scroll_into_view_if_needed()
    # page.click("//span[contains(text(),'Delete this repository')]")
    # page.click("//span[contains(text(),'I want to delete this repository')]")
    # page.click("button[id='repo-delete-proceed-button'] span[class='Button-label']")
    # # Get the full text from the warning paragraph
    # full_text = page.locator("div[id='repo-delete-warning-container'] p[class='text-bold f3 mt-2']").inner_text()
    # page.locator("//input[@id='verification_field']").fill(full_text)
    # page.click("button[id='repo-delete-proceed-button'] span[class='Button-label']")



    # # # Locate the confirmation input field and fill it
    # # page.click("button[id='repo-delete-proceed-button'] span[class='Button-label']")
    # repo_full_name = page.selector("//div[@id='repo-delete-warning-container']//p[@class='text-bold f3 mt-2']")
    # # page.get_by_label(
    # #     "Type in the name of the repository to confirm that you want to delete this repository."
    # # ).fill(repo_full_name)
    # # page.click("button[id='repo-delete-proceed-button'] span[class='Button-label']")
    # # page.pause()
    # # page.click("button[id='visibility_menu-button'] span[class='Button-label']")
    # # page.click("//span[normalize-space()='Change to private']")
    # # page.click("//button[@id='repo-visibility-proceed-button-private']//span[@class='Button-content']")
    # # page.click("button[id='repo-visibility-proceed-button-private'] span[class='Button-label']")
    # # page.click("//span[contains(text(),'Make this repository private')]")

    # Navigate to profile repositories page
    # logger.info("Navigating to user's repositories")
    # page.goto(f"{GITHUB_BASE_URL}/{GITHUB_USERNAME}?tab=repositories")
    #
    # # Get all repo links
    # logger.info("Fetching repository links from profile")
    # repo_links = page.locator("a[itemprop='name codeRepository']").all()
    #
    # deleted_count = 0
    # while True:
    #     logger.info("Navigating to user's repositories")
    #     page.goto(f"{GITHUB_BASE_URL}/{GITHUB_USERNAME}?tab=repositories")
    #     page.wait_for_load_state("domcontentloaded")
    #     expect(page.locator("a[itemprop='name codeRepository']").first).to_be_visible()
    #
    #     repo_locator = page.locator("a[itemprop='name codeRepository']")
    #     repo_count = repo_locator.count()
    #     found = False
    #
    #     for i in range(repo_count):
    #         repo = repo_locator.nth(i)
    #         expect(repo).to_be_visible()
    #         repo_name = repo.inner_text().strip()
    #         logger.debug(f"Found repository: {repo_name}")
    #
    #         if re.match(r"ui-repo-(175984[2-9]\d*|175985\d+|\d{7,})", repo_name):
    #             logger.info(f"Targeting repository for deletion: {repo_name}")
    #             repo.click()
    #             page.wait_for_load_state("domcontentloaded")
    #
    #             # Go to settings
    #             logger.info("Navigating to repository settings")
    #             page.click("//span[normalize-space()='Settings']")
    #
    #             # Scroll to Danger Zone
    #             logger.info("Scrolling to visibility menu and danger zone")
    #             page.locator(
    #                 "button[id='visibility_menu-button'] span[class='Button-label']").scroll_into_view_if_needed()
    #             page.click("//span[contains(text(),'Delete this repository')]")
    #             page.click("//span[contains(text(),'I want to delete this repository')]")
    #             page.click("button[id='repo-delete-proceed-button'] span[class='Button-label']")
    #
    #             # Extract confirmation text
    #             logger.info("Extracting confirmation text from deletion modal")
    #             full_text = page.locator(
    #                 "div[id='repo-delete-warning-container'] p[class='text-bold f3 mt-2']").inner_text()
    #             match = re.search(r'"([^"]+)"', full_text)
    #             repo_full_name = match.group(1) if match else full_text.strip()
    #
    #             # Confirm deletion
    #             logger.info(f"Confirming deletion for: {repo_full_name}")
    #             page.locator("//input[@id='verification_field']").fill(repo_full_name)
    #             page.click("button[id='repo-delete-proceed-button'] span[class='Button-label']")
    #             page.wait_for_timeout(1000)
    #             logger.info(f"✅ Deleted repository: {repo_full_name}")
    #
    #             deleted_count += 1
    #             found = True
    #             break  # Refresh repo list after deletion
    #
    #     if not found:
    #         break  # No more matching repos
    #
    # logger.info(f"✅ Total repositories deleted: {deleted_count}")

#Backup
#
# import re
# import time
# import pytest
# from loguru import logger
# from playwright.sync_api import expect
# from auth_helpers import login
# from config import GITHUB_USERNAME, GITHUB_PASSWORD, GITHUB_BASE_URL
#
# #1. Create Repository
# @pytest.mark.order(1)
# def test_create_repository(page):
#     login(page)
#     repo_name = f"ui-repo-{int(time.time())}"
#     desc = "This is a test repository"
#     page.goto("https://github.com/new")
#
#     logger.info("=============== test_create_repository Started ===============")
#     # Fill form
#     page.fill("//input[@id='repository-name-input']", repo_name)
#     # Wait for name validation (GitHub shows green checkmark or hides error)
#     expect(page.locator("#RepoNameInput-is-available")).to_be_visible()
#     # Fill description (after name is validated)
#     page.fill("//input[@name='Description']", desc)
#     # Verify successful creation
#     page.click("//span[normalize-space()='Create repository']")
#     # Verify repository appears in profile
#     expected_url = f"https://github.com/{GITHUB_USERNAME}/{repo_name}"
#     page.wait_for_url(expected_url)
#     assert page.url == expected_url
#     logger.info("Repository created successfully")
#     logger.info("=============== test_create_repository Ended ===============")
#
# @pytest.mark.order(2)
# def test_repository_settings(page):
#     login(page)
#     repo_name = f"ui-repo-settings-{int(time.time())}"
#     updated_desc = "Updated via UI test"
#     logger.info("=============== test_repository_settings Started ===============")
#
#     # Create repository first
#     repo_name = f"ui-repo-{int(time.time())}"
#     desc = "This is a test repository"
#     page.goto("https://github.com/new")
#
#     # Fill form
#     page.fill("//input[@id='repository-name-input']", repo_name)
#     # Wait for name validation (GitHub shows green checkmark or hides error)
#     expect(page.locator("#RepoNameInput-is-available")).to_be_visible()
#     # Fill description (after name is validated)
#     page.fill("//input[@name='Description']", updated_desc)
#     # Verify successful creation
#     page.click("//span[normalize-space()='Create repository']")
#
#     # Navigate to settings
#     page.click("//span[normalize-space()='Settings']")
#
#     # Modify repo visibility (Changed Repo Visibility from Public to Private)
#     page.locator("button[id='visibility_menu-button'] span[class='Button-label']").scroll_into_view_if_needed()
#     page.click("button[id='visibility_menu-button'] span[class='Button-label']")
#     page.click("//span[normalize-space()='Change to private']")
#     page.click("//button[@id='repo-visibility-proceed-button-private']//span[@class='Button-content']")
#     page.click("button[id='repo-visibility-proceed-button-private'] span[class='Button-label']")
#     page.click("//span[contains(text(),'Make this repository private')]")
#
#     #Verify changes persist
#     page.locator("button[id='visibility_menu-button'] span[class='Button-label']").scroll_into_view_if_needed()
#     updatedRepo = page.get_by_text("This repository is currently private.")
#     assert updatedRepo.is_visible()
#     logger.info("Verified Repository changes updated successfully")
#     logger.info("=============== test_repository_settings Ended ===============")
#
# @pytest.mark.order(3)
# def test_delete_repository(page):
#     login(page)
#     logger.info("=============== test_delete_repository Started ===============")
#     deleted_count = 0
#     while True:
#         # Navigate to profile repositories page
#         logger.info("Navigating to user's repositories")
#         page.goto(f"{GITHUB_BASE_URL}/{GITHUB_USERNAME}?tab=repositories")
#         page.wait_for_load_state("domcontentloaded")
#         expect(page.locator("a[itemprop='name codeRepository']").first).to_be_visible()
#
#         repo_locator = page.locator("a[itemprop='name codeRepository']")
#         repo_count = repo_locator.count()
#         found = False
#
#         for i in range(repo_count):
#             repo = repo_locator.nth(i)
#             expect(repo).to_be_visible()
#             repo_name = repo.inner_text().strip()
#             logger.debug(f"Found repository: {repo_name}")
#
#             if re.match(r"ui-repo-(175984[2-9]\d*|175985\d+|\d{7,})", repo_name):
#                 logger.info(f"Targeting repository for deletion: {repo_name}")
#                 repo.click()
#                 page.wait_for_load_state("domcontentloaded")
#
#                 # Go to settings
#                 logger.info("Navigating to repository settings")
#                 page.click("//span[normalize-space()='Settings']")
#
#                 # Scroll to Danger Zone
#                 logger.info("Scrolling to visibility menu and danger zone")
#                 page.locator(
#                     "button[id='visibility_menu-button'] span[class='Button-label']").scroll_into_view_if_needed()
#                 page.click("//span[contains(text(),'Delete this repository')]")
#                 page.click("//span[contains(text(),'I want to delete this repository')]")
#                 page.click("button[id='repo-delete-proceed-button'] span[class='Button-label']")
#
#                 # Extract confirmation text
#                 logger.info("Extracting confirmation text from deletion modal")
#                 full_text = page.locator(
#                     "div[id='repo-delete-warning-container'] p[class='text-bold f3 mt-2']").inner_text()
#                 match = re.search(r'"([^"]+)"', full_text)
#                 repo_full_name = match.group(1) if match else full_text.strip()
#
#                 # Confirm deletion
#                 logger.info(f"Confirming deletion for: {repo_full_name}")
#                 page.locator("//input[@id='verification_field']").fill(repo_full_name)
#                 page.click("button[id='repo-delete-proceed-button'] span[class='Button-label']")
#                 page.wait_for_timeout(1000)
#                 logger.info(f"Deleted repository: {repo_full_name}")
#
#                 deleted_count += 1
#                 found = True
#                 break  # Refresh repo list after deletion
#
#         if not found:
#             break  # No more matching repos
#
#     logger.info(f"Total repositories deleted: {deleted_count}")
#     logger.info("=============== test_delete_repository Ended ===============")

# UI Operations File Backup
import re
import time
import pytest
from loguru import logger
from playwright.sync_api import expect
from helpers import login
from config import GITHUB_USERNAME, GITHUB_PASSWORD, GITHUB_BASE_URL

# ========================= Test 1: Create Repository =========================
@pytest.mark.order(1)
def test_create_repository(page):
    login(page)
    repo_name = f"ui-repo-{int(time.time())}"
    desc = "This is a test repository"
    page.goto("https://github.com/new")

    logger.info("🔧 Starting repository creation flow")

    # Fill repository name
    page.fill("//input[@id='repository-name-input']", repo_name)

    # Wait for GitHub to validate name availability
    expect(page.locator("#RepoNameInput-is-available")).to_be_visible()

    # Fill description after name is validated
    page.fill("//input[@name='Description']", desc)

    # Submit form to create repository
    page.click("//span[normalize-space()='Create repository']")

    # Confirm repository was created successfully
    expected_url = f"https://github.com/{GITHUB_USERNAME}/{repo_name}"
    page.wait_for_url(expected_url)
    assert page.url == expected_url

    logger.info(f" Repository created: {repo_name}")
    logger.info("test_create_repository completed")

# ========================= Test 2: Update Repository Settings =========================
@pytest.mark.order(2)
def test_repository_settings(page):
    login(page)
    repo_name = f"ui-repo-{int(time.time())}"
    updated_desc = "Updated via UI test"

    logger.info("🔧 Starting repository settings update flow")

    # Create a new repository
    page.goto("https://github.com/new")
    page.fill("//input[@id='repository-name-input']", repo_name)
    expect(page.locator("#RepoNameInput-is-available")).to_be_visible()
    page.fill("//input[@name='Description']", updated_desc)
    page.click("//span[normalize-space()='Create repository']")

    # Navigate to repository settings
    page.click("//span[normalize-space()='Settings']")

    # Change visibility from public to private
    page.locator("button[id='visibility_menu-button'] span[class='Button-label']").scroll_into_view_if_needed()
    page.click("button[id='visibility_menu-button'] span[class='Button-label']")
    page.click("//span[normalize-space()='Change to private']")
    page.click("//button[@id='repo-visibility-proceed-button-private']//span[@class='Button-content']")
    page.click("button[id='repo-visibility-proceed-button-private'] span[class='Button-label']")
    page.click("//span[contains(text(),'Make this repository private')]")

    # Confirm visibility change
    page.locator("button[id='visibility_menu-button'] span[class='Button-label']").scroll_into_view_if_needed()
    updatedRepo = page.get_by_text("This repository is currently private.")
    assert updatedRepo.is_visible()

    logger.info(f" Repository visibility updated: {repo_name}")
    logger.info("test_repository_settings completed")

# ========================= Test 3: Delete Matching Repositories =========================
@pytest.mark.order(3)
def test_delete_repository(page):
    login(page)
    logger.info("🗑️ Starting repository deletion flow")

    deleted_count = 0

    while True:
        # Navigate to user's repository list
        page.goto(f"{GITHUB_BASE_URL}/{GITHUB_USERNAME}?tab=repositories")
        page.wait_for_load_state("domcontentloaded")
        expect(page.locator("a[itemprop='name codeRepository']").first).to_be_visible()

        repo_locator = page.locator("a[itemprop='name codeRepository']")
        repo_count = repo_locator.count()
        found = False

        for i in range(repo_count):
            repo = repo_locator.nth(i)
            expect(repo).to_be_visible()
            repo_name = repo.inner_text().strip()
            logger.debug(f"Found repository: {repo_name}")

            # Match repositories with numeric suffix >= 1759842
            if re.match(r"ui-repo-(175984[2-9]\d*|175985\d+|\d{7,})", repo_name):
                logger.info(f"🗑️ Deleting repository: {repo_name}")
                repo.click()
                page.wait_for_load_state("domcontentloaded")

                # Navigate to settings
                page.click("//span[normalize-space()='Settings']")

                # Scroll to Danger Zone and initiate deletion
                page.locator("button[id='visibility_menu-button'] span[class='Button-label']").scroll_into_view_if_needed()
                page.click("//span[contains(text(),'Delete this repository')]")
                page.click("//span[contains(text(),'I want to delete this repository')]")
                page.click("button[id='repo-delete-proceed-button'] span[class='Button-label']")

                # Extract confirmation name
                full_text = page.locator("div[id='repo-delete-warning-container'] p[class='text-bold f3 mt-2']").inner_text()
                match = re.search(r'"([^"]+)"', full_text)
                repo_full_name = match.group(1) if match else full_text.strip()

                # Confirm deletion
                page.locator("//input[@id='verification_field']").fill(repo_full_name)
                page.click("button[id='repo-delete-proceed-button'] span[class='Button-label']")
                page.wait_for_timeout(1000)

                logger.info(f" Deleted repository: {repo_full_name}")
                deleted_count += 1
                found = True
                break  # Refresh repo list after deletion

        if not found:
            break  # No more matching repositories

    logger.info(f"Total repositories deleted: {deleted_count}")
    logger.info("test_delete_repository completed")