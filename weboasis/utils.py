import re
from weboasis.agents.types import Message
from typing import List


def messages_to_list(messages: List[Message], name: str, mode: str = "openai"):
    """
    Converts a Messages object to a list of dictionaries, suitable for OpenAI API.
    The name argument is used to determine the assistant role of the messages. The messages with the same name will be assistant, others will be user.
    """
    if mode == "openai":
        messages_list = []
        for message in messages:

            if message.name == "system":
                role = "system"
            elif message.name == name:
                role = "assistant"
            else:
                role = "user"
            messages_list.append({"role": role, "name": message.name, "content": message.content})
        return messages_list
    else:
        raise ValueError(f"Invalid mode: {mode}")
    
    
def messages_to_str_without_image(messages: List[Message]):  
    '''
    Convert messages to a string, remove the image_url content.
    '''
    return [{"role": message["role"], "name": message["name"], "content": [ content if content["type"] != "image_url" else {"type":"image_url", "image_url": "[image]"} for content in message["content"]] } for message in messages]


def interactive_elems_to_str(interactive_elements, indent_char="\t"):
    """
    Formats interactive elements into lines that include:
    [test_id] type text="..." title="..." aria="..." href=...

    - Always shows test_id and type
    - text/title/aria-label/href are shown only if present and non-empty
    - Skips elements with include=False
    """

    def first_present(d, keys):
        for key in keys:
            val = d.get(key)
            if val is not None and val != "":
                return val
        return None

    lines = []
    for elem in interactive_elements:
        if not elem.get("include", True):
            continue

        test_id = elem.get("test_id")
        elem_type = first_present(elem, ["type", "tag"]) or "unknown"

        # Normalize text
        raw_text = first_present(elem, ["text"]) or ""
        text = raw_text.replace("\n", " ").strip()

        title = first_present(elem, ["title"]) or None
        aria = first_present(elem, ["ariaLabel", "aria-label", "aria_label"]) or None
        href = first_present(elem, ["href"]) or None

        parts = []
        # test_id and type first
        if test_id is not None:
            parts.append(f"test_id={test_id}")
        parts.append(f"tag={elem_type}")

        # Optional fields
        if text:
            parts.append(f"text={text!r}")
        if title:
            parts.append(f"title={title!r}")
        if aria:
            parts.append(f"aria={aria!r}")
        if href:
            parts.append(f"href={href}")

        lines.append(" ".join(parts))

    return "\n".join(lines)

def parse_thinking_action(text):
    """
    Parses a string with [User Experience], [Previous Action Analysis] and [Action] sections.
    Returns a dict with 'user_experience', 'previous_action_analysis' and 'action' keys.
    Sections can appear in any order and are all optional.
    """
    import re
    user_experience = ''
    previous_action_analysis = ''
    action = ''
    # Use non-greedy matching and lookahead to stop at the next section or end of string (including trailing whitespace)
    user_experience_match = re.search(
        r"\[User Experience\](.*?)(?=\[Previous Action Analysis\]|\[Action\]|$)", text, re.DOTALL)
    previous_action_analysis_match = re.search(
        r"\[Previous Action Analysis\](.*?)(?=\[User Experience\]|\[Action\]|$)", text, re.DOTALL)
    action_match = re.search(
        r"\[Action\](.*?)(?=\[User Experience\]|\[Previous Action Analysis\]|$)", text, re.DOTALL)
    if user_experience_match:
        user_experience = user_experience_match.group(1).strip()
    if previous_action_analysis_match:
        previous_action_analysis = previous_action_analysis_match.group(1).strip()
    if action_match:
        action = action_match.group(1).strip()
    return {'user_experience': user_experience, 'previous_action_analysis': previous_action_analysis, 'action': action}

# Example usage:
text = """
[Action] Click the right arrow button (>) to move forward to the next slide in the series and continue reviewing the slides for this section.
"""
result = parse_thinking_action(text)
print(result)
# Output: {'user_experience': 'I need to log in before I can proceed.', 'previous_action_analysis': 'I made a mistake in the previous action. I should use the correct action. I should try to correct them and use the correct action.', 'action': "fill('29', 'c3c4')"}
