from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
try:
    from .utils.db import load_api_key, load_model_settings
except ImportError:
    from utils.db import load_api_key
from langchain_groq import ChatGroq


try:
    from .utils.db import load_api_key, load_openai_url, load_model_settings, load_groq_api_key
except ImportError:
    from utils.db import load_api_key, load_openai_url, load_model_settings, load_groq_api_key

def get_model():
    the_model = load_model_settings()
    the_api_key = load_api_key()
    the_openai_url = load_openai_url()
    
<<<<<<< HEAD
    args_mapping = {
        ChatOpenAI: f"model='{the_model}', api_key='{the_api_key}', base_url='{the_openai_url}'",
        ChatOllama: f"model='{the_model}'",
        ChatGroq: f"temperature=0, model_name='{the_model}', groq_api_key='{load_groq_api_key()}'"
=======
    def open_ai_base():
        if the_openai_url == "default":
            return {"model": the_model, "api_key": the_api_key, "max_retries":15}
        else:
            return {"model": the_model, "api_key": the_api_key, "max_retries":15, "base_url": the_openai_url}
    
    args_mapping = {
        ChatOpenAI: open_ai_base(),
        ChatOllama: {"model": the_model},
        ChatGroq: {"temperature": 0, "model_name": the_model.replace("-groq", ""), "groq_api_key": load_groq_api_key()}
>>>>>>> e38c63346bfd6108e3fc88b5128e78aeba0ea05f
    }
    
    model_mapping = {
        "gpt-4o": (ChatOpenAI, args_mapping[ChatOpenAI]),
<<<<<<< HEAD
        "gpt-3.5": (ChatOpenAI, args_mapping[ChatOpenAI]),
=======
        "gpt-4-turbo": (ChatOpenAI, args_mapping[ChatOpenAI]),
        "gpt-3.5-turbo": (ChatOpenAI, args_mapping[ChatOpenAI]),
>>>>>>> e38c63346bfd6108e3fc88b5128e78aeba0ea05f
        "llava": (ChatOllama, args_mapping[ChatOllama]),
        "bakllava": (ChatOllama, args_mapping[ChatOllama]),
        "mixtral-8x7b-groq": (ChatGroq, args_mapping[ChatGroq])
    }
    
<<<<<<< HEAD
    model_class, args = model_mapping[the_model] 
    return model_class(**args) if model_class else None 
    
=======
    model_class, args = model_mapping[the_model]
    return model_class(**args) if model_class else None

>>>>>>> e38c63346bfd6108e3fc88b5128e78aeba0ea05f

def get_client():
    the_api_key = load_api_key()
    the_openai_url = load_openai_url()
    if the_openai_url == "default":
        return OpenAI(api_key=the_api_key)
    else:
        return OpenAI(api_key=the_api_key, base_url=the_openai_url)