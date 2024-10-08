from typing import cast
from unittest.mock import patch, Mock

from clairview.constants import INSIGHT_FUNNELS, TRENDS_LINEAR
from clairview.clairql_queries.insights.funnels.funnels_query_runner import FunnelsQueryRunner
from clairview.clairql_queries.insights.funnels.test.test_funnel_trends import BaseTestFunnelTrends
from clairview.clairql_queries.legacy_compatibility.filter_to_query import filter_to_query
from clairview.schema import FunnelsQuery, FunnelsQueryResponse


@patch(
    "clairviewanalytics.feature_enabled",
    new=Mock(side_effect=lambda key, *args, **kwargs: key == "insight-funnels-use-udf-trends"),
)
class TestFunnelTrendsUDF(BaseTestFunnelTrends):
    __test__ = True

    def test_assert_udf_flag_is_working(self):
        filters = {
            "insight": INSIGHT_FUNNELS,
            "funnel_viz_type": "trends",
            "display": TRENDS_LINEAR,
            "interval": "hour",
            "date_from": "2021-05-01 00:00:00",
            "funnel_window_interval": 7,
            "events": [
                {"id": "step one", "order": 0},
                {"id": "step two", "order": 1},
                {"id": "step three", "order": 2},
            ],
        }

        query = cast(FunnelsQuery, filter_to_query(filters))
        results = cast(FunnelsQueryResponse, FunnelsQueryRunner(query=query, team=self.team).calculate())

        self.assertTrue(results.isUdf)

    def test_assert_steps_flag_is_off(self):
        filters = {
            "insight": INSIGHT_FUNNELS,
            "funnel_viz_type": "steps",
            "interval": "hour",
            "date_from": "2021-05-01 00:00:00",
            "funnel_window_interval": 7,
            "events": [
                {"id": "step one", "order": 0},
                {"id": "step two", "order": 1},
                {"id": "step three", "order": 2},
            ],
        }

        query = cast(FunnelsQuery, filter_to_query(filters))
        results = cast(FunnelsQueryResponse, FunnelsQueryRunner(query=query, team=self.team).calculate())

        self.assertFalse(results.isUdf)
