from typing import Optional
from clairview.clairql_queries.clairql_query_runner import ClairQLQueryRunner

from clairview.schema import (
    DashboardFilter,
    DateRange,
    EventPropertyFilter,
    ClairQLFilters,
    ClairQLQuery,
)

from clairview.test.base import BaseTest


class TestClairQLDashboardFilters(BaseTest):
    def _create_clairql_runner(
        self, query: str = "SELECT uuid FROM events", filters: Optional[ClairQLFilters] = None
    ) -> ClairQLQueryRunner:
        return ClairQLQueryRunner(team=self.team, query=ClairQLQuery(query=query, filters=filters))

    def test_empty_dashboard_filters_change_nothing(self):
        query_runner = self._create_clairql_runner()
        query_runner.apply_dashboard_filters(DashboardFilter())

        assert query_runner.query.filters == ClairQLFilters()

    def test_date_from_override_updates_whole_date_range(self):
        query_runner = self._create_clairql_runner()
        query_runner.apply_dashboard_filters(DashboardFilter(date_from="-14d"))

        assert query_runner.query.filters == ClairQLFilters(dateRange=DateRange(date_from="-14d", date_to=None))

    def test_date_from_and_date_to_override_updates_whole_date_range(self):
        query_runner = self._create_clairql_runner(
            filters=ClairQLFilters(dateRange=DateRange(date_from="-7d", date_to=None))
        )
        query_runner.apply_dashboard_filters(DashboardFilter(date_from="2024-07-07", date_to="2024-07-14"))

        assert query_runner.query.filters == ClairQLFilters(
            dateRange=DateRange(date_from="2024-07-07", date_to="2024-07-14")
        )

    def test_properties_set_when_no_filters_present(self):
        query_runner = self._create_clairql_runner()
        query_runner.apply_dashboard_filters(
            DashboardFilter(properties=[EventPropertyFilter(key="key", value="value", operator="exact")])
        )

        assert query_runner.query.filters == ClairQLFilters(
            properties=[EventPropertyFilter(key="key", value="value", operator="exact")]
        )

    def test_properties_list_extends_filters_list(self):
        query_runner = self._create_clairql_runner(
            filters=ClairQLFilters(properties=[EventPropertyFilter(key="abc", value="foo", operator="regex")])
        )
        query_runner.apply_dashboard_filters(
            DashboardFilter(properties=[EventPropertyFilter(key="xyz", value="bar", operator="regex")])
        )

        assert query_runner.query.filters == ClairQLFilters(
            properties=[
                EventPropertyFilter(key="abc", value="foo", operator="regex"),
                EventPropertyFilter(key="xyz", value="bar", operator="regex"),
            ]
        )
