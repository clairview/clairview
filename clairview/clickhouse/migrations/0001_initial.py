from clairview.clickhouse.client.migration_tools import run_sql_with_exceptions
from clairview.models.event.sql import EVENTS_TABLE_SQL
from clairview.settings import CLICKHOUSE_CLUSTER, CLICKHOUSE_DATABASE

operations = [
    run_sql_with_exceptions(f"CREATE DATABASE IF NOT EXISTS {CLICKHOUSE_DATABASE} ON CLUSTER '{CLICKHOUSE_CLUSTER}'"),
    run_sql_with_exceptions(EVENTS_TABLE_SQL()),
]