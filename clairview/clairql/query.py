import dataclasses
from typing import Optional, Union, cast

from clairview.clickhouse.client.connection import Workload
from clairview.errors import ExposedCHQueryError
from clairview.clairql import ast
from clairview.clairql.constants import ClairQLGlobalSettings, LimitContext, get_default_limit_for_context
from clairview.clairql.errors import ExposedClairQLError
from clairview.clairql.clairql import ClairQLContext
from clairview.clairql.modifiers import create_default_modifiers_for_team
from clairview.clairql.parser import parse_select
from clairview.clairql.placeholders import replace_placeholders, find_placeholders
from clairview.clairql.printer import (
    prepare_ast_for_printing,
    print_ast,
    print_prepared_ast,
)
from clairview.clairql.filters import replace_filters
from clairview.clairql.timings import ClairQLTimings
from clairview.clairql.variables import replace_variables
from clairview.clairql.visitor import clone_expr
from clairview.models.team import Team
from clairview.clickhouse.query_tagging import tag_queries
from clairview.client import sync_execute
from clairview.schema import (
    ClairQLQueryResponse,
    ClairQLFilters,
    ClairQLQueryModifiers,
    ClairQLMetadata,
    ClairQLMetadataResponse,
    HogLanguage,
    ClairQLVariable,
)
from clairview.settings import CLAIRQL_INCREASED_MAX_EXECUTION_TIME


