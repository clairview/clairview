from inline_snapshot import snapshot
from clairview.cdp.templates.helpers import BaseHogFunctionTemplateTest
from clairview.cdp.templates.activecampaign.template_activecampaign import (
    template as template_activecampaign,
)


def create_inputs(**kwargs):
    inputs = {
        "accountName": "clairview",
        "apiKey": "API_KEY",
        "email": "max@clairview.com",
        "firstName": "max",
        "attributes": {"1": "ClairView", "2": "clairview.com"},
    }
    inputs.update(kwargs)

    return inputs


class TestTemplateActiveCampaign(BaseHogFunctionTemplateTest):
    template = template_activecampaign

    def test_function_works(self):
        self.run_function(
            inputs=create_inputs(),
            globals={
                "event": {"event": "$identify"},
            },
        )

        assert self.get_mock_fetch_calls()[0] == snapshot(
            (
                "https://clairview.api-us1.com/api/3/contact/sync",
                {
                    "method": "POST",
                    "headers": {
                        "content-type": "application/json",
                        "Api-Token": "API_KEY",
                    },
                    "body": {
                        "contact": {
                            "email": "max@clairview.com",
                            "firstName": "max",
                            "fieldValues": [{"field": "1", "value": "ClairView"}, {"field": "2", "value": "clairview.com"}],
                        }
                    },
                },
            )
        )

    def test_function_requires_identifier(self):
        self.run_function(inputs=create_inputs(email=""))

        assert not self.get_mock_fetch_calls()
        assert self.get_mock_print_calls() == snapshot([("`email` input is empty. Not creating a contact.",)])
