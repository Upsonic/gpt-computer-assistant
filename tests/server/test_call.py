from upsonicai.server import Call
from pydantic import BaseModel


class Human(BaseModel):
    name: str
    surname: str
    gender: str


def test_gpt4o_call():
    result = Call.gpt_4o("Hi, I am Onur Atakan ULUSOY and I am a male", Human)
    assert result.name == "Onur Atakan"
    assert result.surname == "ULUSOY"
    assert result.gender == "male"


def test_gpt4o_call_without_return_type():
    result = Call.gpt_4o("Say hi to me")
    potential_keywords = ["hi", "hello", "hey"]
    assert any(keyword in result.lower() for keyword in potential_keywords)
