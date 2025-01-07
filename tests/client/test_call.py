from upsonicai import UpsonicServer
from pydantic import BaseModel


server = UpsonicServer("http://localhost:8087")


class Human(BaseModel):
    name: str
    surname: str
    gender: str


class City(BaseModel):
    name: str
    country: str
    population: int


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
    result = server.call(prompt="What are your tools?", tools=["add_numbers", "fetch"], mcp_servers=[{"command": "uvx", "args": ["mcp-server-fetch"]}])
    print(result)
    assert "add_numbers" in result and "fetch" in result


def test_call_with_env_variable():
    result = server.call(prompt="What are your tools?", tools=["add_numbers", "fetch"], mcp_servers=[{"command": "uvx", "args": ["mcp-server-fetch"], "env": {"test": "test"}}],)
    print(result)
    assert "add_numbers" in result and "fetch" in result
