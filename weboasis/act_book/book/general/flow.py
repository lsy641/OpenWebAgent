"""
General flow/control operations
"""

import time
import logging
from weboasis.act_book.core.base import Operation, OperationResult
from weboasis.act_book.core.registry import register_operation

logger = logging.getLogger(__name__)


@register_operation
class NoAction(Operation):
    """Explicitly take no action (no-op), optionally waiting before continuing."""

    def __init__(self):
        super().__init__("no_action", "Do nothing (optional wait in ms, default 1000ms)", "general")

    def execute(self, ui_automator, timeout: int = 1000, **kwargs) -> OperationResult:
        """Perform no operation; wait for 'timeout' milliseconds (default 1000)."""
        try:
            if isinstance(timeout, (int, float)) and timeout > 0:
                time.sleep(timeout / 1000.0)
            return OperationResult(success=True, data=f"No action executed (waited {int(timeout)} ms)")
        except Exception as e:
            logger.warning(f"NoAction operation failed: {e}")
            return OperationResult(success=False, error=str(e))

    def validate_params(self, timeout: int = 1000, **kwargs) -> bool:
        try:
            return int(timeout) >= 0
        except Exception:
            return False


