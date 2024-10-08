from clairview.torql.context import TorQLContext
from clairview.torql.database.database import create_torql_database
from clairview.torql.parser import parse_select
from clairview.torql.printer import print_ast
from clairview.torql.query import create_default_modifiers_for_team
from clairview.test.base import BaseTest
from clairview.torql.database.test.tables import (
    create_aapl_stock_table_view,
    create_aapl_stock_s3_table,
    create_nested_aapl_stock_view,
    create_aapl_stock_table_self_referencing,
)


class TestView(BaseTest):
    maxDiff = None

    def _init_database(self):
        self.database = create_torql_database(self.team.pk)
        self.database.aapl_stock_view = create_aapl_stock_table_view()
        self.database.aapl_stock = create_aapl_stock_s3_table()
        self.database.aapl_stock_nested_view = create_nested_aapl_stock_view()
        self.database.aapl_stock_self = create_aapl_stock_table_self_referencing()
        self.context = TorQLContext(
            team_id=self.team.pk,
            enable_select_queries=True,
            database=self.database,
            modifiers=create_default_modifiers_for_team(self.team),
        )

    def _select(self, query: str, dialect: str = "clickhouse") -> str:
        return print_ast(parse_select(query), self.context, dialect=dialect)

    def test_view_table_select(self):
        self._init_database()

        torql = self._select(query="SELECT * FROM aapl_stock LIMIT 10", dialect="torql")
        self.assertEqual(
            torql,
            "SELECT Date, Open, High, Low, Close, Volume, OpenInt FROM aapl_stock LIMIT 10",
        )

        clickhouse = self._select(query="SELECT * FROM aapl_stock_view LIMIT 10", dialect="clickhouse")

        self.assertEqual(
            clickhouse,
            "SELECT aapl_stock_view.Date AS Date, aapl_stock_view.Open AS Open, aapl_stock_view.High AS High, "
            "aapl_stock_view.Low AS Low, aapl_stock_view.Close AS Close, aapl_stock_view.Volume AS Volume, "
            "aapl_stock_view.OpenInt AS OpenInt FROM (SELECT aapl_stock.Date AS Date, aapl_stock.Open AS Open, "
            "aapl_stock.High AS High, aapl_stock.Low AS Low, aapl_stock.Close AS Close, aapl_stock.Volume AS Volume, "
            "aapl_stock.OpenInt AS OpenInt FROM s3(%(torql_val_0_sensitive)s, %(torql_val_1)s) AS aapl_stock) "
            "AS aapl_stock_view LIMIT 10",
        )

    def test_view_with_alias(self):
        self._init_database()

        torql = self._select(query="SELECT * FROM aapl_stock LIMIT 10", dialect="torql")
        self.assertEqual(
            torql,
            "SELECT Date, Open, High, Low, Close, Volume, OpenInt FROM aapl_stock LIMIT 10",
        )

        clickhouse = self._select(
            query="SELECT * FROM aapl_stock_view AS some_alias LIMIT 10",
            dialect="clickhouse",
        )

        self.assertEqual(
            clickhouse,
            "SELECT some_alias.Date AS Date, some_alias.Open AS Open, some_alias.High AS High, some_alias.Low AS Low, some_alias.Close AS Close, some_alias.Volume AS Volume, some_alias.OpenInt AS OpenInt FROM (SELECT aapl_stock.Date AS Date, aapl_stock.Open AS Open, aapl_stock.High AS High, aapl_stock.Low AS Low, aapl_stock.Close AS Close, aapl_stock.Volume AS Volume, aapl_stock.OpenInt AS OpenInt FROM s3(%(torql_val_0_sensitive)s, %(torql_val_1)s) AS aapl_stock) AS some_alias LIMIT 10",
        )
