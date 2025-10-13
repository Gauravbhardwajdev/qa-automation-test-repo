# GitHub Automation — Full-Stack QA Suite

This repository contains a comprehensive automation framework built to validate GitHub workflows through both UI and API testing. It demonstrates real-world testing capabilities across authentication, repository management, file operations, error handling, and cross-platform reliability.

## 🚀 Tech Stack

- **Language**: Python 3.12+
- **UI Automation**: Playwright
- **API Testing**: requests
- **Logging**: loguru
- **Configuration**: dotenv
- **Test Runner**: Pytest

---

## 📁 Project Structure
<img width="286" height="609" alt="image" src="https://github.com/user-attachments/assets/deaf12ee-8212-426e-a7db-2d0f4c37c430" />

---

## 🧪 Test Coverage

### 🔐 Authentication & Session Management
- `test_github_login_flow`
- `test_session_persistence`
- `test_logout_flow`
- `test_api_authentication`

### 📦 Repository Operations (UI)
- `test_create_repository`
- `test_repository_settings`
- `test_delete_repository`
- `test_file_upload`
- `test_file_editing`
- `test_file_operations_errors`

### 🔗 API Testing
- `test_repository_api_crud`
- `test_api_data_consistency`
- `test_api_error_handling`
- `test_issue_management_api`
- `test_api_pagination_and_filtering`

### 🌐 Cross-Platform & Performance
- `test_cross_browser_functionality`
- `test_mobile_responsive_design`
- `test_page_load_performance`
- `test_error_recovery`
- `test_concurrent_operations`

### 🎯 Bonus Features
- `test_accessibility_compliance`
- `test_visual_consistency`

---

## 🛠 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
playwright install
