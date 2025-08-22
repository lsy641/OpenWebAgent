"""
Browser navigation operations - page navigation and URL management.
"""

from weboasis.act_book.core.base import Operation, OperationResult
from weboasis.act_book.core.registry import register_operation
import logging
import time

logger = logging.getLogger(__name__)


@register_operation
class Navigate(Operation):
    """Navigate to a URL."""
    
    def __init__(self):
        super().__init__("navigate", "Navigate to a URL", "browser_navigation")
    
    def execute(self, ui_automator, url: str, **kwargs) -> OperationResult:
        """Execute navigation operation."""
        try:
            # Use the correct method name: navigate() not goto()
            success = ui_automator.navigate(url)
            if success:
                return OperationResult(success=True, data=f"Navigated to: {url}")
            else:
                return OperationResult(success=False, error="Navigation failed")
        except Exception as e:
            logger.error(f"Error navigating to {url}: {str(e)}")
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, url: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return url is not None and url.startswith(('http://', 'https://'))


@register_operation
class Back(Operation):
    """Go back in browser history."""
    
    def __init__(self):
        super().__init__("back", "Go back in browser history", "browser_navigation")
    
    def execute(self, ui_automator, **kwargs) -> OperationResult:
        """Execute back operation."""
        try:
            # Use the correct method name: go_back() not go_back()
            success = ui_automator.go_back()
            if success:
                return OperationResult(success=True, data="Went back in browser history")
            else:
                return OperationResult(success=False, error="Go back failed")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, **kwargs) -> bool:
        """Validate parameters."""
        return True


@register_operation
class Forward(Operation):
    """Go forward in browser history."""
    
    def __init__(self):
        super().__init__("forward", "Go forward in browser history", "browser_navigation")
    
    def execute(self, ui_automator, **kwargs) -> OperationResult:
        """Execute forward operation."""
        try:
            # Use the correct method name: go_forward() not go_forward()
            success = ui_automator.go_forward()
            if success:
                return OperationResult(success=True, data="Went forward in browser history")
            else:
                return OperationResult(success=False, error="Go forward failed")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, **kwargs) -> bool:
        """Validate parameters."""
        return True


@register_operation
class Refresh(Operation):
    """Refresh the current page."""
    
    def __init__(self):
        super().__init__("refresh", "Refresh the current page", "browser_navigation")
    
    def execute(self, ui_automator, **kwargs) -> OperationResult:
        """Execute refresh operation."""
        try:
            # Use the correct method name: refresh() not refresh()
            success = ui_automator.refresh()
            if success:
                return OperationResult(success=True, data="Refreshed the page")
            else:
                return OperationResult(success=False, error="Refresh failed")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, **kwargs) -> bool:
        """Validate parameters."""
        return True


@register_operation
class WaitForNavigation(Operation):
    """Wait for page navigation to complete."""
    
    def __init__(self):
        super().__init__("wait_for_navigation", "Wait for page navigation to complete", "browser_navigation")
    
    def execute(self, ui_automator, timeout: int = 30000, **kwargs) -> OperationResult:
        """Execute wait for navigation operation."""
        try:
            # Use the correct method name: wait_for_load_state() not wait_for_load_state()
            success = ui_automator.wait_for_load_state("networkidle", timeout=timeout)
            if success:
                return OperationResult(success=True, data=f"Waited for navigation (timeout: {timeout}ms)")
            else:
                return OperationResult(success=False, error="Wait for navigation failed")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, timeout: int = 30000, **kwargs) -> bool:
        """Validate parameters."""
        return isinstance(timeout, int) and timeout > 0


@register_operation
class NewTab(Operation):
    """Open a new tab."""
    
    def __init__(self):
        super().__init__("new_tab", "Open a new tab", "browser_navigation")
    
    def execute(self, ui_automator, **kwargs) -> OperationResult:
        """Execute new tab operation."""
        try:
            # Use the correct method name: new_tab() not new_tab()
            success = ui_automator.new_tab()
            if success:
                return OperationResult(success=True, data="Opened new tab")
            else:
                return OperationResult(success=False, error="New tab failed")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, **kwargs) -> bool:
        """Validate parameters."""
        return True


@register_operation
class CloseTab(Operation):
    """Close the current tab."""
    
    def __init__(self):
        super().__init__("close_tab", "Close the current tab", "browser_navigation")
    
    def execute(self, ui_automator, **kwargs) -> OperationResult:
        """Execute close tab operation."""
        try:
            # Use the correct method name: close_tab() not tab_close()
            success = ui_automator.close_tab()
            if success:
                return OperationResult(success=True, data="Closed current tab")
            else:
                return OperationResult(success=False, error="Close tab failed")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, **kwargs) -> bool:
        """Validate parameters."""
        return True


@register_operation
class FocusTab(Operation):
    """Focus a specific tab by index."""
    
    def __init__(self):
        super().__init__("focus_tab", "Focus a specific tab by index", "browser_navigation")
    
    def execute(self, ui_automator, index: int, **kwargs) -> OperationResult:
        """Execute focus tab operation."""
        try:
            # Use the correct method name: focus_tab() not tab_focus()
            success = ui_automator.focus_tab(index)
            if success:
                return OperationResult(success=True, data=f"Focused tab at index: {index}")
            else:
                return OperationResult(success=False, error="Focus tab failed")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, index: int = None, **kwargs) -> bool:
        """Validate parameters."""
        return isinstance(index, int) and index >= 0