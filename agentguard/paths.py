import os
from pathlib import Path

def base_dir():
    d = Path(os.environ.get("AGENTGUARD_HOME", Path.home() / ".agentguard"))
    d.mkdir(parents=True, exist_ok=True)
    return d

def pending_path():
    return base_dir() / "pending_confirmation.json"

def response_path():
    return base_dir() / "response.json"

def audit_path():
    return base_dir() / "audit.jsonl"