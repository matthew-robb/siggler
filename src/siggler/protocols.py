from typing import Union, List, Dict, TypeVar, Protocol, Awaitable, Type

JsonValue = Union[str, int, float, bool, None]
JsonArray = List[Union[JsonValue, "JsonArray", "JsonObject"]]
JsonObject = Dict[str, Union[JsonValue, "JsonArray", "JsonObject"]]
JsonSerialisable = Union[JsonValue, JsonArray, JsonObject]


R = TypeVar("R", covariant=True)


class JsonTool(Protocol[R]):
    """Protocol for functions with JSON serializable parameters."""

    __name__: str

    def __call__(self, *args: JsonSerialisable, **kwargs: JsonSerialisable) -> R: ...
    signature: dict

class AsyncJsonTool(Protocol[R]):
    """Protocol for async functions with JSON serializable parameters."""

    __name__: str
    async def __call__(
        self, *args: JsonSerialisable, **kwargs: JsonSerialisable
    ) -> Awaitable[R]: ...
    signature: dict
