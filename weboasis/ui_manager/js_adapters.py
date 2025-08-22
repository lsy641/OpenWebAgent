"""
Universal JavaScript adapter for Selenium to handle all JavaScript files from /javascripts folder.
Uses named async functions and Selenium's callback mechanism for maximum compatibility.
"""

import re
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)





class SeleniumJSAdapter:
    """
    Universal JavaScript adapter that can wrap any JavaScript file from /javascripts
    to work with Selenium's execute_script and execute_async_script.
    
    The adapter automatically detects the function signature and creates wrappers
    that handle both synchronous and asynchronous execution.
    """
    
    @staticmethod
    def wrap_async_function(js_code: str, function_name: str = None) -> str:
        """
        Converts Playwright-compatible JavaScript to Selenium-compatible JavaScript.
        
        The converter:
        1. Extracts the top function (arrow or regular) from the top
        2. Separates other functions below it
        3. Assigns the top function to a variable named 'seleniumMainFunction'
        4. Adds callback handling for execute_async_script
        
        Args:
            js_code: The JavaScript code to convert (typically from /javascripts folder)
            function_name: Optional name for the wrapped function (auto-detected if None)
        
        Returns:
            Converted JavaScript code ready for execute_async_script
        """
        
        # Parse the JavaScript code to extract top function and other functions
        top_function, other_functions = SeleniumJSAdapter._parse_js_structure(js_code)
        
        # Create the final Selenium-compatible code
        selenium_code = f"""
        // Get the arguments passed from Python, including the `done` callback
        const args = Array.prototype.slice.call(arguments, 0, -1);
        const done = arguments[arguments.length - 1];
        
        // Define other functions first
        {other_functions}
        
        // Define the main function
        const seleniumMainFunction = {top_function}
        
        // Execute the main function with arguments and handle result
        try {{
            const result = seleniumMainFunction(...args);
            
            // Check if the result is a promise
            if (result && typeof result.then === 'function') {{
                // It's a promise, handle it properly
                result.then(value => {{
                    done(value);
                }}).catch(error => {{
                    console.error('JavaScript execution error:', error);
                    done(error);
                }});
            }} else {{
                // It's not a promise, return the result directly
                done(result);
            }}
        }} catch (error) {{
            // Synchronous error: call the callback with the error
            console.error('JavaScript execution error:', error);
            done(error);
        }}
        """
        
        
        return selenium_code
    
    @staticmethod
    def wrap_sync_function(js_code: str, function_name: str = None) -> str:
        """
        Converts Playwright-compatible JavaScript to Selenium-compatible JavaScript for execute_script.
        
        The converter:
        1. Extracts the top function (arrow or regular) from the top
        2. Separates other functions below it
        3. Assigns the top function to a variable named 'seleniumMainFunction'
        4. Executes it synchronously and returns the result
        
        Args:
            js_code: The JavaScript code to convert (typically from /javascripts folder)
            function_name: Optional name for the wrapped function (auto-detected if None)
        
        Returns:
            Converted JavaScript code ready for execute_script
        """
        
        # Parse the JavaScript code to extract top function and other functions
        top_function, other_functions = SeleniumJSAdapter._parse_js_structure(js_code)
        

        
        # Create the final Selenium-compatible code
        selenium_code = f"""
        // Get the arguments passed from Python
        const args = Array.prototype.slice.call(arguments);
        
        // Define other functions first
        {other_functions}
        
        // Define the main function
        const seleniumMainFunction = {top_function}
        
        // Execute the main function with arguments and return result
        try {{
            const result = seleniumMainFunction(...args);
            return result;
        }} catch (error) {{
            // Synchronous error: log and return null
            console.error('JavaScript execution error:', error);
            return null;
        }}
        """
        
        
        return selenium_code
    
    # Specific wrapper methods removed - use wrap_async_function directly with JS file content
    
    @staticmethod
    def _parse_js_structure(js_code: str) -> tuple[str, str]:
        """
        Parses JavaScript code to separate the top function (arrow or regular) from other functions.
        
        The parser correctly handles nested functions by tracking brace depth.
        
        Args:
            js_code: Raw JavaScript code
            
        Returns:
            Tuple of (top_function, other_functions)
        """
        lines = js_code.split('\n')
        top_func_lines = []
        other_func_lines = []
        in_top_func = False
        brace_count = 0
        
        for line in lines:
            # Check if this line starts the top-level function (arrow or regular)
            if (('=>' in line or line.strip().startswith('function') or 
                 (line.strip().startswith('async') and 'function' in line) or
                 line.strip().startswith('(function')) and 
                not in_top_func):
                in_top_func = True
                top_func_lines.append(line)
                # Count opening braces
                brace_count += line.count('{') - line.count('}')
                continue
            
            if in_top_func:
                top_func_lines.append(line)
                brace_count += line.count('{') - line.count('}')
                # Only exit if we've closed all braces AND we're at the top level
                # This ensures nested functions don't prematurely end the parsing
                if brace_count <= 0:
                    in_top_func = False
            else:
                other_func_lines.append(line)
        
        top_function = '\n'.join(top_func_lines)
        other_functions = '\n'.join(other_func_lines)
        
        
        return top_function, other_functions
    
    # Method removed - no longer needed with simplified approach
    
    # _detect_function_name method removed - no longer needed
    

