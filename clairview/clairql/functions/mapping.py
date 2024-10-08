from dataclasses import dataclass
from itertools import chain
from typing import Optional

from clairview.cloud_utils import is_cloud, is_ci
from clairview.clairql import ast
from clairview.clairql.ast import (
    ArrayType,
    BooleanType,
    DateTimeType,
    DateType,
    FloatType,
    StringType,
    TupleType,
    IntegerType,
    UUIDType,
)
from clairview.clairql.base import ConstantType, UnknownType
from clairview.clairql.errors import QueryError


def validate_function_args(
    args: list[ast.Expr],
    min_args: int,
    max_args: Optional[int],
    function_name: str,
    *,
    function_term="function",
    argument_term="argument",
):
    too_few = len(args) < min_args
    too_many = max_args is not None and len(args) > max_args
    if min_args == max_args and (too_few or too_many):
        raise QueryError(
            f"{function_term.capitalize()} '{function_name}' expects {min_args} {argument_term}{'s' if min_args != 1 else ''}, found {len(args)}"
        )
    if too_few:
        raise QueryError(
            f"{function_term.capitalize()} '{function_name}' expects at least {min_args} {argument_term}{'s' if min_args != 1 else ''}, found {len(args)}"
        )
    if too_many:
        raise QueryError(
            f"{function_term.capitalize()} '{function_name}' expects at most {max_args} {argument_term}{'s' if max_args != 1 else ''}, found {len(args)}"
        )


Overload = tuple[tuple[type[ConstantType], ...] | type[ConstantType], str]
AnyConstantType = (
    StringType
    | BooleanType
    | DateType
    | DateTimeType
    | UUIDType
    | ArrayType
    | TupleType
    | UnknownType
    | IntegerType
    | FloatType
)


@dataclass()
class ClairQLFunctionMeta:
    clickhouse_name: str
    min_args: int = 0
    max_args: Optional[int] = 0
    min_params: int = 0
    max_params: Optional[int] = 0
    aggregate: bool = False
    overloads: Optional[list[Overload]] = None
    """Overloads allow for using a different ClickHouse function depending on the type of the first arg."""
    tz_aware: bool = False
    """Whether the function is timezone-aware. This means the project timezone will be appended as the last arg."""
    case_sensitive: bool = True
    """Not all ClickHouse functions are case-insensitive. See https://clickhouse.com/docs/en/sql-reference/syntax#keywords."""
    signatures: Optional[list[tuple[tuple[AnyConstantType, ...], AnyConstantType]]] = None
    """Signatures allow for specifying the types of the arguments and the return type of the function."""
    suffix_args: Optional[list[ast.Constant]] = None
    """Additional arguments that are added to the end of the arguments provided by the caller"""


def compare_types(arg_types: list[ConstantType], sig_arg_types: tuple[ConstantType, ...]):
    _sig_arg_types = list(sig_arg_types)
    if len(arg_types) != len(sig_arg_types):
        return False

    for index, arg_type in enumerate(arg_types):
        _sig_arg_type = _sig_arg_types[index]
        if not isinstance(arg_type, _sig_arg_type.__class__):
            return False

    return True


CLAIRQL_COMPARISON_MAPPING: dict[str, ast.CompareOperationOp] = {
    "equals": ast.CompareOperationOp.Eq,
    "notEquals": ast.CompareOperationOp.NotEq,
    "less": ast.CompareOperationOp.Lt,
    "greater": ast.CompareOperationOp.Gt,
    "lessOrEquals": ast.CompareOperationOp.LtEq,
    "greaterOrEquals": ast.CompareOperationOp.GtEq,
    "like": ast.CompareOperationOp.Like,
    "ilike": ast.CompareOperationOp.ILike,
    "notLike": ast.CompareOperationOp.NotLike,
    "notILike": ast.CompareOperationOp.NotILike,
    "in": ast.CompareOperationOp.In,
    "notIn": ast.CompareOperationOp.NotIn,
}

