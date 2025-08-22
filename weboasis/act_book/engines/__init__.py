"""
Automation engines module.
Contains implementations for different browser automation engines.
"""

from weboasis.act_book.engines.playwright.playwright_automator import PlaywrightAutomator
from weboasis.act_book.engines.selenium.selenium_automator import SeleniumAutomator

__all__ = ['PlaywrightAutomator', 'SeleniumAutomator']
