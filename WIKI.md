# 📖 Framework Technical Wiki

Welcome to the technical deep-dive of the **Playwright-Pytest Automation Framework**. This document serves as a comprehensive reference for developers and QA engineers to understand the internal architecture, configuration logic, and extension patterns.

---

## 🏗️ 1. Project Architecture

This framework follows a strict **Page Object Model (POM)** with a focus on inheritance and dependency injection via Pytest fixtures.

### BasePage Engine (`pages/base_page.py`)
The `BasePage` is the "heart" of all UI interactions. It wraps Playwright's native commands with:
- **Automatic Logging**: Every click, fill, and navigation is logged.
- **Retry Logic**: Integrated with `utils/retry_util.py` to handle flakiness (3 retries by default).
- **Dynamic Timeouts**: Derived from `config.json` via the page's `env_config` attribute.
- **Allure Step Decoration**: Every core action is automatically tracked as a step in the report.

### Configuration Manager (`core/config_manager.py`)
Uses a singleton-like pattern to load environment profiles. 
- **Environment Switching**: Driven by the `--env` CLI flag.
- **Secrets Management**: Integrated with `python-dotenv` to mask passwords or API keys from being hardcoded in `config.json`.

---

## ⚙️ 2. Advanced Configuration

### The `.env` File
Create a `.env` file for sensitive data. These variables can be accessed globally via `os.getenv()` in any test or page.

### `conftest.py` Fixtures
- **`browser_context_args`**: The critical location for window sizing.
- **`page_factory`**: A powerful utility that allows on-the-fly creation of typed page objects in tests.

---

## 🚀 3. Developer Guide: How to Extend

### Adding a New Page
1. Create `pages/my_new_page.py`.
2. Inherit from `BasePage`.
3. Define locators as class constants.

### Writing a New Test
Use **Type Hints** for full IDE support:
```python
def test_feature(login_page: LoginPage, page_factory):
    admin = page_factory(AdminPage)
    admin.verify_something()
```
> [!TIP]
> Use `(Ctrl + Click)` on the class name in your IDE to jump directly to the Page Object definition.

---

## 📊 4. Reporting & Diagnostics

### Allure Reports
The batch script `Run_Tests.bat` automatically:
1. Cleans old results.
2. Runs tests with metadata.
3. Generates the report with **History Trends**.
4. Opens the browser automatically to show findings.

### Playwright Traces
Found in `reports/playwright-artifacts/`. 
To view a trace: Go to [trace.playwright.dev](https://trace.playwright.dev/) and drag-and-drop the `.zip` file. You can see the **Action Timeline**, **Call Stack**, and **Network Logs** for every second of the test.

---

## 🛠️ 5. Technical "Gotchas" & Fixes

### Browser Maximization Logic
On some high-DPI or virtual displays, the browser may launch maximized but the content area remains small. We fixed this by:
1. Launching with `--start-maximized`.
2. Explicitly setting `--window-size=1920,1080` to provide a "hint" to Chromium.
3. Setting `viewport: None` (headed only) to let the OS-level window control the internal canvas resolution.

---

## ✅ Best Practices
- **Atomic Tests**: Keep tests focused on one objective.
- **No Hardcoding**: All URLs and credentials MUST reside in `config.json` or `.env`.
- **Use Fixtures**: Avoid using `time.sleep()`. Let Playwright's auto-wait and our custom `retry_operation` handle visibility.

---

*For further support, contact the QA Automation Team.*
