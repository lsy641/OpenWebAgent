"""
Composite form operations - complex form interactions.
"""

from weboasis.act_book.core.base import Operation, OperationResult
from weboasis.act_book.core.registry import register_operation


@register_operation
class FillForm(Operation):
    """Fill out a form with multiple fields."""
    
    def __init__(self):
        super().__init__("fill_form", "Fill out a form with multiple fields", "composite_forms")
    
    def execute(self, ui_automator, form_data: dict, **kwargs) -> OperationResult:
        """Execute fill form operation."""
        try:
            results = []
            for field_selector, value in form_data.items():
                # Type the value into the field
                type_op = ui_automator.get_operation("type")
                result = type_op.execute(ui_automator, selector=field_selector, text=value)
                results.append(result)
                
                if not result.success:
                    return OperationResult(success=False, error=f"Failed to fill field {field_selector}: {result.error}")
            
            return OperationResult(success=True, data=f"Filled {len(form_data)} form fields", metadata={"results": results})
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, form_data: dict = None, **kwargs) -> bool:
        """Validate parameters."""
        return form_data is not None and isinstance(form_data, dict) and len(form_data) > 0


@register_operation
class SubmitForm(Operation):
    """Submit a form."""
    
    def __init__(self):
        super().__init__("submit_form", "Submit a form", "composite_forms")
    
    def execute(self, ui_automator, submit_button_selector: str = None, form_selector: str = None, **kwargs) -> OperationResult:
        """Execute submit form operation."""
        try:
            if submit_button_selector:
                # Click the submit button
                click_op = ui_automator.get_operation("click")
                result = click_op.execute(ui_automator, selector=submit_button_selector)
                return result
            elif form_selector:
                # Submit the form directly
                ui_automator.submit_form(form_selector)
                return OperationResult(success=True, data=f"Submitted form: {form_selector}")
            else:
                return OperationResult(success=False, error="No submit button or form selector provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, submit_button_selector: str = None, form_selector: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return submit_button_selector is not None or form_selector is not None


@register_operation
class Login(Operation):
    """Perform a login operation."""
    
    def __init__(self):
        super().__init__("login", "Perform a login operation", "composite_forms")
    
    def execute(self, ui_automator, username: str, password: str, username_field: str, password_field: str, submit_button: str, **kwargs) -> OperationResult:
        """Execute login operation."""
        try:
            # Fill username
            type_op = ui_automator.get_operation("type")
            result = type_op.execute(ui_automator, selector=username_field, text=username)
            if not result.success:
                return result
            
            # Fill password
            result = type_op.execute(ui_automator, selector=password_field, text=password)
            if not result.success:
                return result
            
            # Click submit
            click_op = ui_automator.get_operation("click")
            result = click_op.execute(ui_automator, selector=submit_button)
            if not result.success:
                return result
            
            return OperationResult(success=True, data="Login operation completed")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, username: str = None, password: str = None, username_field: str = None, password_field: str = None, submit_button: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return all([username, password, username_field, password_field, submit_button]) 