CLAIRQL_CLICKHOUSE_FUNCTIONS: dict[str, ClairQLFunctionMeta] = {
    # arithmetic
    "plus": ClairQLFunctionMeta(
        "plus",
        2,
        2,
        signatures=[
            ((IntegerType(), IntegerType()), IntegerType()),
            ((FloatType(), IntegerType()), FloatType()),
            ((IntegerType(), FloatType()), FloatType()),
            (
                (
                    TupleType(item_types=[IntegerType()], repeat=True),
                    TupleType(item_types=[IntegerType()], repeat=True),
                ),
                TupleType(item_types=[IntegerType()], repeat=True),
            ),
            ((DateTimeType(), IntegerType()), DateTimeType()),
            ((IntegerType(), DateTimeType()), DateTimeType()),
        ],
    ),
    "minus": ClairQLFunctionMeta(
        "minus",
        2,
        2,
        signatures=[
            ((IntegerType(), IntegerType()), IntegerType()),
            ((FloatType(), IntegerType()), FloatType()),
            ((IntegerType(), FloatType()), FloatType()),
            (
                (
                    TupleType(item_types=[IntegerType()], repeat=True),
                    TupleType(item_types=[IntegerType()], repeat=True),
                ),
                TupleType(item_types=[IntegerType()], repeat=True),
            ),
            ((DateTimeType(), IntegerType()), DateTimeType()),
            ((IntegerType(), DateTimeType()), DateTimeType()),
        ],
    ),
    "multiply": ClairQLFunctionMeta(
        "multiply",
        2,
        2,
        signatures=[
            ((IntegerType(), IntegerType()), IntegerType()),
            ((FloatType(), IntegerType()), FloatType()),
            ((IntegerType(), FloatType()), FloatType()),
            (
                (
                    TupleType(item_types=[IntegerType()], repeat=True),
                    TupleType(item_types=[IntegerType()], repeat=True),
                ),
                TupleType(item_types=[IntegerType()], repeat=True),
            ),
            (
                (IntegerType(), TupleType(item_types=[IntegerType()], repeat=True)),
                TupleType(item_types=[IntegerType()], repeat=True),
            ),
            (
                (TupleType(item_types=[IntegerType()], repeat=True), IntegerType()),
                TupleType(item_types=[IntegerType()], repeat=True),
            ),
            ((DateTimeType(), IntegerType()), DateTimeType()),
            ((IntegerType(), DateTimeType()), DateTimeType()),
        ],
    ),
    "divide": ClairQLFunctionMeta(
        "divide",
        2,
        2,
        signatures=[
            ((IntegerType(), IntegerType()), IntegerType()),
            ((FloatType(), IntegerType()), FloatType()),
            ((IntegerType(), FloatType()), FloatType()),
            (
                (TupleType(item_types=[IntegerType()], repeat=True), IntegerType()),
                TupleType(item_types=[IntegerType()], repeat=True),
            ),
            ((DateTimeType(), IntegerType()), DateTimeType()),
            ((IntegerType(), DateTimeType()), DateTimeType()),
        ],
    ),
    "intDiv": ClairQLFunctionMeta(
        "intDiv",
        2,
        2,
        signatures=[
            ((IntegerType(), IntegerType()), IntegerType()),
        ],
    ),
    "intDivOrZero": ClairQLFunctionMeta(
        "intDivOrZero",
        2,
        2,
        signatures=[
            ((IntegerType(), IntegerType()), IntegerType()),
        ],
    ),
    "modulo": ClairQLFunctionMeta(
        "modulo",
        2,
        2,
        signatures=[
            ((IntegerType(), IntegerType()), IntegerType()),
            ((FloatType(), IntegerType()), FloatType()),
            ((IntegerType(), FloatType()), FloatType()),
        ],
    ),
    "moduloOrZero": ClairQLFunctionMeta(
        "moduloOrZero",
        2,
        2,
        signatures=[
            ((IntegerType(), IntegerType()), IntegerType()),
            ((FloatType(), IntegerType()), FloatType()),
            ((IntegerType(), FloatType()), FloatType()),
        ],
    ),
    "positiveModulo": ClairQLFunctionMeta(
        "positiveModulo",
        2,
        2,
        signatures=[
            ((IntegerType(), IntegerType()), IntegerType()),
            ((FloatType(), IntegerType()), FloatType()),
            ((IntegerType(), FloatType()), FloatType()),
        ],
    ),
    "negate": ClairQLFunctionMeta(
        "negate",
        1,
        1,
        signatures=[
            ((IntegerType(),), IntegerType()),
            ((FloatType(),), FloatType()),
        ],
    ),
    "abs": ClairQLFunctionMeta(
        "abs",
        1,
        1,
        signatures=[
            ((IntegerType(),), IntegerType()),
        ],
        case_sensitive=False,
    ),
    "gcd": ClairQLFunctionMeta(
        "gcd",
        2,
        2,
        signatures=[
            ((IntegerType(),), IntegerType()),
        ],
    ),
    "lcm": ClairQLFunctionMeta(
        "lcm",
        2,
        2,
        signatures=[
            ((IntegerType(),), IntegerType()),
        ],
    ),
    "max2": ClairQLFunctionMeta(
        "max2",
        2,
        2,
        signatures=[
            ((IntegerType(), IntegerType()), FloatType()),
            ((FloatType(), IntegerType()), FloatType()),
            ((IntegerType(), FloatType()), FloatType()),
        ],
        case_sensitive=False,
    ),
    "min2": ClairQLFunctionMeta(
        "min2",
        2,
        2,
        signatures=[
            ((IntegerType(), IntegerType()), FloatType()),
            ((FloatType(), IntegerType()), FloatType()),
            ((IntegerType(), FloatType()), FloatType()),
        ],
        case_sensitive=False,
    ),
    "multiplyDecimal": ClairQLFunctionMeta("multiplyDecimal", 2, 3),
    "divideDecimal": ClairQLFunctionMeta("divideDecimal", 2, 3),
    # arrays and strings common
    "empty": ClairQLFunctionMeta("empty", 1, 1),
    "notEmpty": ClairQLFunctionMeta("notEmpty", 1, 1),
    "length": ClairQLFunctionMeta("length", 1, 1, case_sensitive=False),
    "reverse": ClairQLFunctionMeta("reverse", 1, 1, case_sensitive=False),
    # arrays
    "array": ClairQLFunctionMeta("array", 0, None),
    "range": ClairQLFunctionMeta("range", 1, 3),
    "arrayConcat": ClairQLFunctionMeta("arrayConcat", 2, None),
    "arrayElement": ClairQLFunctionMeta("arrayElement", 2, 2),
    "has": ClairQLFunctionMeta("has", 2, 2),
    "hasAll": ClairQLFunctionMeta("hasAll", 2, 2),
    "hasAny": ClairQLFunctionMeta("hasAny", 2, 2),
    "hasSubstr": ClairQLFunctionMeta("hasSubstr", 2, 2),
    "indexOf": ClairQLFunctionMeta("indexOf", 2, 2),
    "arrayCount": ClairQLFunctionMeta("arrayCount", 1, None),
    "countEqual": ClairQLFunctionMeta("countEqual", 2, 2),
    "arrayEnumerate": ClairQLFunctionMeta("arrayEnumerate", 1, 1),
    "arrayEnumerateUniq": ClairQLFunctionMeta("arrayEnumerateUniq", 2, None),
    "arrayPopBack": ClairQLFunctionMeta("arrayPopBack", 1, 1),
    "arrayPopFront": ClairQLFunctionMeta("arrayPopFront", 1, 1),
    "arrayPushBack": ClairQLFunctionMeta("arrayPushBack", 2, 2),
    "arrayPushFront": ClairQLFunctionMeta("arrayPushFront", 2, 2),
    "arrayResize": ClairQLFunctionMeta("arrayResize", 2, 3),
    "arraySlice": ClairQLFunctionMeta("arraySlice", 2, 3),
    "arraySort": ClairQLFunctionMeta("arraySort", 1, None),
    "arrayReverseSort": ClairQLFunctionMeta("arraySort", 1, None),
    "arrayUniq": ClairQLFunctionMeta("arrayUniq", 1, None),
    "arrayJoin": ClairQLFunctionMeta("arrayJoin", 1, 1),
    "arrayDifference": ClairQLFunctionMeta("arrayDifference", 1, 1),
    "arrayDistinct": ClairQLFunctionMeta("arrayDistinct", 1, 1),
    "arrayEnumerateDense": ClairQLFunctionMeta("arrayEnumerateDense", 1, 1),
    "arrayIntersect": ClairQLFunctionMeta("arrayIntersect", 1, None),
    # "arrayReduce": ClairQLFunctionMeta("arrayReduce", 2,None),  # takes a "parametric function" as first arg, is that safe?
    # "arrayReduceInRanges": ClairQLFunctionMeta("arrayReduceInRanges", 3,None),  # takes a "parametric function" as first arg, is that safe?
    "arrayReverse": ClairQLFunctionMeta("arrayReverse", 1, 1),
    "arrayFilter": ClairQLFunctionMeta("arrayFilter", 2, None),
    "arrayFlatten": ClairQLFunctionMeta("arrayFlatten", 1, 1),
    "arrayCompact": ClairQLFunctionMeta("arrayCompact", 1, 1),
    "arrayZip": ClairQLFunctionMeta("arrayZip", 2, None),
    "arrayAUC": ClairQLFunctionMeta("arrayAUC", 2, 2),
    "arrayMap": ClairQLFunctionMeta("arrayMap", 2, None),
    "arrayFill": ClairQLFunctionMeta("arrayFill", 2, None),
    "arrayFold": ClairQLFunctionMeta("arrayFold", 3, None),
    "arrayWithConstant": ClairQLFunctionMeta("arrayWithConstant", 2, 2),
    "arraySplit": ClairQLFunctionMeta("arraySplit", 2, None),
    "arrayReverseFill": ClairQLFunctionMeta("arrayReverseFill", 2, None),
    "arrayReverseSplit": ClairQLFunctionMeta("arrayReverseSplit", 2, None),
    "arrayExists": ClairQLFunctionMeta("arrayExists", 1, None),
    "arrayAll": ClairQLFunctionMeta("arrayAll", 1, None),
    "arrayFirst": ClairQLFunctionMeta("arrayFirst", 2, None),
    "arrayLast": ClairQLFunctionMeta("arrayLast", 2, None),
    "arrayFirstIndex": ClairQLFunctionMeta("arrayFirstIndex", 2, None),
    "arrayLastIndex": ClairQLFunctionMeta("arrayLastIndex", 2, None),
    "arrayMin": ClairQLFunctionMeta("arrayMin", 1, 2),
    "arrayMax": ClairQLFunctionMeta("arrayMax", 1, 2),
    "arraySum": ClairQLFunctionMeta("arraySum", 1, 2),
    "arrayAvg": ClairQLFunctionMeta("arrayAvg", 1, 2),
    "arrayCumSum": ClairQLFunctionMeta("arrayCumSum", 1, None),
    "arrayCumSumNonNegative": ClairQLFunctionMeta("arrayCumSumNonNegative", 1, None),
    "arrayProduct": ClairQLFunctionMeta("arrayProduct", 1, 1),
    # comparison
    "equals": ClairQLFunctionMeta("equals", 2, 2),
    "notEquals": ClairQLFunctionMeta("notEquals", 2, 2),
    "less": ClairQLFunctionMeta("less", 2, 2),
    "greater": ClairQLFunctionMeta("greater", 2, 2),
    "lessOrEquals": ClairQLFunctionMeta("lessOrEquals", 2, 2),
    "greaterOrEquals": ClairQLFunctionMeta("greaterOrEquals", 2, 2),
    # logical
    "and": ClairQLFunctionMeta("and", 2, None),
    "or": ClairQLFunctionMeta("or", 2, None),
    "xor": ClairQLFunctionMeta("xor", 2, None),
    "not": ClairQLFunctionMeta("not", 1, 1, case_sensitive=False),
    # type conversions
    "hex": ClairQLFunctionMeta("hex", 1, 1),
    "unhex": ClairQLFunctionMeta("unhex", 1, 1),
    # instead of just "reinterpret" we use specific list of "reinterpretAs*"" functions
    # that we know are safe to use to minimize the security risk
    "reinterpretAsUInt8": ClairQLFunctionMeta("reinterpretAsUInt8", 1, 1),
    "reinterpretAsUInt16": ClairQLFunctionMeta("reinterpretAsUInt16", 1, 1),
    "reinterpretAsUInt32": ClairQLFunctionMeta("reinterpretAsUInt32", 1, 1),
    "reinterpretAsUInt64": ClairQLFunctionMeta("reinterpretAsUInt64", 1, 1),
    "reinterpretAsUInt128": ClairQLFunctionMeta("reinterpretAsUInt128", 1, 1),
    "reinterpretAsUInt256": ClairQLFunctionMeta("reinterpretAsUInt256", 1, 1),
    "reinterpretAsInt8": ClairQLFunctionMeta("reinterpretAsInt8", 1, 1),
    "reinterpretAsInt16": ClairQLFunctionMeta("reinterpretAsInt16", 1, 1),
    "reinterpretAsInt32": ClairQLFunctionMeta("reinterpretAsInt32", 1, 1),
    "reinterpretAsInt64": ClairQLFunctionMeta("reinterpretAsInt64", 1, 1),
    "reinterpretAsInt128": ClairQLFunctionMeta("reinterpretAsInt128", 1, 1),
    "reinterpretAsInt256": ClairQLFunctionMeta("reinterpretAsInt256", 1, 1),
    "reinterpretAsFloat32": ClairQLFunctionMeta("reinterpretAsFloat32", 1, 1),
    "reinterpretAsFloat64": ClairQLFunctionMeta("reinterpretAsFloat64", 1, 1),
    "reinterpretAsUUID": ClairQLFunctionMeta("reinterpretAsUUID", 1, 1),
    "toInt": ClairQLFunctionMeta("accurateCastOrNull", 1, 1, suffix_args=[ast.Constant(value="Int64")]),
    "_toInt64": ClairQLFunctionMeta("toInt64", 1, 1),
    "_toUInt64": ClairQLFunctionMeta("toUInt64", 1, 1),
    "_toUInt128": ClairQLFunctionMeta("toUInt128", 1, 1),
    "toFloat": ClairQLFunctionMeta("accurateCastOrNull", 1, 1, suffix_args=[ast.Constant(value="Float64")]),
    "toDecimal": ClairQLFunctionMeta("accurateCastOrNull", 1, 1, suffix_args=[ast.Constant(value="Decimal64")]),
    "toDate": ClairQLFunctionMeta(
        "toDateOrNull",
        1,
        1,
        overloads=[((ast.DateTimeType, ast.DateType), "toDate")],
    ),
    "toDateTime": ClairQLFunctionMeta(
        "parseDateTime64BestEffortOrNull",
        1,
        2,
        tz_aware=True,
        overloads=[((ast.DateTimeType, ast.DateType, ast.IntegerType), "toDateTime")],
        signatures=[
            ((StringType(),), DateTimeType(nullable=True)),
            ((StringType(), IntegerType()), DateTimeType(nullable=True)),
            ((StringType(), IntegerType(), StringType()), DateTimeType(nullable=True)),
        ],
    ),
    "toUUID": ClairQLFunctionMeta("accurateCastOrNull", 1, 1, suffix_args=[ast.Constant(value="UUID")]),
    "toString": ClairQLFunctionMeta(
        "toString",
        1,
        1,
        signatures=[
            ((IntegerType(),), StringType()),
            ((StringType(),), StringType()),
            ((FloatType(),), StringType()),
            ((DateType(),), StringType()),
            ((DateTimeType(),), StringType()),
        ],
    ),
    "toJSONString": ClairQLFunctionMeta("toJSONString", 1, 1),
    "parseDateTime": ClairQLFunctionMeta("parseDateTimeOrNull", 2, 3, tz_aware=True),
    "parseDateTimeBestEffort": ClairQLFunctionMeta("parseDateTime64BestEffortOrNull", 1, 2, tz_aware=True),
    "toTypeName": ClairQLFunctionMeta("toTypeName", 1, 1),
    "cityHash64": ClairQLFunctionMeta("cityHash64", 1, 1),
    # dates and times
    "toTimeZone": ClairQLFunctionMeta("toTimeZone", 2, 2),
    "timeZoneOf": ClairQLFunctionMeta("timeZoneOf", 1, 1),
    "timeZoneOffset": ClairQLFunctionMeta("timeZoneOffset", 1, 1),
    "toYear": ClairQLFunctionMeta("toYear", 1, 1),
    "toQuarter": ClairQLFunctionMeta("toQuarter", 1, 1),
    "toMonth": ClairQLFunctionMeta("toMonth", 1, 1),
    "toDayOfYear": ClairQLFunctionMeta("toDayOfYear", 1, 1),
    "toDayOfMonth": ClairQLFunctionMeta("toDayOfMonth", 1, 1),
    "toDayOfWeek": ClairQLFunctionMeta("toDayOfWeek", 1, 3),
    "toHour": ClairQLFunctionMeta("toHour", 1, 1),
    "toMinute": ClairQLFunctionMeta("toMinute", 1, 1),
    "toSecond": ClairQLFunctionMeta("toSecond", 1, 1),
    "toUnixTimestamp": ClairQLFunctionMeta("toUnixTimestamp", 1, 2),
    "toUnixTimestamp64Milli": ClairQLFunctionMeta("toUnixTimestamp64Milli", 1, 1),
    "toStartOfYear": ClairQLFunctionMeta("toStartOfYear", 1, 1),
    "toStartOfISOYear": ClairQLFunctionMeta("toStartOfISOYear", 1, 1),
    "toStartOfQuarter": ClairQLFunctionMeta("toStartOfQuarter", 1, 1),
    "toStartOfMonth": ClairQLFunctionMeta("toStartOfMonth", 1, 1),
    "toLastDayOfMonth": ClairQLFunctionMeta("toLastDayOfMonth", 1, 1),
    "toMonday": ClairQLFunctionMeta("toMonday", 1, 1),
    "toStartOfWeek": ClairQLFunctionMeta("toStartOfWeek", 1, 2),
    "toStartOfDay": ClairQLFunctionMeta("toStartOfDay", 1, 2),
    "toLastDayOfWeek": ClairQLFunctionMeta("toLastDayOfWeek", 1, 2),
    "toStartOfHour": ClairQLFunctionMeta("toStartOfHour", 1, 1),
    "toStartOfMinute": ClairQLFunctionMeta("toStartOfMinute", 1, 1),
    "toStartOfSecond": ClairQLFunctionMeta("toStartOfSecond", 1, 1),
    "toStartOfFiveMinutes": ClairQLFunctionMeta("toStartOfFiveMinutes", 1, 1),
    "toStartOfTenMinutes": ClairQLFunctionMeta("toStartOfTenMinutes", 1, 1),
    "toStartOfFifteenMinutes": ClairQLFunctionMeta("toStartOfFifteenMinutes", 1, 1),
    "toTime": ClairQLFunctionMeta("toTime", 1, 1),
    "toISOYear": ClairQLFunctionMeta("toISOYear", 1, 1),
    "toISOWeek": ClairQLFunctionMeta("toISOWeek", 1, 1),
    "toWeek": ClairQLFunctionMeta("toWeek", 1, 3),
    "toYearWeek": ClairQLFunctionMeta("toYearWeek", 1, 3),
    "age": ClairQLFunctionMeta("age", 3, 3),
    "dateDiff": ClairQLFunctionMeta("dateDiff", 3, 3),
    "dateTrunc": ClairQLFunctionMeta("dateTrunc", 2, 2),
    "dateAdd": ClairQLFunctionMeta("dateAdd", 2, 2),
    "dateSub": ClairQLFunctionMeta("dateSub", 3, 3),
    "timeStampAdd": ClairQLFunctionMeta("timeStampAdd", 2, 2),
    "timeStampSub": ClairQLFunctionMeta("timeStampSub", 2, 2),
    "now": ClairQLFunctionMeta("now64", 0, 1, tz_aware=True, case_sensitive=False),
    "nowInBlock": ClairQLFunctionMeta("nowInBlock", 1, 1),
    "rowNumberInBlock": ClairQLFunctionMeta("rowNumberInBlock", 0, 0),
    "rowNumberInAllBlocks": ClairQLFunctionMeta("rowNumberInAllBlocks", 0, 0),
    "today": ClairQLFunctionMeta("today"),
    "yesterday": ClairQLFunctionMeta("yesterday"),
    "timeSlot": ClairQLFunctionMeta("timeSlot", 1, 1),
    "toYYYYMM": ClairQLFunctionMeta("toYYYYMM", 1, 1),
    "toYYYYMMDD": ClairQLFunctionMeta("toYYYYMMDD", 1, 1),
    "toYYYYMMDDhhmmss": ClairQLFunctionMeta("toYYYYMMDDhhmmss", 1, 1),
    "addYears": ClairQLFunctionMeta("addYears", 2, 2),
    "addMonths": ClairQLFunctionMeta("addMonths", 2, 2),
    "addWeeks": ClairQLFunctionMeta("addWeeks", 2, 2),
    "addDays": ClairQLFunctionMeta("addDays", 2, 2),
    "addHours": ClairQLFunctionMeta("addHours", 2, 2),
    "addMinutes": ClairQLFunctionMeta("addMinutes", 2, 2),
    "addSeconds": ClairQLFunctionMeta("addSeconds", 2, 2),
    "addQuarters": ClairQLFunctionMeta("addQuarters", 2, 2),
    "subtractYears": ClairQLFunctionMeta("subtractYears", 2, 2),
    "subtractMonths": ClairQLFunctionMeta("subtractMonths", 2, 2),
    "subtractWeeks": ClairQLFunctionMeta("subtractWeeks", 2, 2),
    "subtractDays": ClairQLFunctionMeta("subtractDays", 2, 2),
    "subtractHours": ClairQLFunctionMeta("subtractHours", 2, 2),
    "subtractMinutes": ClairQLFunctionMeta("subtractMinutes", 2, 2),
    "subtractSeconds": ClairQLFunctionMeta("subtractSeconds", 2, 2),
    "subtractQuarters": ClairQLFunctionMeta("subtractQuarters", 2, 2),
    "timeSlots": ClairQLFunctionMeta("timeSlots", 2, 3),
    "formatDateTime": ClairQLFunctionMeta("formatDateTime", 2, 3),
    "dateName": ClairQLFunctionMeta("dateName", 2, 2),
    "monthName": ClairQLFunctionMeta("monthName", 1, 1),
    "fromUnixTimestamp": ClairQLFunctionMeta(
        "fromUnixTimestamp",
        1,
        1,
        signatures=[
            ((IntegerType(),), DateTimeType()),
        ],
    ),
    "toModifiedJulianDay": ClairQLFunctionMeta("toModifiedJulianDayOrNull", 1, 1),
    "fromModifiedJulianDay": ClairQLFunctionMeta("fromModifiedJulianDayOrNull", 1, 1),
    "toIntervalSecond": ClairQLFunctionMeta("toIntervalSecond", 1, 1),
    "toIntervalMinute": ClairQLFunctionMeta("toIntervalMinute", 1, 1),
    "toIntervalHour": ClairQLFunctionMeta("toIntervalHour", 1, 1),
    "toIntervalDay": ClairQLFunctionMeta("toIntervalDay", 1, 1),
    "toIntervalWeek": ClairQLFunctionMeta("toIntervalWeek", 1, 1),
    "toIntervalMonth": ClairQLFunctionMeta("toIntervalMonth", 1, 1),
    "toIntervalQuarter": ClairQLFunctionMeta("toIntervalQuarter", 1, 1),
    "toIntervalYear": ClairQLFunctionMeta("toIntervalYear", 1, 1),
    # strings
    "left": ClairQLFunctionMeta("left", 2, 2),
    "right": ClairQLFunctionMeta("right", 2, 2),
    "lengthUTF8": ClairQLFunctionMeta("lengthUTF8", 1, 1),
    "leftPad": ClairQLFunctionMeta("leftPad", 2, 3),
    "rightPad": ClairQLFunctionMeta("rightPad", 2, 3),
    "leftPadUTF8": ClairQLFunctionMeta("leftPadUTF8", 2, 3),
    "rightPadUTF8": ClairQLFunctionMeta("rightPadUTF8", 2, 3),
    "lower": ClairQLFunctionMeta("lower", 1, 1, case_sensitive=False),
    "upper": ClairQLFunctionMeta("upper", 1, 1, case_sensitive=False),
    "lowerUTF8": ClairQLFunctionMeta("lowerUTF8", 1, 1),
    "upperUTF8": ClairQLFunctionMeta("upperUTF8", 1, 1),
    "isValidUTF8": ClairQLFunctionMeta("isValidUTF8", 1, 1),
    "toValidUTF8": ClairQLFunctionMeta("toValidUTF8", 1, 1),
    "repeat": ClairQLFunctionMeta("repeat", 2, 2, case_sensitive=False),
    "format": ClairQLFunctionMeta("format", 2, None),
    "reverseUTF8": ClairQLFunctionMeta("reverseUTF8", 1, 1),
    "concat": ClairQLFunctionMeta("concat", 2, None, case_sensitive=False),
    "substring": ClairQLFunctionMeta("substring", 3, 3, case_sensitive=False),
    "substringUTF8": ClairQLFunctionMeta("substringUTF8", 3, 3),
    "appendTrailingCharIfAbsent": ClairQLFunctionMeta("appendTrailingCharIfAbsent", 2, 2),
    "convertCharset": ClairQLFunctionMeta("convertCharset", 3, 3),
    "base58Encode": ClairQLFunctionMeta("base58Encode", 1, 1),
    "base58Decode": ClairQLFunctionMeta("base58Decode", 1, 1),
    "tryBase58Decode": ClairQLFunctionMeta("tryBase58Decode", 1, 1),
    "base64Encode": ClairQLFunctionMeta("base64Encode", 1, 1),
    "base64Decode": ClairQLFunctionMeta("base64Decode", 1, 1),
    "tryBase64Decode": ClairQLFunctionMeta("tryBase64Decode", 1, 1),
    "endsWith": ClairQLFunctionMeta("endsWith", 2, 2),
    "startsWith": ClairQLFunctionMeta("startsWith", 2, 2),
    "trim": ClairQLFunctionMeta("trim", 1, 2, case_sensitive=False),
    "trimLeft": ClairQLFunctionMeta("trimLeft", 1, 2),
    "trimRight": ClairQLFunctionMeta("trimRight", 1, 2),
    "encodeXMLComponent": ClairQLFunctionMeta("encodeXMLComponent", 1, 1),
    "decodeXMLComponent": ClairQLFunctionMeta("decodeXMLComponent", 1, 1),
    "extractTextFromHTML": ClairQLFunctionMeta("extractTextFromHTML", 1, 1),
    "ascii": ClairQLFunctionMeta("ascii", 1, 1, case_sensitive=False),
    "concatWithSeparator": ClairQLFunctionMeta("concatWithSeparator", 2, None),
    # searching in strings
    "position": ClairQLFunctionMeta("position", 2, 3, case_sensitive=False),
    "positionCaseInsensitive": ClairQLFunctionMeta("positionCaseInsensitive", 2, 3),
    "positionUTF8": ClairQLFunctionMeta("positionUTF8", 2, 3),
    "positionCaseInsensitiveUTF8": ClairQLFunctionMeta("positionCaseInsensitiveUTF8", 2, 3),
    "multiSearchAllPositions": ClairQLFunctionMeta("multiSearchAllPositions", 2, 2),
    "multiSearchAllPositionsUTF8": ClairQLFunctionMeta("multiSearchAllPositionsUTF8", 2, 2),
    "multiSearchFirstPosition": ClairQLFunctionMeta("multiSearchFirstPosition", 2, 2),
    "multiSearchFirstIndex": ClairQLFunctionMeta("multiSearchFirstIndex", 2, 2),
    "multiSearchAny": ClairQLFunctionMeta("multiSearchAny", 2, 2),
    "match": ClairQLFunctionMeta("match", 2, 2),
    "multiMatchAny": ClairQLFunctionMeta("multiMatchAny", 2, 2),
    "multiMatchAnyIndex": ClairQLFunctionMeta("multiMatchAnyIndex", 2, 2),
    "multiMatchAllIndices": ClairQLFunctionMeta("multiMatchAllIndices", 2, 2),
    "multiFuzzyMatchAny": ClairQLFunctionMeta("multiFuzzyMatchAny", 3, 3),
    "multiFuzzyMatchAnyIndex": ClairQLFunctionMeta("multiFuzzyMatchAnyIndex", 3, 3),
    "multiFuzzyMatchAllIndices": ClairQLFunctionMeta("multiFuzzyMatchAllIndices", 3, 3),
    "extract": ClairQLFunctionMeta("extract", 2, 2, case_sensitive=False),
    "extractAll": ClairQLFunctionMeta("extractAll", 2, 2),
    "extractAllGroupsHorizontal": ClairQLFunctionMeta("extractAllGroupsHorizontal", 2, 2),
    "extractAllGroupsVertical": ClairQLFunctionMeta("extractAllGroupsVertical", 2, 2),
    "like": ClairQLFunctionMeta("like", 2, 2),
    "ilike": ClairQLFunctionMeta("ilike", 2, 2),
    "notLike": ClairQLFunctionMeta("notLike", 2, 2),
    "notILike": ClairQLFunctionMeta("notILike", 2, 2),
    "ngramDistance": ClairQLFunctionMeta("ngramDistance", 2, 2),
    "ngramSearch": ClairQLFunctionMeta("ngramSearch", 2, 2),
    "countSubstrings": ClairQLFunctionMeta("countSubstrings", 2, 3),
    "countSubstringsCaseInsensitive": ClairQLFunctionMeta("countSubstringsCaseInsensitive", 2, 3),
    "countSubstringsCaseInsensitiveUTF8": ClairQLFunctionMeta("countSubstringsCaseInsensitiveUTF8", 2, 3),
    "countMatches": ClairQLFunctionMeta("countMatches", 2, 2),
    "regexpExtract": ClairQLFunctionMeta("regexpExtract", 2, 3),
    # replacing in strings
    "replace": ClairQLFunctionMeta("replace", 3, 3, case_sensitive=False),
    "replaceAll": ClairQLFunctionMeta("replaceAll", 3, 3),
    "replaceOne": ClairQLFunctionMeta("replaceOne", 3, 3),
    "replaceRegexpAll": ClairQLFunctionMeta("replaceRegexpAll", 3, 3),
    "replaceRegexpOne": ClairQLFunctionMeta("replaceRegexpOne", 3, 3),
    "regexpQuoteMeta": ClairQLFunctionMeta("regexpQuoteMeta", 1, 1),
    "translate": ClairQLFunctionMeta("translate", 3, 3),
    "translateUTF8": ClairQLFunctionMeta("translateUTF8", 3, 3),
    # conditional
    "if": ClairQLFunctionMeta("if", 3, 3, case_sensitive=False),
    "multiIf": ClairQLFunctionMeta("multiIf", 3, None),
    # mathematical
    "e": ClairQLFunctionMeta("e"),
    "pi": ClairQLFunctionMeta("pi"),
    "exp": ClairQLFunctionMeta("exp", 1, 1, case_sensitive=False),
    "log": ClairQLFunctionMeta("log", 1, 1, case_sensitive=False),
    "ln": ClairQLFunctionMeta("ln", 1, 1, case_sensitive=False),
    "exp2": ClairQLFunctionMeta("exp2", 1, 1),
    "log2": ClairQLFunctionMeta("log2", 1, 1, case_sensitive=False),
    "exp10": ClairQLFunctionMeta("exp10", 1, 1),
    "log10": ClairQLFunctionMeta("log10", 1, 1, case_sensitive=False),
    "sqrt": ClairQLFunctionMeta("sqrt", 1, 1, case_sensitive=False),
    "cbrt": ClairQLFunctionMeta("cbrt", 1, 1),
    "erf": ClairQLFunctionMeta("erf", 1, 1),
    "erfc": ClairQLFunctionMeta("erfc", 1, 1),
    "lgamma": ClairQLFunctionMeta("lgamma", 1, 1),
    "tgamma": ClairQLFunctionMeta("tgamma", 1, 1),
    "sin": ClairQLFunctionMeta("sin", 1, 1, case_sensitive=False),
    "cos": ClairQLFunctionMeta("cos", 1, 1, case_sensitive=False),
    "tan": ClairQLFunctionMeta("tan", 1, 1, case_sensitive=False),
    "asin": ClairQLFunctionMeta("asin", 1, 1, case_sensitive=False),
    "acos": ClairQLFunctionMeta("acos", 1, 1, case_sensitive=False),
    "atan": ClairQLFunctionMeta("atan", 1, 1, case_sensitive=False),
    "pow": ClairQLFunctionMeta("pow", 2, 2, case_sensitive=False),
    "power": ClairQLFunctionMeta("power", 2, 2, case_sensitive=False),
    "intExp2": ClairQLFunctionMeta("intExp2", 1, 1),
    "intExp10": ClairQLFunctionMeta("intExp10", 1, 1),
    "cosh": ClairQLFunctionMeta("cosh", 1, 1),
    "acosh": ClairQLFunctionMeta("acosh", 1, 1),
    "sinh": ClairQLFunctionMeta("sinh", 1, 1),
    "asinh": ClairQLFunctionMeta("asinh", 1, 1),
    "atanh": ClairQLFunctionMeta("atanh", 1, 1),
    "atan2": ClairQLFunctionMeta("atan2", 2, 2),
    "hypot": ClairQLFunctionMeta("hypot", 2, 2),
    "log1p": ClairQLFunctionMeta("log1p", 1, 1),
    "sign": ClairQLFunctionMeta("sign", 1, 1, case_sensitive=False),
    "degrees": ClairQLFunctionMeta("degrees", 1, 1, case_sensitive=False),
    "radians": ClairQLFunctionMeta("radians", 1, 1, case_sensitive=False),
    "factorial": ClairQLFunctionMeta("factorial", 1, 1, case_sensitive=False),
    "width_bucket": ClairQLFunctionMeta("width_bucket", 4, 4),
    # rounding
    "floor": ClairQLFunctionMeta("floor", 1, 2, case_sensitive=False),
    "ceil": ClairQLFunctionMeta("ceil", 1, 2, case_sensitive=False),
    "trunc": ClairQLFunctionMeta("trunc", 1, 2, case_sensitive=False),
    "round": ClairQLFunctionMeta("round", 1, 2, case_sensitive=False),
    "roundBankers": ClairQLFunctionMeta("roundBankers", 1, 2),
    "roundToExp2": ClairQLFunctionMeta("roundToExp2", 1, 1),
    "roundDuration": ClairQLFunctionMeta("roundDuration", 1, 1),
    "roundAge": ClairQLFunctionMeta("roundAge", 1, 1),
    "roundDown": ClairQLFunctionMeta("roundDown", 2, 2),
    # maps
    "map": ClairQLFunctionMeta("map", 2, None),
    "mapFromArrays": ClairQLFunctionMeta("mapFromArrays", 2, 2),
    "mapAdd": ClairQLFunctionMeta("mapAdd", 2, None),
    "mapSubtract": ClairQLFunctionMeta("mapSubtract", 2, None),
    "mapPopulateSeries": ClairQLFunctionMeta("mapPopulateSeries", 1, 3),
    "mapContains": ClairQLFunctionMeta("mapContains", 2, 2),
    "mapKeys": ClairQLFunctionMeta("mapKeys", 1, 1),
    "mapValues": ClairQLFunctionMeta("mapValues", 1, 1),
    "mapContainsKeyLike": ClairQLFunctionMeta("mapContainsKeyLike", 2, 2),
    "mapExtractKeyLike": ClairQLFunctionMeta("mapExtractKeyLike", 2, 2),
    "mapApply": ClairQLFunctionMeta("mapApply", 2, 2),
    "mapFilter": ClairQLFunctionMeta("mapFilter", 2, 2),
    "mapUpdate": ClairQLFunctionMeta("mapUpdate", 2, 2),
    # splitting strings
    "splitByChar": ClairQLFunctionMeta("splitByChar", 2, 3),
    "splitByString": ClairQLFunctionMeta("splitByString", 2, 3),
    "splitByRegexp": ClairQLFunctionMeta("splitByRegexp", 2, 3),
    "splitByWhitespace": ClairQLFunctionMeta("splitByWhitespace", 1, 2),
    "splitByNonAlpha": ClairQLFunctionMeta("splitByNonAlpha", 1, 2),
    "arrayStringConcat": ClairQLFunctionMeta("arrayStringConcat", 1, 2),
    "alphaTokens": ClairQLFunctionMeta("alphaTokens", 1, 2),
    "extractAllGroups": ClairQLFunctionMeta("extractAllGroups", 2, 2),
    "ngrams": ClairQLFunctionMeta("ngrams", 2, 2),
    "tokens": ClairQLFunctionMeta("tokens", 1, 1),
    # bit
    "bitAnd": ClairQLFunctionMeta("bitAnd", 2, 2),
    "bitOr": ClairQLFunctionMeta("bitOr", 2, 2),
    "bitXor": ClairQLFunctionMeta("bitXor", 2, 2),
    "bitNot": ClairQLFunctionMeta("bitNot", 1, 1),
    "bitShiftLeft": ClairQLFunctionMeta("bitShiftLeft", 2, 2),
    "bitShiftRight": ClairQLFunctionMeta("bitShiftRight", 2, 2),
    "bitRotateLeft": ClairQLFunctionMeta("bitRotateLeft", 2, 2),
    "bitRotateRight": ClairQLFunctionMeta("bitRotateRight", 2, 2),
    "bitSlice": ClairQLFunctionMeta("bitSlice", 3, 3),
    "bitTest": ClairQLFunctionMeta("bitTest", 2, 2),
    "bitTestAll": ClairQLFunctionMeta("bitTestAll", 3, None),
    "bitTestAny": ClairQLFunctionMeta("bitTestAny", 3, None),
    "bitCount": ClairQLFunctionMeta("bitCount", 1, 1),
    "bitHammingDistance": ClairQLFunctionMeta("bitHammingDistance", 2, 2),
    # bitmap
    "bitmapBuild": ClairQLFunctionMeta("bitmapBuild", 1, 1),
    "bitmapToArray": ClairQLFunctionMeta("bitmapToArray", 1, 1),
    "bitmapSubsetInRange": ClairQLFunctionMeta("bitmapSubsetInRange", 3, 3),
    "bitmapSubsetLimit": ClairQLFunctionMeta("bitmapSubsetLimit", 3, 3),
    "subBitmap": ClairQLFunctionMeta("subBitmap", 3, 3),
    "bitmapContains": ClairQLFunctionMeta("bitmapContains", 2, 2),
    "bitmapHasAny": ClairQLFunctionMeta("bitmapHasAny", 2, 2),
    "bitmapHasAll": ClairQLFunctionMeta("bitmapHasAll", 2, 2),
    "bitmapCardinality": ClairQLFunctionMeta("bitmapCardinality", 1, 1),
    "bitmapMin": ClairQLFunctionMeta("bitmapMin", 1, 1),
    "bitmapMax": ClairQLFunctionMeta("bitmapMax", 1, 1),
    "bitmapTransform": ClairQLFunctionMeta("bitmapTransform", 3, 3),
    "bitmapAnd": ClairQLFunctionMeta("bitmapAnd", 2, 2),
    "bitmapOr": ClairQLFunctionMeta("bitmapOr", 2, 2),
    "bitmapXor": ClairQLFunctionMeta("bitmapXor", 2, 2),
    "bitmapAndnot": ClairQLFunctionMeta("bitmapAndnot", 2, 2),
    "bitmapAndCardinality": ClairQLFunctionMeta("bitmapAndCardinality", 2, 2),
    "bitmapOrCardinality": ClairQLFunctionMeta("bitmapOrCardinality", 2, 2),
    "bitmapXorCardinality": ClairQLFunctionMeta("bitmapXorCardinality", 2, 2),
    "bitmapAndnotCardinality": ClairQLFunctionMeta("bitmapAndnotCardinality", 2, 2),
    # urls TODO
    "protocol": ClairQLFunctionMeta("protocol", 1, 1),
    "domain": ClairQLFunctionMeta("domain", 1, 1),
    "domainWithoutWWW": ClairQLFunctionMeta("domainWithoutWWW", 1, 1),
    "topLevelDomain": ClairQLFunctionMeta("topLevelDomain", 1, 1),
    "firstSignificantSubdomain": ClairQLFunctionMeta("firstSignificantSubdomain", 1, 1),
    "cutToFirstSignificantSubdomain": ClairQLFunctionMeta("cutToFirstSignificantSubdomain", 1, 1),
    "cutToFirstSignificantSubdomainWithWWW": ClairQLFunctionMeta("cutToFirstSignificantSubdomainWithWWW", 1, 1),
    "port": ClairQLFunctionMeta("port", 1, 2),
    "path": ClairQLFunctionMeta("path", 1, 1),
    "pathFull": ClairQLFunctionMeta("pathFull", 1, 1),
    "queryString": ClairQLFunctionMeta("queryString", 1, 1),
    "fragment": ClairQLFunctionMeta("fragment", 1, 1),
    "queryStringAndFragment": ClairQLFunctionMeta("queryStringAndFragment", 1, 1),
    "extractURLParameter": ClairQLFunctionMeta("extractURLParameter", 2, 2),
    "extractURLParameters": ClairQLFunctionMeta("extractURLParameters", 1, 1),
    "extractURLParameterNames": ClairQLFunctionMeta("extractURLParameterNames", 1, 1),
    "URLHierarchy": ClairQLFunctionMeta("URLHierarchy", 1, 1),
    "URLPathHierarchy": ClairQLFunctionMeta("URLPathHierarchy", 1, 1),
    "encodeURLComponent": ClairQLFunctionMeta("encodeURLComponent", 1, 1),
    "decodeURLComponent": ClairQLFunctionMeta("decodeURLComponent", 1, 1),
    "encodeURLFormComponent": ClairQLFunctionMeta("encodeURLFormComponent", 1, 1),
    "decodeURLFormComponent": ClairQLFunctionMeta("decodeURLFormComponent", 1, 1),
    "netloc": ClairQLFunctionMeta("netloc", 1, 1),
    "cutWWW": ClairQLFunctionMeta("cutWWW", 1, 1),
    "cutQueryString": ClairQLFunctionMeta("cutQueryString", 1, 1),
    "cutFragment": ClairQLFunctionMeta("cutFragment", 1, 1),
    "cutQueryStringAndFragment": ClairQLFunctionMeta("cutQueryStringAndFragment", 1, 1),
    "cutURLParameter": ClairQLFunctionMeta("cutURLParameter", 2, 2),
    # json
    "isValidJSON": ClairQLFunctionMeta("isValidJSON", 1, 1),
    "JSONHas": ClairQLFunctionMeta("JSONHas", 1, None),
    "JSONLength": ClairQLFunctionMeta("JSONLength", 1, None),
    "JSONArrayLength": ClairQLFunctionMeta("JSONArrayLength", 1, None),
    "JSONType": ClairQLFunctionMeta("JSONType", 1, None),
    "JSONExtract": ClairQLFunctionMeta("JSONExtract", 2, None),
    "JSONExtractUInt": ClairQLFunctionMeta("JSONExtractUInt", 1, None),
    "JSONExtractInt": ClairQLFunctionMeta("JSONExtractInt", 1, None),
    "JSONExtractFloat": ClairQLFunctionMeta("JSONExtractFloat", 1, None),
    "JSONExtractBool": ClairQLFunctionMeta("JSONExtractBool", 1, None),
    "JSONExtractString": ClairQLFunctionMeta("JSONExtractString", 1, None),
    "JSONExtractKey": ClairQLFunctionMeta("JSONExtractKey", 1, None),
    "JSONExtractKeys": ClairQLFunctionMeta("JSONExtractKeys", 1, None),
    "JSONExtractRaw": ClairQLFunctionMeta("JSONExtractRaw", 1, None),
    "JSONExtractArrayRaw": ClairQLFunctionMeta("JSONExtractArrayRaw", 1, None),
    "JSONExtractKeysAndValues": ClairQLFunctionMeta("JSONExtractKeysAndValues", 1, 3),
    "JSONExtractKeysAndValuesRaw": ClairQLFunctionMeta("JSONExtractKeysAndValuesRaw", 1, None),
    # in
    "in": ClairQLFunctionMeta("in", 2, 2),
    "notIn": ClairQLFunctionMeta("notIn", 2, 2),
    # geo
    "greatCircleDistance": ClairQLFunctionMeta("greatCircleDistance", 4, 4),
    "geoDistance": ClairQLFunctionMeta("geoDistance", 4, 4),
    "greatCircleAngle": ClairQLFunctionMeta("greatCircleAngle", 4, 4),
    "pointInEllipses": ClairQLFunctionMeta("pointInEllipses", 6, None),
    "pointInPolygon": ClairQLFunctionMeta("pointInPolygon", 2, None),
    "geohashEncode": ClairQLFunctionMeta("geohashEncode", 2, 3),
    "geohashDecode": ClairQLFunctionMeta("geohashDecode", 1, 1),
    "geohashesInBox": ClairQLFunctionMeta("geohashesInBox", 5, 5),
    # nullable
    "isnull": ClairQLFunctionMeta("isNull", 1, 1, case_sensitive=False),
    "isNotNull": ClairQLFunctionMeta("isNotNull", 1, 1),
    "coalesce": ClairQLFunctionMeta("coalesce", 1, None, case_sensitive=False),
    "ifnull": ClairQLFunctionMeta("ifNull", 2, 2, case_sensitive=False),
    "nullif": ClairQLFunctionMeta("nullIf", 2, 2, case_sensitive=False),
    "assumeNotNull": ClairQLFunctionMeta("assumeNotNull", 1, 1),
    "toNullable": ClairQLFunctionMeta("toNullable", 1, 1),
    # tuples
    "tuple": ClairQLFunctionMeta("tuple", 0, None),
    "tupleElement": ClairQLFunctionMeta("tupleElement", 2, 3),
    "untuple": ClairQLFunctionMeta("untuple", 1, 1),
    "tupleHammingDistance": ClairQLFunctionMeta("tupleHammingDistance", 2, 2),
    "tupleToNameValuePairs": ClairQLFunctionMeta("tupleToNameValuePairs", 1, 1),
    "tuplePlus": ClairQLFunctionMeta("tuplePlus", 2, 2),
    "tupleMinus": ClairQLFunctionMeta("tupleMinus", 2, 2),
    "tupleMultiply": ClairQLFunctionMeta("tupleMultiply", 2, 2),
    "tupleDivide": ClairQLFunctionMeta("tupleDivide", 2, 2),
    "tupleNegate": ClairQLFunctionMeta("tupleNegate", 1, 1),
    "tupleMultiplyByNumber": ClairQLFunctionMeta("tupleMultiplyByNumber", 2, 2),
    "tupleDivideByNumber": ClairQLFunctionMeta("tupleDivideByNumber", 2, 2),
    "dotProduct": ClairQLFunctionMeta("dotProduct", 2, 2),
    # other
    "isFinite": ClairQLFunctionMeta("isFinite", 1, 1),
    "isInfinite": ClairQLFunctionMeta("isInfinite", 1, 1),
    "ifNotFinite": ClairQLFunctionMeta("ifNotFinite", 1, 1),
    "isNaN": ClairQLFunctionMeta("isNaN", 1, 1),
    "bar": ClairQLFunctionMeta("bar", 4, 4),
    "transform": ClairQLFunctionMeta("transform", 3, 4),
    "formatReadableDecimalSize": ClairQLFunctionMeta("formatReadableDecimalSize", 1, 1),
    "formatReadableSize": ClairQLFunctionMeta("formatReadableSize", 1, 1),
    "formatReadableQuantity": ClairQLFunctionMeta("formatReadableQuantity", 1, 1),
    "formatReadableTimeDelta": ClairQLFunctionMeta("formatReadableTimeDelta", 1, 2),
    "least": ClairQLFunctionMeta("least", 2, 2, case_sensitive=False),
    "greatest": ClairQLFunctionMeta("greatest", 2, 2, case_sensitive=False),
    # time window
    "tumble": ClairQLFunctionMeta("tumble", 2, 2),
    "hop": ClairQLFunctionMeta("hop", 3, 3),
    "tumbleStart": ClairQLFunctionMeta("tumbleStart", 1, 3),
    "tumbleEnd": ClairQLFunctionMeta("tumbleEnd", 1, 3),
    "hopStart": ClairQLFunctionMeta("hopStart", 1, 3),
    "hopEnd": ClairQLFunctionMeta("hopEnd", 1, 3),
    # distance window
    "L1Norm": ClairQLFunctionMeta("L1Norm", 1, 1),
    "L2Norm": ClairQLFunctionMeta("L2Norm", 1, 1),
    "LinfNorm": ClairQLFunctionMeta("LinfNorm", 1, 1),
    "LpNorm": ClairQLFunctionMeta("LpNorm", 2, 2),
    "L1Distance": ClairQLFunctionMeta("L1Distance", 2, 2),
    "L2Distance": ClairQLFunctionMeta("L2Distance", 2, 2),
    "LinfDistance": ClairQLFunctionMeta("LinfDistance", 2, 2),
    "LpDistance": ClairQLFunctionMeta("LpDistance", 3, 3),
    "L1Normalize": ClairQLFunctionMeta("L1Normalize", 1, 1),
    "L2Normalize": ClairQLFunctionMeta("L2Normalize", 1, 1),
    "LinfNormalize": ClairQLFunctionMeta("LinfNormalize", 1, 1),
    "LpNormalize": ClairQLFunctionMeta("LpNormalize", 2, 2),
    "cosineDistance": ClairQLFunctionMeta("cosineDistance", 2, 2),
    # window functions
    "rank": ClairQLFunctionMeta("rank"),
    "dense_rank": ClairQLFunctionMeta("dense_rank"),
    "row_number": ClairQLFunctionMeta("row_number"),
    "first_value": ClairQLFunctionMeta("first_value", 1, 1),
    "last_value": ClairQLFunctionMeta("last_value", 1, 1),
    "nth_value": ClairQLFunctionMeta("nth_value", 2, 2),
    "lagInFrame": ClairQLFunctionMeta("lagInFrame", 1, 1),
    "leadInFrame": ClairQLFunctionMeta("leadInFrame", 1, 1),
    # table functions
    "generateSeries": ClairQLFunctionMeta("generate_series", 3, 3),
}

