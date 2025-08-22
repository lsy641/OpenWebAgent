"""
Browser extraction operations - getting data and content from the page.
"""

from weboasis.act_book.core.base import Operation, OperationResult
from weboasis.act_book.core.registry import register_operation


@register_operation
class GetText(Operation):
    """Get text content from an element."""
    
    def __init__(self):
        super().__init__("get_text", "Get text content from an element", "browser_extraction")
    
    def execute(self, ui_automator, selector: str = None, test_id: str = None, **kwargs) -> OperationResult:
        """Execute get text operation."""
        try:
            if test_id:
                text = ui_automator.get_text_by_test_id(test_id)
                return OperationResult(success=True, data=text, metadata={"test_id": test_id})
            elif selector:
                text = ui_automator.get_text(selector)
                return OperationResult(success=True, data=text, metadata={"selector": selector})
            else:
                return OperationResult(success=False, error="No selector or test_id provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return selector is not None or test_id is not None


@register_operation
class GetAttribute(Operation):
    """Get attribute value from an element."""
    
    def __init__(self):
        super().__init__("get_attribute", "Get attribute value from an element", "browser_extraction")
    
    def execute(self, ui_automator, attribute: str, selector: str = None, test_id: str = None, **kwargs) -> OperationResult:
        """Execute get attribute operation."""
        try:
            if test_id:
                value = ui_automator.get_attribute_by_test_id(test_id, attribute)
                return OperationResult(success=True, data=value, metadata={"test_id": test_id, "attribute": attribute})
            elif selector:
                value = ui_automator.get_attribute(selector, attribute)
                return OperationResult(success=True, data=value, metadata={"selector": selector, "attribute": attribute})
            else:
                return OperationResult(success=False, error="No selector or test_id provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, attribute: str = None, selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return attribute is not None and (selector is not None or test_id is not None)


@register_operation
class GetScreenshot(Operation):
    """Take a screenshot of the page or element."""
    
    def __init__(self):
        super().__init__("screenshot", "Take a screenshot of the page or element", "browser_extraction")
    
    def execute(self, ui_automator, path: str = "screenshot.png", selector: str = None, test_id: str = None, **kwargs) -> OperationResult:
        """Execute screenshot operation."""
        try:
            if test_id:
                screenshot_data = ui_automator.screenshot_by_test_id(test_id)
                if path and screenshot_data:
                    with open(path, 'wb') as f:
                        f.write(screenshot_data)
                    return OperationResult(success=True, data=path, metadata={"test_id": test_id, "path": path})
                return OperationResult(success=True, data=screenshot_data, metadata={"test_id": test_id})
            elif selector:
                # For selector-based screenshots, we need to implement element screenshot
                # For now, return full page screenshot
                screenshot_data = ui_automator.screenshot()
                if path and screenshot_data:
                    with open(path, 'wb') as f:
                        f.write(screenshot_data)
                    return OperationResult(success=True, data=path, metadata={"selector": selector, "path": path})
                return OperationResult(success=True, data=screenshot_data, metadata={"selector": selector})
            else:
                # Full page screenshot
                screenshot_data = ui_automator.screenshot()
                if path and screenshot_data:
                    with open(path, 'wb') as f:
                        f.write(screenshot_data)
                    return OperationResult(success=True, data=path, metadata={"path": path})
                return OperationResult(success=True, data=screenshot_data, metadata={"type": "full_page"})
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, path: str = "screenshot.png", selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return path is not None


@register_operation
class GetUrl(Operation):
    """Get the current page URL."""
    
    def __init__(self):
        super().__init__("get_current_url", "Get the current page URL", "browser_extraction")
    
    def execute(self, ui_automator, **kwargs) -> OperationResult:
        """Execute get URL operation."""
        try:
            url = ui_automator.get_current_url()
            return OperationResult(success=True, data=url)
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, **kwargs) -> bool:
        """Validate parameters."""
        return True


@register_operation
class GetTitle(Operation):
    """Get the page title."""
    
    def __init__(self):
        super().__init__("get_page_title", "Get the page title", "browser_extraction")
    
    def execute(self, ui_automator, **kwargs) -> OperationResult:
        """Execute get title operation."""
        try:
            title = ui_automator.get_page_title()
            return OperationResult(success=True, data=title)
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, **kwargs) -> bool:
        """Validate parameters."""
        return True 