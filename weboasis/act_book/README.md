# Act Book Module to Support Operating Browsers

## Design

- Registering operations into the act book
- Separating operation definition and registration from concrete implementation for specific UI automator types (such as Playwright and Selenium)
- Easy to extend and add new operations into the act book

## Current Structure

```
act_book/
├── __init__.py              # Main package initialization
├── controller.py            # High-level operation management
├── operations.py            # Centralized operation imports
├── core/                    # Core abstractions and registry
│   ├── __init__.py
│   ├── base.py              # Operation base classes
│   ├── registry.py          # Simplified operation registry
│   └── automator_interface.py # BrowserAutomator interface
├── book/                    # Operation implementations
│   ├── __init__.py
│   ├── browser/             # Browser interaction operations
│   │   ├── interaction.py   # Click, fill, type, etc.
│   │   ├── navigation.py    # Navigate, back, forward, etc.
│   │   └── extraction.py    # Get text, attributes, screenshots
│   ├── dom/                 # DOM manipulation operations
│   │   └── selector.py      # Find elements, wait for elements
│   └── composite/           # Complex operations
│       ├── forms.py         # Form filling, login
│       └── highlighting.py  # Element highlighting
└── engines/                 # Browser engine implementations
    ├── __init__.py
    ├── playwright/          # Playwright automation engine
    └── selenium/            # Selenium automation engine
```

## Key Features

### 1. Simplified Operation Registration
```python
from act_book import register_operation

@register_operation
class Click(Operation):
    """Click on an element."""
    
    def __init__(self):
        super().__init__("click", "Click on an element", "browser/interaction")
    
    def execute(self, automator: BrowserAutomator, bid: str = None, selector: str = None, **kwargs) -> OperationResult:
        # Implementation here
        pass
```

### 2. Clean Controller Interface
```python
from act_book.controller import ActBookController

# Initialize controller
controller = ActBookController(auto_register=True)

# List all operations
operations = controller.list_operations()

# Execute operations
result = controller.execute_operation("click", automator, bid="123.45")
```

### 3. Unified Browser Interface
```python
from act_book.core.automator_interface import BrowserAutomator

class MyAutomator(BrowserAutomator):
    def click(self, selector: str, **kwargs) -> bool:
        # Implement click logic
        pass
    
    def fill(self, selector: str, text: str, **kwargs) -> bool:
        # Implement fill logic
        pass
```

## Usage Examples

### Basic Operation Execution
```python
from act_book.controller import ActBookController
from WebOasis.ui_manager.playwright_manager import SyncPlaywrightManager

# Create manager and controller
manager = SyncPlaywrightManager()
controller = ActBookController()

# Execute operations
result = controller.execute_operation("click", manager, bid="123.45")
if result.success:
    print(f"Clicked element: {result.data}")
else:
    print(f"Error: {result.error}")
```

### Working with Categories
```python
# Get operations by category
browser_ops = controller.get_operations_by_category("browser/interaction")
dom_ops = controller.get_operations_by_category("dom")

# Get operation information
op_info = controller.get_operation_info()
click_info = controller.get_operation("click")
```

### Custom Operation Registration
```python
from act_book import register_operation

@register_operation
class CustomOperation(Operation):
    def __init__(self):
        super().__init__("custom", "Custom operation", "custom_category")
    
    def execute(self, automator: BrowserAutomator, **kwargs) -> OperationResult:
        # Custom logic here
        return OperationResult(success=True, data="Custom operation completed")
```

## Available Operations

### Browser Interactions (browser_interaction)
- `click` - Click elements by bid or selector
- `double_click` - Double click elements
- `hover` - Hover over elements
- `fill` - Fill form fields with text
- `type_text` - Type text into elements
- `check` - Check checkboxes/radio buttons
- `uncheck` - Uncheck checkboxes
- `select_option` - Select dropdown options
- `scroll` - Scroll page or elements
- `press` - Press keys on elements
- `mouse_click` - Click at specific coordinates
- `mouse_move` - Move mouse to coordinates
- `keyboard_type` - Type text using keyboard
- `keyboard_press` - Press key combinations
- `drag_and_drop` - Drag and drop elements
- `upload_file` - Upload files to elements

### Navigation (browser_navigation)
- `navigate` - Navigate to URL
- `back` - Go back in browser history
- `forward` - Go forward in browser history
- `refresh` - Refresh the current page
- `wait_for_navigation` - Wait for page navigation
- `new_tab` - Open a new tab
- `close_tab` - Close the current tab
- `focus_tab` - Focus a specific tab by index

### Information Extraction (browser_extraction)
- `get_text` - Get text content from elements
- `get_attribute` - Get attribute values from elements
- `get_screenshot` - Take screenshots of page or elements
- `get_url` - Get the current page URL
- `get_title` - Get the page title

### DOM Operations (dom_selector)
- `find_element` - Find single element by selector
- `find_elements` - Find multiple elements by selector
- `wait_for_element` - Wait for element to appear
- `element_exists` - Check if element exists
- `is_visible` - Check if element is visible

### Composite Operations (composite_forms, composite_highlighting)
- `fill_form` - Fill out forms with multiple fields
- `submit_form` - Submit forms
- `login` - Perform login operations
- `highlight_element` - Highlight elements for visualization
- `highlight_from_action` - Highlight based on action strings


## License

This implementation is part of the WebOasis project and follows the same licensing terms.



