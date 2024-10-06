from markettor.settings import EE_AVAILABLE

if EE_AVAILABLE:
    from ee.clickhouse.queries.stickiness import ClickhouseStickiness as Stickiness
    from ee.clickhouse.queries.stickiness import (
        ClickhouseStickinessActors as StickinessActors,
    )
else:
    from markettor.queries.stickiness.stickiness import Stickiness  # type: ignore
    from markettor.queries.stickiness.stickiness_actors import StickinessActors  # type: ignore
