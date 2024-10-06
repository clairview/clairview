from markettor.clickhouse.log_entries import (
    KAFKA_LOG_ENTRIES_TABLE_SQL,
    LOG_ENTRIES_TABLE_MV_SQL,
    LOG_ENTRIES_TABLE_SQL,
)
from markettor.clickhouse.client.migration_tools import run_sql_with_exceptions

operations = [
    run_sql_with_exceptions(LOG_ENTRIES_TABLE_SQL()),
    run_sql_with_exceptions(KAFKA_LOG_ENTRIES_TABLE_SQL()),
    run_sql_with_exceptions(LOG_ENTRIES_TABLE_MV_SQL),
]
