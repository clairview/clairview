
// Generated from ClairQLParser.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "ClairQLParser.h"



/**
 * This class defines an abstract visitor for a parse tree
 * produced by ClairQLParser.
 */
class  ClairQLParserVisitor : public antlr4::tree::AbstractParseTreeVisitor {
public:

  /**
   * Visit parse trees produced by ClairQLParser.
   */
    virtual std::any visitProgram(ClairQLParser::ProgramContext *context) = 0;

    virtual std::any visitDeclaration(ClairQLParser::DeclarationContext *context) = 0;

    virtual std::any visitExpression(ClairQLParser::ExpressionContext *context) = 0;

    virtual std::any visitVarDecl(ClairQLParser::VarDeclContext *context) = 0;

    virtual std::any visitIdentifierList(ClairQLParser::IdentifierListContext *context) = 0;

    virtual std::any visitStatement(ClairQLParser::StatementContext *context) = 0;

    virtual std::any visitReturnStmt(ClairQLParser::ReturnStmtContext *context) = 0;

    virtual std::any visitThrowStmt(ClairQLParser::ThrowStmtContext *context) = 0;

    virtual std::any visitCatchBlock(ClairQLParser::CatchBlockContext *context) = 0;

    virtual std::any visitTryCatchStmt(ClairQLParser::TryCatchStmtContext *context) = 0;

    virtual std::any visitIfStmt(ClairQLParser::IfStmtContext *context) = 0;

    virtual std::any visitWhileStmt(ClairQLParser::WhileStmtContext *context) = 0;

    virtual std::any visitForStmt(ClairQLParser::ForStmtContext *context) = 0;

    virtual std::any visitForInStmt(ClairQLParser::ForInStmtContext *context) = 0;

    virtual std::any visitFuncStmt(ClairQLParser::FuncStmtContext *context) = 0;

    virtual std::any visitVarAssignment(ClairQLParser::VarAssignmentContext *context) = 0;

    virtual std::any visitExprStmt(ClairQLParser::ExprStmtContext *context) = 0;

    virtual std::any visitEmptyStmt(ClairQLParser::EmptyStmtContext *context) = 0;

    virtual std::any visitBlock(ClairQLParser::BlockContext *context) = 0;

    virtual std::any visitKvPair(ClairQLParser::KvPairContext *context) = 0;

    virtual std::any visitKvPairList(ClairQLParser::KvPairListContext *context) = 0;

    virtual std::any visitSelect(ClairQLParser::SelectContext *context) = 0;

    virtual std::any visitSelectUnionStmt(ClairQLParser::SelectUnionStmtContext *context) = 0;

    virtual std::any visitSelectStmtWithParens(ClairQLParser::SelectStmtWithParensContext *context) = 0;

    virtual std::any visitSelectStmt(ClairQLParser::SelectStmtContext *context) = 0;

    virtual std::any visitWithClause(ClairQLParser::WithClauseContext *context) = 0;

    virtual std::any visitTopClause(ClairQLParser::TopClauseContext *context) = 0;

    virtual std::any visitFromClause(ClairQLParser::FromClauseContext *context) = 0;

    virtual std::any visitArrayJoinClause(ClairQLParser::ArrayJoinClauseContext *context) = 0;

    virtual std::any visitWindowClause(ClairQLParser::WindowClauseContext *context) = 0;

    virtual std::any visitPrewhereClause(ClairQLParser::PrewhereClauseContext *context) = 0;

    virtual std::any visitWhereClause(ClairQLParser::WhereClauseContext *context) = 0;

    virtual std::any visitGroupByClause(ClairQLParser::GroupByClauseContext *context) = 0;

    virtual std::any visitHavingClause(ClairQLParser::HavingClauseContext *context) = 0;

    virtual std::any visitOrderByClause(ClairQLParser::OrderByClauseContext *context) = 0;

    virtual std::any visitProjectionOrderByClause(ClairQLParser::ProjectionOrderByClauseContext *context) = 0;

