from typing import TypeVar

from clairview.torql import ast
from clairview.torql.errors import QueryError
from clairview.torql.visitor import CloningVisitor
from clairview.models.insight_variable import InsightVariable
from clairview.models.team.team import Team
from clairview.schema import TorQLVariable

T = TypeVar("T", bound=ast.Expr)


def replace_variables(node: T, variables: list[TorQLVariable], team: Team) -> T:
    return ReplaceVariables(variables, team).visit(node)


class ReplaceVariables(CloningVisitor):
    insight_variables: list[InsightVariable]

    def __init__(self, variables: list[TorQLVariable], team: Team):
        super().__init__()

        insight_vars = InsightVariable.objects.filter(team_id=team.pk, id__in=[v.variableId for v in variables]).all()

        self.insight_variables = list(insight_vars)
        self.variables = variables
        self.team = team

    def visit_placeholder(self, node):
        if node.chain[0] == "variables":
            variable_code_name = node.chain[1]
            if not self.variables:
                raise QueryError(f"Variable {variable_code_name} is missing from query")

            matching_variables = [variable for variable in self.variables if variable.code_name == variable_code_name]
            if not matching_variables:
                raise QueryError(f"Variable {variable_code_name} is missing from query")

            matching_variable = matching_variables[0]

            matching_insight_variable = [
                variable for variable in self.insight_variables if variable.code_name == variable_code_name
            ]
            if not matching_insight_variable:
                raise QueryError(f"Variable {variable_code_name} does not exist")

            value = matching_variable.value or matching_insight_variable[0].default_value

            return ast.Constant(value=value)

        return super().visit_placeholder(node)