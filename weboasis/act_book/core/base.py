"""
Core base classes for the action book module.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional

from .automator_interface import BrowserAutomator


@dataclass
class OperationResult:
    """Result of an operation execution."""
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Operation(ABC):
    """Abstract base class for all operations."""
    
    def __init__(self, name: str, description: str, category: str = "general"):
        self.name = name
        self.description = description
        self.category = category
    
    @abstractmethod
    def execute(self, automator: BrowserAutomator, **kwargs) -> OperationResult:
        """Execute the operation using the provided automator."""
        pass
    
    @abstractmethod
    def validate_params(self, **kwargs) -> bool:
        """Validate the parameters for this operation."""
        pass
    
    def __str__(self) -> str:
        return f"{self.name} ({self.category}): {self.description}"
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>" 