from upsonicai.server.tools.mcp_client import MCPToolManager



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
