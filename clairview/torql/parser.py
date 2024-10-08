from typing import Literal, Optional, cast
from collections.abc import Callable

from antlr4 import CommonTokenStream, InputStream, ParseTreeVisitor, ParserRuleContext
from antlr4.error.ErrorListener import ErrorListener
from prometheus_client import Histogram

from clairview.torql import ast
from clairview.torql.base import AST
from clairview.torql.constants import RESERVED_KEYWORDS
from clairview.torql.errors import BaseTorQLError, NotImplementedError, SyntaxError
from clairview.torql.grammar.TorQLLexer import TorQLLexer
from clairview.torql.grammar.TorQLParser import TorQLParser
from clairview.torql.parse_string import parse_string_literal_text, parse_string_literal_ctx, parse_string_text_ctx
from clairview.torql.placeholders import replace_placeholders
from clairview.torql.timings import TorQLTimings
from torql_parser import (
    parse_expr as _parse_expr_cpp,
    parse_order_expr as _parse_order_expr_cpp,
    parse_select as _parse_select_cpp,
    parse_full_template_string as _parse_full_template_string_cpp,
    parse_program as _parse_program_cpp,
)


def safe_lambda(f):
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            if str(e) == "Empty Stack":  # Antlr throws `Exception("Empty Stack")` ¯\_(ツ)_/¯
                raise SyntaxError("Unmatched curly bracket") from e
            raise

    return wrapped


RULE_TO_PARSE_FUNCTION: dict[
    Literal["python", "cpp"], dict[Literal["expr", "order_expr", "select", "full_template_string", "program"], Callable]
] = {
    "python": {
        "expr": safe_lambda(
            lambda string, start: TorQLParseTreeConverter(start=start).visit(get_parser(string).expr())
        ),
        "order_expr": safe_lambda(lambda string: TorQLParseTreeConverter().visit(get_parser(string).orderExpr())),
        "select": safe_lambda(lambda string: TorQLParseTreeConverter().visit(get_parser(string).select())),
        "full_template_string": safe_lambda(
            lambda string: TorQLParseTreeConverter().visit(get_parser(string).fullTemplateString())
        ),
        "program": safe_lambda(lambda string: TorQLParseTreeConverter().visit(get_parser(string).program())),
    },
    "cpp": {
        "expr": lambda string, start: _parse_expr_cpp(string, is_internal=start is None),
        "order_expr": lambda string: _parse_order_expr_cpp(string),
        "select": lambda string: _parse_select_cpp(string),
        "full_template_string": lambda string: _parse_full_template_string_cpp(string),
        "program": lambda string: _parse_program_cpp(string),
    },
}

RULE_TO_HISTOGRAM: dict[Literal["expr", "order_expr", "select", "full_template_string"], Histogram] = {
    cast(Literal["expr", "order_expr", "select", "full_template_string"], rule): Histogram(
        f"parse_{rule}_seconds",
        f"Time to parse {rule} expression",
        labelnames=["backend"],
    )
    for rule in ("expr", "order_expr", "select", "full_template_string")
}


def parse_string_template(
    string: str,
    placeholders: Optional[dict[str, ast.Expr]] = None,
    timings: Optional[TorQLTimings] = None,
    *,
    backend: Literal["python", "cpp"] = "cpp",
) -> ast.Call:
    """Parse a full template string without start/end quotes"""
    if timings is None:
        timings = TorQLTimings()
    with timings.measure(f"parse_full_template_string_{backend}"):
        with RULE_TO_HISTOGRAM["full_template_string"].labels(backend=backend).time():
            node = RULE_TO_PARSE_FUNCTION[backend]["full_template_string"]("F'" + string)
        if placeholders:
            with timings.measure("replace_placeholders"):
                node = replace_placeholders(node, placeholders)
    return node


def parse_expr(
    expr: str,
    placeholders: Optional[dict[str, ast.Expr]] = None,
    start: Optional[int] = 0,
    timings: Optional[TorQLTimings] = None,
    *,
    backend: Literal["python", "cpp"] = "cpp",
) -> ast.Expr:
    if expr == "":
        raise SyntaxError("Empty query")
    if timings is None:
        timings = TorQLTimings()
    with timings.measure(f"parse_expr_{backend}"):
        with RULE_TO_HISTOGRAM["expr"].labels(backend=backend).time():
            node = RULE_TO_PARSE_FUNCTION[backend]["expr"](expr, start)
        if placeholders:
            with timings.measure("replace_placeholders"):
                node = replace_placeholders(node, placeholders)
    return node


def parse_order_expr(
    order_expr: str,
    placeholders: Optional[dict[str, ast.Expr]] = None,
    timings: Optional[TorQLTimings] = None,
    *,
    backend: Literal["python", "cpp"] = "cpp",
) -> ast.OrderExpr:
    if timings is None:
        timings = TorQLTimings()
    with timings.measure(f"parse_order_expr_{backend}"):
        with RULE_TO_HISTOGRAM["order_expr"].labels(backend=backend).time():
            node = RULE_TO_PARSE_FUNCTION[backend]["order_expr"](order_expr)
        if placeholders:
            with timings.measure("replace_placeholders"):
                node = replace_placeholders(node, placeholders)
    return node


def parse_select(
    statement: str,
    placeholders: Optional[dict[str, ast.Expr]] = None,
    timings: Optional[TorQLTimings] = None,
    *,
    backend: Literal["python", "cpp"] = "cpp",
) -> ast.SelectQuery | ast.SelectUnionQuery:
    if timings is None:
        timings = TorQLTimings()
    with timings.measure(f"parse_select_{backend}"):
        with RULE_TO_HISTOGRAM["select"].labels(backend=backend).time():
            node = RULE_TO_PARSE_FUNCTION[backend]["select"](statement)
        if placeholders:
            with timings.measure("replace_placeholders"):
                node = replace_placeholders(node, placeholders)
    return node


def parse_program(
    source: str,
    timings: Optional[TorQLTimings] = None,
    *,
    backend: Literal["python", "cpp"] = "cpp",
) -> ast.Program:
    if timings is None:
        timings = TorQLTimings()
    with timings.measure(f"parse_expr_{backend}"):
        with RULE_TO_HISTOGRAM["expr"].labels(backend=backend).time():
            node = RULE_TO_PARSE_FUNCTION[backend]["program"](source)
    return node


def get_parser(query: str) -> TorQLParser:
    input_stream = InputStream(data=query)
    lexer = TorQLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = TorQLParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(TorQLErrorListener(query))
    return parser


