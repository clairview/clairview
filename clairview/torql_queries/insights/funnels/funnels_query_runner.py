from datetime import timedelta

from clairview.torql.constants import TorQLGlobalSettings, MAX_BYTES_BEFORE_EXTERNAL_GROUP_BY
from math import ceil
from typing import Optional, Any

from django.utils.timezone import datetime
from clairview.caching.insights_api import (
    BASE_MINIMUM_INSIGHT_REFRESH_INTERVAL,
    REDUCED_MINIMUM_INSIGHT_REFRESH_INTERVAL,
)

from clairview.torql import ast
from clairview.torql.constants import LimitContext
from clairview.torql.printer import to_printed_torql
from clairview.torql.query import execute_torql_query
from clairview.torql.timings import TorQLTimings
from clairview.torql_queries.insights.funnels.funnel_query_context import FunnelQueryContext
from clairview.torql_queries.insights.funnels.funnel_time_to_convert import FunnelTimeToConvert
from clairview.torql_queries.insights.funnels.funnel_trends import FunnelTrends
from clairview.torql_queries.insights.funnels.funnel_trends_udf import FunnelTrendsUDF
from clairview.torql_queries.insights.funnels.utils import get_funnel_actor_class, get_funnel_order_class, use_udf
from clairview.torql_queries.query_runner import QueryRunner
from clairview.torql_queries.utils.query_date_range import QueryDateRange
from clairview.models import Team
from clairview.models.filters.mixins.utils import cached_property
from clairview.schema import (
    CachedFunnelsQueryResponse,
    FunnelVizType,
    FunnelsQuery,
    FunnelsQueryResponse,
    TorQLQueryModifiers,
    StepOrderValue,
)


class FunnelsQueryRunner(QueryRunner):
    query: FunnelsQuery
    response: FunnelsQueryResponse
    cached_response: CachedFunnelsQueryResponse
    context: FunnelQueryContext

    def __init__(
        self,
        query: FunnelsQuery | dict[str, Any],
        team: Team,
        timings: Optional[TorQLTimings] = None,
        modifiers: Optional[TorQLQueryModifiers] = None,
        limit_context: Optional[LimitContext] = None,
        **kwargs,
    ):
        super().__init__(query, team=team, timings=timings, modifiers=modifiers, limit_context=limit_context)

        self.context = FunnelQueryContext(
            query=self.query, team=team, timings=timings, modifiers=modifiers, limit_context=limit_context
        )
        self.kwargs = kwargs

    def _refresh_frequency(self):
        date_to = self.query_date_range.date_to()
        date_from = self.query_date_range.date_from()
        interval = self.query_date_range.interval_name

        delta_days: Optional[int] = None
        if date_from and date_to:
            delta = date_to - date_from
            delta_days = ceil(delta.total_seconds() / timedelta(days=1).total_seconds())

        refresh_frequency = BASE_MINIMUM_INSIGHT_REFRESH_INTERVAL
        if interval == "hour" or (delta_days is not None and delta_days <= 7):
            # The interval is shorter for short-term insights
            refresh_frequency = REDUCED_MINIMUM_INSIGHT_REFRESH_INTERVAL

        return refresh_frequency

    def to_query(self) -> ast.SelectQuery:
        return self.funnel_class.get_query()

    def to_actors_query(self) -> ast.SelectQuery | ast.SelectUnionQuery:
        return self.funnel_actor_class.actor_query()

    def calculate(self):
        query = self.to_query()
        timings = []

        # TODO: can we get this from execute_torql_query as well?
        torql = to_printed_torql(query, self.team)

        response = execute_torql_query(
            query_type="FunnelsQuery",
            query=query,
            team=self.team,
            timings=self.timings,
            modifiers=self.modifiers,
            limit_context=self.limit_context,
            settings=TorQLGlobalSettings(
                # Make sure funnel queries never OOM
                max_bytes_before_external_group_by=MAX_BYTES_BEFORE_EXTERNAL_GROUP_BY,
                allow_experimental_analyzer=True,
            ),
        )

        results = self.funnel_class._format_results(response.results)

        if response.timings is not None:
            timings.extend(response.timings)

        return FunnelsQueryResponse(
            isUdf=self._use_udf, results=results, timings=timings, torql=torql, modifiers=self.modifiers
        )

    @cached_property
    def _use_udf(self):
        return use_udf(self.context.funnelsFilter, self.team)

    @cached_property
    def funnel_order_class(self):
        return get_funnel_order_class(self.context.funnelsFilter, use_udf=self._use_udf)(context=self.context)

    @cached_property
    def funnel_class(self):
        funnelVizType = self.context.funnelsFilter.funnelVizType

        if funnelVizType == FunnelVizType.TRENDS:
            return (
                FunnelTrendsUDF(context=self.context, **self.kwargs)
                if self._use_udf and self.context.funnelsFilter.funnelOrderType != StepOrderValue.UNORDERED
                else FunnelTrends(context=self.context, **self.kwargs)
            )
        elif funnelVizType == FunnelVizType.TIME_TO_CONVERT:
            return FunnelTimeToConvert(context=self.context)
        else:
            return self.funnel_order_class

    @cached_property
    def funnel_actor_class(self):
        return get_funnel_actor_class(self.context.funnelsFilter, self._use_udf)(context=self.context)

    @cached_property
    def query_date_range(self):
        return QueryDateRange(
            date_range=self.query.dateRange,
            team=self.team,
            interval=self.query.interval,
            now=datetime.now(),
        )