from typing import Any, Optional, cast
from unittest.mock import MagicMock
from clairview.cdp.templates.hog_function_template import HogFunctionTemplate
from clairview.cdp.validation import compile_hog
from clairview.test.base import BaseTest
from clairvm.python.execute import execute_bytecode


class BaseHogFunctionTemplateTest(BaseTest):
    template: HogFunctionTemplate
    compiled_hog: Any
    mock_fetch = MagicMock()
    mock_print = MagicMock()
    mock_clairview_capture = MagicMock()

    def setUp(self):
        super().setUp()
        self.compiled_hog = compile_hog(self.template.hog, supported_functions={"fetch", "print", "clairViewCapture"})

        self.mock_print = MagicMock(side_effect=lambda *args: print("[DEBUG HogFunctionPrint]", *args))  # noqa: T201
        # Side effect - log the fetch call and return  with sensible output
        self.mock_fetch = MagicMock(
            side_effect=lambda *args: print("[DEBUG HogFunctionFetch]", *args) or self.mock_fetch_response(*args)  # noqa: T201
        )
        self.mock_clairview_capture = MagicMock(
            side_effect=lambda *args: print("[DEBUG HogFunctionClairviewCapture]", *args)  # noqa: T201
        )

    mock_fetch_response = lambda *args: {"status": 200, "body": {}}

    def get_mock_fetch_calls(self):
        # Return a simple array which is easier to debug
        return [call.args for call in self.mock_fetch.mock_calls]

    def get_mock_print_calls(self):
        # Return a simple array which is easier to debug
        return [call.args for call in self.mock_print.mock_calls]

    def get_mock_clairview_capture_calls(self):
        # Return a simple array which is easier to debug
        return [call.args for call in self.mock_clairview_capture.mock_calls]

    def createHogGlobals(self, globals=None) -> dict:
        # Return an object simulating the
        data = {
            "event": {
                "uuid": "event-id",
                "event": "event-name",
                "name": "event-name",
                "distinct_id": "distinct-id",
                "properties": {"$current_url": "https://example.com"},
                "timestamp": "2024-01-01T00:00:00Z",
                "elements_chain": "",
            },
            "person": {"id": "person-id", "properties": {"email": "example@clairview.com"}},
            "source": {"url": "https://us.clairview.com/hog_functions/1234"},
        }

        if globals:
            if globals.get("event"):
                cast(dict, data["event"]).update(globals["event"])
            if globals.get("person"):
                cast(dict, data["person"]).update(globals["person"])

        return data

    def run_function(self, inputs: dict, globals=None, functions: Optional[dict] = None):
        self.mock_fetch.reset_mock()
        self.mock_print.reset_mock()
        # Create the globals object
        globals = self.createHogGlobals(globals)
        globals["inputs"] = inputs

        # Run the function

        final_functions: dict = {
            "fetch": self.mock_fetch,
            "print": self.mock_print,
            "clairViewCapture": self.mock_clairview_capture,
        }

        if functions:
            final_functions.update(functions)

        return execute_bytecode(
            self.compiled_hog,
            globals,
            functions=final_functions,
        )
