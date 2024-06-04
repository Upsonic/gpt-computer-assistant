from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from .utils.db import load_api_key





def get_model():
    the_api_key = load_api_key()
    if the_api_key is None:
        return ChatOllama(model="llava")
    return ChatOpenAI(model="gpt-4o", api_key=the_api_key)


def get_client():
    the_api_key = load_api_key()
    return OpenAI(api_key=the_api_key)
