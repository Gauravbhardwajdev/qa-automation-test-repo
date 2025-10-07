from helpers import login
from logger_config import logger
from config import GITHUB_USERNAME, GITHUB_TOKEN, GITHUB_BASE_URL, GITHUB_PASSWORD
from pages.login_page import LoginPage


def test_github_login_flow(page):
    login(page)
    logger.info("=============== Starting GitHub login flow test ===============")
    login_page = LoginPage(page)
    login_page.navigate_to_login(GITHUB_BASE_URL)
    login_page.verify_dashboard_loaded()
    logger.info("=============== Login flow test completed successfully ===============")

def test_session_persistence(browser):
    logger.info("🔐 Starting session persistence test")

    # Step 1: Login and save session
    context = browser.new_context()
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.navigate_to_login(GITHUB_BASE_URL)
    login_page.login(GITHUB_USERNAME, GITHUB_PASSWORD)
    context.storage_state(path="state.json")
    context.close()

    # Step 2: Reopen browser with saved session
    new_context = browser.new_context(storage_state="state.json")
    new_page = new_context.new_page()
    login_page = LoginPage(new_page)
    new_page.goto(f"{GITHUB_BASE_URL}/")
    login_page.verify_dashboard_loaded()
    logger.info("✅ Session persistence verified")
    new_context.close()

def test_logout_flow(page):
    logger.info("🔐 Starting logout flow test")

    login_page = LoginPage(page)
    login_page.navigate_to_login(GITHUB_BASE_URL)
    login_page.login(GITHUB_USERNAME, GITHUB_PASSWORD)
    logger.info("✅ Logged in successfully")

    login_page.logout(GITHUB_BASE_URL)
    logger.info("✅ Logout flow verified successfully")


