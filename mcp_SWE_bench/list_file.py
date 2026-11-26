from pathlib import Path
from typing import Annotated
from utils import check_directory, BASE_DIR
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import Field

mcp = MCPServer("mbpp")
BASE_DIR = Path.cwd().resolve()
MAX_RESULTS = 200

"""===LIST_FILES==="""

@mcp.tool(
    name="list_files",
    description="List files in a directory matching a given pattern.",
)
def list_files(
    directory: Annotated[
        str,
        Field(description="Relative directory path inside the repository ('.' for root)."),
    ] = ".",
    pattern: Annotated[
        str,
        Field(min_length=1, description="Glob pattern to match files (e.g. '*.py' or '**/*.py').")
    ] = "*",
) -> str:
    """List files that match a patern in a given directory.

    Args:
        directory: Relative directory path inside the repository ('.' for root).
        pattern: Glob pattern to match files (e.g. '*.py' or '**/*.py').

    Return:
        A string listing all the files matching the pattern.

    Raises:
        ToolError if the pattern is invalid
    """
    if not pattern.strip():
        raise ToolError("The pattern cannot be empty.")
    target = check_directory(directory)
    try:
        matches = target.rglob(pattern.strip())
    except ValueError as exc:
        raise ToolError(f"Invalid pattern '{pattern}': {exc}") from exc
    except PermissionError as exc:
        raise ToolError(f"Permission denied while lising '{directory}'.") from exc
    files: list[str] = []
    for entry in matches:
        resolved_entry = entry.resolve()
        if BASE_DIR not in resolved_entry.parents:
            continue
        if resolved_entry.is_file():
            files.append(resolved_entry.relative_to(BASE_DIR).as_posix())
    files.sort()
    if not files:
        return f"No files matching '{pattern}' found in '{directory}'."
    truncated = len(files) > MAX_RESULTS  # May not mandatory with bench
    shown = files[:MAX_RESULTS]
    output = "\n".join(shown)
    if truncated:
        output += f"\n... (showing first {MAX_RESULTS} of {len(files)} files)"
    return output
