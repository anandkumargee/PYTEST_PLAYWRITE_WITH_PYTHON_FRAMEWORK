import allure
import pytest
from pages.login_page import LoginPage
from utils.logger import setup_logger

logger = setup_logger("LoginTest")

@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regression
def test_login_with_config_data(login_page, env_config):
    """Verify login functionality using credentials from config.json."""
    logger.info("Starting login test with ConfigManager data")
    
    # Get credentials from env_config (ConfigManager)
    credentials = env_config.get("user_credentials")
    username = credentials.get("username")
    password = credentials.get("password")
    
    logger.info(f"Attempting login for user: {username}")
    login_page.login_to_the_application(username, password)
    
    # Verify success
    assert login_page.is_login_successful(), "Login failed - dashboard not visible"
    logger.info(f"Successfully logged in with user: {username} from config.json")

@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.ui
def test_login_page_title(page, login_page):
    """Verify that the login page loads with the correct title."""
    assert "OrangeHRM" in page.title()
    logger.info("Successfully verified login page title.")