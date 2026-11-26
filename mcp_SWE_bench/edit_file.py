from pathlib import Path
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import Field
from typing import Annotated

mcp = MCPServer("mbpp")
BASE_DIR = Path.cwd().resolve()

"""===EDIT_FILE==="""

@mcp.tool(
    name="edit_file_content",
    description="Edit a file by replacing a string in the file content with a new string."
)
def edit_file(
    filepath: Annotated[str, Field(description="Relative path of the file to read.")],
    old_str: Annotated[
        str,
        Field(min_length=1, description="Exact non-empty string to replace."),
    ],
    new_str: Annotated[
        str,
        Field(description="Replacement string."),
    ]
) -> str:
    """Edit the content of a given file.

    Args:
        filepath: Relative path of the file to read.
        old_str: Exact non-empty string to replace.
        new_str: Replacement string.

    Return:
        A string stating the success of the opperation.

    Raises:
        ToolError if the 'filepath' isn't accessible or don't have the write/read right or if t
he 'old_str' is empty.
    """
    target = _check_path(filepath)
    if old_str == "":
        raise ToolError("You cannot replace an empty string")
    text = _read_text_file(target, filepath)
    occurrences = text.count(old_str)
    if occurrences < 1:
        raise ToolError(f"There is no occurrances of '{old_str}' in the file '{filepath}'.")
    if occurrences > 1:
        raise ToolError(f"There is multiple occurrances of '{old_str}' in the file '{filepath}'
, the old_str need to be more precice.")
    updated = text.replace(old_str, new_str, 1)
    try:
        target.write_text(updated, encoding="utf-8")
    except PermissionError as exc:
        raise ToolError(f"Cannot write to '{filepath}'.") from exc
    return f"'{filepath}' Successfully updated."


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
