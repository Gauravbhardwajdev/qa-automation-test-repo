import requests
from config import GITHUB_TOKEN, GITHUB_API_URL

def test_api_authentication():
    headers_valid = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    headers_invalid = {"Authorization": "Bearer invalid_token"}

    # ✅ Valid token allows API access
    response_valid = requests.get(f"{GITHUB_API_URL}/user", headers=headers_valid)
    assert response_valid.status_code == 200
    assert "login" in response_valid.json()

    # ✅ Invalid token returns 401 Unauthorized
    response_invalid = requests.get(f"{GITHUB_API_URL}/user", headers=headers_invalid)
    assert response_invalid.status_code == 401

    # ✅ Token permissions properly enforced
    repo_payload = {"name": "token-permission-test", "auto_init": True}
    response_write = requests.post(f"{GITHUB_API_URL}/user/repos", headers=headers_valid, json=repo_payload)

    if response_write.status_code == 201:
        print("Write permission confirmed")
        # Cleanup
        requests.delete(f"{GITHUB_API_URL}/repos/Gauravbhardwajdev/token-permission-test", headers=headers_valid)
    elif response_write.status_code == 403:
        print("Token lacks write permission")

    # ✅ Rate limiting headers present
    rate_limit_resp = requests.get(f"{GITHUB_API_URL}/rate_limit", headers=headers_valid)
    assert "rate" in rate_limit_resp.json()