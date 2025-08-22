"""
Operations Module - Imports and registers all operation classes
"""

# Import all operation classes from various modules
from .book.browser.interaction import (
    Click, DoubleClick, Hover, FormFill, Type, Check, Uncheck, 
    SelectOption, Scroll, Press, MouseClick, MouseMove, 
    KeyboardType, KeyboardPress
)

from .book.browser.navigation import (
    Navigate, Back, Forward, Refresh, WaitForNavigation, 
    NewTab, CloseTab, FocusTab
)

from .book.browser.extraction import (
    GetText, GetAttribute, GetScreenshot, GetUrl, GetTitle
)

from .book.dom.selector import (
    FindElement, FindElements, WaitForElement, ElementExists, IsVisible
)

from .book.composite.forms import (
    FillForm, SubmitForm, Login
)

from .book.composite.highlighting import (
    HighlightElement, HighlightFromAction
)

# General/flow operations
from .book.general.flow import (
    NoAction
)
# All operations are automatically registered when imported due to the @register_operation decorator

__all__ = [
    # Browser interaction operations
    'Click', 'DoubleClick', 'Hover', 'FormFill', 'Type', 'Check', 'Uncheck',
    'SelectOption', 'Scroll', 'Press', 'MouseClick', 'MouseMove',
    'KeyboardType', 'KeyboardPress',
    
    # Browser navigation operations
    'Navigate', 'Back', 'Forward', 'Refresh', 'WaitForNavigation',
    'NewTab', 'CloseTab', 'FocusTab',
    
    # Browser extraction operations
    'GetText', 'GetAttribute', 'GetScreenshot', 'GetUrl', 'GetTitle',
    
    # DOM selector operations
    'FindElement', 'FindElements', 'WaitForElement', 'ElementExists', 'IsVisible',
    
    # Composite operations
    'FillForm', 'SubmitForm', 'Login',
    'HighlightElement', 'HighlightFromAction'

    # General/flow operations
    'NoAction'
    
]
