from pathlib import Path
import subprocess
from typing import Annotated
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import Field
from utils import check_directory, run_subprocess

mcp = MCPServer("mbpp")
TIMEOUT_SECONDS = 60

"""===RUN_COMMAND==="""

@mcp.tool(
    name="run_command",
    description="Execute a shell command in the specified working directory and return stdout,
stderr, and exit code.",
)
def run_command(
    command: Annotated[
        str,
        Field(min_length=1, description="Shell command to execute."),
    ],
    workdir: Annotated[
        str,
        Field(description="Relative working directory inside the repository (use '.' for root).
"),
    ] = ".",
) -> str:
    """Execute a shell command inside 'workdir' within BASE_DIR.

    Args:
        command: Shell command to execute.
        workdir: Relative path to the working directory inside BASE_DIR.

    Return:
        Formatted output containing exit code, stdout, and stderr.

    Raises:
        ToolError: If inputs/workdir are invalid, execution times out, or an OS error occurs.
    """
    if not command.strip():
        raise ToolError("'command' cannot be empty.")
    target = check_directory(workdir)
    return run_subprocess(command, target, True)
