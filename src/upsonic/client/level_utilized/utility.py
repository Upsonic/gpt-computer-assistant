import copy
import dill
import cloudpickle
import base64

from pydantic import BaseModel


def context_serializer(context):
    if context is not None:
        copy_of_context = copy.deepcopy(context)
        if isinstance(copy_of_context, list):
            for each in copy_of_context:

                each.tools = []
                each.response_format = None


                the_module = dill.detect.getmodule(each)
                if the_module is not None:
                    cloudpickle.register_pickle_by_value(the_module)
                pickled_context = cloudpickle.dumps(each)
                each = base64.b64encode(pickled_context).decode("utf-8")
        else:
            # Serialize the context
            copy_of_context.tools = []
            the_module = dill.detect.getmodule(copy_of_context)
            if the_module is not None:
                cloudpickle.register_pickle_by_value(the_module)
        pickled_context = cloudpickle.dumps(copy_of_context)
        context = base64.b64encode(pickled_context).decode("utf-8")
    else:
        context = None

    return context



def response_format_serializer(response_format):
    if response_format is None:
        response_format_str = "str"
    elif isinstance(response_format, (type, BaseModel)):
        # If it's a Pydantic model or other type, cloudpickle and base64 encode it
        the_module = dill.detect.getmodule(response_format)
        if the_module is not None:
            cloudpickle.register_pickle_by_value(the_module)
        pickled_format = cloudpickle.dumps(response_format)
        response_format_str = base64.b64encode(pickled_format).decode("utf-8")
    else:
        response_format_str = "str"

    return response_format_str


def response_format_deserializer(response_format_str, result):
    if response_format_str != "str":
        decoded_result = base64.b64decode(result["result"])
        deserialized_result = cloudpickle.loads(decoded_result)
    else:
        deserialized_result = result["result"]

    return deserialized_result


def tools_serializer(tools_):
    tools = []
    for i in tools_:


        if isinstance(i, type):

            tools.append(i.__name__+".*")
        # If its a string, get the name of the string
        elif isinstance(i, str):

            tools.append(i)
    return tools



class NoAPIKeyException(Exception):
    pass


class UnsupportedLLMModelException(Exception):
    pass


class CallErrorException(Exception):
    pass


def error_handler(result):
    if result["status_code"] == 401:
        raise NoAPIKeyException(result["detail"])
    
    if result["status_code"] == 400:
        raise UnsupportedLLMModelException(result["detail"])

    if result["status_code"] == 500:
        raise CallErrorException(result)