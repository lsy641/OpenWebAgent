"""
Simple Parser System for UI Automation

This module provides a simple parser system focused on response formats
that prompt engineers design, not on specific models.
"""

from .simple_parser import (
    SimpleParser,
    ParsedAction,
    create_simple_parser
)

__all__ = [
    # Simple parser
    'SimpleParser',
    'ParsedAction',
    'create_simple_parser'
]
