import subprocess
import json
import sys
from .enforcer import enforce
from .logger import log_decision
from .policy import load_policy

def run_proxy(server_command, config_path):

    policy_data = load_policy(config_path)

    process = subprocess.Popen(server_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    while True:

        ag_input = sys.stdin.readline()
    
        if not ag_input:
            break

        ag_input_stripped = ag_input.strip()

        try:
            json_input = json.loads(ag_input_stripped)
        except json.JSONDecodeError:
            print("Invalid JSON received. Skipping")
            log_decision(ag_input, "invalid_json", "block")
            continue

        state = enforce(json_input, policy_data)

        if state[0] == "block":
            print("Action blocked by policy.")
            log_decision(json_input, state[1], state[0])
            continue
        else:
            log_decision(json_input, state[1], state[0])
            process.stdin.write(json.dumps(json_input) + "\n")
            process.stdin.flush()
            response = process.stdout.readline()
            print(response) #{"tool": "delete_file", "args": {"path": "x"}}, {"tool": "read_file", "args": {"path": "notes.txt"}}
        

if __name__ == "__main__":
    run_proxy(["python3", "tests/fake_mcp_server.py"], "policy.example.yaml")