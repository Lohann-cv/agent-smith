import ast
from pathlib import Path
import re
from typing import Annotated
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import Field

mcp = MCPServer("mbpp")
BASE_DIR = Path.cwd().resolve()

"""===SEARCH_FUNCTION_OR_CLASS_DEFINITION_IN_CODE==="""

@mcp.tool(
    name="search_function_or_class_definition_in_code",
    description="Find the definition of a function or a class in codebase."
)
def search_function_or_class_definition_in_code(
    name: Annotated[
        str,
        Field(min_length=1, description="Name of the function or class to find.")
    ]
) -> str:
    """Find the definition of a function or a class in codebase.

    Args:
        name: Name of the function or class to find.

    Return:
        A string listing all the occurrences with their path, line id and content.

    Raises:
        ToolError if the name is empty.
    """
    target = name.strip()
    if not target:
        raise ToolError("'name' cannot be empty.")
    matches: list[str] = []
    for file in BASE_DIR.rglob("*.py"):
        resolved = file.resolve()
        if BASE_DIR not in resolved.parents or not resolved.is_file():
            continue
        try:
            text = resolved.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        try:
            tree = ast.parse(text, filename=resolved.as_posix())
        except SyntaxError:
            continue
        lines = text.splitlines()
        str_path = resolved.as_posix()
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if node.name == target:
                    line_id = node.lineno
                    line_content = lines[line_id - 1]
                    matches.append(f"{str_path}:{line_id} {line_content}")
    matches.sort()
    if not matches:
        return f"No definition found for '{target}'."
    return "\n".join(matches)
