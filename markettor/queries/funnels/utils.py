from markettor.constants import FunnelOrderType
from markettor.models.filters import Filter
from markettor.queries.funnels import ClickhouseFunnelBase


def get_funnel_order_class(filter: Filter) -> type[ClickhouseFunnelBase]:
    from markettor.queries.funnels import (
        ClickhouseFunnel,
        ClickhouseFunnelStrict,
        ClickhouseFunnelUnordered,
    )

    if filter.funnel_order_type == FunnelOrderType.UNORDERED:
        return ClickhouseFunnelUnordered
    elif filter.funnel_order_type == FunnelOrderType.STRICT:
        return ClickhouseFunnelStrict
    return ClickhouseFunnel


def get_funnel_order_actor_class(filter: Filter):
    from markettor.queries.funnels import (
        ClickhouseFunnelActors,
        ClickhouseFunnelStrictActors,
        ClickhouseFunnelUnorderedActors,
    )

    if filter.funnel_order_type == FunnelOrderType.UNORDERED:
        return ClickhouseFunnelUnorderedActors
    elif filter.funnel_order_type == FunnelOrderType.STRICT:
        return ClickhouseFunnelStrictActors
    return ClickhouseFunnelActors
