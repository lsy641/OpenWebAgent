"""
DOM selector operations - finding and waiting for elements.
"""

from weboasis.act_book.core.base import Operation, OperationResult
from weboasis.act_book.core.registry import register_operation


@register_operation
class FindElement(Operation):
    """Find an element by selector."""
    
    def __init__(self):
        super().__init__("find_element", "Find an element by selector", "dom_selector")
    
    def execute(self, ui_automator, selector: str, **kwargs) -> OperationResult:
        """Execute find element operation."""
        try:
            element = ui_automator.find_element(selector)
            if element:
                return OperationResult(success=True, data=element, metadata={"selector": selector})
            else:
                return OperationResult(success=False, error=f"Element not found: {selector}")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, selector: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return selector is not None


@register_operation
class FindElements(Operation):
    """Find multiple elements by selector."""
    
    def __init__(self):
        super().__init__("find_elements", "Find multiple elements by selector", "dom_selector")
    
    def execute(self, ui_automator, selector: str, **kwargs) -> OperationResult:
        """Execute find elements operation."""
        try:
            elements = ui_automator.find_elements(selector)
            return OperationResult(success=True, data=elements, metadata={"selector": selector, "count": len(elements)})
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, selector: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return selector is not None


@register_operation
class WaitForElement(Operation):
    """Wait for an element to appear."""
    
    def __init__(self):
        super().__init__("wait_for_element", "Wait for an element to appear", "dom_selector")
    
    def execute(self, ui_automator, selector: str, timeout: int = 5000, **kwargs) -> OperationResult:
        """Execute wait for element operation."""
        try:
            element = ui_automator.wait_for_element(selector, timeout=timeout)
            return OperationResult(success=True, data=element, metadata={"selector": selector, "timeout": timeout})
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, selector: str = None, timeout: int = 5000, **kwargs) -> bool:
        """Validate parameters."""
        return selector is not None and isinstance(timeout, int) and timeout > 0


@register_operation
class ElementExists(Operation):
    """Check if an element exists."""
    
    def __init__(self):
        super().__init__("element_exists", "Check if an element exists", "dom_selector")
    
    def execute(self, ui_automator, selector: str, **kwargs) -> OperationResult:
        """Execute element exists check."""
        try:
            exists = ui_automator.element_exists(selector)
            return OperationResult(success=True, data=exists, metadata={"selector": selector})
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, selector: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return selector is not None


@register_operation
class IsVisible(Operation):
    """Check if an element is visible."""
    
    def __init__(self):
        super().__init__("is_visible", "Check if an element is visible", "dom_selector")
    
    def execute(self, ui_automator, selector: str = None, test_id: str = None, **kwargs) -> OperationResult:
        """Execute visibility check."""
        try:
            if test_id:
                visible = ui_automator.is_visible_by_test_id(test_id)
                return OperationResult(success=True, data=visible, metadata={"test_id": test_id})
            elif selector:
                visible = ui_automator.is_visible(selector)
                return OperationResult(success=True, data=visible, metadata={"selector": selector})
            else:
                return OperationResult(success=False, error="No selector or test_id provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, selector: str = None, test_id: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return selector is not None or test_id is not None 