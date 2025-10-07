from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("input[name='login']")
        self.password_input = page.locator("input[name='password']")
        self.sign_in_button = page.locator("input[name='commit']")
        self.dashboard_label = page.locator("//span[@class='AppHeader-context-item-label ']")
        self.user_menu_button = page.locator("button[aria-label='Open user navigation menu']")
        self.sign_out_link = page.locator("a:has-text('Sign out')")
        self.confirm_sign_out_button = page.locator("input[value='Sign out']")

    def navigate_to_login(self, base_url):
        self.page.goto(f"{base_url}/login")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.sign_in_button.click()
        expect(self.dashboard_label).to_be_visible()

    def verify_dashboard_loaded(self):
        expect(self.dashboard_label).to_be_visible()

    def logout(self, base_url):
        self.user_menu_button.scroll_into_view_if_needed()
        self.user_menu_button.click(force=True)
        self.page.wait_for_timeout(500)
        expect(self.user_menu_button).to_be_visible()
        self.user_menu_button.click()
        expect(self.sign_out_link).to_be_visible()
        self.sign_out_link.click()
        self.page.wait_for_url("**/logout")
        expect(self.confirm_sign_out_button).to_be_visible()
        self.confirm_sign_out_button.click()
        self.page.goto(f"{base_url}/settings/profile")
        expect(self.username_input).to_be_visible()