
// Generated from TorQLParser.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "TorQLParser.h"



/**
 * This class defines an abstract visitor for a parse tree
 * produced by TorQLParser.
 */
class  TorQLParserVisitor : public antlr4::tree::AbstractParseTreeVisitor {
public:

  /**
   * Visit parse trees produced by TorQLParser.
   */
    virtual std::any visitProgram(TorQLParser::ProgramContext *context) = 0;

    virtual std::any visitDeclaration(TorQLParser::DeclarationContext *context) = 0;

    virtual std::any visitExpression(TorQLParser::ExpressionContext *context) = 0;

    virtual std::any visitVarDecl(TorQLParser::VarDeclContext *context) = 0;

    virtual std::any visitIdentifierList(TorQLParser::IdentifierListContext *context) = 0;

    virtual std::any visitStatement(TorQLParser::StatementContext *context) = 0;

    virtual std::any visitReturnStmt(TorQLParser::ReturnStmtContext *context) = 0;

    virtual std::any visitThrowStmt(TorQLParser::ThrowStmtContext *context) = 0;

    virtual std::any visitCatchBlock(TorQLParser::CatchBlockContext *context) = 0;

    virtual std::any visitTryCatchStmt(TorQLParser::TryCatchStmtContext *context) = 0;

    virtual std::any visitIfStmt(TorQLParser::IfStmtContext *context) = 0;

    virtual std::any visitWhileStmt(TorQLParser::WhileStmtContext *context) = 0;

    virtual std::any visitForStmt(TorQLParser::ForStmtContext *context) = 0;

    virtual std::any visitForInStmt(TorQLParser::ForInStmtContext *context) = 0;

    virtual std::any visitFuncStmt(TorQLParser::FuncStmtContext *context) = 0;

    virtual std::any visitVarAssignment(TorQLParser::VarAssignmentContext *context) = 0;

    virtual std::any visitExprStmt(TorQLParser::ExprStmtContext *context) = 0;

    virtual std::any visitEmptyStmt(TorQLParser::EmptyStmtContext *context) = 0;

    virtual std::any visitBlock(TorQLParser::BlockContext *context) = 0;

    virtual std::any visitKvPair(TorQLParser::KvPairContext *context) = 0;

    virtual std::any visitKvPairList(TorQLParser::KvPairListContext *context) = 0;

    virtual std::any visitSelect(TorQLParser::SelectContext *context) = 0;

    virtual std::any visitSelectUnionStmt(TorQLParser::SelectUnionStmtContext *context) = 0;

    virtual std::any visitSelectStmtWithParens(TorQLParser::SelectStmtWithParensContext *context) = 0;

    virtual std::any visitSelectStmt(TorQLParser::SelectStmtContext *context) = 0;

    virtual std::any visitWithClause(TorQLParser::WithClauseContext *context) = 0;

    virtual std::any visitTopClause(TorQLParser::TopClauseContext *context) = 0;

    virtual std::any visitFromClause(TorQLParser::FromClauseContext *context) = 0;

    virtual std::any visitArrayJoinClause(TorQLParser::ArrayJoinClauseContext *context) = 0;

    virtual std::any visitWindowClause(TorQLParser::WindowClauseContext *context) = 0;

    virtual std::any visitPrewhereClause(TorQLParser::PrewhereClauseContext *context) = 0;

    virtual std::any visitWhereClause(TorQLParser::WhereClauseContext *context) = 0;

    virtual std::any visitGroupByClause(TorQLParser::GroupByClauseContext *context) = 0;

    virtual std::any visitHavingClause(TorQLParser::HavingClauseContext *context) = 0;

    virtual std::any visitOrderByClause(TorQLParser::OrderByClauseContext *context) = 0;

    virtual std::any visitProjectionOrderByClause(TorQLParser::ProjectionOrderByClauseContext *context) = 0;

