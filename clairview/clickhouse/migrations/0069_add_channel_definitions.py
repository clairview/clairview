from infi.clickhouse_orm import migrations

from clairview.models.channel_type.sql import (
    add_missing_channel_types,
)

operations = [
    migrations.RunPython(add_missing_channel_types),
]
