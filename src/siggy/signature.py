import inspect
from typing import Union, Awaitable, Callable

from pydantic import create_model
from .protocols import R


def gen_signature(fn: Union[Callable[..., R], Callable[..., Awaitable[R]]]) -> dict:
    """
    Generate a tool signature dictionary for an OpenAI responses API function
    using Pydantic to dynamically build a model reflecting the function's signature.
    Parameters with default values (and any *args/**kwargs) are omitted as they are considered 'known'.

    Returns:
        A dictionary with keys "name", "description", and "parameters" (the JSON schema).
    """
    sig = inspect.signature(fn)
    fields = {}

    for name, param in sig.parameters.items():
        if param.kind in {
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        }:
            continue
        if param.default is not inspect.Parameter.empty:
            continue

        annotation = (
            param.annotation if param.annotation is not inspect.Parameter.empty else str
        )
        fields[name] = (annotation, ...)

    Model = create_model(fn.__name__ + "Model", **fields)
    parameters_schema = Model.model_json_schema()

    return {
        "type": "function",
        "name": fn.__name__,
        "description": fn.__doc__ or "",
        "parameters": parameters_schema,
    }
