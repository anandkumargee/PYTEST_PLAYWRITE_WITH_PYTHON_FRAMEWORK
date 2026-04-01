# Playwright-Pytest Automation Framework

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/playwright-1.40%2B-green.svg)](https://playwright.dev/)
[![Pytest](https://img.shields.io/badge/pytest-7.0%2B-yellow.svg)](https://pytest.org/)
[![Allure](https://img.shields.io/badge/allure-2.24%2B-orange.svg)](https://docs.qameta.io/allure/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://opensource.org/licenses/MIT)

A modern, high-performance, and scalable automation framework built with **Python**, **Playwright**, and **Pytest**. This framework is optimized for reliability, speed, and ease of use in any organizational environment.

---

## 📑 Table of Contents
- [🚀 Why This Framework Over Java Selenium?](#-why-this-framework-over-java-selenium)
- [🛠️ Prerequisites & Multi-Platform Setup](#️-prerequisites--multi-platform-setup)
- [⚙️ Organization Setup (Adaptive Guide)](#️-organization-setup-adaptive-guide)
- [🏗️ Project Architecture & Workflow](#️-project-architecture--workflow)
- [📈 Running and Reporting](#-running-and-reporting)
- [🛠️ Troubleshooting & Setup Checklist](#️-troubleshooting--setup-checklist)
- [📁 Folder Structure](#-folder-structure)
- [📊 Reporting & Artifacts](#-reporting--artifacts)
- [✅ Best Practices](#-best-practices)
- [🏷️ Keywords & Search Tags](#️-keywords--search-tags)

---

## 🚀 Why This Framework Over Java Selenium?

| Feature | Playwright (This Framework) | Java Selenium |
| :--- | :--- | :--- |
| **Speed** | 🚀 Native asynchronous execution (Fastest). | 🐢 Slower, synchronous execution. |
| **Stability** | ✅ Built-in Auto-waits (Retry-ability). | ❌ Manual `Thread.sleep` or `ExpectedConditions`. |
| **Architecture** | 🔥 WebSocket (Direct) - Bidirectional. | ⛓️ HTTP (Indirect) - Unidirectional. |
| **Parallelism** | ⚡ Simple `pytest -n` (Zero Config). | ⚙️ Complex TestNG/Grid infrastructure. |
| **Browser Support** | 🌐 Chrome, Firefox, Safari (Full engines). | 📦 Requires separate binary drivers. |
| **Shadow DOM** | 🔦 Native support for piercing Shadow DOM. | 🧱 Manual JS execution required. |
| **Debug Tools** | 🛠️ Trace Viewer & Inspector (Visual). | 📉 Standard stack traces only. |

---

## 🛠️ Prerequisites & Multi-Platform Setup

Before using the framework, ensure you have **Python** and **Java (JDK)** installed on your machine.

### 🐍 Step 1: Install Python (3.8+)

| OS | Download Link | Path Configuration |
| :--- | :--- | :--- |
| **Windows** | [Python Official](https://www.python.org/downloads/windows/) | Check **"Add Python to PATH"** during installation. |
| **macOS** | [Python Official](https://www.python.org/downloads/macos/) | Use `brew install python` (Homebrew recommended). |
| **Linux** | `sudo apt install python3` | Standard on most distributions. |

### ☕ Step 2: Install Java (For Allure Reports)
Allure requires Java to generate and serve interactive reports. 

- **Download**: [Eclipse Adoptium (OpenJDK)](https://adoptium.net/)
- **Configuration**:
  - **Windows**: Add `JAVA_HOME` to your System Variables and add `%JAVA_HOME%\bin` to your **PATH**.
  - **macOS/Linux**: Add `export JAVA_HOME=$(/usr/libexec/java_home)` to your `.zshrc` or `.bashrc`.

### 📊 Step 3: Install Allure CLI
The Allure command-line tool is used to view the reports.

- **Windows**: `scoop install allure` or manual download from [GitHub Releases](https://github.com/allure-framework/allure2/releases).
- **macOS**: `brew install allure`
- **Linux**: `npm install -g allure-commandline --save-dev`

### 🏗️ Step 4: Local Framework Setup (The checklist)

1. **Clone the Project**:
   ```bash
   git clone https://github.com/anandkumargee/PYTEST_PLAYWRITE_WITH_PYTHON_FRAMEWORK.git
   cd PUB_PYTEST_PLAYWRITE_FRAMEWORK
   ```

2. **Create a Virtual Environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate   # Mac/Linux: source venv/bin/activate
   ```

3. **Install Project Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Install Playwright Browsers**:
   ```powershell
   playwright install
   ```

---

## ✅ Installation Verification Checklist

Run these commands to confirm your environment is ready:

| Command | Expected Output | Purpose |
| :--- | :--- | :--- |
| `python --version` | `Python 3.8+` | Core logic and Pytest. |
| `java -version` | `openjdk version "11+"` | Required by Allure. |
| `allure --version` | `2.x.x` | Reporting tool. |
| `pytest --version` | `pytest 7.x.x+` | Test runner. |

---

## ⚙️ Organization Setup (Adaptive Guide)

To start using this framework for your own organization:

### 1. Update Core Configuration
Edit `config/config.json` to reflect your environments (QA, Prod, Staging):
- **base_url**: The entry point for your application.
- **browser**: Target browser (chromium, firefox, webkit).
- **headless**: Toggle between `true` (running in background) or `false` (seeing the browser).
- **user_credentials**: Store your test accounts here.

### 2. Manage Secrets
Create a `.env` file in the root directory to store sensitive data:
```env
DB_PASSWORD=your_password
API_KEY=your_key
```

---

## 🏗️ Project Architecture & Workflow

### 1. Create a Page Object (`pages/`)
Create a new file (e.g., `dashboard_page.py`) that inherits from `BasePage`:
```python
class DashboardPage(BasePage):
    HEADER = "//h6[contains(@class, 'oxd-topbar-header')]"
    
    def is_header_visible(self) -> bool:
        return self.is_visible(self.HEADER)
```

### 2. Add as a Fixture (`conftest.py`)
Register your new page in `conftest.py` to make it available to all tests:
```python
@pytest.fixture
def dashboard_page(page_factory):
    return page_factory(DashboardPage)
```

### 3. Write Your Test (`tests/`)
Create a test file (e.g., `test_dashboard.py`) and use **Type Hinting** for IDE support:
```python
def test_dashboard_header(dashboard_page: DashboardPage):
    assert dashboard_page.is_header_visible()
```

---

## 📈 Running and Reporting

### 1. Using the Batch Script (Recommended)
The `Run_Tests.bat` script handles cleaning old reports and activating the virtual environment automatically.

**Basic Usage:**
```powershell
.\Run_Tests.bat <environment> <browser>
```

**Examples:**
- **Run in QA with Chrome**: `.\Run_Tests.bat qa chromium`
- **Run in Prod with Firefox**: `.\Run_Tests.bat prod firefox`
- **Run in Staging with Safari**: `.\Run_Tests.bat staging webkit` (WebKit)

### 2. Alternative Command Line (Pytest)
If you prefer running directly via `pytest`, ensure your virtual environment is active:
```powershell
pytest --env=qa --browser=chromium
```
- **Parallel Run (xdist)**: `pytest -n 4 --env=qa` (Runs on 4 CPUs)
- **Specific Marker**: `pytest -m smoke --env=qa`

### 🛠️ Troubleshooting & Setup Checklist
If you encounter issues during installation or execution, check the following:

- [ ] **Python Version**: Ensure you are using **Python 3.8 or higher** (`python --version`).
- [ ] **Virtual Environment**: Confirm `(venv)` is visible in your terminal before running tests.
- [ ] **Playwright Binaries**: Did you run `playwright install`? If not, browsers will not launch.
- [ ] **Java Installation**: Verify `java -version` works (Allure needs this to generate reports).
- [ ] **Execution Policy**: If `.bat` scripts are blocked on Windows, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in PowerShell.
- [ ] **Config Errors**: Verify that your `config/config.json` exists and is valid JSON (no missing commas or braces).
- [ ] **Drivers**: Playwright manages its own drivers, but ensure your firewall is not blocking the downloader during `playwright install`.
- [ ] **Env Config**: Verify `config/config.json` has the correct `base_url` for your target environment.
- [ ] **Allure CLI**: Ensure `allure --version` works if you want to see the visual reports.

---

---

## 📊 Reporting & Artifacts

| Report Type | Path | Description |
| :--- | :--- | :--- |
| **Allure Report** | `reports/allure-report/` | Interactive, trend-based report (Requires Allure CLI). |
| **Pytest HTML** | `reports/pytest-reports/` | Single-file static HTML report. |
| **Traces** | `reports/playwright-artifacts/` | Detailed Playwright Traces for debbuging. |
| **Screenshots** | Attached to Allure | Captured automatically on failure. |

## 📁 Folder Structure

- `config/`: Environment profiles (`config.json`).
- `core/`: Framework engines and configuration managers.
- `data/`: Test data files (JSON, CSV, etc.) for data-driven testing. 🆕
- `pages/`: Page Object Models (POM) - UI interactions and locators.
- `tests/`: Test suites categorized by functionality.
- `utils/`: Common helpers (Logging, Retry logic, Excel/JSON utils).
- `reports/`: Organized output for all test execution artifacts.

---

## ✅ Best Practices
- **Use Type Hints**: Always use `: PageClassName` in test arguments to enable **<Ctrl + Click>** navigation.
- **Avoid Hardcoding**: Put all timeouts and URLs into `config.json`.
- **Suite Setup**: Use `scope="module"` fixtures in individual files for efficient single-session execution.

---

## 🏷️ Keywords & Search Tags
For discovery and SEO, this project focuses on:
`#PythonAutomation` `#PlaywrightTesting` `#PytestFramework` `#TestAutomationStrategy` `#WebAutomation` `#QA` `#SoftwareTesting` `#AllureReports` `#CI/CD` `#OrangeHRMAutomation`

---

*This framework is designed for quality at scale. Happy Testing!*
