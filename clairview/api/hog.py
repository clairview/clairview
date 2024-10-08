from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from clairview.api.mixins import PydanticModelMixin
from clairview.api.routing import TeamAndOrgViewSetMixin
from clairview.cdp.validation import compile_hog
from clairview.schema import HogCompileResponse


class HogViewSet(TeamAndOrgViewSetMixin, PydanticModelMixin, viewsets.ViewSet):
    scope_object = "INTERNAL"

    def create(self, request, *args, **kwargs) -> Response:
        hog = request.data.get("hog")
        bytecode = compile_hog(hog)

        return Response(HogCompileResponse(bytecode=bytecode).model_dump(), status=status.HTTP_200_OK)
