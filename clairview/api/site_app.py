import json

from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from sentry_sdk import capture_exception
from statshog.defaults.django import statsd

from clairview.exceptions import generate_exception_response
from clairview.logging.timing import timed
from clairview.plugins.site import get_site_config_from_schema, get_transpiled_site_source


@csrf_exempt
@timed("clairview_cloud_site_app_endpoint")
def get_site_app(request: HttpRequest, id: int, token: str, hash: str) -> HttpResponse:
    try:
        source_file = get_transpiled_site_source(id, token) if token else None
        if not source_file:
            raise Exception("No source file found")

        id = source_file.id
        source = source_file.source
        config = get_site_config_from_schema(source_file.config_schema, source_file.config)
        response = f"{source}().inject({{config:{json.dumps(config)},clairview:window['__$$ph_site_app_{id}']}})"

        statsd.incr(f"clairview_cloud_raw_endpoint_success", tags={"endpoint": "site_app"})
        return HttpResponse(content=response, content_type="application/javascript")
    except Exception as e:
        capture_exception(e, {"data": {"id": id, "token": token}})
        statsd.incr("clairview_cloud_raw_endpoint_failure", tags={"endpoint": "site_app"})
        return generate_exception_response(
            "site_app",
            "Unable to serve site app source code.",
            code="missing_site_app_source",
            type="server_error",
            status_code=status.HTTP_404_NOT_FOUND,
        )