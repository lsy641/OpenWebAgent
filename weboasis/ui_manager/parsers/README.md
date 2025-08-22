# Simple Parser System

## Overview

The parser handles different response formats that prompt engineers can design for their models:

- **Function call format**: `fill('29', 'c3c4')`
- **JSON format**: `{"action": "fill", "params": ["29", "c3c4"]}`
- **Natural language**: `"Fill the field with '29' and 'c3c4'"`

## Files

- `simple_parser.py` - The main parser implementation
- `__init__.py` - Module exports
- `README.md` - This documentation

## Usage

```python
from ttweb.ui_automator import create_simple_parser, ParsedAction

# Create a simple parser
parser = create_simple_parser()

# Parse different response formats
available_operations = ['click', 'type_text', 'fill', 'scroll']

# Function call format
response = "fill('29', 'c3c4')"
parsed = parser.parse(response, available_operations)
# Result: ParsedAction(operation_name='fill', parameters={'arg_0': '29', 'arg_1': 'c3c4'})

# JSON format
response = '{"action": "click", "params": ["submit"]}'
parsed = parser.parse(response, available_operations)
# Result: ParsedAction(operation_name='click', parameters={'arg_0': 'submit'})

# Natural language
response = 'Click the "Submit" button'
parsed = parser.parse(response, available_operations)
# Result: ParsedAction(operation_name='click', parameters={'arg_0': 'Submit'})
```

## Integration with simulated_webagent.py

The simple parser is used in `simulated_webagent.py` to parse LLM responses:

```python
from ttweb.ui_automator import create_simple_parser

# Create parser
parser = create_simple_parser()

# In the main loop
for i in range(3000):
    # ... get interactive elements and screenshot ...
    
    # Parse LLM response
    parsed_action = parser.parse(llm_response, available_operations)
    
    if parsed_action:
        # Execute the parsed action
        execute_operation(parsed_action.operation_name, parsed_action.parameters)
```

## Adding New Response Formats

To add support for new response formats, extend the `SimpleParser` class:

```python
def _parse_custom_format(self, response: str, available_operations: List[str]) -> Optional[ParsedAction]:
    # Your custom parsing logic here
    pass
```

Then add it to the main `parse` method.
