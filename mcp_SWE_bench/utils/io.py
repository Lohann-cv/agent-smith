from pathlib import Path
import subprocess
import sys
from mcp.server.mcpserver.exceptions import ToolError

BASE_DIR = Path.cwd().resolve()

def check_path(filepath: str) -> Path:
    """Check if a path is a text file"""
    if not filepath.strip():
        raise ToolError("'filepath' cannot be empty.")
    target = (BASE_DIR / filepath).resolve()
    if target == BASE_DIR or BASE_DIR not in target.parents:
        raise ToolError("The targeted file cannot be outside the repository.")
    if not target.exists():
        raise ToolError(f"The file '{filepath}' dosn't exists.")
    if not target.is_file():
        raise ToolError(f"The given path '{filepath}' isn't a file.")
    return target


def read_text_file(target: Path, filepath: str) -> str:
    """Read a text file and return its content as a string."""
    try:
        return target.read_text(encoding="utf-8")
    except PermissionError as exc:
        raise ToolError(f"Cannot read the file '{filepath}', permission refused.") from exc
    except UnicodeDecodeError as exc:
        raise ToolError(f"Cannot convert the file '{filepath}' to UTF-8") from exc

def check_directory(directory: str) -> Path:
    """Resolve and validate a directory path inside BASE_DIRE."""
    if not directory.strip():
        raise ToolError("'directory' cannot be empty")
    target = (BASE_DIR / directory).resolve()
    if target != BASE_DIR and BASE_DIR not in target.parents:
        raise ToolError(
            f"Access denied: '{directory}' is outside the allowed repository."
        )
    if not target.exists():
        raise ToolError(f"Directory '{directory}' dosn't exist.")
    if not target.is_dir():
        raise ToolError(f"Path '{directory}' isn't a directory.")
    return target

def run_subprocess(args: list[str], directory: Path, shell_mod: bool) -> str:
    """TODO"""
    try:
        result = subprocess.run(
            args,
            cwd=directory,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT_SECOND,
            shell=shell_mod
        )
    except subprocess.TimeoutExpired as exc:
        raise ToolError(f"Execution failed: {exc}") from exc
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
    subpro_exit = [f"Exit code: {result.returncode}"]
    if stdout:
        subpro_exit.append(f"STDOUT:\n{stdout}")
    if stderr:
        subpro_exit.append(f"STDERR:\n{stderr}")
    if not stdout and not strerr:
        subpro_exit.append("(no output)")
    return "\n\n".join(subpro_exit)
