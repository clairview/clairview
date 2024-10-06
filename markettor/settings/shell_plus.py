from markettor.settings.utils import get_from_env, str_to_bool

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
    ("markettor.models.filters", ("Filter",)),
    ("markettor.models.property", ("Property",)),
    ("markettor.client", ("sync_execute",)),
    ("markettor.hogql", ("ast")),
    ("markettor.hogql.parser", ("parse_select", "parse_expr")),
    ("markettor.hogql.query", ("execute_hogql_query")),
]
