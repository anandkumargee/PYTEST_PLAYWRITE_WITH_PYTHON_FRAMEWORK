from playwright.sync_api import Page, expect
import logging
import allure
from utils.retry_util import retry_operation

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)
        # Get timeout from config, fallback to 10000 if not found
        self.default_timeout = getattr(self.page, "env_config", {}).get("timeout", 30000)

    @allure.step("Navigate to: {path}")
    def navigate(self, path: str = ""):
        self.logger.info(f"Navigating to: {path}")
        self.page.goto(path)

    @allure.step("Clicking element: {selector}")
    def click(self, selector: str, timeout: int = None):
        t = timeout if timeout is not None else self.default_timeout
        self.logger.info(f"Clicking element: {selector}")
        def _click_action():
            self.page.locator(selector).scroll_into_view_if_needed()
            self.page.click(selector, timeout=t)
        retry_operation(_click_action)

    @allure.step("Typing '{text}' into: {selector}")
    def type_text(self, selector: str, text: str, timeout: int = None):
        t = timeout if timeout is not None else self.default_timeout
        self.logger.info(f"Typing '{text}' into: {selector}")
        def _type_action():
            self.page.locator(selector).scroll_into_view_if_needed()
            self.page.fill(selector, text, timeout=t)
        retry_operation(_type_action)

    @allure.step("Getting text from: {selector}")
    def get_text(self, selector: str, timeout: int = None) -> str:
        t = timeout if timeout is not None else self.default_timeout
        self.page.locator(selector).scroll_into_view_if_needed()
        return self.page.locator(selector).inner_text(timeout=t)

    @allure.step("Waiting for selector: {selector}")
    def wait_for_selector(self, selector: str, state="visible", timeout=None):
        t = timeout if timeout is not None else self.default_timeout
        self.page.wait_for_selector(selector, state=state, timeout=t)
        self.page.locator(selector).scroll_into_view_if_needed()

    @allure.step("Checking visibility of: {selector}")
    def is_visible(self, selector: str, timeout: int = None) -> bool:
        t = timeout if timeout is not None else self.default_timeout
        try:
            self.logger.info(f"Checking visibility of: {selector} with timeout: {t}")
            self.page.wait_for_selector(selector, state="visible", timeout=t)
            self.page.locator(selector).scroll_into_view_if_needed()
            return True
        except Exception:
            return False

    def handle_iframe(self, iframe_selector: str):
        return self.page.frame_locator(iframe_selector)

    @allure.step("Smart clicking element: {selector}")
    def smart_click(self, selector: str, alt_selectors: list = None, timeout: int = None):
        """Try to click an element, optionally trying alternative selectors if the primary fails."""
        t = timeout if timeout is not None else self.default_timeout
        selectors = [selector] + (alt_selectors or [])
        for sel in selectors:
            try:
                self.logger.info(f"Attempting smart click on: {sel}")
                def _smart_click_action():
                    self.page.locator(sel).scroll_into_view_if_needed()
                    self.page.click(sel, timeout=t // len(selectors))
                retry_operation(_smart_click_action)
                return
            except Exception as e:
                self.logger.warning(f"Failed to click {sel}: {e}")
        raise Exception(f"Could not click any of the selectors: {selectors}")

    def handle_new_tab(self):
        with self.page.context.expect_page() as new_page_info:
            yield new_page_info.value
