import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.logger import setup_logger

logger = setup_logger("DashboardTest")

@pytest.fixture(scope="module")
def dashboard(context, env_config) -> DashboardPage:
    """Module-level setup: Login once using credentials from config.json."""
    logger.info("Suite Setup: Performing login for dashboard tests")
    
    credentials = env_config.get("user_credentials")
    username = credentials.get("username")
    password = credentials.get("password")
    
    # Create module-level page
    page = context.new_page()
    
    # Login process
    login_page = LoginPage(page)
    login_page.navigate_to_login()
    login_page.login_to_the_application(username, password)
    
    dashboard_page = DashboardPage(page)
    assert dashboard_page.is_header_visible(), "Dashboard header not visible after login"
    
    yield dashboard_page
    
    # Cleanup: close module-level page
    page.close()

@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Dashboard functionality")
@pytest.mark.dashboard
@pytest.mark.ui
def test_dashboard_header(dashboard: DashboardPage):
    """Verify the dashboard header text."""
    title = dashboard.get_header_title()
    assert title == "Dashboard", f"Expected header 'Dashboard' but got '{title}'"
    logger.info("Successfully verified Dashboard header.")

@allure.severity(allure.severity_level.NORMAL)
@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Assign Leave")
@pytest.mark.dashboard
def test_assign_leave_functionality(dashboard: DashboardPage):
    """Verify that the Assign Leave functionality is accessible."""
    dashboard.verify_assign_leave()
    logger.info("Successfully verified Assign Leave functionality access.")

@allure.severity(allure.severity_level.TRIVIAL)
@allure.feature("Verify all leave tabs")
@pytest.mark.dashboard
def test_verify_all_leave_tabs(dashboard: DashboardPage):
    """Verify that the Assign Leave functionality is accessible."""
    dashboard.verify_leave_tabs()
    logger.info("Successfully verified Assign Leave functionality access.")
