/**
 * Show Developer Features Script
 * 
 * This script shows all previously hidden developer elements that have the 'developer_elem' attribute.
 * Restores elements to their original display and visibility states.
 */

(function() {
    'use strict';
    
    console.log('WebAgent: Showing developer features...');
    
    // Find all hidden developer elements
    var hiddenElements = document.querySelectorAll('.webagent-hidden');
    var shownCount = 0;
    
    console.log(`WebAgent: Found ${hiddenElements.length} hidden developer elements to show`);
    
    // Show each hidden developer element
    for (var i = 0; i < hiddenElements.length; i++) {
        var element = hiddenElements[i];
        try {
            // Get stored original values
            var originalDisplay = element.getAttribute('data-original-display');
            var originalVisibility = element.getAttribute('data-original-visibility');
            
            // Log what we're showing
            var elementInfo = {
                tagName: element.tagName,
                id: element.id || 'No ID',
                className: element.className || 'No class',
                text: element.textContent?.trim().substring(0, 50) || 'No text'
            };
            
            console.log(`WebAgent: Showing developer element:`, elementInfo);
            
            // Restore original display value
            if (originalDisplay) {
                element.style.display = originalDisplay;
                console.log(`WebAgent: Restored display to: ${originalDisplay}`);
            } else {
                // Fallback to default display if no original value stored
                element.style.display = '';
                console.log(`WebAgent: Reset display to default`);
            }
            
            // Restore original visibility value
            if (originalVisibility) {
                element.style.visibility = originalVisibility;
                console.log(`WebAgent: Restored visibility to: ${originalVisibility}`);
            } else {
                // Fallback to default visibility if no original value stored
                element.style.visibility = '';
                console.log(`WebAgent: Reset visibility to default`);
            }
            
            // Remove the hidden class
            element.classList.remove('webagent-hidden');
            
            // Remove the stored attributes
            element.removeAttribute('data-original-display');
            element.removeAttribute('data-original-visibility');
            
            shownCount++;
            
        } catch (e) {
            console.error('WebAgent: Error showing developer element:', e);
        }
    }
    
    // Also check for any developer elements that might not have the hidden class
    var allDeveloperElements = document.querySelectorAll('[developer_elem]');
    var visibleCount = 0;
    
    for (var j = 0; j < allDeveloperElements.length; j++) {
        var elem = allDeveloperElements[j];
        var computedStyle = window.getComputedStyle(elem);
        
        if (computedStyle.display !== 'none' && computedStyle.visibility !== 'hidden') {
            visibleCount++;
        }
    }
    
    console.log(`WebAgent: Successfully shown ${shownCount} developer elements`);
    console.log(`WebAgent: Total visible developer elements: ${visibleCount}`);
    
    // Add utility functions to the global scope
    window.webagentUtils = window.webagentUtils || {};
    
    // Function to check if developer elements are visible
    window.webagentUtils.areDeveloperElementsVisible = function() {
        var hiddenElements = document.querySelectorAll('.webagent-hidden');
        return hiddenElements.length === 0;
    };
    
    // Function to get count of visible developer elements
    window.webagentUtils.getVisibleDeveloperElementsCount = function() {
        var allElements = document.querySelectorAll('[developer_elem]');
        var visibleCount = 0;
        
        for (var k = 0; k < allElements.length; k++) {
            var elem = allElements[k];
            var computedStyle = window.getComputedStyle(elem);
            
            if (computedStyle.display !== 'none' && computedStyle.visibility !== 'hidden') {
                visibleCount++;
            }
        }
        
        return visibleCount;
    };
    
    // Function to get count of hidden developer elements
    window.webagentUtils.getHiddenDeveloperElementsCount = function() {
        var hiddenElements = document.querySelectorAll('.webagent-hidden');
        return hiddenElements.length;
    };
    
    // Function to show specific developer element by ID
    window.webagentUtils.showDeveloperElementById = function(elementId) {
        var element = document.getElementById(elementId);
        if (element && element.hasAttribute('developer_elem')) {
            try {
                var originalDisplay = element.getAttribute('data-original-display');
                var originalVisibility = element.getAttribute('data-original-visibility');
                
                if (originalDisplay) {
                    element.style.display = originalDisplay;
                } else {
                    element.style.display = '';
                }
                
                if (originalVisibility) {
                    element.style.visibility = originalVisibility;
                } else {
                    element.style.visibility = '';
                }
                
                element.classList.remove('webagent-hidden');
                element.removeAttribute('data-original-display');
                element.removeAttribute('data-original-visibility');
                
                console.log(`WebAgent: Shown specific developer element: ${elementId}`);
                return true;
                
            } catch (e) {
                console.error(`WebAgent: Error showing developer element ${elementId}:`, e);
                return false;
            }
        } else {
            console.warn(`WebAgent: Developer element with ID '${elementId}' not found`);
            return false;
        }
    };
    
    console.log('WebAgent: Available utilities: webagentUtils.areDeveloperElementsVisible(), webagentUtils.getVisibleDeveloperElementsCount(), webagentUtils.getHiddenDeveloperElementsCount(), webagentUtils.showDeveloperElementById()');
    
    // Return the count of shown elements
    return shownCount;
    
})();