from pathlib import Path
import sys
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from utils import BASE_DIR, run_subprocess, TIMEOUT_SECONDS

mcp = MCPServer("mbpp")
SCRIPT_TO_RUN = BASE_DIR / "testbed.py"


@mcp.tool(
    name="run_tests",
    description="Execute the evaluation script."
)
def run_tests() -> str:
    """Execute the evaluation script inside BASE_DIR and return its output.

    Return:
        Formatted execution result including exit code, stdout and stderr.

    Raises:
        ToolError: If the script to run is missing, outside BASE_DIR or times out.
    """
    target = SCRIPT_TO_RUN.resolve()
    if target == BASE_DIR or BASE_DIR not in target.parents:
        raise ToolError("The script to run is outside the allowed repository.")
    if not target.exists() or not target.is_file():
        raise ToolError(f"The script to run '{target.name}' doesn't exist.")
    return run_subprocess([sys.executable, str(target)], BASE_DIR, False)