# Permitted ClairQL aggregations
CLAIRQL_AGGREGATIONS: dict[str, ClairQLFunctionMeta] = {
    # Standard aggregate functions
    "count": ClairQLFunctionMeta("count", 0, 1, aggregate=True, case_sensitive=False),
    "countIf": ClairQLFunctionMeta("countIf", 1, 2, aggregate=True),
    "countDistinctIf": ClairQLFunctionMeta("countDistinctIf", 1, 2, aggregate=True),
    "min": ClairQLFunctionMeta("min", 1, 1, aggregate=True, case_sensitive=False),
    "minIf": ClairQLFunctionMeta("minIf", 2, 2, aggregate=True),
    "max": ClairQLFunctionMeta("max", 1, 1, aggregate=True, case_sensitive=False),
    "maxIf": ClairQLFunctionMeta("maxIf", 2, 2, aggregate=True),
    "sum": ClairQLFunctionMeta("sum", 1, 1, aggregate=True, case_sensitive=False),
    "sumIf": ClairQLFunctionMeta("sumIf", 2, 2, aggregate=True),
    "avg": ClairQLFunctionMeta("avg", 1, 1, aggregate=True, case_sensitive=False),
    "avgIf": ClairQLFunctionMeta("avgIf", 2, 2, aggregate=True),
    "any": ClairQLFunctionMeta("any", 1, 1, aggregate=True),
    "anyIf": ClairQLFunctionMeta("anyIf", 2, 2, aggregate=True),
    "stddevPop": ClairQLFunctionMeta("stddevPop", 1, 1, aggregate=True),
    "stddevPopIf": ClairQLFunctionMeta("stddevPopIf", 2, 2, aggregate=True),
    "stddevSamp": ClairQLFunctionMeta("stddevSamp", 1, 1, aggregate=True),
    "stddevSampIf": ClairQLFunctionMeta("stddevSampIf", 2, 2, aggregate=True),
    "varPop": ClairQLFunctionMeta("varPop", 1, 1, aggregate=True),
    "varPopIf": ClairQLFunctionMeta("varPopIf", 2, 2, aggregate=True),
    "varSamp": ClairQLFunctionMeta("varSamp", 1, 1, aggregate=True),
    "varSampIf": ClairQLFunctionMeta("varSampIf", 2, 2, aggregate=True),
    "covarPop": ClairQLFunctionMeta("covarPop", 2, 2, aggregate=True),
    "covarPopIf": ClairQLFunctionMeta("covarPopIf", 3, 3, aggregate=True),
    "covarSamp": ClairQLFunctionMeta("covarSamp", 2, 2, aggregate=True),
    "covarSampIf": ClairQLFunctionMeta("covarSampIf", 3, 3, aggregate=True),
    "corr": ClairQLFunctionMeta("corr", 2, 2, aggregate=True),
    # ClickHouse-specific aggregate functions
    "anyHeavy": ClairQLFunctionMeta("anyHeavy", 1, 1, aggregate=True),
    "anyHeavyIf": ClairQLFunctionMeta("anyHeavyIf", 2, 2, aggregate=True),
    "anyLast": ClairQLFunctionMeta("anyLast", 1, 1, aggregate=True),
    "anyLastIf": ClairQLFunctionMeta("anyLastIf", 2, 2, aggregate=True),
    "argMin": ClairQLFunctionMeta("argMin", 2, 2, aggregate=True),
    "argMinIf": ClairQLFunctionMeta("argMinIf", 3, 3, aggregate=True),
    "argMax": ClairQLFunctionMeta("argMax", 2, 2, aggregate=True),
    "argMaxIf": ClairQLFunctionMeta("argMaxIf", 3, 3, aggregate=True),
    "argMinMerge": ClairQLFunctionMeta("argMinMerge", 1, 1, aggregate=True),
    "argMaxMerge": ClairQLFunctionMeta("argMaxMerge", 1, 1, aggregate=True),
    "avgState": ClairQLFunctionMeta("avgState", 1, 1, aggregate=True),
    "avgMerge": ClairQLFunctionMeta("avgMerge", 1, 1, aggregate=True),
    "avgWeighted": ClairQLFunctionMeta("avgWeighted", 2, 2, aggregate=True),
    "avgWeightedIf": ClairQLFunctionMeta("avgWeightedIf", 3, 3, aggregate=True),
    "avgArray": ClairQLFunctionMeta("avgArrayOrNull", 1, 1, aggregate=True),
    "topK": ClairQLFunctionMeta("topK", 1, 1, min_params=1, max_params=1, aggregate=True),
    # "topKIf": ClairQLFunctionMeta("topKIf", 2, 2, aggregate=True),
    # "topKWeighted": ClairQLFunctionMeta("topKWeighted", 1, 1, aggregate=True),
    # "topKWeightedIf": ClairQLFunctionMeta("topKWeightedIf", 2, 2, aggregate=True),
    "groupArray": ClairQLFunctionMeta("groupArray", 1, 1, aggregate=True),
    "groupArrayIf": ClairQLFunctionMeta("groupArrayIf", 2, 2, aggregate=True),
    # "groupArrayLast": ClairQLFunctionMeta("groupArrayLast", 1, 1, aggregate=True),
    # "groupArrayLastIf": ClairQLFunctionMeta("groupArrayLastIf", 2, 2, aggregate=True),
    "groupUniqArray": ClairQLFunctionMeta("groupUniqArray", 1, 1, aggregate=True),
    "groupUniqArrayIf": ClairQLFunctionMeta("groupUniqArrayIf", 2, 2, aggregate=True),
    "groupArrayInsertAt": ClairQLFunctionMeta("groupArrayInsertAt", 2, 2, aggregate=True),
    "groupArrayInsertAtIf": ClairQLFunctionMeta("groupArrayInsertAtIf", 3, 3, aggregate=True),
    "groupArrayMovingAvg": ClairQLFunctionMeta("groupArrayMovingAvg", 1, 1, aggregate=True),
    "groupArrayMovingAvgIf": ClairQLFunctionMeta("groupArrayMovingAvgIf", 2, 2, aggregate=True),
    "groupArrayMovingSum": ClairQLFunctionMeta("groupArrayMovingSum", 1, 1, aggregate=True),
    "groupArrayMovingSumIf": ClairQLFunctionMeta("groupArrayMovingSumIf", 2, 2, aggregate=True),
    "groupBitAnd": ClairQLFunctionMeta("groupBitAnd", 1, 1, aggregate=True),
    "groupBitAndIf": ClairQLFunctionMeta("groupBitAndIf", 2, 2, aggregate=True),
    "groupBitOr": ClairQLFunctionMeta("groupBitOr", 1, 1, aggregate=True),
    "groupBitOrIf": ClairQLFunctionMeta("groupBitOrIf", 2, 2, aggregate=True),
    "groupBitXor": ClairQLFunctionMeta("groupBitXor", 1, 1, aggregate=True),
    "groupBitXorIf": ClairQLFunctionMeta("groupBitXorIf", 2, 2, aggregate=True),
    "groupBitmap": ClairQLFunctionMeta("groupBitmap", 1, 1, aggregate=True),
    "groupBitmapIf": ClairQLFunctionMeta("groupBitmapIf", 2, 2, aggregate=True),
    "groupBitmapAnd": ClairQLFunctionMeta("groupBitmapAnd", 1, 1, aggregate=True),
    "groupBitmapAndIf": ClairQLFunctionMeta("groupBitmapAndIf", 2, 2, aggregate=True),
    "groupBitmapOr": ClairQLFunctionMeta("groupBitmapOr", 1, 1, aggregate=True),
    "groupBitmapOrIf": ClairQLFunctionMeta("groupBitmapOrIf", 2, 2, aggregate=True),
    "groupBitmapXor": ClairQLFunctionMeta("groupBitmapXor", 1, 1, aggregate=True),
    "groupBitmapXorIf": ClairQLFunctionMeta("groupBitmapXorIf", 2, 2, aggregate=True),
    "sumWithOverflow": ClairQLFunctionMeta("sumWithOverflow", 1, 1, aggregate=True),
    "sumWithOverflowIf": ClairQLFunctionMeta("sumWithOverflowIf", 2, 2, aggregate=True),
    "deltaSum": ClairQLFunctionMeta("deltaSum", 1, 1, aggregate=True),
    "deltaSumIf": ClairQLFunctionMeta("deltaSumIf", 2, 2, aggregate=True),
    "deltaSumTimestamp": ClairQLFunctionMeta("deltaSumTimestamp", 2, 2, aggregate=True),
    "deltaSumTimestampIf": ClairQLFunctionMeta("deltaSumTimestampIf", 3, 3, aggregate=True),
    "sumMap": ClairQLFunctionMeta("sumMap", 1, 2, aggregate=True),
    "sumMapIf": ClairQLFunctionMeta("sumMapIf", 2, 3, aggregate=True),
    "sumMapMerge": ClairQLFunctionMeta("sumMapMerge", 1, 1, aggregate=True),
    "minMap": ClairQLFunctionMeta("minMap", 1, 2, aggregate=True),
    "minMapIf": ClairQLFunctionMeta("minMapIf", 2, 3, aggregate=True),
    "maxMap": ClairQLFunctionMeta("maxMap", 1, 2, aggregate=True),
    "maxMapIf": ClairQLFunctionMeta("maxMapIf", 2, 3, aggregate=True),
    "medianArray": ClairQLFunctionMeta("medianArrayOrNull", 1, 1, aggregate=True),
    "skewSamp": ClairQLFunctionMeta("skewSamp", 1, 1, aggregate=True),
    "skewSampIf": ClairQLFunctionMeta("skewSampIf", 2, 2, aggregate=True),
    "skewPop": ClairQLFunctionMeta("skewPop", 1, 1, aggregate=True),
    "skewPopIf": ClairQLFunctionMeta("skewPopIf", 2, 2, aggregate=True),
    "kurtSamp": ClairQLFunctionMeta("kurtSamp", 1, 1, aggregate=True),
    "kurtSampIf": ClairQLFunctionMeta("kurtSampIf", 2, 2, aggregate=True),
    "kurtPop": ClairQLFunctionMeta("kurtPop", 1, 1, aggregate=True),
    "kurtPopIf": ClairQLFunctionMeta("kurtPopIf", 2, 2, aggregate=True),
    "uniq": ClairQLFunctionMeta("uniq", 1, None, aggregate=True),
    "uniqIf": ClairQLFunctionMeta("uniqIf", 2, None, aggregate=True),
    "uniqExact": ClairQLFunctionMeta("uniqExact", 1, None, aggregate=True),
    "uniqExactIf": ClairQLFunctionMeta("uniqExactIf", 2, None, aggregate=True),
    # "uniqCombined": ClairQLFunctionMeta("uniqCombined", 1, 1, aggregate=True),
    # "uniqCombinedIf": ClairQLFunctionMeta("uniqCombinedIf", 2, 2, aggregate=True),
    # "uniqCombined64": ClairQLFunctionMeta("uniqCombined64", 1, 1, aggregate=True),
    # "uniqCombined64If": ClairQLFunctionMeta("uniqCombined64If", 2, 2, aggregate=True),
    "uniqHLL12": ClairQLFunctionMeta("uniqHLL12", 1, None, aggregate=True),
    "uniqHLL12If": ClairQLFunctionMeta("uniqHLL12If", 2, None, aggregate=True),
    "uniqTheta": ClairQLFunctionMeta("uniqTheta", 1, None, aggregate=True),
    "uniqThetaIf": ClairQLFunctionMeta("uniqThetaIf", 2, None, aggregate=True),
    "uniqMerge": ClairQLFunctionMeta("uniqMerge", 1, 1, aggregate=True),
    "uniqUpToMerge": ClairQLFunctionMeta("uniqUpToMerge", 1, 1, 1, 1, aggregate=True),
    "median": ClairQLFunctionMeta("median", 1, 1, aggregate=True),
    "medianIf": ClairQLFunctionMeta("medianIf", 2, 2, aggregate=True),
    "medianExact": ClairQLFunctionMeta("medianExact", 1, 1, aggregate=True),
    "medianExactIf": ClairQLFunctionMeta("medianExactIf", 2, 2, aggregate=True),
    "medianExactLow": ClairQLFunctionMeta("medianExactLow", 1, 1, aggregate=True),
    "medianExactLowIf": ClairQLFunctionMeta("medianExactLowIf", 2, 2, aggregate=True),
    "medianExactHigh": ClairQLFunctionMeta("medianExactHigh", 1, 1, aggregate=True),
    "medianExactHighIf": ClairQLFunctionMeta("medianExactHighIf", 2, 2, aggregate=True),
    "medianExactWeighted": ClairQLFunctionMeta("medianExactWeighted", 1, 1, aggregate=True),
    "medianExactWeightedIf": ClairQLFunctionMeta("medianExactWeightedIf", 2, 2, aggregate=True),
    "medianTiming": ClairQLFunctionMeta("medianTiming", 1, 1, aggregate=True),
    "medianTimingIf": ClairQLFunctionMeta("medianTimingIf", 2, 2, aggregate=True),
    "medianTimingWeighted": ClairQLFunctionMeta("medianTimingWeighted", 1, 1, aggregate=True),
    "medianTimingWeightedIf": ClairQLFunctionMeta("medianTimingWeightedIf", 2, 2, aggregate=True),
    "medianDeterministic": ClairQLFunctionMeta("medianDeterministic", 1, 1, aggregate=True),
    "medianDeterministicIf": ClairQLFunctionMeta("medianDeterministicIf", 2, 2, aggregate=True),
    "medianTDigest": ClairQLFunctionMeta("medianTDigest", 1, 1, aggregate=True),
    "medianTDigestIf": ClairQLFunctionMeta("medianTDigestIf", 2, 2, aggregate=True),
    "medianTDigestWeighted": ClairQLFunctionMeta("medianTDigestWeighted", 1, 1, aggregate=True),
    "medianTDigestWeightedIf": ClairQLFunctionMeta("medianTDigestWeightedIf", 2, 2, aggregate=True),
    "medianBFloat16": ClairQLFunctionMeta("medianBFloat16", 1, 1, aggregate=True),
    "medianBFloat16If": ClairQLFunctionMeta("medianBFloat16If", 2, 2, aggregate=True),
    "quantile": ClairQLFunctionMeta("quantile", 1, 1, min_params=1, max_params=1, aggregate=True),
    "quantileIf": ClairQLFunctionMeta("quantileIf", 2, 2, min_params=1, max_params=1, aggregate=True),
    "quantiles": ClairQLFunctionMeta("quantiles", 1, None, aggregate=True),
    "quantilesIf": ClairQLFunctionMeta("quantilesIf", 2, 2, min_params=1, max_params=1, aggregate=True),
    # "quantileExact": ClairQLFunctionMeta("quantileExact", 1, 1, aggregate=True),
    # "quantileExactIf": ClairQLFunctionMeta("quantileExactIf", 2, 2, aggregate=True),
    # "quantileExactLow": ClairQLFunctionMeta("quantileExactLow", 1, 1, aggregate=True),
    # "quantileExactLowIf": ClairQLFunctionMeta("quantileExactLowIf", 2, 2, aggregate=True),
    # "quantileExactHigh": ClairQLFunctionMeta("quantileExactHigh", 1, 1, aggregate=True),
    # "quantileExactHighIf": ClairQLFunctionMeta("quantileExactHighIf", 2, 2, aggregate=True),
    # "quantileExactWeighted": ClairQLFunctionMeta("quantileExactWeighted", 1, 1, aggregate=True),
    # "quantileExactWeightedIf": ClairQLFunctionMeta("quantileExactWeightedIf", 2, 2, aggregate=True),
    # "quantileTiming": ClairQLFunctionMeta("quantileTiming", 1, 1, aggregate=True),
    # "quantileTimingIf": ClairQLFunctionMeta("quantileTimingIf", 2, 2, aggregate=True),
    # "quantileTimingWeighted": ClairQLFunctionMeta("quantileTimingWeighted", 1, 1, aggregate=True),
    # "quantileTimingWeightedIf": ClairQLFunctionMeta("quantileTimingWeightedIf", 2, 2, aggregate=True),
    # "quantileDeterministic": ClairQLFunctionMeta("quantileDeterministic", 1, 1, aggregate=True),
    # "quantileDeterministicIf": ClairQLFunctionMeta("quantileDeterministicIf", 2, 2, aggregate=True),
    # "quantileTDigest": ClairQLFunctionMeta("quantileTDigest", 1, 1, aggregate=True),
    # "quantileTDigestIf": ClairQLFunctionMeta("quantileTDigestIf", 2, 2, aggregate=True),
    # "quantileTDigestWeighted": ClairQLFunctionMeta("quantileTDigestWeighted", 1, 1, aggregate=True),
    # "quantileTDigestWeightedIf": ClairQLFunctionMeta("quantileTDigestWeightedIf", 2, 2, aggregate=True),
    # "quantileBFloat16": ClairQLFunctionMeta("quantileBFloat16", 1, 1, aggregate=True),
    # "quantileBFloat16If": ClairQLFunctionMeta("quantileBFloat16If", 2, 2, aggregate=True),
    # "quantileBFloat16Weighted": ClairQLFunctionMeta("quantileBFloat16Weighted", 1, 1, aggregate=True),
    # "quantileBFloat16WeightedIf": ClairQLFunctionMeta("quantileBFloat16WeightedIf", 2, 2, aggregate=True),
    "simpleLinearRegression": ClairQLFunctionMeta("simpleLinearRegression", 2, 2, aggregate=True),
    "simpleLinearRegressionIf": ClairQLFunctionMeta("simpleLinearRegressionIf", 3, 3, aggregate=True),
    # "stochasticLinearRegression": ClairQLFunctionMeta("stochasticLinearRegression", 1, 1, aggregate=True),
    # "stochasticLinearRegressionIf": ClairQLFunctionMeta("stochasticLinearRegressionIf", 2, 2, aggregate=True),
    # "stochasticLogisticRegression": ClairQLFunctionMeta("stochasticLogisticRegression", 1, 1, aggregate=True),
    # "stochasticLogisticRegressionIf": ClairQLFunctionMeta("stochasticLogisticRegressionIf", 2, 2, aggregate=True),
    # "categoricalInformationValue": ClairQLFunctionMeta("categoricalInformationValue", 1, 1, aggregate=True),
    # "categoricalInformationValueIf": ClairQLFunctionMeta("categoricalInformationValueIf", 2, 2, aggregate=True),
    "contingency": ClairQLFunctionMeta("contingency", 2, 2, aggregate=True),
    "contingencyIf": ClairQLFunctionMeta("contingencyIf", 3, 3, aggregate=True),
    "cramersV": ClairQLFunctionMeta("cramersV", 2, 2, aggregate=True),
    "cramersVIf": ClairQLFunctionMeta("cramersVIf", 3, 3, aggregate=True),
    "cramersVBiasCorrected": ClairQLFunctionMeta("cramersVBiasCorrected", 2, 2, aggregate=True),
    "cramersVBiasCorrectedIf": ClairQLFunctionMeta("cramersVBiasCorrectedIf", 3, 3, aggregate=True),
    "theilsU": ClairQLFunctionMeta("theilsU", 2, 2, aggregate=True),
    "theilsUIf": ClairQLFunctionMeta("theilsUIf", 3, 3, aggregate=True),
    "maxIntersections": ClairQLFunctionMeta("maxIntersections", 2, 2, aggregate=True),
    "maxIntersectionsIf": ClairQLFunctionMeta("maxIntersectionsIf", 3, 3, aggregate=True),
    "maxIntersectionsPosition": ClairQLFunctionMeta("maxIntersectionsPosition", 2, 2, aggregate=True),
    "maxIntersectionsPositionIf": ClairQLFunctionMeta("maxIntersectionsPositionIf", 3, 3, aggregate=True),
}
CLAIRQL_CLAIRVIEW_FUNCTIONS: dict[str, ClairQLFunctionMeta] = {
    "matchesAction": ClairQLFunctionMeta("matchesAction", 1, 1),
    "sparkline": ClairQLFunctionMeta("sparkline", 1, 1),
    "recording_button": ClairQLFunctionMeta("recording_button", 1, 1),
    "clairql_lookupDomainType": ClairQLFunctionMeta("clairql_lookupDomainType", 1, 1),
    "clairql_lookupPaidSourceType": ClairQLFunctionMeta("clairql_lookupPaidSourceType", 1, 1),
    "clairql_lookupPaidMediumType": ClairQLFunctionMeta("clairql_lookupPaidMediumType", 1, 1),
    "clairql_lookupOrganicSourceType": ClairQLFunctionMeta("clairql_lookupOrganicSourceType", 1, 1),
    "clairql_lookupOrganicMediumType": ClairQLFunctionMeta("clairql_lookupOrganicMediumType", 1, 1),
}


