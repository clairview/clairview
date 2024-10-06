from markettor.clickhouse.client.migration_tools import run_sql_with_exceptions
from markettor.models.person.sql import CREATE_PERSON_DISTINCT_ID_OVERRIDES_DICTIONARY

operations = [
    run_sql_with_exceptions(CREATE_PERSON_DISTINCT_ID_OVERRIDES_DICTIONARY),
]
