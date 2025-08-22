"""
Browser Automator Interface - Core interface for browser automation engines

Copyright 2024 Siyang Liu

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from abc import ABC, abstractmethod
from typing import Optional, Any, Dict, List

class BrowserAutomator(ABC):
    """
    Abstract base class for browser automation engines.
    
    This interface defines the contract that all browser automation engines
    must implement, ensuring consistent behavior across different technologies
    like Playwright, Selenium, etc.
    """
    
    @abstractmethod
    def click(self, selector: str, **kwargs) -> bool:
        """Click an element by selector."""
        pass
    
    @abstractmethod
    def click_by_test_id(self, test_id: str, **kwargs) -> bool:
        """Click an element by test_id."""
        pass
    
    @abstractmethod
    def fill(self, selector: str, text: str, **kwargs) -> bool:
        """Fill a form field by selector."""
        pass
    
    @abstractmethod
    def fill_by_test_id(self, test_id: str, text: str, **kwargs) -> bool:
        """Fill a form field by test_id."""
        pass
    
    @abstractmethod
    def type_text(self, selector: str, text: str, **kwargs) -> bool:
        """Type text into an element by selector."""
        pass
    
    @abstractmethod
    def type_text_by_test_id(self, test_id: str, text: str, **kwargs) -> bool:
        """Type text into an element by test_id."""
        pass
    
    @abstractmethod
    def hover(self, selector: str, **kwargs) -> bool:
        """Hover over an element by selector."""
        pass
    
    @abstractmethod
    def hover_by_test_id(self, test_id: str, **kwargs) -> bool:
        """Hover over an element by test_id."""
        pass
    
    @abstractmethod
    def double_click(self, selector: str, **kwargs) -> bool:
        """Double-click an element by selector."""
        pass
    
    @abstractmethod
    def double_click_by_test_id(self, test_id: str, **kwargs) -> bool:
        """Double-click an element by test_id."""
        pass
    
    @abstractmethod
    def check(self, selector: str, **kwargs) -> bool:
        """Check a checkbox by selector."""
        pass
    
    @abstractmethod
    def check_by_test_id(self, test_id: str, **kwargs) -> bool:
        """Check a checkbox by test_id."""
        pass
    
    @abstractmethod
    def uncheck(self, selector: str, **kwargs) -> bool:
        """Uncheck a checkbox by selector."""
        pass
    
    @abstractmethod
    def uncheck_by_test_id(self, test_id: str, **kwargs) -> bool:
        """Uncheck a checkbox by test_id."""
        pass
    
    @abstractmethod
    def select_option(self, selector: str, value: str, **kwargs) -> bool:
        """Select an option by selector."""
        pass
    
    @abstractmethod
    def select_option_by_test_id(self, test_id: str, value: str, **kwargs) -> bool:
        """Select an option by test_id."""
        pass
    
    @abstractmethod
    def scroll_to(self, selector: str, **kwargs) -> bool:
        """Scroll to an element by selector."""
        pass
    
    @abstractmethod
    def scroll_to_by_test_id(self, test_id: str, **kwargs) -> bool:
        """Scroll to an element by test_id."""
        pass
    
    @abstractmethod
    def scroll(self, x: int, y: int, **kwargs) -> bool:
        """Scroll by x and y pixels."""
        pass

    @abstractmethod
    def scroll_around_element(
        self,
        selector: str = None,
        test_id: str = None,
        delta_x: float = 0,
        delta_y: float = 300,
        **kwargs,
    ) -> bool:
        """Scroll the nearest scrollable container around the specified element by the given deltas."""
        pass

    @abstractmethod
    def scroll_from_position(
        self,
        x: float,
        y: float,
        delta_x: float = 0,
        delta_y: float = 300,
        **kwargs,
    ) -> bool:
        """Scroll by wheel deltas starting at absolute viewport position (x, y)."""
        pass
    
    @abstractmethod
    def get_text(self, selector: str, **kwargs) -> Optional[str]:
        """Get text content by selector."""
        pass
    
    @abstractmethod
    def get_text_by_test_id(self, test_id: str, **kwargs) -> Optional[str]:
        """Get text content by test_id."""
        pass
    
    @abstractmethod
    def get_attribute(self, selector: str, attribute: str, **kwargs) -> Optional[str]:
        """Get element attribute by selector."""
        pass
    
    @abstractmethod
    def get_attribute_by_test_id(self, test_id: str, attribute: str, **kwargs) -> Optional[str]:
        """Get element attribute by test_id."""
        pass
    
    @abstractmethod
    def set_attribute(self, selector: str, attribute: str, value: str, **kwargs) -> bool:
        """Set element attribute by selector."""
        pass
    
    @abstractmethod
    def set_attribute_by_test_id(self, test_id: str, attribute: str, value: str, **kwargs) -> bool:
        """Set element attribute by test_id."""
        pass
    
    @abstractmethod
    def screenshot(self, **kwargs) -> Optional[bytes]:
        """Take a screenshot of the current page."""
        pass
    
    @abstractmethod
    def screenshot_by_test_id(self, test_id: str, **kwargs) -> Optional[bytes]:
        """Take a screenshot of a specific element by test_id."""
        pass
    
    @abstractmethod
    def upload_file(self, selector: str, file_path: str, **kwargs) -> bool:
        """Upload a file by selector."""
        pass
    
    @abstractmethod
    def upload_file_by_test_id(self, test_id: str, file_path: str, **kwargs) -> bool:
        """Upload a file by test_id."""
        pass
    
    @abstractmethod
    def play_video(self, selector: str, **kwargs) -> bool:
        """Play a video by selector."""
        pass
    
    @abstractmethod
    def play_video_by_test_id(self, test_id: str, **kwargs) -> bool:
        """Play a video by test_id."""
        pass
    
    @abstractmethod
    def pause_video(self, selector: str, **kwargs) -> bool:
        """Pause a video by selector."""
        pass
    
    @abstractmethod
    def pause_video_by_test_id(self, test_id: str, **kwargs) -> bool:
        """Pause a video by test_id."""
        pass
    
    @abstractmethod
    def navigate(self, url: str, **kwargs) -> bool:
        """Navigate to a URL."""
        pass
    
    @abstractmethod
    def get_current_url(self, **kwargs) -> Optional[str]:
        """Get the current URL."""
        pass
    
    @abstractmethod
    def wait_for_element(self, selector: str, timeout: int = 30000, **kwargs) -> bool:
        """Wait for an element to appear by selector."""
        pass
    
    @abstractmethod
    def wait_for_element_by_test_id(self, test_id: str, timeout: int = 30000, **kwargs) -> bool:
        """Wait for an element to appear by test_id."""
        pass
    
    @abstractmethod
    def get_page_title(self, **kwargs) -> Optional[str]:
        """Get the page title."""
        pass
    
    @abstractmethod
    def get_page_source(self, **kwargs) -> Optional[str]:
        """Get the page source HTML."""
        pass 