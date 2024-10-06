from unittest.mock import Mock, patch

from markettor.hogql_queries.insights.funnels.test.test_funnel_correlation import BaseTestClickhouseFunnelCorrelation
from markettor.hogql_queries.insights.funnels.test.test_funnel_udf import use_udf_funnel_flag_side_effect


@patch("markettoranalytics.feature_enabled", new=Mock(side_effect=use_udf_funnel_flag_side_effect))
class TestClickhouseFunnelCorrelationUDF(BaseTestClickhouseFunnelCorrelation):
    __test__ = True
