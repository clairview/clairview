import clairviewanalytics
from clairview.models import Team


def torql_insights_replace_filters(team: Team) -> bool:
    return clairviewanalytics.feature_enabled(
        "torql-insights-replace-filters",
        str(team.uuid),
        groups={
            "organization": str(team.organization_id),
            "project": str(team.id),
        },
        group_properties={
            "organization": {
                "id": str(team.organization_id),
            },
            "project": {
                "id": str(team.id),
            },
        },
        only_evaluate_locally=True,
        send_feature_flag_events=False,
    )


def insight_funnels_use_udf(team: Team) -> bool:
    return clairviewanalytics.feature_enabled(
        "insight-funnels-use-udf",
        str(team.uuid),
        groups={
            "organization": str(team.organization_id),
            "project": str(team.id),
        },
        group_properties={
            "organization": {
                "id": str(team.organization_id),
            },
            "project": {
                "id": str(team.id),
            },
        },
        only_evaluate_locally=False,
        send_feature_flag_events=False,
    )


def insight_funnels_use_udf_trends(team: Team) -> bool:
    return clairviewanalytics.feature_enabled(
        "insight-funnels-use-udf-trends",
        str(team.uuid),
        groups={
            "organization": str(team.organization_id),
            "project": str(team.id),
        },
        group_properties={
            "organization": {
                "id": str(team.organization_id),
            },
            "project": {
                "id": str(team.id),
            },
        },
        only_evaluate_locally=False,
        send_feature_flag_events=False,
    )