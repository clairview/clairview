import json
import re
import uuid

from django.http import JsonResponse, StreamingHttpResponse
from drf_spectacular.utils import OpenApiResponse
from pydantic import BaseModel
from rest_framework import status, viewsets
from rest_framework.exceptions import NotAuthenticated, ValidationError
from rest_framework.renderers import BaseRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from sentry_sdk import capture_exception, set_tag

from ee.hogai.generate_trends_agent import Conversation, GenerateTrendsAgent
from clairview.api.documentation import extend_schema
from clairview.api.mixins import PydanticModelMixin
from clairview.api.monitoring import Feature, monitor
from clairview.api.routing import TeamAndOrgViewSetMixin
from clairview.api.services.query import process_query_model
from clairview.api.utils import action
from clairview.clickhouse.client.execute_async import (
    cancel_query,
    get_query_status,
)
from clairview.clickhouse.query_tagging import tag_queries
from clairview.errors import ExposedCHQueryError
from clairview.event_usage import report_user_action
from clairview.clairql.ai import PromptUnclear, write_sql_from_prompt
from clairview.clairql.errors import ExposedClairQLError
from clairview.clairql_queries.apply_dashboard_filters import apply_dashboard_filters_to_dict
from clairview.clairql_queries.query_runner import ExecutionMode, execution_mode_from_refresh
from clairview.models.user import User
from clairview.rate_limit import (
    AIBurstRateThrottle,
    AISustainedRateThrottle,
    ClairQLQueryThrottle,
    ClickHouseBurstRateThrottle,
    ClickHouseSustainedRateThrottle,
)
from clairview.schema import QueryRequest, QueryResponseAlternative, QueryStatusResponse