UDFS: dict[str, ClairQLFunctionMeta] = {
    "aggregate_funnel": ClairQLFunctionMeta("aggregate_funnel", 6, 6, aggregate=False),
    "aggregate_funnel_array": ClairQLFunctionMeta("aggregate_funnel_array", 6, 6, aggregate=False),
    "aggregate_funnel_cohort": ClairQLFunctionMeta("aggregate_funnel_cohort", 6, 6, aggregate=False),
    "aggregate_funnel_trends": ClairQLFunctionMeta("aggregate_funnel_trends", 7, 7, aggregate=False),
    "aggregate_funnel_array_trends": ClairQLFunctionMeta("aggregate_funnel_array_trends", 7, 7, aggregate=False),
    "aggregate_funnel_cohort_trends": ClairQLFunctionMeta("aggregate_funnel_cohort_trends", 7, 7, aggregate=False),
    "aggregate_funnel_test": ClairQLFunctionMeta("aggregate_funnel_test", 6, 6, aggregate=False),
}
# We want CI to fail if there is a breaking change and the version hasn't been incremented
if is_cloud() or is_ci():
    from clairview.udf_versioner import augment_function_name

    for v in UDFS.values():
        v.clickhouse_name = augment_function_name(v.clickhouse_name)

CLAIRQL_CLICKHOUSE_FUNCTIONS.update(UDFS)


