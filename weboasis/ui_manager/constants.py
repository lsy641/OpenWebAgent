import yaml
import os

# Get the directory where this constants.py file is located
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the weboasis root directory
root_dir = os.path.dirname(current_dir)

TEXT_MAX_LENGTH = 2**32 - 1

TEST_ID_ATTRIBUTE = "data-testid"  # Playwright's default is "data-testid"


EXTRACT_OBS_MAX_TRIES = 5


js_path = os.path.join(root_dir, "javascript", "frame_mark_elements.js")
with open(js_path, "r", encoding="utf-8") as f:
    js_frame_mark_elements = f.read()
    
MARK_ELEMENTS_JS = js_frame_mark_elements

js_path = os.path.join(root_dir, "javascript", "add_outline_elements.js")
with open(js_path, "r", encoding="utf-8") as f:
    js_add_outline = f.read()
    
ADD_OUTLINE_ELEMENTS_JS = js_add_outline


js_path = os.path.join(root_dir, "javascript", "remove_outline_elements.js")
with open(js_path, "r", encoding="utf-8") as f:
    js_remove_outline = f.read()
    
REMOVE_OUTLINE_ELEMENTS_JS = js_remove_outline


js_path = os.path.join(root_dir, "javascript", "identify_interactive_elements.js")
with open(js_path, "r", encoding="utf-8") as f:
    js_identify_interactive_elements = f.read()
    
IDENTIFY_INTERACTIVE_ELEMENTS_JS = js_identify_interactive_elements


js_path = os.path.join(root_dir, "javascript", "show_decision_making_process.js")
with open(js_path, "r", encoding="utf-8") as f:
    js_show_decision_making_process = f.read()
    
SHOW_DECISION_MAKING_PROCESS_JS = js_show_decision_making_process


js_path = os.path.join(root_dir, "javascript", "create_developper_panel.js")
with open(js_path, "r", encoding="utf-8") as f:
    js_create_developper_panel = f.read()
    
INJECT_DEVELOPER_PANEL_JS = js_create_developper_panel

js_path = os.path.join(root_dir, "javascript", "hide_developer_elements.js")
with open(js_path, "r", encoding="utf-8") as f:
    js_hide_developer_elements = f.read()
    
HIDE_DEVELOPER_ELEMENTS_JS = js_hide_developer_elements

js_path = os.path.join(root_dir, "javascript", "show_developer_elements.js")
with open(js_path, "r", encoding="utf-8") as f:
    js_show_developer_elements = f.read()
    
SHOW_DEVELOPER_ELEMENTS_JS = js_show_developer_elements

# Accessibility tree extractor
js_path = os.path.join(root_dir, "javascript", "extract_accessbility_tree.js")
with open(js_path, "r", encoding="utf-8") as f:
    js_extract_accessibility_tree = f.read()
    
EXTRACT_ACCESSIBILITY_TREE_JS = js_extract_accessibility_tree