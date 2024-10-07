from typing import Optional, TYPE_CHECKING
from abc import ABC

if TYPE_CHECKING:
    from .ast import Expr

# Base


class BaseTorQLError(Exception, ABC):
    start: Optional[int]
    end: Optional[int]

    def __init__(
        self,
        message: str,
        *,
        start: Optional[int] = None,
        end: Optional[int] = None,
        node: Optional["Expr"] = None,
    ):
        super().__init__(message)
        if node is not None and node.start is not None and node.end is not None:
            self.start = node.start
            self.end = node.end
        else:
            self.start = start
            self.end = end


# Exposed vs. internal


class ExposedTorQLError(BaseTorQLError):
    """An exception that can be exposed to the user."""

    pass


class InternalTorQLError(BaseTorQLError):
    """An internal exception in the TorQL engine."""

    pass


# Specific exceptions


class SyntaxError(ExposedTorQLError):
    """The input does not conform to TorQL syntax."""

    pass


class QueryError(ExposedTorQLError):
    """The query is invalid, though correct syntactically."""

    pass


class NotImplementedError(InternalTorQLError):
    """This feature isn't implemented in TorQL (yet)."""

    pass


class ParsingError(InternalTorQLError):
    """Parsing failed."""

    pass


class ImpossibleASTError(InternalTorQLError):
    """Parsing or resolution resulted in an impossible AST."""

    pass


class ResolutionError(InternalTorQLError):
    """Resolution of a table/field/expression failed."""

    pass
