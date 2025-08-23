// Extract simplified accessibility-like tree (compact and bounded)
// Usage (testIdAttr is REQUIRED):
// page.evaluate(EXTRACT_ACCESSIBILITY_TREE_JS, {
//   maxDepth: 3, maxTextLen: 80, onlyViewport: true, maxNodes: 300, testIdAttr: 'web-testid'
// })
(options) => {
    const cfg = Object.assign({ maxDepth: 3, maxTextLen: 80, maxNodes: 300, testIdAttr: null }, options || {});
    const testIdAttr = cfg.testIdAttr && String(cfg.testIdAttr);
    if (!testIdAttr) {
        throw new Error('extract_accessbility_tree: "testIdAttr" option is required');
    }

    // Interactive marking is handled elsewhere (identify_interactive_elements.js)
    // Detect interactive elements via attribute set by identify_interactive_elements.js
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
        if (element.hasAttribute('developer_elem')) {
            return false;
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
        const test_id = element.getAttribute(testIdAttr);
        
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
                elementAtPoint?.closest(`[${testIdAttr}="${test_id}"]`) === element) {
                visiblePoints++;
            }
        }
        
        // Element is considered visible if at least 80% of test points are accessible
        const visibilityRatio = visiblePoints / totalPoints;
        return visibilityRatio >= 0.8;
    }

    const inViewport = (el) => {
        try {
            const r = el.getBoundingClientRect();
            const vw = window.innerWidth || document.documentElement.clientWidth;
            const vh = window.innerHeight || document.documentElement.clientHeight;
            // Consider partially visible
            return r.bottom > 0 && r.right > 0 && r.top < vh && r.left < vw;
        } catch { return true; }
    };

    const trimText = (t) => {
        if (!t) return "";
        const s = (t || "").replace(/\s+/g, " ").trim();
        return s.length > cfg.maxTextLen ? s.slice(0, cfg.maxTextLen) + "…" : s;
    };

    const tree = [];
    let nodeCount = 0;
    let preorderIndex = 0; // position in preorder traversal

    const walk = (node, depth, path) => {
        if (!node || depth > cfg.maxDepth || nodeCount >= cfg.maxNodes) return;
        if (!(node instanceof Element)) {
            // Skip non-element nodes
            Array.from(node.childNodes || []).forEach((c) => walk(c, depth, path));
            return;
        }

        const role = node.getAttribute("role") || node.tagName.toLowerCase();
        const hasAriaAttribute = Array.from(node.attributes).some(attr => attr.name.startsWith('aria-'));
        const text = trimText(node.textContent || "");
        const interactive = isInteractive(node);
        const notOverlapped = isElementNotOverlapped(node);
        const id = node.id || "";
        const testId = node.getAttribute(testIdAttr) || "";
        const elementInViewport = inViewport(node);
        const developerElem = node.hasAttribute('developer_elem');
        // Only add elements that are interactive or have text content
        if ((interactive || text) && !developerElem) {
            // Minimal box info for spatial grounding (viewport coords)
            let rect = null;
            try {
                const r = node.getBoundingClientRect();
                rect = { left: Math.round(r.left), top: Math.round(r.top), width: Math.round(r.width), height: Math.round(r.height) };
            } catch { rect = null; }

            const entry = {
                role,
                textContent: text,
                inViewport: elementInViewport,
                rect,
                notOverlapped,
                depth,
                preorderIndex: preorderIndex++,
                path: path.length ? path.join('.') : '0'
            };
            // Use dynamic key for test id attribute
            entry["test_id"] = testId || undefined;
            tree.push(entry);
            nodeCount += 1;
        }

        Array.from(node.children).forEach((c, i) => walk(c, depth + 1, path.concat(i)));
    };

    walk(document.body, 0, []);
    return tree.slice(0, cfg.maxNodes);
}