    virtual std::any visitLimitAndOffsetClause(TorQLParser::LimitAndOffsetClauseContext *context) = 0;

    virtual std::any visitOffsetOnlyClause(TorQLParser::OffsetOnlyClauseContext *context) = 0;

    virtual std::any visitSettingsClause(TorQLParser::SettingsClauseContext *context) = 0;

    virtual std::any visitJoinExprOp(TorQLParser::JoinExprOpContext *context) = 0;

    virtual std::any visitJoinExprTable(TorQLParser::JoinExprTableContext *context) = 0;

    virtual std::any visitJoinExprParens(TorQLParser::JoinExprParensContext *context) = 0;

    virtual std::any visitJoinExprCrossOp(TorQLParser::JoinExprCrossOpContext *context) = 0;

    virtual std::any visitJoinOpInner(TorQLParser::JoinOpInnerContext *context) = 0;

    virtual std::any visitJoinOpLeftRight(TorQLParser::JoinOpLeftRightContext *context) = 0;

    virtual std::any visitJoinOpFull(TorQLParser::JoinOpFullContext *context) = 0;

    virtual std::any visitJoinOpCross(TorQLParser::JoinOpCrossContext *context) = 0;

    virtual std::any visitJoinConstraintClause(TorQLParser::JoinConstraintClauseContext *context) = 0;

    virtual std::any visitSampleClause(TorQLParser::SampleClauseContext *context) = 0;

    virtual std::any visitOrderExprList(TorQLParser::OrderExprListContext *context) = 0;

    virtual std::any visitOrderExpr(TorQLParser::OrderExprContext *context) = 0;

    virtual std::any visitRatioExpr(TorQLParser::RatioExprContext *context) = 0;

    virtual std::any visitSettingExprList(TorQLParser::SettingExprListContext *context) = 0;

    virtual std::any visitSettingExpr(TorQLParser::SettingExprContext *context) = 0;

    virtual std::any visitWindowExpr(TorQLParser::WindowExprContext *context) = 0;

    virtual std::any visitWinPartitionByClause(TorQLParser::WinPartitionByClauseContext *context) = 0;

    virtual std::any visitWinOrderByClause(TorQLParser::WinOrderByClauseContext *context) = 0;

    virtual std::any visitWinFrameClause(TorQLParser::WinFrameClauseContext *context) = 0;

    virtual std::any visitFrameStart(TorQLParser::FrameStartContext *context) = 0;

    virtual std::any visitFrameBetween(TorQLParser::FrameBetweenContext *context) = 0;

    virtual std::any visitWinFrameBound(TorQLParser::WinFrameBoundContext *context) = 0;

    virtual std::any visitExpr(TorQLParser::ExprContext *context) = 0;

    virtual std::any visitColumnTypeExprSimple(TorQLParser::ColumnTypeExprSimpleContext *context) = 0;

    virtual std::any visitColumnTypeExprNested(TorQLParser::ColumnTypeExprNestedContext *context) = 0;

    virtual std::any visitColumnTypeExprEnum(TorQLParser::ColumnTypeExprEnumContext *context) = 0;

    virtual std::any visitColumnTypeExprComplex(TorQLParser::ColumnTypeExprComplexContext *context) = 0;

    virtual std::any visitColumnTypeExprParam(TorQLParser::ColumnTypeExprParamContext *context) = 0;

    virtual std::any visitColumnExprList(TorQLParser::ColumnExprListContext *context) = 0;

    virtual std::any visitColumnExprTernaryOp(TorQLParser::ColumnExprTernaryOpContext *context) = 0;

    virtual std::any visitColumnExprAlias(TorQLParser::ColumnExprAliasContext *context) = 0;

    virtual std::any visitColumnExprNegate(TorQLParser::ColumnExprNegateContext *context) = 0;

    virtual std::any visitColumnExprDict(TorQLParser::ColumnExprDictContext *context) = 0;

