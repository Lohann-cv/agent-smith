from pydantic import Field
from mcp.server import MCPServer

MAXIMUM_ITERATIONS = 10
MAXIMUM_INPUT_TOKENS = 6000
MAXIMUM_OUTPUT_TOKENS = 1500
TIMEOUT = 120

mcp = MCPServer("mbpp")

@mcp.tool(
    name="run_test_on_code",
    description="Run a solution against the mbpp problemes."
)
def run_tests(code: str, test_list: list[str]) -> str:
    """Run a candidate solution against the given test assertions.

    Args:
        code: The python code to solve the tests.
        test_list: List of the assert statment to solve.

    Returns:
        JSON string: {"success": bool, "output": str}.
    """
