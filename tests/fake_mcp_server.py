import json
import sys


while True:
    line = sys.stdin.readline()

    if not line:
        break

    line_stripped = line.strip()

    try:
        request = json.loads(line_stripped)
    except json.JSONDecodeError:
        print("Invalid JSON received. Skipping")
        continue
    
    req_id = request["id"]
    req_method = request["method"]
    req_params_name = request["params"]["name"]
    req_params_arg = request["params"]["arguments"]

    if req_params_name == "read_file":
        result_text = "fake file contents here"
    elif req_params_name == "list_directory":
        result_text = "file1.txt, file2.txt, notes.txt"
    else:
        result_text = f"fake result for unknown tool: {req_params_name}"

    response = {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": result_text}]}}

    print(json.dumps(response))
    sys.stdout.flush()
