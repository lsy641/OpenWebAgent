
/**
 * Hide Developer Features Script
 * 
 * This script hides all elements that have the 'developer_elem' attribute.
 * Elements are hidden but not deleted, so they can be restored later if needed.
 */

(function() {
    'use strict';
    
    console.log('WebAgent: Hiding developer features...');
    
    // Find all elements with developer_elem attribute
    var developerElements = document.querySelectorAll('[developer_elem]');
    var hiddenCount = 0;
    
    console.log(`WebAgent: Found ${developerElements.length} developer elements to hide`);
    
    // Hide each developer element
    for (var i = 0; i < developerElements.length; i++) {
        var element = developerElements[i];
        try {
            // Store original display/visibility only once (do not overwrite)
            if (!element.hasAttribute('data-original-display')) {
                var originalDisplay = window.getComputedStyle(element).display;
                element.setAttribute('data-original-display', originalDisplay);
            }
            if (!element.hasAttribute('data-original-visibility')) {
                var originalVisibility = window.getComputedStyle(element).visibility;
                element.setAttribute('data-original-visibility', originalVisibility);
            }
            
            // Log what we're hiding
            var elementInfo = {
                tagName: element.tagName,
                id: element.id || 'No ID',
                className: element.className || 'No class',
                text: element.textContent?.trim().substring(0, 50) || 'No text'
            };
            
            console.log(`WebAgent: Hiding developer element:`, elementInfo);
            
            // Hide the element by setting display to none
            element.style.display = 'none';
            element.style.visibility = 'hidden';
            
            // Add a class to mark it as hidden
            element.classList.add('webagent-hidden');
            
            hiddenCount++;
            
        } catch (e) {
            console.error('WebAgent: Error hiding developer element:', e);
        }
    }
    
    // Also hide any remaining developer elements that might have been added dynamically
    setTimeout(function() {
        var remainingElements = document.querySelectorAll('[developer_elem]:not(.webagent-hidden)');
        if (remainingElements.length > 0) {
            console.log(`WebAgent: Found ${remainingElements.length} additional developer elements, hiding...`);
            
            for (var j = 0; j < remainingElements.length; j++) {
                var elem = remainingElements[j];
                try {
                    // Store original values only if not already stored
                    if (!elem.hasAttribute('data-original-display')) {
                        var originalDisplay = window.getComputedStyle(elem).display;
                        elem.setAttribute('data-original-display', originalDisplay);
                    }
                    if (!elem.hasAttribute('data-original-visibility')) {
                        var originalVisibility = window.getComputedStyle(elem).visibility;
                        elem.setAttribute('data-original-visibility', originalVisibility);
                    }
                    
                    // Hide the element
                    elem.style.display = 'none';
                    elem.style.visibility = 'hidden';
                    elem.classList.add('webagent-hidden');
                    
                    hiddenCount++;
                    
                } catch (e) {
                    console.error('WebAgent: Error hiding additional developer element:', e);
                }
            }
        }
    }, 100);
    
    console.log(`WebAgent: Successfully hidden ${hiddenCount} developer elements`);
    
    // Add utility functions to the global scope for showing/hiding
    window.webagentUtils = window.webagentUtils || {};
    
    // Function to show all hidden developer elements
    window.webagentUtils.showDeveloperElements = function() {
        var hiddenElements = document.querySelectorAll('.webagent-hidden');
        var shownCount = 0;
        
        for (var k = 0; k < hiddenElements.length; k++) {
            var elem = hiddenElements[k];
            try {
                // Restore original display and visibility
                var originalDisplay = elem.getAttribute('data-original-display');
                var originalVisibility = elem.getAttribute('data-original-visibility');
                
                if (originalDisplay) {
                    elem.style.display = originalDisplay;
                }
                if (originalVisibility) {
                    elem.style.visibility = originalVisibility;
                }
                
                // Remove hidden class
                elem.classList.remove('webagent-hidden');
                shownCount++;
                
            } catch (e) {
                console.error('WebAgent: Error showing developer element:', e);
            }
        }
        
        console.log(`WebAgent: Shown ${shownCount} developer elements`);
        return shownCount;
    };
    
    // Function to hide all developer elements again
    window.webagentUtils.hideDeveloperElements = function() {
        var developerElements = document.querySelectorAll('[developer_elem]:not(.webagent-hidden)');
        var hiddenCount = 0;
        
        for (var l = 0; l < developerElements.length; l++) {
            var elem = developerElements[l];
            try {
                // Store original values
                var originalDisplay = window.getComputedStyle(elem).display;
                elem.setAttribute('data-original-display', originalDisplay);
                
                var originalVisibility = window.getComputedStyle(elem).visibility;
                elem.setAttribute('data-original-visibility', originalVisibility);
                
                // Hide the element
                elem.style.display = 'none';
                elem.style.visibility = 'hidden';
                elem.classList.add('webagent-hidden');
                
                hiddenCount++;
                
            } catch (e) {
                console.error('WebAgent: Error hiding developer element:', e);
            }
        }
        
        console.log(`WebAgent: Hidden ${hiddenCount} developer elements`);
        return hiddenCount;
    };
    
    // Function to toggle developer elements visibility
    window.webagentUtils.toggleDeveloperElements = function() {
        var hiddenElements = document.querySelectorAll('.webagent-hidden');
        if (hiddenElements.length > 0) {
            return this.showDeveloperElements();
        } else {
            return this.hideDeveloperElements();
        }
    };
    
    console.log('WebAgent: Available utilities: webagentUtils.showDeveloperElements(), webagentUtils.hideDeveloperElements(), webagentUtils.toggleDeveloperElements()');
    
    // Return the count of hidden elements
    return hiddenCount;
    
})();