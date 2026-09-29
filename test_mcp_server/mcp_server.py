import sys, json, os

def send(msg):
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()

def list_files(path="."):
    # List files in a directory.
    return ", ".join(os.listdir(path))

def delete_file(path):
    # Delete a file.
    if not path:
        raise ValueError("Missing 'path' argument")
    os.remove(path)
    return f"Deleted file: {path}"

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def handle_request(req):

    print("REQ OBJECT:", repr(req), file=sys.stderr)
    print("METHOD:", repr(req.get("method")), file=sys.stderr)
    print("ID:", repr(req.get("id")), file=sys.stderr)

    method = req.get("method")
    req_id = req.get("id")

    if "id" not in req:
        print(f"Notification received: {method}", file=sys.stderr)
        return None

    if method == "initialize":
        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "protocolVersion": "2025-11-25",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "test-mcp-server", "version": "0.1.0"}
        }}

    if method == "notifications/initialized":

        print("initialized successfully", file=sys.stderr)

        # Notifications do NOT receive responses
        return None
    

    if method == "tools/list":
        print("🔥 TOOLS/LIST RECEIVED", file=sys.stderr, flush=True)

        return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {
            "tools": [
                {
                    "name": "list_files",
                    "description": "List files in a directory.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                },
                {
                    "name": "read_file",
                    "description": "Read the contents of a file.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to the file."
                            }
                        },
                        "required": ["path"]
                    }
                },
                {
                    "name": "delete_file",
                    "description": "Delete a file.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to the file."
                            }
                        },
                        "required": ["path"]
                    }
                }
            ]
        }
    }

    if method == "tools/call":

        print("🔥 TOOL CALL RECEIVED", file=sys.stderr, flush=True)

        name = req["params"]["name"]
        args = req["params"].get("arguments", {})
        # TODO: dispatch to list_files / read_file / delete_file

        print(f"🔥 TOOL NAME: {name}", file=sys.stderr, flush=True)
        print(f"🔥 TOOL ARGS: {args}", file=sys.stderr, flush=True)

        DISPATCH = {
            "list_files": list_files,
            "read_file": read_file,
            "delete_file": delete_file
        }

        fn = DISPATCH.get(name)
        if not fn:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "method not found"}}

        try:
            result = fn(**args)
        except Exception as e:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32603, "message": str(e)}}

        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "content": [{"type": "text", "text": result}]
        }}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "method not found"}}

def main():

    print("MCP SERVER STARTED", file=sys.stderr)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:

            req = json.loads(line)
            resp = handle_request(req)
            if resp is not None:
                print("RESP OBJECT:", repr(resp), file=sys.stderr)
                send(resp)
        except Exception as e:
            print(f"Error processing request: {e}", file=sys.stderr)

            
if __name__ == "__main__":
    main()