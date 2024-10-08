from datetime import datetime
from typing import Any

from zoneinfo import ZoneInfo

from clairview.models.subscription import Subscription


def create_subscription(**kwargs: Any) -> Subscription:
    payload = {
        "target_type": "email",
        "target_value": "test1@clairview.com,test2@clairview.com",
        "frequency": "daily",
        "interval": 1,
        "start_date": datetime(2022, 1, 1, 9, 0).replace(tzinfo=ZoneInfo("UTC")),
    }

    payload.update(kwargs)
    return Subscription.objects.create(**payload)
