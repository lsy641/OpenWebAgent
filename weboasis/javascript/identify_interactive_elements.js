(webagentIdAttribute) => {
    function isInteractive(element) {
        const tag = element.tagName.toLowerCase();
        const type = element.type ? element.type.toLowerCase() : null;
        
        // Primary interactive elements (highest priority)
        const primaryInteractiveTags = [
            'button', 'input', 'select', 'textarea', 'a', 'video', 'audio'
        ];
        
        // Secondary interactive elements (medium priority)
        const secondaryInteractiveTags = [
            'summary', 'details', 'dialog', 'option', 'img'
        ];
        
        // Container elements that might be interactive (lowest priority)
        const containerInteractiveTags = [
            'label', 'fieldset', 'datalist', 'output', 'menu'
        ];
        
        // Check if element has more specific interactive children
        function hasInteractiveChildren(element) {
            const interactiveChildren = element.querySelectorAll('button, input, select, textarea, a, video, audio');
            return interactiveChildren.length > 0;
        }
        
        // Primary interactive elements - always return true
        if (primaryInteractiveTags.includes(tag)) {
            return true;
        }
        
        // Secondary interactive elements - check if they're not just containers
        if (secondaryInteractiveTags.includes(tag)) {
            // If it has interactive children, it's probably just a container
            if (hasInteractiveChildren(element)) {
                return false;
            }
            return true;
        }
        
        // Container elements - only return true if they don't have interactive children
        if (containerInteractiveTags.includes(tag)) {
            // If label/fieldset has interactive children, don't mark it as interactive
            if (hasInteractiveChildren(element)) {
                return false;
            }
            return true;
        }
        
        // Other interactive checks
        if (element.hasAttribute('tabindex')) return true;
        if (element.getAttribute('contenteditable') === 'true') return true;
        if (typeof element.onclick === 'function') return true;
        if (element.getAttribute('onclick')) return true;
        if (window.getComputedStyle(element).cursor === 'pointer') {
            console.log('Pointer cursor detected:', element, element.className, element.id);
            return true;
        }
        if (typeof element.focus === 'function' && element.tabIndex >= 0) return true;
        
        return false;
    }

    function isElementNotOverlapped(element) {
        const rect = element.getBoundingClientRect();
        const test_id = element.getAttribute(webagentIdAttribute);
        
        // Test multiple points across the element to detect overlap
        const testPoints = [
            // Center point
            [rect.left + rect.width / 2, rect.top + rect.height / 2],
            // Corner points
            [rect.left + 5, rect.top + 5],
            [rect.right - 5, rect.top + 5],
            [rect.left + 5, rect.bottom - 5],
            [rect.right - 5, rect.bottom - 5],
            // Edge midpoints
            [rect.left + rect.width / 2, rect.top + 5],
            [rect.left + rect.width / 2, rect.bottom - 5],
            [rect.left + 5, rect.top + rect.height / 2],
            [rect.right - 5, rect.top + rect.height / 2]
        ];
        
        let visiblePoints = 0;
        const totalPoints = testPoints.length;
        
        for (const [x, y] of testPoints) {
            const elementAtPoint = document.elementFromPoint(x, y);
            
            // Check if our element is at this point or contains it
            if (elementAtPoint === element || 
                elementAtPoint?.closest(`[${webagentIdAttribute}="${test_id}"]`) === element) {
                visiblePoints++;
            }
        }
        
        // Element is considered visible if at least 50% of test points are accessible
        const visibilityRatio = visiblePoints / totalPoints;
        return visibilityRatio >= 0.8;
    }


    function isElementFullyVisible(element) {
        const rect = element.getBoundingClientRect();
        const style = window.getComputedStyle(element);
        
        // Check CSS properties that might hide the element
        if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') {
            return false;
        }
        
        // Check if element has zero dimensions
        if (rect.width === 0 || rect.height === 0) {
            return false;
        }
        
        // Check if element is outside viewport
        if (rect.right < 0 || rect.bottom < 0 || rect.left > window.innerWidth || rect.top > window.innerHeight) {
            return false;
        }
        
        // Check if element is disabled
        if (element.disabled || element.hasAttribute('disabled')) {
            return false;
        }
        
        // Check for disabled classes
        if (element.className && typeof element.className === 'string' && 
            element.className.includes('disabled')) {
            return false;
        }
        
        // Check for grayed out appearance
        if (style.opacity && parseFloat(style.opacity) < 0.5) {
            return false;
        }
        
        return true;
    }

    // Unmark any previously marked interactive elements (attribute-based)
    document.querySelectorAll('[webagent-interactive-elem]').forEach(el => el.removeAttribute('webagent-interactive-elem'));

    var vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
    var vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);

    var items = Array.prototype.slice
        .call(document.querySelectorAll("*"))
        .map(function (element) {
            var test_id = element.getAttribute(webagentIdAttribute) || "";
            if (element.hasAttribute('developer_elem')) {
                return null;
            }
            
            // Enhanced filtering: check interactivity, visibility, and overlap
            if (test_id === "" || 
                !isInteractive(element) || 
                !isElementFullyVisible(element) || 
                !isElementNotOverlapped(element)) {
                return null;
            }
            
            var rects = [...element.getClientRects()]
                .filter((bb) => {
                    var center_x = bb.left + bb.width / 2;
                    var center_y = bb.top + bb.height / 2;
                    var elAtCenter = document.elementFromPoint(center_x, center_y);
                    return elAtCenter === element || elAtCenter?.closest(`[${webagentIdAttribute}="${test_id}"]`) === element;
                })
                .map((bb) => {
                    const rect = {
                        left: Math.max(0, bb.left),
                        top: Math.max(0, bb.top),
                        right: Math.min(vw, bb.right),
                        bottom: Math.min(vh, bb.bottom),
                    };
                    return {
                        ...rect,
                        width: rect.right - rect.left,
                        height: rect.bottom - rect.top,
                    };
                });
            
            var area = rects.reduce((acc, rect) => acc + rect.width * rect.height, 0);
            return {
                include: true,
                area: area,
                rects: rects,
                text: element.textContent.trim().replace(/\\s{2,}/g, " "),
                type: element.tagName.toLowerCase(),
                ariaLabel: element.getAttribute("aria-label") || "",
                test_id: test_id,
                tag: element.tagName.toLowerCase(),
                id: element.id || null,
                class: typeof element.className === 'string' ? element.className : null,
                href: element.getAttribute("href") || null,
                title: element.getAttribute("title") || null
            };
        })
        .filter((item) => item !== null && item.area >= 10);
   

    // Robust containment filter
    items = items.filter((x) => {
        const xElem = document.querySelector(`[${webagentIdAttribute}="${x.test_id}"]`);
        if (!xElem) return false;
        return !items.some((y) => {
            if (x === y) return false;
            const yElem = document.querySelector(`[${webagentIdAttribute}="${y.test_id}"]`);
            if (!yElem) return false;
            return yElem !== xElem && yElem.contains(xElem);
        });
    });

    // Mark only the final filtered elements
    items.forEach((x) => {
        try {
            const el = document.querySelector(`[${webagentIdAttribute}="${x.test_id}"]`);
            if (el) el.setAttribute('webagent-interactive-elem', '');
        } catch (e) {}
    });

    return items;
}