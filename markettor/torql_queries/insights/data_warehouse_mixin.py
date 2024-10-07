from markettor.torql import ast
from markettor.models.filters.mixins.utils import cached_property
from markettor.schema import ActionsNode, EventsNode, DataWarehouseNode


class DataWarehouseInsightQueryMixin:
    series: EventsNode | ActionsNode | DataWarehouseNode

    @cached_property
    def _table_expr(self) -> ast.Field:
        if isinstance(self.series, DataWarehouseNode):
            return ast.Field(chain=[self.series.table_name])

        return ast.Field(chain=["events"])
