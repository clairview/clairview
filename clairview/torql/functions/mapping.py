from dataclasses import dataclass
from itertools import chain
from typing import Optional

from clairview.cloud_utils import is_cloud, is_ci
from clairview.torql import ast
from clairview.torql.ast import (
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
from clairview.torql.base import ConstantType, UnknownType
from clairview.torql.errors import QueryError


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
class TorQLFunctionMeta:
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


TORQL_COMPARISON_MAPPING: dict[str, ast.CompareOperationOp] = {
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

TORQL_CLICKHOUSE_FUNCTIONS: dict[str, TorQLFunctionMeta] = {
    # arithmetic
    "plus": TorQLFunctionMeta(
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
    "minus": TorQLFunctionMeta(
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
    "multiply": TorQLFunctionMeta(
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
    "divide": TorQLFunctionMeta(
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
    "intDiv": TorQLFunctionMeta(
        "intDiv",
        2,
        2,
        signatures=[
            ((IntegerType(), IntegerType()), IntegerType()),
        ],
    ),
    "intDivOrZero": TorQLFunctionMeta(
        "intDivOrZero",
        2,
        2,
        signatures=[
            ((IntegerType(), IntegerType()), IntegerType()),
        ],
    ),
    "modulo": TorQLFunctionMeta(
        "modulo",
        2,
        2,
        signatures=[
            ((IntegerType(), IntegerType()), IntegerType()),
            ((FloatType(), IntegerType()), FloatType()),
            ((IntegerType(), FloatType()), FloatType()),
        ],
    ),
    "moduloOrZero": TorQLFunctionMeta(
        "moduloOrZero",
        2,
        2,
        signatures=[
            ((IntegerType(), IntegerType()), IntegerType()),
            ((FloatType(), IntegerType()), FloatType()),
            ((IntegerType(), FloatType()), FloatType()),
        ],
    ),
    "positiveModulo": TorQLFunctionMeta(
        "positiveModulo",
        2,
        2,
        signatures=[
            ((IntegerType(), IntegerType()), IntegerType()),
            ((FloatType(), IntegerType()), FloatType()),
            ((IntegerType(), FloatType()), FloatType()),
        ],
    ),
    "negate": TorQLFunctionMeta(
        "negate",
        1,
        1,
        signatures=[
            ((IntegerType(),), IntegerType()),
            ((FloatType(),), FloatType()),
        ],
    ),
    "abs": TorQLFunctionMeta(
        "abs",
        1,
        1,
        signatures=[
            ((IntegerType(),), IntegerType()),
        ],
        case_sensitive=False,
    ),
    "gcd": TorQLFunctionMeta(
        "gcd",
        2,
        2,
        signatures=[
            ((IntegerType(),), IntegerType()),
        ],
    ),
    "lcm": TorQLFunctionMeta(
        "lcm",
        2,
        2,
        signatures=[
            ((IntegerType(),), IntegerType()),
        ],
    ),
    "max2": TorQLFunctionMeta(
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
    "min2": TorQLFunctionMeta(
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
    "multiplyDecimal": TorQLFunctionMeta("multiplyDecimal", 2, 3),
    "divideDecimal": TorQLFunctionMeta("divideDecimal", 2, 3),
    # arrays and strings common
    "empty": TorQLFunctionMeta("empty", 1, 1),
    "notEmpty": TorQLFunctionMeta("notEmpty", 1, 1),
    "length": TorQLFunctionMeta("length", 1, 1, case_sensitive=False),
    "reverse": TorQLFunctionMeta("reverse", 1, 1, case_sensitive=False),
    # arrays
    "array": TorQLFunctionMeta("array", 0, None),
    "range": TorQLFunctionMeta("range", 1, 3),
    "arrayConcat": TorQLFunctionMeta("arrayConcat", 2, None),
    "arrayElement": TorQLFunctionMeta("arrayElement", 2, 2),
    "has": TorQLFunctionMeta("has", 2, 2),
    "hasAll": TorQLFunctionMeta("hasAll", 2, 2),
    "hasAny": TorQLFunctionMeta("hasAny", 2, 2),
    "hasSubstr": TorQLFunctionMeta("hasSubstr", 2, 2),
    "indexOf": TorQLFunctionMeta("indexOf", 2, 2),
    "arrayCount": TorQLFunctionMeta("arrayCount", 1, None),
    "countEqual": TorQLFunctionMeta("countEqual", 2, 2),
    "arrayEnumerate": TorQLFunctionMeta("arrayEnumerate", 1, 1),
    "arrayEnumerateUniq": TorQLFunctionMeta("arrayEnumerateUniq", 2, None),
    "arrayPopBack": TorQLFunctionMeta("arrayPopBack", 1, 1),
    "arrayPopFront": TorQLFunctionMeta("arrayPopFront", 1, 1),
    "arrayPushBack": TorQLFunctionMeta("arrayPushBack", 2, 2),
    "arrayPushFront": TorQLFunctionMeta("arrayPushFront", 2, 2),
    "arrayResize": TorQLFunctionMeta("arrayResize", 2, 3),
    "arraySlice": TorQLFunctionMeta("arraySlice", 2, 3),
    "arraySort": TorQLFunctionMeta("arraySort", 1, None),
    "arrayReverseSort": TorQLFunctionMeta("arraySort", 1, None),
    "arrayUniq": TorQLFunctionMeta("arrayUniq", 1, None),
    "arrayJoin": TorQLFunctionMeta("arrayJoin", 1, 1),
    "arrayDifference": TorQLFunctionMeta("arrayDifference", 1, 1),
    "arrayDistinct": TorQLFunctionMeta("arrayDistinct", 1, 1),
    "arrayEnumerateDense": TorQLFunctionMeta("arrayEnumerateDense", 1, 1),
    "arrayIntersect": TorQLFunctionMeta("arrayIntersect", 1, None),
    # "arrayReduce": TorQLFunctionMeta("arrayReduce", 2,None),  # takes a "parametric function" as first arg, is that safe?
    # "arrayReduceInRanges": TorQLFunctionMeta("arrayReduceInRanges", 3,None),  # takes a "parametric function" as first arg, is that safe?
    "arrayReverse": TorQLFunctionMeta("arrayReverse", 1, 1),
    "arrayFilter": TorQLFunctionMeta("arrayFilter", 2, None),
    "arrayFlatten": TorQLFunctionMeta("arrayFlatten", 1, 1),
    "arrayCompact": TorQLFunctionMeta("arrayCompact", 1, 1),
    "arrayZip": TorQLFunctionMeta("arrayZip", 2, None),
    "arrayAUC": TorQLFunctionMeta("arrayAUC", 2, 2),
    "arrayMap": TorQLFunctionMeta("arrayMap", 2, None),
    "arrayFill": TorQLFunctionMeta("arrayFill", 2, None),
    "arrayFold": TorQLFunctionMeta("arrayFold", 3, None),
    "arrayWithConstant": TorQLFunctionMeta("arrayWithConstant", 2, 2),
    "arraySplit": TorQLFunctionMeta("arraySplit", 2, None),
    "arrayReverseFill": TorQLFunctionMeta("arrayReverseFill", 2, None),
    "arrayReverseSplit": TorQLFunctionMeta("arrayReverseSplit", 2, None),
    "arrayExists": TorQLFunctionMeta("arrayExists", 1, None),
    "arrayAll": TorQLFunctionMeta("arrayAll", 1, None),
    "arrayFirst": TorQLFunctionMeta("arrayFirst", 2, None),
    "arrayLast": TorQLFunctionMeta("arrayLast", 2, None),
    "arrayFirstIndex": TorQLFunctionMeta("arrayFirstIndex", 2, None),
    "arrayLastIndex": TorQLFunctionMeta("arrayLastIndex", 2, None),
    "arrayMin": TorQLFunctionMeta("arrayMin", 1, 2),
    "arrayMax": TorQLFunctionMeta("arrayMax", 1, 2),
    "arraySum": TorQLFunctionMeta("arraySum", 1, 2),
    "arrayAvg": TorQLFunctionMeta("arrayAvg", 1, 2),
    "arrayCumSum": TorQLFunctionMeta("arrayCumSum", 1, None),
    "arrayCumSumNonNegative": TorQLFunctionMeta("arrayCumSumNonNegative", 1, None),
    "arrayProduct": TorQLFunctionMeta("arrayProduct", 1, 1),
    # comparison
    "equals": TorQLFunctionMeta("equals", 2, 2),
    "notEquals": TorQLFunctionMeta("notEquals", 2, 2),
    "less": TorQLFunctionMeta("less", 2, 2),
    "greater": TorQLFunctionMeta("greater", 2, 2),
    "lessOrEquals": TorQLFunctionMeta("lessOrEquals", 2, 2),
    "greaterOrEquals": TorQLFunctionMeta("greaterOrEquals", 2, 2),
    # logical
    "and": TorQLFunctionMeta("and", 2, None),
    "or": TorQLFunctionMeta("or", 2, None),
    "xor": TorQLFunctionMeta("xor", 2, None),
    "not": TorQLFunctionMeta("not", 1, 1, case_sensitive=False),
    # type conversions
    "hex": TorQLFunctionMeta("hex", 1, 1),
    "unhex": TorQLFunctionMeta("unhex", 1, 1),
    # instead of just "reinterpret" we use specific list of "reinterpretAs*"" functions
    # that we know are safe to use to minimize the security risk
    "reinterpretAsUInt8": TorQLFunctionMeta("reinterpretAsUInt8", 1, 1),
    "reinterpretAsUInt16": TorQLFunctionMeta("reinterpretAsUInt16", 1, 1),
    "reinterpretAsUInt32": TorQLFunctionMeta("reinterpretAsUInt32", 1, 1),
    "reinterpretAsUInt64": TorQLFunctionMeta("reinterpretAsUInt64", 1, 1),
    "reinterpretAsUInt128": TorQLFunctionMeta("reinterpretAsUInt128", 1, 1),
    "reinterpretAsUInt256": TorQLFunctionMeta("reinterpretAsUInt256", 1, 1),
    "reinterpretAsInt8": TorQLFunctionMeta("reinterpretAsInt8", 1, 1),
    "reinterpretAsInt16": TorQLFunctionMeta("reinterpretAsInt16", 1, 1),
    "reinterpretAsInt32": TorQLFunctionMeta("reinterpretAsInt32", 1, 1),
    "reinterpretAsInt64": TorQLFunctionMeta("reinterpretAsInt64", 1, 1),
    "reinterpretAsInt128": TorQLFunctionMeta("reinterpretAsInt128", 1, 1),
    "reinterpretAsInt256": TorQLFunctionMeta("reinterpretAsInt256", 1, 1),
    "reinterpretAsFloat32": TorQLFunctionMeta("reinterpretAsFloat32", 1, 1),
    "reinterpretAsFloat64": TorQLFunctionMeta("reinterpretAsFloat64", 1, 1),
    "reinterpretAsUUID": TorQLFunctionMeta("reinterpretAsUUID", 1, 1),
    "toInt": TorQLFunctionMeta("accurateCastOrNull", 1, 1, suffix_args=[ast.Constant(value="Int64")]),
    "_toInt64": TorQLFunctionMeta("toInt64", 1, 1),
    "_toUInt64": TorQLFunctionMeta("toUInt64", 1, 1),
    "_toUInt128": TorQLFunctionMeta("toUInt128", 1, 1),
    "toFloat": TorQLFunctionMeta("accurateCastOrNull", 1, 1, suffix_args=[ast.Constant(value="Float64")]),
    "toDecimal": TorQLFunctionMeta("accurateCastOrNull", 1, 1, suffix_args=[ast.Constant(value="Decimal64")]),
    "toDate": TorQLFunctionMeta(
        "toDateOrNull",
        1,
        1,
        overloads=[((ast.DateTimeType, ast.DateType), "toDate")],
    ),
    "toDateTime": TorQLFunctionMeta(
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
    "toUUID": TorQLFunctionMeta("accurateCastOrNull", 1, 1, suffix_args=[ast.Constant(value="UUID")]),
    "toString": TorQLFunctionMeta(
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
    "toJSONString": TorQLFunctionMeta("toJSONString", 1, 1),
    "parseDateTime": TorQLFunctionMeta("parseDateTimeOrNull", 2, 3, tz_aware=True),
    "parseDateTimeBestEffort": TorQLFunctionMeta("parseDateTime64BestEffortOrNull", 1, 2, tz_aware=True),
    "toTypeName": TorQLFunctionMeta("toTypeName", 1, 1),
    "cityHash64": TorQLFunctionMeta("cityHash64", 1, 1),
    # dates and times
    "toTimeZone": TorQLFunctionMeta("toTimeZone", 2, 2),
    "timeZoneOf": TorQLFunctionMeta("timeZoneOf", 1, 1),
    "timeZoneOffset": TorQLFunctionMeta("timeZoneOffset", 1, 1),
    "toYear": TorQLFunctionMeta("toYear", 1, 1),
    "toQuarter": TorQLFunctionMeta("toQuarter", 1, 1),
    "toMonth": TorQLFunctionMeta("toMonth", 1, 1),
    "toDayOfYear": TorQLFunctionMeta("toDayOfYear", 1, 1),
    "toDayOfMonth": TorQLFunctionMeta("toDayOfMonth", 1, 1),
    "toDayOfWeek": TorQLFunctionMeta("toDayOfWeek", 1, 3),
    "toHour": TorQLFunctionMeta("toHour", 1, 1),
    "toMinute": TorQLFunctionMeta("toMinute", 1, 1),
    "toSecond": TorQLFunctionMeta("toSecond", 1, 1),
    "toUnixTimestamp": TorQLFunctionMeta("toUnixTimestamp", 1, 2),
    "toUnixTimestamp64Milli": TorQLFunctionMeta("toUnixTimestamp64Milli", 1, 1),
    "toStartOfYear": TorQLFunctionMeta("toStartOfYear", 1, 1),
    "toStartOfISOYear": TorQLFunctionMeta("toStartOfISOYear", 1, 1),
    "toStartOfQuarter": TorQLFunctionMeta("toStartOfQuarter", 1, 1),
    "toStartOfMonth": TorQLFunctionMeta("toStartOfMonth", 1, 1),
    "toLastDayOfMonth": TorQLFunctionMeta("toLastDayOfMonth", 1, 1),
    "toMonday": TorQLFunctionMeta("toMonday", 1, 1),
    "toStartOfWeek": TorQLFunctionMeta("toStartOfWeek", 1, 2),
    "toStartOfDay": TorQLFunctionMeta("toStartOfDay", 1, 2),
    "toLastDayOfWeek": TorQLFunctionMeta("toLastDayOfWeek", 1, 2),
    "toStartOfHour": TorQLFunctionMeta("toStartOfHour", 1, 1),
    "toStartOfMinute": TorQLFunctionMeta("toStartOfMinute", 1, 1),
    "toStartOfSecond": TorQLFunctionMeta("toStartOfSecond", 1, 1),
    "toStartOfFiveMinutes": TorQLFunctionMeta("toStartOfFiveMinutes", 1, 1),
    "toStartOfTenMinutes": TorQLFunctionMeta("toStartOfTenMinutes", 1, 1),
    "toStartOfFifteenMinutes": TorQLFunctionMeta("toStartOfFifteenMinutes", 1, 1),
    "toTime": TorQLFunctionMeta("toTime", 1, 1),
    "toISOYear": TorQLFunctionMeta("toISOYear", 1, 1),
    "toISOWeek": TorQLFunctionMeta("toISOWeek", 1, 1),
    "toWeek": TorQLFunctionMeta("toWeek", 1, 3),
    "toYearWeek": TorQLFunctionMeta("toYearWeek", 1, 3),
    "age": TorQLFunctionMeta("age", 3, 3),
    "dateDiff": TorQLFunctionMeta("dateDiff", 3, 3),
    "dateTrunc": TorQLFunctionMeta("dateTrunc", 2, 2),
    "dateAdd": TorQLFunctionMeta("dateAdd", 2, 2),
    "dateSub": TorQLFunctionMeta("dateSub", 3, 3),
    "timeStampAdd": TorQLFunctionMeta("timeStampAdd", 2, 2),
    "timeStampSub": TorQLFunctionMeta("timeStampSub", 2, 2),
    "now": TorQLFunctionMeta("now64", 0, 1, tz_aware=True, case_sensitive=False),
    "nowInBlock": TorQLFunctionMeta("nowInBlock", 1, 1),
    "rowNumberInBlock": TorQLFunctionMeta("rowNumberInBlock", 0, 0),
    "rowNumberInAllBlocks": TorQLFunctionMeta("rowNumberInAllBlocks", 0, 0),
    "today": TorQLFunctionMeta("today"),
    "yesterday": TorQLFunctionMeta("yesterday"),
    "timeSlot": TorQLFunctionMeta("timeSlot", 1, 1),
    "toYYYYMM": TorQLFunctionMeta("toYYYYMM", 1, 1),
    "toYYYYMMDD": TorQLFunctionMeta("toYYYYMMDD", 1, 1),
    "toYYYYMMDDhhmmss": TorQLFunctionMeta("toYYYYMMDDhhmmss", 1, 1),
    "addYears": TorQLFunctionMeta("addYears", 2, 2),
    "addMonths": TorQLFunctionMeta("addMonths", 2, 2),
    "addWeeks": TorQLFunctionMeta("addWeeks", 2, 2),
    "addDays": TorQLFunctionMeta("addDays", 2, 2),
    "addHours": TorQLFunctionMeta("addHours", 2, 2),
    "addMinutes": TorQLFunctionMeta("addMinutes", 2, 2),
    "addSeconds": TorQLFunctionMeta("addSeconds", 2, 2),
    "addQuarters": TorQLFunctionMeta("addQuarters", 2, 2),
    "subtractYears": TorQLFunctionMeta("subtractYears", 2, 2),
    "subtractMonths": TorQLFunctionMeta("subtractMonths", 2, 2),
    "subtractWeeks": TorQLFunctionMeta("subtractWeeks", 2, 2),
    "subtractDays": TorQLFunctionMeta("subtractDays", 2, 2),
    "subtractHours": TorQLFunctionMeta("subtractHours", 2, 2),
    "subtractMinutes": TorQLFunctionMeta("subtractMinutes", 2, 2),
    "subtractSeconds": TorQLFunctionMeta("subtractSeconds", 2, 2),
    "subtractQuarters": TorQLFunctionMeta("subtractQuarters", 2, 2),
    "timeSlots": TorQLFunctionMeta("timeSlots", 2, 3),
    "formatDateTime": TorQLFunctionMeta("formatDateTime", 2, 3),
    "dateName": TorQLFunctionMeta("dateName", 2, 2),
    "monthName": TorQLFunctionMeta("monthName", 1, 1),
    "fromUnixTimestamp": TorQLFunctionMeta(
        "fromUnixTimestamp",
        1,
        1,
        signatures=[
            ((IntegerType(),), DateTimeType()),
        ],
    ),
    "toModifiedJulianDay": TorQLFunctionMeta("toModifiedJulianDayOrNull", 1, 1),
    "fromModifiedJulianDay": TorQLFunctionMeta("fromModifiedJulianDayOrNull", 1, 1),
    "toIntervalSecond": TorQLFunctionMeta("toIntervalSecond", 1, 1),
    "toIntervalMinute": TorQLFunctionMeta("toIntervalMinute", 1, 1),
    "toIntervalHour": TorQLFunctionMeta("toIntervalHour", 1, 1),
    "toIntervalDay": TorQLFunctionMeta("toIntervalDay", 1, 1),
    "toIntervalWeek": TorQLFunctionMeta("toIntervalWeek", 1, 1),
    "toIntervalMonth": TorQLFunctionMeta("toIntervalMonth", 1, 1),
    "toIntervalQuarter": TorQLFunctionMeta("toIntervalQuarter", 1, 1),
    "toIntervalYear": TorQLFunctionMeta("toIntervalYear", 1, 1),
    # strings
    "left": TorQLFunctionMeta("left", 2, 2),
    "right": TorQLFunctionMeta("right", 2, 2),
    "lengthUTF8": TorQLFunctionMeta("lengthUTF8", 1, 1),
    "leftPad": TorQLFunctionMeta("leftPad", 2, 3),
    "rightPad": TorQLFunctionMeta("rightPad", 2, 3),
    "leftPadUTF8": TorQLFunctionMeta("leftPadUTF8", 2, 3),
    "rightPadUTF8": TorQLFunctionMeta("rightPadUTF8", 2, 3),
    "lower": TorQLFunctionMeta("lower", 1, 1, case_sensitive=False),
    "upper": TorQLFunctionMeta("upper", 1, 1, case_sensitive=False),
    "lowerUTF8": TorQLFunctionMeta("lowerUTF8", 1, 1),
    "upperUTF8": TorQLFunctionMeta("upperUTF8", 1, 1),
    "isValidUTF8": TorQLFunctionMeta("isValidUTF8", 1, 1),
    "toValidUTF8": TorQLFunctionMeta("toValidUTF8", 1, 1),
    "repeat": TorQLFunctionMeta("repeat", 2, 2, case_sensitive=False),
    "format": TorQLFunctionMeta("format", 2, None),
    "reverseUTF8": TorQLFunctionMeta("reverseUTF8", 1, 1),
    "concat": TorQLFunctionMeta("concat", 2, None, case_sensitive=False),
    "substring": TorQLFunctionMeta("substring", 3, 3, case_sensitive=False),
    "substringUTF8": TorQLFunctionMeta("substringUTF8", 3, 3),
    "appendTrailingCharIfAbsent": TorQLFunctionMeta("appendTrailingCharIfAbsent", 2, 2),
    "convertCharset": TorQLFunctionMeta("convertCharset", 3, 3),
    "base58Encode": TorQLFunctionMeta("base58Encode", 1, 1),
    "base58Decode": TorQLFunctionMeta("base58Decode", 1, 1),
    "tryBase58Decode": TorQLFunctionMeta("tryBase58Decode", 1, 1),
    "base64Encode": TorQLFunctionMeta("base64Encode", 1, 1),
    "base64Decode": TorQLFunctionMeta("base64Decode", 1, 1),
    "tryBase64Decode": TorQLFunctionMeta("tryBase64Decode", 1, 1),
    "endsWith": TorQLFunctionMeta("endsWith", 2, 2),
    "startsWith": TorQLFunctionMeta("startsWith", 2, 2),
    "trim": TorQLFunctionMeta("trim", 1, 2, case_sensitive=False),
    "trimLeft": TorQLFunctionMeta("trimLeft", 1, 2),
    "trimRight": TorQLFunctionMeta("trimRight", 1, 2),
    "encodeXMLComponent": TorQLFunctionMeta("encodeXMLComponent", 1, 1),
    "decodeXMLComponent": TorQLFunctionMeta("decodeXMLComponent", 1, 1),
    "extractTextFromHTML": TorQLFunctionMeta("extractTextFromHTML", 1, 1),
    "ascii": TorQLFunctionMeta("ascii", 1, 1, case_sensitive=False),
    "concatWithSeparator": TorQLFunctionMeta("concatWithSeparator", 2, None),
    # searching in strings
    "position": TorQLFunctionMeta("position", 2, 3, case_sensitive=False),
    "positionCaseInsensitive": TorQLFunctionMeta("positionCaseInsensitive", 2, 3),
    "positionUTF8": TorQLFunctionMeta("positionUTF8", 2, 3),
    "positionCaseInsensitiveUTF8": TorQLFunctionMeta("positionCaseInsensitiveUTF8", 2, 3),
    "multiSearchAllPositions": TorQLFunctionMeta("multiSearchAllPositions", 2, 2),
    "multiSearchAllPositionsUTF8": TorQLFunctionMeta("multiSearchAllPositionsUTF8", 2, 2),
    "multiSearchFirstPosition": TorQLFunctionMeta("multiSearchFirstPosition", 2, 2),
    "multiSearchFirstIndex": TorQLFunctionMeta("multiSearchFirstIndex", 2, 2),
    "multiSearchAny": TorQLFunctionMeta("multiSearchAny", 2, 2),
    "match": TorQLFunctionMeta("match", 2, 2),
    "multiMatchAny": TorQLFunctionMeta("multiMatchAny", 2, 2),
    "multiMatchAnyIndex": TorQLFunctionMeta("multiMatchAnyIndex", 2, 2),
    "multiMatchAllIndices": TorQLFunctionMeta("multiMatchAllIndices", 2, 2),
    "multiFuzzyMatchAny": TorQLFunctionMeta("multiFuzzyMatchAny", 3, 3),
    "multiFuzzyMatchAnyIndex": TorQLFunctionMeta("multiFuzzyMatchAnyIndex", 3, 3),
    "multiFuzzyMatchAllIndices": TorQLFunctionMeta("multiFuzzyMatchAllIndices", 3, 3),
    "extract": TorQLFunctionMeta("extract", 2, 2, case_sensitive=False),
    "extractAll": TorQLFunctionMeta("extractAll", 2, 2),
    "extractAllGroupsHorizontal": TorQLFunctionMeta("extractAllGroupsHorizontal", 2, 2),
    "extractAllGroupsVertical": TorQLFunctionMeta("extractAllGroupsVertical", 2, 2),
    "like": TorQLFunctionMeta("like", 2, 2),
    "ilike": TorQLFunctionMeta("ilike", 2, 2),
    "notLike": TorQLFunctionMeta("notLike", 2, 2),
    "notILike": TorQLFunctionMeta("notILike", 2, 2),
    "ngramDistance": TorQLFunctionMeta("ngramDistance", 2, 2),
    "ngramSearch": TorQLFunctionMeta("ngramSearch", 2, 2),
    "countSubstrings": TorQLFunctionMeta("countSubstrings", 2, 3),
    "countSubstringsCaseInsensitive": TorQLFunctionMeta("countSubstringsCaseInsensitive", 2, 3),
    "countSubstringsCaseInsensitiveUTF8": TorQLFunctionMeta("countSubstringsCaseInsensitiveUTF8", 2, 3),
    "countMatches": TorQLFunctionMeta("countMatches", 2, 2),
    "regexpExtract": TorQLFunctionMeta("regexpExtract", 2, 3),
    # replacing in strings
    "replace": TorQLFunctionMeta("replace", 3, 3, case_sensitive=False),
    "replaceAll": TorQLFunctionMeta("replaceAll", 3, 3),
    "replaceOne": TorQLFunctionMeta("replaceOne", 3, 3),
    "replaceRegexpAll": TorQLFunctionMeta("replaceRegexpAll", 3, 3),
    "replaceRegexpOne": TorQLFunctionMeta("replaceRegexpOne", 3, 3),
    "regexpQuoteMeta": TorQLFunctionMeta("regexpQuoteMeta", 1, 1),
    "translate": TorQLFunctionMeta("translate", 3, 3),
    "translateUTF8": TorQLFunctionMeta("translateUTF8", 3, 3),
    # conditional
    "if": TorQLFunctionMeta("if", 3, 3, case_sensitive=False),
    "multiIf": TorQLFunctionMeta("multiIf", 3, None),
    # mathematical
    "e": TorQLFunctionMeta("e"),
    "pi": TorQLFunctionMeta("pi"),
    "exp": TorQLFunctionMeta("exp", 1, 1, case_sensitive=False),
    "log": TorQLFunctionMeta("log", 1, 1, case_sensitive=False),
    "ln": TorQLFunctionMeta("ln", 1, 1, case_sensitive=False),
    "exp2": TorQLFunctionMeta("exp2", 1, 1),
    "log2": TorQLFunctionMeta("log2", 1, 1, case_sensitive=False),
    "exp10": TorQLFunctionMeta("exp10", 1, 1),
    "log10": TorQLFunctionMeta("log10", 1, 1, case_sensitive=False),
    "sqrt": TorQLFunctionMeta("sqrt", 1, 1, case_sensitive=False),
    "cbrt": TorQLFunctionMeta("cbrt", 1, 1),
    "erf": TorQLFunctionMeta("erf", 1, 1),
    "erfc": TorQLFunctionMeta("erfc", 1, 1),
    "lgamma": TorQLFunctionMeta("lgamma", 1, 1),
    "tgamma": TorQLFunctionMeta("tgamma", 1, 1),
    "sin": TorQLFunctionMeta("sin", 1, 1, case_sensitive=False),
    "cos": TorQLFunctionMeta("cos", 1, 1, case_sensitive=False),
    "tan": TorQLFunctionMeta("tan", 1, 1, case_sensitive=False),
    "asin": TorQLFunctionMeta("asin", 1, 1, case_sensitive=False),
    "acos": TorQLFunctionMeta("acos", 1, 1, case_sensitive=False),
    "atan": TorQLFunctionMeta("atan", 1, 1, case_sensitive=False),
    "pow": TorQLFunctionMeta("pow", 2, 2, case_sensitive=False),
    "power": TorQLFunctionMeta("power", 2, 2, case_sensitive=False),
    "intExp2": TorQLFunctionMeta("intExp2", 1, 1),
    "intExp10": TorQLFunctionMeta("intExp10", 1, 1),
    "cosh": TorQLFunctionMeta("cosh", 1, 1),
    "acosh": TorQLFunctionMeta("acosh", 1, 1),
    "sinh": TorQLFunctionMeta("sinh", 1, 1),
    "asinh": TorQLFunctionMeta("asinh", 1, 1),
    "atanh": TorQLFunctionMeta("atanh", 1, 1),
    "atan2": TorQLFunctionMeta("atan2", 2, 2),
    "hypot": TorQLFunctionMeta("hypot", 2, 2),
    "log1p": TorQLFunctionMeta("log1p", 1, 1),
    "sign": TorQLFunctionMeta("sign", 1, 1, case_sensitive=False),
    "degrees": TorQLFunctionMeta("degrees", 1, 1, case_sensitive=False),
    "radians": TorQLFunctionMeta("radians", 1, 1, case_sensitive=False),
    "factorial": TorQLFunctionMeta("factorial", 1, 1, case_sensitive=False),
    "width_bucket": TorQLFunctionMeta("width_bucket", 4, 4),
    # rounding
    "floor": TorQLFunctionMeta("floor", 1, 2, case_sensitive=False),
    "ceil": TorQLFunctionMeta("ceil", 1, 2, case_sensitive=False),
    "trunc": TorQLFunctionMeta("trunc", 1, 2, case_sensitive=False),
    "round": TorQLFunctionMeta("round", 1, 2, case_sensitive=False),
    "roundBankers": TorQLFunctionMeta("roundBankers", 1, 2),
    "roundToExp2": TorQLFunctionMeta("roundToExp2", 1, 1),
    "roundDuration": TorQLFunctionMeta("roundDuration", 1, 1),
    "roundAge": TorQLFunctionMeta("roundAge", 1, 1),
    "roundDown": TorQLFunctionMeta("roundDown", 2, 2),
    # maps
    "map": TorQLFunctionMeta("map", 2, None),
    "mapFromArrays": TorQLFunctionMeta("mapFromArrays", 2, 2),
    "mapAdd": TorQLFunctionMeta("mapAdd", 2, None),
    "mapSubtract": TorQLFunctionMeta("mapSubtract", 2, None),
    "mapPopulateSeries": TorQLFunctionMeta("mapPopulateSeries", 1, 3),
    "mapContains": TorQLFunctionMeta("mapContains", 2, 2),
    "mapKeys": TorQLFunctionMeta("mapKeys", 1, 1),
    "mapValues": TorQLFunctionMeta("mapValues", 1, 1),
    "mapContainsKeyLike": TorQLFunctionMeta("mapContainsKeyLike", 2, 2),
    "mapExtractKeyLike": TorQLFunctionMeta("mapExtractKeyLike", 2, 2),
    "mapApply": TorQLFunctionMeta("mapApply", 2, 2),
    "mapFilter": TorQLFunctionMeta("mapFilter", 2, 2),
    "mapUpdate": TorQLFunctionMeta("mapUpdate", 2, 2),
    # splitting strings
    "splitByChar": TorQLFunctionMeta("splitByChar", 2, 3),
    "splitByString": TorQLFunctionMeta("splitByString", 2, 3),
    "splitByRegexp": TorQLFunctionMeta("splitByRegexp", 2, 3),
    "splitByWhitespace": TorQLFunctionMeta("splitByWhitespace", 1, 2),
    "splitByNonAlpha": TorQLFunctionMeta("splitByNonAlpha", 1, 2),
    "arrayStringConcat": TorQLFunctionMeta("arrayStringConcat", 1, 2),
    "alphaTokens": TorQLFunctionMeta("alphaTokens", 1, 2),
    "extractAllGroups": TorQLFunctionMeta("extractAllGroups", 2, 2),
    "ngrams": TorQLFunctionMeta("ngrams", 2, 2),
    "tokens": TorQLFunctionMeta("tokens", 1, 1),
    # bit
    "bitAnd": TorQLFunctionMeta("bitAnd", 2, 2),
    "bitOr": TorQLFunctionMeta("bitOr", 2, 2),
    "bitXor": TorQLFunctionMeta("bitXor", 2, 2),
    "bitNot": TorQLFunctionMeta("bitNot", 1, 1),
    "bitShiftLeft": TorQLFunctionMeta("bitShiftLeft", 2, 2),
    "bitShiftRight": TorQLFunctionMeta("bitShiftRight", 2, 2),
    "bitRotateLeft": TorQLFunctionMeta("bitRotateLeft", 2, 2),
    "bitRotateRight": TorQLFunctionMeta("bitRotateRight", 2, 2),
    "bitSlice": TorQLFunctionMeta("bitSlice", 3, 3),
    "bitTest": TorQLFunctionMeta("bitTest", 2, 2),
    "bitTestAll": TorQLFunctionMeta("bitTestAll", 3, None),
    "bitTestAny": TorQLFunctionMeta("bitTestAny", 3, None),
    "bitCount": TorQLFunctionMeta("bitCount", 1, 1),
    "bitHammingDistance": TorQLFunctionMeta("bitHammingDistance", 2, 2),
    # bitmap
    "bitmapBuild": TorQLFunctionMeta("bitmapBuild", 1, 1),
    "bitmapToArray": TorQLFunctionMeta("bitmapToArray", 1, 1),
    "bitmapSubsetInRange": TorQLFunctionMeta("bitmapSubsetInRange", 3, 3),
    "bitmapSubsetLimit": TorQLFunctionMeta("bitmapSubsetLimit", 3, 3),
    "subBitmap": TorQLFunctionMeta("subBitmap", 3, 3),
    "bitmapContains": TorQLFunctionMeta("bitmapContains", 2, 2),
    "bitmapHasAny": TorQLFunctionMeta("bitmapHasAny", 2, 2),
    "bitmapHasAll": TorQLFunctionMeta("bitmapHasAll", 2, 2),
    "bitmapCardinality": TorQLFunctionMeta("bitmapCardinality", 1, 1),
    "bitmapMin": TorQLFunctionMeta("bitmapMin", 1, 1),
    "bitmapMax": TorQLFunctionMeta("bitmapMax", 1, 1),
    "bitmapTransform": TorQLFunctionMeta("bitmapTransform", 3, 3),
    "bitmapAnd": TorQLFunctionMeta("bitmapAnd", 2, 2),
    "bitmapOr": TorQLFunctionMeta("bitmapOr", 2, 2),
    "bitmapXor": TorQLFunctionMeta("bitmapXor", 2, 2),
    "bitmapAndnot": TorQLFunctionMeta("bitmapAndnot", 2, 2),
    "bitmapAndCardinality": TorQLFunctionMeta("bitmapAndCardinality", 2, 2),
    "bitmapOrCardinality": TorQLFunctionMeta("bitmapOrCardinality", 2, 2),
    "bitmapXorCardinality": TorQLFunctionMeta("bitmapXorCardinality", 2, 2),
    "bitmapAndnotCardinality": TorQLFunctionMeta("bitmapAndnotCardinality", 2, 2),
    # urls TODO
    "protocol": TorQLFunctionMeta("protocol", 1, 1),
    "domain": TorQLFunctionMeta("domain", 1, 1),
    "domainWithoutWWW": TorQLFunctionMeta("domainWithoutWWW", 1, 1),
    "topLevelDomain": TorQLFunctionMeta("topLevelDomain", 1, 1),
    "firstSignificantSubdomain": TorQLFunctionMeta("firstSignificantSubdomain", 1, 1),
    "cutToFirstSignificantSubdomain": TorQLFunctionMeta("cutToFirstSignificantSubdomain", 1, 1),
    "cutToFirstSignificantSubdomainWithWWW": TorQLFunctionMeta("cutToFirstSignificantSubdomainWithWWW", 1, 1),
    "port": TorQLFunctionMeta("port", 1, 2),
    "path": TorQLFunctionMeta("path", 1, 1),
    "pathFull": TorQLFunctionMeta("pathFull", 1, 1),
    "queryString": TorQLFunctionMeta("queryString", 1, 1),
    "fragment": TorQLFunctionMeta("fragment", 1, 1),
    "queryStringAndFragment": TorQLFunctionMeta("queryStringAndFragment", 1, 1),
    "extractURLParameter": TorQLFunctionMeta("extractURLParameter", 2, 2),
    "extractURLParameters": TorQLFunctionMeta("extractURLParameters", 1, 1),
    "extractURLParameterNames": TorQLFunctionMeta("extractURLParameterNames", 1, 1),
    "URLHierarchy": TorQLFunctionMeta("URLHierarchy", 1, 1),
    "URLPathHierarchy": TorQLFunctionMeta("URLPathHierarchy", 1, 1),
    "encodeURLComponent": TorQLFunctionMeta("encodeURLComponent", 1, 1),
    "decodeURLComponent": TorQLFunctionMeta("decodeURLComponent", 1, 1),
    "encodeURLFormComponent": TorQLFunctionMeta("encodeURLFormComponent", 1, 1),
    "decodeURLFormComponent": TorQLFunctionMeta("decodeURLFormComponent", 1, 1),
    "netloc": TorQLFunctionMeta("netloc", 1, 1),
    "cutWWW": TorQLFunctionMeta("cutWWW", 1, 1),
    "cutQueryString": TorQLFunctionMeta("cutQueryString", 1, 1),
    "cutFragment": TorQLFunctionMeta("cutFragment", 1, 1),
    "cutQueryStringAndFragment": TorQLFunctionMeta("cutQueryStringAndFragment", 1, 1),
    "cutURLParameter": TorQLFunctionMeta("cutURLParameter", 2, 2),
    # json
    "isValidJSON": TorQLFunctionMeta("isValidJSON", 1, 1),
    "JSONHas": TorQLFunctionMeta("JSONHas", 1, None),
    "JSONLength": TorQLFunctionMeta("JSONLength", 1, None),
    "JSONArrayLength": TorQLFunctionMeta("JSONArrayLength", 1, None),
    "JSONType": TorQLFunctionMeta("JSONType", 1, None),
    "JSONExtract": TorQLFunctionMeta("JSONExtract", 2, None),
    "JSONExtractUInt": TorQLFunctionMeta("JSONExtractUInt", 1, None),
    "JSONExtractInt": TorQLFunctionMeta("JSONExtractInt", 1, None),
    "JSONExtractFloat": TorQLFunctionMeta("JSONExtractFloat", 1, None),
    "JSONExtractBool": TorQLFunctionMeta("JSONExtractBool", 1, None),
    "JSONExtractString": TorQLFunctionMeta("JSONExtractString", 1, None),
    "JSONExtractKey": TorQLFunctionMeta("JSONExtractKey", 1, None),
    "JSONExtractKeys": TorQLFunctionMeta("JSONExtractKeys", 1, None),
    "JSONExtractRaw": TorQLFunctionMeta("JSONExtractRaw", 1, None),
    "JSONExtractArrayRaw": TorQLFunctionMeta("JSONExtractArrayRaw", 1, None),
    "JSONExtractKeysAndValues": TorQLFunctionMeta("JSONExtractKeysAndValues", 1, 3),
    "JSONExtractKeysAndValuesRaw": TorQLFunctionMeta("JSONExtractKeysAndValuesRaw", 1, None),
    # in
    "in": TorQLFunctionMeta("in", 2, 2),
    "notIn": TorQLFunctionMeta("notIn", 2, 2),
    # geo
    "greatCircleDistance": TorQLFunctionMeta("greatCircleDistance", 4, 4),
    "geoDistance": TorQLFunctionMeta("geoDistance", 4, 4),
    "greatCircleAngle": TorQLFunctionMeta("greatCircleAngle", 4, 4),
    "pointInEllipses": TorQLFunctionMeta("pointInEllipses", 6, None),
    "pointInPolygon": TorQLFunctionMeta("pointInPolygon", 2, None),
    "geohashEncode": TorQLFunctionMeta("geohashEncode", 2, 3),
    "geohashDecode": TorQLFunctionMeta("geohashDecode", 1, 1),
    "geohashesInBox": TorQLFunctionMeta("geohashesInBox", 5, 5),
    # nullable
    "isnull": TorQLFunctionMeta("isNull", 1, 1, case_sensitive=False),
    "isNotNull": TorQLFunctionMeta("isNotNull", 1, 1),
    "coalesce": TorQLFunctionMeta("coalesce", 1, None, case_sensitive=False),
    "ifnull": TorQLFunctionMeta("ifNull", 2, 2, case_sensitive=False),
    "nullif": TorQLFunctionMeta("nullIf", 2, 2, case_sensitive=False),
    "assumeNotNull": TorQLFunctionMeta("assumeNotNull", 1, 1),
    "toNullable": TorQLFunctionMeta("toNullable", 1, 1),
    # tuples
    "tuple": TorQLFunctionMeta("tuple", 0, None),
    "tupleElement": TorQLFunctionMeta("tupleElement", 2, 3),
    "untuple": TorQLFunctionMeta("untuple", 1, 1),
    "tupleHammingDistance": TorQLFunctionMeta("tupleHammingDistance", 2, 2),
    "tupleToNameValuePairs": TorQLFunctionMeta("tupleToNameValuePairs", 1, 1),
    "tuplePlus": TorQLFunctionMeta("tuplePlus", 2, 2),
    "tupleMinus": TorQLFunctionMeta("tupleMinus", 2, 2),
    "tupleMultiply": TorQLFunctionMeta("tupleMultiply", 2, 2),
    "tupleDivide": TorQLFunctionMeta("tupleDivide", 2, 2),
    "tupleNegate": TorQLFunctionMeta("tupleNegate", 1, 1),
    "tupleMultiplyByNumber": TorQLFunctionMeta("tupleMultiplyByNumber", 2, 2),
    "tupleDivideByNumber": TorQLFunctionMeta("tupleDivideByNumber", 2, 2),
    "dotProduct": TorQLFunctionMeta("dotProduct", 2, 2),
    # other
    "isFinite": TorQLFunctionMeta("isFinite", 1, 1),
    "isInfinite": TorQLFunctionMeta("isInfinite", 1, 1),
    "ifNotFinite": TorQLFunctionMeta("ifNotFinite", 1, 1),
    "isNaN": TorQLFunctionMeta("isNaN", 1, 1),
    "bar": TorQLFunctionMeta("bar", 4, 4),
    "transform": TorQLFunctionMeta("transform", 3, 4),
    "formatReadableDecimalSize": TorQLFunctionMeta("formatReadableDecimalSize", 1, 1),
    "formatReadableSize": TorQLFunctionMeta("formatReadableSize", 1, 1),
    "formatReadableQuantity": TorQLFunctionMeta("formatReadableQuantity", 1, 1),
    "formatReadableTimeDelta": TorQLFunctionMeta("formatReadableTimeDelta", 1, 2),
    "least": TorQLFunctionMeta("least", 2, 2, case_sensitive=False),
    "greatest": TorQLFunctionMeta("greatest", 2, 2, case_sensitive=False),
    # time window
    "tumble": TorQLFunctionMeta("tumble", 2, 2),
    "hop": TorQLFunctionMeta("hop", 3, 3),
    "tumbleStart": TorQLFunctionMeta("tumbleStart", 1, 3),
    "tumbleEnd": TorQLFunctionMeta("tumbleEnd", 1, 3),
    "hopStart": TorQLFunctionMeta("hopStart", 1, 3),
    "hopEnd": TorQLFunctionMeta("hopEnd", 1, 3),
    # distance window
    "L1Norm": TorQLFunctionMeta("L1Norm", 1, 1),
    "L2Norm": TorQLFunctionMeta("L2Norm", 1, 1),
    "LinfNorm": TorQLFunctionMeta("LinfNorm", 1, 1),
    "LpNorm": TorQLFunctionMeta("LpNorm", 2, 2),
    "L1Distance": TorQLFunctionMeta("L1Distance", 2, 2),
    "L2Distance": TorQLFunctionMeta("L2Distance", 2, 2),
    "LinfDistance": TorQLFunctionMeta("LinfDistance", 2, 2),
    "LpDistance": TorQLFunctionMeta("LpDistance", 3, 3),
    "L1Normalize": TorQLFunctionMeta("L1Normalize", 1, 1),
    "L2Normalize": TorQLFunctionMeta("L2Normalize", 1, 1),
    "LinfNormalize": TorQLFunctionMeta("LinfNormalize", 1, 1),
    "LpNormalize": TorQLFunctionMeta("LpNormalize", 2, 2),
    "cosineDistance": TorQLFunctionMeta("cosineDistance", 2, 2),
    # window functions
    "rank": TorQLFunctionMeta("rank"),
    "dense_rank": TorQLFunctionMeta("dense_rank"),
    "row_number": TorQLFunctionMeta("row_number"),
    "first_value": TorQLFunctionMeta("first_value", 1, 1),
    "last_value": TorQLFunctionMeta("last_value", 1, 1),
    "nth_value": TorQLFunctionMeta("nth_value", 2, 2),
    "lagInFrame": TorQLFunctionMeta("lagInFrame", 1, 1),
    "leadInFrame": TorQLFunctionMeta("leadInFrame", 1, 1),
    # table functions
    "generateSeries": TorQLFunctionMeta("generate_series", 3, 3),
}

# Permitted TorQL aggregations
TORQL_AGGREGATIONS: dict[str, TorQLFunctionMeta] = {
    # Standard aggregate functions
    "count": TorQLFunctionMeta("count", 0, 1, aggregate=True, case_sensitive=False),
    "countIf": TorQLFunctionMeta("countIf", 1, 2, aggregate=True),
    "countDistinctIf": TorQLFunctionMeta("countDistinctIf", 1, 2, aggregate=True),
    "min": TorQLFunctionMeta("min", 1, 1, aggregate=True, case_sensitive=False),
    "minIf": TorQLFunctionMeta("minIf", 2, 2, aggregate=True),
    "max": TorQLFunctionMeta("max", 1, 1, aggregate=True, case_sensitive=False),
    "maxIf": TorQLFunctionMeta("maxIf", 2, 2, aggregate=True),
    "sum": TorQLFunctionMeta("sum", 1, 1, aggregate=True, case_sensitive=False),
    "sumIf": TorQLFunctionMeta("sumIf", 2, 2, aggregate=True),
    "avg": TorQLFunctionMeta("avg", 1, 1, aggregate=True, case_sensitive=False),
    "avgIf": TorQLFunctionMeta("avgIf", 2, 2, aggregate=True),
    "any": TorQLFunctionMeta("any", 1, 1, aggregate=True),
    "anyIf": TorQLFunctionMeta("anyIf", 2, 2, aggregate=True),
    "stddevPop": TorQLFunctionMeta("stddevPop", 1, 1, aggregate=True),
    "stddevPopIf": TorQLFunctionMeta("stddevPopIf", 2, 2, aggregate=True),
    "stddevSamp": TorQLFunctionMeta("stddevSamp", 1, 1, aggregate=True),
    "stddevSampIf": TorQLFunctionMeta("stddevSampIf", 2, 2, aggregate=True),
    "varPop": TorQLFunctionMeta("varPop", 1, 1, aggregate=True),
    "varPopIf": TorQLFunctionMeta("varPopIf", 2, 2, aggregate=True),
    "varSamp": TorQLFunctionMeta("varSamp", 1, 1, aggregate=True),
    "varSampIf": TorQLFunctionMeta("varSampIf", 2, 2, aggregate=True),
    "covarPop": TorQLFunctionMeta("covarPop", 2, 2, aggregate=True),
    "covarPopIf": TorQLFunctionMeta("covarPopIf", 3, 3, aggregate=True),
    "covarSamp": TorQLFunctionMeta("covarSamp", 2, 2, aggregate=True),
    "covarSampIf": TorQLFunctionMeta("covarSampIf", 3, 3, aggregate=True),
    "corr": TorQLFunctionMeta("corr", 2, 2, aggregate=True),
    # ClickHouse-specific aggregate functions
    "anyHeavy": TorQLFunctionMeta("anyHeavy", 1, 1, aggregate=True),
    "anyHeavyIf": TorQLFunctionMeta("anyHeavyIf", 2, 2, aggregate=True),
    "anyLast": TorQLFunctionMeta("anyLast", 1, 1, aggregate=True),
    "anyLastIf": TorQLFunctionMeta("anyLastIf", 2, 2, aggregate=True),
    "argMin": TorQLFunctionMeta("argMin", 2, 2, aggregate=True),
    "argMinIf": TorQLFunctionMeta("argMinIf", 3, 3, aggregate=True),
    "argMax": TorQLFunctionMeta("argMax", 2, 2, aggregate=True),
    "argMaxIf": TorQLFunctionMeta("argMaxIf", 3, 3, aggregate=True),
    "argMinMerge": TorQLFunctionMeta("argMinMerge", 1, 1, aggregate=True),
    "argMaxMerge": TorQLFunctionMeta("argMaxMerge", 1, 1, aggregate=True),
    "avgState": TorQLFunctionMeta("avgState", 1, 1, aggregate=True),
    "avgMerge": TorQLFunctionMeta("avgMerge", 1, 1, aggregate=True),
    "avgWeighted": TorQLFunctionMeta("avgWeighted", 2, 2, aggregate=True),
    "avgWeightedIf": TorQLFunctionMeta("avgWeightedIf", 3, 3, aggregate=True),
    "avgArray": TorQLFunctionMeta("avgArrayOrNull", 1, 1, aggregate=True),
    "topK": TorQLFunctionMeta("topK", 1, 1, min_params=1, max_params=1, aggregate=True),
    # "topKIf": TorQLFunctionMeta("topKIf", 2, 2, aggregate=True),
    # "topKWeighted": TorQLFunctionMeta("topKWeighted", 1, 1, aggregate=True),
    # "topKWeightedIf": TorQLFunctionMeta("topKWeightedIf", 2, 2, aggregate=True),
    "groupArray": TorQLFunctionMeta("groupArray", 1, 1, aggregate=True),
    "groupArrayIf": TorQLFunctionMeta("groupArrayIf", 2, 2, aggregate=True),
    # "groupArrayLast": TorQLFunctionMeta("groupArrayLast", 1, 1, aggregate=True),
    # "groupArrayLastIf": TorQLFunctionMeta("groupArrayLastIf", 2, 2, aggregate=True),
    "groupUniqArray": TorQLFunctionMeta("groupUniqArray", 1, 1, aggregate=True),
    "groupUniqArrayIf": TorQLFunctionMeta("groupUniqArrayIf", 2, 2, aggregate=True),
    "groupArrayInsertAt": TorQLFunctionMeta("groupArrayInsertAt", 2, 2, aggregate=True),
    "groupArrayInsertAtIf": TorQLFunctionMeta("groupArrayInsertAtIf", 3, 3, aggregate=True),
    "groupArrayMovingAvg": TorQLFunctionMeta("groupArrayMovingAvg", 1, 1, aggregate=True),
    "groupArrayMovingAvgIf": TorQLFunctionMeta("groupArrayMovingAvgIf", 2, 2, aggregate=True),
    "groupArrayMovingSum": TorQLFunctionMeta("groupArrayMovingSum", 1, 1, aggregate=True),
    "groupArrayMovingSumIf": TorQLFunctionMeta("groupArrayMovingSumIf", 2, 2, aggregate=True),
    "groupBitAnd": TorQLFunctionMeta("groupBitAnd", 1, 1, aggregate=True),
    "groupBitAndIf": TorQLFunctionMeta("groupBitAndIf", 2, 2, aggregate=True),
    "groupBitOr": TorQLFunctionMeta("groupBitOr", 1, 1, aggregate=True),
    "groupBitOrIf": TorQLFunctionMeta("groupBitOrIf", 2, 2, aggregate=True),
    "groupBitXor": TorQLFunctionMeta("groupBitXor", 1, 1, aggregate=True),
    "groupBitXorIf": TorQLFunctionMeta("groupBitXorIf", 2, 2, aggregate=True),
    "groupBitmap": TorQLFunctionMeta("groupBitmap", 1, 1, aggregate=True),
    "groupBitmapIf": TorQLFunctionMeta("groupBitmapIf", 2, 2, aggregate=True),
    "groupBitmapAnd": TorQLFunctionMeta("groupBitmapAnd", 1, 1, aggregate=True),
    "groupBitmapAndIf": TorQLFunctionMeta("groupBitmapAndIf", 2, 2, aggregate=True),
    "groupBitmapOr": TorQLFunctionMeta("groupBitmapOr", 1, 1, aggregate=True),
    "groupBitmapOrIf": TorQLFunctionMeta("groupBitmapOrIf", 2, 2, aggregate=True),
    "groupBitmapXor": TorQLFunctionMeta("groupBitmapXor", 1, 1, aggregate=True),
    "groupBitmapXorIf": TorQLFunctionMeta("groupBitmapXorIf", 2, 2, aggregate=True),
    "sumWithOverflow": TorQLFunctionMeta("sumWithOverflow", 1, 1, aggregate=True),
    "sumWithOverflowIf": TorQLFunctionMeta("sumWithOverflowIf", 2, 2, aggregate=True),
    "deltaSum": TorQLFunctionMeta("deltaSum", 1, 1, aggregate=True),
    "deltaSumIf": TorQLFunctionMeta("deltaSumIf", 2, 2, aggregate=True),
    "deltaSumTimestamp": TorQLFunctionMeta("deltaSumTimestamp", 2, 2, aggregate=True),
    "deltaSumTimestampIf": TorQLFunctionMeta("deltaSumTimestampIf", 3, 3, aggregate=True),
    "sumMap": TorQLFunctionMeta("sumMap", 1, 2, aggregate=True),
    "sumMapIf": TorQLFunctionMeta("sumMapIf", 2, 3, aggregate=True),
    "sumMapMerge": TorQLFunctionMeta("sumMapMerge", 1, 1, aggregate=True),
    "minMap": TorQLFunctionMeta("minMap", 1, 2, aggregate=True),
    "minMapIf": TorQLFunctionMeta("minMapIf", 2, 3, aggregate=True),
    "maxMap": TorQLFunctionMeta("maxMap", 1, 2, aggregate=True),
    "maxMapIf": TorQLFunctionMeta("maxMapIf", 2, 3, aggregate=True),
    "medianArray": TorQLFunctionMeta("medianArrayOrNull", 1, 1, aggregate=True),
    "skewSamp": TorQLFunctionMeta("skewSamp", 1, 1, aggregate=True),
    "skewSampIf": TorQLFunctionMeta("skewSampIf", 2, 2, aggregate=True),
    "skewPop": TorQLFunctionMeta("skewPop", 1, 1, aggregate=True),
    "skewPopIf": TorQLFunctionMeta("skewPopIf", 2, 2, aggregate=True),
    "kurtSamp": TorQLFunctionMeta("kurtSamp", 1, 1, aggregate=True),
    "kurtSampIf": TorQLFunctionMeta("kurtSampIf", 2, 2, aggregate=True),
    "kurtPop": TorQLFunctionMeta("kurtPop", 1, 1, aggregate=True),
    "kurtPopIf": TorQLFunctionMeta("kurtPopIf", 2, 2, aggregate=True),
    "uniq": TorQLFunctionMeta("uniq", 1, None, aggregate=True),
    "uniqIf": TorQLFunctionMeta("uniqIf", 2, None, aggregate=True),
    "uniqExact": TorQLFunctionMeta("uniqExact", 1, None, aggregate=True),
    "uniqExactIf": TorQLFunctionMeta("uniqExactIf", 2, None, aggregate=True),
    # "uniqCombined": TorQLFunctionMeta("uniqCombined", 1, 1, aggregate=True),
    # "uniqCombinedIf": TorQLFunctionMeta("uniqCombinedIf", 2, 2, aggregate=True),
    # "uniqCombined64": TorQLFunctionMeta("uniqCombined64", 1, 1, aggregate=True),
    # "uniqCombined64If": TorQLFunctionMeta("uniqCombined64If", 2, 2, aggregate=True),
    "uniqHLL12": TorQLFunctionMeta("uniqHLL12", 1, None, aggregate=True),
    "uniqHLL12If": TorQLFunctionMeta("uniqHLL12If", 2, None, aggregate=True),
    "uniqTheta": TorQLFunctionMeta("uniqTheta", 1, None, aggregate=True),
    "uniqThetaIf": TorQLFunctionMeta("uniqThetaIf", 2, None, aggregate=True),
    "uniqMerge": TorQLFunctionMeta("uniqMerge", 1, 1, aggregate=True),
    "uniqUpToMerge": TorQLFunctionMeta("uniqUpToMerge", 1, 1, 1, 1, aggregate=True),
    "median": TorQLFunctionMeta("median", 1, 1, aggregate=True),
    "medianIf": TorQLFunctionMeta("medianIf", 2, 2, aggregate=True),
    "medianExact": TorQLFunctionMeta("medianExact", 1, 1, aggregate=True),
    "medianExactIf": TorQLFunctionMeta("medianExactIf", 2, 2, aggregate=True),
    "medianExactLow": TorQLFunctionMeta("medianExactLow", 1, 1, aggregate=True),
    "medianExactLowIf": TorQLFunctionMeta("medianExactLowIf", 2, 2, aggregate=True),
    "medianExactHigh": TorQLFunctionMeta("medianExactHigh", 1, 1, aggregate=True),
    "medianExactHighIf": TorQLFunctionMeta("medianExactHighIf", 2, 2, aggregate=True),
    "medianExactWeighted": TorQLFunctionMeta("medianExactWeighted", 1, 1, aggregate=True),
    "medianExactWeightedIf": TorQLFunctionMeta("medianExactWeightedIf", 2, 2, aggregate=True),
    "medianTiming": TorQLFunctionMeta("medianTiming", 1, 1, aggregate=True),
    "medianTimingIf": TorQLFunctionMeta("medianTimingIf", 2, 2, aggregate=True),
    "medianTimingWeighted": TorQLFunctionMeta("medianTimingWeighted", 1, 1, aggregate=True),
    "medianTimingWeightedIf": TorQLFunctionMeta("medianTimingWeightedIf", 2, 2, aggregate=True),
    "medianDeterministic": TorQLFunctionMeta("medianDeterministic", 1, 1, aggregate=True),
    "medianDeterministicIf": TorQLFunctionMeta("medianDeterministicIf", 2, 2, aggregate=True),
    "medianTDigest": TorQLFunctionMeta("medianTDigest", 1, 1, aggregate=True),
    "medianTDigestIf": TorQLFunctionMeta("medianTDigestIf", 2, 2, aggregate=True),
    "medianTDigestWeighted": TorQLFunctionMeta("medianTDigestWeighted", 1, 1, aggregate=True),
    "medianTDigestWeightedIf": TorQLFunctionMeta("medianTDigestWeightedIf", 2, 2, aggregate=True),
    "medianBFloat16": TorQLFunctionMeta("medianBFloat16", 1, 1, aggregate=True),
    "medianBFloat16If": TorQLFunctionMeta("medianBFloat16If", 2, 2, aggregate=True),
    "quantile": TorQLFunctionMeta("quantile", 1, 1, min_params=1, max_params=1, aggregate=True),
    "quantileIf": TorQLFunctionMeta("quantileIf", 2, 2, min_params=1, max_params=1, aggregate=True),
    "quantiles": TorQLFunctionMeta("quantiles", 1, None, aggregate=True),
    "quantilesIf": TorQLFunctionMeta("quantilesIf", 2, 2, min_params=1, max_params=1, aggregate=True),
    # "quantileExact": TorQLFunctionMeta("quantileExact", 1, 1, aggregate=True),
    # "quantileExactIf": TorQLFunctionMeta("quantileExactIf", 2, 2, aggregate=True),
    # "quantileExactLow": TorQLFunctionMeta("quantileExactLow", 1, 1, aggregate=True),
    # "quantileExactLowIf": TorQLFunctionMeta("quantileExactLowIf", 2, 2, aggregate=True),
    # "quantileExactHigh": TorQLFunctionMeta("quantileExactHigh", 1, 1, aggregate=True),
    # "quantileExactHighIf": TorQLFunctionMeta("quantileExactHighIf", 2, 2, aggregate=True),
    # "quantileExactWeighted": TorQLFunctionMeta("quantileExactWeighted", 1, 1, aggregate=True),
    # "quantileExactWeightedIf": TorQLFunctionMeta("quantileExactWeightedIf", 2, 2, aggregate=True),
    # "quantileTiming": TorQLFunctionMeta("quantileTiming", 1, 1, aggregate=True),
    # "quantileTimingIf": TorQLFunctionMeta("quantileTimingIf", 2, 2, aggregate=True),
    # "quantileTimingWeighted": TorQLFunctionMeta("quantileTimingWeighted", 1, 1, aggregate=True),
    # "quantileTimingWeightedIf": TorQLFunctionMeta("quantileTimingWeightedIf", 2, 2, aggregate=True),
    # "quantileDeterministic": TorQLFunctionMeta("quantileDeterministic", 1, 1, aggregate=True),
    # "quantileDeterministicIf": TorQLFunctionMeta("quantileDeterministicIf", 2, 2, aggregate=True),
    # "quantileTDigest": TorQLFunctionMeta("quantileTDigest", 1, 1, aggregate=True),
    # "quantileTDigestIf": TorQLFunctionMeta("quantileTDigestIf", 2, 2, aggregate=True),
    # "quantileTDigestWeighted": TorQLFunctionMeta("quantileTDigestWeighted", 1, 1, aggregate=True),
    # "quantileTDigestWeightedIf": TorQLFunctionMeta("quantileTDigestWeightedIf", 2, 2, aggregate=True),
    # "quantileBFloat16": TorQLFunctionMeta("quantileBFloat16", 1, 1, aggregate=True),
    # "quantileBFloat16If": TorQLFunctionMeta("quantileBFloat16If", 2, 2, aggregate=True),
    # "quantileBFloat16Weighted": TorQLFunctionMeta("quantileBFloat16Weighted", 1, 1, aggregate=True),
    # "quantileBFloat16WeightedIf": TorQLFunctionMeta("quantileBFloat16WeightedIf", 2, 2, aggregate=True),
    "simpleLinearRegression": TorQLFunctionMeta("simpleLinearRegression", 2, 2, aggregate=True),
    "simpleLinearRegressionIf": TorQLFunctionMeta("simpleLinearRegressionIf", 3, 3, aggregate=True),
    # "stochasticLinearRegression": TorQLFunctionMeta("stochasticLinearRegression", 1, 1, aggregate=True),
    # "stochasticLinearRegressionIf": TorQLFunctionMeta("stochasticLinearRegressionIf", 2, 2, aggregate=True),
    # "stochasticLogisticRegression": TorQLFunctionMeta("stochasticLogisticRegression", 1, 1, aggregate=True),
    # "stochasticLogisticRegressionIf": TorQLFunctionMeta("stochasticLogisticRegressionIf", 2, 2, aggregate=True),
    # "categoricalInformationValue": TorQLFunctionMeta("categoricalInformationValue", 1, 1, aggregate=True),
    # "categoricalInformationValueIf": TorQLFunctionMeta("categoricalInformationValueIf", 2, 2, aggregate=True),
    "contingency": TorQLFunctionMeta("contingency", 2, 2, aggregate=True),
    "contingencyIf": TorQLFunctionMeta("contingencyIf", 3, 3, aggregate=True),
    "cramersV": TorQLFunctionMeta("cramersV", 2, 2, aggregate=True),
    "cramersVIf": TorQLFunctionMeta("cramersVIf", 3, 3, aggregate=True),
    "cramersVBiasCorrected": TorQLFunctionMeta("cramersVBiasCorrected", 2, 2, aggregate=True),
    "cramersVBiasCorrectedIf": TorQLFunctionMeta("cramersVBiasCorrectedIf", 3, 3, aggregate=True),
    "theilsU": TorQLFunctionMeta("theilsU", 2, 2, aggregate=True),
    "theilsUIf": TorQLFunctionMeta("theilsUIf", 3, 3, aggregate=True),
    "maxIntersections": TorQLFunctionMeta("maxIntersections", 2, 2, aggregate=True),
    "maxIntersectionsIf": TorQLFunctionMeta("maxIntersectionsIf", 3, 3, aggregate=True),
    "maxIntersectionsPosition": TorQLFunctionMeta("maxIntersectionsPosition", 2, 2, aggregate=True),
    "maxIntersectionsPositionIf": TorQLFunctionMeta("maxIntersectionsPositionIf", 3, 3, aggregate=True),
}
TORQL_MARKETTOR_FUNCTIONS: dict[str, TorQLFunctionMeta] = {
    "matchesAction": TorQLFunctionMeta("matchesAction", 1, 1),
    "sparkline": TorQLFunctionMeta("sparkline", 1, 1),
    "recording_button": TorQLFunctionMeta("recording_button", 1, 1),
    "torql_lookupDomainType": TorQLFunctionMeta("torql_lookupDomainType", 1, 1),
    "torql_lookupPaidSourceType": TorQLFunctionMeta("torql_lookupPaidSourceType", 1, 1),
    "torql_lookupPaidMediumType": TorQLFunctionMeta("torql_lookupPaidMediumType", 1, 1),
    "torql_lookupOrganicSourceType": TorQLFunctionMeta("torql_lookupOrganicSourceType", 1, 1),
    "torql_lookupOrganicMediumType": TorQLFunctionMeta("torql_lookupOrganicMediumType", 1, 1),
}


UDFS: dict[str, TorQLFunctionMeta] = {
    "aggregate_funnel": TorQLFunctionMeta("aggregate_funnel", 6, 6, aggregate=False),
    "aggregate_funnel_array": TorQLFunctionMeta("aggregate_funnel_array", 6, 6, aggregate=False),
    "aggregate_funnel_cohort": TorQLFunctionMeta("aggregate_funnel_cohort", 6, 6, aggregate=False),
    "aggregate_funnel_trends": TorQLFunctionMeta("aggregate_funnel_trends", 7, 7, aggregate=False),
    "aggregate_funnel_array_trends": TorQLFunctionMeta("aggregate_funnel_array_trends", 7, 7, aggregate=False),
    "aggregate_funnel_cohort_trends": TorQLFunctionMeta("aggregate_funnel_cohort_trends", 7, 7, aggregate=False),
    "aggregate_funnel_test": TorQLFunctionMeta("aggregate_funnel_test", 6, 6, aggregate=False),
}
# We want CI to fail if there is a breaking change and the version hasn't been incremented
if is_cloud() or is_ci():
    from clairview.udf_versioner import augment_function_name

    for v in UDFS.values():
        v.clickhouse_name = augment_function_name(v.clickhouse_name)

TORQL_CLICKHOUSE_FUNCTIONS.update(UDFS)


ALL_EXPOSED_FUNCTION_NAMES = [
    name for name in chain(TORQL_CLICKHOUSE_FUNCTIONS.keys(), TORQL_AGGREGATIONS.keys()) if not name.startswith("_")
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


def _find_function(name: str, functions: dict[str, TorQLFunctionMeta]) -> Optional[TorQLFunctionMeta]:
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


def find_torql_aggregation(name: str) -> Optional[TorQLFunctionMeta]:
    return _find_function(name, TORQL_AGGREGATIONS)


def find_torql_function(name: str) -> Optional[TorQLFunctionMeta]:
    return _find_function(name, TORQL_CLICKHOUSE_FUNCTIONS)


def find_torql_clairview_function(name: str) -> Optional[TorQLFunctionMeta]:
    return _find_function(name, TORQL_MARKETTOR_FUNCTIONS)
