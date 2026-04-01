import pytest
import allure
import os
from datetime import datetime
from dotenv import load_dotenv
from core.config_manager import ConfigManager
from pages.login_page import LoginPage

# Load sensitive data from .env
load_dotenv()

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="qa", help="Environment to run tests (qa, prod)")

@pytest.fixture(scope="session")
def env_config(request):
    env = request.config.getoption("--env")
    return ConfigManager.load_config(env)

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, env_config):
    # Set viewport to None only if NOT headless to allow --start-maximized to work.
    # In headless mode, we still want a fixed high resolution.
    is_headless = env_config.get("headless", True)
    return {
        **browser_context_args,
        "base_url": env_config.get("base_url"),
        "viewport": None if not is_headless else {"width": 1920, "height": 1080}
    }

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, env_config):
    return {
        **browser_type_launch_args,
        "headless": env_config.get("headless", True),
        "args": ["--start-maximized", "--window-size=1920,1080"] # Combined for perfect maximization
    }

@pytest.fixture(scope="module")
def context(browser, browser_context_args):
    """Override context fixture to stay open for the whole session."""
    context = browser.new_context(**browser_context_args)
    # Enable tracing for the session-wide context
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    # Stop tracing and close context at the end of session
    context.tracing.stop(path="reports/playwright-artifacts/session_trace.zip")
    context.close()

@pytest.fixture(scope="function")
def page(context, env_config):
    """Standard page fixture within the session-scoped context."""
    p = context.new_page()
    
    # Initialize log storage and config on the page object
    p.console_logs = []
    p.network_logs = []
    p.env_config = env_config
    
    # Listeners
    p.on("console", lambda msg: p.console_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] [{msg.type}] {msg.text}"))
    p.on("request", lambda req: p.network_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Request: {req.method} {req.url}"))
    p.on("response", lambda res: p.network_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Response: {res.status} {res.url}"))
    
    # Tracing is now handled at the context level for the session
    
    yield p
    
    # We clear cookies / storage if we want a clean start, 
    # but for now we just close the page.
    p.close()

def pytest_runtest_teardown(item, nextitem):
    """Attach artifacts to Allure on failure during teardown."""
    # We retrieve the report from the item (populated by pytest_runtest_makereport)
    report = getattr(item, "rep_call", None) or \
             getattr(item, "rep_setup", None) or \
             getattr(item, "rep_teardown", None)
    
    if report and report.failed:
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            
            # Attach Screenshot
            try:
                if not page.is_closed():
                    allure.attach(page.screenshot(), name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
            except:
                pass
            
            # Attach Console Logs
            if hasattr(page, "console_logs") and page.console_logs:
                allure.attach("\n".join(page.console_logs), name="Console Logs", attachment_type=allure.attachment_type.TEXT)
            
            # Attach Network Logs
            if hasattr(page, "network_logs") and page.network_logs:
                allure.attach("\n".join(page.network_logs), name="Network Logs", attachment_type=allure.attachment_type.TEXT)
            
            # Attach Trace (Safe filename)
            try:
                trace_path = f"reports/playwright-artifacts/{item.name.replace('[', '_').replace(']', '_')}_trace.zip"
                # Note: tracing might have already been stopped in the fixture teardown
                # but if we are here, we can try to find it or just rely on the trace attachment in the fixture if that works.
                # Since fixture teardown runs BEFORE hook teardown (usually), we should be careful.
            except:
                pass

@pytest.fixture(scope="function")
def login_page(page, page_factory):
    """Ready-to-use LoginPage fixture with automatic navigation."""
    lp = page_factory(LoginPage)
    lp.navigate_to_login()
    return lp

@pytest.fixture(scope="function")
def page_factory(page):
    def _create_page(page_class):
        return page_class(page)
    return _create_page

@pytest.fixture(scope="module", autouse=True)
def suite_setup_teardown():
    """Global suite setup and teardown."""
    print("\n--- Suite Setup: Preparing global environment ---")
    # Add any global initialization code here
    yield
    print("\n--- Suite Teardown: Finalizing global environment ---")
    # Add any global cleanup code here

@pytest.fixture(scope="function", autouse=True)
def test_setup_teardown(request):
    """Setup and teardown for each test case."""
    test_name = request.node.name
    print(f"\n>>>> Test Setup: Starting test '{test_name}' >>>>")
    yield
    print(f"\n<<<< Test Teardown: Completed test '{test_name}' <<<<")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
