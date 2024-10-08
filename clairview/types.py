from typing import TypeAlias, Union

from clairview.models.filters.filter import Filter
from clairview.models.filters.path_filter import PathFilter
from clairview.models.filters.retention_filter import RetentionFilter
from clairview.models.filters.stickiness_filter import StickinessFilter
from clairview.schema import (
    ActionsNode,
    CohortPropertyFilter,
    DataWarehouseNode,
    ElementPropertyFilter,
    EmptyPropertyFilter,
    EventPropertyFilter,
    EventsNode,
    DataWarehousePropertyFilter,
    DataWarehousePersonPropertyFilter,
    FeaturePropertyFilter,
    FunnelCorrelationActorsQuery,
    FunnelExclusionActionsNode,
    FunnelExclusionEventsNode,
    FunnelsActorsQuery,
    GroupPropertyFilter,
    ClairQLPropertyFilter,
    InsightActorsQuery,
    PersonPropertyFilter,
    RecordingPropertyFilter,
    SessionPropertyFilter,
    LogEntryPropertyFilter,
    TrendsQuery,
    FunnelsQuery,
    RetentionQuery,
    PathsQuery,
    StickinessQuery,
    LifecycleQuery,
)

FilterType: TypeAlias = Union[Filter, PathFilter, RetentionFilter, StickinessFilter]
"""Legacy insight filters."""

InsightQueryNode: TypeAlias = Union[
    TrendsQuery,
    FunnelsQuery,
    RetentionQuery,
    PathsQuery,
    StickinessQuery,
    LifecycleQuery,
]

InsightActorsQueryNode: TypeAlias = Union[InsightActorsQuery, FunnelsActorsQuery, FunnelCorrelationActorsQuery]

AnyPropertyFilter: TypeAlias = Union[
    EventPropertyFilter,
    PersonPropertyFilter,
    ElementPropertyFilter,
    SessionPropertyFilter,
    LogEntryPropertyFilter,
    CohortPropertyFilter,
    RecordingPropertyFilter,
    GroupPropertyFilter,
    FeaturePropertyFilter,
    ClairQLPropertyFilter,
    EmptyPropertyFilter,
    DataWarehousePropertyFilter,
    DataWarehousePersonPropertyFilter,
]

EntityNode: TypeAlias = Union[EventsNode, ActionsNode, DataWarehouseNode]
ExclusionEntityNode: TypeAlias = Union[FunnelExclusionEventsNode, FunnelExclusionActionsNode]
