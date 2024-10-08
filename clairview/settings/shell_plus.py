from clairview.settings.utils import get_from_env, str_to_bool

# shell_plus settings
# https://django-extensions.readthedocs.io/en/latest/shell_plus.html

SHELL_PLUS_PRINT_SQL = get_from_env("PRINT_SQL", False, type_cast=str_to_bool)
SHELL_PLUS_POST_IMPORTS = [
    (
        "datetime",
        (
            "datetime",
            "timedelta",
        ),
    ),
    ("django.utils.timezone", ("now",)),
    ("infi.clickhouse_orm.utils", ("import_submodules",)),
    ("clairview.models.filters", ("Filter",)),
    ("clairview.models.property", ("Property",)),
    ("clairview.client", ("sync_execute",)),
    ("clairview.torql", ("ast")),
    ("clairview.torql.parser", ("parse_select", "parse_expr")),
    ("clairview.torql.query", ("execute_torql_query")),
]
