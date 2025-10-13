import re

from loguru import logger
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

        # File Upload()
        self.click_add_file_button = page.locator("//span[@class='react-directory-add-file-button']")
        self.upload_file = page.locator("//a[normalize-space()='uploading an existing file']")
        self.upload_file1 = page.locator("a:has-text('Upload files')")
        self.choose_file = page.locator("#upload-manifest-files-input")
        self.commit_button = page.locator("button:has-text('Commit changes')")
        self.commit_message_input = page.locator("input[name='message']")
        self.uploaded_file_row = lambda filename: page.locator(f"text={filename}")
        self.commit_changes_description = page.locator("//input[@id='commit-summary-input']")
        self.commit_changes_message = page.locator("//textarea[@id='commit-description-textarea']")
        self.commit_changes_button = page.locator("//button[normalize-space()='Commit changes']")
        self.uploaded_file_row = lambda filename: self.page.locator(
            f"td.react-directory-row-name-cell-large-screen a[title='{filename}']"
        )
        self.edit_button = page.locator("(//*[name()='svg'][@class='octicon octicon-pencil'])[1]")

    def navigate_to_creation_page(self):
        self.page.goto("https://github.com/new")

    def fill_repository_details(self, repo_name: str, description: str):
        self.repo_name_input.fill(repo_name)
        expect(self.name_available_indicator).to_be_visible()
        self.repo_desc_input.fill(description)

    #custom method to Open the Created Repo
    def open_repository_by_name(self, repo_name: str):
        repo_link = self.page.locator(f"a[href*='/{repo_name}']")
        expect(repo_link).to_be_visible()
        repo_link.click()
        self.page.wait_for_url(f"**/{repo_name}")

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

    def upload_and_commit_file(self, file_path: str, summary: str, description: str):
        # Step 1: Click "uploading an existing file" link
        expect(self.upload_file).to_be_visible(timeout=10000)
        self.upload_file.click()
        self.page.wait_for_timeout(2000)

        expect(self.choose_file).to_be_visible()
        self.page.wait_for_timeout(2000)

        # Step 2: Upload the file
        self.choose_file.set_input_files(file_path)
        filename = file_path.split("/")[-1]

        # Step 3: Fill commit summary and description
        self.commit_changes_description.fill(summary)
        self.page.wait_for_timeout(2000)
        self.commit_changes_message.fill(description)
        self.page.wait_for_timeout(2000)

        # Step 4: Click "Commit changes"
        self.commit_changes_button.click()

        # Step 5: Wait for redirect and file list to appear
        self.page.wait_for_url(re.compile(r".*/[^/]+$"), timeout=10000)
        self.page.wait_for_load_state("load")
        self.page.wait_for_timeout(3000)

        # Step 6: Confirm file is visible
        file_locator = self.uploaded_file_row(filename)
        expect(file_locator).to_be_visible(timeout=10000)

        # Step 7: Return summary for validation
        return summary

    def verify_uploaded_file(self, filename: str, timeout: int = 10000) -> str:
        self.page.wait_for_url(re.compile(r".*/[^/]+$"), timeout=timeout)
        self.page.wait_for_load_state("load")

        file_locator = self.uploaded_file_row(filename)
        try:
            expect(file_locator).to_be_visible(timeout=timeout)
            return filename
        except:
            return "uploading failed"


    # Test File Editing
    def navigate_to_profile_repositories(self, username: str):
        self.page.goto(f"https://github.com/{username}?tab=repositories")
        self.page.wait_for_load_state("load")

    def open_latest_repository(self) -> str:
        latest_repo = self.page.locator("li[itemprop='owns'] a[itemprop='name codeRepository']").first
        repo_name = latest_repo.inner_text()
        latest_repo.click()
        self.page.wait_for_url(re.compile(r".*/[^/]+$"), timeout=10000)
        return repo_name



    #File Editing
    def open_file_preview(self, filename: str):

        file_locator = self.page.locator(
            f"td.react-directory-row-name-cell-large-screen a[title='{filename}']"
        )
        expect(file_locator).to_be_visible(timeout=10000)
        file_locator.click()
        self.page.wait_for_url(re.compile(r".*/blob/.*"), timeout=10000)


    def open_file_in_editor(self):
        edit_button = self.page.locator("(//*[name()='svg'][@class='octicon octicon-pencil'])[1]")
        expect(edit_button).to_be_visible(timeout=5000)
        edit_button.click()
        self.page.wait_for_url(re.compile(r".*/edit/.*"), timeout=10000)

    def edit_file_content(self, new_text: str):
        editor = self.page.locator("div[role='textbox']").first
        expect(editor).to_be_visible(timeout=5000)
        editor.fill(new_text)
        self.page.wait_for_timeout(1000)
        logger.info(f"✅ File content updated with: '{new_text}'")

    def commit_file_changes(self, message: str):
        commit_button = self.page.locator("button:has-text('Commit changes')")
        expect(commit_button).to_be_visible(timeout=5000)
        commit_button.click()
        self.page.wait_for_url(re.compile(r".*/[^/]+$"), timeout=10000)
        logger.info(f"✅ Changes committed with message: '{message}'")

        logger.info("📤 Committing changes...")
        commit_input = self.page.locator("#commit-message-input")
        expect(commit_input).to_be_visible(timeout=5000)
        commit_input.fill(message)

        logger.info("📤 Committing Extended description")
        commit_input = self.page.locator("#commit-description-input")
        expect(commit_input).to_be_visible(timeout=5000)
        commit_input.fill(message)

        logger.info("📤 Clicking Commit Changes button...")
        commit_btn = self.page.locator("button[aria-disabled='false'] span[class='prc-Button-Label-pTQ3x']")
        commit_btn.click()

    def verify_file_content(self, expected_text: str):
        logger.info("🔍 Verifying updated content in file preview...")

        content_area = self.page.locator("//textarea[@id='read-only-cursor-text-area']")
        expect(content_area).to_be_visible(timeout=5000)

        file_text = content_area.input_value()
        assert expected_text in file_text, f"❌ Edited content not found. Actual content: {file_text}"

        logger.info("✅ File changes successfully reflected in preview")

    def upload_file_to_repo(self, file_path: str, summary: str, description: str):
        logger.info("🖱️ Clicking 'Add file' dropdown...")

        # Step 1: Click the Add File button
        expect(self.click_add_file_button).to_be_visible(timeout=5000)
        self.page.wait_for_timeout(1000)
        self.click_add_file_button.click()

        # Step 2: Click the 'Upload files' link from dropdown
        logger.info("🖱️ Clicking 'Upload files' link...")
        expect(self.upload_file1).to_be_visible(timeout=5000)
        self.page.wait_for_timeout(1000)
        self.upload_file1.click()
        logger.info("✅ 'Upload files' link clicked successfully")

        # Step 3: Upload the file
        logger.info(f"📁 Uploading file: {file_path}")
        expect(self.choose_file).to_be_visible(timeout=10000)
        expect(self.choose_file).to_be_enabled(timeout=10000)
        self.choose_file.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)
        self.choose_file.set_input_files(file_path)
        filename = file_path.split("/")[-1]

        # Step 4: Fill commit summary and description
        self.commit_changes_description.fill(summary)
        self.page.wait_for_timeout(2000)
        self.commit_changes_message.fill(description)
        self.page.wait_for_timeout(2000)

        # Step 5: Click "Commit changes"
        self.commit_changes_button.click()

        # Step 6: Wait for redirect and file list to appear
        self.page.wait_for_url(re.compile(r".*/[^/]+$"), timeout=10000)
        self.page.wait_for_load_state("load")
        self.page.wait_for_timeout(3000)

        # Step 7: Confirm file is visible
        file_locator = self.uploaded_file_row(filename)
        expect(file_locator).to_be_visible(timeout=10000)

        # Step 8: Return summary for validation
        logger.info(f"✅ File '{filename}' uploaded and committed successfully")
        return summary

    #
    # def click_choose_your_files(self, file_path: str, summary: str, description: str):
    #     logger.info(f"📁 Selecting file: {file_path}")
    #
    #     expect(self.choose_file).to_be_visible()
    #     self.page.wait_for_timeout(2000)
    #     self.choose_file.click()
    #
    #     # Step 2: Upload the file
    #     self.choose_file.set_input_files(file_path)
    #     filename = file_path.split("/")[-1]
    #
    #     # Step 3: Fill commit summary and description
    #     self.commit_changes_description.fill(summary)
    #     self.page.wait_for_timeout(2000)
    #     self.commit_changes_message.fill(description)
    #     self.page.wait_for_timeout(2000)
    #
    #     # Step 4: Click "Commit changes"
    #     self.commit_changes_button.click()
    #
    #     # Step 5: Wait for redirect and file list to appear
    #     self.page.wait_for_url(re.compile(r".*/[^/]+$"), timeout=10000)
    #     self.page.wait_for_load_state("load")
    #     self.page.wait_for_timeout(3000)
    #
    #     # Step 6: Confirm file is visible
    #     file_locator = self.uploaded_file_row(filename)
    #     expect(file_locator).to_be_visible(timeout=10000)


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






