ALL_EXPOSED_FUNCTION_NAMES = [
    name for name in chain(CLAIRQL_CLICKHOUSE_FUNCTIONS.keys(), CLAIRQL_AGGREGATIONS.keys()) if not name.startswith("_")
]

# TODO: Make the below details part of function meta
# Functions where we use a -OrNull variant by default
ADD_OR_NULL_DATETIME_FUNCTIONS = (
    "toDateTime",
    "parseDateTime",
    "parseDateTimeBestEffort",
)
# Functions where the first argument needs to be DateTime and not DateTime64
FIRST_ARG_DATETIME_FUNCTIONS = (
    "tumble",
    "tumbleStart",
    "tumbleEnd",
    "hop",
    "hopStart",
    "hopEnd",
)


def _find_function(name: str, functions: dict[str, ClairQLFunctionMeta]) -> Optional[ClairQLFunctionMeta]:
    func = functions.get(name)
    if func is not None:
        return func

    func = functions.get(name.lower())
    if func is None:
        return None
    # If we haven't found a function with the case preserved, but we have found it in lowercase,
    # then the function names are different case-wise only.
    if func.case_sensitive:
        return None

    return func


def find_clairql_aggregation(name: str) -> Optional[ClairQLFunctionMeta]:
    return _find_function(name, CLAIRQL_AGGREGATIONS)


def find_clairql_function(name: str) -> Optional[ClairQLFunctionMeta]:
    return _find_function(name, CLAIRQL_CLICKHOUSE_FUNCTIONS)


def find_clairql_clairview_function(name: str) -> Optional[ClairQLFunctionMeta]:
    return _find_function(name, CLAIRQL_CLAIRVIEW_FUNCTIONS)
