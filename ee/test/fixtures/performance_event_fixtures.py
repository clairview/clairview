import uuid
from datetime import datetime
from typing import Optional

from markettor.kafka_client.client import ClickhouseProducer
from markettor.kafka_client.topics import KAFKA_PERFORMANCE_EVENTS
from markettor.models.performance.sql import PERFORMANCE_EVENT_DATA_TABLE
from markettor.utils import cast_timestamp_or_now


def create_performance_event(
    team_id: int,
    distinct_id: str,
    session_id: str,
    window_id: str = "window_1",
    current_url: str = "https://markettor.com",
    timestamp: Optional[datetime] = None,
    entry_type="resource",
    **kwargs,
) -> str:
    timestamp_str = cast_timestamp_or_now(timestamp)

    data = {
        "uuid": str(uuid.uuid4()),
        "team_id": team_id,
        "distinct_id": distinct_id,
        "session_id": session_id,
        "window_id": window_id,
        "pageview_id": window_id,
        "current_url": current_url,
        "timestamp": timestamp_str,
        "entry_type": entry_type,
        "name": "https://markettor.com/static/js/1.0.0/MarketTor.js",
    }

    data.update(kwargs)

    selects = [f"%({x})s" for x in data.keys()]
    sql = f"""
INSERT INTO {PERFORMANCE_EVENT_DATA_TABLE()} ({', '.join(data.keys()) }, _timestamp, _offset)
SELECT {', '.join(selects) }, now(), 0
"""

    p = ClickhouseProducer()
    p.produce(sql=sql, topic=KAFKA_PERFORMANCE_EVENTS, data=data)

    return str(uuid)
