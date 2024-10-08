from typing import Optional
from warnings import warn

from django.db import models

from clairview.clairql.ast import SelectQuery
from clairview.clairql.context import ClairQLContext
from clairview.clairql.database.models import LazyJoinToAdd
from clairview.clairql.errors import ResolutionError
from clairview.clairql.parser import parse_expr
from clairview.models.team import Team
from clairview.models.utils import CreatedMetaFields, DeletedMetaFields, UUIDModel
from clairview.warehouse.models.datawarehouse_saved_query import DataWarehouseSavedQuery


class DataWarehouseViewLink(CreatedMetaFields, UUIDModel, DeletedMetaFields):
    """Deprecated model, use DataWarehouseJoin instead"""

    def __init_subclass__(cls, **kwargs):
        """This throws a deprecation warning on subclassing."""
        warn("DataWarehouseViewLink is deprecated, use DataWarehouseJoin", DeprecationWarning, stacklevel=2)
        super().__init_subclass__(**kwargs)

    def __init__(self, *args, **kwargs):
        """This throws a deprecation warning on initialization."""
        warn("DataWarehouseViewLink is deprecated, use DataWarehouseJoin", DeprecationWarning, stacklevel=2)
        super().__init__(*args, **kwargs)

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    table = models.CharField(max_length=128)
    from_join_key = models.CharField(max_length=400)
    saved_query = models.ForeignKey(DataWarehouseSavedQuery, on_delete=models.CASCADE)
    to_join_key = models.CharField(max_length=400)


class DataWarehouseJoin(CreatedMetaFields, UUIDModel, DeletedMetaFields):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    source_table_name = models.CharField(max_length=400)
    source_table_key = models.CharField(max_length=400)
    joining_table_name = models.CharField(max_length=400)
    joining_table_key = models.CharField(max_length=400)
    field_name = models.CharField(max_length=400)

    def join_function(
        self, override_source_table_key: Optional[str] = None, override_joining_table_key: Optional[str] = None
    ):
        def _join_function(
            join_to_add: LazyJoinToAdd,
            context: ClairQLContext,
            node: SelectQuery,
        ):
            _source_table_key = override_source_table_key or self.source_table_key
            _joining_table_key = override_joining_table_key or self.joining_table_key

            from clairview.clairql import ast

            if not join_to_add.fields_accessed:
                raise ResolutionError(f"No fields requested from {join_to_add.to_table}")

            left = parse_expr(_source_table_key)
            if not isinstance(left, ast.Field):
                raise ResolutionError("Data Warehouse Join ClairQL expression should be a Field node")
            left.chain = [join_to_add.from_table, *left.chain]

            right = parse_expr(_joining_table_key)
            if not isinstance(right, ast.Field):
                raise ResolutionError("Data Warehouse Join ClairQL expression should be a Field node")
            right.chain = [join_to_add.to_table, *right.chain]

            join_expr = ast.JoinExpr(
                table=ast.SelectQuery(
                    select=[
                        ast.Alias(alias=alias, expr=ast.Field(chain=chain))
                        for alias, chain in join_to_add.fields_accessed.items()
                    ],
                    select_from=ast.JoinExpr(table=ast.Field(chain=[self.joining_table_name])),
                ),
                join_type="LEFT JOIN",
                alias=join_to_add.to_table,
                constraint=ast.JoinConstraint(
                    expr=ast.CompareOperation(
                        op=ast.CompareOperationOp.Eq,
                        left=left,
                        right=right,
                    ),
                    constraint_type="ON",
                ),
            )
            return join_expr

        return _join_function