def execute_clairql_query(
    query: Union[str, ast.SelectQuery, ast.SelectUnionQuery],
    team: Team,
    *,
    query_type: str = "clairql_query",
    filters: Optional[ClairQLFilters] = None,
    placeholders: Optional[dict[str, ast.Expr]] = None,
    variables: Optional[dict[str, ClairQLVariable]] = None,
    workload: Workload = Workload.DEFAULT,
    settings: Optional[ClairQLGlobalSettings] = None,
    modifiers: Optional[ClairQLQueryModifiers] = None,
    limit_context: Optional[LimitContext] = LimitContext.QUERY,
    timings: Optional[ClairQLTimings] = None,
    pretty: Optional[bool] = True,
    context: Optional[ClairQLContext] = None,
) -> ClairQLQueryResponse:
    if timings is None:
        timings = ClairQLTimings()

    if context is None:
        context = ClairQLContext(team_id=team.pk)

    query_modifiers = create_default_modifiers_for_team(team, modifiers)
    debug = modifiers is not None and modifiers.debug
    error: Optional[str] = None
    explain: Optional[list[str]] = None
    results = None
    types = None
    metadata: Optional[ClairQLMetadataResponse] = None

    with timings.measure("query"):
        if isinstance(query, ast.SelectQuery) or isinstance(query, ast.SelectUnionQuery):
            select_query = query
            query = None
        else:
            select_query = parse_select(str(query), timings=timings)

    with timings.measure("variables"):
        if variables and len(variables.keys()) > 0:
            select_query = replace_variables(node=select_query, variables=list(variables.values()), team=team)

    with timings.measure("replace_placeholders"):
        placeholders_in_query = find_placeholders(select_query)
        placeholders = placeholders or {}

        if "filters" in placeholders and filters is not None:
            raise ValueError(
                f"Query contains 'filters' placeholder, yet filters are also provided as a standalone query parameter."
            )
        if "filters" in placeholders_in_query or any(
            placeholder and placeholder.startswith("filters.") for placeholder in placeholders_in_query
        ):
            select_query = replace_filters(select_query, filters, team)

            leftover_placeholders: list[str] = []
            for placeholder in placeholders_in_query:
                if placeholder is None:
                    raise ValueError("Placeholder expressions are not yet supported")
                if placeholder != "filters" and not placeholder.startswith("filters."):
                    leftover_placeholders.append(placeholder)

            placeholders_in_query = leftover_placeholders

        if len(placeholders_in_query) > 0:
            if len(placeholders) == 0:
                raise ValueError(
                    f"Query contains placeholders, but none were provided. Placeholders in query: {', '.join(s for s in placeholders_in_query if s is not None)}"
                )
            select_query = replace_placeholders(select_query, placeholders)

    with timings.measure("max_limit"):
        select_queries = (
            select_query.select_queries if isinstance(select_query, ast.SelectUnionQuery) else [select_query]
        )
        for one_query in select_queries:
            if one_query.limit is None:
                one_query.limit = ast.Constant(value=get_default_limit_for_context(limit_context))

    # Get printed ClairQL query, and returned columns. Using a cloned query.
    with timings.measure("clairql"):
        with timings.measure("prepare_ast"):
            clairql_query_context = dataclasses.replace(
                context,
                # set the team.pk here so someone can't pass a context for a different team 🤷‍️
                team_id=team.pk,
                team=team,
                enable_select_queries=True,
                timings=timings,
                modifiers=query_modifiers,
            )

            with timings.measure("clone"):
                cloned_query = clone_expr(select_query, True)
            select_query_clairql = cast(
                ast.SelectQuery,
                prepare_ast_for_printing(node=cloned_query, context=clairql_query_context, dialect="clairql"),
            )

        with timings.measure("print_ast"):
            clairql = print_prepared_ast(
                select_query_clairql, clairql_query_context, "clairql", pretty=pretty if pretty is not None else True
            )
            print_columns = []
            columns_query = (
                select_query_clairql.select_queries[0]
                if isinstance(select_query_clairql, ast.SelectUnionQuery)
                else select_query_clairql
            )
            for node in columns_query.select:
                if isinstance(node, ast.Alias):
                    print_columns.append(node.alias)
                else:
                    print_columns.append(
                        print_prepared_ast(
                            node=node,
                            context=clairql_query_context,
                            dialect="clairql",
                            stack=[select_query_clairql],
                        )
                    )

    settings = settings or ClairQLGlobalSettings()
    if limit_context in (LimitContext.EXPORT, LimitContext.COHORT_CALCULATION, LimitContext.QUERY_ASYNC):
        settings.max_execution_time = CLAIRQL_INCREASED_MAX_EXECUTION_TIME

    # Print the ClickHouse SQL query
    with timings.measure("print_ast"):
        try:
            clickhouse_context = dataclasses.replace(
                context,
                # set the team.pk here so someone can't pass a context for a different team 🤷‍️
                team_id=team.pk,
                team=team,
                enable_select_queries=True,
                timings=timings,
                modifiers=query_modifiers,
            )
            clickhouse_sql = print_ast(
                select_query,
                context=clickhouse_context,
                dialect="clickhouse",
                settings=settings,
                pretty=pretty if pretty is not None else True,
            )
        except Exception as e:
            if debug:
                clickhouse_sql = None
                if isinstance(e, ExposedCHQueryError | ExposedClairQLError):
                    error = str(e)
                else:
                    error = "Unknown error"
            else:
                raise

    if clickhouse_sql is not None:
        timings_dict = timings.to_dict()
        with timings.measure("clickhouse_execute"):
            tag_queries(
                team_id=team.pk,
                query_type=query_type,
                has_joins="JOIN" in clickhouse_sql,
                has_json_operations="JSONExtract" in clickhouse_sql or "JSONHas" in clickhouse_sql,
                timings=timings_dict,
                modifiers={k: v for k, v in modifiers.model_dump().items() if v is not None} if modifiers else {},
            )

            try:
                results, types = sync_execute(
                    clickhouse_sql,
                    clickhouse_context.values,
                    with_column_types=True,
                    workload=workload,
                    team_id=team.pk,
                    readonly=True,
                )
            except Exception as e:
                if debug:
                    results = []
                    if isinstance(e, ExposedCHQueryError | ExposedClairQLError):
                        error = str(e)
                    else:
                        error = "Unknown error"
                else:
                    raise

        if debug and error is None:  # If the query errored, explain will fail as well.
            with timings.measure("explain"):
                explain_results = sync_execute(
                    f"EXPLAIN {clickhouse_sql}",
                    clickhouse_context.values,
                    with_column_types=True,
                    workload=workload,
                    team_id=team.pk,
                    readonly=True,
                )
                explain = [str(r[0]) for r in explain_results[0]]
            with timings.measure("metadata"):
                from clairview.clairql.metadata import get_clairql_metadata

                metadata = get_clairql_metadata(ClairQLMetadata(language=HogLanguage.HOG_QL, query=clairql, debug=True), team)

    return ClairQLQueryResponse(
        query=query,
        clairql=clairql,
        clickhouse=clickhouse_sql,
        error=error,
        timings=timings.to_list(),
        results=results,
        columns=print_columns,
        types=types,
        modifiers=query_modifiers,
        explain=explain,
        metadata=metadata,
    )
