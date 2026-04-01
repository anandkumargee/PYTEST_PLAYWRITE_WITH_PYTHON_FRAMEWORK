from pages.base_page import BasePage
import allure

class LoginPage(BasePage):
    # Flexible locators for OrangeHRM
    USERNAME_INPUT = "//input[@name='username']"
    PASSWORD_INPUT = "//input[@name='password']"
    LOGIN_BUTTON = "//button[@type='submit']"
    DASHBOARD_SIDE_BTN = '//a[@href="/web/index.php/dashboard/index"]'
    
    # Selectors

    @allure.step("Navigating to OrangeHRM Login Page")
    def navigate_to_login(self):
        self.navigate("")
        # Wait for the form to be ready
        self.is_visible(self.USERNAME_INPUT, timeout=self.default_timeout)

    @allure.step("Logging in with user: {username}")
    def login_to_the_application(self, username, password):
        self.logger.info(f"Logging in with user: {username}")
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        self.is_visible(self.DASHBOARD_SIDE_BTN, timeout=self.default_timeout)
        
    def is_login_successful(self):
        return self.is_visible(self.DASHBOARD_SIDE_BTN)

