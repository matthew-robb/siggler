import inspect
from typing import (
    Any,
    Dict,
    Union,
    Callable,
    Awaitable,
    overload, cast,
)

from .exceptions import ToolNotFoundError, AsyncToolNotFoundError
from .protocols import R, JsonTool, AsyncJsonTool
from .signature import gen_signature


_tool_registry: Dict[str, JsonTool[Any]] = {}
_atool_registry: Dict[str, AsyncJsonTool[Any]] = {}


def get_tool(name: str) -> JsonTool[Any]:
    """
    Get a tool by name from the registry.
    """

    fn = _tool_registry.get(name)
    if not fn:
        raise ToolNotFoundError(f"Tool '{name}' not found in registry.")
    return fn


def get_atool(name: str) -> AsyncJsonTool[Any]:
    """
    Get an asynchronous tool by name from the registry.
    """
    fn = _atool_registry.get(name)
    if not fn:
        raise AsyncToolNotFoundError(f"Async tool '{name}' not found in registry.")
    return fn


@overload
def tool(fn: Callable[..., R]) -> JsonTool[R]: ...


@overload
def tool(fn: Callable[..., Awaitable[R]]) -> AsyncJsonTool[R]: ...


def tool(fn: Union[Callable[..., R], Callable[..., Awaitable[R]]]) -> Union[JsonTool[R], AsyncJsonTool[R]]:
    """
    Decorator that attaches a 'signature' attribute to the function.

    All parameter types must be JSON serializable (str, int, float, bool, None,
    lists, and dictionaries) for the tool to function correctly with OpenAI API.

    Usage:
        @tool
        def my_tool(param: str) -> str:
            ...

    The generated signature can be accessed via my_tool.signature.
    """

    sig = gen_signature(fn)
    setattr(fn, "signature", sig)

    if inspect.iscoroutinefunction(fn):
        _atool_registry[fn.__name__] = cast(AsyncJsonTool[R], fn)
        return cast(AsyncJsonTool[R], fn)
    else:
        _tool_registry[fn.__name__] = cast(JsonTool[R], fn)
        return cast(JsonTool[R], fn)
