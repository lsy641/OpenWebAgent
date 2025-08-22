"""
Browser interaction operations - simulating user interactions.
"""

from weboasis.act_book.core.base import Operation, OperationResult
from weboasis.act_book.core.registry import register_operation
from weboasis.act_book.core.automator_interface import BrowserAutomator
from typing import Literal, List


@register_operation
class Click(Operation):
    """Click on an element."""
    
    def __init__(self):
        super().__init__("click", "Click on an element", "browser_interaction")
    
    def execute(self, automator: BrowserAutomator, test_id: str = None, selector: str = None, button: Literal["left", "middle", "right"] = "left", 
                modifiers: List[Literal["Alt", "Control", "Meta", "Shift"]] = None, timeout: int = 3000, **kwargs) -> OperationResult:
        """Execute click operation."""
        try:
            if modifiers is None:
                modifiers = []
                
            if test_id:
                # Use test_id if provided
                success = automator.click_by_test_id(test_id, button=button, modifiers=modifiers, timeout=timeout)
                if success:
                    return OperationResult(success=True, data=f"Clicked element with test_id: {test_id}")
                else:
                    return OperationResult(success=False, error=f"Failed to click element with test_id: {test_id}")
            elif selector:
                # Use selector if provided
                success = automator.click(selector, button=button, modifiers=modifiers, timeout=timeout)
                if success:
                    return OperationResult(success=True, data=f"Clicked element: {selector}")
                else:
                    return OperationResult(success=False, error=f"Failed to click element: {selector}")
            else:
                return OperationResult(success=False, error="No selector or test_id provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, test_id: str = None, selector: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return test_id is not None or selector is not None


@register_operation
class DoubleClick(Operation):
    """Double click on an element."""
    
    def __init__(self):
        super().__init__("double_click", "Double click on an element", "browser_interaction")
    
    def execute(self, automator: BrowserAutomator, test_id: str = None, selector: str = None, button: Literal["left", "middle", "right"] = "left", 
                modifiers: List[Literal["Alt", "Control", "Meta", "Shift"]] = None, **kwargs) -> OperationResult:
        """Execute double click operation."""
        try:
            if modifiers is None:
                modifiers = []
                
            if test_id:
                success = automator.double_click_by_test_id(test_id, button=button, modifiers=modifiers)
                if success:
                    return OperationResult(success=True, data=f"Double clicked element with test_id: {test_id}")
                else:
                    return OperationResult(success=False, error=f"Failed to double click element with test_id: {test_id}")
            elif selector:
                success = automator.double_click(selector, button=button, modifiers=modifiers)
                if success:
                    return OperationResult(success=True, data=f"Double clicked element: {selector}")
                else:
                    return OperationResult(success=False, error=f"Failed to double click element: {selector}")
            else:
                return OperationResult(success=False, error="No selector or test_id provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, test_id: str = None, selector: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return test_id is not None or selector is not None


@register_operation
class Hover(Operation):
    """Hover over an element."""
    
    def __init__(self):
        super().__init__("hover", "Hover over an element", "browser_interaction")
    
    def execute(self, automator: BrowserAutomator, test_id: str = None, selector: str = None, **kwargs) -> OperationResult:
        """Execute hover operation."""
        try:
            if test_id:
                success = automator.hover_by_test_id(test_id)
                if success:
                    return OperationResult(success=True, data=f"Hovered over element with test_id: {test_id}")
                else:
                    return OperationResult(success=False, error=f"Failed to hover over element with test_id: {test_id}")
            elif selector:
                success = automator.hover(selector)
                if success:
                    return OperationResult(success=True, data=f"Hovered over element: {selector}")
                else:
                    return OperationResult(success=False, error=f"Failed to hover over element: {selector}")
            else:
                return OperationResult(success=False, error="No selector or test_id provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, test_id: str = None, selector: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return test_id is not None or selector is not None


@register_operation
class FormFill(Operation):
    """Fill a form field with text."""
    
    def __init__(self):
        super().__init__("form_fill", "Fill a form field with text", "browser_interaction")
    
    def execute(self, automator: BrowserAutomator, test_id: str = None, selector: str = None, value: str = None, timeout: int = 10000, **kwargs) -> OperationResult:
        """Execute fill operation."""
        try:
            if test_id:
                success = automator.fill_by_test_id(test_id, value, timeout=timeout)
                if success:
                    return OperationResult(success=True, data=f"Filled element with test_id: {test_id}")
                else:
                    return OperationResult(success=False, error=f"Failed to fill element with test_id: {test_id}")
            elif selector:
                success = automator.fill(selector, value, timeout=timeout)
                if success:
                    return OperationResult(success=True, data=f"Filled element: {selector}")
                else:
                    return OperationResult(success=False, error=f"Failed to fill element: {selector}")
            else:
                return OperationResult(success=False, error="No selector or test_id provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, test_id: str = None, selector: str = None, value: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return (test_id is not None or selector is not None) and value is not None


@register_operation
class Type(Operation):
    """Type text into an element."""
    
    def __init__(self):
        super().__init__("type", "Type text into an element", "browser_interaction")
    
    def execute(self, automator: BrowserAutomator, text: str, test_id: str = None, selector: str = None, **kwargs) -> OperationResult:
        """Execute type operation."""
        try:
            if test_id:
                success = automator.type_text_by_test_id(test_id, text)
                if success:
                    return OperationResult(success=True, data=f"Typed '{text}' into element with test_id: {test_id}")
                else:
                    return OperationResult(success=False, error=f"Failed to type into element with test_id: {test_id}")
            elif selector:
                success = automator.type_text(selector, text)
                if success:
                    return OperationResult(success=True, data=f"Typed '{text}' into element: {selector}")
                else:
                    return OperationResult(success=False, error=f"Failed to type into element: {selector}")
            else:
                return OperationResult(success=False, error="No selector or test_id provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, text: str = None, test_id: str = None, selector: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return text is not None and (test_id is not None or selector is not None)


@register_operation
class ClearInput(Operation):
    """Clear text content of an input/textarea element."""
    
    def __init__(self):
        super().__init__("clear_input", "Clear text content of an input/textarea element", "browser_interaction")
    
    def execute(self, automator: BrowserAutomator, test_id: str = None, selector: str = None, **kwargs) -> OperationResult:
        """Execute clear_input operation using test_id or selector."""
        try:
            if test_id:
                success = automator.clear_by_test_id(test_id)
                if success:
                    return OperationResult(success=True, data=f"Cleared input with test_id: {test_id}")
                else:
                    return OperationResult(success=False, error=f"Failed to clear input with test_id: {test_id}")
            elif selector:
                success = automator.clear(selector)
                if success:
                    return OperationResult(success=True, data=f"Cleared input: {selector}")
                else:
                    return OperationResult(success=False, error=f"Failed to clear input: {selector}")
            else:
                return OperationResult(success=False, error="No selector or test_id provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, test_id: str = None, selector: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return test_id is not None or selector is not None


@register_operation
class Check(Operation):
    """Check a checkbox or radio button."""
    
    def __init__(self):
        super().__init__("check", "Check a checkbox or radio button", "browser_interaction")
    
    def execute(self, automator: BrowserAutomator, test_id: str = None, selector: str = None, **kwargs) -> OperationResult:
        """Execute check operation."""
        try:
            if test_id:
                success = automator.check_by_test_id(test_id)
                if success:
                    return OperationResult(success=True, data=f"Checked element with test_id: {test_id}")
                else:
                    return OperationResult(success=False, error=f"Failed to check element with test_id: {test_id}")
            elif selector:
                success = automator.check(selector)
                if success:
                    return OperationResult(success=True, data=f"Checked element: {selector}")
                else:
                    return OperationResult(success=False, error=f"Failed to check element: {selector}")
            else:
                return OperationResult(success=False, error="No selector or test_id provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, test_id: str = None, selector: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return test_id is not None or selector is not None


@register_operation
class Uncheck(Operation):
    """Uncheck a checkbox."""
    
    def __init__(self):
        super().__init__("uncheck", "Uncheck a checkbox", "browser_interaction")
    
    def execute(self, automator: BrowserAutomator, test_id: str = None, selector: str = None, **kwargs) -> OperationResult:
        """Execute uncheck operation."""
        try:
            if test_id:
                success = automator.uncheck_by_test_id(test_id)
                if success:
                    return OperationResult(success=True, data=f"Unchecked element with test_id: {test_id}")
                else:
                    return OperationResult(success=False, error=f"Failed to uncheck element with test_id: {test_id}")
            elif selector:
                success = automator.uncheck(selector)
                if success:
                    return OperationResult(success=True, data=f"Unchecked element: {selector}")
                else:
                    return OperationResult(success=False, error=f"Failed to uncheck element: {selector}")
            else:
                return OperationResult(success=False, error="No selector or test_id provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, test_id: str = None, selector: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return test_id is not None or selector is not None


@register_operation
class SelectOption(Operation):
    """Select option(s) from a dropdown."""
    
    def __init__(self):
        super().__init__("select_option", "Select option(s) from a dropdown", "browser_interaction")
    
    def execute(self, automator: BrowserAutomator, test_id: str = None, selector: str = None, options: str | List[str] = None, **kwargs) -> OperationResult:
        """Execute select option operation."""
        try:
            if test_id:
                success = automator.select_option_by_test_id(test_id, options)
                if success:
                    return OperationResult(success=True, data=f"Selected options in element with test_id: {test_id}")
                else:
                    return OperationResult(success=False, error=f"Failed to select options in element with test_id: {test_id}")
            elif selector:
                success = automator.select_option(selector, options)
                if success:
                    return OperationResult(success=True, data=f"Selected options in element: {selector}")
                else:
                    return OperationResult(success=False, error=f"Failed to select options in element: {selector}")
            else:
                return OperationResult(success=False, error="No selector or test_id provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, test_id: str = None, selector: str = None, options: str | List[str] = None, **kwargs) -> bool:
        """Validate parameters."""
        return (test_id is not None or selector is not None) and options is not None


@register_operation
class Scroll(Operation):
    """Scroll with three modes: general, from absolute position, or from an element."""
    
    def __init__(self):
        super().__init__("scroll", "Scroll around an element by (delta_x, delta_y)", "browser_interaction")
    
    def execute(
        self,
        automator: BrowserAutomator,
        delta_x: float = 0,
        delta_y: float = 300,
        x: float = None,
        y: float = None,
        test_id: str = None,
        selector: str = None,
        **kwargs,
    ) -> OperationResult:
        """Execute scroll.
        - scroll(delta_x, delta_y): general page scroll
        - scroll(x, y, delta_x, delta_y): scroll from absolute position
        - scroll(test_id|selector, delta_x, delta_y): scroll from element position
        """
        try:
            if test_id is not None or selector is not None:
                # Element-based
                success = automator.scroll_around_element(selector=selector, test_id=test_id, delta_x=delta_x, delta_y=delta_y)
                if success:
                    target = f"test_id={test_id}" if test_id else f"selector={selector}"
                    return OperationResult(success=True, data=f"Scrolled {target} by ({delta_x}, {delta_y})")
                return OperationResult(success=False, error="Failed to scroll from element")
            if x is not None and y is not None:
                # Absolute position-based
                success = automator.scroll_from_position(x, y, delta_x=delta_x, delta_y=delta_y)
                if success:
                    return OperationResult(success=True, data=f"Scrolled from ({x}, {y}) by ({delta_x}, {delta_y})")
                return OperationResult(success=False, error="Failed to scroll from position")
            # General page scroll
            success = automator.scroll(delta_x, delta_y)
            if success:
                return OperationResult(success=True, data=f"Scrolled by ({delta_x}, {delta_y})")
            return OperationResult(success=False, error="Failed to scroll")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, delta_x: float = 0, delta_y: float = 300, x: float = None, y: float = None, test_id: str = None, selector: str = None, **kwargs) -> bool:
        """Validate parameters for any of the three modes."""
        if not isinstance(delta_x, (int, float)) or not isinstance(delta_y, (int, float)):
            return False
        # Mode 1: general
        if x is None and y is None and test_id is None and selector is None:
            return True
        # Mode 2: position-based
        if x is not None and y is not None and test_id is None and selector is None:
            return isinstance(x, (int, float)) and isinstance(y, (int, float))
        # Mode 3: element-based
        if (test_id is not None) ^ (selector is not None) or (test_id is not None and selector is not None):
            return True
        return False


@register_operation
class Press(Operation):
    """Press a key on an element."""
    
    def __init__(self):
        super().__init__("press", "Press a key on an element", "browser_interaction")
    
    def execute(self, automator: BrowserAutomator, test_id: str = None, selector: str = None, key: str = None, **kwargs) -> OperationResult:
        """Execute press operation."""
        try:
            if test_id:
                success = automator.press_by_test_id(test_id, key)
                if success:
                    return OperationResult(success=True, data=f"Pressed '{key}' on element with test_id: {test_id}")
                else:
                    return OperationResult(success=False, error=f"Failed to press key on element with test_id: {test_id}")
            elif selector:
                success = automator.press(selector, key)
                if success:
                    return OperationResult(success=True, data=f"Pressed '{key}' on element: {selector}")
                else:
                    return OperationResult(success=False, error=f"Failed to press key on element: {selector}")
            else:
                return OperationResult(success=False, error="No selector or test_id provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, test_id: str = None, selector: str = None, key: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return (test_id is not None or selector is not None) and key is not None


@register_operation
class MouseClick(Operation):
    """Click at specific coordinates."""
    
    def __init__(self):
        super().__init__("mouse_click", "Click at specific coordinates", "browser_interaction")
    
    def execute(self, automator: BrowserAutomator, x: float, y: float, button: Literal["left", "middle", "right"] = "left", **kwargs) -> OperationResult:
        """Execute mouse click operation."""
        try:
            success = automator.mouse_click(x, y, button=button)
            if success:
                return OperationResult(success=True, data=f"Mouse clicked at ({x}, {y})")
            else:
                return OperationResult(success=False, error="Failed to perform mouse click")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, x: float = None, y: float = None, **kwargs) -> bool:
        """Validate parameters."""
        return isinstance(x, (int, float)) and isinstance(y, (int, float))


@register_operation
class MouseMove(Operation):
    """Move mouse to specific coordinates."""
    
    def __init__(self):
        super().__init__("mouse_move", "Move mouse to specific coordinates", "browser_interaction")
    
    def execute(self, automator: BrowserAutomator, x: float, y: float, **kwargs) -> OperationResult:
        """Execute mouse move operation."""
        try:
            success = automator.mouse_move(x, y)
            if success:
                return OperationResult(success=True, data=f"Mouse moved to ({x}, {y})")
            else:
                return OperationResult(success=False, error="Failed to move mouse")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, x: float = None, y: float = None, **kwargs) -> bool:
        """Validate parameters."""
        return isinstance(x, (int, float)) and isinstance(y, (int, float))


@register_operation
class KeyboardType(Operation):
    """Type text using keyboard."""
    
    def __init__(self):
        super().__init__("keyboard_type", "Type text using keyboard", "browser_interaction")
    
    def execute(self, automator: BrowserAutomator, text: str, **kwargs) -> OperationResult:
        """Execute keyboard type operation."""
        try:
            success = automator.keyboard_type(text)
            if success:
                return OperationResult(success=True, data=f"Typed '{text}' using keyboard")
            else:
                return OperationResult(success=False, error="Failed to type using keyboard")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, text: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return text is not None


@register_operation
class KeyboardPress(Operation):
    """Press a key combination."""
    
    def __init__(self):
        super().__init__("keyboard_press", "Press a key combination", "browser_interaction")
    
    def execute(self, automator: BrowserAutomator, key: str, **kwargs) -> OperationResult:
        """Execute keyboard press operation."""
        try:
            success = automator.keyboard_press(key)
            if success:
                return OperationResult(success=True, data=f"Pressed key: {key}")
            else:
                return OperationResult(success=False, error="Failed to press key")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, key: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return key is not None


@register_operation
class DragAndDrop(Operation):
    """Drag and drop an element to another location."""
    
    def __init__(self):
        super().__init__("drag_and_drop", "Drag and drop an element to another location", "browser_interaction")
    
    def execute(self, automator: BrowserAutomator, from_test_id: str = None, to_test_id: str = None, 
                from_selector: str = None, to_selector: str = None, **kwargs) -> OperationResult:
        """Execute drag and drop operation."""
        try:
            if from_test_id and to_test_id:
                # Use test_id if provided
                success = automator.drag_and_drop_by_test_id(from_test_id, to_test_id)
                if success:
                    return OperationResult(success=True, data=f"Dragged element with test_id {from_test_id} to element with test_id {to_test_id}")
                else:
                    return OperationResult(success=False, error=f"Failed to drag and drop from test_id {from_test_id} to test_id {to_test_id}")
            elif from_selector and to_selector:
                # Use selector if provided
                success = automator.drag_and_drop(from_selector, to_selector)
                if success:
                    return OperationResult(success=True, data=f"Dragged element {from_selector} to element {to_selector}")
                else:
                    return OperationResult(success=False, error=f"Failed to drag and drop from {from_selector} to {to_selector}")
            else:
                return OperationResult(success=False, error="Both from and to selectors/test_ids must be provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, from_test_id: str = None, to_test_id: str = None, 
                       from_selector: str = None, to_selector: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return (from_test_id is not None and to_test_id is not None) or (from_selector is not None and to_selector is not None)


@register_operation
class UploadFile(Operation):
    """Upload a file to an element."""
    
    def __init__(self):
        super().__init__("upload_file", "Upload a file to an element", "browser_interaction")
    
    def execute(self, automator: BrowserAutomator, test_id: str = None, selector: str = None, 
                file_path: str = None, file_paths: List[str] = None, **kwargs) -> OperationResult:
        """Execute file upload operation."""
        try:
            if file_paths is None:
                file_paths = [file_path] if file_path else []
            
            if not file_paths:
                return OperationResult(success=False, error="No file path provided")
            
            if test_id:
                success = automator.upload_file_by_test_id(test_id, file_paths)
                if success:
                    return OperationResult(success=True, data=f"Uploaded files to element with test_id {test_id}: {file_paths}")
                else:
                    return OperationResult(success=False, error=f"Failed to upload files to element with test_id {test_id}")
            elif selector:
                success = automator.upload_file(selector, file_paths)
                if success:
                    return OperationResult(success=True, data=f"Uploaded files to element {selector}: {file_paths}")
                else:
                    return OperationResult(success=False, error=f"Failed to upload files to element {selector}")
            else:
                return OperationResult(success=False, error="No selector or test_id provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, test_id: str = None, selector: str = None, 
                       file_path: str = None, file_paths: List[str] = None, **kwargs) -> bool:
        """Validate parameters."""
        has_element = test_id is not None or selector is not None
        has_files = file_path is not None or file_paths is not None
        return has_element and has_files


@register_operation
class PlayVideo(Operation):
    """Play a video element."""
    
    def __init__(self):
        super().__init__("play_video", "Play a video element", "browser_interaction")
    
    def execute(self, automator: BrowserAutomator, test_id: str = None, selector: str = None, **kwargs) -> OperationResult:
        """Execute play video operation."""
        try:
            if test_id:
                success = automator.play_video_by_test_id(test_id)
                if success:
                    return OperationResult(success=True, data=f"Started playing video with test_id {test_id}")
                else:
                    return OperationResult(success=False, error=f"Failed to play video with test_id {test_id}")
            elif selector:
                success = automator.play_video(selector)
                if success:
                    return OperationResult(success=True, data=f"Started playing video {selector}")
                else:
                    return OperationResult(success=False, error=f"Failed to play video {selector}")
            else:
                return OperationResult(success=False, error="No selector or test_id provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, test_id: str = None, selector: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return test_id is not None or selector is not None


@register_operation
class PauseVideo(Operation):
    """Pause a video element."""
    
    def __init__(self):
        super().__init__("pause_video", "Pause a video element", "browser_interaction")
    
    def execute(self, automator: BrowserAutomator, test_id: str = None, selector: str = None, **kwargs) -> OperationResult:
        """Execute pause video operation."""
        try:
            if test_id:
                success = automator.pause_video_by_test_id(test_id)
                if success:
                    return OperationResult(success=True, data=f"Paused video with test_id {test_id}")
                else:
                    return OperationResult(success=False, error=f"Failed to pause video with test_id {test_id}")
            elif selector:
                success = automator.pause_video(selector)
                if success:
                    return OperationResult(success=True, data=f"Paused video {selector}")
                else:
                    return OperationResult(success=False, error=f"Failed to pause video {selector}")
            else:
                return OperationResult(success=False, error="No selector or test_id provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, test_id: str = None, selector: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return test_id is not None or selector is not None 