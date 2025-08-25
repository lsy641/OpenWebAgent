// OUTLINE_INTERACTIVE_ELEMENTS_JS
(testIdAttr) => {
    if (!testIdAttr) return 0;
    // Remove any previous outlines
    // document.querySelectorAll('.webagent-outline-box, .webagent-outline-label').forEach(el => el.remove());

    // Elegant color palette
    const colors = [
        "#6C5B7B", "#355C7D", "#F67280", "#C06C84", "#F8B195",
        "#355C7D", "#99B898", "#FECEAB", "#FF847C", "#E84A5F"
    ];

    let highlightedCount = 0;
    const gap = 2; // distance between outline and label
    
    // ---------- helpers to compute live rects from DOM elements ----------
    function computeRectForElement(el) {
        try {
            const r = el.getBoundingClientRect();
            return { left: r.left, top: r.top, width: r.width, height: r.height };
        } catch {
            return null;
        }
    }

    const overlays = new Map(); // Element -> { outline, label, el }
    let rafPending = false;
    function updatePositions() {
        rafPending = false;
        overlays.forEach(({ outline, label, el }) => {
            const rect = computeRectForElement(el);
            if (!rect) return;
            // position: fixed uses viewport coords; do NOT add window.scrollX/Y
            outline.style.left = `${rect.left}px`;
            outline.style.top = `${rect.top}px`;
            outline.style.width = `${rect.width}px`;
            outline.style.height = `${rect.height}px`;
            // measure current label size to keep it outside the outline
            const labelRect = label.getBoundingClientRect();
            const top = Math.max(0, rect.top - labelRect.height - gap);
            const left = Math.min(
                Math.max(0, rect.left),
                window.innerWidth - labelRect.width - 8
            );
            label.style.left = `${left}px`;
            label.style.top = `${top}px`;
        });
    }
    function scheduleUpdate() {
        if (!rafPending) {
            rafPending = true;
            requestAnimationFrame(updatePositions);
        }
    }
    const elements = document.querySelectorAll('[webagent-interactive-elem]');
    elements.forEach((el, idx) => {
        const rect = computeRectForElement(el);
        if (!rect) return;
        const color = colors[idx % colors.length];

        // Create outline box
        const outline = document.createElement('div');
        outline.className = 'webagent-outline-box';
        outline.style.position = 'fixed';
        outline.style.left = `${rect.left}px`;
        outline.style.top = `${rect.top}px`;
        outline.style.width = `${rect.width}px`;
        outline.style.height = `${rect.height}px`;
        outline.style.border = `1.5px dashed ${color}`; // Thinner border
        outline.style.zIndex = 2147483647;
        outline.style.pointerEvents = 'none';
        outline.style.boxSizing = 'border-box';
        outline.style.borderRadius = '6px';
        outline.style.background = 'none';

        // Create label
        const label = document.createElement('div');
        label.className = 'webagent-outline-label';
        const testIdValue = el.getAttribute(testIdAttr) || '';
        label.innerText = testIdValue;
        label.style.position = 'fixed';
        label.style.padding = '1px 5px'; // Smaller padding
        label.style.background = color;
        label.style.color = '#fff';
        label.style.fontSize = '10px'; // Smaller font size
        label.style.fontFamily = 'monospace';
        label.style.borderRadius = '4px';
        label.style.zIndex = 2147483647;
        label.style.pointerEvents = 'none';
        label.style.boxShadow = '0 2px 6px rgba(0,0,0,0.08)';
        label.style.whiteSpace = 'nowrap';

        document.body.appendChild(outline);
        // Append hidden first to measure its size, then position outside the outline
        label.style.visibility = 'hidden';
        document.body.appendChild(label);
        const labelRect = label.getBoundingClientRect();
        const top = Math.max(0, rect.top - labelRect.height - gap);
        const left = Math.min(
            Math.max(0, rect.left),
            window.innerWidth - labelRect.width - 8
        );
        label.style.top = `${top}px`;
        label.style.left = `${left}px`;
        label.style.visibility = 'visible';
        overlays.set(el, { outline, label, el });

        highlightedCount++;
    });

    // Keep overlays synced on any scroll/resize (capture to catch inner scrollables)
    window.addEventListener('scroll', scheduleUpdate, true);
    document.addEventListener('scroll', scheduleUpdate, true);
    window.addEventListener('resize', scheduleUpdate, true);
    scheduleUpdate();

    return highlightedCount;
}