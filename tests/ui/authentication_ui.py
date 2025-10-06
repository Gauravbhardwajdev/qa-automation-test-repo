from config import logger, GITHUB_USERNAME, GITHUB_TOKEN, GITHUB_BASE_URL, GITHUB_PASSWORD
from playwright.sync_api import expect

def test_github_login_flow(page):
    logger.info("Starting GitHub login flow test")

    # Navigate to GitHub login
    logger.info("Navigating to GitHub login page")
    page.goto(f"{GITHUB_BASE_URL}/login")

    # Enter credentials
    logger.info("Entering login credentials")
    page.fill("input[name='login']", GITHUB_USERNAME)
    page.fill("input[name='password']", GITHUB_PASSWORD)

    # Verify successful login (dashboard visible)
    logger.info("Verifying successful login")
    page.click("[name='commit']")
    expect(page.locator("//span[@class='AppHeader-context-item-label ']")).to_be_visible()

    logger.info("Login flow test completed successfully")


from config import logger, GITHUB_USERNAME, GITHUB_PASSWORD, GITHUB_BASE_URL
from playwright.sync_api import expect

def test_session_persistence(browser):
    logger.info("Starting session persistence test")

    # Step 1: Login and save session
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"{GITHUB_BASE_URL}/login")
    page.fill("input[name='login']", GITHUB_USERNAME)
    page.fill("input[name='password']", GITHUB_PASSWORD)
    page.click("input[name='commit']")
    expect(page.locator("//span[@class='AppHeader-context-item-label ']")).to_be_visible()
    context.storage_state(path="state.json")
    context.close()

    # Step 2: Reopen browser with saved session
    new_context = browser.new_context(storage_state="state.json")
    new_page = new_context.new_page()
    new_page.goto(f"{GITHUB_BASE_URL}/")
    expect(new_page.locator("//span[@class='AppHeader-context-item-label ']")).to_be_visible()
    logger.info("Session persistence verified successfully")
    new_context.close()

def test_logout_flow(page):
    logger.info("Starting logout flow test")

    # --- Step 1: Login ---
    page.goto(f"{GITHUB_BASE_URL}/login")
    page.fill("input[name='login']", GITHUB_USERNAME)
    page.fill("input[name='password']", GITHUB_PASSWORD)
    page.click("input[name='commit']")
    expect(page.locator("//span[@class='AppHeader-context-item-label ']")).to_be_visible()
    logger.info("Logged in successfully Dashboard is Displayed")

    # --- Step 2: Open user menu ---
    user_menu = page.locator("button[aria-label='Open user navigation menu']")
    user_menu.scroll_into_view_if_needed()
    user_menu.click(force=True)
    page.wait_for_timeout(500)  # Give dropdown time to render
    logger.info("User menu opened")
    expect(user_menu).to_be_visible()
    user_menu.click()
    logger.info("User menu opened")

    # --- Step 3: Click 'Sign out' ---
    sign_out_link = page.locator("a:has-text('Sign out')")
    expect(sign_out_link).to_be_visible()
    sign_out_link.click()
    page.wait_for_url("**/logout")
    logger.info("Sign out link clicked, logout page loaded")

    # --- Step 4: Click confirm 'Sign out' ---
    confirm_sign_out_link = page.locator("input[value='Sign out']")
    expect(confirm_sign_out_link).to_be_visible()
    confirm_sign_out_link.click()
    logger.info("Confirm Sign out link clicked, logout page loaded")

    # Verify if Logged Out
    page.goto(f"{GITHUB_BASE_URL}/settings/profile")

    # Verify redirect to login
    expect(page.locator("input[name='login']")).to_be_visible()
    logger.info("Logout flow verified successfully")



