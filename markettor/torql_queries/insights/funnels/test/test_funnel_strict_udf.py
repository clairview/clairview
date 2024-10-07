from unittest.mock import Mock, patch

from markettor.torql_queries.insights.funnels.test.test_funnel_strict import (
    BaseTestFunnelStrictStepsBreakdown,
    BaseTestFunnelStrictSteps,
    BaseTestStrictFunnelGroupBreakdown,
    BaseTestFunnelStrictStepsConversionTime,
)


@patch("markettoranalytics.feature_enabled", new=Mock(return_value=True))
class TestFunnelStrictStepsBreakdownUDF(BaseTestFunnelStrictStepsBreakdown):
    __test__ = True


@patch("markettoranalytics.feature_enabled", new=Mock(return_value=True))
class TestFunnelStrictStepsUDF(BaseTestFunnelStrictSteps):
    __test__ = True


@patch("markettoranalytics.feature_enabled", new=Mock(return_value=True))
class TestStrictFunnelGroupBreakdownUDF(BaseTestStrictFunnelGroupBreakdown):
    __test__ = True


@patch("markettoranalytics.feature_enabled", new=Mock(return_value=True))
class TestFunnelStrictStepsConversionTimeUDF(BaseTestFunnelStrictStepsConversionTime):
    __test__ = True
