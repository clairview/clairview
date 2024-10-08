from typing import Literal, cast, Optional

from clairview.clairql import ast
from clairview.clairql.context import ClairQLContext
from clairview.clairql.database.database import create_clairql_database
from clairview.clairql.errors import NotImplementedError, QueryError, SyntaxError
from clairview.clairql.parser import parse_expr
from clairview.clairql.printer import prepare_ast_for_printing, print_prepared_ast
from clairview.queries.util import alias_poe_mode_for_legacy


# This is called only from "non-clairql-based" insights to translate ClairQL expressions into ClickHouse SQL
# All the constant string values will be collected into context.values
def translate_clairql(
    query: str,
    context: ClairQLContext,
    dialect: Literal["clairql", "clickhouse"] = "clickhouse",
    *,
    events_table_alias: Optional[str] = None,
    placeholders: Optional[dict[str, ast.Expr]] = None,
) -> str:
    """Translate a ClairQL expression into a ClickHouse expression."""
    if query == "":
        raise QueryError("Empty query")

    # TRICKY: As `translate_clairql` is only used in legacy queries (not the all-ClairQL ones), we must guard against
    # the PersonsOnEventsMode.PERSON_ID_OVERRIDE_PROPERTIES_JOINED being used here, as that is not supported in legacy
    actual_poe_mode = context.modifiers.personsOnEventsMode
    try:
        context.modifiers.personsOnEventsMode = alias_poe_mode_for_legacy(actual_poe_mode)
        # Create a fake query that selects from "events" to have fields to select from.
        if context.database is None:
            if context.team_id is None:
                raise ValueError("Cannot translate ClairQL for a filter with no team specified")
            context.database = create_clairql_database(context.team_id, context.modifiers)
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
