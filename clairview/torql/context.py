from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Literal, Optional

from clairview.torql.timings import TorQLTimings
from clairview.schema import TorQLNotice, TorQLQueryModifiers

if TYPE_CHECKING:
    from clairview.torql.database.database import Database
    from clairview.torql.transforms.property_types import PropertySwapper
    from clairview.models import Team


@dataclass
class TorQLFieldAccess:
    input: list[str]
    type: Optional[Literal["event", "event.properties", "person", "person.properties"]]
    field: Optional[str]
    sql: str


@dataclass
class TorQLContext:
    """Context given to a TorQL expression printer"""

    # Team making the queries
    team_id: Optional[int]
    # Team making the queries - if team is passed in, then the team isn't queried when creating the database
    team: Optional["Team"] = None
    # Virtual database we're querying, will be populated from team_id if not present
    database: Optional["Database"] = None
    # If set, will save string constants to this dict. Inlines strings into the query if None.
    values: dict = field(default_factory=dict)
    # Are we small part of a non-TorQL query? If so, use custom syntax for accessed person properties.
    within_non_torql_query: bool = False
    # Enable full SELECT queries and subqueries in ClickHouse
    enable_select_queries: bool = False
    # Do we apply a limit of MAX_SELECT_RETURNED_ROWS=10000 to the topmost select query?
    limit_top_select: bool = True
    # Globals that will be resolved in the context of the query
    globals: Optional[dict] = None

    # Warnings returned with the metadata query
    warnings: list["TorQLNotice"] = field(default_factory=list)
    # Notices returned with the metadata query
    notices: list["TorQLNotice"] = field(default_factory=list)
    # Errors returned with the metadata query
    errors: list["TorQLNotice"] = field(default_factory=list)

    # Timings in seconds for different parts of the TorQL query
    timings: TorQLTimings = field(default_factory=TorQLTimings)
    # Modifications requested by the TorQL client
    modifiers: TorQLQueryModifiers = field(default_factory=TorQLQueryModifiers)
    # Enables more verbose output for debugging
    debug: bool = False

    property_swapper: Optional["PropertySwapper"] = None

    def add_value(self, value: Any) -> str:
        key = f"torql_val_{len(self.values)}"
        self.values[key] = value
        return f"%({key})s"

    def add_sensitive_value(self, value: Any) -> str:
        key = f"torql_val_{len(self.values)}_sensitive"
        self.values[key] = value
        return f"%({key})s"

    def add_notice(
        self,
        message: str,
        start: Optional[int] = None,
        end: Optional[int] = None,
        fix: Optional[str] = None,
    ):
        if not any(n.start == start and n.end == end and n.message == message and n.fix == fix for n in self.notices):
            self.notices.append(TorQLNotice(start=start, end=end, message=message, fix=fix))

    def add_warning(
        self,
        message: str,
        start: Optional[int] = None,
        end: Optional[int] = None,
        fix: Optional[str] = None,
    ):
        if not any(n.start == start and n.end == end and n.message == message and n.fix == fix for n in self.warnings):
            self.warnings.append(TorQLNotice(start=start, end=end, message=message, fix=fix))

    def add_error(
        self,
        message: str,
        start: Optional[int] = None,
        end: Optional[int] = None,
        fix: Optional[str] = None,
    ):
        if not any(n.start == start and n.end == end and n.message == message and n.fix == fix for n in self.errors):
            self.errors.append(TorQLNotice(start=start, end=end, message=message, fix=fix))