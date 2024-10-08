# Generated from TorQLParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .TorQLParser import TorQLParser
else:
    from TorQLParser import TorQLParser

# This class defines a complete generic visitor for a parse tree produced by TorQLParser.

class TorQLParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TorQLParser#program.
    def visitProgram(self, ctx:TorQLParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#declaration.
    def visitDeclaration(self, ctx:TorQLParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#expression.
    def visitExpression(self, ctx:TorQLParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#varDecl.
    def visitVarDecl(self, ctx:TorQLParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#identifierList.
    def visitIdentifierList(self, ctx:TorQLParser.IdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#statement.
    def visitStatement(self, ctx:TorQLParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#returnStmt.
    def visitReturnStmt(self, ctx:TorQLParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#throwStmt.
    def visitThrowStmt(self, ctx:TorQLParser.ThrowStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#catchBlock.
    def visitCatchBlock(self, ctx:TorQLParser.CatchBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#tryCatchStmt.
    def visitTryCatchStmt(self, ctx:TorQLParser.TryCatchStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ifStmt.
    def visitIfStmt(self, ctx:TorQLParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#whileStmt.
    def visitWhileStmt(self, ctx:TorQLParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#forStmt.
    def visitForStmt(self, ctx:TorQLParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#forInStmt.
    def visitForInStmt(self, ctx:TorQLParser.ForInStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#funcStmt.
    def visitFuncStmt(self, ctx:TorQLParser.FuncStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#varAssignment.
    def visitVarAssignment(self, ctx:TorQLParser.VarAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#exprStmt.
    def visitExprStmt(self, ctx:TorQLParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#emptyStmt.
    def visitEmptyStmt(self, ctx:TorQLParser.EmptyStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#block.
    def visitBlock(self, ctx:TorQLParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#kvPair.
    def visitKvPair(self, ctx:TorQLParser.KvPairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#kvPairList.
    def visitKvPairList(self, ctx:TorQLParser.KvPairListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#select.
    def visitSelect(self, ctx:TorQLParser.SelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#selectUnionStmt.
    def visitSelectUnionStmt(self, ctx:TorQLParser.SelectUnionStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#selectStmtWithParens.
    def visitSelectStmtWithParens(self, ctx:TorQLParser.SelectStmtWithParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#selectStmt.
    def visitSelectStmt(self, ctx:TorQLParser.SelectStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#withClause.
    def visitWithClause(self, ctx:TorQLParser.WithClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#topClause.
    def visitTopClause(self, ctx:TorQLParser.TopClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#fromClause.
    def visitFromClause(self, ctx:TorQLParser.FromClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#arrayJoinClause.
    def visitArrayJoinClause(self, ctx:TorQLParser.ArrayJoinClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#windowClause.
    def visitWindowClause(self, ctx:TorQLParser.WindowClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#prewhereClause.
    def visitPrewhereClause(self, ctx:TorQLParser.PrewhereClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#whereClause.
    def visitWhereClause(self, ctx:TorQLParser.WhereClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#groupByClause.
    def visitGroupByClause(self, ctx:TorQLParser.GroupByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#havingClause.
    def visitHavingClause(self, ctx:TorQLParser.HavingClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#orderByClause.
    def visitOrderByClause(self, ctx:TorQLParser.OrderByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#projectionOrderByClause.
    def visitProjectionOrderByClause(self, ctx:TorQLParser.ProjectionOrderByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#limitAndOffsetClause.
    def visitLimitAndOffsetClause(self, ctx:TorQLParser.LimitAndOffsetClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#offsetOnlyClause.
    def visitOffsetOnlyClause(self, ctx:TorQLParser.OffsetOnlyClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#settingsClause.
    def visitSettingsClause(self, ctx:TorQLParser.SettingsClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#JoinExprOp.
    def visitJoinExprOp(self, ctx:TorQLParser.JoinExprOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#JoinExprTable.
    def visitJoinExprTable(self, ctx:TorQLParser.JoinExprTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#JoinExprParens.
    def visitJoinExprParens(self, ctx:TorQLParser.JoinExprParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#JoinExprCrossOp.
    def visitJoinExprCrossOp(self, ctx:TorQLParser.JoinExprCrossOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#JoinOpInner.
    def visitJoinOpInner(self, ctx:TorQLParser.JoinOpInnerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#JoinOpLeftRight.
    def visitJoinOpLeftRight(self, ctx:TorQLParser.JoinOpLeftRightContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#JoinOpFull.
    def visitJoinOpFull(self, ctx:TorQLParser.JoinOpFullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#joinOpCross.
    def visitJoinOpCross(self, ctx:TorQLParser.JoinOpCrossContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#joinConstraintClause.
    def visitJoinConstraintClause(self, ctx:TorQLParser.JoinConstraintClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#sampleClause.
    def visitSampleClause(self, ctx:TorQLParser.SampleClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#orderExprList.
    def visitOrderExprList(self, ctx:TorQLParser.OrderExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#orderExpr.
    def visitOrderExpr(self, ctx:TorQLParser.OrderExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ratioExpr.
    def visitRatioExpr(self, ctx:TorQLParser.RatioExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#settingExprList.
    def visitSettingExprList(self, ctx:TorQLParser.SettingExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#settingExpr.
    def visitSettingExpr(self, ctx:TorQLParser.SettingExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#windowExpr.
    def visitWindowExpr(self, ctx:TorQLParser.WindowExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#winPartitionByClause.
    def visitWinPartitionByClause(self, ctx:TorQLParser.WinPartitionByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#winOrderByClause.
    def visitWinOrderByClause(self, ctx:TorQLParser.WinOrderByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#winFrameClause.
    def visitWinFrameClause(self, ctx:TorQLParser.WinFrameClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#frameStart.
    def visitFrameStart(self, ctx:TorQLParser.FrameStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#frameBetween.
    def visitFrameBetween(self, ctx:TorQLParser.FrameBetweenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#winFrameBound.
    def visitWinFrameBound(self, ctx:TorQLParser.WinFrameBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#expr.
    def visitExpr(self, ctx:TorQLParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnTypeExprSimple.
    def visitColumnTypeExprSimple(self, ctx:TorQLParser.ColumnTypeExprSimpleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnTypeExprNested.
    def visitColumnTypeExprNested(self, ctx:TorQLParser.ColumnTypeExprNestedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnTypeExprEnum.
    def visitColumnTypeExprEnum(self, ctx:TorQLParser.ColumnTypeExprEnumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnTypeExprComplex.
    def visitColumnTypeExprComplex(self, ctx:TorQLParser.ColumnTypeExprComplexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnTypeExprParam.
    def visitColumnTypeExprParam(self, ctx:TorQLParser.ColumnTypeExprParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#columnExprList.
    def visitColumnExprList(self, ctx:TorQLParser.ColumnExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprTernaryOp.
    def visitColumnExprTernaryOp(self, ctx:TorQLParser.ColumnExprTernaryOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprAlias.
    def visitColumnExprAlias(self, ctx:TorQLParser.ColumnExprAliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprNegate.
    def visitColumnExprNegate(self, ctx:TorQLParser.ColumnExprNegateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprDict.
    def visitColumnExprDict(self, ctx:TorQLParser.ColumnExprDictContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprSubquery.
    def visitColumnExprSubquery(self, ctx:TorQLParser.ColumnExprSubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprLiteral.
    def visitColumnExprLiteral(self, ctx:TorQLParser.ColumnExprLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprArray.
    def visitColumnExprArray(self, ctx:TorQLParser.ColumnExprArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprSubstring.
    def visitColumnExprSubstring(self, ctx:TorQLParser.ColumnExprSubstringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprCast.
    def visitColumnExprCast(self, ctx:TorQLParser.ColumnExprCastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprOr.
    def visitColumnExprOr(self, ctx:TorQLParser.ColumnExprOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprNullTupleAccess.
    def visitColumnExprNullTupleAccess(self, ctx:TorQLParser.ColumnExprNullTupleAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprPrecedence1.
    def visitColumnExprPrecedence1(self, ctx:TorQLParser.ColumnExprPrecedence1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprPrecedence2.
    def visitColumnExprPrecedence2(self, ctx:TorQLParser.ColumnExprPrecedence2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprPrecedence3.
    def visitColumnExprPrecedence3(self, ctx:TorQLParser.ColumnExprPrecedence3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprInterval.
    def visitColumnExprInterval(self, ctx:TorQLParser.ColumnExprIntervalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprIsNull.
    def visitColumnExprIsNull(self, ctx:TorQLParser.ColumnExprIsNullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprWinFunctionTarget.
    def visitColumnExprWinFunctionTarget(self, ctx:TorQLParser.ColumnExprWinFunctionTargetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprNullPropertyAccess.
    def visitColumnExprNullPropertyAccess(self, ctx:TorQLParser.ColumnExprNullPropertyAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprTrim.
    def visitColumnExprTrim(self, ctx:TorQLParser.ColumnExprTrimContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprTagElement.
    def visitColumnExprTagElement(self, ctx:TorQLParser.ColumnExprTagElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprTemplateString.
    def visitColumnExprTemplateString(self, ctx:TorQLParser.ColumnExprTemplateStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprTuple.
    def visitColumnExprTuple(self, ctx:TorQLParser.ColumnExprTupleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprCall.
    def visitColumnExprCall(self, ctx:TorQLParser.ColumnExprCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprArrayAccess.
    def visitColumnExprArrayAccess(self, ctx:TorQLParser.ColumnExprArrayAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprBetween.
    def visitColumnExprBetween(self, ctx:TorQLParser.ColumnExprBetweenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprPropertyAccess.
    def visitColumnExprPropertyAccess(self, ctx:TorQLParser.ColumnExprPropertyAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprParens.
    def visitColumnExprParens(self, ctx:TorQLParser.ColumnExprParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprNullArrayAccess.
    def visitColumnExprNullArrayAccess(self, ctx:TorQLParser.ColumnExprNullArrayAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprTimestamp.
    def visitColumnExprTimestamp(self, ctx:TorQLParser.ColumnExprTimestampContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprNullish.
    def visitColumnExprNullish(self, ctx:TorQLParser.ColumnExprNullishContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprAnd.
    def visitColumnExprAnd(self, ctx:TorQLParser.ColumnExprAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprTupleAccess.
    def visitColumnExprTupleAccess(self, ctx:TorQLParser.ColumnExprTupleAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprCase.
    def visitColumnExprCase(self, ctx:TorQLParser.ColumnExprCaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprDate.
    def visitColumnExprDate(self, ctx:TorQLParser.ColumnExprDateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprNot.
    def visitColumnExprNot(self, ctx:TorQLParser.ColumnExprNotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprWinFunction.
    def visitColumnExprWinFunction(self, ctx:TorQLParser.ColumnExprWinFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprLambda.
    def visitColumnExprLambda(self, ctx:TorQLParser.ColumnExprLambdaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprIdentifier.
    def visitColumnExprIdentifier(self, ctx:TorQLParser.ColumnExprIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprFunction.
    def visitColumnExprFunction(self, ctx:TorQLParser.ColumnExprFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#ColumnExprAsterisk.
    def visitColumnExprAsterisk(self, ctx:TorQLParser.ColumnExprAsteriskContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#columnLambdaExpr.
    def visitColumnLambdaExpr(self, ctx:TorQLParser.ColumnLambdaExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#TorqlxTagElementClosed.
    def visitTorqlxTagElementClosed(self, ctx:TorQLParser.TorqlxTagElementClosedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#TorqlxTagElementNested.
    def visitTorqlxTagElementNested(self, ctx:TorQLParser.TorqlxTagElementNestedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#torqlxTagAttribute.
    def visitTorqlxTagAttribute(self, ctx:TorQLParser.TorqlxTagAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#withExprList.
    def visitWithExprList(self, ctx:TorQLParser.WithExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#WithExprSubquery.
    def visitWithExprSubquery(self, ctx:TorQLParser.WithExprSubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#WithExprColumn.
    def visitWithExprColumn(self, ctx:TorQLParser.WithExprColumnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#columnIdentifier.
    def visitColumnIdentifier(self, ctx:TorQLParser.ColumnIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#nestedIdentifier.
    def visitNestedIdentifier(self, ctx:TorQLParser.NestedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#TableExprTag.
    def visitTableExprTag(self, ctx:TorQLParser.TableExprTagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#TableExprIdentifier.
    def visitTableExprIdentifier(self, ctx:TorQLParser.TableExprIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#TableExprPlaceholder.
    def visitTableExprPlaceholder(self, ctx:TorQLParser.TableExprPlaceholderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#TableExprSubquery.
    def visitTableExprSubquery(self, ctx:TorQLParser.TableExprSubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#TableExprAlias.
    def visitTableExprAlias(self, ctx:TorQLParser.TableExprAliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#TableExprFunction.
    def visitTableExprFunction(self, ctx:TorQLParser.TableExprFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#tableFunctionExpr.
    def visitTableFunctionExpr(self, ctx:TorQLParser.TableFunctionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#tableIdentifier.
    def visitTableIdentifier(self, ctx:TorQLParser.TableIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#tableArgList.
    def visitTableArgList(self, ctx:TorQLParser.TableArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#databaseIdentifier.
    def visitDatabaseIdentifier(self, ctx:TorQLParser.DatabaseIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#floatingLiteral.
    def visitFloatingLiteral(self, ctx:TorQLParser.FloatingLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#numberLiteral.
    def visitNumberLiteral(self, ctx:TorQLParser.NumberLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#literal.
    def visitLiteral(self, ctx:TorQLParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#interval.
    def visitInterval(self, ctx:TorQLParser.IntervalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#keyword.
    def visitKeyword(self, ctx:TorQLParser.KeywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#keywordForAlias.
    def visitKeywordForAlias(self, ctx:TorQLParser.KeywordForAliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#alias.
    def visitAlias(self, ctx:TorQLParser.AliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#identifier.
    def visitIdentifier(self, ctx:TorQLParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#enumValue.
    def visitEnumValue(self, ctx:TorQLParser.EnumValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#placeholder.
    def visitPlaceholder(self, ctx:TorQLParser.PlaceholderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#string.
    def visitString(self, ctx:TorQLParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#templateString.
    def visitTemplateString(self, ctx:TorQLParser.TemplateStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#stringContents.
    def visitStringContents(self, ctx:TorQLParser.StringContentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#fullTemplateString.
    def visitFullTemplateString(self, ctx:TorQLParser.FullTemplateStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TorQLParser#stringContentsFull.
    def visitStringContentsFull(self, ctx:TorQLParser.StringContentsFullContext):
        return self.visitChildren(ctx)



del TorQLParser