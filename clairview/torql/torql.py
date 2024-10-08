from typing import Literal, cast, Optional

from clairview.torql import ast
from clairview.torql.context import TorQLContext
from clairview.torql.database.database import create_torql_database
from clairview.torql.errors import NotImplementedError, QueryError, SyntaxError
from clairview.torql.parser import parse_expr
from clairview.torql.printer import prepare_ast_for_printing, print_prepared_ast
from clairview.queries.util import alias_poe_mode_for_legacy


# This is called only from "non-torql-based" insights to translate TorQL expressions into ClickHouse SQL
# All the constant string values will be collected into context.values
def translate_torql(
    query: str,
    context: TorQLContext,
    dialect: Literal["torql", "clickhouse"] = "clickhouse",
    *,
    events_table_alias: Optional[str] = None,
    placeholders: Optional[dict[str, ast.Expr]] = None,
) -> str:
    """Translate a TorQL expression into a ClickHouse expression."""
    if query == "":
        raise QueryError("Empty query")

    # TRICKY: As `translate_torql` is only used in legacy queries (not the all-TorQL ones), we must guard against
    # the PersonsOnEventsMode.PERSON_ID_OVERRIDE_PROPERTIES_JOINED being used here, as that is not supported in legacy
    actual_poe_mode = context.modifiers.personsOnEventsMode
    try:
        context.modifiers.personsOnEventsMode = alias_poe_mode_for_legacy(actual_poe_mode)
        # Create a fake query that selects from "events" to have fields to select from.
        if context.database is None:
            if context.team_id is None:
                raise ValueError("Cannot translate TorQL for a filter with no team specified")
            context.database = create_torql_database(context.team_id, context.modifiers)
        node = parse_expr(query, placeholders=placeholders)
        select_query = ast.SelectQuery(select=[node], select_from=ast.JoinExpr(table=ast.Field(chain=["events"])))

        if events_table_alias is not None and isinstance(select_query.select_from, ast.JoinExpr):
            select_query.select_from.alias = events_table_alias

        prepared_select_query: ast.SelectQuery = cast(
            ast.SelectQuery,
            prepare_ast_for_printing(select_query, context=context, dialect=dialect, stack=[select_query]),
        )
        return print_prepared_ast(
            prepared_select_query.select[0],
            context=context,
            dialect=dialect,
            stack=[prepared_select_query],
        )
    except (NotImplementedError, SyntaxError):
        raise
    finally:
        context.modifiers.personsOnEventsMode = actual_poe_mode  # Restore the original value
