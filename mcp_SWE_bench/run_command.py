from pathlib import Path
import subprocess
from typing import Annotated
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import Field
from utils import check_directory

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
    try:
        completed = subprocess.run(
            command,
            cwd=target,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise ToolError(
            f"Command timed out after {TIMEOUT_SECONDS} seconds."
        ) from exc
    except OSError as exc:
        raise ToolError(f"Failed to execute command: {exc}") from exc
    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()
    parts = [f"Exit code: {completed.returncode}"]
    if stdout:
        parts.append(f"STDOUT:\n{stdout}")
    if stderr:
        parts.append(f"STDERR:\n{stderr}")
    if not stdout and not stderr:
        parts.append("(no output)")
    return "\n\n".join(parts)
