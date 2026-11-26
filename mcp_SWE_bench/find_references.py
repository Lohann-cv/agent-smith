import ast
from pathlib import Path
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from typing import Annotated
from pydantic import Field

mcp = MCPServer("mbpp")
BASE_DIR = Path.cwd().resolve()

"""===FIND_REFERENCES==="""

@mcp.tool(
    name="find_references",
    description="Find all usages of a symbol in the codebase (function or class)."
)
def find_references(
    name: Annotated[
        str,
        Field(min_length=1, description="Name of the function or class symbol to find reference
s for.")
    ],
    filepath: Annotated[
        str,
        Field(min_length=1, description="Relative path of the file containing the symbol.")
    ],
    line: Annotated[
        int,
        Field(ge=1, description="1-based line number of the symbol in filepath.")
    ]
) -> str:
    """TODO"""
    target = name.strip()
    if not target:
        raise ToolError("'name' cannot be empty.")
    if line < 1:
        raise ToolError("'line' must be greater than or equal to 1.")
    origin_file = _check_path(filepath)
    origin_lines = _read_text_file(origin_file, filepath).splitlines()
    if not origin_lines or line > len(origin_lines):
        raise ToolError(
            f"'line' ({line}) is out of range for '{filepath}' (total lines: {len(origin_lines)
})."
        )
    seen: set[tuple[str, int]] = set()
    results: list[tuple[str, int, str]] = []
    for file in BASE_DIR.rglob("*.py"):
        resolved = file.resolve()
        if BASE_DIR not in resolved.parents or not resolved.is_file():
            continue
        try:
            text = resolved.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        try:
            tree = ast.parse(text, filename=resolved.as_posix())
        except SyntaxError:
            continue
        lines = text.splitlines()
        str_path = resolved.as_posix()
        for node in ast.walk(tree):
            is_ref = False
            if isinstance(node, ast.Name) and node.id == target:
                is_ref = True
            elif isinstance(node, ast.Attribute) and node.attr == target:
                is_ref = True
            if not is_ref:
                continue
            line_id = node.lineno
            key = (str_path, line_id)
            if key not in seen:
                seen.add(key)
                results.append((str_path, line_id, lines[line_id - 1]))
    results.sort(key=lambda item: (item[0], item[1]))
    if not results:
        return f"No references found for '{target}'."
    return "\n".join(f"{path}:{line_id} {content}" for path, line_id, content in results)

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