    virtual std::any visitLimitAndOffsetClause(ClairQLParser::LimitAndOffsetClauseContext *context) = 0;

    virtual std::any visitOffsetOnlyClause(ClairQLParser::OffsetOnlyClauseContext *context) = 0;

    virtual std::any visitSettingsClause(ClairQLParser::SettingsClauseContext *context) = 0;

    virtual std::any visitJoinExprOp(ClairQLParser::JoinExprOpContext *context) = 0;

    virtual std::any visitJoinExprTable(ClairQLParser::JoinExprTableContext *context) = 0;

    virtual std::any visitJoinExprParens(ClairQLParser::JoinExprParensContext *context) = 0;

    virtual std::any visitJoinExprCrossOp(ClairQLParser::JoinExprCrossOpContext *context) = 0;

    virtual std::any visitJoinOpInner(ClairQLParser::JoinOpInnerContext *context) = 0;

    virtual std::any visitJoinOpLeftRight(ClairQLParser::JoinOpLeftRightContext *context) = 0;

    virtual std::any visitJoinOpFull(ClairQLParser::JoinOpFullContext *context) = 0;

    virtual std::any visitJoinOpCross(ClairQLParser::JoinOpCrossContext *context) = 0;

    virtual std::any visitJoinConstraintClause(ClairQLParser::JoinConstraintClauseContext *context) = 0;

    virtual std::any visitSampleClause(ClairQLParser::SampleClauseContext *context) = 0;

    virtual std::any visitOrderExprList(ClairQLParser::OrderExprListContext *context) = 0;

    virtual std::any visitOrderExpr(ClairQLParser::OrderExprContext *context) = 0;

    virtual std::any visitRatioExpr(ClairQLParser::RatioExprContext *context) = 0;

    virtual std::any visitSettingExprList(ClairQLParser::SettingExprListContext *context) = 0;

    virtual std::any visitSettingExpr(ClairQLParser::SettingExprContext *context) = 0;

    virtual std::any visitWindowExpr(ClairQLParser::WindowExprContext *context) = 0;

    virtual std::any visitWinPartitionByClause(ClairQLParser::WinPartitionByClauseContext *context) = 0;

    virtual std::any visitWinOrderByClause(ClairQLParser::WinOrderByClauseContext *context) = 0;

    virtual std::any visitWinFrameClause(ClairQLParser::WinFrameClauseContext *context) = 0;

    virtual std::any visitFrameStart(ClairQLParser::FrameStartContext *context) = 0;

    virtual std::any visitFrameBetween(ClairQLParser::FrameBetweenContext *context) = 0;

    virtual std::any visitWinFrameBound(ClairQLParser::WinFrameBoundContext *context) = 0;

    virtual std::any visitExpr(ClairQLParser::ExprContext *context) = 0;

    virtual std::any visitColumnTypeExprSimple(ClairQLParser::ColumnTypeExprSimpleContext *context) = 0;

    virtual std::any visitColumnTypeExprNested(ClairQLParser::ColumnTypeExprNestedContext *context) = 0;

    virtual std::any visitColumnTypeExprEnum(ClairQLParser::ColumnTypeExprEnumContext *context) = 0;

    virtual std::any visitColumnTypeExprComplex(ClairQLParser::ColumnTypeExprComplexContext *context) = 0;

    virtual std::any visitColumnTypeExprParam(ClairQLParser::ColumnTypeExprParamContext *context) = 0;

    virtual std::any visitColumnExprList(ClairQLParser::ColumnExprListContext *context) = 0;

    virtual std::any visitColumnExprTernaryOp(ClairQLParser::ColumnExprTernaryOpContext *context) = 0;

    virtual std::any visitColumnExprAlias(ClairQLParser::ColumnExprAliasContext *context) = 0;

    virtual std::any visitColumnExprNegate(ClairQLParser::ColumnExprNegateContext *context) = 0;

    virtual std::any visitColumnExprDict(ClairQLParser::ColumnExprDictContext *context) = 0;

