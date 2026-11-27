from pathlib import Path
import re
from typing import Annotated
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import Field

mcp = MCPServer("mbpp")
BASE_DIR = Path.cwd().resolve()


@mcp.tool(
    name="search_code",
    description="Perform a grep-like regex search in the codebase matching a file pattern."
)
def search_code(
    pattern: Annotated[
        str,
        Field(min_length=1, description="Regex pattern to search for in file lines.")
    ],
    file_pattern: Annotated[
        str,
        Field(min_length=1, description="Glob pattern to filter target files."),
    ] = "*"
) -> str:
    """Search for a pattern across files matching 'file_pattern' inside BASE_DIR.

    Args:
        pattern: Regex pattern to search for in file lines.
        file_pattern: Glob pattern to filter target files.

    Return:
        A string listing all the occurrences with their path, line id and content.

    Raises:
        ToolError if the pattern is invalid.
    """
    if not pattern:
        raise ToolError("'pattern' cannot be empty.")
    if not file_pattern.strip():
        raise ToolError("'file_pattern' cannot be empty.")
    try:
        regex = re.compile(pattern)
    except re.error as exc:
        raise ToolError(f"Invalid regex pattern '{pattern}': {exc}") from exc
    files = BASE_DIR.rglob(file_pattern.strip())
    matches: list[str] = []
    for file in files:
        resolved = file.resolve()
        if BASE_DIR not in resolved.parents or not resolved.is_file():
            continue
        try:
            lines = resolved.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        str_path = resolved.as_posix()
        for line_id, line_content in enumerate(lines, start=1):
            if regex.search(line_content):
                matches.append(f"{str_path}:{line_id} {line_content}")
    if not matches:
        return f"No matches found for '{pattern}' with file pattern '{file_pattern}'."
    return "\n".join(matches)
