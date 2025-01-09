import pytest
from fastapi.testclient import TestClient
from upsonic.tools_server.server.api import (
    app,
    timeout,
    timeout_handler,
    TimeoutException,
)
import asyncio
from httpx import AsyncClient

client = TestClient(app)


@pytest.mark.asyncio
async def test_timeout_handler():
    # Test successful completion within timeout
    async def quick_operation():
        return "success"

    result = await timeout_handler(1.0, quick_operation())
    assert result == "success"

    # Test timeout exception
    async def slow_operation():
        await asyncio.sleep(2)
        return "too late"

    with pytest.raises(TimeoutException):
        await timeout_handler(1.0, slow_operation())


@pytest.mark.asyncio
async def test_timeout_decorator():
    @timeout(1.0)
    async def test_endpoint():
        await asyncio.sleep(2)
        return {"message": "success"}

    # Test that the decorator raises HTTPException on timeout
    with pytest.raises(Exception) as exc_info:
        await test_endpoint()
    assert "408" in str(exc_info.value)

    # Test successful completion
    @timeout(2.0)
    async def quick_endpoint():
        return {"message": "success"}

    result = await quick_endpoint()
    assert result == {"message": "success"}


@pytest.mark.asyncio
async def test_list_tools():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/mcp/tools",
            json={"command": "uvx", "args": ["mcp-server-fetch"], "env": None},
        )
        assert response.status_code == 200

        response_data = response.json()
        tools = response_data["available_tools"]["tools"]

        # Find the fetch tool
        fetch_tool = next((tool for tool in tools if tool["name"] == "fetch"), None)
        assert fetch_tool is not None, "Fetch tool not found"

        # Check URL property structure
        url_schema = fetch_tool["inputSchema"]["properties"]["url"]
        assert url_schema["type"] == "string"
        assert url_schema["format"] == "uri"
        assert url_schema["minLength"] == 1


@pytest.mark.asyncio
async def test_call_tool():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/mcp/call_tool",
            json={
                "command": "uvx",
                "args": ["mcp-server-fetch"],
                "env": None,
                "tool_name": "fetch",
                "arguments": {"url": "http://localhost:8086/status"},
            },
        )
        assert response.status_code == 200

        response_data = response.json()
        result = response_data["result"]

        # Check response structure
        assert "_meta" in result
        assert result["_meta"] is None
        assert "content" in result
        assert isinstance(result["content"], list)
        assert len(result["content"]) > 0
        assert "isError" in result
        assert result["isError"] is False

        # Check content structure
        content = result["content"][0]
        assert "type" in content
        assert content["type"] == "text"
        assert "text" in content
        assert isinstance(content["text"], str)
        assert "Server is running" in content["text"]
