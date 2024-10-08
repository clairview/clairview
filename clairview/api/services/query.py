import structlog
from typing import Optional

from pydantic import BaseModel
from rest_framework.exceptions import ValidationError

from clairvm.python.debugger import color_bytecode
from clairview.clickhouse.query_tagging import tag_queries
from clairview.cloud_utils import is_cloud
from clairview.clairql.bytecode import execute_hog
from clairview.clairql.constants import LimitContext
from clairview.clairql.context import ClairQLContext
from clairview.clairql.database.database import create_clairql_database, serialize_database
from clairview.clairql.autocomplete import get_clairql_autocomplete
from clairview.clairql.metadata import get_clairql_metadata
from clairview.clairql.modifiers import create_default_modifiers_for_team
from clairview.clairql_queries.query_runner import CacheMissResponse, ExecutionMode, get_query_runner
from clairview.models import Team, User
from clairview.schema import (
    DatabaseSchemaQueryResponse,
    HogQuery,
    DashboardFilter,
    ClairQLAutocomplete,
    ClairQLMetadata,
    QuerySchemaRoot,
    DatabaseSchemaQuery,
    HogQueryResponse,
)

logger = structlog.get_logger(__name__)


def process_query_dict(
    team: Team,
    query_json: dict,
    *,
    dashboard_filters_json: Optional[dict] = None,
    limit_context: Optional[LimitContext] = None,
    execution_mode: ExecutionMode = ExecutionMode.RECENT_CACHE_CALCULATE_BLOCKING_IF_STALE,
    user: Optional[User] = None,
    query_id: Optional[str] = None,
    insight_id: Optional[int] = None,
    dashboard_id: Optional[int] = None,
) -> dict | BaseModel:
    model = QuerySchemaRoot.model_validate(query_json)
    tag_queries(query=query_json)
    dashboard_filters = DashboardFilter.model_validate(dashboard_filters_json) if dashboard_filters_json else None
    return process_query_model(
        team,
        model.root,
        dashboard_filters=dashboard_filters,
        limit_context=limit_context,
        execution_mode=execution_mode,
        user=user,
        query_id=query_id,
        insight_id=insight_id,
        dashboard_id=dashboard_id,
    )


def process_query_model(
    team: Team,
    query: BaseModel,  # mypy has problems with unions and isinstance
    *,
    dashboard_filters: Optional[DashboardFilter] = None,
    limit_context: Optional[LimitContext] = None,
    execution_mode: ExecutionMode = ExecutionMode.RECENT_CACHE_CALCULATE_BLOCKING_IF_STALE,
    user: Optional[User] = None,
    query_id: Optional[str] = None,
    insight_id: Optional[int] = None,
    dashboard_id: Optional[int] = None,
) -> dict | BaseModel:
    result: dict | BaseModel

    try:
        query_runner = get_query_runner(query, team, limit_context=limit_context)
    except ValueError:  # This query doesn't run via query runner
        if hasattr(query, "source") and isinstance(query.source, BaseModel):
            result = process_query_model(
                team,
                query.source,
                dashboard_filters=dashboard_filters,
                limit_context=limit_context,
                execution_mode=execution_mode,
                user=user,
                query_id=query_id,
                insight_id=insight_id,
                dashboard_id=dashboard_id,
            )
        elif execution_mode == ExecutionMode.CACHE_ONLY_NEVER_CALCULATE:
            # Caching is handled by query runners, so in this case we can only return a cache miss
            result = CacheMissResponse(cache_key=None)
        elif isinstance(query, HogQuery):
            if is_cloud() and (user is None or not user.is_staff):
                return {"results": "Hog queries currently require staff user privileges."}

            try:
                hog_result = execute_hog(query.code or "", team=team)
                result = HogQueryResponse(
                    results=hog_result.result,
                    bytecode=hog_result.bytecode,
                    coloredBytecode=color_bytecode(hog_result.bytecode),
                    stdout="\n".join(hog_result.stdout),
                )
            except Exception as e:
                result = HogQueryResponse(results=f"ERROR: {str(e)}")
        elif isinstance(query, ClairQLAutocomplete):
            result = get_clairql_autocomplete(query=query, team=team)
        elif isinstance(query, ClairQLMetadata):
            metadata_query = ClairQLMetadata.model_validate(query)
            metadata_response = get_clairql_metadata(query=metadata_query, team=team)
            result = metadata_response
        elif isinstance(query, DatabaseSchemaQuery):
            database = create_clairql_database(team.pk, modifiers=create_default_modifiers_for_team(team))
            context = ClairQLContext(team_id=team.pk, team=team, database=database)
            result = DatabaseSchemaQueryResponse(tables=serialize_database(context))
        else:
            raise ValidationError(f"Unsupported query kind: {query.__class__.__name__}")
    else:  # Query runner available - it will handle execution as well as caching
        if dashboard_filters:
            query_runner.apply_dashboard_filters(dashboard_filters)
        result = query_runner.run(
            execution_mode=execution_mode,
            user=user,
            query_id=query_id,
            insight_id=insight_id,
            dashboard_id=dashboard_id,
        )

    return result
