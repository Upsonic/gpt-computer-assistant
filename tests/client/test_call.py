from upsonic import UpsonicClient
from pydantic import BaseModel


server = UpsonicClient("http://localhost:7541")


class Human(BaseModel):
    name: str
    surname: str
    gender: str


class City(BaseModel):
    name: str
    country: str
    population: int


class ToolList(BaseModel):
    tools: list[str]

def test_gpt4o_call():
    result = server.call(prompt="Hi, I am Onur Atakan ULUSOY and I am a male", response_format=Human)
    print(result)
    assert result.name.lower() == "onur atakan"
    assert result.surname.lower() == "ulusoy"
    assert result.gender.lower() == "male"


def test_gpt4o_call_without_return_type():
    result = server.call("Say hi to me")
    potential_keywords = ["hi", "hello", "hey"]
    assert any(keyword in result.lower() for keyword in potential_keywords)


def test_call_with_response_format():
    result = server.call(prompt="What is capital of Turkey?", response_format=City)
    print(result)
    assert result.name.lower() == "ankara"
    assert result.country.lower() == "turkey"
    assert result.population > 0


def test_call_with_tools():
    result = server.call(prompt="What are your tools?", tools=["add_numbers"])
    print(result)
    assert "add_numbers" in result


def test_call_with_mcp_server():
    result = server.call(prompt="What are your tools?", response_format=ToolList, tools=["add_numbers", "fetch"], mcp_servers=[{"command": "uvx", "args": ["mcp-server-fetch"]}])
    print(result)

    any_found_add_numbers = False
    any_found_fetch = False
    for tool in result.tools:
        if "add_numbers" in tool.lower():
            any_found_add_numbers = True
            
        if "fetch" in tool.lower():
            any_found_fetch = True
            

    print(any_found_add_numbers, any_found_fetch)
    assert any_found_add_numbers and any_found_fetch


def test_call_with_env_variable():
    result = server.call(prompt="What are your tools?", response_format=ToolList, tools=["add_numbers", "fetch"], mcp_servers=[{"command": "uvx", "args": ["mcp-server-fetch"], "env": {"test": "test"}}],)
    print(result)

    any_found_add_numbers = False
    any_found_fetch = False
    for tool in result.tools:
        if "add_numbers" in tool.lower():
            any_found_add_numbers = True
            
        if "fetch" in tool.lower():
            any_found_fetch = True
            

    print(any_found_add_numbers, any_found_fetch)
    assert any_found_add_numbers and any_found_fetch