import argparse
import json
import sys

from .proxy import run_proxy

def main():
    parser = argparse.ArgumentParser(description="AgentGuard CLI")
    subparsers = parser.add_subparsers(dest="command")

    start_parser = subparsers.add_parser("start")
    start_parser.add_argument("--config", default="policy.example.yaml", help="Path to the policy configuration file")
    start_parser.add_argument("--server", default="tests/fake_mcp_server.py", help="Path to the server script to run")

    confirm_parser = subparsers.add_parser("confirm")

    args = parser.parse_args()

    if args.command == "start":
        run_proxy([sys.executable, args.server], args.config)
    elif args.command == "confirm":
        confirm_command()
        

def confirm_command():

    # Write the decision to a file for the proxy to read
    with open("pending_confirmation.json", "r", encoding="utf-8-sig") as f:
        pending_confirmation = json.load(f)

    while True:
        human_response = input(f"Tool: {pending_confirmation['tool_call']['params']['name']}\nArgs: {pending_confirmation['tool_call']['params']['arguments']}\nLabel: {pending_confirmation['label']}\nallow/block?: ")

        if human_response.lower() not in ["allow", "block", "a","b"]:
            print("Invalid input. Please enter 'allow' or 'block'.")

        elif human_response.lower() in ["allow", "a"]:
            response_file = {
                    "id": pending_confirmation["id"],
                    "decision": "allow"
                }
            break
        else:
            response_file = {
                    "id": pending_confirmation["id"],
                    "decision": "block"
                }
            break

    with open("response.json", "w", encoding="utf-8-sig") as f:
        json.dump(response_file, f)

if __name__ == "__main__":
    main() # {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "list_directory", "arguments": {"path": "."}}}