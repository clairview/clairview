import re
from typing import Any, Optional, Union

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

from clairview.torql import ast
from clairview.torql.database.database import Database
from clairview.torql.database.models import FieldOrTable, SavedQuery
from clairview.models.team import Team
from clairview.models.utils import CreatedMetaFields, DeletedMetaFields, UUIDModel
from clairview.schema import TorQLQueryModifiers
from clairview.warehouse.models.util import (
    CLICKHOUSE_TORQL_MAPPING,
    STR_TO_TORQL_MAPPING,
    clean_type,
    remove_named_tuples,
)
from clairview.torql.database.s3_table import S3Table
from clairview.warehouse.util import database_sync_to_async


def validate_saved_query_name(value):
    if not re.match(r"^[A-Za-z_$][A-Za-z0-9_$]*$", value):
        raise ValidationError(
            f"{value} is not a valid view name. View names can only contain letters, numbers, '_', or '$' ",
            params={"value": value},
        )

    # This doesnt protect us from naming a table the same as a warehouse table
    database = Database()
    all_keys = list(vars(database).keys())
    table_names = [key for key in all_keys if isinstance(getattr(database, key), ast.Table)]

    if value in table_names:
        raise ValidationError(
            f"{value} is not a valid view name. View names cannot overlap with ClairView table names.",
            params={"value": value},
        )


class DataWarehouseSavedQuery(CreatedMetaFields, UUIDModel, DeletedMetaFields):
    class Status(models.TextChoices):
        """Possible states of this SavedQuery."""

        CANCELLED = "Cancelled"
        COMPLETED = "Completed"
        FAILED = "Failed"
        RUNNING = "Running"

    name = models.CharField(max_length=128, validators=[validate_saved_query_name])
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    columns = models.JSONField(
        default=dict,
        null=True,
        blank=True,
        help_text="Dict of all columns with ClickHouse type (including Nullable())",
    )
    external_tables = models.JSONField(default=list, null=True, blank=True, help_text="List of all external tables")
    query = models.JSONField(default=dict, null=True, blank=True, help_text="TorQL query")
    status = models.CharField(
        null=True, choices=Status.choices, max_length=64, help_text="The status of when this SavedQuery last ran."
    )
    last_run_at = models.DateTimeField(
        null=True,
        help_text="The timestamp of this SavedQuery's last run (if any).",
    )
    table = models.ForeignKey("clairview.DataWarehouseTable", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["team", "name"],
                name="clairview_datawarehouse_saved_query_unique_name",
            )
        ]

    def get_columns(self) -> dict[str, dict[str, Any]]:
        from clairview.api.services.query import process_query_dict
        from clairview.torql_queries.query_runner import ExecutionMode

        response = process_query_dict(self.team, self.query, execution_mode=ExecutionMode.CALCULATE_BLOCKING_ALWAYS)
        result = getattr(response, "types", [])

        if result is None or isinstance(result, int):
            raise Exception("No columns types provided by clickhouse in get_columns")

        columns = {
            str(item[0]): {
                "torql": CLICKHOUSE_TORQL_MAPPING[clean_type(str(item[1]))].__name__,
                "clickhouse": item[1],
                "valid": True,
            }
            for item in result
        }

        return columns

    def get_clickhouse_column_type(self, column_name: str) -> Optional[str]:
        clickhouse_type = self.columns.get(column_name, None)

        if isinstance(clickhouse_type, dict) and self.columns[column_name].get("clickhouse"):
            clickhouse_type = self.columns[column_name].get("clickhouse")

            if clickhouse_type.startswith("Nullable("):
                clickhouse_type = clickhouse_type.replace("Nullable(", "")[:-1]

        return clickhouse_type

    @property
    def s3_tables(self):
        from clairview.torql.context import TorQLContext
        from clairview.torql.database.database import create_torql_database
        from clairview.torql.parser import parse_select
        from clairview.torql.query import create_default_modifiers_for_team
        from clairview.torql.resolver import resolve_types
        from clairview.models.property.util import S3TableVisitor

        context = TorQLContext(
            team_id=self.team.pk,
            enable_select_queries=True,
            modifiers=create_default_modifiers_for_team(self.team),
        )
        node = parse_select(self.query["query"])
        context.database = create_torql_database(context.team_id)

        node = resolve_types(node, context, dialect="clickhouse")
        table_collector = S3TableVisitor()
        table_collector.visit(node)

        return list(table_collector.tables)

    @property
    def folder_path(self):
        return f"team_{self.team.pk}_model_{self.id.hex}/modeling"

    @property
    def url_pattern(self):
        return (
            f"https://{settings.AIRBYTE_BUCKET_DOMAIN}/dlt/team_{self.team.pk}_model_{self.id.hex}/modeling/{self.name}"
        )

    def torql_definition(self, modifiers: Optional[TorQLQueryModifiers] = None) -> Union[SavedQuery, S3Table]:
        from clairview.warehouse.models.table import CLICKHOUSE_TORQL_MAPPING

        columns = self.columns or {}

        fields: dict[str, FieldOrTable] = {}
        structure = []
        for column, type in columns.items():
            # Support for 'old' style columns
            if isinstance(type, str):
                clickhouse_type = type
            else:
                clickhouse_type = type["clickhouse"]

            if clickhouse_type.startswith("Nullable("):
                clickhouse_type = clickhouse_type.replace("Nullable(", "")[:-1]

            # TODO: remove when addressed https://github.com/ClickHouse/ClickHouse/issues/37594
            if clickhouse_type.startswith("Array("):
                clickhouse_type = remove_named_tuples(clickhouse_type)

            if isinstance(type, dict):
                column_invalid = not type.get("valid", True)
            else:
                column_invalid = False

            if not column_invalid or (modifiers is not None and modifiers.s3TableUseInvalidColumns):
                structure.append(f"`{column}` {clickhouse_type}")

            # Support for 'old' style columns
            if isinstance(type, str):
                torql_type_str = clickhouse_type.partition("(")[0]
                torql_type = CLICKHOUSE_TORQL_MAPPING[torql_type_str]
            else:
                torql_type = STR_TO_TORQL_MAPPING[type["torql"]]

            fields[column] = torql_type(name=column)

        if (
            self.table is not None
            and (self.status == DataWarehouseSavedQuery.Status.COMPLETED or self.last_run_at is not None)
            and modifiers is not None
            and modifiers.useMaterializedViews
        ):
            return self.table.torql_definition(modifiers)
        else:
            return SavedQuery(
                id=str(self.id),
                name=self.name,
                query=self.query["query"],
                fields=fields,
            )


@database_sync_to_async
def aget_saved_query_by_id(saved_query_id: str, team_id: int) -> DataWarehouseSavedQuery | None:
    return (
        DataWarehouseSavedQuery.objects.prefetch_related("team")
        .exclude(deleted=True)
        .get(id=saved_query_id, team_id=team_id)
    )


@database_sync_to_async
def asave_saved_query(saved_query: DataWarehouseSavedQuery) -> None:
    saved_query.save()


@database_sync_to_async
def aget_table_by_saved_query_id(saved_query_id: str, team_id: int):
    return DataWarehouseSavedQuery.objects.get(id=saved_query_id, team_id=team_id).table