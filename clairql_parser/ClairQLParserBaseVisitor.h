
// Generated from ClairQLParser.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "ClairQLParserVisitor.h"


/**
 * This class provides an empty implementation of ClairQLParserVisitor, which can be
 * extended to create a visitor which only needs to handle a subset of the available methods.
 */
class  ClairQLParserBaseVisitor : public ClairQLParserVisitor {
public:

  virtual std::any visitProgram(ClairQLParser::ProgramContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDeclaration(ClairQLParser::DeclarationContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitExpression(ClairQLParser::ExpressionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitVarDecl(ClairQLParser::VarDeclContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitIdentifierList(ClairQLParser::IdentifierListContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStatement(ClairQLParser::StatementContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitReturnStmt(ClairQLParser::ReturnStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitThrowStmt(ClairQLParser::ThrowStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitCatchBlock(ClairQLParser::CatchBlockContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTryCatchStmt(ClairQLParser::TryCatchStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitIfStmt(ClairQLParser::IfStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWhileStmt(ClairQLParser::WhileStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitForStmt(ClairQLParser::ForStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitForInStmt(ClairQLParser::ForInStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFuncStmt(ClairQLParser::FuncStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitVarAssignment(ClairQLParser::VarAssignmentContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitExprStmt(ClairQLParser::ExprStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitEmptyStmt(ClairQLParser::EmptyStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitBlock(ClairQLParser::BlockContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitKvPair(ClairQLParser::KvPairContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitKvPairList(ClairQLParser::KvPairListContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSelect(ClairQLParser::SelectContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSelectUnionStmt(ClairQLParser::SelectUnionStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSelectStmtWithParens(ClairQLParser::SelectStmtWithParensContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSelectStmt(ClairQLParser::SelectStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWithClause(ClairQLParser::WithClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTopClause(ClairQLParser::TopClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFromClause(ClairQLParser::FromClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitArrayJoinClause(ClairQLParser::ArrayJoinClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWindowClause(ClairQLParser::WindowClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPrewhereClause(ClairQLParser::PrewhereClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWhereClause(ClairQLParser::WhereClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitGroupByClause(ClairQLParser::GroupByClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitHavingClause(ClairQLParser::HavingClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitOrderByClause(ClairQLParser::OrderByClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitProjectionOrderByClause(ClairQLParser::ProjectionOrderByClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLimitAndOffsetClause(ClairQLParser::LimitAndOffsetClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitOffsetOnlyClause(ClairQLParser::OffsetOnlyClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSettingsClause(ClairQLParser::SettingsClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJoinExprOp(ClairQLParser::JoinExprOpContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJoinExprTable(ClairQLParser::JoinExprTableContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJoinExprParens(ClairQLParser::JoinExprParensContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJoinExprCrossOp(ClairQLParser::JoinExprCrossOpContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJoinOpInner(ClairQLParser::JoinOpInnerContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJoinOpLeftRight(ClairQLParser::JoinOpLeftRightContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJoinOpFull(ClairQLParser::JoinOpFullContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJoinOpCross(ClairQLParser::JoinOpCrossContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJoinConstraintClause(ClairQLParser::JoinConstraintClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSampleClause(ClairQLParser::SampleClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitOrderExprList(ClairQLParser::OrderExprListContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitOrderExpr(ClairQLParser::OrderExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitRatioExpr(ClairQLParser::RatioExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSettingExprList(ClairQLParser::SettingExprListContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSettingExpr(ClairQLParser::SettingExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWindowExpr(ClairQLParser::WindowExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWinPartitionByClause(ClairQLParser::WinPartitionByClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWinOrderByClause(ClairQLParser::WinOrderByClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWinFrameClause(ClairQLParser::WinFrameClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFrameStart(ClairQLParser::FrameStartContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFrameBetween(ClairQLParser::FrameBetweenContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWinFrameBound(ClairQLParser::WinFrameBoundContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitExpr(ClairQLParser::ExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnTypeExprSimple(ClairQLParser::ColumnTypeExprSimpleContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnTypeExprNested(ClairQLParser::ColumnTypeExprNestedContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnTypeExprEnum(ClairQLParser::ColumnTypeExprEnumContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnTypeExprComplex(ClairQLParser::ColumnTypeExprComplexContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnTypeExprParam(ClairQLParser::ColumnTypeExprParamContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprList(ClairQLParser::ColumnExprListContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprTernaryOp(ClairQLParser::ColumnExprTernaryOpContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprAlias(ClairQLParser::ColumnExprAliasContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprNegate(ClairQLParser::ColumnExprNegateContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprDict(ClairQLParser::ColumnExprDictContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprSubquery(ClairQLParser::ColumnExprSubqueryContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprLiteral(ClairQLParser::ColumnExprLiteralContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprArray(ClairQLParser::ColumnExprArrayContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprSubstring(ClairQLParser::ColumnExprSubstringContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprCast(ClairQLParser::ColumnExprCastContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprOr(ClairQLParser::ColumnExprOrContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprNullTupleAccess(ClairQLParser::ColumnExprNullTupleAccessContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprPrecedence1(ClairQLParser::ColumnExprPrecedence1Context *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprPrecedence2(ClairQLParser::ColumnExprPrecedence2Context *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprPrecedence3(ClairQLParser::ColumnExprPrecedence3Context *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprInterval(ClairQLParser::ColumnExprIntervalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprIsNull(ClairQLParser::ColumnExprIsNullContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprWinFunctionTarget(ClairQLParser::ColumnExprWinFunctionTargetContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprNullPropertyAccess(ClairQLParser::ColumnExprNullPropertyAccessContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprTrim(ClairQLParser::ColumnExprTrimContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprTagElement(ClairQLParser::ColumnExprTagElementContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprTemplateString(ClairQLParser::ColumnExprTemplateStringContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprTuple(ClairQLParser::ColumnExprTupleContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprCall(ClairQLParser::ColumnExprCallContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprArrayAccess(ClairQLParser::ColumnExprArrayAccessContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprBetween(ClairQLParser::ColumnExprBetweenContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprPropertyAccess(ClairQLParser::ColumnExprPropertyAccessContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprParens(ClairQLParser::ColumnExprParensContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprNullArrayAccess(ClairQLParser::ColumnExprNullArrayAccessContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprTimestamp(ClairQLParser::ColumnExprTimestampContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprNullish(ClairQLParser::ColumnExprNullishContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprAnd(ClairQLParser::ColumnExprAndContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprTupleAccess(ClairQLParser::ColumnExprTupleAccessContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprCase(ClairQLParser::ColumnExprCaseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprDate(ClairQLParser::ColumnExprDateContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprNot(ClairQLParser::ColumnExprNotContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprWinFunction(ClairQLParser::ColumnExprWinFunctionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprLambda(ClairQLParser::ColumnExprLambdaContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprIdentifier(ClairQLParser::ColumnExprIdentifierContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprFunction(ClairQLParser::ColumnExprFunctionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprAsterisk(ClairQLParser::ColumnExprAsteriskContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnLambdaExpr(ClairQLParser::ColumnLambdaExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitClairqlxTagElementClosed(ClairQLParser::ClairqlxTagElementClosedContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitClairqlxTagElementNested(ClairQLParser::ClairqlxTagElementNestedContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitClairqlxTagAttribute(ClairQLParser::ClairqlxTagAttributeContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWithExprList(ClairQLParser::WithExprListContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWithExprSubquery(ClairQLParser::WithExprSubqueryContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWithExprColumn(ClairQLParser::WithExprColumnContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnIdentifier(ClairQLParser::ColumnIdentifierContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitNestedIdentifier(ClairQLParser::NestedIdentifierContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTableExprTag(ClairQLParser::TableExprTagContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTableExprIdentifier(ClairQLParser::TableExprIdentifierContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTableExprPlaceholder(ClairQLParser::TableExprPlaceholderContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTableExprSubquery(ClairQLParser::TableExprSubqueryContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTableExprAlias(ClairQLParser::TableExprAliasContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTableExprFunction(ClairQLParser::TableExprFunctionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTableFunctionExpr(ClairQLParser::TableFunctionExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTableIdentifier(ClairQLParser::TableIdentifierContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTableArgList(ClairQLParser::TableArgListContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDatabaseIdentifier(ClairQLParser::DatabaseIdentifierContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFloatingLiteral(ClairQLParser::FloatingLiteralContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitNumberLiteral(ClairQLParser::NumberLiteralContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLiteral(ClairQLParser::LiteralContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitInterval(ClairQLParser::IntervalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitKeyword(ClairQLParser::KeywordContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitKeywordForAlias(ClairQLParser::KeywordForAliasContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAlias(ClairQLParser::AliasContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitIdentifier(ClairQLParser::IdentifierContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitEnumValue(ClairQLParser::EnumValueContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPlaceholder(ClairQLParser::PlaceholderContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitString(ClairQLParser::StringContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTemplateString(ClairQLParser::TemplateStringContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStringContents(ClairQLParser::StringContentsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFullTemplateString(ClairQLParser::FullTemplateStringContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStringContentsFull(ClairQLParser::StringContentsFullContext *ctx) override {
    return visitChildren(ctx);
  }


};

