from infi.clickhouse_orm import migrations

from markettor.models.channel_type.sql import (
    add_missing_channel_types,
)

operations = [
    migrations.RunPython(add_missing_channel_types),
]
