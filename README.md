# AgentGuard

A policy enforcement proxy for MCP-based AI agents. AgentGuard sits between an AI agent and the tools it can call, intercepting every tool call, classifying its risk, and enforcing a policy before anything is allowed to execute.

## Why

AI agents connected via MCP (Model Context Protocol) can take real actions — reading and writing files, running shell commands, hitting APIs. Without a policy layer in front of that, a prompt injection or a bad model decision can turn into a destructive action with nothing standing in the way. AgentGuard is that layer.

## How it works

```
Agent (e.g. Claude Desktop)  →  AgentGuard  →  Real MCP Server
```

AgentGuard poses as the MCP server from the agent's side, and as the MCP client from the real server's side. Protocol-level messages (the `initialize` handshake and `notifications/initialized`) pass through untouched. Every `tools/call` request goes through three stages before it's forwarded or rejected:

1. **Classify** — the tool call is scored as `safe`, `dangerous`, or `suspicious` based on the tool name and its arguments.
2. **Enforce** — a policy file maps each risk label to an action: `allow`, `block`, or `confirm`.
3. **Log** — every decision, regardless of outcome, is written to an audit trail.

Blocked calls never reach the real MCP server. Allowed calls are forwarded transparently, and the response is passed back to the agent as if AgentGuard weren't there. Calls mapped to `confirm` pause and wait for a human decision (see below).

Tested end-to-end against a server built on the official MCP Python SDK — real protocol handshake, real spec-compliant responses.

## Installation

```bash
git clone https://github.com/Cookkiieess/Agent-Guard.git
cd Agent-Guard
pip install -e .
```

This registers `agentguard` as a command-line tool.

## Usage

```bash
agentguard start --config policy.example.yaml --server path/to/mcp_server.py
```

- `--config` — path to your policy YAML file
- `--server` — path to the MCP server script AgentGuard should spawn and guard

## Human-in-the-loop confirmation

Some tool calls aren't clearly safe or dangerous — an unrecognized tool, for instance. Policies can map these to `confirm` instead of an automatic allow/block. When this happens:

1. AgentGuard writes the pending call's details (tool, arguments, risk label) to `pending_confirmation.json` and pauses, polling for a response.
2. In a separate terminal, run:
   ```bash
   agentguard confirm
   ```
   This shows what's pending and prompts for `allow` or `block`.
3. AgentGuard picks up the decision within about a second and proceeds accordingly.

If nobody responds within the timeout (60 seconds by default), the call fails closed — it's automatically blocked.

**Known limitation:** only one confirmation is handled at a time; the proxy pauses entirely while waiting on it. Concurrent confirmation handling is planned for a future version.

## Policy configuration

Policies are defined in a simple YAML file:

```yaml
default: block
safe: allow
suspicious: confirm
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
├── logger.py          # audit trail + pending confirmation tracking
├── proxy.py            # the stdio interception loop, incl. confirm wait/poll
└── cli.py                # command-line entry point (`start`, `confirm`)
```

## Status

v2 — real MCP protocol compliance (verified against the official Python SDK) and human-in-the-loop confirmation for ambiguous tool calls, alongside v1's rule-based classification and allow/block enforcement.

Planned next (v3): concurrent confirmation handling with a real pending queue, per-tool policy overrides, and hardening against bypass attempts (fail-closed exception handling, process/privilege isolation, protection against obfuscated tool-name matching).

## License

MIT
