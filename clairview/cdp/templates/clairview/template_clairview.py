import dataclasses
from copy import deepcopy

from clairview.cdp.templates.hog_function_template import HogFunctionTemplate, HogFunctionTemplateMigrator
from clairview.clairql.escape_sql import escape_clairql_string

template: HogFunctionTemplate = HogFunctionTemplate(
    status="beta",
    id="template-clairview-replicator",
    name="ClairView",
    description="Send a copy of the incoming data in realtime to another ClairView instance",
    icon_url="/static/clairview-icon.svg",
    category=["Custom", "Analytics"],
    hog="""
let host := inputs.host
let token := inputs.token
let include_all_properties := inputs.include_all_properties
let propertyOverrides := inputs.properties
let properties := include_all_properties ? event.properties : {}

for (let key, value in propertyOverrides) {
    properties[key] := value
}

fetch(f'{host}/e', {
    'method': 'POST',
    'headers': {
        'Content-Type': 'application/json'
    },
    'body': {
        'token': token,
        'event': event.event,
        'timestamp': event.timestamp,
        'distinct_id': event.distinct_id,
        'elements_chain': event.elements_chain,
        'properties': properties
    }
})
""".strip(),
    inputs_schema=[
        {
            "key": "host",
            "type": "string",
            "label": "ClairView host",
            "description": "For cloud accounts this is either https://us.i.clairview.com or https://eu.i.clairview.com",
            "default": "https://us.i.clairview.com",
            "secret": False,
            "required": True,
        },
        {
            "key": "token",
            "type": "string",
            "label": "ClairView API key",
            "secret": False,
            "required": True,
        },
        {
            "key": "include_all_properties",
            "type": "boolean",
            "label": "Include all properties by default",
            "description": "If set, all event properties will be included in the payload. Individual properties can be overridden below.",
            "default": True,
            "secret": False,
            "required": True,
        },
        {
            "key": "properties",
            "type": "dictionary",
            "label": "Property overrides",
            "description": "Provided values will override the event properties.",
            "default": {},
            "secret": False,
            "required": False,
        },
    ],
)


class TemplateClairViewMigrator(HogFunctionTemplateMigrator):
    plugin_url = "https://github.com/ClairView/clairview-plugin-replicator"

    @classmethod
    def migrate(cls, obj):
        hf = deepcopy(dataclasses.asdict(template))

        host = obj.config.get("host", "")
        project_api_key = obj.config.get("project_api_key", "")
        # replication = obj.config.get("replication", "") # not used
        events_to_ignore = [x.strip() for x in obj.config.get("events_to_ignore", "").split(",") if x]
        disable_geoip = obj.config.get("disable_geoip", "No") == "Yes"

        hf["inputs"] = {
            "host": {"value": host},
            "token": {"value": project_api_key},
            "include_all_properties": {"value": True},
            "properties": {"value": {"$geoip_disable": True} if disable_geoip else {}},
        }

        hf["filters"] = {}
        if events_to_ignore:
            event_names = ", ".join([escape_clairql_string(event) for event in events_to_ignore])
            hf["filters"]["events"] = [
                {
                    "id": None,
                    "name": "All events",
                    "type": "events",
                    "order": 0,
                    "properties": [{"type": "clairql", "key": f"event not in ({event_names})"}],
                }
            ]

        return hf