class TorQLErrorListener(ErrorListener):
    query: str

    def __init__(self, query: str = ""):
        super().__init__()
        self.query = query

    def get_position(self, line, column):
        lines = self.query.split("\n")
        try:
            position = sum(len(lines[i]) + 1 for i in range(line - 1)) + column
        except IndexError:
            return -1
        if position > len(self.query):
            return -1
        return position

    def syntaxError(self, recognizer, offendingType, line, column, msg, e):
        start = max(self.get_position(line, column), 0)
        raise SyntaxError(msg, start=start, end=len(self.query))


class TorQLParseTreeConverter(ParseTreeVisitor):
    def __init__(self, start: Optional[int] = 0):
        super().__init__()
        self.start = start

    def visit(self, ctx: ParserRuleContext):
        start = ctx.start.start if ctx.start else None
        end = ctx.stop.stop + 1 if ctx.stop else None
        try:
            node = super().visit(ctx)
            if isinstance(node, AST) and self.start is not None:
                node.start = start
                node.end = end
            return node
        except BaseTorQLError as e:
            if start is not None and end is not None and e.start is None or e.end is None:
                e.start = start
                e.end = end
            raise

    def visitProgram(self, ctx: TorQLParser.ProgramContext):
        declarations: list[ast.Declaration] = []
        for declaration in ctx.declaration():
            if not declaration.statement() or not declaration.statement().emptyStmt():
                statement = self.visit(declaration)
                declarations.append(cast(ast.Declaration, statement))
        return ast.Program(declarations=declarations)

    def visitDeclaration(self, ctx: TorQLParser.DeclarationContext):
        return self.visitChildren(ctx)

    def visitExpression(self, ctx: TorQLParser.ExpressionContext):
        return self.visitChildren(ctx)

    def visitVarDecl(self, ctx: TorQLParser.VarDeclContext):
        return ast.VariableDeclaration(
            name=ctx.identifier().getText(),
            expr=self.visit(ctx.expression()) if ctx.expression() else None,
        )

    def visitVarAssignment(self, ctx: TorQLParser.VarAssignmentContext):
        return ast.VariableAssignment(
            left=self.visit(ctx.expression(0)),
            right=self.visit(ctx.expression(1)),
        )

    def visitStatement(self, ctx: TorQLParser.StatementContext):
        return self.visitChildren(ctx)

    def visitExprStmt(self, ctx: TorQLParser.ExprStmtContext):
        return ast.ExprStatement(expr=self.visit(ctx.expression()))

    def visitReturnStmt(self, ctx: TorQLParser.ReturnStmtContext):
        return ast.ReturnStatement(expr=self.visit(ctx.expression()) if ctx.expression() else None)

    def visitThrowStmt(self, ctx: TorQLParser.ThrowStmtContext):
        return ast.ThrowStatement(expr=self.visit(ctx.expression()) if ctx.expression() else None)

    def visitCatchBlock(self, ctx: TorQLParser.CatchBlockContext):
        return (
            self.visit(ctx.catchVar) if ctx.catchVar else None,
            self.visit(ctx.catchType) if ctx.catchType else None,
            self.visit(ctx.catchStmt),
        )

    def visitTryCatchStmt(self, ctx: TorQLParser.TryCatchStmtContext):
        return ast.TryCatchStatement(
            try_stmt=self.visit(ctx.tryStmt),
            catches=[self.visit(catch) for catch in ctx.catchBlock()],
            finally_stmt=self.visit(ctx.finallyStmt) if ctx.finallyStmt else None,
        )

    def visitIfStmt(self, ctx: TorQLParser.IfStmtContext):
        return ast.IfStatement(
            expr=self.visit(ctx.expression()),
            then=self.visit(ctx.statement(0)),
            else_=self.visit(ctx.statement(1)) if ctx.statement(1) else None,
        )

    def visitWhileStmt(self, ctx: TorQLParser.WhileStmtContext):
        return ast.WhileStatement(
            expr=self.visit(ctx.expression()),
            body=self.visit(ctx.statement()) if ctx.statement() else None,
        )

    def visitForInStmt(self, ctx: TorQLParser.ForInStmtContext):
        first_identifier = ctx.identifier(0).getText()
        second_identifier = ctx.identifier(1).getText() if ctx.identifier(1) else None
        return ast.ForInStatement(
            valueVar=second_identifier if second_identifier is not None else first_identifier,
            keyVar=first_identifier if second_identifier is not None else None,
            expr=self.visit(ctx.expression()),
            body=self.visit(ctx.statement()),
        )

    def visitForStmt(self, ctx: TorQLParser.ForStmtContext):
        initializer = ctx.initializerVarDeclr or ctx.initializerVarAssignment or ctx.initializerExpression
        increment = ctx.incrementVarDeclr or ctx.incrementVarAssignment or ctx.incrementExpression

        return ast.ForStatement(
            initializer=self.visit(initializer) if initializer else None,
            condition=self.visit(ctx.condition) if ctx.condition else None,
            increment=self.visit(increment) if increment else None,
            body=self.visit(ctx.statement()),
        )

    def visitFuncStmt(self, ctx: TorQLParser.FuncStmtContext):
        return ast.Function(
            name=ctx.identifier().getText(),
            params=self.visit(ctx.identifierList()) if ctx.identifierList() else [],
            body=self.visit(ctx.block()),
        )

    def visitKvPairList(self, ctx: TorQLParser.KvPairListContext):
        return [self.visit(kv) for kv in ctx.kvPair()]

    def visitKvPair(self, ctx: TorQLParser.KvPairContext):
        k, v = ctx.expression()
        return (self.visit(k), self.visit(v))

    def visitIdentifierList(self, ctx: TorQLParser.IdentifierListContext):
        return [ident.getText() for ident in ctx.identifier()]

    def visitEmptyStmt(self, ctx: TorQLParser.EmptyStmtContext):
        return ast.ExprStatement(expr=None)

    def visitBlock(self, ctx: TorQLParser.BlockContext):
        declarations: list[ast.Declaration] = []
        for declaration in ctx.declaration():
            if not declaration.statement() or not declaration.statement().emptyStmt():
                statement = self.visit(declaration)
                declarations.append(cast(ast.Declaration, statement))
        return ast.Block(declarations=declarations)

    ##### TorQL rules

    def visitSelect(self, ctx: TorQLParser.SelectContext):
        return self.visit(ctx.selectUnionStmt() or ctx.selectStmt() or ctx.torqlxTagElement())

    def visitSelectUnionStmt(self, ctx: TorQLParser.SelectUnionStmtContext):
        select_queries: list[ast.SelectQuery | ast.SelectUnionQuery | ast.Placeholder] = [
            self.visit(select) for select in ctx.selectStmtWithParens()
        ]
        flattened_queries: list[ast.SelectQuery] = []
        for query in select_queries:
            if isinstance(query, ast.SelectQuery):
                flattened_queries.append(query)
            elif isinstance(query, ast.SelectUnionQuery):
                flattened_queries.extend(query.select_queries)
            elif isinstance(query, ast.Placeholder):
                flattened_queries.append(query)  # type: ignore
            else:
                raise Exception(f"Unexpected query node type {type(query).__name__}")
        if len(flattened_queries) == 1:
            return flattened_queries[0]
        return ast.SelectUnionQuery(select_queries=flattened_queries)

    def visitSelectStmtWithParens(self, ctx: TorQLParser.SelectStmtWithParensContext):
        return self.visit(ctx.selectStmt() or ctx.selectUnionStmt() or ctx.placeholder())

    def visitSelectStmt(self, ctx: TorQLParser.SelectStmtContext):
        select_query = ast.SelectQuery(
            ctes=self.visit(ctx.withClause()) if ctx.withClause() else None,
            select=self.visit(ctx.columnExprList()) if ctx.columnExprList() else [],
            distinct=True if ctx.DISTINCT() else None,
            select_from=self.visit(ctx.fromClause()) if ctx.fromClause() else None,
            where=self.visit(ctx.whereClause()) if ctx.whereClause() else None,
            prewhere=self.visit(ctx.prewhereClause()) if ctx.prewhereClause() else None,
            having=self.visit(ctx.havingClause()) if ctx.havingClause() else None,
            group_by=self.visit(ctx.groupByClause()) if ctx.groupByClause() else None,
            order_by=self.visit(ctx.orderByClause()) if ctx.orderByClause() else None,
        )

        if window_clause := ctx.windowClause():
            select_query.window_exprs = {}
            for index, window_expr in enumerate(window_clause.windowExpr()):
                name = self.visit(window_clause.identifier()[index])
                select_query.window_exprs[name] = self.visit(window_expr)

        if limit_and_offset_clause := ctx.limitAndOffsetClause():
            select_query.limit = self.visit(limit_and_offset_clause.columnExpr(0))
            if offset := limit_and_offset_clause.columnExpr(1):
                select_query.offset = self.visit(offset)
            if limit_by_exprs := limit_and_offset_clause.columnExprList():
                select_query.limit_by = self.visit(limit_by_exprs)
            if limit_and_offset_clause.WITH() and limit_and_offset_clause.TIES():
                select_query.limit_with_ties = True
        elif offset_only_clause := ctx.offsetOnlyClause():
            select_query.offset = self.visit(offset_only_clause.columnExpr())

        if ctx.arrayJoinClause():
            array_join_clause = ctx.arrayJoinClause()
            if select_query.select_from is None:
                raise SyntaxError("Using ARRAY JOIN without a FROM clause is not permitted")
            if array_join_clause.LEFT():
                select_query.array_join_op = "LEFT ARRAY JOIN"
            elif array_join_clause.INNER():
                select_query.array_join_op = "INNER ARRAY JOIN"
            else:
                select_query.array_join_op = "ARRAY JOIN"
            select_query.array_join_list = self.visit(array_join_clause.columnExprList())
            for expr in select_query.array_join_list:
                if not isinstance(expr, ast.Alias):
                    raise SyntaxError(
                        "ARRAY JOIN arrays must have an alias",
                        start=expr.start,
                        end=expr.end,
                    )

        if ctx.topClause():
            raise NotImplementedError(f"Unsupported: SelectStmt.topClause()")
        if ctx.settingsClause():
            raise NotImplementedError(f"Unsupported: SelectStmt.settingsClause()")

        return select_query

    def visitWithClause(self, ctx: TorQLParser.WithClauseContext):
        return self.visit(ctx.withExprList())

    def visitTopClause(self, ctx: TorQLParser.TopClauseContext):
        raise NotImplementedError(f"Unsupported node: TopClause")

    def visitFromClause(self, ctx: TorQLParser.FromClauseContext):
        return self.visit(ctx.joinExpr())

    def visitArrayJoinClause(self, ctx: TorQLParser.ArrayJoinClauseContext):
        raise NotImplementedError(f"Unsupported node: ArrayJoinClause")

    def visitWindowClause(self, ctx: TorQLParser.WindowClauseContext):
        raise NotImplementedError(f"Unsupported node: WindowClause")

    def visitPrewhereClause(self, ctx: TorQLParser.PrewhereClauseContext):
        return self.visit(ctx.columnExpr())

    def visitWhereClause(self, ctx: TorQLParser.WhereClauseContext):
        return self.visit(ctx.columnExpr())

    def visitGroupByClause(self, ctx: TorQLParser.GroupByClauseContext):
        return self.visit(ctx.columnExprList())

    def visitHavingClause(self, ctx: TorQLParser.HavingClauseContext):
        return self.visit(ctx.columnExpr())

    def visitOrderByClause(self, ctx: TorQLParser.OrderByClauseContext):
        return self.visit(ctx.orderExprList())

    def visitProjectionOrderByClause(self, ctx: TorQLParser.ProjectionOrderByClauseContext):
        raise NotImplementedError(f"Unsupported node: ProjectionOrderByClause")

    def visitLimitAndOffsetClauseClause(self, ctx: TorQLParser.LimitAndOffsetClauseContext):
        raise Exception(f"Parsed as part of SelectStmt, can't parse directly")

    def visitSettingsClause(self, ctx: TorQLParser.SettingsClauseContext):
        raise NotImplementedError(f"Unsupported node: SettingsClause")

    def visitJoinExprOp(self, ctx: TorQLParser.JoinExprOpContext):
        join1: ast.JoinExpr = self.visit(ctx.joinExpr(0))
        join2: ast.JoinExpr = self.visit(ctx.joinExpr(1))

        if ctx.joinOp():
            join2.join_type = f"{self.visit(ctx.joinOp())} JOIN"
        else:
            join2.join_type = "JOIN"
        join2.constraint = self.visit(ctx.joinConstraintClause())

        last_join = join1
        while last_join.next_join is not None:
            last_join = last_join.next_join
        last_join.next_join = join2

        return join1

    def visitJoinExprTable(self, ctx: TorQLParser.JoinExprTableContext):
        sample = None
        if ctx.sampleClause():
            sample = self.visit(ctx.sampleClause())
        table = self.visit(ctx.tableExpr())
        table_final = True if ctx.FINAL() else None
        if isinstance(table, ast.JoinExpr):
            # visitTableExprAlias returns a JoinExpr to pass the alias
            # visitTableExprFunction returns a JoinExpr to pass the args
            table.table_final = table_final
            table.sample = sample
            return table
        return ast.JoinExpr(table=table, table_final=table_final, sample=sample)

    def visitJoinExprParens(self, ctx: TorQLParser.JoinExprParensContext):
        return self.visit(ctx.joinExpr())

    def visitJoinExprCrossOp(self, ctx: TorQLParser.JoinExprCrossOpContext):
        join1: ast.JoinExpr = self.visit(ctx.joinExpr(0))
        join2: ast.JoinExpr = self.visit(ctx.joinExpr(1))
        join2.join_type = "CROSS JOIN"
        last_join = join1
        while last_join.next_join is not None:
            last_join = last_join.next_join
        last_join.next_join = join2
        return join1

    def visitJoinOpInner(self, ctx: TorQLParser.JoinOpInnerContext):
        tokens = []
        if ctx.ALL():
            tokens.append("ALL")
        if ctx.ANY():
            tokens.append("ANY")
        if ctx.ASOF():
            tokens.append("ASOF")
        tokens.append("INNER")
        return " ".join(tokens)

    def visitJoinOpLeftRight(self, ctx: TorQLParser.JoinOpLeftRightContext):
        tokens = []
        if ctx.LEFT():
            tokens.append("LEFT")
        if ctx.RIGHT():
            tokens.append("RIGHT")
        if ctx.OUTER():
            tokens.append("OUTER")
        if ctx.SEMI():
            tokens.append("SEMI")
        if ctx.ALL():
            tokens.append("ALL")
        if ctx.ANTI():
            tokens.append("ANTI")
        if ctx.ANY():
            tokens.append("ANY")
        if ctx.ASOF():
            tokens.append("ASOF")
        return " ".join(tokens)

    def visitJoinOpFull(self, ctx: TorQLParser.JoinOpFullContext):
        tokens = []
        if ctx.FULL():
            tokens.append("FULL")
        if ctx.OUTER():
            tokens.append("OUTER")
        if ctx.ALL():
            tokens.append("ALL")
        if ctx.ANY():
            tokens.append("ANY")
        return " ".join(tokens)

    def visitJoinOpCross(self, ctx: TorQLParser.JoinOpCrossContext):
        raise NotImplementedError(f"Unsupported node: JoinOpCross")

    def visitJoinConstraintClause(self, ctx: TorQLParser.JoinConstraintClauseContext):
        column_expr_list = self.visit(ctx.columnExprList())
        if len(column_expr_list) != 1:
            raise NotImplementedError(f"Unsupported: JOIN ... ON with multiple expressions")
        return ast.JoinConstraint(expr=column_expr_list[0], constraint_type="USING" if ctx.USING() else "ON")

    def visitSampleClause(self, ctx: TorQLParser.SampleClauseContext):
        ratio_expressions = ctx.ratioExpr()

        sample_ratio_expr = self.visit(ratio_expressions[0])
        offset_ratio_expr = self.visit(ratio_expressions[1]) if len(ratio_expressions) > 1 and ctx.OFFSET() else None

        return ast.SampleExpr(sample_value=sample_ratio_expr, offset_value=offset_ratio_expr)

    def visitOrderExprList(self, ctx: TorQLParser.OrderExprListContext):
        return [self.visit(expr) for expr in ctx.orderExpr()]

    def visitOrderExpr(self, ctx: TorQLParser.OrderExprContext):
        order = "DESC" if ctx.DESC() or ctx.DESCENDING() else "ASC"
        return ast.OrderExpr(expr=self.visit(ctx.columnExpr()), order=cast(Literal["ASC", "DESC"], order))

    def visitRatioExpr(self, ctx: TorQLParser.RatioExprContext):
        if ctx.placeholder():
            return self.visit(ctx.placeholder())

        number_literals = ctx.numberLiteral()

        left = number_literals[0]
        right = number_literals[1] if ctx.SLASH() and len(number_literals) > 1 else None

        return ast.RatioExpr(
            left=self.visitNumberLiteral(left),
            right=self.visitNumberLiteral(right) if right else None,
        )

    def visitSettingExprList(self, ctx: TorQLParser.SettingExprListContext):
        raise NotImplementedError(f"Unsupported node: SettingExprList")

    def visitSettingExpr(self, ctx: TorQLParser.SettingExprContext):
        raise NotImplementedError(f"Unsupported node: SettingExpr")

    def visitWindowExpr(self, ctx: TorQLParser.WindowExprContext):
        frame = ctx.winFrameClause()
        visited_frame = self.visit(frame) if frame else None
        expr = ast.WindowExpr(
            partition_by=self.visit(ctx.winPartitionByClause()) if ctx.winPartitionByClause() else None,
            order_by=self.visit(ctx.winOrderByClause()) if ctx.winOrderByClause() else None,
            frame_method="RANGE" if frame and frame.RANGE() else "ROWS" if frame and frame.ROWS() else None,
            frame_start=visited_frame[0] if isinstance(visited_frame, tuple) else visited_frame,
            frame_end=visited_frame[1] if isinstance(visited_frame, tuple) else None,
        )
        return expr

    def visitWinPartitionByClause(self, ctx: TorQLParser.WinPartitionByClauseContext):
        return self.visit(ctx.columnExprList())

    def visitWinOrderByClause(self, ctx: TorQLParser.WinOrderByClauseContext):
        return self.visit(ctx.orderExprList())

    def visitWinFrameClause(self, ctx: TorQLParser.WinFrameClauseContext):
        return self.visit(ctx.winFrameExtend())

    def visitFrameStart(self, ctx: TorQLParser.FrameStartContext):
        return self.visit(ctx.winFrameBound())

    def visitFrameBetween(self, ctx: TorQLParser.FrameBetweenContext):
        return (self.visit(ctx.winFrameBound(0)), self.visit(ctx.winFrameBound(1)))

    def visitWinFrameBound(self, ctx: TorQLParser.WinFrameBoundContext):
        if ctx.PRECEDING():
            return ast.WindowFrameExpr(
                frame_type="PRECEDING",
                frame_value=self.visit(ctx.numberLiteral()).value if ctx.numberLiteral() else None,
            )
        if ctx.FOLLOWING():
            return ast.WindowFrameExpr(
                frame_type="FOLLOWING",
                frame_value=self.visit(ctx.numberLiteral()).value if ctx.numberLiteral() else None,
            )
        return ast.WindowFrameExpr(frame_type="CURRENT ROW")

    def visitExpr(self, ctx: TorQLParser.ExprContext):
        return self.visit(ctx.columnExpr())

    def visitColumnTypeExprSimple(self, ctx: TorQLParser.ColumnTypeExprSimpleContext):
        raise NotImplementedError(f"Unsupported node: ColumnTypeExprSimple")

    def visitColumnTypeExprNested(self, ctx: TorQLParser.ColumnTypeExprNestedContext):
        raise NotImplementedError(f"Unsupported node: ColumnTypeExprNested")

    def visitColumnTypeExprEnum(self, ctx: TorQLParser.ColumnTypeExprEnumContext):
        raise NotImplementedError(f"Unsupported node: ColumnTypeExprEnum")

    def visitColumnTypeExprComplex(self, ctx: TorQLParser.ColumnTypeExprComplexContext):
        raise NotImplementedError(f"Unsupported node: ColumnTypeExprComplex")

    def visitColumnTypeExprParam(self, ctx: TorQLParser.ColumnTypeExprParamContext):
        raise NotImplementedError(f"Unsupported node: ColumnTypeExprParam")

    def visitColumnExprList(self, ctx: TorQLParser.ColumnExprListContext):
        return [self.visit(c) for c in ctx.columnExpr()]

    def visitColumnExprTernaryOp(self, ctx: TorQLParser.ColumnExprTernaryOpContext):
        return ast.Call(
            name="if",
            args=[
                self.visit(ctx.columnExpr(0)),
                self.visit(ctx.columnExpr(1)),
                self.visit(ctx.columnExpr(2)),
            ],
        )

    def visitColumnExprAlias(self, ctx: TorQLParser.ColumnExprAliasContext):
        alias: str
        if ctx.identifier():
            alias = self.visit(ctx.identifier())
        elif ctx.STRING_LITERAL():
            alias = parse_string_literal_ctx(ctx.STRING_LITERAL())
        else:
            raise SyntaxError(f"Must specify an alias")
        expr = self.visit(ctx.columnExpr())

        if alias.lower() in RESERVED_KEYWORDS:
            raise SyntaxError(f'"{alias}" cannot be an alias or identifier, as it\'s a reserved keyword')

        return ast.Alias(expr=expr, alias=alias)

    def visitColumnExprNegate(self, ctx: TorQLParser.ColumnExprNegateContext):
        return ast.ArithmeticOperation(
            op=ast.ArithmeticOperationOp.Sub,
            left=ast.Constant(value=0),
            right=self.visit(ctx.columnExpr()),
        )

    def visitColumnExprDict(self, ctx: TorQLParser.ColumnExprDictContext):
        return ast.Dict(items=self.visit(ctx.kvPairList()) if ctx.kvPairList() else [])

    def visitColumnExprSubquery(self, ctx: TorQLParser.ColumnExprSubqueryContext):
        return self.visit(ctx.selectUnionStmt())

    def visitColumnExprLiteral(self, ctx: TorQLParser.ColumnExprLiteralContext):
        return self.visitChildren(ctx)

    def visitColumnExprArray(self, ctx: TorQLParser.ColumnExprArrayContext):
        return ast.Array(exprs=self.visit(ctx.columnExprList()) if ctx.columnExprList() else [])

    def visitColumnExprSubstring(self, ctx: TorQLParser.ColumnExprSubstringContext):
        raise NotImplementedError(f"Unsupported node: ColumnExprSubstring")

    def visitColumnExprCast(self, ctx: TorQLParser.ColumnExprCastContext):
        raise NotImplementedError(f"Unsupported node: ColumnExprCast")

    def visitColumnExprPrecedence1(self, ctx: TorQLParser.ColumnExprPrecedence1Context):
        if ctx.SLASH():
            op = ast.ArithmeticOperationOp.Div
        elif ctx.ASTERISK():
            op = ast.ArithmeticOperationOp.Mult
        elif ctx.PERCENT():
            op = ast.ArithmeticOperationOp.Mod
        else:
            raise NotImplementedError(f"Unsupported ColumnExprPrecedence1: {ctx.operator.text}")
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        return ast.ArithmeticOperation(left=left, right=right, op=op)

    def visitColumnExprPrecedence2(self, ctx: TorQLParser.ColumnExprPrecedence2Context):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)

        if ctx.PLUS():
            return ast.ArithmeticOperation(left=left, right=right, op=ast.ArithmeticOperationOp.Add)
        elif ctx.DASH():
            return ast.ArithmeticOperation(left=left, right=right, op=ast.ArithmeticOperationOp.Sub)
        elif ctx.CONCAT():
            args = []
            if isinstance(left, ast.Call) and left.name == "concat":
                args.extend(left.args)
            else:
                args.append(left)

            if isinstance(right, ast.Call) and right.name == "concat":
                args.extend(right.args)
            else:
                args.append(right)

            return ast.Call(name="concat", args=args)
        else:
            raise NotImplementedError(f"Unsupported ColumnExprPrecedence2: {ctx.operator.text}")

    def visitColumnExprPrecedence3(self, ctx: TorQLParser.ColumnExprPrecedence3Context):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)

        if ctx.EQ_SINGLE() or ctx.EQ_DOUBLE():
            op = ast.CompareOperationOp.Eq
        elif ctx.NOT_EQ():
            op = ast.CompareOperationOp.NotEq
        elif ctx.LT():
            op = ast.CompareOperationOp.Lt
        elif ctx.LT_EQ():
            op = ast.CompareOperationOp.LtEq
        elif ctx.GT():
            op = ast.CompareOperationOp.Gt
        elif ctx.GT_EQ():
            op = ast.CompareOperationOp.GtEq
        elif ctx.LIKE():
            if ctx.NOT():
                op = ast.CompareOperationOp.NotLike
            else:
                op = ast.CompareOperationOp.Like
        elif ctx.ILIKE():
            if ctx.NOT():
                op = ast.CompareOperationOp.NotILike
            else:
                op = ast.CompareOperationOp.ILike
        elif ctx.REGEX_SINGLE() or ctx.REGEX_DOUBLE():
            op = ast.CompareOperationOp.Regex
        elif ctx.NOT_REGEX():
            op = ast.CompareOperationOp.NotRegex
        elif ctx.IREGEX_SINGLE() or ctx.IREGEX_DOUBLE():
            op = ast.CompareOperationOp.IRegex
        elif ctx.NOT_IREGEX():
            op = ast.CompareOperationOp.NotIRegex
        elif ctx.IN():
            if ctx.COHORT():
                if ctx.NOT():
                    op = ast.CompareOperationOp.NotInCohort
                else:
                    op = ast.CompareOperationOp.InCohort
            else:
                if ctx.NOT():
                    op = ast.CompareOperationOp.NotIn
                else:
                    op = ast.CompareOperationOp.In
        else:
            raise NotImplementedError(f"Unsupported ColumnExprPrecedence3: {ctx.getText()}")

        return ast.CompareOperation(left=left, right=right, op=op)

    def visitColumnExprInterval(self, ctx: TorQLParser.ColumnExprIntervalContext):
        if ctx.interval().SECOND():
            name = "toIntervalSecond"
        elif ctx.interval().MINUTE():
            name = "toIntervalMinute"
        elif ctx.interval().HOUR():
            name = "toIntervalHour"
        elif ctx.interval().DAY():
            name = "toIntervalDay"
        elif ctx.interval().WEEK():
            name = "toIntervalWeek"
        elif ctx.interval().MONTH():
            name = "toIntervalMonth"
        elif ctx.interval().QUARTER():
            name = "toIntervalQuarter"
        elif ctx.interval().YEAR():
            name = "toIntervalYear"
        else:
            raise NotImplementedError(f"Unsupported interval type: {ctx.interval().getText()}")

        return ast.Call(name=name, args=[self.visit(ctx.columnExpr())])

    def visitColumnExprIsNull(self, ctx: TorQLParser.ColumnExprIsNullContext):
        return ast.CompareOperation(
            left=self.visit(ctx.columnExpr()),
            right=ast.Constant(value=None),
            op=ast.CompareOperationOp.NotEq if ctx.NOT() else ast.CompareOperationOp.Eq,
        )

    def visitColumnExprTrim(self, ctx: TorQLParser.ColumnExprTrimContext):
        args = [self.visit(ctx.columnExpr()), self.visit(ctx.string())]
        if ctx.LEADING():
            return ast.Call(name="trimLeft", args=args)
        if ctx.TRAILING():
            return ast.Call(name="trimRight", args=args)
        if ctx.BOTH():
            return ast.Call(name="trim", args=args)
        raise NotImplementedError(f"Unsupported modifier for ColumnExprTrim, must be LEADING, TRAILING or BOTH")

    def visitColumnExprTuple(self, ctx: TorQLParser.ColumnExprTupleContext):
        return ast.Tuple(exprs=self.visit(ctx.columnExprList()) if ctx.columnExprList() else [])

    def visitColumnExprArrayAccess(self, ctx: TorQLParser.ColumnExprArrayAccessContext):
        object: ast.Expr = self.visit(ctx.columnExpr(0))
        property: ast.Expr = self.visit(ctx.columnExpr(1))
        return ast.ArrayAccess(array=object, property=property)

    def visitColumnExprNullArrayAccess(self, ctx: TorQLParser.ColumnExprNullArrayAccessContext):
        object: ast.Expr = self.visit(ctx.columnExpr(0))
        property: ast.Expr = self.visit(ctx.columnExpr(1))
        return ast.ArrayAccess(array=object, property=property, nullish=True)

    def visitColumnExprPropertyAccess(self, ctx: TorQLParser.ColumnExprPropertyAccessContext):
        object = self.visit(ctx.columnExpr())
        property = ast.Constant(value=self.visit(ctx.identifier()))
        return ast.ArrayAccess(array=object, property=property)

    def visitColumnExprNullPropertyAccess(self, ctx: TorQLParser.ColumnExprNullPropertyAccessContext):
        object = self.visit(ctx.columnExpr())
        property = ast.Constant(value=self.visit(ctx.identifier()))
        return ast.ArrayAccess(array=object, property=property, nullish=True)

    def visitColumnExprBetween(self, ctx: TorQLParser.ColumnExprBetweenContext):
        raise NotImplementedError(f"Unsupported node: ColumnExprBetween")

    def visitColumnExprParens(self, ctx: TorQLParser.ColumnExprParensContext):
        return self.visit(ctx.columnExpr())

    def visitColumnExprTimestamp(self, ctx: TorQLParser.ColumnExprTimestampContext):
        raise NotImplementedError(f"Unsupported node: ColumnExprTimestamp")

    def visitColumnExprAnd(self, ctx: TorQLParser.ColumnExprAndContext):
        left = self.visit(ctx.columnExpr(0))
        if isinstance(left, ast.And):
            left_array = left.exprs
        else:
            left_array = [left]

        right = self.visit(ctx.columnExpr(1))
        if isinstance(right, ast.And):
            right_array = right.exprs
        else:
            right_array = [right]

        return ast.And(exprs=left_array + right_array)

    def visitColumnExprOr(self, ctx: TorQLParser.ColumnExprOrContext):
        left = self.visit(ctx.columnExpr(0))
        if isinstance(left, ast.Or):
            left_array = left.exprs
        else:
            left_array = [left]

        right = self.visit(ctx.columnExpr(1))
        if isinstance(right, ast.Or):
            right_array = right.exprs
        else:
            right_array = [right]

        return ast.Or(exprs=left_array + right_array)

    def visitColumnExprTupleAccess(self, ctx: TorQLParser.ColumnExprTupleAccessContext):
        tuple = self.visit(ctx.columnExpr())
        index = int(ctx.DECIMAL_LITERAL().getText())
        return ast.TupleAccess(tuple=tuple, index=index)

    def visitColumnExprNullTupleAccess(self, ctx: TorQLParser.ColumnExprNullTupleAccessContext):
        tuple = self.visit(ctx.columnExpr())
        index = int(ctx.DECIMAL_LITERAL().getText())
        return ast.TupleAccess(tuple=tuple, index=index, nullish=True)

    def visitColumnExprCase(self, ctx: TorQLParser.ColumnExprCaseContext):
        columns = [self.visit(column) for column in ctx.columnExpr()]
        if ctx.caseExpr:
            args = [columns[0], ast.Array(exprs=[]), ast.Array(exprs=[]), columns[-1]]
            for index, column in enumerate(columns):
                if 0 < index < len(columns) - 1:
                    args[((index - 1) % 2) + 1].exprs.append(column)
            return ast.Call(name="transform", args=args)
        elif len(columns) == 3:
            return ast.Call(name="if", args=columns)
        else:
            return ast.Call(name="multiIf", args=columns)

    def visitColumnExprDate(self, ctx: TorQLParser.ColumnExprDateContext):
        raise NotImplementedError(f"Unsupported node: ColumnExprDate")

    def visitColumnExprNot(self, ctx: TorQLParser.ColumnExprNotContext):
        return ast.Not(expr=self.visit(ctx.columnExpr()))

    def visitColumnExprWinFunctionTarget(self, ctx: TorQLParser.ColumnExprWinFunctionTargetContext):
        return ast.WindowFunction(
            name=self.visit(ctx.identifier(0)),
            exprs=self.visit(ctx.columnExprs) if ctx.columnExprs else [],
            args=self.visit(ctx.columnArgList) if ctx.columnArgList else [],
            over_identifier=self.visit(ctx.identifier(1)),
        )

    def visitColumnExprWinFunction(self, ctx: TorQLParser.ColumnExprWinFunctionContext):
        return ast.WindowFunction(
            name=self.visit(ctx.identifier()),
            exprs=self.visit(ctx.columnExprs) if ctx.columnExprs else [],
            args=self.visit(ctx.columnArgList) if ctx.columnArgList else [],
            over_expr=self.visit(ctx.windowExpr()) if ctx.windowExpr() else None,
        )

    def visitColumnExprIdentifier(self, ctx: TorQLParser.ColumnExprIdentifierContext):
        return self.visit(ctx.columnIdentifier())

    def visitColumnExprFunction(self, ctx: TorQLParser.ColumnExprFunctionContext):
        name = self.visit(ctx.identifier())

        parameters: list[ast.Expr] | None = self.visit(ctx.columnExprs) if ctx.columnExprs is not None else None
        # two sets of parameters fn()(), return an empty list for the first even if no parameters
        if ctx.LPAREN(1) and parameters is None:
            parameters = []

        args: list[ast.Expr] = self.visit(ctx.columnArgList) if ctx.columnArgList is not None else []
        distinct = True if ctx.DISTINCT() else False
        return ast.Call(name=name, params=parameters, args=args, distinct=distinct)

    def visitColumnExprAsterisk(self, ctx: TorQLParser.ColumnExprAsteriskContext):
        if ctx.tableIdentifier():
            table = self.visit(ctx.tableIdentifier())
            return ast.Field(chain=[*table, "*"])
        return ast.Field(chain=["*"])

    def visitColumnExprTagElement(self, ctx: TorQLParser.ColumnExprTagElementContext):
        return self.visit(ctx.torqlxTagElement())

    def visitColumnLambdaExpr(self, ctx: TorQLParser.ColumnLambdaExprContext):
        return ast.Lambda(
            args=[self.visit(identifier) for identifier in ctx.identifier()],
            expr=self.visit(ctx.columnExpr() or ctx.block()),
        )

    def visitWithExprList(self, ctx: TorQLParser.WithExprListContext):
        ctes: dict[str, ast.CTE] = {}
        for expr in ctx.withExpr():
            cte = self.visit(expr)
            ctes[cte.name] = cte
        return ctes

    def visitWithExprSubquery(self, ctx: TorQLParser.WithExprSubqueryContext):
        subquery = self.visit(ctx.selectUnionStmt())
        name = self.visit(ctx.identifier())
        return ast.CTE(name=name, expr=subquery, cte_type="subquery")

    def visitWithExprColumn(self, ctx: TorQLParser.WithExprColumnContext):
        expr = self.visit(ctx.columnExpr())
        name = self.visit(ctx.identifier())
        return ast.CTE(name=name, expr=expr, cte_type="column")

    def visitColumnIdentifier(self, ctx: TorQLParser.ColumnIdentifierContext):
        if ctx.placeholder():
            return self.visit(ctx.placeholder())

        table = self.visit(ctx.tableIdentifier()) if ctx.tableIdentifier() else []
        nested = self.visit(ctx.nestedIdentifier()) if ctx.nestedIdentifier() else []

        if len(table) == 0 and len(nested) > 0:
            text = ctx.getText().lower()
            if text == "true":
                return ast.Constant(value=True)
            if text == "false":
                return ast.Constant(value=False)
            return ast.Field(chain=nested)

        return ast.Field(chain=table + nested)

    def visitNestedIdentifier(self, ctx: TorQLParser.NestedIdentifierContext):
        return [self.visit(identifier) for identifier in ctx.identifier()]

    def visitTableExprIdentifier(self, ctx: TorQLParser.TableExprIdentifierContext):
        chain = self.visit(ctx.tableIdentifier())
        return ast.Field(chain=chain)

    def visitTableExprSubquery(self, ctx: TorQLParser.TableExprSubqueryContext):
        return self.visit(ctx.selectUnionStmt())

    def visitTableExprPlaceholder(self, ctx: TorQLParser.TableExprPlaceholderContext):
        return self.visit(ctx.placeholder())

    def visitTableExprAlias(self, ctx: TorQLParser.TableExprAliasContext):
        alias: str = self.visit(ctx.alias() or ctx.identifier())
        if alias.lower() in RESERVED_KEYWORDS:
            raise SyntaxError(f'"{alias}" cannot be an alias or identifier, as it\'s a reserved keyword')
        table = self.visit(ctx.tableExpr())
        if isinstance(table, ast.JoinExpr):
            table.alias = alias
            return table
        return ast.JoinExpr(table=table, alias=alias)

    def visitTableExprFunction(self, ctx: TorQLParser.TableExprFunctionContext):
        return self.visit(ctx.tableFunctionExpr())

    def visitTableExprTag(self, ctx: TorQLParser.TableExprTagContext):
        return self.visit(ctx.torqlxTagElement())

    def visitTableFunctionExpr(self, ctx: TorQLParser.TableFunctionExprContext):
        name = self.visit(ctx.identifier())
        args = self.visit(ctx.tableArgList()) if ctx.tableArgList() else []
        return ast.JoinExpr(table=ast.Field(chain=[name]), table_args=args)

    def visitTableIdentifier(self, ctx: TorQLParser.TableIdentifierContext):
        text = self.visit(ctx.identifier())
        if ctx.databaseIdentifier():
            return [self.visit(ctx.databaseIdentifier()), text]
        return [text]

    def visitTableArgList(self, ctx: TorQLParser.TableArgListContext):
        return [self.visit(arg) for arg in ctx.columnExpr()]

    def visitDatabaseIdentifier(self, ctx: TorQLParser.DatabaseIdentifierContext):
        return self.visit(ctx.identifier())

    def visitFloatingLiteral(self, ctx: TorQLParser.FloatingLiteralContext):
        raise NotImplementedError(f"Unsupported node: visitFloatingLiteral")

    def visitNumberLiteral(self, ctx: TorQLParser.NumberLiteralContext):
        text = ctx.getText().lower()
        if "." in text or "e" in text or text == "-inf" or text == "inf" or text == "nan":
            return ast.Constant(value=float(text))
        return ast.Constant(value=int(text))

    def visitLiteral(self, ctx: TorQLParser.LiteralContext):
        if ctx.NULL_SQL():
            return ast.Constant(value=None)
        if ctx.STRING_LITERAL():
            text = parse_string_literal_ctx(ctx)
            return ast.Constant(value=text)
        return self.visitChildren(ctx)

    def visitInterval(self, ctx: TorQLParser.IntervalContext):
        raise NotImplementedError(f"Unsupported node: Interval")

    def visitKeyword(self, ctx: TorQLParser.KeywordContext):
        raise NotImplementedError(f"Unsupported node: Keyword")

    def visitKeywordForAlias(self, ctx: TorQLParser.KeywordForAliasContext):
        raise NotImplementedError(f"Unsupported node: KeywordForAlias")

    def visitAlias(self, ctx: TorQLParser.AliasContext):
        text = ctx.getText()
        if len(text) >= 2 and (
            (text.startswith("`") and text.endswith("`")) or (text.startswith('"') and text.endswith('"'))
        ):
            text = parse_string_literal_text(text)
        return text

    def visitIdentifier(self, ctx: TorQLParser.IdentifierContext):
        text = ctx.getText()
        if len(text) >= 2 and (
            (text.startswith("`") and text.endswith("`")) or (text.startswith('"') and text.endswith('"'))
        ):
            text = parse_string_literal_text(text)
        return text

    def visitEnumValue(self, ctx: TorQLParser.EnumValueContext):
        raise NotImplementedError(f"Unsupported node: EnumValue")

    def visitColumnExprNullish(self, ctx: TorQLParser.ColumnExprNullishContext):
        return ast.Call(
            name="ifNull",
            args=[self.visit(ctx.columnExpr(0)), self.visit(ctx.columnExpr(1))],
        )

    def visitColumnExprCall(self, ctx: TorQLParser.ColumnExprCallContext):
        return ast.ExprCall(
            expr=self.visit(ctx.columnExpr()), args=self.visit(ctx.columnExprList()) if ctx.columnExprList() else []
        )

    def visitTorqlxTagElementClosed(self, ctx: TorQLParser.TorqlxTagElementClosedContext):
        kind = self.visit(ctx.identifier())
        attributes = [self.visit(a) for a in ctx.torqlxTagAttribute()] if ctx.torqlxTagAttribute() else []
        return ast.TorQLXTag(kind=kind, attributes=attributes)

    def visitTorqlxTagElementNested(self, ctx: TorQLParser.TorqlxTagElementNestedContext):
        opening = self.visit(ctx.identifier(0))
        closing = self.visit(ctx.identifier(1))
        if opening != closing:
            raise SyntaxError(f"Opening and closing TorQLX tags must match. Got {opening} and {closing}")

        attributes = [self.visit(a) for a in ctx.torqlxTagAttribute()] if ctx.torqlxTagAttribute() else []
        if ctx.torqlxTagElement():
            source = self.visit(ctx.torqlxTagElement())
            for a in attributes:
                if a.name == "source":
                    raise SyntaxError(f"Nested TorQLX tags cannot have a source attribute")
            attributes.append(ast.TorQLXAttribute(name="source", value=source))
        if ctx.columnExpr():
            source = self.visit(ctx.columnExpr())
            for a in attributes:
                if a.name == "source":
                    raise SyntaxError(f"Nested TorQLX tags cannot have a source attribute")
            attributes.append(ast.TorQLXAttribute(name="source", value=source))
        return ast.TorQLXTag(kind=opening, attributes=attributes)

    def visitTorqlxTagAttribute(self, ctx: TorQLParser.TorqlxTagAttributeContext):
        name = self.visit(ctx.identifier())
        if ctx.columnExpr():
            return ast.TorQLXAttribute(name=name, value=self.visit(ctx.columnExpr()))
        elif ctx.string():
            return ast.TorQLXAttribute(name=name, value=self.visit(ctx.string()))
        else:
            return ast.TorQLXAttribute(name=name, value=ast.Constant(value=True))

    def visitPlaceholder(self, ctx: TorQLParser.PlaceholderContext):
        return ast.Placeholder(expr=self.visit(ctx.columnExpr()))

    def visitColumnExprTemplateString(self, ctx: TorQLParser.ColumnExprTemplateStringContext):
        return self.visit(ctx.templateString())

    def visitString(self, ctx: TorQLParser.StringContext):
        if ctx.STRING_LITERAL():
            return ast.Constant(value=parse_string_literal_ctx(ctx.STRING_LITERAL()))
        return self.visit(ctx.templateString())

    def visitTemplateString(self, ctx: TorQLParser.TemplateStringContext):
        pieces = []
        for chunk in ctx.stringContents():
            pieces.append(self.visit(chunk))

        if len(pieces) == 0:
            return ast.Constant(value="")
        elif len(pieces) == 1:
            return pieces[0]

        return ast.Call(name="concat", args=pieces)

    def visitFullTemplateString(self, ctx: TorQLParser.FullTemplateStringContext):
        pieces = []
        for chunk in ctx.stringContentsFull():
            pieces.append(self.visit(chunk))

        if len(pieces) == 0:
            return ast.Constant(value="")
        elif len(pieces) == 1:
            return pieces[0]

        return ast.Call(name="concat", args=pieces)

    def visitStringContents(self, ctx: TorQLParser.StringContentsContext):
        if ctx.STRING_TEXT():
            return ast.Constant(value=parse_string_text_ctx(ctx.STRING_TEXT(), escape_quotes=True))
        elif ctx.columnExpr():
            return self.visit(ctx.columnExpr())
        return ast.Constant(value="")

    def visitStringContentsFull(self, ctx: TorQLParser.StringContentsFullContext):
        if ctx.FULL_STRING_TEXT():
            return ast.Constant(value=parse_string_text_ctx(ctx.FULL_STRING_TEXT(), escape_quotes=False))
        elif ctx.columnExpr():
            return self.visit(ctx.columnExpr())
        return ast.Constant(value="")
