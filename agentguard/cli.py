import argparse
from .proxy import run_proxy

def main():
    parser = argparse.ArgumentParser(description="AgentGuard CLI")
    parser.add_argument("--config", default="policy.example.yaml", help="Path to the policy configuration file")
    parser.add_argument("--server", default="tests/fake_mcp_server.py", help="Path to the server script to run")
    args = parser.parse_args()

    run_proxy(["python3", args.server], args.config)

if __name__ == "__main__":
    main() # {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "list_directory", "arguments": {"path": "."}}}