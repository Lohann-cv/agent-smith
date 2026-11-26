from pathlib import Path
import sys
import subprocess
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("mbpp")
BASE_DIR = Path.cwd().resolve()
SCRIPT_TO_RUN = BASE_DIR / #TODO put the asked path of the subject
TIMEOUT_SECONDS = #TODO but the asked timeout

"""===RUN_TESTS==="""

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
    try:
        completed = subprocess.run(
            [sys.executable, str(target)],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT_SECONDS,
            shell=False
        )
    except subprocess.TimeoutExpired as exc:
        raise ToolError(f"Evaluation script timed out after {TIMEOUT_SECONDS} seconds.") from e
xc
    except OSError as exc:
        raise ToolError(f"Failed to execute the script: {exc}") from exc
    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()
    complet_exit = [f"Exit code: {completed.returncode}"]
    if stdout:
        complet_exit.append(f"STDOUT:\n{stdout}")
    if stderr:
        complet_exit.append(f"STDERR:\n{stderr}")
    if not stdout and not stderr:
        complet_exit.append("(no output)")  # For script that only write, ill check if it's usefull in the bench erepo
    return "\n\n".join(complet_exit)
