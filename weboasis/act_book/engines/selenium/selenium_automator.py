"""
Selenium Automator - Implements BrowserAutomator interface for Selenium operations
"""
import time
import logging
from typing import Optional, Union, List, Literal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, ElementNotInteractableException,
    StaleElementReferenceException, WebDriverException
)

from weboasis.act_book.core.automator_interface import BrowserAutomator

logger = logging.getLogger(__name__)


class SeleniumAutomator(BrowserAutomator):
    """Selenium implementation of BrowserAutomator with abstract attributes."""
    
    def __init__(self):
        """
        Initialize the Selenium automator with abstract attributes.
        
        The actual _driver and _test_id_attribute will be set by the manager
        that inherits from this class.
        """
        # Abstract attributes - will be set by the manager
        self._driver = None
        self._demo_mode = "off"
        self._test_id_attribute = None
    
    def set_driver(self, driver: webdriver.Remote) -> None:
        """Set the WebDriver instance."""
        self._driver = driver
        logger.info("WebDriver set in SeleniumAutomator")
    
    def set_test_id_attribute(self, test_id_attribute: str) -> None:
        """Set the test ID attribute."""
        self._test_id_attribute = test_id_attribute
        logger.info(f"Test ID attribute set to: {test_id_attribute}")
    
    @property
    def driver(self) -> Optional[webdriver.Remote]:
        """Get the WebDriver instance."""
        return self._driver
    
    @property
    def test_id_attribute(self) -> Optional[str]:
        """Get the test ID attribute."""
        return self._test_id_attribute
    
    def _demo_mode_action(self, action_name: str, **kwargs) -> bool:
        """Handle demo mode actions."""
        if self._demo_mode == "on":
            logger.info(f"[DEMO MODE] {action_name}: {kwargs}")
            time.sleep(0.5)  # Simulate action delay
            return True
        return False
    
    # Helper methods for element finding and interaction
    def _find_element(self, selector: str = None, test_id: str = None, timeout: int = 10000):
        """Find element by selector or test_id."""
        wait = WebDriverWait(self._driver, timeout / 1000)
        
        try:
            if test_id:
                # Find by test_id (custom attribute)
                if self._test_id_attribute:
                    element = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, f'[{self._test_id_attribute}="{test_id}"]'))
                    )
                else:
                    logger.warning("test_id_attribute not set, cannot find element by test_id")
                    return None
            elif selector:
                # Find by selector
                element = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
            else:
                raise ValueError("Either selector or test_id must be provided")
            
            return element
        except TimeoutException:
            logger.error(f"Element not found: selector={selector}, test_id={test_id}")
            return None
    
    def _wait_for_interactable(self, element, timeout: int = 10000) -> bool:
        """Wait for element to be interactable."""
        wait = WebDriverWait(self._driver, timeout / 1000)
        
        try:
            # Wait for element to be clickable using the element directly
            wait.until(EC.element_to_be_clickable(element))
            return True
        except TimeoutException:
            logger.warning(f"Element not interactable within {timeout}ms")
            return False
    
    # BrowserAutomator interface methods
    def click(self, selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Click an element by selector or test_id."""
        if self._demo_mode_action("click", selector=selector, test_id=test_id):
            return True
        
        try:
            element = self._find_element(selector, test_id)
            if not element:
                return False
            
            if not self._wait_for_interactable(element):
                return False
            
            element.click()
            return True
        except Exception as e:
            logger.error(f"Click failed: {e}")
            return False
    
    def click_by_test_id(self, test_id: str, **kwargs) -> bool:
        return self.click(test_id=test_id, **kwargs)
    
    def fill(self, selector: str, text: str, **kwargs) -> bool:
        """Fill a form field by selector."""
        if self._demo_mode_action("fill", selector=selector, text=text):
            return True
        
        try:
            element = self._find_element(selector=selector)
            if not element:
                return False
            
            if not self._wait_for_interactable(element):
                return False
            
            element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            logger.error(f"Fill failed: {e}")
            return False
    
    def fill_by_test_id(self, test_id: str, text: str, **kwargs) -> bool:
        """Fill a form field by test_id."""
        if self._demo_mode_action("fill_by_test_id", test_id=test_id, text=text):
            return True
        
        try:
            element = self._find_element(test_id=test_id)
            if not element:
                return False
            
            if not self._wait_for_interactable(element):
                return False
            
            element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            logger.error(f"Fill by test_id failed: {e}")
            return False
    
    def type_text(self, selector: str = None, text: str = "", test_id: str = None, **kwargs) -> bool:
        """Type text into an element by selector or test_id."""
        if self._demo_mode_action("type_text", selector=selector, text=text, test_id=test_id):
            return True
        
        try:
            element = self._find_element(selector, test_id)
            if not element:
                return False
            
            if not self._wait_for_interactable(element):
                return False
            
            element.send_keys(text)
            return True
        except Exception as e:
            logger.error(f"Type text failed: {e}")
            return False
    
    def type_text_by_test_id(self, test_id: str, text: str, **kwargs) -> bool:
        return self.type_text(test_id=test_id, text=text, **kwargs)
    
    def hover(self, selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Hover over an element by selector or test_id."""
        if self._demo_mode_action("hover", selector=selector, test_id=test_id):
            return True
        
        try:
            element = self._find_element(selector, test_id)
            if not element:
                return False
            
            actions = ActionChains(self._driver)
            actions.move_to_element(element).perform()
            return True
        except Exception as e:
            logger.error(f"Hover failed: {e}")
            return False
    
    def hover_by_test_id(self, test_id: str, **kwargs) -> bool:
        return self.hover(test_id=test_id, **kwargs)
    
    def double_click(self, selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Double click an element by selector or test_id."""
        if self._demo_mode_action("double_click", selector=selector, test_id=test_id):
            return True
        
        try:
            element = self._find_element(selector, test_id)
            if not element:
                return False
            
            if not self._wait_for_interactable(element):
                return False
            
            actions = ActionChains(self._driver)
            actions.double_click(element).perform()
            return True
        except Exception as e:
            logger.error(f"Double click failed: {e}")
            return False
    
    def double_click_by_test_id(self, test_id: str, **kwargs) -> bool:
        return self.double_click(test_id=test_id, **kwargs)
    
    def check(self, selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Check a checkbox by selector or test_id."""
        if self._demo_mode_action("check", selector=selector, test_id=test_id):
            return True
        
        try:
            element = self._find_element(selector, test_id)
            if not element:
                return False
            
            if not self._wait_for_interactable(element):
                return False
            
            if not element.is_selected():
                element.click()
            return True
        except Exception as e:
            logger.error(f"Check failed: {e}")
            return False
    
    def check_by_test_id(self, test_id: str, **kwargs) -> bool:
        return self.check(test_id=test_id, **kwargs)
    
    def uncheck(self, selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Uncheck a checkbox by selector or test_id."""
        if self._demo_mode_action("uncheck", selector=selector, test_id=test_id):
            return True
        
        try:
            element = self._find_element(selector, test_id)
            if not element:
                return False
            
            if not self._wait_for_interactable(element):
                return False
            
            if element.is_selected():
                element.click()
            return True
        except Exception as e:
            logger.error(f"Uncheck failed: {e}")
            return False
    
    def uncheck_by_test_id(self, test_id: str, **kwargs) -> bool:
        return self.uncheck(test_id=test_id, **kwargs)
    
    def select_option(self, selector: str, value: str, **kwargs) -> bool:
        """Select option from a dropdown by selector."""
        if self._demo_mode_action("select_option", selector=selector, value=value):
            return True
        
        try:
            element = self._find_element(selector=selector)
            if not element:
                return False
            
            if not self._wait_for_interactable(element):
                return False
            
            select = Select(element)
            select.select_by_value(value)
            return True
        except Exception as e:
            logger.error(f"Select option failed: {e}")
            return False
    
    def select_option_by_test_id(self, test_id: str, value: str, **kwargs) -> bool:
        """Select option from a dropdown by test_id."""
        if self._demo_mode_action("select_option_by_test_id", test_id=test_id, value=value):
            return True
        
        try:
            element = self._find_element(test_id=test_id)
            if not element:
                return False
            
            if not self._wait_for_interactable(element):
                return False
            
            select = Select(element)
            # Use select_by_visible_text since the value parameter is actually the visible text
            select.select_by_visible_text(value)
            return True
        except Exception as e:
            logger.error(f"Select option by test_id failed: {e}")
            return False
    
    def navigate(self, url: str, **kwargs) -> bool:
        """Navigate to a URL."""
        if self._demo_mode_action("navigate", url=url):
            return True
        
        try:
            self._driver.get(url)
            return True
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            return False
    
    def go_back(self, **kwargs) -> bool:
        """Go back in browser history."""
        if self._demo_mode_action("go_back"):
            return True
        
        try:
            self._driver.back()
            return True
        except Exception as e:
            logger.error(f"Go back failed: {e}")
            return False
    
    def go_forward(self, **kwargs) -> bool:
        """Go forward in browser history."""
        if self._demo_mode_action("go_forward"):
            return True
        
        try:
            self._driver.forward()
            return True
        except Exception as e:
            logger.error(f"Go forward failed: {e}")
            return False
    
    def refresh(self, **kwargs) -> bool:
        """Refresh the current page."""
        if self._demo_mode_action("refresh"):
            return True
        
        try:
            self._driver.refresh()
            return True
        except Exception as e:
            logger.error(f"Refresh failed: {e}")
            return False
    
    
    def wait_for_load_state(self, state: str = "networkidle", timeout: int = 30000, **kwargs) -> bool:
        """Wait for specific load state (Selenium equivalent of Playwright's wait_for_load_state)."""
        try:
            if self._demo_mode_action("wait_for_load_state", state=state, timeout=timeout, **kwargs):
                return True
            
            if state == "networkidle":
                # Wait for network to be idle (simplified implementation)
                time.sleep(1)  # Basic wait
                return True
            elif state == "domcontentloaded":
                # Wait for DOM content loaded
                WebDriverWait(self._driver, timeout / 1000).until(
                    lambda driver: driver.execute_script("return document.readyState") in ["interactive", "complete"]
                )
                return True
            else:
                # Default to complete
                return self.wait_for_load(timeout, **kwargs)
        except Exception as e:
            logger.error(f"Wait for load state failed: {e}")
            return False
    
    def new_tab(self, **kwargs) -> bool:
        """Open a new tab."""
        try:
            if self._demo_mode_action("new_tab", **kwargs):
                return True
            
            # Open new tab using JavaScript
            self._driver.execute_script("window.open('', '_blank');")
            return True
        except Exception as e:
            logger.error(f"New tab failed: {e}")
            return False
    
    def close_tab(self, **kwargs) -> bool:
        """Close the current tab."""
        try:
            if self._demo_mode_action("close_tab", **kwargs):
                return True
            
            self._driver.close()
            return True
        except Exception as e:
            logger.error(f"Close tab failed: {e}")
            return False
    
    def focus_tab(self, index: int, **kwargs) -> bool:
        """Focus on a specific tab by index."""
        try:
            if self._demo_mode_action("focus_tab", index=index, **kwargs):
                return True
            
            # Switch to tab by index
            if 0 <= index < len(self._driver.window_handles):
                self._driver.switch_to.window(self._driver.window_handles[index])
                return True
            return False
        except Exception as e:
            logger.error(f"Focus tab failed: {e}")
            return False
    
    def tab_close(self, **kwargs) -> bool:
        """Close the current tab (alias for close_tab)."""
        return self.close_tab(**kwargs)
    
    def tab_focus(self, index: int, **kwargs) -> bool:
        """Focus on a specific tab by index (alias for focus_tab)."""
        return self.focus_tab(index, **kwargs)
    
    def mouse_click(self, x: float, y: float, **kwargs) -> bool:
        """Click at specific coordinates."""
        try:
            if self._demo_mode_action("mouse_click", x=x, y=y, **kwargs):
                return True
            
            actions = ActionChains(self._driver)
            actions.move_by_offset(x, y).click().perform()
            return True
        except Exception as e:
            logger.error(f"Mouse click failed: {e}")
            return False
    
    def mouse_move(self, x: float, y: float, **kwargs) -> bool:
        """Move mouse to specific coordinates."""
        try:
            if self._demo_mode_action("mouse_move", x=x, y=y, **kwargs):
                return True
            
            actions = ActionChains(self._driver)
            actions.move_by_offset(x, y).perform()
            return True
        except Exception as e:
            logger.error(f"Mouse move failed: {e}")
            return False
    
    def scroll(self, delta_x: float, delta_y: float, **kwargs) -> bool:
        """Scroll the page by delta values."""
        try:
            if self._demo_mode_action("scroll", delta_x=delta_x, delta_y=delta_y, **kwargs):
                return True
            
            self._driver.execute_script(f"window.scrollBy({delta_x}, {delta_y});")
            return True
        except Exception as e:
            logger.error(f"Scroll failed: {e}")
            return False

    def scroll_around_element(
        self,
        selector: str = None,
        test_id: str = None,
        delta_x: float = 0,
        delta_y: float = 300,
        **kwargs,
    ) -> bool:
        """Dispatch a wheel event at the element's center (lets browser choose the scroller)."""
        try:
            if self._demo_mode_action(
                "scroll_around_element",
                selector=selector,
                test_id=test_id,
                delta_x=delta_x,
                delta_y=delta_y,
                **kwargs,
            ):
                return True

            element = self._find_element(selector, test_id)
            if not element:
                return False
            # Use JS to dispatch a WheelEvent at the element center
            js = """
                const el = arguments[0];
                const dx = arguments[1];
                const dy = arguments[2];
                const rect = el.getBoundingClientRect();
                const cx = rect.left + rect.width / 2;
                const cy = rect.top + rect.height / 2;
                const evt = new WheelEvent('wheel', {
                    deltaX: dx,
                    deltaY: dy,
                    clientX: cx,
                    clientY: cy,
                    bubbles: true,
                    cancelable: true,
                    view: window
                });
                const target = document.elementFromPoint(cx, cy) || el;
                return target.dispatchEvent(evt);
            """
            ok = self._driver.execute_script(js, element, float(delta_x), float(delta_y))
            return bool(ok)
        except Exception as e:
            logger.error(f"scroll_around_element failed: {e}")
            return False

    def scroll_from_position(
        self,
        x: float,
        y: float,
        delta_x: float = 0,
        delta_y: float = 300,
        **kwargs,
    ) -> bool:
        """Dispatch a wheel event at absolute viewport position (x, y)."""
        try:
            if self._demo_mode_action("scroll_from_position", x=x, y=y, delta_x=delta_x, delta_y=delta_y, **kwargs):
                return True

            js = """
                const x = arguments[0];
                const y = arguments[1];
                const dx = arguments[2];
                const dy = arguments[3];
                const target = document.elementFromPoint(x, y) || document.body;
                const evt = new WheelEvent('wheel', {
                    deltaX: dx,
                    deltaY: dy,
                    clientX: x,
                    clientY: y,
                    bubbles: true,
                    cancelable: true,
                    view: window
                });
                return target.dispatchEvent(evt);
            """
            ok = self._driver.execute_script(js, float(x), float(y), float(delta_x), float(delta_y))
            return bool(ok)
        except Exception as e:
            logger.error(f"scroll_from_position failed: {e}")
            return False

    
    def keyboard_type(self, text: str, **kwargs) -> bool:
        """Type text using keyboard."""
        try:
            if self._demo_mode_action("keyboard_type", text=text, **kwargs):
                return True
            
            actions = ActionChains(self._driver)
            actions.send_keys(text).perform()
            return True
        except Exception as e:
            logger.error(f"Keyboard type failed: {e}")
            return False
    
    def keyboard_press(self, key: str, **kwargs) -> bool:
        """Press a keyboard key."""
        try:
            if self._demo_mode_action("keyboard_press", key=key, **kwargs):
                return True
            
            actions = ActionChains(self._driver)
            actions.send_keys(key).perform()
            return True
        except Exception as e:
            logger.error(f"Keyboard press failed: {e}")
            return False
    
    def press(self, selector: str = None, key: str = None, test_id: str = None, **kwargs) -> bool:
        """Press a key on an element."""
        try:
            if self._demo_mode_action("press", selector=selector, key=key, test_id=test_id, **kwargs):
                return True
            
            element = self._find_element(selector, test_id)
            if element and self._wait_for_interactable(element):
                element.send_keys(key)
                return True
            return False
        except Exception as e:
            logger.error(f"Press failed: {e}")
            return False
    
    def press_by_test_id(self, test_id: str, key: str, **kwargs) -> bool:
        return self.press(test_id=test_id, key=key, **kwargs)
    
    def focus(self, selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Focus on an element."""
        try:
            if self._demo_mode_action("focus", selector=selector, test_id=test_id, **kwargs):
                return True
            
            element = self._find_element(selector, test_id)
            if element and self._wait_for_interactable(element):
                element.click()  # Click to focus
                return True
            return False
        except Exception as e:
            logger.error(f"Focus failed: {e}")
            return False
    
    def focus_by_test_id(self, test_id: str, **kwargs) -> bool:
        return self.focus(test_id=test_id, **kwargs)
    
    def clear(self, selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Clear the content of an element."""
        try:
            if self._demo_mode_action("clear", selector=selector, test_id=test_id, **kwargs):
                return True
            
            element = self._find_element(selector, test_id)
            if element and self._wait_for_interactable(element):
                element.clear()
                return True
            return False
        except Exception as e:
            logger.error(f"Clear failed: {e}")
            return False
    
    def clear_by_test_id(self, test_id: str, **kwargs) -> bool:
        return self.clear(test_id=test_id, **kwargs)

    # test_id alias helpers (for repos using test_id naming)
    def clear_by_test_id(self, test_id: str, **kwargs) -> bool:
        return self.clear(test_id=test_id, **kwargs)
    
    def set_attribute(self, selector: str = None, attribute: str = "", value: str = "", test_id: str = None, **kwargs) -> bool:
        """Set attribute value on an element."""
        try:
            if self._demo_mode_action("set_attribute", selector=selector, attribute=attribute, value=value, test_id=test_id, **kwargs):
                return True
            
            element = self._find_element(selector, test_id)
            if element:
                self._driver.execute_script(f'arguments[0].setAttribute("{attribute}", "{value}");', element)
                return True
            return False
        except Exception as e:
            logger.error(f"Set attribute failed: {e}")
            return False
    
    def set_attribute_by_test_id(self, test_id: str, attribute: str, value: str, **kwargs) -> bool:
        return self.set_attribute(test_id=test_id, attribute=attribute, value=value, **kwargs)
    
    def wait_for_element(self, selector: str, timeout: int = 30000, **kwargs) -> bool:
        """Wait for an element to appear."""
        try:
            if self._demo_mode_action("wait_for_element", selector=selector, timeout=timeout, **kwargs):
                return True
            
            wait = WebDriverWait(self._driver, timeout / 1000)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            return True
        except Exception as e:
            logger.error(f"Wait for element failed: {e}")
            return False
    
    def wait_for_element_by_test_id(self, test_id: str, timeout: int = 30000, **kwargs) -> bool:
        return self.wait_for_element(test_id=test_id, timeout=timeout, **kwargs)
    
    def upload_file(self, selector: str, file_path: str, **kwargs) -> bool:
        """Upload a file to an element."""
        try:
            if self._demo_mode_action("upload_file", selector=selector, file_path=file_path, **kwargs):
                return True
            
            element = self._find_element(selector)
            if element and self._wait_for_interactable(element):
                element.send_keys(file_path)
                return True
            return False
        except Exception as e:
            logger.error(f"Upload file failed: {e}")
            return False
    
    def upload_file_by_test_id(self, test_id: str, file_path: str, **kwargs) -> bool:
        return self.upload_file(test_id=test_id, file_path=file_path, **kwargs)
    
    def mouse_upload_file(self, x: float, y: float, file: str, **kwargs) -> bool:
        """Upload file by clicking at coordinates."""
        try:
            if self._demo_mode_action("mouse_upload_file", x=x, y=y, file=file, **kwargs):
                return True
            
            # Click at coordinates first
            self.mouse_click(x, y)
            # This would need more complex implementation for file dialog
            logger.warning("Mouse upload file not fully implemented for Selenium")
            return False
        except Exception as e:
            logger.error(f"Mouse upload file failed: {e}")
            return False
    
    def play_video(self, selector: str, **kwargs) -> bool:
        """Play a video element."""
        try:
            if self._demo_mode_action("play_video", selector=selector, **kwargs):
                return True
            
            element = self._find_element(selector)
            if element:
                self._driver.execute_script('arguments[0].play();', element)
                return True
            return False
        except Exception as e:
            logger.error(f"Play video failed: {e}")
            return False
    
    def play_video_by_test_id(self, test_id: str, **kwargs) -> bool:
        return self.play_video(test_id=test_id, **kwargs)
        
    def pause_video(self, selector: str, **kwargs) -> bool:
        """Pause a video element."""
        try:
            if self._demo_mode_action("pause_video", selector=selector, **kwargs):
                return True
            
            element = self._find_element(selector)
            if element:
                self._driver.execute_script('arguments[0].pause();', element)
                return True
            return False
        except Exception as e:
            logger.error(f"Pause video failed: {e}")
            return False
    
    def pause_video_by_test_id(self, test_id: str, **kwargs) -> bool:
        return self.pause_video(test_id=test_id, **kwargs)
    
    def get_text(self, selector: str, **kwargs) -> Optional[str]:
        """Get text content from an element by selector."""
        try:
            element = self._find_element(selector=selector)
            if element:
                return element.text
            return None
        except Exception as e:
            logger.error(f"Get text failed: {e}")
            return None
    
    def get_text_by_test_id(self, test_id: str, **kwargs) -> Optional[str]:
        """Get text content from an element by test_id."""
        try:
            element = self._find_element(test_id=test_id)
            if element:
                return element.text
            return None
        except Exception as e:
            logger.error(f"Get text by test_id failed: {e}")
            return None
    
    def get_attribute(self, selector: str, attribute: str, **kwargs) -> Optional[str]:
        """Get attribute value from an element by selector."""
        try:
            element = self._find_element(selector=selector)
            if element:
                return element.get_attribute(attribute)
            return None
        except Exception as e:
            logger.error(f"Get attribute failed: {e}")
            return None
    
    def get_attribute_by_test_id(self, test_id: str, attribute: str, **kwargs) -> Optional[str]:
        """Get attribute value from an element by test_id."""
        try:
            element = self._find_element(test_id=test_id)
            if element:
                return element.get_attribute(attribute)
            return None
        except Exception as e:
            logger.error(f"Get attribute by test_id failed: {e}")
            return None
    
    def get_current_url(self, **kwargs) -> Optional[str]:
        """Get the current URL."""
        try:
            return self._driver.current_url
        except Exception as e:
            logger.error(f"Get current URL failed: {e}")
            return None
    
    def get_page_title(self, **kwargs) -> Optional[str]:
        """Get the page title."""
        try:
            return self._driver.title
        except Exception as e:
            logger.error(f"Get page title failed: {e}")
            return None
    
    def get_page_source(self, **kwargs) -> Optional[str]:
        """Get the page source HTML."""
        try:
            return self._driver.page_source
        except Exception as e:
            logger.error(f"Get page source failed: {e}")
            return None
    
    def drag_and_drop(self, from_selector: str, to_selector: str, **kwargs) -> bool:
        """Drag and drop from one element to another using selectors."""
        try:
            if self._demo_mode_action("drag_and_drop", from_selector=from_selector, to_selector=to_selector, **kwargs):
                return True
            
            from_element = self._find_element(from_selector)
            to_element = self._find_element(to_selector)
            
            if from_element and to_element:
                actions = ActionChains(self._driver)
                actions.drag_and_drop(from_element, to_element).perform()
                return True
            return False
        except Exception as e:
            logger.error(f"Drag and drop failed: {e}")
            return False
    
    def drag_and_drop_by_test_id(self, from_test_id: str, to_test_id: str, **kwargs) -> bool:
        """Drag and drop from one element to another using test_ids."""
        try:
            if self._demo_mode_action("drag_and_drop_by_test_id", from_test_id=from_test_id, to_test_id=to_test_id, **kwargs):
                return True
            
            from_element = self._find_element(test_id=from_test_id)
            to_element = self._find_element(test_id=to_test_id)
            
            if from_element and to_element:
                actions = ActionChains(self._driver)
                actions.drag_and_drop(from_element, to_element).perform()
                return True
            return False
        except Exception as e:
            logger.error(f"Drag and drop by test_id failed: {e}")
            return False
    
    def element_exists(self, selector: str, **kwargs) -> bool:
        """Check if an element exists."""
        try:
            if self._demo_mode_action("element_exists", selector=selector, **kwargs):
                return True
            
            elements = self._driver.find_elements(By.CSS_SELECTOR, selector)
            return len(elements) > 0
        except Exception as e:
            logger.error(f"Element exists check failed: {e}")
            return False
    
    def is_visible(self, selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Check if an element is visible."""
        try:
            if self._demo_mode_action("is_visible", selector=selector, test_id=test_id, **kwargs):
                return True
            
            element = self._find_element(selector, test_id)
            if element:
                return element.is_displayed()
            return False
        except Exception as e:
            logger.error(f"Visibility check failed: {e}")
            return False
    
    def is_visible_by_test_id(self, test_id: str, **kwargs) -> bool:
        return self.is_visible(test_id=test_id, **kwargs)
    
    def find_element(self, selector: str, **kwargs):
        """Find an element by selector (alias for _find_element)."""
        return self._find_element(selector=selector)
    
    def find_elements(self, selector: str, **kwargs):
        """Find multiple elements by selector."""
        try:
            if self._demo_mode_action("find_elements", selector=selector, **kwargs):
                return []
            
            return self._driver.find_elements(By.CSS_SELECTOR, selector)
        except Exception as e:
            logger.error(f"Find elements failed: {e}")
            return []
    
    def submit_form(self, selector: str, **kwargs) -> bool:
        """Submit a form."""
        try:
            if self._demo_mode_action("submit_form", selector=selector, **kwargs):
                return True
            
            element = self._find_element(selector)
            if element:
                element.submit()
                return True
            return False
        except Exception as e:
            logger.error(f"Submit form failed: {e}")
            return False
    
    def get_elem_by_test_id(self, test_id: str, **kwargs):
        """Get element by test_id (alias for _find_element with test_id)."""
        return self._find_element(test_id=test_id)
    
    def wait_for_timeout(self, timeout: int, **kwargs):
        """Wait for a specified timeout (Selenium equivalent of Playwright's wait_for_timeout)."""
        try:
            if self._demo_mode_action("wait_for_timeout", timeout=timeout, **kwargs):
                return
            
            time.sleep(timeout / 1000)
        except Exception as e:
            logger.error(f"Wait for timeout failed: {e}")
    
    def wait_for_function(self, function_js: str, timeout: int = 30000, **kwargs):
        """Wait for a JavaScript function to return true (Selenium equivalent of Playwright's wait_for_function)."""
        try:
            if self._demo_mode_action("wait_for_function", function_js=function_js, timeout=timeout, **kwargs):
                return True
            
            wait = WebDriverWait(self._driver, timeout / 1000)
            wait.until(lambda driver: driver.execute_script(f"return ({function_js})"))
            return True
        except Exception as e:
            logger.error(f"Wait for function failed: {e}")
            return False
    
    def evaluate(self, function_js: str, *args, **kwargs):
        """Evaluate JavaScript function on the page (Selenium equivalent of Playwright's evaluate)."""
        try:
            if self._demo_mode_action("evaluate", function_js=function_js, *args, **kwargs):
                return None
            
            # Convert args to JavaScript arguments
            js_args = []
            for arg in args:
                if isinstance(arg, str):
                    js_args.append(f"'{arg}'")
                elif isinstance(arg, (int, float)):
                    js_args.append(str(arg))
                elif isinstance(arg, bool):
                    js_args.append(str(arg).lower())
                else:
                    js_args.append("null")
            
            # Execute the JavaScript function
            js_code = f"({function_js})({', '.join(js_args)})"
            return self._driver.execute_script(js_code)
        except Exception as e:
            logger.error(f"Evaluate failed: {e}")
            return None
    
    def goto(self, url: str, **kwargs) -> bool:
        """Navigate to a URL (alias for navigate)."""
        return self.navigate(url, **kwargs)
    
    def wait_for_selector(self, selector: str, timeout: int = 30000, **kwargs) -> bool:
        """Wait for a selector to appear (alias for wait_for_element)."""
        return self.wait_for_element(selector, timeout, **kwargs)
    
    def locator(self, selector: str):
        """Create a locator for an element (Selenium equivalent of Playwright's locator)."""
        try:
            # Return a simple wrapper that mimics Playwright's locator behavior
            class SeleniumLocator:
                def __init__(self, driver, selector):
                    self.driver = driver
                    self.selector = selector
                
                def count(self):
                    return len(self.driver.find_elements(By.CSS_SELECTOR, self.selector))
                
                @property
                def first(self):
                    elements = self.driver.find_elements(By.CSS_SELECTOR, self.selector)
                    return elements[0] if elements else None
                
                def wait_for(self, state: str = "visible", timeout: int = 30000):
                    wait = WebDriverWait(self.driver, timeout / 1000)
                    if state == "visible":
                        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.selector)))
                    elif state == "attached":
                        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.selector)))
                    return True
            
            return SeleniumLocator(self._driver, selector)
        except Exception as e:
            logger.error(f"Locator creation failed: {e}")
            return None
    
    # Additional methods required by BrowserAutomator interface
    def take_screenshot(self, path: str = None, **kwargs) -> str:
        """Take a screenshot and save to path (alias for screenshot)."""
        try:
            screenshot_data = self.screenshot(**kwargs)
            if screenshot_data and path:
                with open(path, 'wb') as f:
                    f.write(screenshot_data)
                return path
            return ""
        except Exception as e:
            logger.error(f"Take screenshot failed: {e}")
            return ""
    
    def get_url(self, **kwargs) -> str:
        """Get the current URL (alias for get_current_url)."""
        return self.get_current_url(**kwargs) or ""
    
    def get_title(self, **kwargs) -> str:
        """Get the page title (alias for get_page_title)."""
        return self.get_page_title(**kwargs) or ""
    
    def tab_close(self, **kwargs) -> bool:
        """Close the current tab (alias for close_tab)."""
        return self.close_tab(**kwargs)
    
    def tab_focus(self, index: int, **kwargs) -> bool:
        """Focus on a specific tab by index (alias for focus_tab)."""
        return self.focus_tab(index, **kwargs)
    
    def tab_open(self, **kwargs) -> bool:
        """Open a new tab (alias for new_tab)."""
        return self.new_tab(**kwargs)
    
    def scroll_to(self, selector: str, **kwargs) -> bool:
        """Scroll to an element by selector."""
        try:
            if self._demo_mode_action("scroll_to", selector=selector, **kwargs):
                return True
            
            element = self._find_element(selector)
            if element:
                self._driver.execute_script("arguments[0].scrollIntoView(true);", element)
                return True
            return False
        except Exception as e:
            logger.error(f"Scroll to element failed: {e}")
            return False
    
    def scroll_to_by_test_id(self, test_id: str, **kwargs) -> bool:
        """Scroll to an element by test_id."""
        try:
            if self._demo_mode_action("scroll_to_by_test_id", test_id=test_id, **kwargs):
                return True
            
            element = self._find_element(test_id=test_id)
            if element:
                self._driver.execute_script("arguments[0].scrollIntoView(true);", element)
                return True
            return False
        except Exception as e:
            logger.error(f"Scroll to element by test_id failed: {e}")
            return False
    
    def screenshot(self, **kwargs) -> Optional[bytes]:
        """Take a screenshot of the current page."""
        try:
            if self._demo_mode_action("screenshot", **kwargs):
                return b"demo_screenshot"
            
            screenshot_data = self._driver.get_screenshot_as_png()
            return screenshot_data
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return None
    
    def screenshot_by_test_id(self, test_id: str, **kwargs) -> Optional[bytes]:
        """Take a screenshot of a specific element by test_id."""
        try:
            if self._demo_mode_action("screenshot_by_test_id", test_id=test_id, **kwargs):
                return b"demo_element_screenshot"
            
            element = self._find_element(test_id=test_id)
            if element:
                # For element screenshots, we need to implement a more complex approach
                # For now, return the full page screenshot
                screenshot_data = self._driver.get_screenshot_as_png()
                return screenshot_data
            return None
        except Exception as e:
            logger.error(f"Screenshot by test_id failed: {e}")
            return None
    
    @property
    def url(self) -> str:
        """Get the current URL (property equivalent of get_current_url)."""
        return self.get_current_url() or ""
    
    def title(self) -> str:
        """Get the page title (method equivalent of get_page_title)."""
        return self.get_page_title() or ""
    
    def content(self) -> str:
        """Get the page source HTML (method equivalent of get_page_source)."""
        return self.get_page_source() or ""
    
    def context(self):
        """Get the browser context (Selenium equivalent of Playwright's context)."""
        # In Selenium, we return a wrapper that mimics Playwright's context behavior
        class SeleniumContext:
            def __init__(self, driver):
                self.driver = driver
            
            @property
            def pages(self):
                # Return list of window handles as page-like objects
                return [SeleniumPage(handle, self.driver) for handle in self.driver.window_handles]
        
        return SeleniumContext(self._driver)
    
    def new_page(self, **kwargs):
        """Create a new page (Selenium equivalent of Playwright's new_page)."""
        try:
            # Open new tab
            self._driver.execute_script("window.open('', '_blank');")
            # Switch to the new tab
            self._driver.switch_to.window(self._driver.window_handles[-1])
            return SeleniumPage(self._driver.current_window_handle, self._driver)
        except Exception as e:
            logger.error(f"New page creation failed: {e}")
            return None
    

class SeleniumPage:
    """Selenium wrapper to mimic Playwright's Page behavior."""
    
    def __init__(self, window_handle, driver):
        self.window_handle = window_handle
        self.driver = driver
    
    def close(self):
        """Close the page/tab."""
        try:
            self.driver.switch_to.window(self.window_handle)
            self.driver.close()
            # Switch back to remaining tab if available
            if self.driver.window_handles:
                self.driver.switch_to.window(self.driver.window_handles[0])
        except Exception as e:
            logger.error(f"Page close failed: {e}")
    
    def screenshot(self, **kwargs) -> Optional[bytes]:
        """Take a screenshot of the page."""
        try:
            self.driver.switch_to.window(self.window_handle)
            return self.driver.get_screenshot_as_png()
        except Exception as e:
            logger.error(f"Page screenshot failed: {e}")
            return None
