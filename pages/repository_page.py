import re

from playwright.sync_api import Page, expect
from config import GITHUB_USERNAME, GITHUB_BASE_URL


class RepositoryPage:
    def __init__(self, page: Page):
        # Creation
        self.page = page
        self.repo_name_input = page.locator("//input[@id='repository-name-input']")
        self.repo_desc_input = page.locator("//input[@name='Description']")
        self.name_available_indicator = page.locator("#RepoNameInput-is-available")
        self.create_button = page.locator("//span[normalize-space()='Create repository']")

        # Settings
        self.settings_tab = page.locator("//span[normalize-space()='Settings']")
        self.visibility_button = page.locator("button[id='visibility_menu-button'] span[class='Button-label']")
        self.change_to_private = page.locator("//span[normalize-space()='Change to private']")
        self.proceed_private_1 = page.locator("//button[@id='repo-visibility-proceed-button-private']//span[@class='Button-content']")
        self.proceed_private_2 = page.locator("button[id='repo-visibility-proceed-button-private'] span[class='Button-label']")
        self.confirm_private = page.locator("//span[contains(text(),'Make this repository private')]")
        self.private_status_text = page.get_by_text("This repository is currently private.")

    def navigate_to_creation_page(self):
        self.page.goto("https://github.com/new")

    def fill_repository_details(self, repo_name: str, description: str):
        self.repo_name_input.fill(repo_name)
        expect(self.name_available_indicator).to_be_visible()
        self.repo_desc_input.fill(description)

    def submit_creation(self):
        self.page.wait_for_selector("//span[normalize-space()='Create repository']", state="visible", timeout=10000)
        self.page.click("//span[normalize-space()='Create repository']")

    def verify_creation_success(self, repo_name: str):
        expected_url = f"https://github.com/{GITHUB_USERNAME}/{repo_name}"
        self.page.wait_for_url(expected_url)
        assert self.page.url == expected_url

    def navigate_to_settings(self):
        self.page.wait_for_selector("//span[normalize-space()='Settings']", state="visible", timeout=10000)
        self.page.click("//span[normalize-space()='Settings']")

    def update_visibility_to_private(self):
        expect(self.visibility_button).to_be_visible()
        self.visibility_button.scroll_into_view_if_needed()
        self.visibility_button.click()
        self.change_to_private.click()
        self.proceed_private_1.click()
        self.proceed_private_2.click()
        self.confirm_private.click()
        self.visibility_button.scroll_into_view_if_needed()
        expect(self.private_status_text).to_be_visible()

    def delete_matching_repositories(self, pattern: str):
        deleted_count = 0

        while True:
            self.page.goto(f"{GITHUB_BASE_URL}/{GITHUB_USERNAME}?tab=repositories")
            self.page.wait_for_load_state("domcontentloaded")
            repo_locator = self.page.locator("a[itemprop='name codeRepository']")
            expect(repo_locator.first).to_be_visible()

            repo_count = repo_locator.count()
            found = False

            for i in range(repo_count):
                repo = repo_locator.nth(i)
                expect(repo).to_be_visible()
                repo_name = repo.inner_text().strip()

                if re.match(pattern, repo_name):
                    repo.click()
                    self.page.wait_for_load_state("domcontentloaded")

                    # Navigate to settings
                    self.page.wait_for_selector("//span[normalize-space()='Settings']", state="visible", timeout=10000)
                    self.page.click("//span[normalize-space()='Settings']")

                    # Scroll to Danger Zone and initiate deletion
                    self.page.locator(
                        "button[id='visibility_menu-button'] span[class='Button-label']").scroll_into_view_if_needed()
                    self.page.click("//span[contains(text(),'Delete this repository')]")
                    self.page.click("//span[contains(text(),'I want to delete this repository')]")
                    self.page.click("button[id='repo-delete-proceed-button'] span[class='Button-label']")

                    # Extract confirmation name
                    full_text = self.page.locator(
                        "div[id='repo-delete-warning-container'] p[class='text-bold f3 mt-2']").inner_text()
                    match = re.search(r'"([^"]+)"', full_text)
                    repo_full_name = match.group(1) if match else full_text.strip()

                    # Confirm deletion
                    self.page.locator("//input[@id='verification_field']").fill(repo_full_name)
                    self.page.click("button[id='repo-delete-proceed-button'] span[class='Button-label']")
                    self.page.wait_for_timeout(1000)

                    deleted_count += 1
                    found = True
                    break  # Refresh repo list after deletion

            if not found:
                break

        return deleted_count






















