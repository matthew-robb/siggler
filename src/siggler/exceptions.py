class sigglerError(Exception):
    """Base class for all exceptions raised by siggler."""


class ToolNotFoundError(sigglerError):
    """Raised when a tool is not found im the registry."""


class AsyncToolNotFoundError(sigglerError):
    """Raised when an async tool is not found in the registry."""


class InvalidArgumentsError(sigglerError):
    """Raised when the arguments provided to a tool are invalid."""
