from inline_snapshot import snapshot
from markettor.cdp.templates.helpers import BaseHogFunctionTemplateTest
from markettor.cdp.templates.webhook.template_webhook import template as template_webhook


class TestTemplateWebhook(BaseHogFunctionTemplateTest):
    template = template_webhook

    def test_function_works(self):
        self.run_function(
            inputs={
                "url": "https://markettor.com",
                "method": "GET",
                "headers": {},
                "body": {"hello": "world"},
                "debug": False,
            }
        )

        assert self.get_mock_fetch_calls()[0] == snapshot(
            ("https://markettor.com", {"headers": {}, "body": {"hello": "world"}, "method": "GET"})
        )
        assert self.get_mock_print_calls() == snapshot([])

    def test_prints_when_debugging(self):
        self.run_function(
            inputs={
                "url": "https://markettor.com",
                "method": "GET",
                "headers": {},
                "body": {"hello": "world"},
                "debug": True,
            }
        )

        assert self.get_mock_fetch_calls()[0] == snapshot(
            ("https://markettor.com", {"headers": {}, "body": {"hello": "world"}, "method": "GET"})
        )
        assert self.get_mock_print_calls() == snapshot([("Response", 200, {})])