    virtual std::any visitColumnExprSubquery(TorQLParser::ColumnExprSubqueryContext *context) = 0;

    virtual std::any visitColumnExprLiteral(TorQLParser::ColumnExprLiteralContext *context) = 0;

    virtual std::any visitColumnExprArray(TorQLParser::ColumnExprArrayContext *context) = 0;

    virtual std::any visitColumnExprSubstring(TorQLParser::ColumnExprSubstringContext *context) = 0;

    virtual std::any visitColumnExprCast(TorQLParser::ColumnExprCastContext *context) = 0;

    virtual std::any visitColumnExprOr(TorQLParser::ColumnExprOrContext *context) = 0;

    virtual std::any visitColumnExprNullTupleAccess(TorQLParser::ColumnExprNullTupleAccessContext *context) = 0;

    virtual std::any visitColumnExprPrecedence1(TorQLParser::ColumnExprPrecedence1Context *context) = 0;

    virtual std::any visitColumnExprPrecedence2(TorQLParser::ColumnExprPrecedence2Context *context) = 0;

    virtual std::any visitColumnExprPrecedence3(TorQLParser::ColumnExprPrecedence3Context *context) = 0;

    virtual std::any visitColumnExprInterval(TorQLParser::ColumnExprIntervalContext *context) = 0;

    virtual std::any visitColumnExprIsNull(TorQLParser::ColumnExprIsNullContext *context) = 0;

    virtual std::any visitColumnExprWinFunctionTarget(TorQLParser::ColumnExprWinFunctionTargetContext *context) = 0;

    virtual std::any visitColumnExprNullPropertyAccess(TorQLParser::ColumnExprNullPropertyAccessContext *context) = 0;

    virtual std::any visitColumnExprTrim(TorQLParser::ColumnExprTrimContext *context) = 0;

    virtual std::any visitColumnExprTagElement(TorQLParser::ColumnExprTagElementContext *context) = 0;

    virtual std::any visitColumnExprTemplateString(TorQLParser::ColumnExprTemplateStringContext *context) = 0;

    virtual std::any visitColumnExprTuple(TorQLParser::ColumnExprTupleContext *context) = 0;

    virtual std::any visitColumnExprCall(TorQLParser::ColumnExprCallContext *context) = 0;

    virtual std::any visitColumnExprArrayAccess(TorQLParser::ColumnExprArrayAccessContext *context) = 0;

    virtual std::any visitColumnExprBetween(TorQLParser::ColumnExprBetweenContext *context) = 0;

    virtual std::any visitColumnExprPropertyAccess(TorQLParser::ColumnExprPropertyAccessContext *context) = 0;

    virtual std::any visitColumnExprParens(TorQLParser::ColumnExprParensContext *context) = 0;

    virtual std::any visitColumnExprNullArrayAccess(TorQLParser::ColumnExprNullArrayAccessContext *context) = 0;

    virtual std::any visitColumnExprTimestamp(TorQLParser::ColumnExprTimestampContext *context) = 0;

    virtual std::any visitColumnExprNullish(TorQLParser::ColumnExprNullishContext *context) = 0;

    virtual std::any visitColumnExprAnd(TorQLParser::ColumnExprAndContext *context) = 0;

    virtual std::any visitColumnExprTupleAccess(TorQLParser::ColumnExprTupleAccessContext *context) = 0;

    virtual std::any visitColumnExprCase(TorQLParser::ColumnExprCaseContext *context) = 0;

    virtual std::any visitColumnExprDate(TorQLParser::ColumnExprDateContext *context) = 0;

    virtual std::any visitColumnExprNot(TorQLParser::ColumnExprNotContext *context) = 0;

    virtual std::any visitColumnExprWinFunction(TorQLParser::ColumnExprWinFunctionContext *context) = 0;

    virtual std::any visitColumnExprLambda(TorQLParser::ColumnExprLambdaContext *context) = 0;

