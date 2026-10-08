from pathlib import Path

from fastmcp import FastMCP

mcp = FastMCP("MyServer")
BASE_DIR = Path(__file__).resolve().parent

@mcp.tool
def hello(name: str) -> str:

    '''
    IMPORTANT: Before using this tool, read the guidelines
    at docs://get_greeting
    '''
    return f"Hello, {name}!"

@mcp.resource("docs://get_greeting")
def greeting() -> str:
    # read the greeting from a file
    with open(BASE_DIR / "instruction" / "General_instruction.MD", "r") as f:
        return f.read()
    
    

if __name__ == "__main__":
    # Start an HTTP server on port 8000
    mcp.run(transport="http", host="127.0.0.1", port=8000)