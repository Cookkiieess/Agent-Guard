import subprocess
import json
import sys
import time
import os
from .enforcer import enforce
from .logger import log_confirmation, log_decision
from .policy import load_policy
from .paths import response_path

print("PROXY PROCESS STARTED", file=sys.stderr)

def wait_for_confirmation(pending_id, timeout=60):
    start_time = time.time()
    while True:
        time.sleep(1)
        if os.path.exists(response_path()):
            with open(response_path(), "r", encoding="utf-8-sig") as f:
                read_response = json.loads(f.read())
                if read_response["id"] == pending_id:
                    return read_response["decision"]
                else:
                    continue

        if time.time() - start_time > timeout:
            return "block"

def run_proxy(server_command, config_path):

    policy_data = load_policy(config_path)

    process = subprocess.Popen(server_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    while True:
        print("WAITING FOR INPUT", file=sys.stderr, flush=True)
        ag_input = sys.stdin.readline()
        print(f"GOT RAW INPUT: {ag_input!r}", file=sys.stderr, flush=True)
        if not ag_input:
            break

        ag_input_stripped = ag_input.strip()

        try:
            json_input = json.loads(ag_input_stripped)
        except json.JSONDecodeError:
            print("Invalid JSON received. Skipping", file=sys.stderr)
            log_decision(ag_input, "invalid_json", "block")
            continue

        # Pass through protocol-level messages (handshake) without classification
        if json_input.get("method") != "tools/call":
            process.stdin.write(json.dumps(json_input) + "\n")
            process.stdin.flush()

            if "id" in json_input:
                response = process.stdout.readline()
                print(f"SENDING RESPONSE: {response!r}", file=sys.stderr, flush=True)
                sys.stdout.write(response)
                sys.stdout.flush()
            continue


        
        state = enforce(json_input, policy_data)

        if state[0] == "block":
            print("Action blocked by policy.", file=sys.stderr)
            log_decision(json_input, state[1], state[0])
            continue

        elif state[0] == "confirm":
            print("Action requires confirmation.", file=sys.stderr)
            next_id = log_confirmation(json_input, state[1], state[0])
            # give user a chance to confirm or deny the action if confirmed then log if not then long and deny.

            decision = wait_for_confirmation(next_id)
            print(decision, file=sys.stderr)
            if decision == "allow":
                log_decision(json_input, state[1], "allow")
                process.stdin.write(json.dumps(json_input) + "\n")
                process.stdin.flush()
                response = process.stdout.readline()
                sys.stdout.write(response)
                sys.stdout.flush()
            else:
                log_decision(json_input, state[1], "block")
                print("Action blocked by user decision.", file=sys.stderr)
                continue

        else:
            log_decision(json_input, state[1], state[0])
            process.stdin.write(json.dumps(json_input) + "\n")
            process.stdin.flush()
            response = process.stdout.readline()
            sys.stdout.write(response)
            sys.stdout.flush()
        

if __name__ == "__main__":
    run_proxy(["python3", "tests/fake_mcp_server.py"], "policy.example.yaml")