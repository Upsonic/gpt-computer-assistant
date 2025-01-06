from upsonicai.server.tools.mcp_client import MCPToolManager


def test_mcp_client_basic():
    # Initialize the client
    client = MCPToolManager(command="uvx", args=["mcp-server-fetch"])

    # Get list of tools
    tool_list = client.tools()

    # Check if we got any tools
    assert len(tool_list) > 0

    # Test the first tool (fetch)
    first_tool = tool_list[0]

    # Check tool attributes
    assert hasattr(first_tool, "__name__")
    assert hasattr(first_tool, "__doc__")
    assert hasattr(first_tool, "__annotations__")

    # Test tool execution
    result = first_tool(url="https://google.com")
    assert isinstance(result, dict)
    assert "result" in result


def test_get_tools_by_name():
    client = MCPToolManager(command="uvx", args=["mcp-server-fetch"])

    # Get specific tools by name
    tools = client.get_tools_by_name(["fetch"])

    # Check if we got the tool
    assert len(tools) == 1
    assert tools[0].__name__ == "fetch"

    # Test the tool
    result = tools[0](url="https://google.com")
    assert isinstance(result, dict)
    assert "result" in result
    assert not result["result"].get("isError", True)


def test_direct_tool_call():
    client = MCPToolManager(command="uvx", args=["mcp-server-fetch"])

    # Test direct tool call
    result = client.call_tool("fetch", {"url": "https://google.com"})
    assert isinstance(result, dict)
    assert "result" in result
    assert not result["result"].get("isError", True)


def test_with_context_manager():
    with MCPToolManager(command="uvx", args=["mcp-server-fetch"]) as client:
        # Get list of tools
        tool_list = client.tools()

        # Check if we got any tools
        assert len(tool_list) > 0

        # Test the fetch tool
        fetch_tool = tool_list[0]
        result = fetch_tool(url="https://google.com")

        assert isinstance(result, dict)
        assert "result" in result
        assert not result["result"].get("isError", True)
