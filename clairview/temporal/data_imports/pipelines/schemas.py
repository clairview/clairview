from clairview.warehouse.types import IncrementalField
from clairview.temporal.data_imports.pipelines.zendesk.settings import (
    BASE_ENDPOINTS,
    SUPPORT_ENDPOINTS,
    INCREMENTAL_ENDPOINTS as ZENDESK_INCREMENTAL_ENDPOINTS,
    INCREMENTAL_FIELDS as ZENDESK_INCREMENTAL_FIELDS,
)
from clairview.warehouse.models import ExternalDataSource
from clairview.temporal.data_imports.pipelines.stripe.settings import (
    ENDPOINTS as STRIPE_ENDPOINTS,
    INCREMENTAL_ENDPOINTS as STRIPE_INCREMENTAL_ENDPOINTS,
    INCREMENTAL_FIELDS as STRIPE_INCREMENTAL_FIELDS,
)
from clairview.temporal.data_imports.pipelines.hubspot.settings import ENDPOINTS as HUBSPOT_ENDPOINTS
from clairview.temporal.data_imports.pipelines.salesforce.settings import (
    ENDPOINTS as SALESFORCE_ENDPOINTS,
    INCREMENTAL_ENDPOINTS as SALESFORCE_INCREMENTAL_ENDPOINTS,
    INCREMENTAL_FIELDS as SALESFORCE_INCREMENTAL_FIELDS,
)
from clairview.temporal.data_imports.pipelines.vitally.settings import (
    ENDPOINTS as VITALLY_ENDPOINTS,
    INCREMENTAL_ENDPOINTS as VITALLY_INCREMENTAL_ENDPOINTS,
    INCREMENTAL_FIELDS as VITALLY_INCREMENTAL_FIELDS,
)

PIPELINE_TYPE_SCHEMA_DEFAULT_MAPPING = {
    ExternalDataSource.Type.STRIPE: STRIPE_ENDPOINTS,
    ExternalDataSource.Type.HUBSPOT: HUBSPOT_ENDPOINTS,
    ExternalDataSource.Type.ZENDESK: tuple(
        list(BASE_ENDPOINTS) + [resource for resource, endpoint_url, data_key, cursor_paginated in SUPPORT_ENDPOINTS]
    ),
    ExternalDataSource.Type.POSTGRES: (),
    ExternalDataSource.Type.SNOWFLAKE: (),
    ExternalDataSource.Type.SALESFORCE: SALESFORCE_ENDPOINTS,
    ExternalDataSource.Type.MYSQL: (),
    ExternalDataSource.Type.MSSQL: (),
    ExternalDataSource.Type.VITALLY: VITALLY_ENDPOINTS,
    ExternalDataSource.Type.BIGQUERY: (),
}

PIPELINE_TYPE_INCREMENTAL_ENDPOINTS_MAPPING = {
    ExternalDataSource.Type.STRIPE: STRIPE_INCREMENTAL_ENDPOINTS,
    ExternalDataSource.Type.HUBSPOT: (),
    ExternalDataSource.Type.ZENDESK: ZENDESK_INCREMENTAL_ENDPOINTS,
    ExternalDataSource.Type.POSTGRES: (),
    ExternalDataSource.Type.SNOWFLAKE: (),
    ExternalDataSource.Type.SALESFORCE: SALESFORCE_INCREMENTAL_ENDPOINTS,
    ExternalDataSource.Type.MYSQL: (),
    ExternalDataSource.Type.MSSQL: (),
    ExternalDataSource.Type.VITALLY: VITALLY_INCREMENTAL_ENDPOINTS,
    ExternalDataSource.Type.BIGQUERY: (),
}

PIPELINE_TYPE_INCREMENTAL_FIELDS_MAPPING: dict[ExternalDataSource.Type, dict[str, list[IncrementalField]]] = {
    ExternalDataSource.Type.STRIPE: STRIPE_INCREMENTAL_FIELDS,
    ExternalDataSource.Type.HUBSPOT: {},
    ExternalDataSource.Type.ZENDESK: ZENDESK_INCREMENTAL_FIELDS,
    ExternalDataSource.Type.POSTGRES: {},
    ExternalDataSource.Type.SNOWFLAKE: {},
    ExternalDataSource.Type.SALESFORCE: SALESFORCE_INCREMENTAL_FIELDS,
    ExternalDataSource.Type.MYSQL: {},
    ExternalDataSource.Type.MSSQL: {},
    ExternalDataSource.Type.VITALLY: VITALLY_INCREMENTAL_FIELDS,
    ExternalDataSource.Type.BIGQUERY: {},
}