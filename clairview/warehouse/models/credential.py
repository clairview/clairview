from django.db import models

from clairview.helpers.encrypted_fields import EncryptedTextField
from clairview.models.team import Team
from clairview.models.utils import CreatedMetaFields, UUIDModel, sane_repr
from clairview.warehouse.util import database_sync_to_async


class DataWarehouseCredential(CreatedMetaFields, UUIDModel):
    access_key = EncryptedTextField(max_length=500)
    access_secret = EncryptedTextField(max_length=500)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    __repr__ = sane_repr("access_key")


@database_sync_to_async
def aget_or_create_datawarehouse_credential(team_id, access_key, access_secret) -> DataWarehouseCredential:
    return get_or_create_datawarehouse_credential(team_id, access_key, access_secret)


def get_or_create_datawarehouse_credential(team_id, access_key, access_secret) -> DataWarehouseCredential:
    credential, _ = DataWarehouseCredential.objects.get_or_create(
        team_id=team_id, access_key=access_key, access_secret=access_secret
    )

    return credential