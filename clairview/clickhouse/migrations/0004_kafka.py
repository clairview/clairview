from clairview.clickhouse.client.migration_tools import run_sql_with_exceptions
from clairview.models.event.sql import (
    DISTRIBUTED_EVENTS_TABLE_SQL,
    WRITABLE_EVENTS_TABLE_SQL,
)
from clairview.models.person.sql import (
    KAFKA_PERSONS_DISTINCT_ID_TABLE_SQL,
    KAFKA_PERSONS_TABLE_SQL,
    PERSONS_DISTINCT_ID_TABLE_MV_SQL,
    PERSONS_TABLE_MV_SQL,
)

# NOTE: this migration previously created kafka_events and events_mv tables.
# kafka_events was a Kafka ClickHouse engine table that used Protobuf for
# serialization. To remove complexity of deployments, Protobuf support has been
# removed from the ClairView app and the Plugin server. See
# https://github.com/ClairView/clairview/issues/9207 for detail.
#
# These have been superseded by kafka_events_json and events_json_mv. However,
# we can't simply add a DROP TABLE for the old tables as there may still be
# events in Kafka that need to be consumed. We'd need some orchestration around
# this to avoid losing in flight events. See migration
# ee/clickhouse/migrations/0025_json_events.py for details of the new tables.
#
# For new installs however, we don't need to be consider this case, so we can
# simply not create them.
#
# WARNING: this does however mean that you can arrive at different DB states
# depending on which versions of ClairView you have run.
operations = [
    run_sql_with_exceptions(KAFKA_PERSONS_TABLE_SQL()),
    run_sql_with_exceptions(KAFKA_PERSONS_DISTINCT_ID_TABLE_SQL()),
    run_sql_with_exceptions(PERSONS_TABLE_MV_SQL),
    run_sql_with_exceptions(PERSONS_DISTINCT_ID_TABLE_MV_SQL),
    run_sql_with_exceptions(WRITABLE_EVENTS_TABLE_SQL()),
    run_sql_with_exceptions(DISTRIBUTED_EVENTS_TABLE_SQL()),
]