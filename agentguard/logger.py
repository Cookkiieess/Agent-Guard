from datetime import datetime
import json

def log_decision(tool_call, label, action, file_path="audit.jsonl"):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tool_call": tool_call,
        "label": label,
        "action": action
    }
    with open(file_path, "a") as f:
        f.write(json.dumps(log_entry)+"\n")
