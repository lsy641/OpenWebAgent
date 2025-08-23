import logging
from weboasis.act_book import ActBookController
from weboasis.agents import DualAgent
from weboasis.agents.constants import TEST_ID_ATTRIBUTE
from openai import OpenAI
import os

logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

# Suppress OpenAI debug logs while keeping our debug logs
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Create controller for operation management
act_book = ActBookController(auto_register=False, log_level="DEBUG")
# register the operations for the web agent to execute, see /act_book/README.md for more details
act_book.register("browser/interaction")
act_book.register("browser/navigation")
act_book.register("general/flow")


# Print available operations from our act_book
available_operations = act_book.list_operations()
logger.info(f"Available operations: {available_operations}")

# Get operations summary
summary = act_book.get_operations_summary()
logger.info(f"Operations summary: {summary}")


   
# Initialize the openai client and the model
api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=api_key, base_url="https://api.openai.com/v1")
model = "gpt-4.1-mini"


'''
Usually, the first sevral steps are hard-coded, such as go to the target page, login, etc. You can hard-code the goals for the first several steps.
Hard-coded goals for the first several steps, separated by [STEP]
For example, "[STEP]go to https://... [STEP]type password 1234 if requiring login[STEP]click submit button"
'''
def build_hard_coded_goal(step_goals_text: str):
    # Split and strip, ignore empty
    goals = [g.strip() for g in step_goals_text.split('[STEP]') if g.strip()]
    logger.info(f"intial goals: {goals}")
    def hard_coded_goal(step_idx):
        if 0 <= step_idx < len(goals):
            return goals[step_idx]
        return ""
    return hard_coded_goal

hard_coded_goal = build_hard_coded_goal("[STEP]go to https://www.saucedemo.com/[STEP] login(username=“standard_user”，password=“secret_sauce”)")

# Run the dual agent to test the web application, set verbose to True to visualize the decision making process
dual_agent = DualAgent(client=openai_client, model=model, act_book=act_book, web_manager="palywright", test_id_attribute=TEST_ID_ATTRIBUTE, log_dir="./logs/demo", hard_coded_goal=hard_coded_goal, verbose=True)
# allow the user to pause the execution for debugging
dual_agent.web_manager.pause_for_debug()
iterations = 300

for i in range(iterations):
    if not dual_agent.web_manager.is_browser_available():
        logger.error(f"Browser is not available, exiting...")
        break
    dual_agent.step()
    # detect if the user wants to pause the execution for debugging
    dual_agent.web_manager.pause_for_debug()
    
    





