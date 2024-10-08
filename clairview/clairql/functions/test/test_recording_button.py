from clairview.clairql.errors import QueryError
from clairview.clairql.query import execute_clairql_query
from clairview.test.base import BaseTest


class TestRecordingButton(BaseTest):
    def test_recording_button(self):
        response = execute_clairql_query("select recording_button('12345-6789')", self.team, pretty=False)
        self.assertEqual(
            response.clickhouse,
            f"SELECT tuple(%(clairql_val_0)s, %(clairql_val_1)s, %(clairql_val_2)s, %(clairql_val_3)s) LIMIT 100 SETTINGS readonly=2, max_execution_time=60, allow_experimental_object_type=1, format_csv_allow_double_quotes=0, max_ast_elements=4000000, max_expanded_ast_elements=4000000, max_bytes_before_external_group_by=0",
        )
        self.assertEqual(
            response.clairql,
            f"SELECT tuple('__hx_tag', 'RecordingButton', 'sessionId', '12345-6789') LIMIT 100",
        )
        self.assertEqual(
            response.results[0][0],
            ("__hx_tag", "RecordingButton", "sessionId", "12345-6789"),
        )

    def test_sparkline_error(self):
        with self.assertRaises(QueryError) as e:
            execute_clairql_query(f"SELECT recording_button()", self.team)
        self.assertEqual(str(e.exception), "Function 'recording_button' expects 1 argument, found 0")
