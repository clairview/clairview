from django.db import models
from markettor.models import Organization
from markettor.models.utils import UUIDModel


class ProxyRecord(UUIDModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="proxy_records")
    domain = models.CharField(max_length=64, unique=True)
    target_cname = models.CharField(max_length=256, null=False)
    message = models.CharField(max_length=1024, null=True)

    class Status(models.TextChoices):
        WAITING = "waiting"
        ISSUING = "issuing"
        VALID = "valid"
        ERRORING = "erroring"
        DELETING = "deleting"
        TIMED_OUT = "timed_out"

    status = models.CharField(
        choices=Status.choices,
        default=Status.WAITING,
    )

    created_by = models.ForeignKey(
        "markettor.User",
        on_delete=models.SET_NULL,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
