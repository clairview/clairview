from typing import Any, Optional

from clairview.clairql import ast
from clairview.clairql.constants import MAX_SELECT_RETURNED_ROWS
from clairview.clairql.context import ClairQLContext
from clairview.clairql.filters import replace_filters
from clairview.clairql.parser import parse_expr, parse_select
from clairview.clairql.printer import print_ast
from clairview.clairql.visitor import clear_locations
from clairview.schema import (
    ClairQLFilters,
    EventPropertyFilter,
    PersonPropertyFilter,
    DateRange,
)
from clairview.test.base import BaseTest


class TestFilters(BaseTest):
    maxDiff = None

    def _parse_expr(self, expr: str, placeholders: Optional[dict[str, Any]] = None):
        return clear_locations(parse_expr(expr, placeholders=placeholders))

    def _parse_select(self, select: str, placeholders: Optional[dict[str, Any]] = None):
        return clear_locations(parse_select(select, placeholders=placeholders))

    def _print_ast(self, node: ast.Expr):
        return print_ast(
            node,
            dialect="clairql",
            context=ClairQLContext(team_id=self.team.pk, enable_select_queries=True),
        )

    def test_replace_filters_empty(self):
        select = replace_filters(self._parse_select("SELECT event FROM events"), ClairQLFilters(), self.team)
        self.assertEqual(self._print_ast(select), f"SELECT event FROM events LIMIT {MAX_SELECT_RETURNED_ROWS}")

        select = replace_filters(
            self._parse_select("SELECT event FROM events where {filters}"),
            ClairQLFilters(),
            self.team,
        )
        self.assertEqual(
            self._print_ast(select), f"SELECT event FROM events WHERE true LIMIT {MAX_SELECT_RETURNED_ROWS}"
        )

    def test_replace_filters_date_range(self):
        select = replace_filters(
            self._parse_select("SELECT event FROM events where {filters}"),
            ClairQLFilters(dateRange=DateRange(date_from="2020-02-02")),
            self.team,
        )
        self.assertEqual(
            self._print_ast(select),
            f"SELECT event FROM events WHERE greaterOrEquals(timestamp, toDateTime('2020-02-02 00:00:00.000000')) LIMIT {MAX_SELECT_RETURNED_ROWS}",
        )

        select = replace_filters(
            self._parse_select("SELECT event FROM events where {filters}"),
            ClairQLFilters(dateRange=DateRange(date_to="2020-02-02")),
            self.team,
        )
        self.assertEqual(
            self._print_ast(select),
            f"SELECT event FROM events WHERE less(timestamp, toDateTime('2020-02-02 00:00:00.000000')) LIMIT {MAX_SELECT_RETURNED_ROWS}",
        )

        select = replace_filters(
            self._parse_select("SELECT event FROM events where {filters}"),
            ClairQLFilters(dateRange=DateRange(date_from="2020-02-02", date_to="2020-02-03 23:59:59")),
            self.team,
        )
        self.assertEqual(
            self._print_ast(select),
            "SELECT event FROM events WHERE "
            "and(less(timestamp, toDateTime('2020-02-03 23:59:59.000000')), "
            f"greaterOrEquals(timestamp, toDateTime('2020-02-02 00:00:00.000000'))) LIMIT {MAX_SELECT_RETURNED_ROWS}",
        )

        # now with different team timezone
        self.team.timezone = "America/New_York"
        self.team.save()

        select = replace_filters(
            self._parse_select("SELECT event FROM events where {filters}"),
            ClairQLFilters(dateRange=DateRange(date_from="2020-02-02", date_to="2020-02-03 23:59:59")),
            self.team,
        )
        self.assertEqual(
            self._print_ast(select),
            "SELECT event FROM events WHERE "
            "and(less(timestamp, toDateTime('2020-02-03 23:59:59.000000')), "
            f"greaterOrEquals(timestamp, toDateTime('2020-02-02 00:00:00.000000'))) LIMIT {MAX_SELECT_RETURNED_ROWS}",
        )

    def test_replace_filters_event_property(self):
        select = replace_filters(
            self._parse_select("SELECT event FROM events where {filters}"),
            ClairQLFilters(
                properties=[EventPropertyFilter(key="random_uuid", operator="exact", value="123", type="event")]
            ),
            self.team,
        )
        self.assertEqual(
            self._print_ast(select),
            f"SELECT event FROM events WHERE equals(properties.random_uuid, '123') LIMIT {MAX_SELECT_RETURNED_ROWS}",
        )

    def test_replace_filters_person_property(self):
        select = replace_filters(
            self._parse_select("SELECT event FROM events where {filters}"),
            ClairQLFilters(
                properties=[PersonPropertyFilter(key="random_uuid", operator="exact", value="123", type="person")]
            ),
            self.team,
        )
        self.assertEqual(
            self._print_ast(select),
            f"SELECT event FROM events WHERE equals(person.properties.random_uuid, '123') LIMIT {MAX_SELECT_RETURNED_ROWS}",
        )

        select = replace_filters(
            self._parse_select("SELECT event FROM events where {filters}"),
            ClairQLFilters(
                properties=[
                    EventPropertyFilter(key="random_uuid", operator="exact", value="123", type="event"),
                    PersonPropertyFilter(key="random_uuid", operator="exact", value="123", type="person"),
                ]
            ),
            self.team,
        )
        self.assertEqual(
            self._print_ast(select),
            f"SELECT event FROM events WHERE and(equals(properties.random_uuid, '123'), equals(person.properties.random_uuid, '123')) LIMIT {MAX_SELECT_RETURNED_ROWS}",
        )

    def test_replace_filters_test_accounts(self):
        self.team.test_account_filters = [
            {
                "key": "email",
                "type": "person",
                "value": "clairview.com",
                "operator": "not_icontains",
            }
        ]
        self.team.save()

        select = replace_filters(
            self._parse_select("SELECT event FROM events where {filters}"),
            ClairQLFilters(filterTestAccounts=True),
            self.team,
        )
        self.assertEqual(
            self._print_ast(select),
            f"SELECT event FROM events WHERE notILike(person.properties.email, '%clairview.com%') LIMIT {MAX_SELECT_RETURNED_ROWS}",
        )
