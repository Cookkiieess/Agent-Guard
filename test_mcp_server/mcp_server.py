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
    method = req.get("method")
    req_id = req.get("id")

    if method == "initialize":
        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "test-mcp-server", "version": "0.1.0"}
        }}

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [
            # TODO: fill in your tool schemas (name, description, inputSchema)
            {
                "name": "list_files",
                "description": "List files in a directory",
                "inputSchema": {
                    "type": "object",
                    "properties":{},
                    "required": []
                }
            },
            {
                "name": "read_file",
                "description": "Read a file's content in the scratch dir",
                "inputSchema": {
                    "type": "object",
                    "properties":{
                        "path":{
                            "type": "string",
                            "description": "Filename relative to the scratch directory"
                        }
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "delete_file",
                "description": "Delete a file",
                "inputSchema": {
                    "type": "object",
                    "properties":{
                        "path":{
                            "type": "string",
                            "description": "Filename relative to the scratch directory"
                        }
                    },
                    "required": ["path"]
                }
            }
        ]}}

    if method == "tools/call":
        name = req["params"]["name"]
        args = req["params"].get("arguments", {})
        # TODO: dispatch to list_files / read_file / delete_file
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
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        req = json.loads(line)
        resp = handle_request(req)
        send(resp)

if __name__ == "__main__":
    main()