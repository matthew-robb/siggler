import json
from typing import Any, Dict,  Union, cast

from .exceptions import InvalidArgumentsError
from .registry import get_tool, get_atool
from .protocols import JsonSerialisable


def call(name: str, arguments: Union[str, Dict[str, JsonSerialisable]], **kwargs: JsonSerialisable) -> Any:
    """
    Synchronously call the provided tool.
    Args:
        name: Name of the tool to call (must be synchronous).
        arguments: Either a JSON string or a dictionary of JSON serializable arguments.
        **kwargs: Additional JSON serializable keyword arguments.

    Returns:
        The result of the tool call.
    """
    arguments = _parse_arguments(arguments)
    fn = get_tool(name)
    return fn(**arguments, **kwargs)


async def acall(name: str, arguments: Union[str, Dict[str, JsonSerialisable]], **kwargs: JsonSerialisable) -> Any:
    """
    Asynchronously call the provided asynchronous function.
    Args:
        name: Name of the async tool to call (must be asynchronous).
        arguments: Either a JSON string or a dictionary of JSON serializable arguments.
        **kwargs: Additional JSON serializable keyword arguments.

    Returns:
        The result of the tool call.
    """
    arguments = _parse_arguments(arguments)
    fn = get_atool(name)
    return await fn(**arguments, **kwargs)


def _parse_arguments(arguments: Union[str, Dict[str, JsonSerialisable]]) -> Dict[str, JsonSerialisable]:
    if isinstance(arguments, str):
        try:
            parsed = json.loads(arguments)
            return cast(Dict[str, JsonSerialisable], parsed)
        except json.JSONDecodeError as e:
            raise InvalidArgumentsError(
                f"The provided arguments are not valid JSON: {e}"
            )
    return arguments