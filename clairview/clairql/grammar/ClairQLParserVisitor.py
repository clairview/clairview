# Generated from ClairQLParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ClairQLParser import ClairQLParser
else:
    from ClairQLParser import ClairQLParser

# This class defines a complete generic visitor for a parse tree produced by ClairQLParser.

class ClairQLParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ClairQLParser#program.
    def visitProgram(self, ctx:ClairQLParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#declaration.
    def visitDeclaration(self, ctx:ClairQLParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#expression.
    def visitExpression(self, ctx:ClairQLParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#varDecl.
    def visitVarDecl(self, ctx:ClairQLParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#identifierList.
    def visitIdentifierList(self, ctx:ClairQLParser.IdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#statement.
    def visitStatement(self, ctx:ClairQLParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#returnStmt.
    def visitReturnStmt(self, ctx:ClairQLParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#throwStmt.
    def visitThrowStmt(self, ctx:ClairQLParser.ThrowStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#catchBlock.
    def visitCatchBlock(self, ctx:ClairQLParser.CatchBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#tryCatchStmt.
    def visitTryCatchStmt(self, ctx:ClairQLParser.TryCatchStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ifStmt.
    def visitIfStmt(self, ctx:ClairQLParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#whileStmt.
    def visitWhileStmt(self, ctx:ClairQLParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#forStmt.
    def visitForStmt(self, ctx:ClairQLParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#forInStmt.
    def visitForInStmt(self, ctx:ClairQLParser.ForInStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#funcStmt.
    def visitFuncStmt(self, ctx:ClairQLParser.FuncStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#varAssignment.
    def visitVarAssignment(self, ctx:ClairQLParser.VarAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#exprStmt.
    def visitExprStmt(self, ctx:ClairQLParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#emptyStmt.
    def visitEmptyStmt(self, ctx:ClairQLParser.EmptyStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#block.
    def visitBlock(self, ctx:ClairQLParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#kvPair.
    def visitKvPair(self, ctx:ClairQLParser.KvPairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#kvPairList.
    def visitKvPairList(self, ctx:ClairQLParser.KvPairListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#select.
    def visitSelect(self, ctx:ClairQLParser.SelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#selectUnionStmt.
    def visitSelectUnionStmt(self, ctx:ClairQLParser.SelectUnionStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#selectStmtWithParens.
    def visitSelectStmtWithParens(self, ctx:ClairQLParser.SelectStmtWithParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#selectStmt.
    def visitSelectStmt(self, ctx:ClairQLParser.SelectStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#withClause.
    def visitWithClause(self, ctx:ClairQLParser.WithClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#topClause.
    def visitTopClause(self, ctx:ClairQLParser.TopClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#fromClause.
    def visitFromClause(self, ctx:ClairQLParser.FromClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#arrayJoinClause.
    def visitArrayJoinClause(self, ctx:ClairQLParser.ArrayJoinClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#windowClause.
    def visitWindowClause(self, ctx:ClairQLParser.WindowClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#prewhereClause.
    def visitPrewhereClause(self, ctx:ClairQLParser.PrewhereClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#whereClause.
    def visitWhereClause(self, ctx:ClairQLParser.WhereClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#groupByClause.
    def visitGroupByClause(self, ctx:ClairQLParser.GroupByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#havingClause.
    def visitHavingClause(self, ctx:ClairQLParser.HavingClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#orderByClause.
    def visitOrderByClause(self, ctx:ClairQLParser.OrderByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#projectionOrderByClause.
    def visitProjectionOrderByClause(self, ctx:ClairQLParser.ProjectionOrderByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#limitAndOffsetClause.
    def visitLimitAndOffsetClause(self, ctx:ClairQLParser.LimitAndOffsetClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#offsetOnlyClause.
    def visitOffsetOnlyClause(self, ctx:ClairQLParser.OffsetOnlyClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#settingsClause.
    def visitSettingsClause(self, ctx:ClairQLParser.SettingsClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#JoinExprOp.
    def visitJoinExprOp(self, ctx:ClairQLParser.JoinExprOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#JoinExprTable.
    def visitJoinExprTable(self, ctx:ClairQLParser.JoinExprTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#JoinExprParens.
    def visitJoinExprParens(self, ctx:ClairQLParser.JoinExprParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#JoinExprCrossOp.
    def visitJoinExprCrossOp(self, ctx:ClairQLParser.JoinExprCrossOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#JoinOpInner.
    def visitJoinOpInner(self, ctx:ClairQLParser.JoinOpInnerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#JoinOpLeftRight.
    def visitJoinOpLeftRight(self, ctx:ClairQLParser.JoinOpLeftRightContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#JoinOpFull.
    def visitJoinOpFull(self, ctx:ClairQLParser.JoinOpFullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#joinOpCross.
    def visitJoinOpCross(self, ctx:ClairQLParser.JoinOpCrossContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#joinConstraintClause.
    def visitJoinConstraintClause(self, ctx:ClairQLParser.JoinConstraintClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#sampleClause.
    def visitSampleClause(self, ctx:ClairQLParser.SampleClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#orderExprList.
    def visitOrderExprList(self, ctx:ClairQLParser.OrderExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#orderExpr.
    def visitOrderExpr(self, ctx:ClairQLParser.OrderExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ratioExpr.
    def visitRatioExpr(self, ctx:ClairQLParser.RatioExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#settingExprList.
    def visitSettingExprList(self, ctx:ClairQLParser.SettingExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#settingExpr.
    def visitSettingExpr(self, ctx:ClairQLParser.SettingExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#windowExpr.
    def visitWindowExpr(self, ctx:ClairQLParser.WindowExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#winPartitionByClause.
    def visitWinPartitionByClause(self, ctx:ClairQLParser.WinPartitionByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#winOrderByClause.
    def visitWinOrderByClause(self, ctx:ClairQLParser.WinOrderByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#winFrameClause.
    def visitWinFrameClause(self, ctx:ClairQLParser.WinFrameClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#frameStart.
    def visitFrameStart(self, ctx:ClairQLParser.FrameStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#frameBetween.
    def visitFrameBetween(self, ctx:ClairQLParser.FrameBetweenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#winFrameBound.
    def visitWinFrameBound(self, ctx:ClairQLParser.WinFrameBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#expr.
    def visitExpr(self, ctx:ClairQLParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnTypeExprSimple.
    def visitColumnTypeExprSimple(self, ctx:ClairQLParser.ColumnTypeExprSimpleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnTypeExprNested.
    def visitColumnTypeExprNested(self, ctx:ClairQLParser.ColumnTypeExprNestedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnTypeExprEnum.
    def visitColumnTypeExprEnum(self, ctx:ClairQLParser.ColumnTypeExprEnumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnTypeExprComplex.
    def visitColumnTypeExprComplex(self, ctx:ClairQLParser.ColumnTypeExprComplexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnTypeExprParam.
    def visitColumnTypeExprParam(self, ctx:ClairQLParser.ColumnTypeExprParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#columnExprList.
    def visitColumnExprList(self, ctx:ClairQLParser.ColumnExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprTernaryOp.
    def visitColumnExprTernaryOp(self, ctx:ClairQLParser.ColumnExprTernaryOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprAlias.
    def visitColumnExprAlias(self, ctx:ClairQLParser.ColumnExprAliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprNegate.
    def visitColumnExprNegate(self, ctx:ClairQLParser.ColumnExprNegateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprDict.
    def visitColumnExprDict(self, ctx:ClairQLParser.ColumnExprDictContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprSubquery.
    def visitColumnExprSubquery(self, ctx:ClairQLParser.ColumnExprSubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprLiteral.
    def visitColumnExprLiteral(self, ctx:ClairQLParser.ColumnExprLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprArray.
    def visitColumnExprArray(self, ctx:ClairQLParser.ColumnExprArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprSubstring.
    def visitColumnExprSubstring(self, ctx:ClairQLParser.ColumnExprSubstringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprCast.
    def visitColumnExprCast(self, ctx:ClairQLParser.ColumnExprCastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprOr.
    def visitColumnExprOr(self, ctx:ClairQLParser.ColumnExprOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprNullTupleAccess.
    def visitColumnExprNullTupleAccess(self, ctx:ClairQLParser.ColumnExprNullTupleAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprPrecedence1.
    def visitColumnExprPrecedence1(self, ctx:ClairQLParser.ColumnExprPrecedence1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprPrecedence2.
    def visitColumnExprPrecedence2(self, ctx:ClairQLParser.ColumnExprPrecedence2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprPrecedence3.
    def visitColumnExprPrecedence3(self, ctx:ClairQLParser.ColumnExprPrecedence3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprInterval.
    def visitColumnExprInterval(self, ctx:ClairQLParser.ColumnExprIntervalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprIsNull.
    def visitColumnExprIsNull(self, ctx:ClairQLParser.ColumnExprIsNullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprWinFunctionTarget.
    def visitColumnExprWinFunctionTarget(self, ctx:ClairQLParser.ColumnExprWinFunctionTargetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprNullPropertyAccess.
    def visitColumnExprNullPropertyAccess(self, ctx:ClairQLParser.ColumnExprNullPropertyAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprTrim.
    def visitColumnExprTrim(self, ctx:ClairQLParser.ColumnExprTrimContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprTagElement.
    def visitColumnExprTagElement(self, ctx:ClairQLParser.ColumnExprTagElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprTemplateString.
    def visitColumnExprTemplateString(self, ctx:ClairQLParser.ColumnExprTemplateStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprTuple.
    def visitColumnExprTuple(self, ctx:ClairQLParser.ColumnExprTupleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprCall.
    def visitColumnExprCall(self, ctx:ClairQLParser.ColumnExprCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprArrayAccess.
    def visitColumnExprArrayAccess(self, ctx:ClairQLParser.ColumnExprArrayAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprBetween.
    def visitColumnExprBetween(self, ctx:ClairQLParser.ColumnExprBetweenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprPropertyAccess.
    def visitColumnExprPropertyAccess(self, ctx:ClairQLParser.ColumnExprPropertyAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprParens.
    def visitColumnExprParens(self, ctx:ClairQLParser.ColumnExprParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprNullArrayAccess.
    def visitColumnExprNullArrayAccess(self, ctx:ClairQLParser.ColumnExprNullArrayAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprTimestamp.
    def visitColumnExprTimestamp(self, ctx:ClairQLParser.ColumnExprTimestampContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprNullish.
    def visitColumnExprNullish(self, ctx:ClairQLParser.ColumnExprNullishContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprAnd.
    def visitColumnExprAnd(self, ctx:ClairQLParser.ColumnExprAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprTupleAccess.
    def visitColumnExprTupleAccess(self, ctx:ClairQLParser.ColumnExprTupleAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprCase.
    def visitColumnExprCase(self, ctx:ClairQLParser.ColumnExprCaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprDate.
    def visitColumnExprDate(self, ctx:ClairQLParser.ColumnExprDateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprNot.
    def visitColumnExprNot(self, ctx:ClairQLParser.ColumnExprNotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprWinFunction.
    def visitColumnExprWinFunction(self, ctx:ClairQLParser.ColumnExprWinFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprLambda.
    def visitColumnExprLambda(self, ctx:ClairQLParser.ColumnExprLambdaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprIdentifier.
    def visitColumnExprIdentifier(self, ctx:ClairQLParser.ColumnExprIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprFunction.
    def visitColumnExprFunction(self, ctx:ClairQLParser.ColumnExprFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ColumnExprAsterisk.
    def visitColumnExprAsterisk(self, ctx:ClairQLParser.ColumnExprAsteriskContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#columnLambdaExpr.
    def visitColumnLambdaExpr(self, ctx:ClairQLParser.ColumnLambdaExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ClairqlxTagElementClosed.
    def visitClairqlxTagElementClosed(self, ctx:ClairQLParser.ClairqlxTagElementClosedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#ClairqlxTagElementNested.
    def visitClairqlxTagElementNested(self, ctx:ClairQLParser.ClairqlxTagElementNestedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#clairqlxTagAttribute.
    def visitClairqlxTagAttribute(self, ctx:ClairQLParser.ClairqlxTagAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#withExprList.
    def visitWithExprList(self, ctx:ClairQLParser.WithExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#WithExprSubquery.
    def visitWithExprSubquery(self, ctx:ClairQLParser.WithExprSubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#WithExprColumn.
    def visitWithExprColumn(self, ctx:ClairQLParser.WithExprColumnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#columnIdentifier.
    def visitColumnIdentifier(self, ctx:ClairQLParser.ColumnIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#nestedIdentifier.
    def visitNestedIdentifier(self, ctx:ClairQLParser.NestedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#TableExprTag.
    def visitTableExprTag(self, ctx:ClairQLParser.TableExprTagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#TableExprIdentifier.
    def visitTableExprIdentifier(self, ctx:ClairQLParser.TableExprIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#TableExprPlaceholder.
    def visitTableExprPlaceholder(self, ctx:ClairQLParser.TableExprPlaceholderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#TableExprSubquery.
    def visitTableExprSubquery(self, ctx:ClairQLParser.TableExprSubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#TableExprAlias.
    def visitTableExprAlias(self, ctx:ClairQLParser.TableExprAliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#TableExprFunction.
    def visitTableExprFunction(self, ctx:ClairQLParser.TableExprFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#tableFunctionExpr.
    def visitTableFunctionExpr(self, ctx:ClairQLParser.TableFunctionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#tableIdentifier.
    def visitTableIdentifier(self, ctx:ClairQLParser.TableIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#tableArgList.
    def visitTableArgList(self, ctx:ClairQLParser.TableArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#databaseIdentifier.
    def visitDatabaseIdentifier(self, ctx:ClairQLParser.DatabaseIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#floatingLiteral.
    def visitFloatingLiteral(self, ctx:ClairQLParser.FloatingLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#numberLiteral.
    def visitNumberLiteral(self, ctx:ClairQLParser.NumberLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#literal.
    def visitLiteral(self, ctx:ClairQLParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#interval.
    def visitInterval(self, ctx:ClairQLParser.IntervalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#keyword.
    def visitKeyword(self, ctx:ClairQLParser.KeywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#keywordForAlias.
    def visitKeywordForAlias(self, ctx:ClairQLParser.KeywordForAliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#alias.
    def visitAlias(self, ctx:ClairQLParser.AliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#identifier.
    def visitIdentifier(self, ctx:ClairQLParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#enumValue.
    def visitEnumValue(self, ctx:ClairQLParser.EnumValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#placeholder.
    def visitPlaceholder(self, ctx:ClairQLParser.PlaceholderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#string.
    def visitString(self, ctx:ClairQLParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#templateString.
    def visitTemplateString(self, ctx:ClairQLParser.TemplateStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#stringContents.
    def visitStringContents(self, ctx:ClairQLParser.StringContentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#fullTemplateString.
    def visitFullTemplateString(self, ctx:ClairQLParser.FullTemplateStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ClairQLParser#stringContentsFull.
    def visitStringContentsFull(self, ctx:ClairQLParser.StringContentsFullContext):
        return self.visitChildren(ctx)



del ClairQLParser