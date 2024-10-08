from typing import Optional, TYPE_CHECKING
from abc import ABC

if TYPE_CHECKING:
    from .ast import Expr

# Base


class BaseClairQLError(Exception, ABC):
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


class ExposedClairQLError(BaseClairQLError):
    """An exception that can be exposed to the user."""

    pass


class InternalClairQLError(BaseClairQLError):
    """An internal exception in the ClairQL engine."""

    pass


# Specific exceptions


class SyntaxError(ExposedClairQLError):
    """The input does not conform to ClairQL syntax."""

    pass


class QueryError(ExposedClairQLError):
    """The query is invalid, though correct syntactically."""

    pass


class NotImplementedError(InternalClairQLError):
    """This feature isn't implemented in ClairQL (yet)."""

    pass


class ParsingError(InternalClairQLError):
    """Parsing failed."""

    pass


class ImpossibleASTError(InternalClairQLError):
    """Parsing or resolution resulted in an impossible AST."""

    pass


class ResolutionError(InternalClairQLError):
    """Resolution of a table/field/expression failed."""

    pass
