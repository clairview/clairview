from clairview.clairql.ast import FloatType, IntegerType
from clairview.test.base import BaseTest
from typing import Optional
from clairview.clairql.functions.mapping import (
    compare_types,
    find_clairql_function,
    find_clairql_aggregation,
    find_clairql_clairview_function,
    ClairQLFunctionMeta,
)


class TestMappings(BaseTest):
    def _return_present_function(self, function: Optional[ClairQLFunctionMeta]) -> ClairQLFunctionMeta:
        assert function is not None
        return function

    def _get_clairql_function(self, name: str) -> ClairQLFunctionMeta:
        return self._return_present_function(find_clairql_function(name))

    def _get_clairql_aggregation(self, name: str) -> ClairQLFunctionMeta:
        return self._return_present_function(find_clairql_aggregation(name))

    def _get_clairql_clairview_function(self, name: str) -> ClairQLFunctionMeta:
        return self._return_present_function(find_clairql_clairview_function(name))

    def test_find_case_sensitive_function(self):
        self.assertEqual(self._get_clairql_function("toString").clickhouse_name, "toString")
        self.assertEqual(find_clairql_function("TOString"), None)
        self.assertEqual(find_clairql_function("PlUs"), None)

        self.assertEqual(self._get_clairql_aggregation("countIf").clickhouse_name, "countIf")
        self.assertEqual(find_clairql_aggregation("COUNTIF"), None)

        self.assertEqual(self._get_clairql_clairview_function("sparkline").clickhouse_name, "sparkline")
        self.assertEqual(find_clairql_clairview_function("SPARKLINE"), None)

    def test_find_case_insensitive_function(self):
        self.assertEqual(self._get_clairql_function("CoAlesce").clickhouse_name, "coalesce")

        self.assertEqual(self._get_clairql_aggregation("SuM").clickhouse_name, "sum")

    def test_find_non_existent_function(self):
        self.assertEqual(find_clairql_function("functionThatDoesntExist"), None)
        self.assertEqual(find_clairql_aggregation("functionThatDoesntExist"), None)
        self.assertEqual(find_clairql_clairview_function("functionThatDoesntExist"), None)

    def test_compare_types(self):
        res = compare_types([IntegerType()], (IntegerType(),))
        assert res is True

    def test_compare_types_mismatch(self):
        res = compare_types([IntegerType()], (FloatType(),))
        assert res is False

    def test_compare_types_mismatch_lengths(self):
        res = compare_types([IntegerType()], (IntegerType(), IntegerType()))
        assert res is False

    def test_compare_types_mismatch_differing_order(self):
        res = compare_types([IntegerType(), FloatType()], (FloatType(), IntegerType()))
        assert res is False
