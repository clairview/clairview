import clairviewanalytics
from celery import shared_task

from clairview.models import User


@shared_task(ignore_result=True)
def identify_task(user_id: int) -> None:
    user = User.objects.get(id=user_id)
    clairviewanalytics.capture(
        user.distinct_id,
        "update user properties",
        {"$set": user.get_analytics_metadata()},
    )
