from clairview.torql import ast
from clairview.torql.constants import LimitContext
from clairview.torql.parser import parse_select
from clairview.torql_queries.insights.paginators import TorQLHasMorePaginator
from clairview.torql_queries.query_runner import QueryRunner
from clairview.schema import (
    CachedSessionAttributionExplorerQueryResponse,
    SessionAttributionExplorerQuery,
    SessionAttributionExplorerQueryResponse,
    SessionAttributionGroupBy,
    TorQLFilters,
)

BREAKDOWN_NULL_DISPLAY = "(none)"


class SessionAttributionExplorerQueryRunner(QueryRunner):
    query: SessionAttributionExplorerQuery
    response: SessionAttributionExplorerQueryResponse
    cached_response: CachedSessionAttributionExplorerQueryResponse
    paginator: TorQLHasMorePaginator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paginator = TorQLHasMorePaginator.from_limit_context(
            limit_context=LimitContext.QUERY, limit=self.query.limit if self.query.limit else None
        )

    def to_query(self) -> ast.SelectQuery:
        with self.timings.measure("session_attribution_query_runner"):
            # We use string concatenation here, so that the resultant torql can be opened as its own torql insight,
            # so this part must never use user inputs.
            # Note that {filters} is a placeholder that is left as is, and replaced with actual filters in
            # execute_torql_query. Those filters *are* user input, which is why placeholders are used. It helps that
            # placeholders are valid in TorQL insights too, so it will "just work"!

            group_by = []

            def group_or_agg(group_name, field, result):
                if group_name in self.query.groupBy:
                    group_by.append(f'"{result}"')
                    return field
                else:
                    return f"topK(10)({field})"

            channel_type = group_or_agg(
                SessionAttributionGroupBy.CHANNEL_TYPE, "$channel_type", "context.columns.channel_type"
            )
            referring_domain = group_or_agg(
                SessionAttributionGroupBy.REFERRING_DOMAIN,
                "$entry_referring_domain",
                "context.columns.referring_domain",
            )
            utm_source = group_or_agg(
                SessionAttributionGroupBy.SOURCE, "$entry_utm_source", "context.columns.utm_source"
            )
            utm_medium = group_or_agg(
                SessionAttributionGroupBy.MEDIUM, "$entry_utm_medium", "context.columns.utm_medium"
            )
            utm_campaign = group_or_agg(
                SessionAttributionGroupBy.CAMPAIGN, "$entry_utm_campaign", "context.columns.utm_campaign"
            )
            ad_ids = group_or_agg(
                SessionAttributionGroupBy.AD_IDS,
                "nullIf(arrayStringConcat([if(isNotNull($entry_gclid), 'glcid', NULL), if(isNotNull($entry_gad_source), 'gad_source', NULL)], ','), '')",
                "context.columns.ad_ids",
            )
            entry_url = group_or_agg(
                SessionAttributionGroupBy.INITIAL_URL, "$entry_current_url", "context.columns.example_entry_urls"
            )

            filters = "{filters}"
            group_by_str = ("GROUP BY" + ", ".join(group_by)) if group_by else ""

            query_str = f"""
SELECT
    count() as "context.columns.count",
    {channel_type} as "context.columns.channel_type",
    {referring_domain} as "context.columns.referring_domain",
    {utm_source} as "context.columns.utm_source",
    {utm_medium} as "context.columns.utm_medium",
    {utm_campaign} as "context.columns.utm_campaign",
    {ad_ids} as "context.columns.ad_ids",
    {entry_url} as "context.columns.example_entry_urls"
FROM sessions
WHERE {filters}
{group_by_str}
ORDER BY "context.columns.count" DESC
"""

        query = parse_select(
            query_str,
            timings=self.timings,
        )
        assert isinstance(query, ast.SelectQuery)
        return query

    def calculate(self):
        response = self.paginator.execute_torql_query(
            query_type="session_attribution_query",
            query=self.to_query(),
            team=self.team,
            timings=self.timings,
            modifiers=self.modifiers,
            filters=TorQLFilters(dateRange=self.query.filters.dateRange, properties=self.query.filters.properties)
            if self.query.filters
            else None,
        )

        return SessionAttributionExplorerQueryResponse(
            columns=response.columns,
            results=response.results,
            timings=response.timings,
            types=response.types,
            torql=response.torql,
            modifiers=self.modifiers,
            **self.paginator.response_params(),
        )