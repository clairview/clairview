from abc import ABC
from typing import Optional
from datetime import datetime
from clairview.clairql.constants import LimitContext
from clairview.clairql.context import ClairQLContext
from clairview.clairql.modifiers import create_default_modifiers_for_team
from clairview.clairql.timings import ClairQLTimings
from clairview.models.team.team import Team
from clairview.schema import (
    ClairQLQueryModifiers,
)

from clairview.types import InsightQueryNode


class QueryContext(ABC):
    query: InsightQueryNode
    team: Team
    timings: ClairQLTimings
    modifiers: ClairQLQueryModifiers
    limit_context: LimitContext
    clairql_context: ClairQLContext
    now: datetime

    def __init__(
        self,
        query: InsightQueryNode,
        team: Team,
        timings: Optional[ClairQLTimings] = None,
        modifiers: Optional[ClairQLQueryModifiers] = None,
        limit_context: Optional[LimitContext] = None,
        now: Optional[datetime] = None,
    ):
        self.query = query
        self.team = team
        self.timings = timings or ClairQLTimings()
        self.limit_context = limit_context or LimitContext.QUERY
        self.modifiers = create_default_modifiers_for_team(team, modifiers)
        self.clairql_context = ClairQLContext(
            team_id=self.team.pk,
            enable_select_queries=True,
            timings=self.timings,
            modifiers=self.modifiers,
        )
        self.now = now or datetime.now()
