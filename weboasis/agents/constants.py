import yaml
import os

# Get the directory where this constants.py file is located
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the weboasis root directory
root_dir = os.path.dirname(current_dir)

with open(os.path.join(root_dir, "config", "prompts.yaml"), "r") as f:
    prompts = yaml.safe_load(f)
    

WEBAGENT_OBSERVE_PROMPT = prompts["observe_prompt"]

WEBAGENT_INTENTION_PARSE_PROMPT = prompts["intention_parse_prompt"]

WEBAGENT_ACT_PROMPT = prompts["act_prompt"]

WEBAGENT_EXAMPLE_PROFILE = prompts["example_profile2_to_web"]


TEXT_MAX_LENGTH = 2**32 - 1

TEST_ID_ATTRIBUTE = "web-testid"  # Playwright's default is "data-testid"


EXTRACT_OBS_MAX_TRIES = 5


