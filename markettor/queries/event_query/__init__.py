from markettor.settings import EE_AVAILABLE

if EE_AVAILABLE:
    from ee.clickhouse.queries.event_query import EnterpriseEventQuery as EventQuery
else:
    from markettor.queries.event_query.event_query import EventQuery  # type: ignore
