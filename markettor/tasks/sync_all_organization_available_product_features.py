from collections.abc import Sequence
from typing import cast

from markettor.models.organization import Organization


def sync_all_organization_available_product_features() -> None:
    for organization in cast(Sequence[Organization], Organization.objects.all().only("id")):
        organization.update_available_product_features()
        organization.save(update_fields=["available_product_features"])
