class SiggyError(Exception):
    """Base class for all exceptions raised by Siggy."""


class ToolNotFoundError(SiggyError):
    """Raised when a tool is not found im the registry."""


class AsyncToolNotFoundError(SiggyError):
    """Raised when an async tool is not found in the registry."""


class InvalidArgumentsError(SiggyError):
    """Raised when the arguments provided to a tool are invalid."""
