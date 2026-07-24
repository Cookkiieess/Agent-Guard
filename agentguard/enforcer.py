from .policy import get_action, load_policy
from .classifier import classify

def enforce(prompt, policy_data):
    class_prompt = classify(prompt)
    tool_action = get_action(policy_data, class_prompt)

    return tool_action, class_prompt
