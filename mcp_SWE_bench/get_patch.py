from pathlib import Path
import subprocess
from utils import BASE_DIR
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("mbpp")
TIMEOUT_SECONDS = 30

"""===GET_PATCH==="""

@mcp.tool(
    name="get_patch",
    description="Retrieve the unified git diff of all changes made to the repository.",
)
def get_patch() -> str:
    """Return the unified git diff of changes in BASE_DIR.

    Return:
        Unified diff string of all staged and unstaged changes, or a message if clean.

    Raises:
        ToolError: If git execution fails.
    """
    try:
        diff_proc = subprocess.run(
            ["git", "diff"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT_SECONDS,
            shell=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise ToolError(
            f"Git diff timed out after {TIMEOUT_SECONDS} seconds."
        ) from exc
    except OSError as exc:
        raise ToolError(f"Failed to execute git diff: {exc}") from exc
    if diff_proc.returncode != 0:
        raise ToolError(f"git diff failed: {diff_proc.stderr.strip()}")
    patch = diff_proc.stdout
    if not patch:
        return "No changes detected in repository."

    return patch
