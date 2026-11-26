from pathlib import Path
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
    cleaned = directory.strip()
    confirmed = cleaned if cleaned else "." # TODO move that line to refactor with check_workdir
    target = (BASE_DIR / confirmed).resolve()
    if target != BASE_DIR and BASE_DIR not in target.parents:
        raise ToolError(
            f"Access denied: '{directory}' is outside the allowed repository."
        )
    if not target.exists():
        raise ToolError(f"Directory '{directory}' dosn't exist.")
    if not target.is_dir():
        raise ToolError(f"Path '{directory}' isn't a directory.")
    return target
