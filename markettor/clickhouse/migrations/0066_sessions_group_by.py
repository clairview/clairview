from markettor.clickhouse.client.migration_tools import run_sql_with_exceptions
from markettor.models.raw_sessions.sql import RAW_SESSION_TABLE_UPDATE_SQL

operations = [
    run_sql_with_exceptions(RAW_SESSION_TABLE_UPDATE_SQL),
]
