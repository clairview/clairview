from unittest.mock import Mock, patch

from clairview.clairql_queries.insights.funnels.test.test_funnel_correlation_actors import BaseTestFunnelCorrelationActors
from clairview.clairql_queries.insights.funnels.test.test_funnel_udf import use_udf_funnel_flag_side_effect


@patch("clairviewanalytics.feature_enabled", new=Mock(side_effect=use_udf_funnel_flag_side_effect))
class TestFunnelCorrelationsActorsUDF(BaseTestFunnelCorrelationActors):
    __test__ = True
