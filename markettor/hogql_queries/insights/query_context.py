from abc import ABC
from typing import Optional
from datetime import datetime
from markettor.hogql.constants import LimitContext
from markettor.hogql.context import HogQLContext
from markettor.hogql.modifiers import create_default_modifiers_for_team
from markettor.hogql.timings import HogQLTimings
from markettor.models.team.team import Team
from markettor.schema import (
    HogQLQueryModifiers,
)

from markettor.types import InsightQueryNode


class QueryContext(ABC):
    query: InsightQueryNode
    team: Team
    timings: HogQLTimings
    modifiers: HogQLQueryModifiers
    limit_context: LimitContext
    hogql_context: HogQLContext
    now: datetime

    def __init__(
        self,
        query: InsightQueryNode,
        team: Team,
        timings: Optional[HogQLTimings] = None,
        modifiers: Optional[HogQLQueryModifiers] = None,
        limit_context: Optional[LimitContext] = None,
        now: Optional[datetime] = None,
    ):
        self.query = query
        self.team = team
        self.timings = timings or HogQLTimings()
        self.limit_context = limit_context or LimitContext.QUERY
        self.modifiers = create_default_modifiers_for_team(team, modifiers)
        self.hogql_context = HogQLContext(
            team_id=self.team.pk,
            enable_select_queries=True,
            timings=self.timings,
            modifiers=self.modifiers,
        )
        self.now = now or datetime.now()
