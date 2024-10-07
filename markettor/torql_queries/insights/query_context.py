from abc import ABC
from typing import Optional
from datetime import datetime
from markettor.torql.constants import LimitContext
from markettor.torql.context import TorQLContext
from markettor.torql.modifiers import create_default_modifiers_for_team
from markettor.torql.timings import TorQLTimings
from markettor.models.team.team import Team
from markettor.schema import (
    TorQLQueryModifiers,
)

from markettor.types import InsightQueryNode


class QueryContext(ABC):
    query: InsightQueryNode
    team: Team
    timings: TorQLTimings
    modifiers: TorQLQueryModifiers
    limit_context: LimitContext
    torql_context: TorQLContext
    now: datetime

    def __init__(
        self,
        query: InsightQueryNode,
        team: Team,
        timings: Optional[TorQLTimings] = None,
        modifiers: Optional[TorQLQueryModifiers] = None,
        limit_context: Optional[LimitContext] = None,
        now: Optional[datetime] = None,
    ):
        self.query = query
        self.team = team
        self.timings = timings or TorQLTimings()
        self.limit_context = limit_context or LimitContext.QUERY
        self.modifiers = create_default_modifiers_for_team(team, modifiers)
        self.torql_context = TorQLContext(
            team_id=self.team.pk,
            enable_select_queries=True,
            timings=self.timings,
            modifiers=self.modifiers,
        )
        self.now = now or datetime.now()
