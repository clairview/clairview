from django.db import models

from clairview.models.team import Team
from clairview.models.utils import sane_repr


class EventProperty(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    event = models.CharField(max_length=400, null=False)
    property = models.CharField(max_length=400, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["team", "event", "property"],
                name="clairview_event_property_unique_team_event_property",
            )
        ]
        indexes = [
            models.Index(fields=["team", "event"]),
            models.Index(fields=["team", "property"]),
        ]

    __repr__ = sane_repr("event", "property", "team_id")
