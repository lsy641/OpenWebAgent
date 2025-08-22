/**
 * Developer Wrapper Script - Simple Layout with Proper Fitting
 * 
 * This script fits the original page content within 80% container without stretching,
 * with the remaining space used for a developer panel.
 * 
 * Usage: Run this script after navigating to a URL to create a development environment.
 */

(function() {
    'use strict';
    
    // Wait for page to be stable before initializing
    function waitForPageStability() {
        if (document.readyState === 'complete' && 
            document.body && 
            !document.querySelector('#webagent-wrapper')) {
            setTimeout(initDeveloperWrapper, 1000);
        } else {
            setTimeout(waitForPageStability, 500);
        }
    }
    
    // Start waiting for page stability
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', waitForPageStability);
    } else {
        waitForPageStability();
    }
    
    function initDeveloperWrapper() {
        console.log('WebAgent: Initializing developer wrapper...');
        
        // Create wrapper container
        var wrapper = document.createElement('div');
        wrapper.id = 'webagent-wrapper';
        wrapper.style.cssText = 'position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1000; pointer-events: none;';
        
        // Create page container (80% of viewport)
        var pageContainer = document.createElement('div');
        pageContainer.id = 'webagent-page-container';
        pageContainer.style.cssText = 'position: absolute; top: 0; left: 0; width: 90%; height: 90%; overflow: auto; pointer-events: auto; background: white;';
        
        // Create inner content wrapper for fitting
        var contentWrapper = document.createElement('div');
        contentWrapper.id = 'webagent-content-wrapper';
        contentWrapper.style.cssText = 'position: relative; width: 100%; height: 100%; transform-origin: top left;';
        
        // Create developer panel (remaining space)
        var devPanel = document.createElement('div');
        devPanel.id = 'webagent-dev-panel';
        devPanel.style.cssText = 'position: absolute; top: 0; right: 0; width: 10%; height: 100%; background: #1e1e1e; color: white; overflow: auto; pointer-events: auto;';
        
        // Create bottom dev panel
        var bottomDevPanel = document.createElement('div');
        bottomDevPanel.id = 'webagent-bottom-dev-panel';
        bottomDevPanel.style.cssText = 'position: absolute; bottom: 0; left: 0; width: 100%; height: 10%; background: #2d2d2d; color: white; overflow: auto; pointer-events: auto;';
        
        // Move ALL body content to content wrapper
        moveAllBodyContent(contentWrapper);
        
        // Calculate and apply proper fitting (no stretching)
        applyProperFitting(contentWrapper, pageContainer);
        
        // Assemble the layout
        pageContainer.appendChild(contentWrapper);
        wrapper.appendChild(pageContainer);
        wrapper.appendChild(devPanel);
        wrapper.appendChild(bottomDevPanel);
        document.body.appendChild(wrapper);
        
        console.log('WebAgent: Developer wrapper initialized successfully');
    }
    
    function moveAllBodyContent(container) {
        // Get ALL elements in the document, not just direct children
        var allElements = document.querySelectorAll('*');
        var bodyChildren = Array.prototype.slice.call(document.body.children);
        var elementsToMove = [];
        
        console.log('WebAgent: Found ' + allElements.length + ' total elements in document');
        console.log('WebAgent: Found ' + bodyChildren.length + ' direct body children');
        
        // First, move all direct body children
        for (var i = 0; i < bodyChildren.length; i++) {
            var child = bodyChildren[i];
            if (child.id !== 'webagent-wrapper' && 
                child.tagName !== 'SCRIPT') {
                elementsToMove.push(child);
            }
        }
        
        // Move elements to content wrapper
        for (var j = 0; j < elementsToMove.length; j++) {
            container.appendChild(elementsToMove[j]);
        }
        
        // Now handle any remaining elements that might be outside normal flow
        handleRemainingElements(container);
        
        console.log('WebAgent: Moved ' + elementsToMove.length + ' elements to content wrapper');
    }
    
    function handleRemainingElements(container) {
        // Look for any elements that might still be in the original body
        var remainingElements = document.body.querySelectorAll('*');
        var movedElements = container.querySelectorAll('*');
        
        console.log('WebAgent: Remaining elements in body: ' + remainingElements.length);
        console.log('WebAgent: Elements in container: ' + movedElements.length);
        
        // If there are still elements in body, force move them
        if (remainingElements.length > 0) {
            var forceMoveElements = [];
            for (var i = 0; i < remainingElements.length; i++) {
                var elem = remainingElements[i];
                if (elem.id !== 'webagent-wrapper' && 
                    elem.tagName !== 'SCRIPT' &&
                    elem !== document.body) {
                    forceMoveElements.push(elem);
                }
            }
            
            for (var j = 0; j < forceMoveElements.length; j++) {
                try {
                    container.appendChild(forceMoveElements[j]);
                } catch (e) {
                    console.warn('WebAgent: Could not move element:', forceMoveElements[j], e);
                }
            }
            
            console.log('WebAgent: Force moved ' + forceMoveElements.length + ' additional elements');
        }
    }
    
    function applyProperFitting(contentWrapper, pageContainer) {
        // Wait a bit for content to settle, then calculate dimensions
        setTimeout(function() {
            // Get the actual content dimensions
            var contentRect = contentWrapper.getBoundingClientRect();
            var contentWidth = contentWrapper.scrollWidth;
            var contentHeight = contentWrapper.scrollHeight;
            
            // Get the container dimensions
            var containerWidth = pageContainer.offsetWidth;
            var containerHeight = pageContainer.offsetHeight;
            
            console.log('WebAgent: Content dimensions:', contentWidth, 'x', contentHeight);
            console.log('WebAgent: Container dimensions:', containerWidth, 'x', containerHeight);
            
            // Calculate the scale to fit content within container while preserving aspect ratio
            var scaleX = containerWidth / contentWidth;
            var scaleY = containerHeight / contentHeight;
            var scale = Math.min(scaleX, scaleY);
            
            console.log('WebAgent: Calculated scale factor:', scale);
            
            // Apply the scale transform
            contentWrapper.style.transform = 'scale(' + scale + ')';
            
            // Set the wrapper dimensions to maintain proper layout
            contentWrapper.style.width = contentWidth + 'px';
            contentWrapper.style.height = contentHeight + 'px';
            
            // Center the content within the container
            var scaledWidth = contentWidth * scale;
            var scaledHeight = contentHeight * scale;
            
            if (scaledWidth < containerWidth) {
                var extraWidth = containerWidth - scaledWidth;
                contentWrapper.style.left = (extraWidth / 2) + 'px';
            }
            
            if (scaledHeight < containerHeight) {
                var extraHeight = containerHeight - scaledHeight;
                contentWrapper.style.top = (extraHeight / 2) + 'px';
            }
            
            console.log('WebAgent: Applied proper fitting with scale:', scale);
            
            // Force a reflow to ensure everything is applied
            contentWrapper.offsetHeight;
            
        }, 1000);
    }
    
    // Add utility functions to the global scope
    window.webagentUtils = {
        // Get the developer panel (right side)
        getDevPanel: function() {
            return document.getElementById('webagent-dev-panel');
        },
        
        // Get the bottom developer panel
        getBottomDevPanel: function() {
            return document.getElementById('webagent-bottom-dev-panel');
        },
        
        // Get the page container
        getPageContainer: function() {
            return document.getElementById('webagent-page-container');
        },
        
        // Get the content wrapper
        getContentWrapper: function() {
            return document.getElementById('webagent-content-wrapper');
        },
        
        // Add content to right developer panel
        addToDevPanel: function(element) {
            var panel = this.getDevPanel();
            if (panel && element) {
                panel.appendChild(element);
                return true;
            }
            return false;
        },
        
        // Add content to bottom developer panel
        addToBottomDevPanel: function(element) {
            var panel = this.getBottomDevPanel();
            if (panel && element) {
                panel.appendChild(element);
                return true;
            }
            return false;
        },
        
        // Clear right developer panel
        clearDevPanel: function() {
            var panel = this.getDevPanel();
            if (panel) {
                panel.innerHTML = '';
                return true;
            }
            return false;
        },
        
        // Clear bottom developer panel
        clearBottomDevPanel: function() {
            var panel = this.getBottomDevPanel();
            if (panel) {
                panel.innerHTML = '';
                return true;
            }
            return false;
        },
        
        // Toggle the entire wrapper
        toggleWrapper: function() {
            var wrapper = document.getElementById('webagent-wrapper');
            if (wrapper) {
                if (wrapper.style.display === 'none') {
                    wrapper.style.display = 'block';
                } else {
                    wrapper.style.display = 'none';
                }
            }
        },
        
        // Refresh the content and recalculate fitting
        refreshContent: function() {
            var container = this.getPageContainer();
            var contentWrapper = this.getContentWrapper();
            if (container && contentWrapper) {
                handleRemainingElements(contentWrapper);
                applyProperFitting(contentWrapper, container);
                return true;
            }
            return false;
        },
        
        // Manually adjust the scale
        adjustScale: function(scale) {
            var contentWrapper = this.getContentWrapper();
            if (contentWrapper && scale > 0 && scale <= 1) {
                contentWrapper.style.transform = 'scale(' + scale + ')';
                console.log('WebAgent: Manually adjusted scale to:', scale);
                return true;
            }
            return false;
        }
    };
    
    console.log('WebAgent: Developer wrapper script loaded successfully');
    console.log('WebAgent: Available utilities: webagentUtils.getDevPanel(), webagentUtils.addToDevPanel(), webagentUtils.refreshContent(), webagentUtils.adjustScale()');
    
})();