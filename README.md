# ControlUP - Automation Home Test

Welcome to the ControlUp Automation Test! This project includes automated UI and API tests based on the outlined requirements. The purpose of this exercise is to evaluate coding proficiency, problem-solving skills, and adherence to best practices.

---

## 📌 Project Overview
This test suite consists of:
- **UI Tests**: Automated tests for the [SauceDemo](https://www.saucedemo.com/) website.
- **API Tests**: Automated tests for the [Airport Gap](https://airportgap.com/) API service.

---

## 🛠️ Tech Stack
- **Programming Language**: Python
- **Testing Framework**: Pytest
- **UI Automation**: Selenium WebDriver
- **API Testing**: Requests Library
- **CI/CD**: GitHub Actions

---

## 📂 Project Structure
```
📦 project-root
 ┣ 📂 config
 ┃ ┗ 📜 config.yaml          # Configuration (e.g., base URLs, credentials)
 ┣ 📂 utilities
 ┃ ┣ 📜 logger.py            # Logging setup
 ┃ ┣ 📜 api_client.py        # API helper functions
 ┣ 📂 pages
 ┃ ┣ 📜 base_page.py         # BasePage class (generic methods)
 ┃ ┣ 📜 store_page.py        # StorePage class (specific UI interactions)
 ┣ 📂 tests
 ┃ ┣ 📜 test_store.py        # UI tests for the store
 ┃ ┣ 📜 test_api.py          # API tests
 ┃ ┣ 📜 conftest.py          # Common test setup (WebDriver, Hooks, Fixtures)
 ┣ 📂 reports                # Test reports and logs
 ┣ 📂 logs                   # Execution logs
 ┣ 📜 requirements.txt       # Dependencies
 ┣ 📜 pytest.ini             # Pytest configurations
 ┣ 📜 .gitignore
```

---

## 🔧 Setup & Installation
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/NillyOfan/ControlUP
cd NillyOfan/ControlUP
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Run UI & API Tests
#### 🖥️ Run UI Tests
```sh
pytest tests/test_store.py 
```

#### 🔗 Run API Tests
```sh
pytest tests/test_api.py
```

---

## 📊 Test Logs
- Test execution logs are stored in the `logs/` directory.
- CI/CD logs can be found in **GitHub Actions** under the "Actions" tab.

---

## 🏗️ CI/CD Integration (GitHub Actions)
This project includes a **GitHub Actions workflow** that automatically runs tests on each push and pull request.
### 🚀 Workflow Steps
1. Checkout repository
2. Set up Python environment
3. Install dependencies
4. Run Pytest tests
5. Upload logs & reports as artifacts

### 📌 Trigger Options
- `push`
- `pull_request`
- `workflow_dispatch`- [Trigger Test Workflow page](https://github.com/NillyOfan/ControlUP/actions/workflows/pytest.yml)

---

## ❓ Support
For any questions or clarifications, feel free to reach out.

📢 **Happy Testing! 🚀**

