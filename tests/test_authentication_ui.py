from helpers import login
from logger_config import logger
from config import GITHUB_USERNAME, GITHUB_TOKEN, GITHUB_BASE_URL, GITHUB_PASSWORD
from pages.login_page import LoginPage


def test_github_login_flow(page):
    logger.info("🚀 Initiating GitHub login flow test")
    login(page)
    logger.info("🔐 Login helper executed")

    login_page = LoginPage(page)
    logger.info("🌐 Navigating to GitHub login page")
    login_page.navigate_to_login(GITHUB_BASE_URL)

    logger.info("📊 Verifying dashboard load post-login")
    login_page.verify_dashboard_loaded()

    logger.info("✅ GitHub login flow test completed successfully")


def test_session_persistence(browser):
    logger.info("🔐 Starting session persistence test")

    # Step 1: Login and save session
    logger.info("🗝️ Creating new browser context for login")
    context = browser.new_context()
    page = context.new_page()
    login_page = LoginPage(page)

    logger.info("🌐 Navigating to GitHub login page")
    login_page.navigate_to_login(GITHUB_BASE_URL)

    logger.info("🔐 Logging in with credentials")
    login_page.login(GITHUB_USERNAME, GITHUB_PASSWORD)

    logger.info("💾 Saving session state to 'state.json'")
    context.storage_state(path="state.json")
    context.close()
    logger.info("📁 Initial context closed after saving session")

    # Step 2: Reopen browser with saved session
    logger.info("🔄 Reopening browser with saved session state")
    new_context = browser.new_context(storage_state="state.json")
    new_page = new_context.new_page()
    login_page = LoginPage(new_page)

    logger.info("🌐 Navigating to GitHub dashboard with persisted session")
    new_page.goto(f"{GITHUB_BASE_URL}/")

    logger.info("📊 Verifying dashboard load with persisted session")
    login_page.verify_dashboard_loaded()

    logger.info("✅ Session persistence verified successfully")
    new_context.close()
    logger.info("📁 New context closed after verification")


def test_logout_flow(page):
    logger.info("🔐 Starting logout flow test")

    login_page = LoginPage(page)
    logger.info("🌐 Navigating to GitHub login page")
    login_page.navigate_to_login(GITHUB_BASE_URL)

    logger.info("🔐 Logging in with credentials")
    login_page.login(GITHUB_USERNAME, GITHUB_PASSWORD)
    logger.info("✅ Logged in successfully")

    logger.info("🚪 Initiating logout sequence")
    login_page.logout(GITHUB_BASE_URL)
    logger.info("✅ Logout flow verified successfully")