from clairview.settings import EE_AVAILABLE

if EE_AVAILABLE:
    from ee.clickhouse.queries.stickiness import ClickhouseStickiness as Stickiness
    from ee.clickhouse.queries.stickiness import (
        ClickhouseStickinessActors as StickinessActors,
    )
else:
    from clairview.queries.stickiness.stickiness import Stickiness  # type: ignore
    from clairview.queries.stickiness.stickiness_actors import StickinessActors  # type: ignore
