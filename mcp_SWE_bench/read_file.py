from pathlib import Path
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from typing import Annotated
from pydantic import Field

mcp = MCPServer("mbpp")
BASE_DIR = Path.cwd().resolve()


"""===READ_FILE==="""

@mcp.tool(
    name="read_file_content",
    description="Read the content of a file and return it as a formated string."
)
def read_file(
    filepath: Annotated[str, Field(description="Relative path of the file to read.")],
    start_line: Annotated[
        int | None,
        Field(ge=1, description="Starting line number (inclusive)."),
    ] = None,
    end_line: Annotated[
        int | None,
        Field(ge=1, description="Ending line number (inclusive)."),
    ] = None
) -> str:
    """Read the content of a given file.

    Args:
        filepath: Relative path of the file to read.
        start_line: Starting line number (inclusive).
        end_line: Ending line number (inclusive).

    Return:
        A formated string with the line id followed by its content.

    Raises:
        ToolError if the 'filepath' isn't accessible or dosn't have the read right or if the 's
tart_line' and 'end_line' don't permit the file reading.
    """
    target = _check_path(filepath)
    start = start_line if start_line is not None else 1
    if end_line is not None and end_line < start:
        raise ToolError(
            f"'end_line' ({end_line}) cannot be less than 'start_line' ({start})."
        )
    text = _read_text_file(target, filepath).splitlines()
    total_lines = len(text)
    if total_lines == 0:
        return ""
    if start > total_lines:
        raise ToolError(
            f"'start_line' ({start}) cannot be above the number of lines of the file ({total_lines})."
        )
    end = min(end_line, total_lines) if end_line is not None else total_lines
    selected_lines = text[start - 1: end]
    return "\n".join(
        f"{ids}: {line}"
        for ids, line in enumerate(selected_lines, start)
    )


"""===UTILS==="""

def _check_path(filepath: str) -> Path:
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

def _read_text_file(target: Path, filepath: str) -> str:
    """Read a text file and return its content as a string."""
    try:
        return target.read_text(encoding="utf-8")
    except PermissionError as exc:
        raise ToolError(f"Cannot read the file '{filepath}', permission refused.") from exc
    except UnicodeDecodeError as exc:
        raise ToolError(f"Cannot convert the file '{filepath}' to UTF-8") from exc
