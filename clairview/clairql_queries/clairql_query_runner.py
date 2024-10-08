from typing import Optional, cast
from collections.abc import Callable

from clairview.clairql import ast
from clairview.clairql.filters import replace_filters
from clairview.clairql.parser import parse_select
from clairview.clairql.placeholders import find_placeholders
from clairview.clairql.query import execute_clairql_query
from clairview.clairql.timings import ClairQLTimings
from clairview.clairql_queries.insights.paginators import ClairQLHasMorePaginator
from clairview.clairql_queries.query_runner import QueryRunner
from clairview.schema import (
    CachedClairQLQueryResponse,
    ClairQLQuery,
    ClairQLQueryResponse,
    DashboardFilter,
    ClairQLFilters,
    DateRange,
)


class ClairQLQueryRunner(QueryRunner):
    query: ClairQLQuery
    response: ClairQLQueryResponse
    cached_response: CachedClairQLQueryResponse

    def to_query(self) -> ast.SelectQuery:
        if self.timings is None:
            self.timings = ClairQLTimings()
        values: Optional[dict[str, ast.Expr]] = (
            {key: ast.Constant(value=value) for key, value in self.query.values.items()} if self.query.values else None
        )
        with self.timings.measure("parse_select"):
            parsed_select = parse_select(str(self.query.query), timings=self.timings, placeholders=values)

        if self.query.filters:
            with self.timings.measure("filters"):
                placeholders_in_query = find_placeholders(parsed_select)
                if "filters" in placeholders_in_query:
                    parsed_select = replace_filters(parsed_select, self.query.filters, self.team)
        return parsed_select

    def to_actors_query(self) -> ast.SelectQuery:
        return self.to_query()

    def calculate(self) -> ClairQLQueryResponse:
        query = self.to_query()
        paginator = None
        if isinstance(query, ast.SelectQuery) and not query.limit:
            paginator = ClairQLHasMorePaginator.from_limit_context(limit_context=self.limit_context)
        func = cast(
            Callable[..., ClairQLQueryResponse],
            execute_clairql_query if paginator is None else paginator.execute_clairql_query,
        )
        response = func(
            query_type="ClairQLQuery",
            query=query,
            filters=self.query.filters,
            modifiers=self.query.modifiers or self.modifiers,
            team=self.team,
            timings=self.timings,
            variables=self.query.variables,
            limit_context=self.limit_context,
        )
        if paginator:
            response = response.model_copy(update={**paginator.response_params(), "results": paginator.results})
        return response

    def apply_dashboard_filters(self, dashboard_filter: DashboardFilter):
        self.query.filters = self.query.filters or ClairQLFilters()

        if dashboard_filter.date_to or dashboard_filter.date_from:
            if self.query.filters.dateRange is None:
                self.query.filters.dateRange = DateRange()
            self.query.filters.dateRange.date_to = dashboard_filter.date_to
            self.query.filters.dateRange.date_from = dashboard_filter.date_from

        if dashboard_filter.properties:
            self.query.filters.properties = (self.query.filters.properties or []) + dashboard_filter.properties
