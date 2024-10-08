from typing import Union, Optional

from clairview.torql import ast
from clairview.torql.context import TorQLContext
from clairview.torql.modifiers import create_default_modifiers_for_team
from clairview.torql.parser import parse_select, parse_expr
from clairview.torql.printer import prepare_ast_for_printing, print_ast
from clairview.torql.visitor import clone_expr, CloningVisitor
from clairview.models import PropertyDefinition
from clairview.schema import PersonsOnEventsMode, PersonsArgMaxVersion
from clairview.test.base import ClickhouseTestMixin, APIBaseTest


def _expr(s: Union[str, ast.Expr, None], placeholders: Optional[dict[str, ast.Expr]] = None) -> Union[ast.Expr, None]:
    if s is None:
        return None
    if isinstance(s, str):
        expr = parse_expr(s, placeholders=placeholders)
    else:
        expr = s
    return clone_expr(expr, clear_types=True, clear_locations=True)


def _select(
    s: str,
    placeholders: Optional[dict[str, ast.Expr]] = None,
) -> ast.SelectQuery | ast.SelectUnionQuery:
    parsed = parse_select(s, placeholders=placeholders)
    return parsed


class RemoveHiddenAliases(CloningVisitor):
    def visit_alias(self, node):
        if node.hidden:
            return self.visit(node.expr)
        return super().visit_alias(node)


