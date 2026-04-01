from pages.base_page import BasePage
import allure

class DashboardPage(BasePage):
    # Selectors
    HEADER = "//h6[contains(@class, 'oxd-topbar-header-breadcrumb-module')]"
    USER_DROPDOWN = "//span[@class='oxd-userdropdown-tab']"
    LOGOUT_LINK = "//a[text()='Logout']"
    MENU_ITEMS = "//nav[@aria-label='Sidepanel']//ul/li"
    
    # Dashboard specific locators
    ASSIGN_LEAVE = "//button[@title='Assign Leave']"
    TYPE_FOR_HINTS = "//input[@placeholder='Type for hints...']"
    #other tab
    APPLY_LEAVE_TAB  = "//a[text()='Apply']"
    LEAVE_FROM_DATE = "//input[@placeholder='yyyy-dd-mm']"
    
    @allure.step("Verifying Assign Leave functionality")
    def verify_assign_leave(self):
        self.is_visible(self.ASSIGN_LEAVE)
        self.click(self.ASSIGN_LEAVE)
        self.is_visible(self.TYPE_FOR_HINTS)
        self.type_text(self.TYPE_FOR_HINTS, "John Doe")

    @allure.step("Verifying Dashboard Header is visible")
    def is_header_visible(self) -> bool:
        return self.is_visible(self.HEADER)

    @allure.step("Getting the header title")
    def get_header_title(self) -> str:
        return self.get_text(self.HEADER)

    @allure.step("Logging out from Dashboard")
    def logout(self):
        self.click(self.USER_DROPDOWN)
        self.click(self.LOGOUT_LINK)

    @allure.step("Verify all leave tabs")
    def verify_leave_tabs(self):
        self.click(self.APPLY_LEAVE_TAB)
        self.is_visible(self.LEAVE_FROM_DATE)

