# mypy: disable-error-code="assignment"

from __future__ import annotations

from enum import Enum, StrEnum
from typing import Any, Literal, Optional, Union

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, RootModel


class SchemaRoot(RootModel[Any]):
    root: Any


class MathGroupTypeIndex(float, Enum):
    NUMBER_0 = 0
    NUMBER_1 = 1
    NUMBER_2 = 2
    NUMBER_3 = 3
    NUMBER_4 = 4


class ActionConversionGoal(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    actionId: int


class AggregationAxisFormat(StrEnum):
    NUMERIC = "numeric"
    DURATION = "duration"
    DURATION_MS = "duration_ms"
    PERCENTAGE = "percentage"
    PERCENTAGE_SCALED = "percentage_scaled"


class AlertCalculationInterval(StrEnum):
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class AlertCondition(BaseModel):
    pass
    model_config = ConfigDict(
        extra="forbid",
    )


class AlertState(StrEnum):
    FIRING = "Firing"
    NOT_FIRING = "Not firing"
    ERRORED = "Errored"


class Kind(StrEnum):
    METHOD = "Method"
    FUNCTION = "Function"
    CONSTRUCTOR = "Constructor"
    FIELD = "Field"
    VARIABLE = "Variable"
    CLASS_ = "Class"
    STRUCT = "Struct"
    INTERFACE = "Interface"
    MODULE = "Module"
    PROPERTY = "Property"
    EVENT = "Event"
    OPERATOR = "Operator"
    UNIT = "Unit"
    VALUE = "Value"
    CONSTANT = "Constant"
    ENUM = "Enum"
    ENUM_MEMBER = "EnumMember"
    KEYWORD = "Keyword"
    TEXT = "Text"
    COLOR = "Color"
    FILE = "File"
    REFERENCE = "Reference"
    CUSTOMCOLOR = "Customcolor"
    FOLDER = "Folder"
    TYPE_PARAMETER = "TypeParameter"
    USER = "User"
    ISSUE = "Issue"
    SNIPPET = "Snippet"


class AutocompleteCompletionItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    detail: Optional[str] = Field(
        default=None,
        description=(
            "A human-readable string with additional information about this item, like type or symbol information."
        ),
    )
    documentation: Optional[str] = Field(
        default=None, description="A human-readable string that represents a doc-comment."
    )
    insertText: str = Field(
        ..., description="A string or snippet that should be inserted in a document when selecting this completion."
    )
    kind: Kind = Field(
        ..., description="The kind of this completion item. Based on the kind an icon is chosen by the editor."
    )
    label: str = Field(
        ...,
        description=(
            "The label of this completion item. By default this is also the text that is inserted when selecting this"
            " completion."
        ),
    )


class BaseMathType(StrEnum):
    TOTAL = "total"
    DAU = "dau"
    WEEKLY_ACTIVE = "weekly_active"
    MONTHLY_ACTIVE = "monthly_active"
    UNIQUE_SESSION = "unique_session"
    FIRST_TIME_FOR_USER = "first_time_for_user"


class BreakdownAttributionType(StrEnum):
    FIRST_TOUCH = "first_touch"
    LAST_TOUCH = "last_touch"
    ALL_EVENTS = "all_events"
    STEP = "step"


class BreakdownType(StrEnum):
    COHORT = "cohort"
    PERSON = "person"
    EVENT = "event"
    GROUP = "group"
    SESSION = "session"
    TORQL = "torql"
    DATA_WAREHOUSE = "data_warehouse"
    DATA_WAREHOUSE_PERSON_PROPERTY = "data_warehouse_person_property"


class CompareItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    label: str
    value: str


class IntervalItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    label: str
    value: int = Field(..., description="An interval selected out of available intervals in source query")


class Series(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    label: str
    value: int


class StatusItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    label: str
    value: str


class ChartDisplayType(StrEnum):
    ACTIONS_LINE_GRAPH = "ActionsLineGraph"
    ACTIONS_BAR = "ActionsBar"
    ACTIONS_STACKED_BAR = "ActionsStackedBar"
    ACTIONS_AREA_GRAPH = "ActionsAreaGraph"
    ACTIONS_LINE_GRAPH_CUMULATIVE = "ActionsLineGraphCumulative"
    BOLD_NUMBER = "BoldNumber"
    ACTIONS_PIE = "ActionsPie"
    ACTIONS_BAR_VALUE = "ActionsBarValue"
    ACTIONS_TABLE = "ActionsTable"
    WORLD_MAP = "WorldMap"


class DisplayType(StrEnum):
    AUTO = "auto"
    LINE = "line"
    BAR = "bar"


class YAxisPosition(StrEnum):
    LEFT = "left"
    RIGHT = "right"


class ChartSettingsDisplay(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    displayType: Optional[DisplayType] = None
    label: Optional[str] = None
    trendLine: Optional[bool] = None
    yAxisPosition: Optional[YAxisPosition] = None


class Style(StrEnum):
    NONE = "none"
    NUMBER = "number"
    PERCENT = "percent"


class ChartSettingsFormatting(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    decimalPlaces: Optional[float] = None
    prefix: Optional[str] = None
    style: Optional[Style] = None
    suffix: Optional[str] = None


class ClickhouseQueryProgress(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    active_cpu_time: int
    bytes_read: int
    estimated_rows_total: int
    rows_read: int
    time_elapsed: int


class CompareFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    compare: Optional[bool] = None
    compare_to: Optional[str] = None


class ColorMode(StrEnum):
    LIGHT = "light"
    DARK = "dark"


class ConditionalFormattingRule(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    bytecode: list
    color: str
    colorMode: Optional[ColorMode] = None
    columnName: str
    id: str
    input: str
    templateId: str


class CountPerActorMathType(StrEnum):
    AVG_COUNT_PER_ACTOR = "avg_count_per_actor"
    MIN_COUNT_PER_ACTOR = "min_count_per_actor"
    MAX_COUNT_PER_ACTOR = "max_count_per_actor"
    MEDIAN_COUNT_PER_ACTOR = "median_count_per_actor"
    P90_COUNT_PER_ACTOR = "p90_count_per_actor"
    P95_COUNT_PER_ACTOR = "p95_count_per_actor"
    P99_COUNT_PER_ACTOR = "p99_count_per_actor"


class CustomEventConversionGoal(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    customEventName: str


class DataWarehouseEventsModifier(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    distinct_id_field: str
    id_field: str
    table_name: str
    timestamp_field: str


class DatabaseSchemaSchema(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: str
    incremental: bool
    last_synced_at: Optional[str] = None
    name: str
    should_sync: bool
    status: Optional[str] = None


class DatabaseSchemaSource(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: str
    last_synced_at: Optional[str] = None
    prefix: str
    source_type: str
    status: str


class Type(StrEnum):
    MARKETTOR = "clairview"
    DATA_WAREHOUSE = "data_warehouse"
    VIEW = "view"
    BATCH_EXPORT = "batch_export"
    MATERIALIZED_VIEW = "materialized_view"


class DatabaseSerializedFieldType(StrEnum):
    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"
    DATETIME = "datetime"
    DATE = "date"
    BOOLEAN = "boolean"
    ARRAY = "array"
    JSON = "json"
    LAZY_TABLE = "lazy_table"
    VIRTUAL_TABLE = "virtual_table"
    FIELD_TRAVERSER = "field_traverser"
    EXPRESSION = "expression"
    VIEW = "view"
    MATERIALIZED_VIEW = "materialized_view"


class DateRange(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    explicitDate: Optional[bool] = Field(
        default=False,
        description=(
            "Whether the date_from and date_to should be used verbatim. Disables rounding to the start and end of"
            " period."
        ),
    )


class DatetimeDay(RootModel[AwareDatetime]):
    root: AwareDatetime


class Day(RootModel[int]):
    root: int


class DurationType(StrEnum):
    DURATION = "duration"
    ACTIVE_SECONDS = "active_seconds"
    INACTIVE_SECONDS = "inactive_seconds"


class Key(StrEnum):
    TAG_NAME = "tag_name"
    TEXT = "text"
    HREF = "href"
    SELECTOR = "selector"


class ElementType(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    attr_class: Optional[list[str]] = None
    attr_id: Optional[str] = None
    attributes: dict[str, str]
    href: Optional[str] = None
    nth_child: Optional[float] = None
    nth_of_type: Optional[float] = None
    order: Optional[float] = None
    tag_name: str
    text: Optional[str] = None


class EmptyPropertyFilter(BaseModel):
    pass
    model_config = ConfigDict(
        extra="forbid",
    )


class EntityType(StrEnum):
    ACTIONS = "actions"
    EVENTS = "events"
    DATA_WAREHOUSE = "data_warehouse"
    NEW_ENTITY = "new_entity"


class Status(StrEnum):
    ARCHIVED = "archived"
    ACTIVE = "active"
    RESOLVED = "resolved"
    PENDING_RELEASE = "pending_release"


class ErrorTrackingGroup(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    assignee: Optional[float] = None
    description: Optional[str] = None
    exception_type: Optional[str] = None
    fingerprint: list[str]
    first_seen: AwareDatetime
    last_seen: AwareDatetime
    merged_fingerprints: list[list[str]]
    occurrences: float
    sessions: float
    status: Status
    users: float
    volume: Optional[Any] = None


class Order(StrEnum):
    LAST_SEEN = "last_seen"
    FIRST_SEEN = "first_seen"
    OCCURRENCES = "occurrences"
    USERS = "users"
    SESSIONS = "sessions"


class EventDefinition(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    elements: list
    event: str
    properties: dict[str, Any]


class CorrelationType(StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"


class EventOddsRatioSerialized(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    correlation_type: CorrelationType
    event: EventDefinition
    failure_count: int
    odds_ratio: float
    success_count: int


class Person(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    distinct_ids: list[str]
    is_identified: Optional[bool] = None
    properties: dict[str, Any]


class EventType(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    distinct_id: str
    elements: list[ElementType]
    elements_chain: Optional[str] = None
    event: str
    id: str
    person: Optional[Person] = None
    properties: dict[str, Any]
    timestamp: str
    uuid: Optional[str] = None


class Properties(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    email: Optional[str] = None
    name: Optional[str] = None


class EventsQueryPersonColumn(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    created_at: str
    distinct_id: str
    properties: Properties
    uuid: str


class ExperimentVariantFunnelResult(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    failure_count: float
    key: str
    success_count: float


class ExperimentVariantTrendResult(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    count: float
    exposure: float


class FilterLogicalOperator(StrEnum):
    AND_ = "AND"
    OR_ = "OR"


class FunnelConversionWindowTimeUnit(StrEnum):
    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"


class FunnelCorrelationResult(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    events: list[EventOddsRatioSerialized]
    skewed: bool


class FunnelCorrelationResultsType(StrEnum):
    EVENTS = "events"
    PROPERTIES = "properties"
    EVENT_WITH_PROPERTIES = "event_with_properties"


class FunnelExclusionLegacy(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    custom_name: Optional[str] = None
    funnel_from_step: float
    funnel_to_step: float
    id: Optional[Union[str, float]] = None
    index: Optional[float] = None
    name: Optional[str] = None
    order: Optional[float] = None
    type: Optional[EntityType] = None


class FunnelExclusionSteps(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    funnelFromStep: int
    funnelToStep: int


class FunnelLayout(StrEnum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class FunnelPathType(StrEnum):
    FUNNEL_PATH_BEFORE_STEP = "funnel_path_before_step"
    FUNNEL_PATH_BETWEEN_STEPS = "funnel_path_between_steps"
    FUNNEL_PATH_AFTER_STEP = "funnel_path_after_step"


class FunnelStepReference(StrEnum):
    TOTAL = "total"
    PREVIOUS = "previous"


class FunnelTimeToConvertResults(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    average_conversion_time: Optional[float] = None
    bins: list[list[int]]


class FunnelVizType(StrEnum):
    STEPS = "steps"
    TIME_TO_CONVERT = "time_to_convert"
    TRENDS = "trends"


class GoalLine(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    label: str
    value: float


class HogCompileResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    bytecode: list


class HogLanguage(StrEnum):
    HOG = "hog"
    HOG_JSON = "hogJson"
    HOG_QL = "torQL"
    HOG_QL_EXPR = "torQLExpr"
    HOG_TEMPLATE = "hogTemplate"


class TorQLNotice(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    end: Optional[int] = None
    fix: Optional[str] = None
    message: str
    start: Optional[int] = None


class BounceRatePageViewMode(StrEnum):
    COUNT_PAGEVIEWS = "count_pageviews"
    UNIQ_URLS = "uniq_urls"
    UNIQ_PAGE_SCREEN_AUTOCAPTURES = "uniq_page_screen_autocaptures"


class InCohortVia(StrEnum):
    AUTO = "auto"
    LEFTJOIN = "leftjoin"
    SUBQUERY = "subquery"
    LEFTJOIN_CONJOINED = "leftjoin_conjoined"


class MaterializationMode(StrEnum):
    AUTO = "auto"
    LEGACY_NULL_AS_STRING = "legacy_null_as_string"
    LEGACY_NULL_AS_NULL = "legacy_null_as_null"
    DISABLED = "disabled"


class PersonsArgMaxVersion(StrEnum):
    AUTO = "auto"
    V1 = "v1"
    V2 = "v2"


class PersonsJoinMode(StrEnum):
    INNER = "inner"
    LEFT = "left"


class PersonsOnEventsMode(StrEnum):
    DISABLED = "disabled"
    PERSON_ID_NO_OVERRIDE_PROPERTIES_ON_EVENTS = "person_id_no_override_properties_on_events"
    PERSON_ID_OVERRIDE_PROPERTIES_ON_EVENTS = "person_id_override_properties_on_events"
    PERSON_ID_OVERRIDE_PROPERTIES_JOINED = "person_id_override_properties_joined"


class PropertyGroupsMode(StrEnum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    OPTIMIZED = "optimized"


class SessionTableVersion(StrEnum):
    AUTO = "auto"
    V1 = "v1"
    V2 = "v2"


class TorQLQueryModifiers(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    bounceRatePageViewMode: Optional[BounceRatePageViewMode] = None
    dataWarehouseEventsModifiers: Optional[list[DataWarehouseEventsModifier]] = None
    debug: Optional[bool] = None
    inCohortVia: Optional[InCohortVia] = None
    materializationMode: Optional[MaterializationMode] = None
    optimizeJoinedFilters: Optional[bool] = None
    personsArgMaxVersion: Optional[PersonsArgMaxVersion] = None
    personsJoinMode: Optional[PersonsJoinMode] = None
    personsOnEventsMode: Optional[PersonsOnEventsMode] = None
    propertyGroupsMode: Optional[PropertyGroupsMode] = None
    s3TableUseInvalidColumns: Optional[bool] = None
    sessionTableVersion: Optional[SessionTableVersion] = None
    useMaterializedViews: Optional[bool] = None


class TorQLVariable(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    code_name: str
    value: Optional[Any] = None
    variableId: str


class HogQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    bytecode: Optional[list] = None
    coloredBytecode: Optional[list] = None
    results: Any
    stdout: Optional[str] = None


class Compare(StrEnum):
    CURRENT = "current"
    PREVIOUS = "previous"


class DayItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    label: str
    value: Union[str, AwareDatetime, int]


class InsightDateRange(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    date_from: Optional[str] = "-7d"
    date_to: Optional[str] = None
    explicitDate: Optional[bool] = Field(
        default=False,
        description=(
            "Whether the date_from and date_to should be used verbatim. Disables rounding to the start and end of"
            " period."
        ),
    )


class InsightFilterProperty(StrEnum):
    TRENDS_FILTER = "trendsFilter"
    FUNNELS_FILTER = "funnelsFilter"
    RETENTION_FILTER = "retentionFilter"
    PATHS_FILTER = "pathsFilter"
    STICKINESS_FILTER = "stickinessFilter"
    LIFECYCLE_FILTER = "lifecycleFilter"


class InsightNodeKind(StrEnum):
    TRENDS_QUERY = "TrendsQuery"
    FUNNELS_QUERY = "FunnelsQuery"
    RETENTION_QUERY = "RetentionQuery"
    PATHS_QUERY = "PathsQuery"
    STICKINESS_QUERY = "StickinessQuery"
    LIFECYCLE_QUERY = "LifecycleQuery"


class InsightsThresholdAbsolute(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    lower: Optional[float] = None
    upper: Optional[float] = None


class IntervalType(StrEnum):
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"


class LifecycleToggle(StrEnum):
    NEW = "new"
    RESURRECTING = "resurrecting"
    RETURNING = "returning"
    DORMANT = "dormant"


class MatchedRecordingEvent(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    uuid: str


class MultipleBreakdownType(StrEnum):
    PERSON = "person"
    EVENT = "event"
    GROUP = "group"
    SESSION = "session"
    TORQL = "torql"


class NodeKind(StrEnum):
    EVENTS_NODE = "EventsNode"
    ACTIONS_NODE = "ActionsNode"
    DATA_WAREHOUSE_NODE = "DataWarehouseNode"
    EVENTS_QUERY = "EventsQuery"
    PERSONS_NODE = "PersonsNode"
    HOG_QUERY = "HogQuery"
    HOG_QL_QUERY = "TorQLQuery"
    HOG_QL_METADATA = "TorQLMetadata"
    HOG_QL_AUTOCOMPLETE = "TorQLAutocomplete"
    ACTORS_QUERY = "ActorsQuery"
    FUNNELS_ACTORS_QUERY = "FunnelsActorsQuery"
    FUNNEL_CORRELATION_ACTORS_QUERY = "FunnelCorrelationActorsQuery"
    SESSIONS_TIMELINE_QUERY = "SessionsTimelineQuery"
    RECORDINGS_QUERY = "RecordingsQuery"
    SESSION_ATTRIBUTION_EXPLORER_QUERY = "SessionAttributionExplorerQuery"
    ERROR_TRACKING_QUERY = "ErrorTrackingQuery"
    DATA_TABLE_NODE = "DataTableNode"
    DATA_VISUALIZATION_NODE = "DataVisualizationNode"
    SAVED_INSIGHT_NODE = "SavedInsightNode"
    INSIGHT_VIZ_NODE = "InsightVizNode"
    TRENDS_QUERY = "TrendsQuery"
    FUNNELS_QUERY = "FunnelsQuery"
    RETENTION_QUERY = "RetentionQuery"
    PATHS_QUERY = "PathsQuery"
    STICKINESS_QUERY = "StickinessQuery"
    LIFECYCLE_QUERY = "LifecycleQuery"
    INSIGHT_ACTORS_QUERY = "InsightActorsQuery"
    INSIGHT_ACTORS_QUERY_OPTIONS = "InsightActorsQueryOptions"
    FUNNEL_CORRELATION_QUERY = "FunnelCorrelationQuery"
    WEB_OVERVIEW_QUERY = "WebOverviewQuery"
    WEB_TOP_CLICKS_QUERY = "WebTopClicksQuery"
    WEB_STATS_TABLE_QUERY = "WebStatsTableQuery"
    WEB_EXTERNAL_CLICKS_TABLE_QUERY = "WebExternalClicksTableQuery"
    WEB_GOALS_QUERY = "WebGoalsQuery"
    EXPERIMENT_FUNNEL_QUERY = "ExperimentFunnelQuery"
    EXPERIMENT_TREND_QUERY = "ExperimentTrendQuery"
    DATABASE_SCHEMA_QUERY = "DatabaseSchemaQuery"


class PathCleaningFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    alias: Optional[str] = None
    regex: Optional[str] = None


class PathType(StrEnum):
    FIELD_PAGEVIEW = "$pageview"
    FIELD_SCREEN = "$screen"
    CUSTOM_EVENT = "custom_event"
    TORQL = "torql"


class PathsFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    edgeLimit: Optional[int] = 50
    endPoint: Optional[str] = None
    excludeEvents: Optional[list[str]] = None
    includeEventTypes: Optional[list[PathType]] = None
    localPathCleaningFilters: Optional[list[PathCleaningFilter]] = None
    maxEdgeWeight: Optional[int] = None
    minEdgeWeight: Optional[int] = None
    pathDropoffKey: Optional[str] = Field(default=None, description="Relevant only within actors query")
    pathEndKey: Optional[str] = Field(default=None, description="Relevant only within actors query")
    pathGroupings: Optional[list[str]] = None
    pathReplacements: Optional[bool] = None
    pathStartKey: Optional[str] = Field(default=None, description="Relevant only within actors query")
    pathsTorQLExpression: Optional[str] = None
    startPoint: Optional[str] = None
    stepLimit: Optional[int] = 5


class PathsFilterLegacy(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    edge_limit: Optional[int] = None
    end_point: Optional[str] = None
    exclude_events: Optional[list[str]] = None
    funnel_filter: Optional[dict[str, Any]] = None
    funnel_paths: Optional[FunnelPathType] = None
    include_event_types: Optional[list[PathType]] = None
    local_path_cleaning_filters: Optional[list[PathCleaningFilter]] = None
    max_edge_weight: Optional[int] = None
    min_edge_weight: Optional[int] = None
    path_groupings: Optional[list[str]] = None
    path_replacements: Optional[bool] = None
    path_type: Optional[PathType] = None
    paths_torql_expression: Optional[str] = None
    start_point: Optional[str] = None
    step_limit: Optional[int] = None


class PersonType(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    created_at: Optional[str] = None
    distinct_ids: list[str]
    id: Optional[str] = None
    is_identified: Optional[bool] = None
    name: Optional[str] = None
    properties: dict[str, Any]
    uuid: Optional[str] = None


class PropertyFilterType(StrEnum):
    META = "meta"
    EVENT = "event"
    PERSON = "person"
    ELEMENT = "element"
    FEATURE = "feature"
    SESSION = "session"
    COHORT = "cohort"
    RECORDING = "recording"
    LOG_ENTRY = "log_entry"
    GROUP = "group"
    TORQL = "torql"
    DATA_WAREHOUSE = "data_warehouse"
    DATA_WAREHOUSE_PERSON_PROPERTY = "data_warehouse_person_property"


class PropertyMathType(StrEnum):
    AVG = "avg"
    SUM = "sum"
    MIN = "min"
    MAX = "max"
    MEDIAN = "median"
    P90 = "p90"
    P95 = "p95"
    P99 = "p99"


class PropertyOperator(StrEnum):
    EXACT = "exact"
    IS_NOT = "is_not"
    ICONTAINS = "icontains"
    NOT_ICONTAINS = "not_icontains"
    REGEX = "regex"
    NOT_REGEX = "not_regex"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IS_SET = "is_set"
    IS_NOT_SET = "is_not_set"
    IS_DATE_EXACT = "is_date_exact"
    IS_DATE_BEFORE = "is_date_before"
    IS_DATE_AFTER = "is_date_after"
    BETWEEN = "between"
    NOT_BETWEEN = "not_between"
    MIN = "min"
    MAX = "max"
    IN_ = "in"
    NOT_IN = "not_in"


class QueryResponseAlternative5(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    bytecode: Optional[list] = None
    coloredBytecode: Optional[list] = None
    results: Any
    stdout: Optional[str] = None


class QueryResponseAlternative7(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    errors: list[TorQLNotice]
    isValid: Optional[bool] = None
    isValidView: Optional[bool] = None
    notices: list[TorQLNotice]
    query: Optional[str] = None
    warnings: list[TorQLNotice]


class QueryResponseAlternative16(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    insight: Literal["FUNNELS"] = "FUNNELS"
    results: dict[str, ExperimentVariantFunnelResult]


class QueryResponseAlternative17(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    insight: Literal["TRENDS"] = "TRENDS"
    results: dict[str, ExperimentVariantTrendResult]


class QueryResponseAlternative28(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    insight: Literal["FUNNELS"] = "FUNNELS"
    results: dict[str, ExperimentVariantFunnelResult]


class QueryResponseAlternative29(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    insight: Literal["TRENDS"] = "TRENDS"
    results: dict[str, ExperimentVariantTrendResult]


class QueryStatus(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    complete: Optional[bool] = Field(
        default=False,
        description=(
            "Whether the query is still running. Will be true if the query is complete, even if it errored. Either"
            " result or error will be set."
        ),
    )
    dashboard_id: Optional[int] = None
    end_time: Optional[AwareDatetime] = Field(
        default=None, description="When did the query execution task finish (whether successfully or not)."
    )
    error: Optional[bool] = Field(
        default=False,
        description=(
            "If the query failed, this will be set to true. More information can be found in the error_message field."
        ),
    )
    error_message: Optional[str] = None
    expiration_time: Optional[AwareDatetime] = None
    id: str
    insight_id: Optional[int] = None
    labels: Optional[list[str]] = None
    pickup_time: Optional[AwareDatetime] = Field(
        default=None, description="When was the query execution task picked up by a worker."
    )
    query_async: Literal[True] = Field(default=True, description="ONLY async queries use QueryStatus.")
    query_progress: Optional[ClickhouseQueryProgress] = None
    results: Optional[Any] = None
    start_time: Optional[AwareDatetime] = Field(default=None, description="When was query execution task enqueued.")
    task_id: Optional[str] = None
    team_id: int


class QueryStatusResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    query_status: QueryStatus


class QueryTiming(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    k: str = Field(..., description="Key. Shortened to 'k' to save on data.")
    t: float = Field(..., description="Time in seconds. Shortened to 't' to save on data.")


class RecordingPropertyFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    key: Union[DurationType, str]
    label: Optional[str] = None
    operator: PropertyOperator
    type: Literal["recording"] = "recording"
    value: Optional[Union[str, float, list[Union[str, float]]]] = None


class Kind1(StrEnum):
    ACTIONS_NODE = "ActionsNode"
    EVENTS_NODE = "EventsNode"


class RetentionEntity(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    custom_name: Optional[str] = None
    id: Optional[Union[str, float]] = None
    kind: Optional[Kind1] = None
    name: Optional[str] = None
    order: Optional[int] = None
    type: Optional[EntityType] = None
    uuid: Optional[str] = None


class RetentionReference(StrEnum):
    TOTAL = "total"
    PREVIOUS = "previous"


class RetentionPeriod(StrEnum):
    HOUR = "Hour"
    DAY = "Day"
    WEEK = "Week"
    MONTH = "Month"


class RetentionType(StrEnum):
    RETENTION_RECURRING = "retention_recurring"
    RETENTION_FIRST_TIME = "retention_first_time"


class RetentionValue(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    count: int


class SamplingRate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    denominator: Optional[float] = None
    numerator: float


class SessionAttributionExplorerQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: Any
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class SessionAttributionGroupBy(StrEnum):
    CHANNEL_TYPE = "ChannelType"
    MEDIUM = "Medium"
    SOURCE = "Source"
    CAMPAIGN = "Campaign"
    AD_IDS = "AdIds"
    REFERRING_DOMAIN = "ReferringDomain"
    INITIAL_URL = "InitialURL"


class SessionPropertyFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    key: str
    label: Optional[str] = None
    operator: PropertyOperator
    type: Literal["session"] = "session"
    value: Optional[Union[str, float, list[Union[str, float]]]] = None


class SnapshotSource(StrEnum):
    WEB = "web"
    MOBILE = "mobile"
    UNKNOWN = "unknown"


class Storage(StrEnum):
    OBJECT_STORAGE_LTS = "object_storage_lts"
    OBJECT_STORAGE = "object_storage"


class StepOrderValue(StrEnum):
    STRICT = "strict"
    UNORDERED = "unordered"
    ORDERED = "ordered"


class StickinessFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    display: Optional[ChartDisplayType] = None
    hiddenLegendIndexes: Optional[list[int]] = None
    showLegend: Optional[bool] = None
    showValuesOnSeries: Optional[bool] = None


class StickinessFilterLegacy(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    compare: Optional[bool] = None
    compare_to: Optional[str] = None
    display: Optional[ChartDisplayType] = None
    hidden_legend_keys: Optional[dict[str, Union[bool, Any]]] = None
    show_legend: Optional[bool] = None
    show_values_on_series: Optional[bool] = None


class StickinessQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[dict[str, Any]]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class TaxonomicFilterGroupType(StrEnum):
    METADATA = "metadata"
    ACTIONS = "actions"
    COHORTS = "cohorts"
    COHORTS_WITH_ALL = "cohorts_with_all"
    DATA_WAREHOUSE = "data_warehouse"
    DATA_WAREHOUSE_PROPERTIES = "data_warehouse_properties"
    DATA_WAREHOUSE_PERSON_PROPERTIES = "data_warehouse_person_properties"
    ELEMENTS = "elements"
    EVENTS = "events"
    EVENT_PROPERTIES = "event_properties"
    EVENT_FEATURE_FLAGS = "event_feature_flags"
    NUMERICAL_EVENT_PROPERTIES = "numerical_event_properties"
    PERSON_PROPERTIES = "person_properties"
    PAGEVIEW_URLS = "pageview_urls"
    SCREENS = "screens"
    CUSTOM_EVENTS = "custom_events"
    WILDCARD = "wildcard"
    GROUPS = "groups"
    PERSONS = "persons"
    FEATURE_FLAGS = "feature_flags"
    INSIGHTS = "insights"
    EXPERIMENTS = "experiments"
    PLUGINS = "plugins"
    DASHBOARDS = "dashboards"
    NAME_GROUPS = "name_groups"
    SESSION_PROPERTIES = "session_properties"
    TORQL_EXPRESSION = "torql_expression"
    NOTEBOOKS = "notebooks"
    LOG_ENTRIES = "log_entries"
    REPLAY = "replay"


class TestBasicQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class TestCachedBasicQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    is_cached: bool
    last_refresh: AwareDatetime
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class TimelineEntry(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    events: list[EventType]
    recording_duration_s: Optional[float] = Field(default=None, description="Duration of the recording in seconds.")
    sessionId: Optional[str] = Field(default=None, description="Session ID. None means out-of-session events")


class TrendsAlertConfig(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    series_index: int
    type: Literal["TrendsAlertConfig"] = "TrendsAlertConfig"


class YAxisScaleType(StrEnum):
    LOG10 = "log10"
    LINEAR = "linear"


class TrendsFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    aggregationAxisFormat: Optional[AggregationAxisFormat] = AggregationAxisFormat.NUMERIC
    aggregationAxisPostfix: Optional[str] = None
    aggregationAxisPrefix: Optional[str] = None
    breakdown_histogram_bin_count: Optional[float] = None
    decimalPlaces: Optional[float] = None
    display: Optional[ChartDisplayType] = ChartDisplayType.ACTIONS_LINE_GRAPH
    formula: Optional[str] = None
    hiddenLegendIndexes: Optional[list[int]] = None
    showLabelsOnSeries: Optional[bool] = None
    showLegend: Optional[bool] = False
    showPercentStackView: Optional[bool] = False
    showValuesOnSeries: Optional[bool] = False
    smoothingIntervals: Optional[int] = 1
    yAxisScaleType: Optional[YAxisScaleType] = None


class TrendsFilterLegacy(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    aggregation_axis_format: Optional[AggregationAxisFormat] = None
    aggregation_axis_postfix: Optional[str] = None
    aggregation_axis_prefix: Optional[str] = None
    breakdown_histogram_bin_count: Optional[float] = None
    compare: Optional[bool] = None
    compare_to: Optional[str] = None
    decimal_places: Optional[float] = None
    display: Optional[ChartDisplayType] = None
    formula: Optional[str] = None
    hidden_legend_keys: Optional[dict[str, Union[bool, Any]]] = None
    show_labels_on_series: Optional[bool] = None
    show_legend: Optional[bool] = None
    show_percent_stack_view: Optional[bool] = None
    show_values_on_series: Optional[bool] = None
    smoothing_intervals: Optional[float] = None
    y_axis_scale_type: Optional[YAxisScaleType] = None


class TrendsQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = Field(default=None, description="Wether more breakdown values are available.")
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[dict[str, Any]]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class ActionsPie(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    disableHoverOffset: Optional[bool] = None
    hideAggregation: Optional[bool] = None


class RETENTION(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    hideLineGraph: Optional[bool] = None
    hideSizeColumn: Optional[bool] = None
    useSmallLayout: Optional[bool] = None


class VizSpecificOptions(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    ActionsPie: Optional[ActionsPie] = None
    RETENTION: Optional[RETENTION] = None


class Sampling(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    enabled: Optional[bool] = None
    forceSamplingRate: Optional[SamplingRate] = None


class WebExternalClicksTableQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    samplingRate: Optional[SamplingRate] = None
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class WebGoalsQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    samplingRate: Optional[SamplingRate] = None
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class Kind2(StrEnum):
    UNIT = "unit"
    DURATION_S = "duration_s"
    PERCENTAGE = "percentage"


class WebOverviewItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    changeFromPreviousPct: Optional[float] = None
    isIncreaseBad: Optional[bool] = None
    key: str
    kind: Kind2
    previous: Optional[float] = None
    value: Optional[float] = None


class WebOverviewQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    dateFrom: Optional[str] = None
    dateTo: Optional[str] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[WebOverviewItem]
    samplingRate: Optional[SamplingRate] = None
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class WebStatsBreakdown(StrEnum):
    PAGE = "Page"
    INITIAL_PAGE = "InitialPage"
    EXIT_PAGE = "ExitPage"
    EXIT_CLICK = "ExitClick"
    INITIAL_CHANNEL_TYPE = "InitialChannelType"
    INITIAL_REFERRING_DOMAIN = "InitialReferringDomain"
    INITIAL_UTM_SOURCE = "InitialUTMSource"
    INITIAL_UTM_CAMPAIGN = "InitialUTMCampaign"
    INITIAL_UTM_MEDIUM = "InitialUTMMedium"
    INITIAL_UTM_TERM = "InitialUTMTerm"
    INITIAL_UTM_CONTENT = "InitialUTMContent"
    INITIAL_UTM_SOURCE_MEDIUM_CAMPAIGN = "InitialUTMSourceMediumCampaign"
    BROWSER = "Browser"
    OS = "OS"
    DEVICE_TYPE = "DeviceType"
    COUNTRY = "Country"
    REGION = "Region"
    CITY = "City"


class WebStatsTableQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    samplingRate: Optional[SamplingRate] = None
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class WebTopClicksQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    samplingRate: Optional[SamplingRate] = None
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class Scale(StrEnum):
    LINEAR = "linear"
    LOGARITHMIC = "logarithmic"


class YAxisSettings(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    scale: Optional[Scale] = None
    startAtZero: Optional[bool] = Field(default=None, description="Whether the Y axis should start at zero")


class ActorsQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: list
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: str = Field(..., description="Generated TorQL query.")
    limit: int
    missing_actors_count: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: int
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[list]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: list[str]


class Breakdown(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    group_type_index: Optional[int] = None
    histogram_bin_count: Optional[int] = None
    normalize_url: Optional[bool] = None
    property: str
    type: Optional[MultipleBreakdownType] = None


class BreakdownFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    breakdown: Optional[Union[str, int, list[Union[str, int]]]] = None
    breakdown_group_type_index: Optional[int] = None
    breakdown_hide_other_aggregation: Optional[bool] = None
    breakdown_histogram_bin_count: Optional[int] = None
    breakdown_limit: Optional[int] = None
    breakdown_normalize_url: Optional[bool] = None
    breakdown_type: Optional[BreakdownType] = BreakdownType.EVENT
    breakdowns: Optional[list[Breakdown]] = Field(default=None, max_length=3)


class BreakdownItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    label: str
    value: Union[str, int]


class CacheMissResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: Optional[str] = None
    query_status: Optional[QueryStatus] = None


class CachedActorsQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    columns: list
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: str = Field(..., description="Generated TorQL query.")
    is_cached: bool
    last_refresh: AwareDatetime
    limit: int
    missing_actors_count: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    offset: int
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[list]
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: list[str]


class CachedErrorTrackingQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    columns: Optional[list[str]] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    is_cached: bool
    last_refresh: AwareDatetime
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[ErrorTrackingGroup]
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class CachedEventsQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    columns: list
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: str = Field(..., description="Generated TorQL query.")
    is_cached: bool
    last_refresh: AwareDatetime
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[list]
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: list[str]


class CachedExperimentFunnelQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    insight: Literal["FUNNELS"] = "FUNNELS"
    is_cached: bool
    last_refresh: AwareDatetime
    next_allowed_client_refresh: AwareDatetime
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: dict[str, ExperimentVariantFunnelResult]
    timezone: str


class CachedExperimentTrendQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    insight: Literal["TRENDS"] = "TRENDS"
    is_cached: bool
    last_refresh: AwareDatetime
    next_allowed_client_refresh: AwareDatetime
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: dict[str, ExperimentVariantTrendResult]
    timezone: str


class CachedFunnelCorrelationResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    is_cached: bool
    last_refresh: AwareDatetime
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: FunnelCorrelationResult
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class CachedFunnelsQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    isUdf: Optional[bool] = None
    is_cached: bool
    last_refresh: AwareDatetime
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: Union[FunnelTimeToConvertResults, list[dict[str, Any]], list[list[dict[str, Any]]]]
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class CachedLifecycleQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    is_cached: bool
    last_refresh: AwareDatetime
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[dict[str, Any]]
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class CachedPathsQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    is_cached: bool
    last_refresh: AwareDatetime
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[dict[str, Any]]
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class CachedSessionAttributionExplorerQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    is_cached: bool
    last_refresh: AwareDatetime
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: Any
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class CachedSessionsTimelineQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    is_cached: bool
    last_refresh: AwareDatetime
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[TimelineEntry]
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class CachedStickinessQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    is_cached: bool
    last_refresh: AwareDatetime
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[dict[str, Any]]
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class CachedTrendsQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = Field(default=None, description="Wether more breakdown values are available.")
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    is_cached: bool
    last_refresh: AwareDatetime
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[dict[str, Any]]
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class CachedWebExternalClicksTableQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    is_cached: bool
    last_refresh: AwareDatetime
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    samplingRate: Optional[SamplingRate] = None
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class CachedWebGoalsQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    is_cached: bool
    last_refresh: AwareDatetime
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    samplingRate: Optional[SamplingRate] = None
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class CachedWebOverviewQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    dateFrom: Optional[str] = None
    dateTo: Optional[str] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    is_cached: bool
    last_refresh: AwareDatetime
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[WebOverviewItem]
    samplingRate: Optional[SamplingRate] = None
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class CachedWebStatsTableQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    is_cached: bool
    last_refresh: AwareDatetime
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    samplingRate: Optional[SamplingRate] = None
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class CachedWebTopClicksQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    is_cached: bool
    last_refresh: AwareDatetime
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    samplingRate: Optional[SamplingRate] = None
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class Settings(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    display: Optional[ChartSettingsDisplay] = None
    formatting: Optional[ChartSettingsFormatting] = None


class ChartAxis(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    column: str
    settings: Optional[Settings] = None


class ChartSettings(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    goalLines: Optional[list[GoalLine]] = None
    leftYAxisSettings: Optional[YAxisSettings] = None
    rightYAxisSettings: Optional[YAxisSettings] = None
    stackBars100: Optional[bool] = Field(default=None, description="Whether we fill the bars to 100% in stacked mode")
    xAxis: Optional[ChartAxis] = None
    yAxis: Optional[list[ChartAxis]] = None
    yAxisAtZero: Optional[bool] = Field(
        default=None, description="Deprecated: use `[left|right]YAxisSettings`. Whether the Y axis should start at zero"
    )


class CohortPropertyFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    key: Literal["id"] = "id"
    label: Optional[str] = None
    operator: Optional[PropertyOperator] = PropertyOperator.IN_
    type: Literal["cohort"] = "cohort"
    value: int


class Response(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: list
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: str = Field(..., description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[list]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: list[str]


class Response1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: list
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: str = Field(..., description="Generated TorQL query.")
    limit: int
    missing_actors_count: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: int
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[list]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: list[str]


class Response3(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    dateFrom: Optional[str] = None
    dateTo: Optional[str] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[WebOverviewItem]
    samplingRate: Optional[SamplingRate] = None
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class Response4(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    samplingRate: Optional[SamplingRate] = None
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class Response6(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    samplingRate: Optional[SamplingRate] = None
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class Response7(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    samplingRate: Optional[SamplingRate] = None
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class Response8(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: Any
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class Response9(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list[str]] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[ErrorTrackingGroup]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class Response10(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    insight: Literal["FUNNELS"] = "FUNNELS"
    results: dict[str, ExperimentVariantFunnelResult]


class Response11(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    insight: Literal["TRENDS"] = "TRENDS"
    results: dict[str, ExperimentVariantTrendResult]


class DataWarehousePersonPropertyFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    key: str
    label: Optional[str] = None
    operator: PropertyOperator
    type: Literal["data_warehouse_person_property"] = "data_warehouse_person_property"
    value: Optional[Union[str, float, list[Union[str, float]]]] = None


class DataWarehousePropertyFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    key: str
    label: Optional[str] = None
    operator: PropertyOperator
    type: Literal["data_warehouse"] = "data_warehouse"
    value: Optional[Union[str, float, list[Union[str, float]]]] = None


class DatabaseSchemaField(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    chain: Optional[list[Union[str, int]]] = None
    fields: Optional[list[str]] = None
    torql_value: str
    id: Optional[str] = None
    name: str
    schema_valid: bool
    table: Optional[str] = None
    type: DatabaseSerializedFieldType


class DatabaseSchemaClairViewTable(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    fields: dict[str, DatabaseSchemaField]
    id: str
    name: str
    type: Literal["clairview"] = "clairview"


class DatabaseSchemaTableCommon(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    fields: dict[str, DatabaseSchemaField]
    id: str
    name: str
    type: Type


class ElementPropertyFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    key: Key
    label: Optional[str] = None
    operator: PropertyOperator
    type: Literal["element"] = "element"
    value: Optional[Union[str, float, list[Union[str, float]]]] = None


class ErrorTrackingQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list[str]] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[ErrorTrackingGroup]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class EventPropertyFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    key: str
    label: Optional[str] = None
    operator: Optional[PropertyOperator] = PropertyOperator.EXACT
    type: Literal["event"] = Field(default="event", description="Event properties")
    value: Optional[Union[str, float, list[Union[str, float]]]] = None


class EventsQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: list
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: str = Field(..., description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[list]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: list[str]


class ExperimentFunnelQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    insight: Literal["FUNNELS"] = "FUNNELS"
    results: dict[str, ExperimentVariantFunnelResult]


class ExperimentTrendQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    insight: Literal["TRENDS"] = "TRENDS"
    results: dict[str, ExperimentVariantTrendResult]


class BreakdownFilter1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    breakdown_hide_other_aggregation: Optional[bool] = None
    breakdown_histogram_bin_count: Optional[int] = None
    breakdown_limit: Optional[int] = None
    breakdowns: Optional[list[Breakdown]] = Field(default=None, max_length=3)


class FeaturePropertyFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    key: str
    label: Optional[str] = None
    operator: PropertyOperator
    type: Literal["feature"] = Field(default="feature", description='Event property with "$feature/" prepended')
    value: Optional[Union[str, float, list[Union[str, float]]]] = None


class FunnelCorrelationResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: FunnelCorrelationResult
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class FunnelsFilterLegacy(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    bin_count: Optional[Union[float, str]] = None
    breakdown_attribution_type: Optional[BreakdownAttributionType] = None
    breakdown_attribution_value: Optional[float] = None
    exclusions: Optional[list[FunnelExclusionLegacy]] = None
    funnel_aggregate_by_torql: Optional[str] = None
    funnel_from_step: Optional[float] = None
    funnel_order_type: Optional[StepOrderValue] = None
    funnel_step_reference: Optional[FunnelStepReference] = None
    funnel_to_step: Optional[float] = None
    funnel_viz_type: Optional[FunnelVizType] = None
    funnel_window_interval: Optional[float] = None
    funnel_window_interval_unit: Optional[FunnelConversionWindowTimeUnit] = None
    hidden_legend_keys: Optional[dict[str, Union[bool, Any]]] = None
    layout: Optional[FunnelLayout] = None


class FunnelsQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    isUdf: Optional[bool] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: Union[FunnelTimeToConvertResults, list[dict[str, Any]], list[list[dict[str, Any]]]]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class GenericCachedQueryResponse(BaseModel):
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    is_cached: bool
    last_refresh: AwareDatetime
    next_allowed_client_refresh: AwareDatetime
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    timezone: str


class GroupPropertyFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    group_type_index: Optional[int] = None
    key: str
    label: Optional[str] = None
    operator: PropertyOperator
    type: Literal["group"] = "group"
    value: Optional[Union[str, float, list[Union[str, float]]]] = None


class TorQLAutocompleteResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    incomplete_list: bool = Field(..., description="Whether or not the suggestions returned are complete")
    suggestions: list[AutocompleteCompletionItem]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class TorQLMetadataResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    errors: list[TorQLNotice]
    isValid: Optional[bool] = None
    isValidView: Optional[bool] = None
    notices: list[TorQLNotice]
    query: Optional[str] = None
    warnings: list[TorQLNotice]


class TorQLPropertyFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    key: str
    label: Optional[str] = None
    type: Literal["torql"] = "torql"
    value: Optional[Union[str, float, list[Union[str, float]]]] = None


class TorQLQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    clickhouse: Optional[str] = Field(default=None, description="Executed ClickHouse query")
    columns: Optional[list] = Field(default=None, description="Returned columns")
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    explain: Optional[list[str]] = Field(default=None, description="Query explanation output")
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    metadata: Optional[TorQLMetadataResponse] = Field(default=None, description="Query metadata output")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query: Optional[str] = Field(default=None, description="Input query string")
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = Field(default=None, description="Types of returned columns")


class HogQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    code: Optional[str] = None
    kind: Literal["HogQuery"] = "HogQuery"
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    response: Optional[HogQueryResponse] = None


class InsightActorsQueryBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    includeRecordings: Optional[bool] = None
    kind: NodeKind
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    response: Optional[ActorsQueryResponse] = None


class InsightThreshold(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    absoluteThreshold: Optional[InsightsThresholdAbsolute] = None


class LifecycleFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    showLegend: Optional[bool] = False
    showValuesOnSeries: Optional[bool] = None
    toggledLifecycles: Optional[list[LifecycleToggle]] = None


class LifecycleFilterLegacy(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    show_legend: Optional[bool] = None
    show_values_on_series: Optional[bool] = None
    toggledLifecycles: Optional[list[LifecycleToggle]] = None


class LifecycleQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[dict[str, Any]]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class LogEntryPropertyFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    key: str
    label: Optional[str] = None
    operator: PropertyOperator
    type: Literal["log_entry"] = "log_entry"
    value: Optional[Union[str, float, list[Union[str, float]]]] = None


class MatchedRecording(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    events: list[MatchedRecordingEvent]
    session_id: Optional[str] = None


class MultipleBreakdownOptions(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    values: list[BreakdownItem]


class PathsQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[dict[str, Any]]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class PersonPropertyFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    key: str
    label: Optional[str] = None
    operator: PropertyOperator
    type: Literal["person"] = Field(default="person", description="Person properties")
    value: Optional[Union[str, float, list[Union[str, float]]]] = None


class QueryResponseAlternative1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: list
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: str = Field(..., description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[list]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: list[str]


class QueryResponseAlternative2(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: list
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: str = Field(..., description="Generated TorQL query.")
    limit: int
    missing_actors_count: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: int
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[list]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: list[str]


class QueryResponseAlternative3(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    breakdown: Optional[list[BreakdownItem]] = None
    breakdowns: Optional[list[MultipleBreakdownOptions]] = None
    compare: Optional[list[CompareItem]] = None
    day: Optional[list[DayItem]] = None
    interval: Optional[list[IntervalItem]] = None
    series: Optional[list[Series]] = None
    status: Optional[list[StatusItem]] = None


class QueryResponseAlternative4(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[TimelineEntry]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class QueryResponseAlternative6(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    clickhouse: Optional[str] = Field(default=None, description="Executed ClickHouse query")
    columns: Optional[list] = Field(default=None, description="Returned columns")
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    explain: Optional[list[str]] = Field(default=None, description="Query explanation output")
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    metadata: Optional[TorQLMetadataResponse] = Field(default=None, description="Query metadata output")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query: Optional[str] = Field(default=None, description="Input query string")
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = Field(default=None, description="Types of returned columns")


class QueryResponseAlternative8(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    incomplete_list: bool = Field(..., description="Whether or not the suggestions returned are complete")
    suggestions: list[AutocompleteCompletionItem]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class QueryResponseAlternative9(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    dateFrom: Optional[str] = None
    dateTo: Optional[str] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[WebOverviewItem]
    samplingRate: Optional[SamplingRate] = None
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class QueryResponseAlternative10(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    samplingRate: Optional[SamplingRate] = None
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class QueryResponseAlternative12(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    samplingRate: Optional[SamplingRate] = None
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class QueryResponseAlternative13(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    samplingRate: Optional[SamplingRate] = None
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class QueryResponseAlternative14(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: Any
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class QueryResponseAlternative15(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list[str]] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[ErrorTrackingGroup]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class QueryResponseAlternative18(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: list
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: str = Field(..., description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[list]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: list[str]


class QueryResponseAlternative19(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: list
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: str = Field(..., description="Generated TorQL query.")
    limit: int
    missing_actors_count: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: int
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[list]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: list[str]


class QueryResponseAlternative20(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    clickhouse: Optional[str] = Field(default=None, description="Executed ClickHouse query")
    columns: Optional[list] = Field(default=None, description="Returned columns")
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    explain: Optional[list[str]] = Field(default=None, description="Query explanation output")
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    metadata: Optional[TorQLMetadataResponse] = Field(default=None, description="Query metadata output")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query: Optional[str] = Field(default=None, description="Input query string")
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = Field(default=None, description="Types of returned columns")


class QueryResponseAlternative21(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    dateFrom: Optional[str] = None
    dateTo: Optional[str] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[WebOverviewItem]
    samplingRate: Optional[SamplingRate] = None
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class QueryResponseAlternative22(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    samplingRate: Optional[SamplingRate] = None
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class QueryResponseAlternative24(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    samplingRate: Optional[SamplingRate] = None
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class QueryResponseAlternative25(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    samplingRate: Optional[SamplingRate] = None
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class QueryResponseAlternative26(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: Any
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class QueryResponseAlternative27(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list[str]] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[ErrorTrackingGroup]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class QueryResponseAlternative30(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = Field(default=None, description="Wether more breakdown values are available.")
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[dict[str, Any]]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class QueryResponseAlternative31(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    isUdf: Optional[bool] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: Union[FunnelTimeToConvertResults, list[dict[str, Any]], list[list[dict[str, Any]]]]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class QueryResponseAlternative33(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[dict[str, Any]]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class QueryResponseAlternative36(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list] = None
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: FunnelCorrelationResult
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = None


class RetentionFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cumulative: Optional[bool] = None
    period: Optional[RetentionPeriod] = RetentionPeriod.DAY
    retentionReference: Optional[RetentionReference] = None
    retentionType: Optional[RetentionType] = None
    returningEntity: Optional[RetentionEntity] = None
    showMean: Optional[bool] = None
    targetEntity: Optional[RetentionEntity] = None
    totalIntervals: Optional[int] = 11


class RetentionFilterLegacy(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cumulative: Optional[bool] = None
    period: Optional[RetentionPeriod] = None
    retention_reference: Optional[RetentionReference] = None
    retention_type: Optional[RetentionType] = None
    returning_entity: Optional[RetentionEntity] = None
    show_mean: Optional[bool] = None
    target_entity: Optional[RetentionEntity] = None
    total_intervals: Optional[int] = None


class RetentionResult(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    date: AwareDatetime
    label: str
    values: list[RetentionValue]


class SavedInsightNode(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    allowSorting: Optional[bool] = Field(
        default=None, description="Can the user click on column headers to sort the table? (default: true)"
    )
    embedded: Optional[bool] = Field(default=None, description="Query is embedded inside another bordered component")
    expandable: Optional[bool] = Field(
        default=None, description="Can expand row to show raw event data (default: true)"
    )
    full: Optional[bool] = Field(
        default=None, description="Show with most visual options enabled. Used in insight scene."
    )
    hidePersonsModal: Optional[bool] = None
    kind: Literal["SavedInsightNode"] = "SavedInsightNode"
    propertiesViaUrl: Optional[bool] = Field(default=None, description="Link properties via the URL (default: false)")
    shortId: str
    showActions: Optional[bool] = Field(default=None, description="Show the kebab menu at the end of the row")
    showColumnConfigurator: Optional[bool] = Field(
        default=None, description="Show a button to configure the table's columns if possible"
    )
    showCorrelationTable: Optional[bool] = None
    showDateRange: Optional[bool] = Field(default=None, description="Show date range selector")
    showElapsedTime: Optional[bool] = Field(default=None, description="Show the time it takes to run a query")
    showEventFilter: Optional[bool] = Field(
        default=None, description="Include an event filter above the table (EventsNode only)"
    )
    showExport: Optional[bool] = Field(default=None, description="Show the export button")
    showFilters: Optional[bool] = None
    showHeader: Optional[bool] = None
    showTorQLEditor: Optional[bool] = Field(default=None, description="Include a TorQL query editor above TorQL tables")
    showLastComputation: Optional[bool] = None
    showLastComputationRefresh: Optional[bool] = None
    showOpenEditorButton: Optional[bool] = Field(
        default=None, description="Show a button to open the current query as a new insight. (default: true)"
    )
    showPersistentColumnConfigurator: Optional[bool] = Field(
        default=None, description="Show a button to configure and persist the table's default columns if possible"
    )
    showPropertyFilter: Optional[Union[bool, list[TaxonomicFilterGroupType]]] = Field(
        default=None, description="Include a property filter above the table"
    )
    showReload: Optional[bool] = Field(default=None, description="Show a reload button")
    showResults: Optional[bool] = None
    showResultsTable: Optional[bool] = Field(default=None, description="Show a results table")
    showSavedQueries: Optional[bool] = Field(default=None, description="Shows a list of saved queries")
    showSearch: Optional[bool] = Field(default=None, description="Include a free text search field (PersonsNode only)")
    showTable: Optional[bool] = None
    showTestAccountFilters: Optional[bool] = Field(default=None, description="Show filter to exclude test accounts")
    showTimings: Optional[bool] = Field(default=None, description="Show a detailed query timing breakdown")
    suppressSessionAnalysisWarning: Optional[bool] = None
    vizSpecificOptions: Optional[VizSpecificOptions] = None


class Filters(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    dateRange: Optional[DateRange] = None
    properties: Optional[list[SessionPropertyFilter]] = None


class SessionAttributionExplorerQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    filters: Optional[Filters] = None
    groupBy: list[SessionAttributionGroupBy]
    kind: Literal["SessionAttributionExplorerQuery"] = "SessionAttributionExplorerQuery"
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    response: Optional[SessionAttributionExplorerQueryResponse] = None


class SessionRecordingType(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    active_seconds: Optional[float] = None
    click_count: Optional[float] = None
    console_error_count: Optional[float] = None
    console_log_count: Optional[float] = None
    console_warn_count: Optional[float] = None
    distinct_id: Optional[str] = None
    email: Optional[str] = None
    end_time: str = Field(..., description="When the recording ends in ISO format.")
    id: str
    inactive_seconds: Optional[float] = None
    keypress_count: Optional[float] = None
    matching_events: Optional[list[MatchedRecording]] = Field(default=None, description="List of matching events. *")
    mouse_activity_count: Optional[float] = Field(
        default=None, description="count of all mouse activity in the recording, not just clicks"
    )
    ongoing: Optional[bool] = Field(
        default=None,
        description=(
            "whether we have received data for this recording in the last 5 minutes (assumes the recording was loaded"
            " from ClickHouse)\n*"
        ),
    )
    person: Optional[PersonType] = None
    recording_duration: float = Field(..., description="Length of recording in seconds.")
    snapshot_source: SnapshotSource
    start_time: str = Field(..., description="When the recording starts in ISO format.")
    start_url: Optional[str] = None
    storage: Optional[Storage] = Field(default=None, description="Where this recording information was loaded from")
    summary: Optional[str] = None
    viewed: bool = Field(..., description="Whether this recording has been viewed already.")


class SessionsTimelineQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[TimelineEntry]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class TableSettings(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    columns: Optional[list[ChartAxis]] = None
    conditionalFormatting: Optional[list[ConditionalFormattingRule]] = None


class WebExternalClicksTableQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    conversionGoal: Optional[Union[ActionConversionGoal, CustomEventConversionGoal]] = None
    dateRange: Optional[DateRange] = None
    filterTestAccounts: Optional[bool] = None
    kind: Literal["WebExternalClicksTableQuery"] = "WebExternalClicksTableQuery"
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    properties: list[Union[EventPropertyFilter, PersonPropertyFilter, SessionPropertyFilter]]
    response: Optional[WebExternalClicksTableQueryResponse] = None
    sampling: Optional[Sampling] = None
    stripQueryParams: Optional[bool] = None
    useSessionsTable: Optional[bool] = None


class WebGoalsQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    conversionGoal: Optional[Union[ActionConversionGoal, CustomEventConversionGoal]] = None
    dateRange: Optional[DateRange] = None
    filterTestAccounts: Optional[bool] = None
    kind: Literal["WebGoalsQuery"] = "WebGoalsQuery"
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    properties: list[Union[EventPropertyFilter, PersonPropertyFilter, SessionPropertyFilter]]
    response: Optional[WebGoalsQueryResponse] = None
    sampling: Optional[Sampling] = None
    useSessionsTable: Optional[bool] = None


class WebOverviewQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    compare: Optional[bool] = None
    conversionGoal: Optional[Union[ActionConversionGoal, CustomEventConversionGoal]] = None
    dateRange: Optional[DateRange] = None
    filterTestAccounts: Optional[bool] = None
    includeLCPScore: Optional[bool] = None
    kind: Literal["WebOverviewQuery"] = "WebOverviewQuery"
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    properties: list[Union[EventPropertyFilter, PersonPropertyFilter, SessionPropertyFilter]]
    response: Optional[WebOverviewQueryResponse] = None
    sampling: Optional[Sampling] = None
    useSessionsTable: Optional[bool] = None


class WebStatsTableQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    breakdownBy: WebStatsBreakdown
    conversionGoal: Optional[Union[ActionConversionGoal, CustomEventConversionGoal]] = None
    dateRange: Optional[DateRange] = None
    doPathCleaning: Optional[bool] = None
    filterTestAccounts: Optional[bool] = None
    includeBounceRate: Optional[bool] = None
    includeScrollDepth: Optional[bool] = None
    kind: Literal["WebStatsTableQuery"] = "WebStatsTableQuery"
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    properties: list[Union[EventPropertyFilter, PersonPropertyFilter, SessionPropertyFilter]]
    response: Optional[WebStatsTableQueryResponse] = None
    sampling: Optional[Sampling] = None
    useSessionsTable: Optional[bool] = None


class WebTopClicksQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    conversionGoal: Optional[Union[ActionConversionGoal, CustomEventConversionGoal]] = None
    dateRange: Optional[DateRange] = None
    filterTestAccounts: Optional[bool] = None
    kind: Literal["WebTopClicksQuery"] = "WebTopClicksQuery"
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    properties: list[Union[EventPropertyFilter, PersonPropertyFilter, SessionPropertyFilter]]
    response: Optional[WebTopClicksQueryResponse] = None
    sampling: Optional[Sampling] = None
    useSessionsTable: Optional[bool] = None


class AnyResponseType(
    RootModel[
        Union[
            dict[str, Any],
            HogQueryResponse,
            TorQLQueryResponse,
            TorQLMetadataResponse,
            TorQLAutocompleteResponse,
            Any,
            EventsQueryResponse,
        ]
    ]
):
    root: Union[
        dict[str, Any],
        HogQueryResponse,
        TorQLQueryResponse,
        TorQLMetadataResponse,
        TorQLAutocompleteResponse,
        Any,
        EventsQueryResponse,
    ]


class CachedTorQLQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    clickhouse: Optional[str] = Field(default=None, description="Executed ClickHouse query")
    columns: Optional[list] = Field(default=None, description="Returned columns")
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    explain: Optional[list[str]] = Field(default=None, description="Query explanation output")
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    is_cached: bool
    last_refresh: AwareDatetime
    limit: Optional[int] = None
    metadata: Optional[TorQLMetadataResponse] = Field(default=None, description="Query metadata output")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    offset: Optional[int] = None
    query: Optional[str] = Field(default=None, description="Input query string")
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = Field(default=None, description="Types of returned columns")


class CachedInsightActorsQueryOptionsResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    breakdown: Optional[list[BreakdownItem]] = None
    breakdowns: Optional[list[MultipleBreakdownOptions]] = None
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    compare: Optional[list[CompareItem]] = None
    day: Optional[list[DayItem]] = None
    interval: Optional[list[IntervalItem]] = None
    is_cached: bool
    last_refresh: AwareDatetime
    next_allowed_client_refresh: AwareDatetime
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    series: Optional[list[Series]] = None
    status: Optional[list[StatusItem]] = None
    timezone: str


class CachedRetentionQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cache_key: str
    cache_target_age: Optional[AwareDatetime] = None
    calculation_trigger: Optional[str] = Field(
        default=None, description="What triggered the calculation of the query, leave empty if user/immediate"
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    is_cached: bool
    last_refresh: AwareDatetime
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    next_allowed_client_refresh: AwareDatetime
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[RetentionResult]
    timezone: str
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class DashboardFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    properties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = None


class Response2(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    clickhouse: Optional[str] = Field(default=None, description="Executed ClickHouse query")
    columns: Optional[list] = Field(default=None, description="Returned columns")
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    explain: Optional[list[str]] = Field(default=None, description="Query explanation output")
    hasMore: Optional[bool] = None
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    limit: Optional[int] = None
    metadata: Optional[TorQLMetadataResponse] = Field(default=None, description="Query metadata output")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    query: Optional[str] = Field(default=None, description="Input query string")
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )
    types: Optional[list] = Field(default=None, description="Types of returned columns")


class DataWarehouseNode(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    custom_name: Optional[str] = None
    distinct_id_field: str
    fixedProperties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = Field(
        default=None,
        description="Fixed properties in the query, can't be edited in the interface (e.g. scoping down by person)",
    )
    id: str
    id_field: str
    kind: Literal["DataWarehouseNode"] = "DataWarehouseNode"
    math: Optional[
        Union[BaseMathType, PropertyMathType, CountPerActorMathType, Literal["unique_group"], Literal["torql"]]
    ] = None
    math_group_type_index: Optional[MathGroupTypeIndex] = None
    math_torql: Optional[str] = None
    math_property: Optional[str] = None
    name: Optional[str] = None
    properties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = Field(default=None, description="Properties configurable in the interface")
    response: Optional[dict[str, Any]] = None
    table_name: str
    timestamp_field: str


class DatabaseSchemaBatchExportTable(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    fields: dict[str, DatabaseSchemaField]
    id: str
    name: str
    type: Literal["batch_export"] = "batch_export"


class DatabaseSchemaDataWarehouseTable(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    fields: dict[str, DatabaseSchemaField]
    format: str
    id: str
    name: str
    schema_: Optional[DatabaseSchemaSchema] = Field(default=None, alias="schema")
    source: Optional[DatabaseSchemaSource] = None
    type: Literal["data_warehouse"] = "data_warehouse"
    url_pattern: str


class EntityNode(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    custom_name: Optional[str] = None
    fixedProperties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = Field(
        default=None,
        description="Fixed properties in the query, can't be edited in the interface (e.g. scoping down by person)",
    )
    kind: NodeKind
    math: Optional[
        Union[BaseMathType, PropertyMathType, CountPerActorMathType, Literal["unique_group"], Literal["torql"]]
    ] = None
    math_group_type_index: Optional[MathGroupTypeIndex] = None
    math_torql: Optional[str] = None
    math_property: Optional[str] = None
    name: Optional[str] = None
    properties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = Field(default=None, description="Properties configurable in the interface")
    response: Optional[dict[str, Any]] = None


class EventsNode(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    custom_name: Optional[str] = None
    event: Optional[str] = Field(default=None, description="The event or `null` for all events.")
    fixedProperties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = Field(
        default=None,
        description="Fixed properties in the query, can't be edited in the interface (e.g. scoping down by person)",
    )
    kind: Literal["EventsNode"] = "EventsNode"
    limit: Optional[int] = None
    math: Optional[
        Union[BaseMathType, PropertyMathType, CountPerActorMathType, Literal["unique_group"], Literal["torql"]]
    ] = None
    math_group_type_index: Optional[MathGroupTypeIndex] = None
    math_torql: Optional[str] = None
    math_property: Optional[str] = None
    name: Optional[str] = None
    orderBy: Optional[list[str]] = Field(default=None, description="Columns to order by")
    properties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = Field(default=None, description="Properties configurable in the interface")
    response: Optional[dict[str, Any]] = None


class FunnelExclusionActionsNode(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    custom_name: Optional[str] = None
    fixedProperties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = Field(
        default=None,
        description="Fixed properties in the query, can't be edited in the interface (e.g. scoping down by person)",
    )
    funnelFromStep: int
    funnelToStep: int
    id: int
    kind: Literal["ActionsNode"] = "ActionsNode"
    math: Optional[
        Union[BaseMathType, PropertyMathType, CountPerActorMathType, Literal["unique_group"], Literal["torql"]]
    ] = None
    math_group_type_index: Optional[MathGroupTypeIndex] = None
    math_torql: Optional[str] = None
    math_property: Optional[str] = None
    name: Optional[str] = None
    properties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = Field(default=None, description="Properties configurable in the interface")
    response: Optional[dict[str, Any]] = None


class FunnelExclusionEventsNode(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    custom_name: Optional[str] = None
    event: Optional[str] = Field(default=None, description="The event or `null` for all events.")
    fixedProperties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = Field(
        default=None,
        description="Fixed properties in the query, can't be edited in the interface (e.g. scoping down by person)",
    )
    funnelFromStep: int
    funnelToStep: int
    kind: Literal["EventsNode"] = "EventsNode"
    limit: Optional[int] = None
    math: Optional[
        Union[BaseMathType, PropertyMathType, CountPerActorMathType, Literal["unique_group"], Literal["torql"]]
    ] = None
    math_group_type_index: Optional[MathGroupTypeIndex] = None
    math_torql: Optional[str] = None
    math_property: Optional[str] = None
    name: Optional[str] = None
    orderBy: Optional[list[str]] = Field(default=None, description="Columns to order by")
    properties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = Field(default=None, description="Properties configurable in the interface")
    response: Optional[dict[str, Any]] = None


class TorQLFilters(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    dateRange: Optional[DateRange] = None
    filterTestAccounts: Optional[bool] = None
    properties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = None


class TorQLQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    explain: Optional[bool] = None
    filters: Optional[TorQLFilters] = None
    kind: Literal["TorQLQuery"] = "TorQLQuery"
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query: str
    response: Optional[TorQLQueryResponse] = None
    values: Optional[dict[str, Any]] = Field(
        default=None, description="Constant values that can be referenced with the {placeholder} syntax in the query"
    )
    variables: Optional[dict[str, TorQLVariable]] = Field(
        default=None, description="Variables to be subsituted into the query"
    )


class InsightActorsQueryOptionsResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    breakdown: Optional[list[BreakdownItem]] = None
    breakdowns: Optional[list[MultipleBreakdownOptions]] = None
    compare: Optional[list[CompareItem]] = None
    day: Optional[list[DayItem]] = None
    interval: Optional[list[IntervalItem]] = None
    series: Optional[list[Series]] = None
    status: Optional[list[StatusItem]] = None


class PersonsNode(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cohort: Optional[int] = None
    distinctId: Optional[str] = None
    fixedProperties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = Field(
        default=None,
        description="Fixed properties in the query, can't be edited in the interface (e.g. scoping down by person)",
    )
    kind: Literal["PersonsNode"] = "PersonsNode"
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    properties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = Field(default=None, description="Properties configurable in the interface")
    response: Optional[dict[str, Any]] = None
    search: Optional[str] = None


class PropertyGroupFilterValue(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    type: FilterLogicalOperator
    values: list[
        Union[
            PropertyGroupFilterValue,
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ],
        ]
    ]


class QueryResponseAlternative32(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[RetentionResult]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class RecordingsQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    has_next: bool
    results: list[SessionRecordingType]


class RetentionQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    error: Optional[str] = Field(
        default=None,
        description="Query error. Returned only if 'explain' or `modifiers.debug` is true. Throws an error otherwise.",
    )
    torql: Optional[str] = Field(default=None, description="Generated TorQL query.")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query_status: Optional[QueryStatus] = Field(
        default=None, description="Query status indicates whether next to the provided data, a query is still running."
    )
    results: list[RetentionResult]
    timings: Optional[list[QueryTiming]] = Field(
        default=None, description="Measured timings for different parts of the query generation process"
    )


class SessionsTimelineQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    after: Optional[str] = Field(
        default=None, description="Only fetch sessions that started after this timestamp (default: '-24h')"
    )
    before: Optional[str] = Field(
        default=None, description="Only fetch sessions that started before this timestamp (default: '+5s')"
    )
    kind: Literal["SessionsTimelineQuery"] = "SessionsTimelineQuery"
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    personId: Optional[str] = Field(default=None, description="Fetch sessions only for a given person")
    response: Optional[SessionsTimelineQueryResponse] = None


class AIActionsNode(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    custom_name: Optional[str] = None
    event: Optional[str] = Field(default=None, description="The event or `null` for all events.")
    fixedProperties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
            ]
        ]
    ] = None
    kind: Literal["EventsNode"] = "EventsNode"
    math: Optional[
        Union[BaseMathType, PropertyMathType, CountPerActorMathType, Literal["unique_group"], Literal["torql"]]
    ] = None
    math_group_type_index: Optional[MathGroupTypeIndex] = None
    math_property: Optional[str] = None
    name: Optional[str] = None
    orderBy: Optional[list[str]] = Field(default=None, description="Columns to order by")
    properties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
            ]
        ]
    ] = None
    response: Optional[dict[str, Any]] = None


class AIEventsNode(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    custom_name: Optional[str] = None
    event: Optional[str] = Field(default=None, description="The event or `null` for all events.")
    fixedProperties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
            ]
        ]
    ] = None
    kind: Literal["EventsNode"] = "EventsNode"
    math: Optional[
        Union[BaseMathType, PropertyMathType, CountPerActorMathType, Literal["unique_group"], Literal["torql"]]
    ] = None
    math_group_type_index: Optional[MathGroupTypeIndex] = None
    math_property: Optional[str] = None
    name: Optional[str] = None
    orderBy: Optional[list[str]] = Field(default=None, description="Columns to order by")
    properties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
            ]
        ]
    ] = None
    response: Optional[dict[str, Any]] = None


class ActionsNode(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    custom_name: Optional[str] = None
    fixedProperties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = Field(
        default=None,
        description="Fixed properties in the query, can't be edited in the interface (e.g. scoping down by person)",
    )
    id: int
    kind: Literal["ActionsNode"] = "ActionsNode"
    math: Optional[
        Union[BaseMathType, PropertyMathType, CountPerActorMathType, Literal["unique_group"], Literal["torql"]]
    ] = None
    math_group_type_index: Optional[MathGroupTypeIndex] = None
    math_torql: Optional[str] = None
    math_property: Optional[str] = None
    name: Optional[str] = None
    properties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = Field(default=None, description="Properties configurable in the interface")
    response: Optional[dict[str, Any]] = None


class DataVisualizationNode(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    chartSettings: Optional[ChartSettings] = None
    display: Optional[ChartDisplayType] = None
    kind: Literal["DataVisualizationNode"] = "DataVisualizationNode"
    source: TorQLQuery
    tableSettings: Optional[TableSettings] = None


class DatabaseSchemaMaterializedViewTable(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    fields: dict[str, DatabaseSchemaField]
    id: str
    last_run_at: Optional[str] = None
    name: str
    query: TorQLQuery
    status: Optional[str] = None
    type: Literal["materialized_view"] = "materialized_view"


class DatabaseSchemaViewTable(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    fields: dict[str, DatabaseSchemaField]
    id: str
    name: str
    query: TorQLQuery
    type: Literal["view"] = "view"


class ExperimentalAITrendsQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    aggregation_group_type_index: Optional[int] = Field(default=None, description="Groups aggregation")
    breakdownFilter: Optional[BreakdownFilter1] = Field(default=None, description="Breakdown of the events and actions")
    compareFilter: Optional[CompareFilter] = Field(default=None, description="Compare to date range")
    dateRange: Optional[InsightDateRange] = Field(default=None, description="Date range for the query")
    filterTestAccounts: Optional[bool] = Field(
        default=False, description="Exclude internal and test users by applying the respective filters"
    )
    interval: Optional[IntervalType] = Field(
        default=IntervalType.DAY,
        description="Granularity of the response. Can be one of `hour`, `day`, `week` or `month`",
    )
    kind: Literal["TrendsQuery"] = "TrendsQuery"
    properties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
            ]
        ]
    ] = Field(default=[], description="Property filters for all series")
    samplingFactor: Optional[float] = Field(default=None, description="Sampling rate")
    series: list[Union[AIEventsNode, AIActionsNode]] = Field(..., description="Events and actions to include")
    trendsFilter: Optional[TrendsFilter] = Field(default=None, description="Properties specific to the trends insight")


class FunnelsFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    binCount: Optional[int] = None
    breakdownAttributionType: Optional[BreakdownAttributionType] = BreakdownAttributionType.FIRST_TOUCH
    breakdownAttributionValue: Optional[int] = None
    exclusions: Optional[list[Union[FunnelExclusionEventsNode, FunnelExclusionActionsNode]]] = []
    funnelAggregateByTorQL: Optional[str] = None
    funnelFromStep: Optional[int] = None
    funnelOrderType: Optional[StepOrderValue] = StepOrderValue.ORDERED
    funnelStepReference: Optional[FunnelStepReference] = FunnelStepReference.TOTAL
    funnelToStep: Optional[int] = None
    funnelVizType: Optional[FunnelVizType] = FunnelVizType.STEPS
    funnelWindowInterval: Optional[int] = 14
    funnelWindowIntervalUnit: Optional[FunnelConversionWindowTimeUnit] = FunnelConversionWindowTimeUnit.DAY
    hiddenLegendBreakdowns: Optional[list[str]] = None
    layout: Optional[FunnelLayout] = FunnelLayout.VERTICAL
    useUdf: Optional[bool] = None


class InsightFilter(
    RootModel[Union[TrendsFilter, FunnelsFilter, RetentionFilter, PathsFilter, StickinessFilter, LifecycleFilter]]
):
    root: Union[TrendsFilter, FunnelsFilter, RetentionFilter, PathsFilter, StickinessFilter, LifecycleFilter]


class PropertyGroupFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    type: FilterLogicalOperator
    values: list[PropertyGroupFilterValue]


class RecordingsQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    actions: Optional[list[dict[str, Any]]] = None
    console_log_filters: Optional[list[LogEntryPropertyFilter]] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    events: Optional[list[dict[str, Any]]] = None
    filter_test_accounts: Optional[bool] = None
    having_predicates: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = None
    kind: Literal["RecordingsQuery"] = "RecordingsQuery"
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    operand: Optional[FilterLogicalOperator] = None
    order: Union[DurationType, str]
    person_uuid: Optional[str] = None
    properties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = None
    response: Optional[RecordingsQueryResponse] = None
    session_ids: Optional[list[str]] = None
    user_modified_filters: Optional[dict[str, Any]] = None


class RetentionQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    aggregation_group_type_index: Optional[int] = Field(default=None, description="Groups aggregation")
    dateRange: Optional[InsightDateRange] = Field(default=None, description="Date range for the query")
    filterTestAccounts: Optional[bool] = Field(
        default=False, description="Exclude internal and test users by applying the respective filters"
    )
    kind: Literal["RetentionQuery"] = "RetentionQuery"
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    properties: Optional[
        Union[
            list[
                Union[
                    EventPropertyFilter,
                    PersonPropertyFilter,
                    ElementPropertyFilter,
                    SessionPropertyFilter,
                    CohortPropertyFilter,
                    RecordingPropertyFilter,
                    LogEntryPropertyFilter,
                    GroupPropertyFilter,
                    FeaturePropertyFilter,
                    TorQLPropertyFilter,
                    EmptyPropertyFilter,
                    DataWarehousePropertyFilter,
                    DataWarehousePersonPropertyFilter,
                ]
            ],
            PropertyGroupFilter,
        ]
    ] = Field(default=[], description="Property filters for all series")
    response: Optional[RetentionQueryResponse] = None
    retentionFilter: RetentionFilter = Field(..., description="Properties specific to the retention insight")
    samplingFactor: Optional[float] = Field(default=None, description="Sampling rate")


class StickinessQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    compareFilter: Optional[CompareFilter] = Field(default=None, description="Compare to date range")
    dateRange: Optional[InsightDateRange] = Field(default=None, description="Date range for the query")
    filterTestAccounts: Optional[bool] = Field(
        default=False, description="Exclude internal and test users by applying the respective filters"
    )
    interval: Optional[IntervalType] = Field(
        default=IntervalType.DAY,
        description="Granularity of the response. Can be one of `hour`, `day`, `week` or `month`",
    )
    kind: Literal["StickinessQuery"] = "StickinessQuery"
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    properties: Optional[
        Union[
            list[
                Union[
                    EventPropertyFilter,
                    PersonPropertyFilter,
                    ElementPropertyFilter,
                    SessionPropertyFilter,
                    CohortPropertyFilter,
                    RecordingPropertyFilter,
                    LogEntryPropertyFilter,
                    GroupPropertyFilter,
                    FeaturePropertyFilter,
                    TorQLPropertyFilter,
                    EmptyPropertyFilter,
                    DataWarehousePropertyFilter,
                    DataWarehousePersonPropertyFilter,
                ]
            ],
            PropertyGroupFilter,
        ]
    ] = Field(default=[], description="Property filters for all series")
    response: Optional[StickinessQueryResponse] = None
    samplingFactor: Optional[float] = Field(default=None, description="Sampling rate")
    series: list[Union[EventsNode, ActionsNode, DataWarehouseNode]] = Field(
        ..., description="Events and actions to include"
    )
    stickinessFilter: Optional[StickinessFilter] = Field(
        default=None, description="Properties specific to the stickiness insight"
    )


class TrendsQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    aggregation_group_type_index: Optional[int] = Field(default=None, description="Groups aggregation")
    breakdownFilter: Optional[BreakdownFilter] = Field(default=None, description="Breakdown of the events and actions")
    compareFilter: Optional[CompareFilter] = Field(default=None, description="Compare to date range")
    dateRange: Optional[InsightDateRange] = Field(default=None, description="Date range for the query")
    filterTestAccounts: Optional[bool] = Field(
        default=False, description="Exclude internal and test users by applying the respective filters"
    )
    interval: Optional[IntervalType] = Field(
        default=IntervalType.DAY,
        description="Granularity of the response. Can be one of `hour`, `day`, `week` or `month`",
    )
    kind: Literal["TrendsQuery"] = "TrendsQuery"
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    properties: Optional[
        Union[
            list[
                Union[
                    EventPropertyFilter,
                    PersonPropertyFilter,
                    ElementPropertyFilter,
                    SessionPropertyFilter,
                    CohortPropertyFilter,
                    RecordingPropertyFilter,
                    LogEntryPropertyFilter,
                    GroupPropertyFilter,
                    FeaturePropertyFilter,
                    TorQLPropertyFilter,
                    EmptyPropertyFilter,
                    DataWarehousePropertyFilter,
                    DataWarehousePersonPropertyFilter,
                ]
            ],
            PropertyGroupFilter,
        ]
    ] = Field(default=[], description="Property filters for all series")
    response: Optional[TrendsQueryResponse] = None
    samplingFactor: Optional[float] = Field(default=None, description="Sampling rate")
    series: list[Union[EventsNode, ActionsNode, DataWarehouseNode]] = Field(
        ..., description="Events and actions to include"
    )
    trendsFilter: Optional[TrendsFilter] = Field(default=None, description="Properties specific to the trends insight")


class ErrorTrackingQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    assignee: Optional[int] = None
    dateRange: DateRange
    filterGroup: Optional[PropertyGroupFilter] = None
    filterTestAccounts: Optional[bool] = None
    fingerprint: Optional[list[str]] = None
    kind: Literal["ErrorTrackingQuery"] = "ErrorTrackingQuery"
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    order: Optional[Order] = None
    response: Optional[ErrorTrackingQueryResponse] = None
    searchQuery: Optional[str] = None
    select: Optional[list[str]] = None


class EventsQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    actionId: Optional[int] = Field(default=None, description="Show events matching a given action")
    after: Optional[str] = Field(default=None, description="Only fetch events that happened after this timestamp")
    before: Optional[str] = Field(default=None, description="Only fetch events that happened before this timestamp")
    event: Optional[str] = Field(default=None, description="Limit to events matching this string")
    filterTestAccounts: Optional[bool] = Field(default=None, description="Filter test accounts")
    fixedProperties: Optional[
        list[
            Union[
                PropertyGroupFilter,
                PropertyGroupFilterValue,
                Union[
                    EventPropertyFilter,
                    PersonPropertyFilter,
                    ElementPropertyFilter,
                    SessionPropertyFilter,
                    CohortPropertyFilter,
                    RecordingPropertyFilter,
                    LogEntryPropertyFilter,
                    GroupPropertyFilter,
                    FeaturePropertyFilter,
                    TorQLPropertyFilter,
                    EmptyPropertyFilter,
                    DataWarehousePropertyFilter,
                    DataWarehousePersonPropertyFilter,
                ],
            ]
        ]
    ] = Field(
        default=None,
        description="Fixed properties in the query, can't be edited in the interface (e.g. scoping down by person)",
    )
    kind: Literal["EventsQuery"] = "EventsQuery"
    limit: Optional[int] = Field(default=None, description="Number of rows to return")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = Field(default=None, description="Number of rows to skip before returning rows")
    orderBy: Optional[list[str]] = Field(default=None, description="Columns to order by")
    personId: Optional[str] = Field(default=None, description="Show events for a given person")
    properties: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = Field(default=None, description="Properties configurable in the interface")
    response: Optional[EventsQueryResponse] = None
    select: list[str] = Field(..., description="Return a limited set of data. Required.")
    where: Optional[list[str]] = Field(default=None, description="TorQL filters to apply on returned data")


class ExperimentTrendQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    count_query: TrendsQuery
    experiment_id: int
    exposure_query: Optional[TrendsQuery] = None
    kind: Literal["ExperimentTrendQuery"] = "ExperimentTrendQuery"
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    response: Optional[ExperimentTrendQueryResponse] = None


class FunnelsQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    aggregation_group_type_index: Optional[int] = Field(default=None, description="Groups aggregation")
    breakdownFilter: Optional[BreakdownFilter] = Field(default=None, description="Breakdown of the events and actions")
    dateRange: Optional[InsightDateRange] = Field(default=None, description="Date range for the query")
    filterTestAccounts: Optional[bool] = Field(
        default=False, description="Exclude internal and test users by applying the respective filters"
    )
    funnelsFilter: Optional[FunnelsFilter] = Field(
        default=None, description="Properties specific to the funnels insight"
    )
    interval: Optional[IntervalType] = Field(
        default=None, description="Granularity of the response. Can be one of `hour`, `day`, `week` or `month`"
    )
    kind: Literal["FunnelsQuery"] = "FunnelsQuery"
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    properties: Optional[
        Union[
            list[
                Union[
                    EventPropertyFilter,
                    PersonPropertyFilter,
                    ElementPropertyFilter,
                    SessionPropertyFilter,
                    CohortPropertyFilter,
                    RecordingPropertyFilter,
                    LogEntryPropertyFilter,
                    GroupPropertyFilter,
                    FeaturePropertyFilter,
                    TorQLPropertyFilter,
                    EmptyPropertyFilter,
                    DataWarehousePropertyFilter,
                    DataWarehousePersonPropertyFilter,
                ]
            ],
            PropertyGroupFilter,
        ]
    ] = Field(default=[], description="Property filters for all series")
    response: Optional[FunnelsQueryResponse] = None
    samplingFactor: Optional[float] = Field(default=None, description="Sampling rate")
    series: list[Union[EventsNode, ActionsNode, DataWarehouseNode]] = Field(
        ..., description="Events and actions to include"
    )


class HasPropertiesNode(RootModel[Union[EventsNode, EventsQuery, PersonsNode]]):
    root: Union[EventsNode, EventsQuery, PersonsNode]


class InsightsQueryBaseFunnelsQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    aggregation_group_type_index: Optional[int] = Field(default=None, description="Groups aggregation")
    dateRange: Optional[InsightDateRange] = Field(default=None, description="Date range for the query")
    filterTestAccounts: Optional[bool] = Field(
        default=False, description="Exclude internal and test users by applying the respective filters"
    )
    kind: NodeKind
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    properties: Optional[
        Union[
            list[
                Union[
                    EventPropertyFilter,
                    PersonPropertyFilter,
                    ElementPropertyFilter,
                    SessionPropertyFilter,
                    CohortPropertyFilter,
                    RecordingPropertyFilter,
                    LogEntryPropertyFilter,
                    GroupPropertyFilter,
                    FeaturePropertyFilter,
                    TorQLPropertyFilter,
                    EmptyPropertyFilter,
                    DataWarehousePropertyFilter,
                    DataWarehousePersonPropertyFilter,
                ]
            ],
            PropertyGroupFilter,
        ]
    ] = Field(default=[], description="Property filters for all series")
    response: Optional[FunnelsQueryResponse] = None
    samplingFactor: Optional[float] = Field(default=None, description="Sampling rate")


class InsightsQueryBaseLifecycleQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    aggregation_group_type_index: Optional[int] = Field(default=None, description="Groups aggregation")
    dateRange: Optional[InsightDateRange] = Field(default=None, description="Date range for the query")
    filterTestAccounts: Optional[bool] = Field(
        default=False, description="Exclude internal and test users by applying the respective filters"
    )
    kind: NodeKind
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    properties: Optional[
        Union[
            list[
                Union[
                    EventPropertyFilter,
                    PersonPropertyFilter,
                    ElementPropertyFilter,
                    SessionPropertyFilter,
                    CohortPropertyFilter,
                    RecordingPropertyFilter,
                    LogEntryPropertyFilter,
                    GroupPropertyFilter,
                    FeaturePropertyFilter,
                    TorQLPropertyFilter,
                    EmptyPropertyFilter,
                    DataWarehousePropertyFilter,
                    DataWarehousePersonPropertyFilter,
                ]
            ],
            PropertyGroupFilter,
        ]
    ] = Field(default=[], description="Property filters for all series")
    response: Optional[LifecycleQueryResponse] = None
    samplingFactor: Optional[float] = Field(default=None, description="Sampling rate")


class InsightsQueryBasePathsQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    aggregation_group_type_index: Optional[int] = Field(default=None, description="Groups aggregation")
    dateRange: Optional[InsightDateRange] = Field(default=None, description="Date range for the query")
    filterTestAccounts: Optional[bool] = Field(
        default=False, description="Exclude internal and test users by applying the respective filters"
    )
    kind: NodeKind
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    properties: Optional[
        Union[
            list[
                Union[
                    EventPropertyFilter,
                    PersonPropertyFilter,
                    ElementPropertyFilter,
                    SessionPropertyFilter,
                    CohortPropertyFilter,
                    RecordingPropertyFilter,
                    LogEntryPropertyFilter,
                    GroupPropertyFilter,
                    FeaturePropertyFilter,
                    TorQLPropertyFilter,
                    EmptyPropertyFilter,
                    DataWarehousePropertyFilter,
                    DataWarehousePersonPropertyFilter,
                ]
            ],
            PropertyGroupFilter,
        ]
    ] = Field(default=[], description="Property filters for all series")
    response: Optional[PathsQueryResponse] = None
    samplingFactor: Optional[float] = Field(default=None, description="Sampling rate")


class InsightsQueryBaseRetentionQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    aggregation_group_type_index: Optional[int] = Field(default=None, description="Groups aggregation")
    dateRange: Optional[InsightDateRange] = Field(default=None, description="Date range for the query")
    filterTestAccounts: Optional[bool] = Field(
        default=False, description="Exclude internal and test users by applying the respective filters"
    )
    kind: NodeKind
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    properties: Optional[
        Union[
            list[
                Union[
                    EventPropertyFilter,
                    PersonPropertyFilter,
                    ElementPropertyFilter,
                    SessionPropertyFilter,
                    CohortPropertyFilter,
                    RecordingPropertyFilter,
                    LogEntryPropertyFilter,
                    GroupPropertyFilter,
                    FeaturePropertyFilter,
                    TorQLPropertyFilter,
                    EmptyPropertyFilter,
                    DataWarehousePropertyFilter,
                    DataWarehousePersonPropertyFilter,
                ]
            ],
            PropertyGroupFilter,
        ]
    ] = Field(default=[], description="Property filters for all series")
    response: Optional[RetentionQueryResponse] = None
    samplingFactor: Optional[float] = Field(default=None, description="Sampling rate")


class InsightsQueryBaseTrendsQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    aggregation_group_type_index: Optional[int] = Field(default=None, description="Groups aggregation")
    dateRange: Optional[InsightDateRange] = Field(default=None, description="Date range for the query")
    filterTestAccounts: Optional[bool] = Field(
        default=False, description="Exclude internal and test users by applying the respective filters"
    )
    kind: NodeKind
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    properties: Optional[
        Union[
            list[
                Union[
                    EventPropertyFilter,
                    PersonPropertyFilter,
                    ElementPropertyFilter,
                    SessionPropertyFilter,
                    CohortPropertyFilter,
                    RecordingPropertyFilter,
                    LogEntryPropertyFilter,
                    GroupPropertyFilter,
                    FeaturePropertyFilter,
                    TorQLPropertyFilter,
                    EmptyPropertyFilter,
                    DataWarehousePropertyFilter,
                    DataWarehousePersonPropertyFilter,
                ]
            ],
            PropertyGroupFilter,
        ]
    ] = Field(default=[], description="Property filters for all series")
    response: Optional[TrendsQueryResponse] = None
    samplingFactor: Optional[float] = Field(default=None, description="Sampling rate")


class LifecycleQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    aggregation_group_type_index: Optional[int] = Field(default=None, description="Groups aggregation")
    dateRange: Optional[InsightDateRange] = Field(default=None, description="Date range for the query")
    filterTestAccounts: Optional[bool] = Field(
        default=False, description="Exclude internal and test users by applying the respective filters"
    )
    interval: Optional[IntervalType] = Field(
        default=IntervalType.DAY,
        description="Granularity of the response. Can be one of `hour`, `day`, `week` or `month`",
    )
    kind: Literal["LifecycleQuery"] = "LifecycleQuery"
    lifecycleFilter: Optional[LifecycleFilter] = Field(
        default=None, description="Properties specific to the lifecycle insight"
    )
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    properties: Optional[
        Union[
            list[
                Union[
                    EventPropertyFilter,
                    PersonPropertyFilter,
                    ElementPropertyFilter,
                    SessionPropertyFilter,
                    CohortPropertyFilter,
                    RecordingPropertyFilter,
                    LogEntryPropertyFilter,
                    GroupPropertyFilter,
                    FeaturePropertyFilter,
                    TorQLPropertyFilter,
                    EmptyPropertyFilter,
                    DataWarehousePropertyFilter,
                    DataWarehousePersonPropertyFilter,
                ]
            ],
            PropertyGroupFilter,
        ]
    ] = Field(default=[], description="Property filters for all series")
    response: Optional[LifecycleQueryResponse] = None
    samplingFactor: Optional[float] = Field(default=None, description="Sampling rate")
    series: list[Union[EventsNode, ActionsNode, DataWarehouseNode]] = Field(
        ..., description="Events and actions to include"
    )


class QueryResponseAlternative37(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    tables: dict[
        str,
        Union[
            DatabaseSchemaClairViewTable,
            DatabaseSchemaDataWarehouseTable,
            DatabaseSchemaViewTable,
            DatabaseSchemaBatchExportTable,
            DatabaseSchemaMaterializedViewTable,
        ],
    ]


class QueryResponseAlternative(
    RootModel[
        Union[
            dict[str, Any],
            QueryResponseAlternative1,
            QueryResponseAlternative2,
            QueryResponseAlternative3,
            QueryResponseAlternative4,
            QueryResponseAlternative5,
            QueryResponseAlternative6,
            QueryResponseAlternative7,
            QueryResponseAlternative8,
            QueryResponseAlternative9,
            QueryResponseAlternative10,
            QueryResponseAlternative12,
            QueryResponseAlternative13,
            QueryResponseAlternative14,
            QueryResponseAlternative15,
            QueryResponseAlternative16,
            QueryResponseAlternative17,
            Any,
            QueryResponseAlternative18,
            QueryResponseAlternative19,
            QueryResponseAlternative20,
            QueryResponseAlternative21,
            QueryResponseAlternative22,
            QueryResponseAlternative24,
            QueryResponseAlternative25,
            QueryResponseAlternative26,
            QueryResponseAlternative27,
            QueryResponseAlternative28,
            QueryResponseAlternative29,
            QueryResponseAlternative30,
            QueryResponseAlternative31,
            QueryResponseAlternative32,
            QueryResponseAlternative33,
            QueryResponseAlternative36,
            QueryResponseAlternative37,
        ]
    ]
):
    root: Union[
        dict[str, Any],
        QueryResponseAlternative1,
        QueryResponseAlternative2,
        QueryResponseAlternative3,
        QueryResponseAlternative4,
        QueryResponseAlternative5,
        QueryResponseAlternative6,
        QueryResponseAlternative7,
        QueryResponseAlternative8,
        QueryResponseAlternative9,
        QueryResponseAlternative10,
        QueryResponseAlternative12,
        QueryResponseAlternative13,
        QueryResponseAlternative14,
        QueryResponseAlternative15,
        QueryResponseAlternative16,
        QueryResponseAlternative17,
        Any,
        QueryResponseAlternative18,
        QueryResponseAlternative19,
        QueryResponseAlternative20,
        QueryResponseAlternative21,
        QueryResponseAlternative22,
        QueryResponseAlternative24,
        QueryResponseAlternative25,
        QueryResponseAlternative26,
        QueryResponseAlternative27,
        QueryResponseAlternative28,
        QueryResponseAlternative29,
        QueryResponseAlternative30,
        QueryResponseAlternative31,
        QueryResponseAlternative32,
        QueryResponseAlternative33,
        QueryResponseAlternative36,
        QueryResponseAlternative37,
    ]


class DatabaseSchemaQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    tables: dict[
        str,
        Union[
            DatabaseSchemaClairViewTable,
            DatabaseSchemaDataWarehouseTable,
            DatabaseSchemaViewTable,
            DatabaseSchemaBatchExportTable,
            DatabaseSchemaMaterializedViewTable,
        ],
    ]


class ExperimentFunnelQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    experiment_id: int
    kind: Literal["ExperimentFunnelQuery"] = "ExperimentFunnelQuery"
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    response: Optional[ExperimentFunnelQueryResponse] = None
    source: FunnelsQuery


class FunnelPathsFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    funnelPathType: Optional[FunnelPathType] = None
    funnelSource: FunnelsQuery
    funnelStep: Optional[int] = None


class FunnelsActorsQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    funnelCustomSteps: Optional[list[int]] = Field(
        default=None,
        description=(
            "Custom step numbers to get persons for. This overrides `funnelStep`. Primarily for correlation use."
        ),
    )
    funnelStep: Optional[int] = Field(
        default=None,
        description=(
            "Index of the step for which we want to get the timestamp for, per person. Positive for converted persons,"
            " negative for dropped of persons."
        ),
    )
    funnelStepBreakdown: Optional[Union[str, float, list[Union[str, float]]]] = Field(
        default=None,
        description=(
            "The breakdown value for which to get persons for. This is an array for person and event properties, a"
            " string for groups and an integer for cohorts."
        ),
    )
    funnelTrendsDropOff: Optional[bool] = None
    funnelTrendsEntrancePeriodStart: Optional[str] = Field(
        default=None,
        description="Used together with `funnelTrendsDropOff` for funnels time conversion date for the persons modal.",
    )
    includeRecordings: Optional[bool] = None
    kind: Literal["FunnelsActorsQuery"] = "FunnelsActorsQuery"
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    response: Optional[ActorsQueryResponse] = None
    source: FunnelsQuery


class PathsQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    aggregation_group_type_index: Optional[int] = Field(default=None, description="Groups aggregation")
    dateRange: Optional[InsightDateRange] = Field(default=None, description="Date range for the query")
    filterTestAccounts: Optional[bool] = Field(
        default=False, description="Exclude internal and test users by applying the respective filters"
    )
    funnelPathsFilter: Optional[FunnelPathsFilter] = Field(
        default=None, description="Used for displaying paths in relation to funnel steps."
    )
    kind: Literal["PathsQuery"] = "PathsQuery"
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    pathsFilter: PathsFilter = Field(..., description="Properties specific to the paths insight")
    properties: Optional[
        Union[
            list[
                Union[
                    EventPropertyFilter,
                    PersonPropertyFilter,
                    ElementPropertyFilter,
                    SessionPropertyFilter,
                    CohortPropertyFilter,
                    RecordingPropertyFilter,
                    LogEntryPropertyFilter,
                    GroupPropertyFilter,
                    FeaturePropertyFilter,
                    TorQLPropertyFilter,
                    EmptyPropertyFilter,
                    DataWarehousePropertyFilter,
                    DataWarehousePersonPropertyFilter,
                ]
            ],
            PropertyGroupFilter,
        ]
    ] = Field(default=[], description="Property filters for all series")
    response: Optional[PathsQueryResponse] = None
    samplingFactor: Optional[float] = Field(default=None, description="Sampling rate")


class DatabaseSchemaQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    kind: Literal["DatabaseSchemaQuery"] = "DatabaseSchemaQuery"
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    response: Optional[DatabaseSchemaQueryResponse] = None


class FunnelCorrelationQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    funnelCorrelationEventExcludePropertyNames: Optional[list[str]] = None
    funnelCorrelationEventNames: Optional[list[str]] = None
    funnelCorrelationExcludeEventNames: Optional[list[str]] = None
    funnelCorrelationExcludeNames: Optional[list[str]] = None
    funnelCorrelationNames: Optional[list[str]] = None
    funnelCorrelationType: FunnelCorrelationResultsType
    kind: Literal["FunnelCorrelationQuery"] = "FunnelCorrelationQuery"
    response: Optional[FunnelCorrelationResponse] = None
    source: FunnelsActorsQuery


class InsightVizNode(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    embedded: Optional[bool] = Field(default=None, description="Query is embedded inside another bordered component")
    full: Optional[bool] = Field(
        default=None, description="Show with most visual options enabled. Used in insight scene."
    )
    hidePersonsModal: Optional[bool] = None
    kind: Literal["InsightVizNode"] = "InsightVizNode"
    showCorrelationTable: Optional[bool] = None
    showFilters: Optional[bool] = None
    showHeader: Optional[bool] = None
    showLastComputation: Optional[bool] = None
    showLastComputationRefresh: Optional[bool] = None
    showResults: Optional[bool] = None
    showTable: Optional[bool] = None
    source: Union[TrendsQuery, FunnelsQuery, RetentionQuery, PathsQuery, StickinessQuery, LifecycleQuery] = Field(
        ..., discriminator="kind"
    )
    suppressSessionAnalysisWarning: Optional[bool] = None
    vizSpecificOptions: Optional[VizSpecificOptions] = None


class FunnelCorrelationActorsQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    funnelCorrelationPersonConverted: Optional[bool] = None
    funnelCorrelationPersonEntity: Optional[Union[EventsNode, ActionsNode, DataWarehouseNode]] = None
    funnelCorrelationPropertyValues: Optional[
        list[
            Union[
                EventPropertyFilter,
                PersonPropertyFilter,
                ElementPropertyFilter,
                SessionPropertyFilter,
                CohortPropertyFilter,
                RecordingPropertyFilter,
                LogEntryPropertyFilter,
                GroupPropertyFilter,
                FeaturePropertyFilter,
                TorQLPropertyFilter,
                EmptyPropertyFilter,
                DataWarehousePropertyFilter,
                DataWarehousePersonPropertyFilter,
            ]
        ]
    ] = None
    includeRecordings: Optional[bool] = None
    kind: Literal["FunnelCorrelationActorsQuery"] = "FunnelCorrelationActorsQuery"
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    response: Optional[ActorsQueryResponse] = None
    source: FunnelCorrelationQuery


class InsightActorsQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    breakdown: Optional[Union[str, list[str], int]] = None
    compare: Optional[Compare] = None
    day: Optional[Union[str, int]] = None
    includeRecordings: Optional[bool] = None
    interval: Optional[int] = Field(
        default=None, description="An interval selected out of available intervals in source query."
    )
    kind: Literal["InsightActorsQuery"] = "InsightActorsQuery"
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    response: Optional[ActorsQueryResponse] = None
    series: Optional[int] = None
    source: Union[TrendsQuery, FunnelsQuery, RetentionQuery, PathsQuery, StickinessQuery, LifecycleQuery] = Field(
        ..., discriminator="kind"
    )
    status: Optional[str] = None


class InsightActorsQueryOptions(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    kind: Literal["InsightActorsQueryOptions"] = "InsightActorsQueryOptions"
    response: Optional[InsightActorsQueryOptionsResponse] = None
    source: Union[InsightActorsQuery, FunnelsActorsQuery, FunnelCorrelationActorsQuery]


class ActorsQuery(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    fixedProperties: Optional[
        list[Union[PersonPropertyFilter, CohortPropertyFilter, TorQLPropertyFilter, EmptyPropertyFilter]]
    ] = Field(
        default=None,
        description=(
            "Currently only person filters supported. No filters for querying groups. See `filter_conditions()` in"
            " actor_strategies.py."
        ),
    )
    kind: Literal["ActorsQuery"] = "ActorsQuery"
    limit: Optional[int] = None
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    offset: Optional[int] = None
    orderBy: Optional[list[str]] = None
    properties: Optional[
        list[Union[PersonPropertyFilter, CohortPropertyFilter, TorQLPropertyFilter, EmptyPropertyFilter]]
    ] = Field(
        default=None,
        description=(
            "Currently only person filters supported. No filters for querying groups. See `filter_conditions()` in"
            " actor_strategies.py."
        ),
    )
    response: Optional[ActorsQueryResponse] = None
    search: Optional[str] = None
    select: Optional[list[str]] = None
    source: Optional[Union[InsightActorsQuery, FunnelsActorsQuery, FunnelCorrelationActorsQuery, TorQLQuery]] = None


class DataTableNode(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    allowSorting: Optional[bool] = Field(
        default=None, description="Can the user click on column headers to sort the table? (default: true)"
    )
    columns: Optional[list[str]] = Field(
        default=None, description="Columns shown in the table, unless the `source` provides them."
    )
    embedded: Optional[bool] = Field(default=None, description="Uses the embedded version of LemonTable")
    expandable: Optional[bool] = Field(
        default=None, description="Can expand row to show raw event data (default: true)"
    )
    full: Optional[bool] = Field(default=None, description="Show with most visual options enabled. Used in scenes.")
    hiddenColumns: Optional[list[str]] = Field(
        default=None, description="Columns that aren't shown in the table, even if in columns or returned data"
    )
    kind: Literal["DataTableNode"] = "DataTableNode"
    propertiesViaUrl: Optional[bool] = Field(default=None, description="Link properties via the URL (default: false)")
    response: Optional[
        Union[
            dict[str, Any],
            Response,
            Response1,
            Response2,
            Response3,
            Response4,
            Response6,
            Response7,
            Response8,
            Response9,
            Response10,
            Response11,
        ]
    ] = None
    showActions: Optional[bool] = Field(default=None, description="Show the kebab menu at the end of the row")
    showColumnConfigurator: Optional[bool] = Field(
        default=None, description="Show a button to configure the table's columns if possible"
    )
    showDateRange: Optional[bool] = Field(default=None, description="Show date range selector")
    showElapsedTime: Optional[bool] = Field(default=None, description="Show the time it takes to run a query")
    showEventFilter: Optional[bool] = Field(
        default=None, description="Include an event filter above the table (EventsNode only)"
    )
    showExport: Optional[bool] = Field(default=None, description="Show the export button")
    showTorQLEditor: Optional[bool] = Field(default=None, description="Include a TorQL query editor above TorQL tables")
    showOpenEditorButton: Optional[bool] = Field(
        default=None, description="Show a button to open the current query as a new insight. (default: true)"
    )
    showPersistentColumnConfigurator: Optional[bool] = Field(
        default=None, description="Show a button to configure and persist the table's default columns if possible"
    )
    showPropertyFilter: Optional[Union[bool, list[TaxonomicFilterGroupType]]] = Field(
        default=None, description="Include a property filter above the table"
    )
    showReload: Optional[bool] = Field(default=None, description="Show a reload button")
    showResultsTable: Optional[bool] = Field(default=None, description="Show a results table")
    showSavedQueries: Optional[bool] = Field(default=None, description="Shows a list of saved queries")
    showSearch: Optional[bool] = Field(default=None, description="Include a free text search field (PersonsNode only)")
    showTestAccountFilters: Optional[bool] = Field(default=None, description="Show filter to exclude test accounts")
    showTimings: Optional[bool] = Field(default=None, description="Show a detailed query timing breakdown")
    source: Union[
        EventsNode,
        EventsQuery,
        PersonsNode,
        ActorsQuery,
        TorQLQuery,
        WebOverviewQuery,
        WebStatsTableQuery,
        WebExternalClicksTableQuery,
        WebTopClicksQuery,
        WebGoalsQuery,
        SessionAttributionExplorerQuery,
        ErrorTrackingQuery,
        ExperimentFunnelQuery,
        ExperimentTrendQuery,
    ] = Field(..., description="Source of the events")


class TorQLAutocomplete(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    endPosition: int = Field(..., description="End position of the editor word")
    filters: Optional[TorQLFilters] = Field(default=None, description="Table to validate the expression against")
    globals: Optional[dict[str, Any]] = Field(default=None, description="Global values in scope")
    kind: Literal["TorQLAutocomplete"] = "TorQLAutocomplete"
    language: HogLanguage = Field(..., description="Language to validate")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query: str = Field(..., description="Query to validate")
    response: Optional[TorQLAutocompleteResponse] = None
    sourceQuery: Optional[
        Union[
            EventsNode,
            ActionsNode,
            PersonsNode,
            EventsQuery,
            ActorsQuery,
            InsightActorsQuery,
            InsightActorsQueryOptions,
            SessionsTimelineQuery,
            HogQuery,
            TorQLQuery,
            TorQLMetadata,
            TorQLAutocomplete,
            WebOverviewQuery,
            WebStatsTableQuery,
            WebExternalClicksTableQuery,
            WebTopClicksQuery,
            WebGoalsQuery,
            SessionAttributionExplorerQuery,
            ErrorTrackingQuery,
            ExperimentFunnelQuery,
            ExperimentTrendQuery,
        ]
    ] = Field(default=None, description="Query in whose context to validate.")
    startPosition: int = Field(..., description="Start position of the editor word")


class TorQLMetadata(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    debug: Optional[bool] = Field(
        default=None, description="Enable more verbose output, usually run from the /debug page"
    )
    filters: Optional[TorQLFilters] = Field(default=None, description="Extra filters applied to query via {filters}")
    globals: Optional[dict[str, Any]] = Field(default=None, description="Extra globals for the query")
    kind: Literal["TorQLMetadata"] = "TorQLMetadata"
    language: HogLanguage = Field(..., description="Language to validate")
    modifiers: Optional[TorQLQueryModifiers] = Field(
        default=None, description="Modifiers used when performing the query"
    )
    query: str = Field(..., description="Query to validate")
    response: Optional[TorQLMetadataResponse] = None
    sourceQuery: Optional[
        Union[
            EventsNode,
            ActionsNode,
            PersonsNode,
            EventsQuery,
            ActorsQuery,
            InsightActorsQuery,
            InsightActorsQueryOptions,
            SessionsTimelineQuery,
            HogQuery,
            TorQLQuery,
            TorQLMetadata,
            TorQLAutocomplete,
            WebOverviewQuery,
            WebStatsTableQuery,
            WebExternalClicksTableQuery,
            WebTopClicksQuery,
            WebGoalsQuery,
            SessionAttributionExplorerQuery,
            ErrorTrackingQuery,
            ExperimentFunnelQuery,
            ExperimentTrendQuery,
        ]
    ] = Field(
        default=None,
        description='Query within which "expr" and "template" are validated. Defaults to "select * from events"',
    )
    variables: Optional[dict[str, TorQLVariable]] = Field(
        default=None, description="Variables to be subsituted into the query"
    )


class QueryRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    async_: Optional[bool] = Field(default=None, alias="async")
    client_query_id: Optional[str] = Field(
        default=None, description="Client provided query ID. Can be used to retrieve the status or cancel the query."
    )
    filters_override: Optional[DashboardFilter] = None
    query: Union[
        EventsNode,
        ActionsNode,
        PersonsNode,
        DataWarehouseNode,
        EventsQuery,
        ActorsQuery,
        InsightActorsQuery,
        InsightActorsQueryOptions,
        SessionsTimelineQuery,
        HogQuery,
        TorQLQuery,
        TorQLMetadata,
        TorQLAutocomplete,
        WebOverviewQuery,
        WebStatsTableQuery,
        WebExternalClicksTableQuery,
        WebTopClicksQuery,
        WebGoalsQuery,
        SessionAttributionExplorerQuery,
        ErrorTrackingQuery,
        ExperimentFunnelQuery,
        ExperimentTrendQuery,
        DataVisualizationNode,
        DataTableNode,
        SavedInsightNode,
        InsightVizNode,
        TrendsQuery,
        FunnelsQuery,
        RetentionQuery,
        PathsQuery,
        StickinessQuery,
        LifecycleQuery,
        FunnelCorrelationQuery,
        DatabaseSchemaQuery,
    ] = Field(
        ...,
        description=(
            "Submit a JSON string representing a query for ClairView data analysis, for example a TorQL query.\n\nExample"
            ' payload:\n\n```\n\n{"query": {"kind": "TorQLQuery", "query": "select * from events limit'
            ' 100"}}\n\n```\n\nFor more details on TorQL queries, see the [ClairView TorQL'
            " documentation](/docs/torql#api-access)."
        ),
        discriminator="kind",
    )
    refresh: Optional[Union[bool, str]] = Field(
        default="blocking",
        description=(
            "Whether results should be calculated sync or async, and how much to rely on the cache:\n- `'blocking'` -"
            " calculate synchronously (returning only when the query is done), UNLESS there are very fresh results in"
            " the cache\n- `'async'` - kick off background calculation (returning immediately with a query status),"
            " UNLESS there are very fresh results in the cache\n- `'lazy_async'` - kick off background calculation,"
            " UNLESS there are somewhat fresh results in the cache\n- `'force_blocking'` - calculate synchronously,"
            " even if fresh results are already cached\n- `'force_async'` - kick off background calculation, even if"
            " fresh results are already cached\n- `'force_cache'` - return cached data or a cache miss; always"
            " completes immediately as it never calculates Background calculation can be tracked using the"
            " `query_status` response field."
        ),
    )


class QuerySchemaRoot(
    RootModel[
        Union[
            EventsNode,
            ActionsNode,
            PersonsNode,
            DataWarehouseNode,
            EventsQuery,
            ActorsQuery,
            InsightActorsQuery,
            InsightActorsQueryOptions,
            SessionsTimelineQuery,
            HogQuery,
            TorQLQuery,
            TorQLMetadata,
            TorQLAutocomplete,
            WebOverviewQuery,
            WebStatsTableQuery,
            WebExternalClicksTableQuery,
            WebTopClicksQuery,
            WebGoalsQuery,
            SessionAttributionExplorerQuery,
            ErrorTrackingQuery,
            ExperimentFunnelQuery,
            ExperimentTrendQuery,
            DataVisualizationNode,
            DataTableNode,
            SavedInsightNode,
            InsightVizNode,
            TrendsQuery,
            FunnelsQuery,
            RetentionQuery,
            PathsQuery,
            StickinessQuery,
            LifecycleQuery,
            FunnelCorrelationQuery,
            DatabaseSchemaQuery,
        ]
    ]
):
    root: Union[
        EventsNode,
        ActionsNode,
        PersonsNode,
        DataWarehouseNode,
        EventsQuery,
        ActorsQuery,
        InsightActorsQuery,
        InsightActorsQueryOptions,
        SessionsTimelineQuery,
        HogQuery,
        TorQLQuery,
        TorQLMetadata,
        TorQLAutocomplete,
        WebOverviewQuery,
        WebStatsTableQuery,
        WebExternalClicksTableQuery,
        WebTopClicksQuery,
        WebGoalsQuery,
        SessionAttributionExplorerQuery,
        ErrorTrackingQuery,
        ExperimentFunnelQuery,
        ExperimentTrendQuery,
        DataVisualizationNode,
        DataTableNode,
        SavedInsightNode,
        InsightVizNode,
        TrendsQuery,
        FunnelsQuery,
        RetentionQuery,
        PathsQuery,
        StickinessQuery,
        LifecycleQuery,
        FunnelCorrelationQuery,
        DatabaseSchemaQuery,
    ] = Field(..., discriminator="kind")


PropertyGroupFilterValue.model_rebuild()
QueryRequest.model_rebuild()