from config import GITHUB_USERNAME, GITHUB_PASSWORD, GITHUB_BASE_URL
import time

def login(page):
    page.goto(f"{GITHUB_BASE_URL}/login")
    page.fill("input[name='login']", GITHUB_USERNAME)
    page.fill("input[name='password']", GITHUB_PASSWORD)
    page.click("input[name='commit']")

def test_data(page):
    repo_name = f"ui-repo-{int(time.time())}"
    desc = "This is a test repository"
    return repo_name, desc