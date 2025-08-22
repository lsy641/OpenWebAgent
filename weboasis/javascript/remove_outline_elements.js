// remove_outline_elements.js
// Removes all highlight boxes and labels created by OUTLINE_INTERACTIVE_ELEMENTS_JS
(function() {
    document.querySelectorAll('.webagent-outline-box, .webagent-outline-label').forEach(el => el.remove());
})();
