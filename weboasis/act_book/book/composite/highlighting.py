"""
Composite operations - highlighting elements for visualization.
"""

import logging
from typing import Dict, Any, Optional
from weboasis.act_book.core.base import Operation, OperationResult
from weboasis.act_book.core.registry import register_operation
from weboasis.act_book.core.extractor import extract_bid_from_action

logger = logging.getLogger(__name__)


@register_operation
class HighlightElement(Operation):
    """Highlight an element on the page for visualization."""
    
    def __init__(self):
        super().__init__("highlight_element", "Highlight an element on the page", "composite_highlighting")
    
    def execute(self, ui_automator, bid: str = None, selector: str = None, text: str = "Highlighted", **kwargs) -> OperationResult:
        """Execute highlight operation."""
        try:
            if bid:
                self._highlight_element_by_bid(ui_automator, bid, text)
                return OperationResult(success=True, data=f"Highlighted element with bid: {bid}")
            elif selector:
                # Find element by selector and get its bid
                element = ui_automator.find_element(selector)
                if element and hasattr(element, 'get_attribute'):
                    element_bid = element.get_attribute(ui_automator.test_id_attribute)
                    if element_bid:
                        self._highlight_element_by_bid(ui_automator, element_bid, text)
                        return OperationResult(success=True, data=f"Highlighted element: {selector}")
                    else:
                        return OperationResult(success=False, error=f"No bid found for element: {selector}")
                else:
                    return OperationResult(success=False, error=f"Element not found: {selector}")
            else:
                return OperationResult(success=False, error="No bid or selector provided")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, bid: str = None, selector: str = None, text: str = "Highlighted", **kwargs) -> bool:
        """Validate parameters."""
        return (bid is not None or selector is not None) and text is not None
    
    def _highlight_element_by_bid(self, ui_automator, bid: str, text: str):
        """Internal method to highlight element by bid."""
        # Get the element using the bid
        elem = ui_automator.get_elem_by_bid(bid)
        if not elem:
            raise ValueError(f"Element with bid {bid} not found")
        
        # Get the bounding box of the element
        box = elem.bounding_box()
        if not box:
            raise ValueError(f"Could not get bounding box for element with bid {bid}")
        
        # Calculate enlarged box dimensions (25% padding)
        padding = min(box['width'], box['height']) * 0.25
        enlarged_box = {
            'x': box['x'] - padding,
            'y': box['y'] - padding,
            'width': box['width'] + padding * 2,
            'height': box['height'] + padding * 2
        }
        
        # Load custom fonts from Google Fonts
        ui_automator.page.evaluate("""
            (() => {
                const link = document.createElement('link');
                link.href = 'https://fonts.googleapis.com/css2?family=Raleway:wght@400;700&family=Roboto:wght@400;700&family=Hind+Siliguri:wght@400;700&display=swap';
                link.rel = 'stylesheet';
                document.head.appendChild(link);
            })()
        """)
        
        # Create a larger highlight with custom text
        ui_automator.page.evaluate(
            """
            ([box, text]) => {
                const overlay = document.createElement('div');
                document.body.appendChild(overlay);
                overlay.setAttribute('style', `
                    all: initial;
                    position: fixed;
                    border: 2px solid #79bd9a;
                    borderRadius: 10px;
                    boxShadow: 0 0 0 4000px rgba(0, 0, 0, 0.1);
                    left: ${box.x}px;
                    top: ${box.y}px;
                    width: ${box.width}px;
                    height: ${box.height}px;
                    z-index: 2147483646;
                    pointerEvents: none;
                `);

                const textElement = document.createElement('div');
                textElement.textContent = text;
                textElement.setAttribute('style', `
                    position: absolute;
                    top: -40px;
                    left: 50%;
                    transform: translateX(-50%);
                    background-color: #79bd9a;
                    color: white;
                    padding: 8px 10px;
                    border-radius: 10px;
                    fontFamily: Roboto, Raleway, Hind Siliguri;
                    fontSize: 16px;
                    fontWeight: bold;
                `);
                overlay.appendChild(textElement);

                setTimeout(() => {
                    document.body.removeChild(overlay);
                }, 5000);  // Remove after 5 seconds
            }
            """,
            [enlarged_box, text]
        )
        
        # Wait for the highlight to be visible
        ui_automator.page.wait_for_timeout(5000)  # Wait for 5 seconds


@register_operation
class HighlightFromAction(Operation):
    """Highlight an element based on an action string."""
    
    def __init__(self):
        super().__init__("highlight_from_action", "Highlight element from action string", "composite_highlighting")
    
    def execute(self, ui_automator, action: str, **kwargs) -> OperationResult:
        """Execute highlight from action operation."""
        try:
            # Extract the bid from the action
            bid = extract_bid_from_action(action)
            
            # Highlight the element only if a bid is found
            if bid:
                highlight_op = HighlightElement()
                return highlight_op.execute(ui_automator, bid=bid, text=action)
            else:
                return OperationResult(success=False, error="No bid found in the action string. Skipping highlight.")
        except Exception as e:
            return OperationResult(success=False, error=str(e))
    
    def validate_params(self, action: str = None, **kwargs) -> bool:
        """Validate parameters."""
        return action is not None 