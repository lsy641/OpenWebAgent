import yaml
import os

# Get the directory where this constants.py file is located
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the weboasis root directory
root_dir = os.path.dirname(current_dir)

# Default prompts file path
default_prompts_path = os.path.join(root_dir, "config", "prompts.yaml")

# Allow user to override prompts file via environment variable
user_prompts_path = os.getenv("WEBOASIS_PROMPTS_PATH")

# Use user's prompts file if provided, otherwise fall back to default
prompts_file_path = user_prompts_path if user_prompts_path else default_prompts_path

try:
    with open(prompts_file_path, "r") as f:
        prompts = yaml.safe_load(f)
    print(f"Loaded prompts from: {prompts_file_path}")
except FileNotFoundError:
    if user_prompts_path:
        print(f"Warning: User prompts file not found: {user_prompts_path}")
        print("Falling back to default prompts")
    # Fall back to default if user file doesn't exist
    try:
        with open(default_prompts_path, "r") as f:
            prompts = yaml.safe_load(f)
    except FileNotFoundError:
        # If even default doesn't exist (e.g., in packaged version), use fallback prompts
        print("Warning: Default prompts file not found, using fallback prompts")
        prompts = {
            "observe_prompt": "# Interactive Elements\n\n${interactive_elements_str}\n\n# Screenshot\nThe image provided is a screenshot of the current application state.\n\n# Response Format\nProvide your response in the following format:\n\n[User Experience] (A short description of your current feelings and experience when interacting with the web application. Skip if not applicable.)\n[Previous Action Analysis] (Briefly reflect on your last action—was it helpful or a mistake? Skip if not needed.)\n[Action] (The next action you plan to do)",
            "act_prompt": "# Interactive elements:\n\n${interactive_elements_str}\n\n# Action Space\n\n${action_space_desc}\n\n# Goal:\n${goal}\n\n# Response Format\nReturn ONLY the action function call without any additional text.",
            "intention_parse_prompt": "# Instructions\nReview the current state of the page and all other information to find the best possible next action to accomplish your goal.\n\nProvide ONLY ONE action. Do not suggest multiple actions or a sequence of actions.\n# Goal:\n${goal}",
            "example_profile2_to_web": "You are a web user. Clearly articulate your current task to the web agent."
        }

# Load prompts from the file (either user's custom or default)
WEBAGENT_OBSERVE_PROMPT = prompts.get("observe_prompt", "")

WEBAGENT_INTENTION_PARSE_PROMPT = prompts.get("intention_parse_prompt", "")

WEBAGENT_ACT_PROMPT = prompts.get("act_prompt", "")

WEBAGENT_EXAMPLE_PROFILE = prompts.get("example_profile", "")


TEXT_MAX_LENGTH = 2**32 - 1

TEST_ID_ATTRIBUTE = "web-testid"  # Playwright's default is "data-testid"


EXTRACT_OBS_MAX_TRIES = 5


