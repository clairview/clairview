from ee.clickhouse.queries.stickiness.stickiness_event_query import (
    ClickhouseStickinessEventsQuery,
)
from clairview.models.filters.mixins.utils import cached_property
from clairview.queries.stickiness.stickiness_actors import StickinessActors


class ClickhouseStickinessActors(StickinessActors):
    event_query_class = ClickhouseStickinessEventsQuery

    @cached_property
    def aggregation_group_type_index(self):
        if self.entity.math == "unique_group":
            return self.entity.math_group_type_index
        return None
