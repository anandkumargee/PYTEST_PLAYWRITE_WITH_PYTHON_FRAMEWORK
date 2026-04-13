from playwright.sync_api import Page, expect
import logging
import allure
from datetime import datetime
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

    @allure.step("Selecting option '{value}/{label}/{index}' from: {selector}")
    def select_option(self, selector: str, value: str = None, label: str = None, index: int = None, timeout: int = None):
        t = timeout if timeout is not None else self.default_timeout
        self.logger.info(f"Selecting option from: {selector}")
        def _select_action():
            self.page.locator(selector).scroll_into_view_if_needed()
            if value:
                self.page.select_option(selector, value=value, timeout=t)
            elif label:
                self.page.select_option(selector, label=label, timeout=t)
            elif index is not None:
                self.page.select_option(selector, index=index, timeout=t)
        retry_operation(_select_action)

    @allure.step("Checking checkbox: {selector}")
    def check(self, selector: str, timeout: int = None):
        t = timeout if timeout is not None else self.default_timeout
        self.logger.info(f"Checking checkbox: {selector}")
        def _check_action():
            self.page.locator(selector).scroll_into_view_if_needed()
            self.page.check(selector, timeout=t)
        retry_operation(_check_action)

    @allure.step("Unchecking checkbox: {selector}")
    def uncheck(self, selector: str, timeout: int = None):
        t = timeout if timeout is not None else self.default_timeout
        self.logger.info(f"Unchecking checkbox: {selector}")
        def _uncheck_action():
            self.page.locator(selector).scroll_into_view_if_needed()
            self.page.uncheck(selector, timeout=t)
        retry_operation(_uncheck_action)

    @allure.step("Hovering over element: {selector}")
    def hover(self, selector: str, timeout: int = None):
        t = timeout if timeout is not None else self.default_timeout
        self.logger.info(f"Hovering over: {selector}")
        def _hover_action():
            self.page.locator(selector).scroll_into_view_if_needed()
            self.page.hover(selector, timeout=t)
        retry_operation(_hover_action)

    @allure.step("Double clicking element: {selector}")
    def double_click(self, selector: str, timeout: int = None):
        t = timeout if timeout is not None else self.default_timeout
        self.logger.info(f"Double clicking: {selector}")
        def _double_click_action():
            self.page.locator(selector).scroll_into_view_if_needed()
            self.page.dblclick(selector, timeout=t)
        retry_operation(_double_click_action)

    @allure.step("Right clicking element: {selector}")
    def right_click(self, selector: str, timeout: int = None):
        t = timeout if timeout is not None else self.default_timeout
        self.logger.info(f"Right clicking: {selector}")
        def _right_click_action():
            self.page.locator(selector).scroll_into_view_if_needed()
            self.page.click(selector, button="right", timeout=t)
        retry_operation(_right_click_action)

    @allure.step("Dragging {source} to {target}")
    def drag_and_drop(self, source: str, target: str, timeout: int = None):
        t = timeout if timeout is not None else self.default_timeout
        self.logger.info(f"Dragging from {source} to {target}")
        def _drag_action():
            self.page.drag_and_drop(source, target, timeout=t)
        retry_operation(_drag_action)

    @allure.step("Pressing key '{key}' on: {selector}")
    def press_key(self, selector: str, key: str, timeout: int = None):
        t = timeout if timeout is not None else self.default_timeout
        self.logger.info(f"Pressing {key} on {selector}")
        def _press_action():
            self.page.press(selector, key, timeout=t)
        retry_operation(_press_action)

    @allure.step("Checking if '{selector}' is checked")
    def is_checked(self, selector: str, timeout: int = None) -> bool:
        t = timeout if timeout is not None else self.default_timeout
        return self.page.is_checked(selector, timeout=t)

    @allure.step("Getting attribute '{attribute_name}' from: {selector}")
    def get_attribute(self, selector: str, attribute_name: str, timeout: int = None) -> str:
        t = timeout if timeout is not None else self.default_timeout
        self.page.locator(selector).scroll_into_view_if_needed()
        return self.page.get_attribute(selector, attribute_name, timeout=t)

    @allure.step("Getting all text contents from: {selector}")
    def get_all_texts(self, selector: str) -> list:
        return self.page.locator(selector).all_text_contents()

    @allure.step("Accessing iframe: {iframe_selector}")
    def get_iframe(self, iframe_selector: str):
        self.logger.info(f"Getting frame locator for: {iframe_selector}")
        return self.page.frame_locator(iframe_selector)

    def wait_for_new_tab(self):
        """Context manager to handle actions that open a new tab."""
        self.logger.info("Waiting for a new tab/window to open...")
        return self.page.context.expect_page()

    @allure.step("Reloading page")
    def reload(self):
        self.logger.info("Reloading current page")
        self.page.reload()

    @allure.step("Going back")
    def go_back(self):
        self.logger.info("Navigating back")
        self.page.go_back()

    @allure.step("Going forward")
    def go_forward(self):
        self.logger.info("Navigating forward")
        self.page.go_forward()

    @allure.step("Accepting alert")
    def accept_alert(self, prompt_text: str = None):
        self.logger.info("Accepting browser alert")
        def _handle_dialog(dialog):
            dialog.accept(prompt_text)
        self.page.once("dialog", _handle_dialog)

    @allure.step("Dismissing alert")
    def dismiss_alert(self):
        self.logger.info("Dismissing browser alert")
        self.page.once("dialog", lambda dialog: dialog.dismiss())

    @allure.step("Taking screenshot: {name}")
    def take_screenshot(self, name: str):
        path = f"reports/playwright-artifacts/{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        self.page.screenshot(path=path)
        allure.attach.file(path, name=name, attachment_type=allure.attachment_type.PNG)
        self.logger.info(f"Screenshot saved to: {path}")

    @allure.step("Executing JavaScript")
    def execute_script(self, script: str, *args):
        return self.page.evaluate(script, *args)

    @allure.step("Switching to tab with title: {title}")
    def switch_to_tab_by_title(self, title: str):
        for page in self.page.context.pages:
            if title in page.title():
                page.bring_to_front()
                self.page = page
                return
        raise Exception(f"Tab with title '{title}' not found.")

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
