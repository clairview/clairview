from django.db import models

from clairview.models.utils import UUIDModel


class NotificationViewed(UUIDModel):
    user = models.ForeignKey("clairview.User", null=True, on_delete=models.SET_NULL)
    # when viewing notifications made by viewing the activity log we count unread notifications
    # as any after the last viewed date
    last_viewed_activity_date = models.DateTimeField(default=None)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user"], name="clairview_user_unique_viewed_date")]
