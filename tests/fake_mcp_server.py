from mcp.server.fastmcp import FastMCP

mcp = FastMCP("TestFS")

@mcp.tool()
def read_file(path: str) -> str:
    """Read a file's contents."""
    with open(path, "r") as f:
        return f.read()

@mcp.tool()
def list_directory(path: str) -> str:
    """List files in a directory."""
    import os
    return ", ".join(os.listdir(path))

if __name__ == "__main__":
    mcp.run()