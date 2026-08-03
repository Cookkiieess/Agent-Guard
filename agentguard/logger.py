from datetime import datetime
import json

next_id = 0

def log_decision(tool_call, label, action, file_path="audit.jsonl"):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tool_call": tool_call,
        "label": label,
        "action": action
    }
    with open(file_path, "a") as f:
        f.write(json.dumps(log_entry)+"\n")


def log_confirmation(tool_call, label, action, file_path="pending_confirmation.json"):
    global next_id
    next_id += 1
    log_entry = {
        "id": next_id,
        "tool_call": tool_call,
        "label": label,
        "action": action
    }
    with open(file_path, "w") as f:
        f.write(json.dumps(log_entry))

    return next_id