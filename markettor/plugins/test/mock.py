import base64
import json
from typing import cast

# This method will be used by the mock to replace requests.get
from markettor.plugins.utils import get_file_from_zip_archive, put_json_into_zip_archive

from .plugin_archives import (
    HELLO_WORLD_PLUGIN_GITHUB_ATTACHMENT_ZIP,
    HELLO_WORLD_PLUGIN_GITHUB_SUBDIR_ZIP,
    HELLO_WORLD_PLUGIN_GITHUB_ZIP,
    HELLO_WORLD_PLUGIN_GITLAB_ZIP,
    HELLO_WORLD_PLUGIN_NPM_TGZ,
    HELLO_WORLD_PLUGIN_SECRET_GITHUB_ZIP,
)


def mocked_plugin_requests_get(*args, **kwargs):
    class MockJSONResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def ok(self):
            return self.status_code < 300

    class MockTextResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

        def ok(self):
            return self.status_code < 300

    class MockBase64Response:
        def __init__(self, base64_data, status_code):
            self.content = base64.b64decode(base64_data)
            self.status_code = status_code

        def ok(self):
            return self.status_code < 300

    if args[0] == "https://api.github.com/repos/MarketTor/markettor/commits?sha=&path=":
        return MockJSONResponse(
            [
                {
                    "sha": "MOCKLATESTCOMMIT",
                    "html_url": "https://www.github.com/MarketTor/markettor/commit/MOCKLATESTCOMMIT",
                }
            ],
            200,
        )

    if args[0] == "https://api.github.com/repos/MarketTor/markettor/commits?sha=main&path=":
        return MockJSONResponse(
            [
                {
                    "sha": "MOCKLATESTCOMMIT",
                    "html_url": "https://www.github.com/MarketTor/markettor/commit/MOCKLATESTCOMMIT",
                }
            ],
            200,
        )

    if args[0] == "https://api.github.com/repos/MarketTor/markettor/commits?sha=main&path=test/path/in/repo":
        return MockJSONResponse(
            [
                {
                    "sha": "MOCKLATESTCOMMIT",
                    "html_url": "https://www.github.com/MarketTor/markettor/commit/MOCKLATESTCOMMIT",
                }
            ],
            200,
        )

    if args[0] == "https://api.github.com/repos/MarketTor/helloworldplugin/commits?sha=&path=":
        return MockJSONResponse(
            [
                {
                    "sha": HELLO_WORLD_PLUGIN_GITHUB_ZIP[0],
                    "html_url": "https://www.github.com/MarketTor/helloworldplugin/commit/{}".format(
                        HELLO_WORLD_PLUGIN_GITHUB_ZIP[0]
                    ),
                }
            ],
            200,
        )

    if args[0] == "https://api.github.com/repos/MarketTor/helloworldplugin/commits?sha=main&path=":
        return MockJSONResponse(
            {"commit": {"sha": HELLO_WORLD_PLUGIN_GITHUB_ZIP[0]}},
            200,
        )

    if args[0].startswith("https://gitlab.com/api/v4/projects/mariusandra%2Fhelloworldplugin/repository/commits"):
        return MockJSONResponse(
            [
                {
                    "id": "ff78cbe1d70316055c610a962a8355a4616d874b",
                    "web_url": "https://gitlab.com/mariusandra/helloworldplugin/-/commit/ff78cbe1d70316055c610a962a8355a4616d874b",
                }
            ],
            200,
        )

    if args[0].startswith("https://gitlab.com/api/v4/projects/mariusandra%2Fhelloworldplugin-other/repository/commits"):
        return MockJSONResponse(
            [
                {
                    "id": "ff78cbe1d70316055c610a962a8355a4616d874b",
                    "web_url": "https://gitlab.com/mariusandra/helloworldplugin-other/-/commit/ff78cbe1d70316055c610a962a8355a4616d874b",
                }
            ],
            200,
        )

    if args[0] == "https://registry.npmjs.org/markettor-helloworld-plugin/latest":
        return MockJSONResponse({"pkg": "markettor-helloworld-plugin", "version": "MOCK"}, 200)

    if args[0] == "https://registry.npmjs.org/@markettor/helloworldplugin/latest":
        return MockJSONResponse({"pkg": "@markettor/helloworldplugin", "version": "MOCK"}, 200)

    if args[0] == "https://github.com/MarketTor/helloworldplugin/archive/{}.zip".format(HELLO_WORLD_PLUGIN_GITHUB_ZIP[0]):
        return MockBase64Response(HELLO_WORLD_PLUGIN_GITHUB_ZIP[1], 200)

    if args[0] == "https://github.com/MarketTor/helloworldplugin/archive/{}.zip".format(
        HELLO_WORLD_PLUGIN_GITHUB_ATTACHMENT_ZIP[0]
    ):
        return MockBase64Response(HELLO_WORLD_PLUGIN_GITHUB_ATTACHMENT_ZIP[1], 200)

    if args[0] == "https://github.com/MarketTor/helloworldplugin/archive/{}.zip".format(
        HELLO_WORLD_PLUGIN_SECRET_GITHUB_ZIP[0]
    ):
        return MockBase64Response(HELLO_WORLD_PLUGIN_SECRET_GITHUB_ZIP[1], 200)

    if args[0] == "https://github.com/MarketTor/helloworldplugin/archive/{}.zip".format(
        HELLO_WORLD_PLUGIN_GITHUB_SUBDIR_ZIP[0]
    ):
        return MockBase64Response(HELLO_WORLD_PLUGIN_GITHUB_SUBDIR_ZIP[1], 200)

    # https://github.com/markettor-plugin/version-equals/commit/{vesrion}
    # https://github.com/markettor-plugin/version-greater-than/commit/{vesrion}
    # https://github.com/markettor-plugin/version-less-than/commit/{vesrion}
    if args[0].startswith(f"https://github.com/markettor-plugin/version-"):
        url_repo = args[0].split("/")[4]
        url_version = args[0].split("/")[6].split(".zip")[0]

        archive = base64.b64decode(HELLO_WORLD_PLUGIN_GITHUB_ZIP[1])
        plugin_json = cast(dict, get_file_from_zip_archive(archive, "plugin.json", json_parse=True))
        plugin_json["markettorVersion"] = url_version

        if url_repo == "version-greater-than":
            plugin_json["markettorVersion"] = f">= {plugin_json['markettorVersion']}"

        if url_repo == "version-less-than":
            plugin_json["markettorVersion"] = f"< {plugin_json['markettorVersion']}"

        archive = put_json_into_zip_archive(archive, plugin_json, "plugin.json")
        return MockBase64Response(base64.b64encode(archive), 200)

    if args[0].startswith(
        "https://gitlab.com/api/v4/projects/mariusandra%2Fhelloworldplugin/repository/archive.zip?sha={}".format(
            HELLO_WORLD_PLUGIN_GITLAB_ZIP[0]
        )
    ) or args[0].startswith(
        "https://gitlab.com/api/v4/projects/mariusandra%2Fhelloworldplugin-other/repository/archive.zip?sha={}".format(
            HELLO_WORLD_PLUGIN_GITLAB_ZIP[0]
        )
    ):
        return MockBase64Response(HELLO_WORLD_PLUGIN_GITLAB_ZIP[1], 200)

    if args[0] == "https://registry.npmjs.org/@markettor/helloworldplugin/-/helloworldplugin-0.0.0.tgz":
        return MockBase64Response(HELLO_WORLD_PLUGIN_NPM_TGZ[1], 200)

    if args[0] == "https://registry.npmjs.org/markettor-helloworld-plugin/-/markettor-helloworld-plugin-0.0.0.tgz":
        return MockBase64Response(HELLO_WORLD_PLUGIN_NPM_TGZ[1], 200)

    if args[0] == "https://raw.githubusercontent.com/MarketTor/integrations-repository/main/plugins.json":
        return MockTextResponse(
            json.dumps(
                [
                    {
                        "name": "markettor-currency-normalization-plugin",
                        "url": "https://github.com/MarketTor/markettor-currency-normalization-plugin",
                        "description": "Normalise monerary values into a base currency",
                        "icon": "https://raw.githubusercontent.com/markettor/markettor-currency-normalization-plugin/main/logo.png",
                        "verified": False,
                        "maintainer": "official",
                    },
                    {
                        "name": "helloworldplugin",
                        "url": "https://github.com/markettor/helloworldplugin",
                        "description": "Greet the World and Foo a Bar",
                        "icon": "https://raw.githubusercontent.com/markettor/helloworldplugin/main/logo.png",
                        "verified": True,
                        "maintainer": "community",
                    },
                ]
            ),
            200,
        )

    return MockJSONResponse(None, 404)
