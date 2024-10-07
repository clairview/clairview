
// Generated from TorQLParser.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "TorQLParserVisitor.h"


/**
 * This class provides an empty implementation of TorQLParserVisitor, which can be
 * extended to create a visitor which only needs to handle a subset of the available methods.
 */
class  TorQLParserBaseVisitor : public TorQLParserVisitor {
public:

  virtual std::any visitProgram(TorQLParser::ProgramContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDeclaration(TorQLParser::DeclarationContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitExpression(TorQLParser::ExpressionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitVarDecl(TorQLParser::VarDeclContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitIdentifierList(TorQLParser::IdentifierListContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStatement(TorQLParser::StatementContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitReturnStmt(TorQLParser::ReturnStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitThrowStmt(TorQLParser::ThrowStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitCatchBlock(TorQLParser::CatchBlockContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTryCatchStmt(TorQLParser::TryCatchStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitIfStmt(TorQLParser::IfStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWhileStmt(TorQLParser::WhileStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitForStmt(TorQLParser::ForStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitForInStmt(TorQLParser::ForInStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFuncStmt(TorQLParser::FuncStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitVarAssignment(TorQLParser::VarAssignmentContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitExprStmt(TorQLParser::ExprStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitEmptyStmt(TorQLParser::EmptyStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitBlock(TorQLParser::BlockContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitKvPair(TorQLParser::KvPairContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitKvPairList(TorQLParser::KvPairListContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSelect(TorQLParser::SelectContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSelectUnionStmt(TorQLParser::SelectUnionStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSelectStmtWithParens(TorQLParser::SelectStmtWithParensContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSelectStmt(TorQLParser::SelectStmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWithClause(TorQLParser::WithClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTopClause(TorQLParser::TopClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFromClause(TorQLParser::FromClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitArrayJoinClause(TorQLParser::ArrayJoinClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWindowClause(TorQLParser::WindowClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPrewhereClause(TorQLParser::PrewhereClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWhereClause(TorQLParser::WhereClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitGroupByClause(TorQLParser::GroupByClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitHavingClause(TorQLParser::HavingClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitOrderByClause(TorQLParser::OrderByClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitProjectionOrderByClause(TorQLParser::ProjectionOrderByClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLimitAndOffsetClause(TorQLParser::LimitAndOffsetClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitOffsetOnlyClause(TorQLParser::OffsetOnlyClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSettingsClause(TorQLParser::SettingsClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJoinExprOp(TorQLParser::JoinExprOpContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJoinExprTable(TorQLParser::JoinExprTableContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJoinExprParens(TorQLParser::JoinExprParensContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJoinExprCrossOp(TorQLParser::JoinExprCrossOpContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJoinOpInner(TorQLParser::JoinOpInnerContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJoinOpLeftRight(TorQLParser::JoinOpLeftRightContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJoinOpFull(TorQLParser::JoinOpFullContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJoinOpCross(TorQLParser::JoinOpCrossContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJoinConstraintClause(TorQLParser::JoinConstraintClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSampleClause(TorQLParser::SampleClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitOrderExprList(TorQLParser::OrderExprListContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitOrderExpr(TorQLParser::OrderExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitRatioExpr(TorQLParser::RatioExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSettingExprList(TorQLParser::SettingExprListContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSettingExpr(TorQLParser::SettingExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWindowExpr(TorQLParser::WindowExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWinPartitionByClause(TorQLParser::WinPartitionByClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWinOrderByClause(TorQLParser::WinOrderByClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWinFrameClause(TorQLParser::WinFrameClauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFrameStart(TorQLParser::FrameStartContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFrameBetween(TorQLParser::FrameBetweenContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWinFrameBound(TorQLParser::WinFrameBoundContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitExpr(TorQLParser::ExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnTypeExprSimple(TorQLParser::ColumnTypeExprSimpleContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnTypeExprNested(TorQLParser::ColumnTypeExprNestedContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnTypeExprEnum(TorQLParser::ColumnTypeExprEnumContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnTypeExprComplex(TorQLParser::ColumnTypeExprComplexContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnTypeExprParam(TorQLParser::ColumnTypeExprParamContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprList(TorQLParser::ColumnExprListContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprTernaryOp(TorQLParser::ColumnExprTernaryOpContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprAlias(TorQLParser::ColumnExprAliasContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprNegate(TorQLParser::ColumnExprNegateContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprDict(TorQLParser::ColumnExprDictContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprSubquery(TorQLParser::ColumnExprSubqueryContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprLiteral(TorQLParser::ColumnExprLiteralContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprArray(TorQLParser::ColumnExprArrayContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprSubstring(TorQLParser::ColumnExprSubstringContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprCast(TorQLParser::ColumnExprCastContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprOr(TorQLParser::ColumnExprOrContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprNullTupleAccess(TorQLParser::ColumnExprNullTupleAccessContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprPrecedence1(TorQLParser::ColumnExprPrecedence1Context *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprPrecedence2(TorQLParser::ColumnExprPrecedence2Context *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprPrecedence3(TorQLParser::ColumnExprPrecedence3Context *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprInterval(TorQLParser::ColumnExprIntervalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprIsNull(TorQLParser::ColumnExprIsNullContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprWinFunctionTarget(TorQLParser::ColumnExprWinFunctionTargetContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprNullPropertyAccess(TorQLParser::ColumnExprNullPropertyAccessContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprTrim(TorQLParser::ColumnExprTrimContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprTagElement(TorQLParser::ColumnExprTagElementContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprTemplateString(TorQLParser::ColumnExprTemplateStringContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprTuple(TorQLParser::ColumnExprTupleContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprCall(TorQLParser::ColumnExprCallContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprArrayAccess(TorQLParser::ColumnExprArrayAccessContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprBetween(TorQLParser::ColumnExprBetweenContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprPropertyAccess(TorQLParser::ColumnExprPropertyAccessContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprParens(TorQLParser::ColumnExprParensContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprNullArrayAccess(TorQLParser::ColumnExprNullArrayAccessContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprTimestamp(TorQLParser::ColumnExprTimestampContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprNullish(TorQLParser::ColumnExprNullishContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprAnd(TorQLParser::ColumnExprAndContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprTupleAccess(TorQLParser::ColumnExprTupleAccessContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprCase(TorQLParser::ColumnExprCaseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprDate(TorQLParser::ColumnExprDateContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprNot(TorQLParser::ColumnExprNotContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprWinFunction(TorQLParser::ColumnExprWinFunctionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprLambda(TorQLParser::ColumnExprLambdaContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprIdentifier(TorQLParser::ColumnExprIdentifierContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprFunction(TorQLParser::ColumnExprFunctionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnExprAsterisk(TorQLParser::ColumnExprAsteriskContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnLambdaExpr(TorQLParser::ColumnLambdaExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTorqlxTagElementClosed(TorQLParser::TorqlxTagElementClosedContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTorqlxTagElementNested(TorQLParser::TorqlxTagElementNestedContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTorqlxTagAttribute(TorQLParser::TorqlxTagAttributeContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWithExprList(TorQLParser::WithExprListContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWithExprSubquery(TorQLParser::WithExprSubqueryContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWithExprColumn(TorQLParser::WithExprColumnContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitColumnIdentifier(TorQLParser::ColumnIdentifierContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitNestedIdentifier(TorQLParser::NestedIdentifierContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTableExprTag(TorQLParser::TableExprTagContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTableExprIdentifier(TorQLParser::TableExprIdentifierContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTableExprPlaceholder(TorQLParser::TableExprPlaceholderContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTableExprSubquery(TorQLParser::TableExprSubqueryContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTableExprAlias(TorQLParser::TableExprAliasContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTableExprFunction(TorQLParser::TableExprFunctionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTableFunctionExpr(TorQLParser::TableFunctionExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTableIdentifier(TorQLParser::TableIdentifierContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTableArgList(TorQLParser::TableArgListContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDatabaseIdentifier(TorQLParser::DatabaseIdentifierContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFloatingLiteral(TorQLParser::FloatingLiteralContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitNumberLiteral(TorQLParser::NumberLiteralContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLiteral(TorQLParser::LiteralContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitInterval(TorQLParser::IntervalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitKeyword(TorQLParser::KeywordContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitKeywordForAlias(TorQLParser::KeywordForAliasContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAlias(TorQLParser::AliasContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitIdentifier(TorQLParser::IdentifierContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitEnumValue(TorQLParser::EnumValueContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPlaceholder(TorQLParser::PlaceholderContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitString(TorQLParser::StringContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTemplateString(TorQLParser::TemplateStringContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStringContents(TorQLParser::StringContentsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFullTemplateString(TorQLParser::FullTemplateStringContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStringContentsFull(TorQLParser::StringContentsFullContext *ctx) override {
    return visitChildren(ctx);
  }


};