    virtual std::any visitColumnExprIdentifier(TorQLParser::ColumnExprIdentifierContext *context) = 0;

    virtual std::any visitColumnExprFunction(TorQLParser::ColumnExprFunctionContext *context) = 0;

    virtual std::any visitColumnExprAsterisk(TorQLParser::ColumnExprAsteriskContext *context) = 0;

    virtual std::any visitColumnLambdaExpr(TorQLParser::ColumnLambdaExprContext *context) = 0;

    virtual std::any visitTorqlxTagElementClosed(TorQLParser::TorqlxTagElementClosedContext *context) = 0;

    virtual std::any visitTorqlxTagElementNested(TorQLParser::TorqlxTagElementNestedContext *context) = 0;

    virtual std::any visitTorqlxTagAttribute(TorQLParser::TorqlxTagAttributeContext *context) = 0;

    virtual std::any visitWithExprList(TorQLParser::WithExprListContext *context) = 0;

    virtual std::any visitWithExprSubquery(TorQLParser::WithExprSubqueryContext *context) = 0;

    virtual std::any visitWithExprColumn(TorQLParser::WithExprColumnContext *context) = 0;

    virtual std::any visitColumnIdentifier(TorQLParser::ColumnIdentifierContext *context) = 0;

    virtual std::any visitNestedIdentifier(TorQLParser::NestedIdentifierContext *context) = 0;

    virtual std::any visitTableExprTag(TorQLParser::TableExprTagContext *context) = 0;

    virtual std::any visitTableExprIdentifier(TorQLParser::TableExprIdentifierContext *context) = 0;

    virtual std::any visitTableExprPlaceholder(TorQLParser::TableExprPlaceholderContext *context) = 0;

    virtual std::any visitTableExprSubquery(TorQLParser::TableExprSubqueryContext *context) = 0;

    virtual std::any visitTableExprAlias(TorQLParser::TableExprAliasContext *context) = 0;

    virtual std::any visitTableExprFunction(TorQLParser::TableExprFunctionContext *context) = 0;

    virtual std::any visitTableFunctionExpr(TorQLParser::TableFunctionExprContext *context) = 0;

    virtual std::any visitTableIdentifier(TorQLParser::TableIdentifierContext *context) = 0;

    virtual std::any visitTableArgList(TorQLParser::TableArgListContext *context) = 0;

    virtual std::any visitDatabaseIdentifier(TorQLParser::DatabaseIdentifierContext *context) = 0;

    virtual std::any visitFloatingLiteral(TorQLParser::FloatingLiteralContext *context) = 0;

    virtual std::any visitNumberLiteral(TorQLParser::NumberLiteralContext *context) = 0;

    virtual std::any visitLiteral(TorQLParser::LiteralContext *context) = 0;

    virtual std::any visitInterval(TorQLParser::IntervalContext *context) = 0;

    virtual std::any visitKeyword(TorQLParser::KeywordContext *context) = 0;

    virtual std::any visitKeywordForAlias(TorQLParser::KeywordForAliasContext *context) = 0;

    virtual std::any visitAlias(TorQLParser::AliasContext *context) = 0;

    virtual std::any visitIdentifier(TorQLParser::IdentifierContext *context) = 0;

    virtual std::any visitEnumValue(TorQLParser::EnumValueContext *context) = 0;

    virtual std::any visitPlaceholder(TorQLParser::PlaceholderContext *context) = 0;

    virtual std::any visitString(TorQLParser::StringContext *context) = 0;

    virtual std::any visitTemplateString(TorQLParser::TemplateStringContext *context) = 0;

    virtual std::any visitStringContents(TorQLParser::StringContentsContext *context) = 0;

    virtual std::any visitFullTemplateString(TorQLParser::FullTemplateStringContext *context) = 0;

    virtual std::any visitStringContentsFull(TorQLParser::StringContentsFullContext *context) = 0;


};