class TestPersonWhereClauseExtractor(ClickhouseTestMixin, APIBaseTest):
    def prep_context(self):
        team = self.team
        modifiers = create_default_modifiers_for_team(team)
        modifiers.optimizeJoinedFilters = True
        modifiers.personsOnEventsMode = PersonsOnEventsMode.DISABLED
        modifiers.personsArgMaxVersion = PersonsArgMaxVersion.V1
        return TorQLContext(
            team_id=team.pk,
            team=team,
            enable_select_queries=True,
            modifiers=modifiers,
        )

    def get_clause(self, query: str):
        context = self.prep_context()
        select = _select(query)
        new_select = prepare_ast_for_printing(select, context, "clickhouse")

        assert isinstance(new_select, ast.SelectQuery)
        assert isinstance(new_select.select_from, ast.JoinExpr)
        assert isinstance(new_select.select_from.next_join, ast.JoinExpr)
        assert isinstance(new_select.select_from.next_join.next_join, ast.JoinExpr)
        assert isinstance(new_select.select_from.next_join.next_join.table, ast.SelectQuery)

        assert new_select.select_from.next_join.alias == "events__pdi"
        assert new_select.select_from.next_join.next_join.alias == "events__pdi__person"

        where = new_select.select_from.next_join.next_join.table.where
        if where is None:
            return None

        where = RemoveHiddenAliases().visit(where)
        assert isinstance(where, ast.Expr)
        return clone_expr(where, clear_types=True, clear_locations=True)

    def print_query(self, query: str):
        context = self.prep_context()
        return print_ast(node=_select(query), context=context, dialect="clickhouse", pretty=False)

    def test_person_properties(self):
        actual = self.get_clause("SELECT * FROM events WHERE person.properties.email = 'jimmy@clairview.com'")
        expected = _expr("properties.email = 'jimmy@clairview.com'")
        assert actual == expected

    def test_person_properties_andor_1(self):
        actual = self.get_clause("SELECT * FROM events WHERE person.properties.email = 'jimmy@clairview.com' or false")
        expected = _expr("properties.email = 'jimmy@clairview.com'")
        assert actual == expected

    def test_person_properties_andor_2(self):
        actual = self.get_clause("SELECT * FROM events WHERE person.properties.email = 'jimmy@clairview.com' and false")
        assert actual is None

    def test_person_properties_andor_3(self):
        actual = self.get_clause(
            "SELECT * FROM events WHERE person.properties.email = 'jimmy@clairview.com' and person.properties.email = 'timmy@clairview.com'"
        )
        expected = _expr("properties.email = 'jimmy@clairview.com' and properties.email = 'timmy@clairview.com'")
        assert actual == expected

    def test_person_properties_andor_4(self):
        actual = self.get_clause(
            "SELECT * FROM events WHERE person.properties.email = 'jimmy@clairview.com' or person.properties.email = 'timmy@clairview.com'"
        )
        expected = _expr("properties.email = 'jimmy@clairview.com' or properties.email = 'timmy@clairview.com'")
        assert actual == expected

    def test_person_properties_andor_5(self):
        actual = self.get_clause(
            "SELECT * FROM events WHERE person.properties.email = 'jimmy@clairview.com' or (1 and person.properties.email = 'timmy@clairview.com')"
        )
        expected = _expr("properties.email = 'jimmy@clairview.com' or properties.email = 'timmy@clairview.com'")
        assert actual == expected

    def test_person_properties_andor_6(self):
        actual = self.get_clause(
            "SELECT * FROM events WHERE person.properties.email = 'jimmy@clairview.com' or (0 or person.properties.email = 'timmy@clairview.com')"
        )
        expected = _expr("properties.email = 'jimmy@clairview.com' or properties.email = 'timmy@clairview.com'")
        assert actual == expected

    def test_person_properties_andor_7(self):
        actual = self.get_clause(
            "SELECT * FROM events WHERE person.properties.email = 'jimmy@clairview.com' or (1 or person.properties.email = 'timmy@clairview.com')"
        )
        assert actual is None

    def test_person_properties_andor_8(self):
        actual = self.get_clause(
            "SELECT * FROM events WHERE event == '$pageview' and person.properties.email = 'jimmy@clairview.com'"
        )
        expected = _expr("properties.email = 'jimmy@clairview.com'")
        assert actual == expected

    def test_person_properties_andor_9(self):
        actual = self.get_clause(
            "SELECT * FROM events WHERE event == '$pageview' or person.properties.email = 'jimmy@clairview.com'"
        )
        assert actual is None

    def test_person_properties_andor_10(self):
        actual = self.get_clause(
            "SELECT * FROM events WHERE properties.email = 'bla@clairview.com' or person.properties.email = 'jimmy@clairview.com'"
        )
        assert actual is None

    def test_person_properties_andor_11(self):
        actual = self.get_clause(
            "SELECT * FROM events WHERE properties.email = 'bla@clairview.com' and person.properties.email = 'jimmy@clairview.com'"
        )
        expected = _expr("properties.email = 'jimmy@clairview.com'")
        assert actual == expected

    def test_person_properties_function_calls(self):
        actual = self.get_clause(
            "SELECT * FROM events WHERE properties.email = 'bla@clairview.com' and toString(person.properties.email) = 'jimmy@clairview.com'"
        )
        expected = _expr("toString(properties.email) = 'jimmy@clairview.com'")
        assert actual == expected

    def test_person_properties_function_call_args(self):
        actual = self.get_clause(
            "SELECT * FROM events WHERE properties.email = 'bla@clairview.com' and substring(person.properties.email, 10) = 'jimmy@clairview.com'"
        )
        expected = _expr("substring(properties.email, 10) = 'jimmy@clairview.com'")
        assert actual == expected

    def test_person_properties_function_call_args_complex(self):
        actual = self.get_clause(
            "SELECT * FROM events WHERE properties.email = 'bla@clairview.com' and substring(person.properties.email, event = 'bla') = 'jimmy@clairview.com'"
        )
        assert actual is None

    def test_boolean(self):
        PropertyDefinition.objects.get_or_create(
            team=self.team,
            name="person_boolean",
            defaults={"property_type": "Boolean"},
            type=PropertyDefinition.Type.PERSON,
        )
        actual = self.print_query("SELECT * FROM events WHERE person.properties.person_boolean = false")
        assert (
            f"FROM person WHERE and(equals(person.team_id, {self.team.id}), ifNull(equals(transform(replaceRegexpAll(nullIf(nullIf(JSONExtractRaw(person.properties"
            in actual
        )
