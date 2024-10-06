import json

from rest_framework import request, response, viewsets
from markettor.api.utils import action
from rest_framework.exceptions import ValidationError

from markettor.api.routing import TeamAndOrgViewSetMixin
from markettor.hogql.database.schema.sessions_v1 import (
    get_lazy_session_table_properties_v1,
    get_lazy_session_table_values_v1,
)
from markettor.hogql.database.schema.sessions_v2 import (
    get_lazy_session_table_values_v2,
    get_lazy_session_table_properties_v2,
)
from markettor.hogql.modifiers import create_default_modifiers_for_team
from markettor.rate_limit import (
    ClickHouseBurstRateThrottle,
    ClickHouseSustainedRateThrottle,
)
from markettor.schema import SessionTableVersion
from markettor.utils import convert_property_value, flatten


class SessionViewSet(
    TeamAndOrgViewSetMixin,
    viewsets.ViewSet,
):
    scope_object = "query"
    throttle_classes = [ClickHouseBurstRateThrottle, ClickHouseSustainedRateThrottle]

    @action(methods=["GET"], detail=False)
    def values(self, request: request.Request, **kwargs) -> response.Response:
        team = self.team

        key = request.GET.get("key")
        search_term = request.GET.get("value")

        if not key:
            raise ValidationError(detail=f"Key not provided")

        modifiers = create_default_modifiers_for_team(team)
        if (
            modifiers.sessionTableVersion == SessionTableVersion.V2
            or modifiers.sessionTableVersion == SessionTableVersion.AUTO
        ):
            result = get_lazy_session_table_values_v2(key, search_term=search_term, team=team)
        else:
            result = get_lazy_session_table_values_v1(key, search_term=search_term, team=team)

        flattened = []
        for value in result:
            try:
                # Try loading as json for dicts or arrays
                flattened.append(json.loads(value[0]))
            except json.decoder.JSONDecodeError:
                flattened.append(value[0])
        return response.Response([{"name": convert_property_value(value)} for value in flatten(flattened)])

    @action(methods=["GET"], detail=False)
    def property_definitions(self, request: request.Request, **kwargs) -> response.Response:
        search = request.GET.get("search")

        # unlike e.g. event properties, there's a very limited number of session properties,
        # so we can just return them all
        modifiers = create_default_modifiers_for_team(self.team)
        if (
            modifiers.sessionTableVersion == SessionTableVersion.V2
            or modifiers.sessionTableVersion == SessionTableVersion.AUTO
        ):
            results = get_lazy_session_table_properties_v2(search)
        else:
            results = get_lazy_session_table_properties_v1(search)
        return response.Response(
            {
                "count": len(results),
                "results": results,
            }
        )
