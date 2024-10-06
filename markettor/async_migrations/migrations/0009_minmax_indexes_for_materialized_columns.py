from markettor.async_migrations.definition import (
    AsyncMigrationDefinition,
    AsyncMigrationOperation,
)


class Migration(AsyncMigrationDefinition):
    description = "Create minmax indexes for materialized columns to speed up queries"

    depends_on = "0008_speed_up_kafka_timestamp_filters"
    markettor_min_version = "1.43.0"
    markettor_max_version = "1.49.99"

    def is_required(self):
        return False

    operations: list[AsyncMigrationOperation] = []