    virtual std::any visitColumnExprSubquery(ClairQLParser::ColumnExprSubqueryContext *context) = 0;

    virtual std::any visitColumnExprLiteral(ClairQLParser::ColumnExprLiteralContext *context) = 0;

    virtual std::any visitColumnExprArray(ClairQLParser::ColumnExprArrayContext *context) = 0;

    virtual std::any visitColumnExprSubstring(ClairQLParser::ColumnExprSubstringContext *context) = 0;

    virtual std::any visitColumnExprCast(ClairQLParser::ColumnExprCastContext *context) = 0;

    virtual std::any visitColumnExprOr(ClairQLParser::ColumnExprOrContext *context) = 0;

    virtual std::any visitColumnExprNullTupleAccess(ClairQLParser::ColumnExprNullTupleAccessContext *context) = 0;

    virtual std::any visitColumnExprPrecedence1(ClairQLParser::ColumnExprPrecedence1Context *context) = 0;

    virtual std::any visitColumnExprPrecedence2(ClairQLParser::ColumnExprPrecedence2Context *context) = 0;

    virtual std::any visitColumnExprPrecedence3(ClairQLParser::ColumnExprPrecedence3Context *context) = 0;

    virtual std::any visitColumnExprInterval(ClairQLParser::ColumnExprIntervalContext *context) = 0;

    virtual std::any visitColumnExprIsNull(ClairQLParser::ColumnExprIsNullContext *context) = 0;

    virtual std::any visitColumnExprWinFunctionTarget(ClairQLParser::ColumnExprWinFunctionTargetContext *context) = 0;

    virtual std::any visitColumnExprNullPropertyAccess(ClairQLParser::ColumnExprNullPropertyAccessContext *context) = 0;

    virtual std::any visitColumnExprTrim(ClairQLParser::ColumnExprTrimContext *context) = 0;

    virtual std::any visitColumnExprTagElement(ClairQLParser::ColumnExprTagElementContext *context) = 0;

    virtual std::any visitColumnExprTemplateString(ClairQLParser::ColumnExprTemplateStringContext *context) = 0;

    virtual std::any visitColumnExprTuple(ClairQLParser::ColumnExprTupleContext *context) = 0;

    virtual std::any visitColumnExprCall(ClairQLParser::ColumnExprCallContext *context) = 0;

    virtual std::any visitColumnExprArrayAccess(ClairQLParser::ColumnExprArrayAccessContext *context) = 0;

    virtual std::any visitColumnExprBetween(ClairQLParser::ColumnExprBetweenContext *context) = 0;

    virtual std::any visitColumnExprPropertyAccess(ClairQLParser::ColumnExprPropertyAccessContext *context) = 0;

    virtual std::any visitColumnExprParens(ClairQLParser::ColumnExprParensContext *context) = 0;

    virtual std::any visitColumnExprNullArrayAccess(ClairQLParser::ColumnExprNullArrayAccessContext *context) = 0;

    virtual std::any visitColumnExprTimestamp(ClairQLParser::ColumnExprTimestampContext *context) = 0;

    virtual std::any visitColumnExprNullish(ClairQLParser::ColumnExprNullishContext *context) = 0;

    virtual std::any visitColumnExprAnd(ClairQLParser::ColumnExprAndContext *context) = 0;

    virtual std::any visitColumnExprTupleAccess(ClairQLParser::ColumnExprTupleAccessContext *context) = 0;

    virtual std::any visitColumnExprCase(ClairQLParser::ColumnExprCaseContext *context) = 0;

    virtual std::any visitColumnExprDate(ClairQLParser::ColumnExprDateContext *context) = 0;

    virtual std::any visitColumnExprNot(ClairQLParser::ColumnExprNotContext *context) = 0;

    virtual std::any visitColumnExprWinFunction(ClairQLParser::ColumnExprWinFunctionContext *context) = 0;

    virtual std::any visitColumnExprLambda(ClairQLParser::ColumnExprLambdaContext *context) = 0;

