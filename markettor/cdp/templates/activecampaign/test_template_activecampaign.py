from inline_snapshot import snapshot
from markettor.cdp.templates.helpers import BaseHogFunctionTemplateTest
from markettor.cdp.templates.activecampaign.template_activecampaign import (
    template as template_activecampaign,
)


def create_inputs(**kwargs):
    inputs = {
        "accountName": "markettor",
        "apiKey": "API_KEY",
        "email": "max@markettor.com",
        "firstName": "max",
        "attributes": {"1": "MarketTor", "2": "markettor.com"},
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
                "https://markettor.api-us1.com/api/3/contact/sync",
                {
                    "method": "POST",
                    "headers": {
                        "content-type": "application/json",
                        "Api-Token": "API_KEY",
                    },
                    "body": {
                        "contact": {
                            "email": "max@markettor.com",
                            "firstName": "max",
                            "fieldValues": [{"field": "1", "value": "MarketTor"}, {"field": "2", "value": "markettor.com"}],
                        }
                    },
                },
            )
        )

    def test_function_requires_identifier(self):
        self.run_function(inputs=create_inputs(email=""))

        assert not self.get_mock_fetch_calls()
        assert self.get_mock_print_calls() == snapshot([("`email` input is empty. Not creating a contact.",)])
