"""
Playwright Automator - Implements BrowserAutomator interface for Playwright operations
"""
import logging
from typing import Optional, List, Dict, Any, Union
from playwright.sync_api import Page, Locator, ElementHandle, TimeoutError as PlaywrightTimeoutError
from weboasis.act_book.core.automator_interface import BrowserAutomator

logger = logging.getLogger(__name__)


class PlaywrightAutomator(BrowserAutomator):
    """Playwright implementation of BrowserAutomator with abstract attributes.""" # Abstract attributes - will be set by the manager
    _page = None
    _test_id_attribute = None

    
    @property
    def page(self) -> Optional[Page]:
        """Get the page instance."""
        return self._page
    
    @property
    def test_id_attribute(self) -> Optional[str]:
        """Get the test ID attribute."""
        return self._test_id_attribute
    
    # BrowserAutomator interface methods
    def click(self, selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Click an element by selector or test_id."""
        try:
            element = self._find_element(selector, test_id)
            if element and self._wait_for_interactable(element):
                element.click()
                return True
            return False
        except Exception as e:
            logger.error(f"Click failed: {e}")
            return False
    
    def click_by_test_id(self, test_id: str, **kwargs) -> bool:
        return self.click(test_id=test_id, **kwargs)
    
    def fill(self, selector: str = None, value: str = "", test_id: str = None, **kwargs) -> bool:
        """Fill a form field by selector or test_id."""
        try:
            element = self._find_element(selector, test_id)
            if element and self._wait_for_interactable(element):
                element.clear()
                element.fill(value)
                return True
            return False
        except Exception as e:
            logger.error(f"Fill failed: {e}")
            return False
    
    def fill_by_test_id(self, test_id: str, value: str, **kwargs) -> bool:
        return self.fill(test_id=test_id, value=value, **kwargs)
    

    
    def type_text(self, selector: str = None, text: str = "", test_id: str = None, **kwargs) -> bool:
        """Type text into an element by selector or test_id."""
        try:
            element = self._find_element(selector, test_id)
            if element and self._wait_for_interactable(element):
                element.type(text)
                return True
            logger.info(f"Type text failed: {element} and {self._wait_for_interactable(element)}")
            return False
        except Exception as e:
            logger.error(f"Type text failed: {e}")
            return False
    
    def type_text_by_test_id(self, test_id: str, text: str, **kwargs) -> bool:
        logger.info(f"Type text by test_id: {test_id}, text: {text}")
        return self.type_text(test_id=test_id, text=text, **kwargs)
    
    def hover(self, selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Hover over an element by selector or test_id."""
        try:
            element = self._find_element(selector, test_id)
            if element and self._wait_for_interactable(element):
                element.hover()
                return True
            return False
        except Exception as e:
            logger.error(f"Hover failed: {e}")
            return False
    
    def hover_by_test_id(self, test_id: str, **kwargs) -> bool:
        return self.hover(test_id=test_id, **kwargs)
    
    def double_click(self, selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Double click an element by selector or test_id."""
        try:
            element = self._find_element(selector, test_id)
            if element and self._wait_for_interactable(element):
                element.dblclick()
                return True
            return False
        except Exception as e:
            logger.error(f"Double click failed: {e}")
            return False
    
    def double_click_by_test_id(self, test_id: str, **kwargs) -> bool:
        return self.double_click(test_id=test_id, **kwargs)
    
    def check(self, selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Check a checkbox by selector or test_id."""
        try:
            element = self._find_element(selector, test_id)
            if element and self._wait_for_interactable(element):
                element.check()
                return True
            return False
        except Exception as e:
            logger.error(f"Check failed: {e}")
            return False
    
    def check_by_test_id(self, test_id: str, **kwargs) -> bool:
        return self.check(test_id=test_id, **kwargs)
    
    def uncheck(self, selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Uncheck a checkbox by selector or test_id."""
        try:
            element = self._find_element(selector, test_id)
            if element and self._wait_for_interactable(element):
                element.uncheck()
                return True
            return False
        except Exception as e:
            logger.error(f"Uncheck failed: {e}")
            return False
    
    def uncheck_by_test_id(self, test_id: str, **kwargs) -> bool:
        return self.uncheck(test_id=test_id, **kwargs)
    
    def select_option(self, selector: str = None, options: str = None, test_id: str = None, **kwargs) -> bool:
        """Select option from a dropdown by selector or test_id."""
        try:
            element = self._find_element(selector, test_id)
            if element and self._wait_for_interactable(element):
                element.select_option(value=options)
                return True
            return False
        except Exception as e:
            logger.error(f"Select option failed: {e}")
            return False
    
    def select_option_by_test_id(self, test_id: str, options: str, **kwargs) -> bool:
        return self.select_option(test_id=test_id, options=options, **kwargs)
    
    def navigate(self, url: str, **kwargs) -> bool:
        """Navigate to a URL."""
        try:
            self._page.goto(url)
            return True
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            return False
    
    def go_back(self, **kwargs) -> bool:
        """Go back in browser history."""
        try:
            self._page.go_back()
            return True
        except Exception as e:
            logger.error(f"Go back failed: {e}")
            return False
    
    def go_forward(self, **kwargs) -> bool:
        """Go forward in browser history."""
        try:
            self._page.go_forward()
            return True
        except Exception as e:
            logger.error(f"Go forward failed: {e}")
            return False
    
    def refresh(self, **kwargs) -> bool:
        """Refresh the current page."""
        try:
            self._page.reload()
            return True
        except Exception as e:
            logger.error(f"Refresh failed: {e}")
            return False
    
    
    def wait_for_load_state(self, state: str = "networkidle", timeout: int = 30000, **kwargs) -> bool:
        """Wait for specific load state."""
        try:
            self._page.wait_for_load_state(state, timeout=timeout)
            return True
        except Exception as e:
            logger.error(f"Wait for load state failed: {e}")
            return False
    
    def new_tab(self, **kwargs) -> bool:
        """Open a new tab."""
        try:
            self._page.context.new_page()
            return True
        except Exception as e:
            logger.error(f"New tab failed: {e}")
            return False
    
    def close_tab(self, **kwargs) -> bool:
        """Close the current tab."""
        try:
            self._page.close()
            return True
        except Exception as e:
            logger.error(f"Close tab failed: {e}")
            return False
    
    def focus_tab(self, index: int, **kwargs) -> bool:
        """Focus on a specific tab by index."""
        try:
            pages = self._page.context.pages
            if 0 <= index < len(pages):
                self._page = pages[index]
                return True
            return False
        except Exception as e:
            logger.error(f"Focus tab failed: {e}")
            return False
    
    def mouse_click(self, x: float, y: float, **kwargs) -> bool:
        """Click at specific coordinates."""
        try:
            self._page.mouse.click(x, y)
            return True
        except Exception as e:
            logger.error(f"Mouse click failed: {e}")
            return False
    
    def mouse_move(self, x: float, y: float, **kwargs) -> bool:
        """Move mouse to specific coordinates."""
        try:
            self._page.mouse.move(x, y)
            return True
        except Exception as e:
            logger.error(f"Mouse move failed: {e}")
            return False
    
    def scroll(self, delta_x: float, delta_y: float, **kwargs) -> bool:
        """Scroll the page by delta values."""
        try:
            self._page.mouse.wheel(delta_x, delta_y)
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
        """Scroll by wheel deltas at the element's position (lets browser choose the scroller)."""
        try:
            element = self._find_element(selector, test_id)
            if not element:
                return False
            # Move the mouse to the element center and wheel there
            box = element.bounding_box()
            if not box:
                return False
            center_x = box["x"] + box["width"] / 2
            center_y = box["y"] + box["height"] / 2
            self._page.mouse.move(center_x, center_y)
            self._page.mouse.wheel(delta_x, delta_y)
            return True
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
        """Scroll by deltas starting at absolute viewport position (x, y)."""
        try:
            self._page.mouse.move(x, y)
            self._page.mouse.wheel(delta_x, delta_y)
            return True
        except Exception as e:
            logger.error(f"scroll_from_position failed: {e}")
            return False
    
    def keyboard_type(self, text: str, **kwargs) -> bool:
        """Type text using keyboard."""
        try:
            self._page.keyboard.type(text)
            return True
        except Exception as e:
            logger.error(f"Keyboard type failed: {e}")
            return False
    
    def keyboard_press(self, key: str, **kwargs) -> bool:
        """Press a keyboard key."""
        try:
            self._page.keyboard.press(key)
            return True
        except Exception as e:
            logger.error(f"Keyboard press failed: {e}")
            return False
    
    def press(self, selector: str = None, key: str = None, test_id: str = None, **kwargs) -> bool:
        """Press a key on an element."""
        try:
            element = self._find_element(selector, test_id)
            if element and self._wait_for_interactable(element):
                element.press(key)
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
            element = self._find_element(selector, test_id)
            if element and self._wait_for_interactable(element):
                element.focus()
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
    
    def set_attribute(self, selector: str = None, attribute: str = "", value: str = "", test_id: str = None, **kwargs) -> bool:
        """Set attribute value on an element."""
        try:
            element = self._find_element(selector, test_id)
            if element:
                element.evaluate(f'el => el.setAttribute("{attribute}", "{value}")')
                return True
            return False
        except Exception as e:
            logger.error(f"Set attribute failed: {e}")
            return False
    
    def set_attribute_by_test_id(self, test_id: str, attribute: str, value: str, **kwargs) -> bool:
        return self.set_attribute(test_id=test_id, attribute=attribute, value=value, **kwargs)
    
    def wait_for_element(self, selector: str = None, timeout: int = 30000, test_id: str = None, **kwargs) -> bool:
        """Wait for an element to appear."""
        try:
            if test_id:
                if self._test_id_attribute and self._page:
                    self._page.wait_for_selector(f'[{self._test_id_attribute}="{test_id}"]', timeout=timeout)
            elif selector:
                self._page.wait_for_selector(selector, timeout=timeout)
            return True
        except Exception as e:
            logger.error(f"Wait for element failed: {e}")
            return False
    
    def wait_for_element_by_test_id(self, test_id: str, timeout: int = 30000, **kwargs) -> bool:
        return self.wait_for_element(test_id=test_id, timeout=timeout, **kwargs)
    
    def upload_file(self, selector: str = None, file: str = "", test_id: str = None, **kwargs) -> bool:
        """Upload a file to an element."""
        try:
            element = self._find_element(selector, test_id)
            if element and self._wait_for_interactable(element):
                element.set_input_files(file)
                return True
            return False
        except Exception as e:
            logger.error(f"Upload file failed: {e}")
            return False
    
    def upload_file_by_test_id(self, test_id: str, file: str, **kwargs) -> bool:
        return self.upload_file(test_id=test_id, file=file, **kwargs)
    
    def mouse_upload_file(self, x: float, y: float, file: str, **kwargs) -> bool:
        """Upload file by clicking at coordinates."""
        try:
            self._page.mouse.click(x, y)
            # This would need more complex implementation for file dialog
            return False
        except Exception as e:
            logger.error(f"Mouse upload file failed: {e}")
            return False
    
    def play_video(self, selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Play a video element."""
        try:
            element = self._find_element(selector, test_id)
            if element:
                element.evaluate('el => el.play()')
                return True
            return False
        except Exception as e:
            logger.error(f"Play video failed: {e}")
            return False
    
    def play_video_by_test_id(self, test_id: str, **kwargs) -> bool:
        return self.play_video(test_id=test_id, **kwargs)
    
    def pause_video(self, selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Pause a video element."""
        try:
            element = self._find_element(selector, test_id)
            if element:
                element.evaluate('el => el.pause()')
                return True
            return False
        except Exception as e:
            logger.error(f"Pause video failed: {e}")
            return False
    
    def pause_video_by_test_id(self, test_id: str, **kwargs) -> bool:
        return self.pause_video(test_id=test_id, **kwargs)
    
    def get_text(self, selector: str = None, test_id: str = None, **kwargs) -> str:
        """Get text content from an element."""
        try:
            element = self._find_element(selector, test_id)
            if element:
                return element.inner_text()
            return ""
        except Exception as e:
            logger.error(f"Get text failed: {e}")
            return ""
    
    def get_text_by_test_id(self, test_id: str, **kwargs) -> str:
        return self.get_text(test_id=test_id, **kwargs)
    
    def get_attribute(self, selector: str = None, attribute: str = "", test_id: str = None, **kwargs) -> str:
        """Get attribute value from an element."""
        try:
            element = self._find_element(selector, test_id)
            if element:
                return element.get_attribute(attribute) or ""
            return ""
        except Exception as e:
            logger.error(f"Get attribute failed: {e}")
            return ""
    
    def get_attribute_by_test_id(self, test_id: str, attribute: str, **kwargs) -> str:
        return self.get_attribute(test_id=test_id, attribute=attribute, **kwargs)
    
    def get_current_url(self, **kwargs) -> Optional[str]:
        """Get the current URL."""
        try:
            return self._page.url
        except Exception as e:
            logger.error(f"Get URL failed: {e}")
            return None
    
    def get_page_title(self, **kwargs) -> Optional[str]:
        """Get the page title."""
        try:
            return self._page.title()
        except Exception as e:
            logger.error(f"Get title failed: {e}")
            return None
    
    def get_page_source(self, **kwargs) -> Optional[str]:
        """Get the page source HTML."""
        try:
            return self._page.content()
        except Exception as e:
            logger.error(f"Get page source failed: {e}")
            return None
    
    def scroll_to(self, selector: str, **kwargs) -> bool:
        """Scroll to an element by selector."""
        try:
            element = self._page.locator(selector)
            if element.count() > 0:
                element.first.scroll_into_view_if_needed()
                return True
            return False
        except Exception as e:
            logger.error(f"Scroll to element failed: {e}")
            return False
    
    def scroll_to_by_test_id(self, test_id: str, **kwargs) -> bool:
        """Scroll to an element by test_id."""
        try:
            if self._test_id_attribute and self._page:
                element = self._page.locator(f'[{self._test_id_attribute}="{test_id}"]')
                if element.count() > 0:
                    element.first.scroll_into_view_if_needed()
                    return True
            return False
        except Exception as e:
            logger.error(f"Scroll to element by test_id failed: {e}")
            return False
    
    def screenshot(self, **kwargs) -> Optional[bytes]:
        """Take a screenshot of the current page."""
        try:
            screenshot_data = self._page.screenshot(**kwargs)
            return screenshot_data
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return None
    
    def screenshot_by_test_id(self, test_id: str, **kwargs) -> Optional[bytes]:
        """Take a screenshot of a specific element by test_id."""
        try:
            element = self._find_element(test_id=test_id)
            if element:
                screenshot_data = element.screenshot(**kwargs)
                return screenshot_data
            return None
        except Exception as e:
            logger.error(f"Screenshot by test_id failed: {e}")
            return None
    
    def drag_and_drop(self, from_selector: str, to_selector: str, **kwargs) -> bool:
        """Drag and drop from one element to another using selectors."""
        try:
            from_element = self._page.locator(from_selector)
            to_element = self._page.locator(to_selector)
            
            if from_element.count() > 0 and to_element.count() > 0:
                from_element.first.drag_to(to_element.first)
                return True
            return False
        except Exception as e:
            logger.error(f"Drag and drop failed: {e}")
            return False
    
    def drag_and_drop_by_test_id(self, from_test_id: str, to_test_id: str, **kwargs) -> bool:
        """Drag and drop from one element to another using test_ids."""
        try:
            if self._test_id_attribute and self._page:
                from_element = self._page.locator(f'[{self._test_id_attribute}="{from_test_id}"]')
                to_element = self._page.locator(f'[{self._test_id_attribute}="{to_test_id}"]')
                
                if from_element.count() > 0 and to_element.count() > 0:
                    from_element.first.drag_to(to_element.first)
                    return True
            return False
        except Exception as e:
            logger.error(f"Drag and drop by test_id failed: {e}")
            return False
    
    # Helper methods for element finding and interaction
    def _find_element(self, selector: str = None, test_id: str = None) -> Optional[Locator]:
        """Find an element by selector or test_id."""
        if test_id:
            try:
                if self._test_id_attribute and self._page:
                    element = self._page.locator(f'[{self._test_id_attribute}="{test_id}"]')
                    if element.count() > 0:
                        return element.first
            except:
                pass
        
        if selector:
            try:
                element = self._page.locator(selector)
                if element.count() > 0:
                    return element.first
            except:
                pass
        
        return None
    
    def _wait_for_interactable(self, element: Locator, timeout: int = 30000) -> bool:
        """Wait for an element to be interactable."""
        try:
            element.wait_for(state="visible", timeout=timeout)
            element.wait_for(state="attached", timeout=timeout)
            return True
        except:
            return False
