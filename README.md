# Playwright-Pytest Automation Framework

A modern, high-performance, and scalable automation framework built with **Python**, **Playwright**, and **Pytest**. This framework is designed for reliability, speed, and ease of use in any organizational environment.

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
   git clone <your-repo-url>
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
    LOCATOR = "//div[@id='example']"
    
    def my_action(self):
        self.click(self.LOCATOR)
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
def test_example(dashboard_page: DashboardPage):
    dashboard_page.my_action()
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

---

## 📊 Reports & Artifacts

## 📁 Folder Structure

- `config/`: Environment-specific configuration.
- `core/`: Framework configuration and management logic.
- `pages/`: Page Object classes (the "Logic").
- `tests/`: Pytest test files (the "Checks").
- `utils/`: Reusable helpers (Logging, Data Loading, Retries).
- `reports/`: Test artifacts (Screenshots, Traces, HTML).

---

## ✅ Best Practices
- **Use Type Hints**: Always use `: PageClassName` in test arguments to enable **<Ctrl + Click>** navigation.
- **Avoid Hardcoding**: Put all timeouts and URLs into `config.json`.
- **Suite Setup**: Use `scope="module"` fixtures in individual files for efficient single-session execution.

---

*This framework is designed for quality at scale. Happy Testing!*
