import ast
import pathlib
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from typing import Annotated
from pydantic import Field
from utils import BASE_DIR, check_path, read_text_file

mcp = MCPServer("mbpp")

@mcp.tool(
    name="find_references",
    description="Find all usages of a symbol in the codebase (function or class)."
)
def find_references(
    name: Annotated[
        str,
        Field(min_length=1, description="Name of the function or class symbol to find referencs for.")
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
    """Find and get all occurences of a given pattern in a codebase.

    Args:
        name: Name of the function or class symbol to find referencs for.
        filepath: Relative path of the file containing the sybol.
        line: 1-based line number of the symbol in filepath.

    Returns
        A fromated string of all the references

    Raises:
        ToolError if the 'name' is emtpy or if the line isn't possible.
    """
    target = name.strip()
    if not target:
        raise ToolError("'name' cannot be empty.")
    if line < 1:
        raise ToolError("'line' must be greater than or equal to 1.") 
    origin_file = check_path(filepath)
    origin_lines = read_text_file(origin_file, filepath).splitlines()
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
