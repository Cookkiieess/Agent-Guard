# AgentGuard

A policy enforcement proxy for MCP-based AI agents. AgentGuard sits between an AI agent and the tools it can call, intercepting every tool call, classifying its risk, and enforcing a policy before anything is allowed to execute.

## Why

AI agents connected via MCP (Model Context Protocol) can take real actions — reading and writing files, running shell commands, hitting APIs. Without a policy layer in front of that, a prompt injection or a bad model decision can turn into a destructive action with nothing standing in the way. AgentGuard is that layer.

## How it works

```
Agent (e.g. Claude Desktop)  →  AgentGuard  →  Real MCP Server
```

AgentGuard poses as the MCP server from the agent's side, and as the MCP client from the real server's side. Every JSON-RPC tool call passes through three stages before it's forwarded or rejected:

1. **Classify** — the tool call is scored as `safe`, `dangerous`, or `suspicious` based on the tool name and its arguments.
2. **Enforce** — a policy file maps each risk label to an action: `allow` or `block`.
3. **Log** — every decision, regardless of outcome, is written to an audit trail.

Blocked calls never reach the real MCP server. Allowed calls are forwarded transparently, and the response is passed back to the agent as if AgentGuard weren't there.

## Installation

```bash
git clone https://github.com/Cookkiieess/agentguard.git
cd agentguard
pip install -e .
```

This registers `agentguard` as a command-line tool.

## Usage

```bash
agentguard --config policy.example.yaml --server path/to/mcp_server.py
```

- `--config` — path to your policy YAML file
- `--server` — path to the MCP server script AgentGuard should spawn and guard

## Policy configuration

Policies are defined in a simple YAML file:

```yaml
default: block
safe: allow
suspicious: allow
dangerous: block
```

`default` is the fallback action for any risk label not explicitly listed — kept as `block` by default so the system fails closed rather than open.

## Classification

Tool calls are checked against two tiers:

- **Always-dangerous tools** — actions that are inherently risky regardless of arguments (`run_command`, `delete_file`, `send_email`, `ssh`, and others).
- **Conditional tools** — read/inspection actions (`read_file`, `list_directory`, `git_log`) that are only flagged dangerous if their arguments touch sensitive paths or keywords (`.env`, `.ssh`, `credentials`, `private_key`, and others).

Any tool name not recognized in either list is labeled `suspicious` rather than assumed safe.

## Audit log

Every decision is appended to a JSONL audit file — one JSON object per line, containing the tool call, the classification label, the enforcement action, and a timestamp.

## Project structure

```
agentguard/
├── classifier.py   # risk classification
├── policy.py        # policy loading and lookup
├── enforcer.py       # ties classification + policy into a decision
├── logger.py          # audit trail
├── proxy.py            # the stdio interception loop
└── cli.py                # command-line entry point
```

## Status

This is v1 — a working, protocol-compliant policy enforcement proxy over stdio transport, with rule-based classification and allow/block enforcement. Planned next: per-tool policy overrides, human-in-the-loop confirmation for ambiguous calls, and hardening against bypass attempts.

## License

MIT