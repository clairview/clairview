from typing import Literal

BreakdownType = Literal["event", "person", "cohort", "group", "session", "clairql"]
IntervalType = Literal["hour", "day", "week", "month"]
FunnelWindowIntervalType = Literal["second", "minute", "hour", "day", "week", "month"]


class BaseParamMixin:
    _data: dict
