"""
Core components of the Action Book.
"""

from .base import Operation, OperationResult
from .registry import OperationRegistry, register_operation

__all__ = [
    'Operation', 'OperationResult',
    'OperationRegistry', 'register_operation'
] 