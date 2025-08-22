from playwright.sync_api import sync_playwright, BrowserContext, Page
from playwright.async_api import async_playwright
import asyncio
import os
import logging
import traceback
from abc import ABC
from typing import Optional

from weboasis.ui_manager.constants import MARK_ELEMENTS_JS, ADD_OUTLINE_ELEMENTS_JS, REMOVE_OUTLINE_ELEMENTS_JS, IDENTIFY_INTERACTIVE_ELEMENTS_JS, SHOW_DECISION_MAKING_PROCESS_JS, INJECT_DEVELOPER_PANEL_JS, HIDE_DEVELOPER_ELEMENTS_JS, SHOW_DEVELOPER_ELEMENTS_JS, EXTRACT_ACCESSIBILITY_TREE_JS
from weboasis.ui_manager.base_manager import SyncWEBManager
from weboasis.act_book.engines.playwright.playwright_automator import PlaywrightAutomator
from weboasis.ui_manager.parsers.simple_parser import SimpleParser
import time

logger = logging.getLogger(__name__)


class SyncPlaywrightManager(SyncWEBManager, PlaywrightAutomator):
    """Playwright implementation of SyncWEBManager with element marking capabilities.
    
    This class provides methods for managing web pages and marking DOM elements
    for automated testing and interaction.
    
    Example usage:
        # Basic element marking (fastest, no additional checks)
        count = manager.mark_elements()
        
        # Element marking with page readiness checks (more reliable)
        count = manager.mark_elements(check_page_readiness=True)
        
        # Check if page is ready before marking
        if manager.is_page_ready_for_marking():
            count = manager.mark_elements()
        
        # Wait for page to be fully loaded, then mark elements
        if manager.is_page_loaded():
            count = manager.mark_elements()
    """
    
    def __init__(self, parser=SimpleParser, test_id_attribute: str = "data-testid"):
        # Initialize base classes
        SyncWEBManager.__init__(self)
        
        self._playwright = sync_playwright().start()
        # TODO: support other browsers
        if os.path.exists('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'):
            executable_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        else:
            executable_path = None
        self._browser = self._playwright.chromium.launch(headless=False,
            args=[
                "--autoplay-policy=no-user-gesture-required",
                "--disable-password-generation",
                "--disable-features=VizDisplayCompositor",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                "--disable-features=TranslateUI",
                "--disable-ipc-flooding-protection"
            ],
            executable_path=executable_path)
        # self._browser = self._playwright.webkit.launch(headless=False)
        self._context = self._browser.new_context(
            device_scale_factor=2,
        )
        self._page = self._browser.new_page()
        self._demo_mode = "default"     
        # Default parser
        self._parser = parser
        self._test_id_attribute = test_id_attribute  # This sets the inherited _test_id_attribute attribute
    
    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, parser_class):
        self._parser = parser_class
        
    @property
    def page(self):
        return self._page
    
    @property
    def context(self):
        return self._context
    
    @property
    def browser(self):
        return self._browser
    
    @property
    def playwright(self):
        return self._playwright
    
    @property
    def test_id_attribute(self):
        return self._test_id_attribute
    
    @property
    def selectors(self):
        '''
        Playwright supports shorthand for selecting elements using certain attributes. Currently, only the following attributes are supported:

        # id
        # data-testid
        # data-test-id
        # data-test
        ''' 
        return self._playwright.selectors
    
    def set_test_id_attribute(self, attribute):
        self._test_id_attribute = attribute


    def is_page_loaded(self, timeout: int = 10000) -> bool:
        """
        Check if the page is fully loaded and ready for element marking.
        This includes waiting for network idle, DOM stability, and dynamic content.
        
        Args:
            timeout (int): Maximum time to wait in milliseconds
            
        Returns:
            bool: True if page is ready, False if timeout exceeded
        """
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout//2)
            # 2) Brief settle: no active animations and DOM stable for ~800ms
            self.page.wait_for_function("""
                () => new Promise((resolve) => {
                const hasAnims = () => (document.getAnimations?.() || []).length > 0;
                if (!hasAnims()) {
                    let last = document.querySelectorAll('*').length;
                    let idle = 0;
                    const obs = new MutationObserver(() => { idle = 0; });
                    obs.observe(document.body, {childList: true, subtree: true});
                    const tick = () => {
                    const now = document.querySelectorAll('*').length;
                    idle += 100;
                    if (now !== last) { last = now; idle = 0; }
                    if (idle >= 800) { obs.disconnect(); resolve(true); }
                    else setTimeout(tick, 100);
                    };
                    tick();
                } else {
                    // Wait a bit for animations to stop then resolve anyway
                    setTimeout(() => resolve(true), 1000);
                }
                })
            """, timeout=timeout//2)
                
            return True
            
        except Exception as e:
            logger.warning(f"Page load waiting failed: {e}. Page may not be fully loaded.")
            return False

    def mark_elements(self, check_page_readiness: bool = True):
        """
        Pre-extraction routine, marks DOM elements (set bid and dynamic attributes like value and checked)
        
        Args:
            check_page_readiness (bool): Whether to perform additional page readiness checks before marking.
                                       Default is True for reliability. Set to False for performance.
        
        Returns:
            int: Total number of elements marked across all frames
        """
        # Wait for page to be fully loaded and stable before marking elements
        if check_page_readiness:
            if not self.is_page_loaded():
                logger.warning("Page load check failed, but proceeding with element marking...")
        
        total_marked = 0  # Track total marked elements
        
        def mark_frames_recursive(frame, frame_bid: str):
            nonlocal total_marked
            assert frame_bid == "" or (frame_bid.islower() and frame_bid.isalpha())

            # Mark all DOM elements in the frame using the universal wrapper
            try:
                result = frame.evaluate(
                    MARK_ELEMENTS_JS,
                    [frame_bid, self._test_id_attribute],
                )
                
                # Extract warning messages and count from result
                if isinstance(result, list) and len(result) >= 2:
                    warning_msgs = result[0]
                    marked_count = result[1]  # JavaScript returns [warnings, count]
                    total_marked += marked_count
                else:
                    # Fallback if JavaScript doesn't return expected format
                    warning_msgs = result if isinstance(result, list) else []
                    marked_count = 0
                
                # Print warning messages if any
                for msg in warning_msgs:
                    logger.warning(msg)
            
                
            except Exception as e:
                logger.error(f"JavaScript execution failed for frame '{frame_bid or 'main'}': {e}")
                marked_count = 0
                total_marked += marked_count

            # Process child frames efficiently
            try:
                child_frames = frame.child_frames
                if child_frames:
                    
                    for child_frame in child_frames:
                        try:
                            # Skip detached frames
                            if child_frame.is_detached():
                                continue
                            
                            # Skip problematic frames
                            child_frame_elem = child_frame.frame_element()
                            if not child_frame_elem.content_frame() == child_frame:
                                logger.warning(f"Skipping frame '{child_frame.name}' for marking, seems problematic.")
                                continue
                            
                            # Skip sandboxed frames with blocked script execution
                            sandbox_attr = child_frame_elem.get_attribute("sandbox")
                            if sandbox_attr is not None and "allow-scripts" not in sandbox_attr.split():
                                continue
                            
                            # Get child frame bid and process recursively
                            child_frame_bid = child_frame_elem.get_attribute(self._test_id_attribute)
                            if child_frame_bid is None:
                                logger.warning("Cannot mark a child frame without a bid.")
                            else:
                                mark_frames_recursive(child_frame, frame_bid=child_frame_bid)
                                
                        except Exception as e:
                            logger.warning(f"Error processing child frame: {e}")
                            continue
                            
            except Exception as e:
                logger.warning(f"Error processing child frames: {e}")

        # Mark all frames recursively
        mark_frames_recursive(self.page.main_frame, frame_bid="")
        
        # Quick retry only if no elements were marked (single attempt)
        if total_marked == 0:
            logger.warning("No elements marked on first attempt. Quick retry...")
            self.page.wait_for_timeout(1000)  # Brief wait for page stability
            
            # Reset and retry
            total_marked = 0
            mark_frames_recursive(self.page.main_frame, frame_bid="")
            
            if total_marked == 0:
                logger.error("Failed to mark any elements after retry!")
            else:
                logger.debug(f"Successfully marked {total_marked} elements after retry")
        
        logger.debug(f"Total elements marked across all frames: {total_marked}")
        return total_marked
        
        
    def outline_interactive_elements(self, interactive_elements: list[dict], max_retries=3, retry_delay=1000):
        for attempt in range(max_retries):
            highlighted_count = self.page.evaluate(ADD_OUTLINE_ELEMENTS_JS, [self._test_id_attribute])
            if highlighted_count == len(interactive_elements):
                logger.debug(f"All {highlighted_count} elements highlighted successfully.")
                return

            logger.debug(
                f"Attempt {attempt + 1}: Highlighted {highlighted_count}/{len(interactive_elements)} elements. Retrying in {retry_delay}ms...")
            self.page.wait_for_timeout(retry_delay)

        logger.warning(f"Warning: Only {highlighted_count}/{len(interactive_elements)} elements were highlighted after {max_retries} attempts.")

        
        
    def remove_outline_elements(self):
        self.page.evaluate(REMOVE_OUTLINE_ELEMENTS_JS)
        
        
    def inject_developer_panel(self):
        self.is_page_loaded()
        self.page.evaluate(INJECT_DEVELOPER_PANEL_JS)
        
         
    
    def locate_element(self,extracted_number):
        try:
            # Define selectors for potentially interactive elements
            selectors = [
                'a', 'button', 'input', 'select', 'textarea', 'summary', 
                'video', 'audio', 'iframe', 'embed', 'object', 'menu', 
                'label', 'fieldset', 'datalist', 'output', 'details', 
                'dialog', 'option', '[role="button"]', '[role="link"]', 
                '[role="checkbox"]', '[role="radio"]', '[role="menuitem"]', 
                '[role="tab"]', '[tabindex]', '[contenteditable="true"]'
            ]
            
            # Verify page is valid
            if not self.page or not self.page.evaluate('() => document.readyState') == 'complete':
                print("Page is not ready or invalid")
                return {}

            # Search for element by ID first (more efficient)
            element =  self.page.query_selector(f'[{self._test_id_attribute}="{extracted_number}"], [id="{extracted_number}"]')
            
            # If not found, then search through individual selectors
            if not element:
                for selector in selectors:
                    try:
                        elements = self.page.query_selector_all(selector)
                        if not elements:
                            continue
                            
                        for el in elements:
                            bid = el.get_attribute(f'{self._test_id_attribute}') or el.get_attribute('id') or ''
                            if bid == extracted_number:
                                element = el
                                break
                        if element:
                            break
                    except Exception as e:
                        print(f"Error searching selector {selector}: {str(e)}")
                        continue
            
            if not element:
                print(f"No element found with ID {extracted_number}")
                return {}
                
            # Extract element properties
            result = {}
            try:
                result = {
                    'text': element.inner_text(),
                    'type': element.get_attribute('type'),
                    'tag': element.evaluate('el => el.tagName.toLowerCase()'),
                    'id': element.get_attribute('id'),
                    'href': element.get_attribute('href'),
                    'title': element.get_attribute('title'),
                    'ariaLabel': element.get_attribute('aria-label'),
                    'name': element.get_attribute('name'),
                    'value': element.get_attribute('value'),
                    'placeholder': element.get_attribute('placeholder'),
                    'class': element.get_attribute('class'),
                    'role': element.get_attribute('role')
                }
                
                # Clean up None values
                result = {k: v for k, v in result.items() if v is not None}
                
            except Exception as e:
                print(f"Error extracting element properties: {str(e)}")
                return {}
                    
            return result

        except Exception as e:
            print(f"Error in locate_element: {str(e)}")
            return {}
        
        
    def show_decision_making_process(self, description):
        # avoid showing the password in the decision making process
        if "password" in description.lower():
            description = "***PASSWORD HIDDEN***"
        
        try:
            # Try to show the decision making process via JavaScript
            self.page.evaluate(SHOW_DECISION_MAKING_PROCESS_JS, [description, True])
        except Exception as e:
            logger.warning(f"Failed to show decision making process via JavaScript: {e}")
            # Fallback: just log the description
            logger.debug(f"Decision making process: {description}")
        
    def identify_interactive_elements(self):
        return self.page.evaluate(IDENTIFY_INTERACTIVE_ELEMENTS_JS, self._test_id_attribute)
    
    def make_self_intro(self, description):
        self.page.on("load", lambda _: self.inject_profile_button())
        import time
        while True:
            paused = self.page.evaluate("document.getElementById('webagent-pause-btn')?.dataset.paused === 'true'")         
            if not paused:
                break
            else:
                self.page.evaluate(SHOW_DECISION_MAKING_PROCESS_JS, [description, False])
            time.sleep(0.5)
        
    def pause_for_debug(self):
        try:
            self.inject_pause_button()
        except Exception as e:
            logger.warning(f"Failed to inject pause button: {e}")
            return
        # Poll for pause state
        import time
        while True:
            paused = self.page.evaluate("document.getElementById('webagent-pause-btn')?.dataset.paused === 'true'")
            if not paused:
                break
            time.sleep(0.5)
        # Now continue execution
        
    def inject_pause_button(self):
        self.page.evaluate("""
            (function() {
                let btn = document.getElementById('webagent-pause-btn');
                if (btn) return;
                btn = document.createElement('button');
                btn.id = 'webagent-pause-btn';
                btn.setAttribute('developer_elem', ''); 
                btn.innerText = 'Pause';
                btn.style.position = 'fixed';
                btn.style.top = '40px';
                btn.style.right = '20px';
                btn.style.zIndex = 2147483647;
                btn.style.background = '#e67e22';
                btn.style.color = '#fff';
                btn.style.padding = '8px 16px';
                btn.style.border = 'none';
                btn.style.borderRadius = '6px';
                btn.style.fontSize = '14px';
                btn.style.fontFamily = 'monospace';
                btn.style.cursor = 'pointer';
                btn.style.boxShadow = '0 2px 12px rgba(0,0,0,0.15)';
                btn.dataset.paused = 'false';
                btn.onclick = function() {
                    if (btn.dataset.paused === 'false') {
                        btn.innerText = 'Resume';
                        btn.dataset.paused = 'true';
                    } else {
                        btn.innerText = 'Pause';
                        btn.dataset.paused = 'false';
                    }
                };
                document.body.appendChild(btn);
            })();
        """)
        
        
    def inject_profile_button(self):
        self.page.evaluate("""
            (function() {
                let btn = document.getElementById('webagent-profile-btn');
                if (btn) return;
                btn = document.createElement('button');
                btn.id = 'webagent-profile-btn';
                btn.setAttribute('developer_elem', ''); 
                btn.innerText = 'Profile';
                btn.style.position = 'fixed';
                btn.style.top = '10px';
                btn.style.right = '20px';
                btn.style.zIndex = 2147483647;
                btn.style.background = '#e67e22';
                btn.style.color = '#fff';
                btn.style.padding = '8px 8px';
                btn.style.border = 'none';
                btn.style.borderRadius = '6px';
                btn.style.fontSize = '14px';
                btn.style.fontFamily = 'monospace';
                btn.style.cursor = 'pointer';
                btn.style.boxShadow = '0 2px 12px rgba(0,0,0,0.15)';
                btn.dataset.paused = 'false';
                btn.onclick = function() {
                    if (btn.dataset.paused === 'false') {
                        btn.innerText = 'Profile Close';
                        btn.dataset.paused = 'true';
                    } else {
                        btn.innerText = 'Profile';
                        btn.dataset.paused = 'false';
                    }
                };
                document.body.appendChild(btn);
            })();
        """)
        
    def hide_developer_elements(self):
        self.page.evaluate(HIDE_DEVELOPER_ELEMENTS_JS)
        
    def show_developer_elements(self):
        self.page.evaluate(SHOW_DEVELOPER_ELEMENTS_JS)
        
    
    def get_accessibility_tree(self, max_depth: int = 5, max_text_len: int = 80, only_viewport: bool = True, max_nodes: int = 300) -> list[dict]:
        """Extract a simplified accessibility-like tree from the current page.
        Returns a list of compact nodes with tag, role, name, interactivity and viewport rect.
        """
        try:
            options = {
                "testIdAttr": self._test_id_attribute,
                "maxDepth": max_depth,
                "maxTextLen": max_text_len,
                "onlyViewport": only_viewport,
                "maxNodes": max_nodes,
            }
            return self.page.evaluate(EXTRACT_ACCESSIBILITY_TREE_JS, options) or []
        except Exception as e:
            logger.warning(f"Failed to extract accessibility tree: {e}")
            return []

    def close(self):
        """
        Close the browser and playwright instance
        """
        try:
            if self._page:
                self._page.close()
            if self._context:
                self._context.close()
            if self._browser:
                self._browser.close()
            if self._playwright:
                self._playwright.stop()
        except Exception as e:
            logger.error(f"Error closing playwright manager: {e}")
            traceback.print_exc()
            
    def is_browser_available(self) -> bool:
        """Check if the browser/page is still available and responsive."""
        try:
            if not self.page:
                return False
            
            # Check if page is closed
            if self.page.is_closed():
                return False
            
            # Try a simple operation to see if page is responsive
            self.page.evaluate("document.readyState")
            return True
            
        except Exception as e:
            logger.debug(f"Browser availability check failed: {e}")
            return False
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        


class AsyncPlaywrightManager(SyncWEBManager, PlaywrightAutomator):
    """Asynchronous Playwright manager that inherits PlaywrightAutomator for operations."""
    
    def __init__(self, test_id_attribute: str = "data-testid"):
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None
        self._test_id_attribute = test_id_attribute
        
        # Initialize PlaywrightAutomator base class
        PlaywrightAutomator.__init__(self)
        
    async def start(self):
        """Start the async playwright instance."""
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=False,
            args=[
                "--autoplay-policy=no-user-gesture-required",
                "--disable-password-generation",
                "--disable-features=VizDisplayCompositor",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                "--disable-features=TranslateUI",
                "--disable-ipc-flooding-protection"
            ])
        self._context = await self._browser.new_context()
        self._page = await self._context.new_page()
        
        # Now initialize PlaywrightAutomator base class
        PlaywrightAutomator.__init__(self)
        
        # Set the inherited attributes
        self._page = self._page
        self._test_id_attribute = self._test_id_attribute
        
    async def close(self):
        """Close the async playwright instance."""
        if self._page:
            await self._page.close()
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
    
    async def __aenter__(self):
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        