    virtual std::any visitColumnExprIdentifier(ClairQLParser::ColumnExprIdentifierContext *context) = 0;

    virtual std::any visitColumnExprFunction(ClairQLParser::ColumnExprFunctionContext *context) = 0;

    virtual std::any visitColumnExprAsterisk(ClairQLParser::ColumnExprAsteriskContext *context) = 0;

    virtual std::any visitColumnLambdaExpr(ClairQLParser::ColumnLambdaExprContext *context) = 0;

    virtual std::any visitClairqlxTagElementClosed(ClairQLParser::ClairqlxTagElementClosedContext *context) = 0;

    virtual std::any visitClairqlxTagElementNested(ClairQLParser::ClairqlxTagElementNestedContext *context) = 0;

    virtual std::any visitClairqlxTagAttribute(ClairQLParser::ClairqlxTagAttributeContext *context) = 0;

    virtual std::any visitWithExprList(ClairQLParser::WithExprListContext *context) = 0;

    virtual std::any visitWithExprSubquery(ClairQLParser::WithExprSubqueryContext *context) = 0;

    virtual std::any visitWithExprColumn(ClairQLParser::WithExprColumnContext *context) = 0;

    virtual std::any visitColumnIdentifier(ClairQLParser::ColumnIdentifierContext *context) = 0;

    virtual std::any visitNestedIdentifier(ClairQLParser::NestedIdentifierContext *context) = 0;

    virtual std::any visitTableExprTag(ClairQLParser::TableExprTagContext *context) = 0;

    virtual std::any visitTableExprIdentifier(ClairQLParser::TableExprIdentifierContext *context) = 0;

    virtual std::any visitTableExprPlaceholder(ClairQLParser::TableExprPlaceholderContext *context) = 0;

    virtual std::any visitTableExprSubquery(ClairQLParser::TableExprSubqueryContext *context) = 0;

    virtual std::any visitTableExprAlias(ClairQLParser::TableExprAliasContext *context) = 0;

    virtual std::any visitTableExprFunction(ClairQLParser::TableExprFunctionContext *context) = 0;

    virtual std::any visitTableFunctionExpr(ClairQLParser::TableFunctionExprContext *context) = 0;

    virtual std::any visitTableIdentifier(ClairQLParser::TableIdentifierContext *context) = 0;

    virtual std::any visitTableArgList(ClairQLParser::TableArgListContext *context) = 0;

    virtual std::any visitDatabaseIdentifier(ClairQLParser::DatabaseIdentifierContext *context) = 0;

    virtual std::any visitFloatingLiteral(ClairQLParser::FloatingLiteralContext *context) = 0;

    virtual std::any visitNumberLiteral(ClairQLParser::NumberLiteralContext *context) = 0;

    virtual std::any visitLiteral(ClairQLParser::LiteralContext *context) = 0;

    virtual std::any visitInterval(ClairQLParser::IntervalContext *context) = 0;

    virtual std::any visitKeyword(ClairQLParser::KeywordContext *context) = 0;

    virtual std::any visitKeywordForAlias(ClairQLParser::KeywordForAliasContext *context) = 0;

    virtual std::any visitAlias(ClairQLParser::AliasContext *context) = 0;

    virtual std::any visitIdentifier(ClairQLParser::IdentifierContext *context) = 0;

    virtual std::any visitEnumValue(ClairQLParser::EnumValueContext *context) = 0;

    virtual std::any visitPlaceholder(ClairQLParser::PlaceholderContext *context) = 0;

    virtual std::any visitString(ClairQLParser::StringContext *context) = 0;

    virtual std::any visitTemplateString(ClairQLParser::TemplateStringContext *context) = 0;

    virtual std::any visitStringContents(ClairQLParser::StringContentsContext *context) = 0;

    virtual std::any visitFullTemplateString(ClairQLParser::FullTemplateStringContext *context) = 0;

    virtual std::any visitStringContentsFull(ClairQLParser::StringContentsFullContext *context) = 0;


};

