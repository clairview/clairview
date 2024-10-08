from typing import Optional
from clairview.torql_queries.torql_query_runner import TorQLQueryRunner

from clairview.schema import (
    DashboardFilter,
    DateRange,
    EventPropertyFilter,
    TorQLFilters,
    TorQLQuery,
)

from clairview.test.base import BaseTest


class TestTorQLDashboardFilters(BaseTest):
    def _create_torql_runner(
        self, query: str = "SELECT uuid FROM events", filters: Optional[TorQLFilters] = None
    ) -> TorQLQueryRunner:
        return TorQLQueryRunner(team=self.team, query=TorQLQuery(query=query, filters=filters))

    def test_empty_dashboard_filters_change_nothing(self):
        query_runner = self._create_torql_runner()
        query_runner.apply_dashboard_filters(DashboardFilter())

        assert query_runner.query.filters == TorQLFilters()

    def test_date_from_override_updates_whole_date_range(self):
        query_runner = self._create_torql_runner()
        query_runner.apply_dashboard_filters(DashboardFilter(date_from="-14d"))

        assert query_runner.query.filters == TorQLFilters(dateRange=DateRange(date_from="-14d", date_to=None))

    def test_date_from_and_date_to_override_updates_whole_date_range(self):
        query_runner = self._create_torql_runner(
            filters=TorQLFilters(dateRange=DateRange(date_from="-7d", date_to=None))
        )
        query_runner.apply_dashboard_filters(DashboardFilter(date_from="2024-07-07", date_to="2024-07-14"))

        assert query_runner.query.filters == TorQLFilters(
            dateRange=DateRange(date_from="2024-07-07", date_to="2024-07-14")
        )

    def test_properties_set_when_no_filters_present(self):
        query_runner = self._create_torql_runner()
        query_runner.apply_dashboard_filters(
            DashboardFilter(properties=[EventPropertyFilter(key="key", value="value", operator="exact")])
        )

        assert query_runner.query.filters == TorQLFilters(
            properties=[EventPropertyFilter(key="key", value="value", operator="exact")]
        )

    def test_properties_list_extends_filters_list(self):
        query_runner = self._create_torql_runner(
            filters=TorQLFilters(properties=[EventPropertyFilter(key="abc", value="foo", operator="regex")])
        )
        query_runner.apply_dashboard_filters(
            DashboardFilter(properties=[EventPropertyFilter(key="xyz", value="bar", operator="regex")])
        )

        assert query_runner.query.filters == TorQLFilters(
            properties=[
                EventPropertyFilter(key="abc", value="foo", operator="regex"),
                EventPropertyFilter(key="xyz", value="bar", operator="regex"),
            ]
        )