class ServerSentEventRenderer(BaseRenderer):
    media_type = "text/event-stream"
    format = "txt"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class QueryViewSet(TeamAndOrgViewSetMixin, PydanticModelMixin, viewsets.ViewSet):
    # NOTE: Do we need to override the scopes for the "create"
    scope_object = "query"
    # Special case for query - these are all essentially read actions
    scope_object_read_actions = ["retrieve", "create", "list", "destroy"]
    scope_object_write_actions: list[str] = []
    sharing_enabled_actions = ["retrieve"]

    def get_throttles(self):
        if self.action in ("draft_sql", "chat"):
            return [AIBurstRateThrottle(), AISustainedRateThrottle()]
        if query := self.request.data.get("query"):
            if isinstance(query, dict) and query.get("kind") == "ClairQLQuery":
                return [ClairQLQueryThrottle()]
        return [ClickHouseBurstRateThrottle(), ClickHouseSustainedRateThrottle()]

    @extend_schema(
        request=QueryRequest,
        responses={
            200: QueryResponseAlternative,
        },
    )
    @monitor(feature=Feature.QUERY, endpoint="query", method="POST")
    def create(self, request, *args, **kwargs) -> Response:
        data = self.get_model(request.data, QueryRequest)
        if data.filters_override is not None:
            data.query = apply_dashboard_filters_to_dict(
                data.query.model_dump(), data.filters_override.model_dump(), self.team
            )  # type: ignore

        client_query_id = data.client_query_id or uuid.uuid4().hex
        execution_mode = execution_mode_from_refresh(data.refresh)
        response_status: int = status.HTTP_200_OK

        self._tag_client_query_id(client_query_id)

        if data.async_:  # TODO: Legacy async, use "refresh=async" instead
            execution_mode = ExecutionMode.RECENT_CACHE_CALCULATE_ASYNC_IF_STALE

        if execution_mode == execution_mode.CACHE_ONLY_NEVER_CALCULATE:
            # Here in query endpoint we always want to calculate if the cache is stale
            execution_mode = ExecutionMode.RECENT_CACHE_CALCULATE_BLOCKING_IF_STALE

        tag_queries(query=request.data["query"])
        try:
            result = process_query_model(
                self.team,
                data.query,
                execution_mode=execution_mode,
                query_id=client_query_id,
                user=request.user,
            )
            if isinstance(result, BaseModel):
                result = result.model_dump(by_alias=True)
            if result.get("query_status") and result["query_status"].get("complete") is False:
                response_status = status.HTTP_202_ACCEPTED
            return Response(result, status=response_status)
        except (ExposedClairQLError, ExposedCHQueryError) as e:
            raise ValidationError(str(e), getattr(e, "code_name", None))
        except Exception as e:
            self.handle_column_ch_error(e)
            capture_exception(e)
            raise

    @extend_schema(
        description="(Experimental)",
        responses={200: QueryStatusResponse},
    )
    @monitor(feature=Feature.QUERY, endpoint="query", method="GET")
    def retrieve(self, request: Request, pk=None, *args, **kwargs) -> JsonResponse:
        show_progress: bool = request.query_params.get("show_progress", False) == "true"
        show_progress = (
            show_progress or request.query_params.get("showProgress", False) == "true"
        )  # TODO: Remove this once we have a consistent naming convention
        query_status = get_query_status(team_id=self.team.pk, query_id=pk, show_progress=show_progress)
        query_status_response = QueryStatusResponse(query_status=query_status)

        http_code: int = status.HTTP_202_ACCEPTED
        if query_status.error:
            if query_status.error_message:
                http_code = status.HTTP_400_BAD_REQUEST  # An error where a user can likely take an action to resolve it
            else:
                http_code = status.HTTP_500_INTERNAL_SERVER_ERROR  # An internal surprise
        elif query_status.complete:
            http_code = status.HTTP_200_OK

        return JsonResponse(query_status_response.model_dump(), safe=False, status=http_code)

    @extend_schema(
        description="(Experimental)",
        responses={
            204: OpenApiResponse(description="Query cancelled"),
        },
    )
    @monitor(feature=Feature.QUERY, endpoint="query", method="DELETE")
    def destroy(self, request, pk=None, *args, **kwargs):
        cancel_query(self.team.pk, pk)
        return Response(status=204)

    @action(methods=["GET"], detail=False)
    def draft_sql(self, request: Request, *args, **kwargs) -> Response:
        if not isinstance(request.user, User):
            raise NotAuthenticated()
        prompt = request.GET.get("prompt")
        current_query = request.GET.get("current_query")
        if not prompt:
            raise ValidationError({"prompt": ["This field is required."]}, code="required")
        if len(prompt) > 400:
            raise ValidationError({"prompt": ["This field is too long."]}, code="too_long")
        try:
            result = write_sql_from_prompt(prompt, current_query=current_query, user=request.user, team=self.team)
        except PromptUnclear as e:
            raise ValidationError({"prompt": [str(e)]}, code="unclear")
        return Response({"sql": result})

    @action(detail=False, methods=["POST"], renderer_classes=[ServerSentEventRenderer])
    def chat(self, request: Request, *args, **kwargs):
        assert request.user is not None
        validated_body = Conversation.model_validate(request.data)
        chain = GenerateTrendsAgent(self.team).bootstrap(validated_body.messages)

        def generate():
            last_message = None
            for message in chain.stream({"question": validated_body.messages[0].content}):
                if message:
                    last_message = message[0].model_dump_json()
                    yield last_message

            if not last_message:
                yield json.dumps({"reasoning_steps": ["Schema validation failed"]})

            report_user_action(
                request.user,  # type: ignore
                "chat with ai",
                {"prompt": validated_body.messages[-1].content, "response": last_message},
            )

        return StreamingHttpResponse(generate(), content_type=ServerSentEventRenderer.media_type)

    def handle_column_ch_error(self, error):
        if getattr(error, "message", None):
            match = re.search(r"There's no column.*in table", error.message)
            if match:
                # TODO: remove once we support all column types
                raise ValidationError(
                    match.group(0) + ". Note: While in beta, not all column types may be fully supported"
                )
        return

    def _tag_client_query_id(self, query_id: str | None):
        if query_id is None:
            return

        tag_queries(client_query_id=query_id)
        set_tag("client_query_id", query_id)
