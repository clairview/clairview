from django.utils.timezone import datetime

from clairview.clairql import ast
from clairview.clairql.parser import parse_select
from clairview.clairql.query import execute_clairql_query
from clairview.clairql_queries.utils.query_date_range import QueryDateRange
from clairview.clairql_queries.web_analytics.web_analytics_query_runner import (
    WebAnalyticsQueryRunner,
)
from clairview.models.filters.mixins.utils import cached_property
from clairview.schema import CachedWebTopClicksQueryResponse, WebTopClicksQuery, WebTopClicksQueryResponse


class WebTopClicksQueryRunner(WebAnalyticsQueryRunner):
    query: WebTopClicksQuery
    response: WebTopClicksQueryResponse
    cached_response: CachedWebTopClicksQueryResponse

    def to_query(self) -> ast.SelectQuery | ast.SelectUnionQuery:
        with self.timings.measure("top_clicks_query"):
            top_sources_query = parse_select(
                """
SELECT
    properties.$el_text as el_text,
    count() as total_clicks,
    COUNT(DISTINCT events.person_id) as unique_visitors
FROM
    events
WHERE
    event == '$autocapture'
AND events.properties.$event_type = 'click'
AND el_text IS NOT NULL
AND ({events_where})
GROUP BY
    el_text
ORDER BY total_clicks DESC
LIMIT 10
                """,
                timings=self.timings,
                placeholders={
                    "event_properties": self.events_where(),
                    "date_from": self.query_date_range.date_from_as_clairql(),
                    "date_to": self.query_date_range.date_to_as_clairql(),
                },
            )
        return top_sources_query

    def calculate(self):
        response = execute_clairql_query(
            query_type="top_sources_query",
            query=self.to_query(),
            team=self.team,
            timings=self.timings,
            modifiers=self.modifiers,
            limit_context=self.limit_context,
        )

        return WebTopClicksQueryResponse(
            columns=response.columns,
            results=response.results,
            timings=response.timings,
            types=response.types,
            modifiers=self.modifiers,
        )

    @cached_property
    def query_date_range(self):
        return QueryDateRange(
            date_range=self.query.dateRange,
            team=self.team,
            interval=None,
            now=datetime.now(),
        )