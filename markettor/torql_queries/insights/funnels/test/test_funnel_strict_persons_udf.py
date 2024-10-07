from unittest.mock import patch, Mock

from markettor.torql_queries.insights.funnels.test.test_funnel_strict_persons import BaseTestFunnelStrictStepsPersons
from markettor.torql_queries.insights.funnels.test.test_funnel_udf import use_udf_funnel_flag_side_effect


@patch("markettoranalytics.feature_enabled", new=Mock(side_effect=use_udf_funnel_flag_side_effect))
class TestFunnelStrictStepsPersons(BaseTestFunnelStrictStepsPersons):
    __test__ = True
