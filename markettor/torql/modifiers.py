from typing import TYPE_CHECKING, Optional

import markettoranalytics

from markettor.cloud_utils import is_cloud
from markettor.schema import (
    TorQLQueryModifiers,
    InCohortVia,
    MaterializationMode,
    PersonsArgMaxVersion,
    BounceRatePageViewMode,
    PropertyGroupsMode,
    SessionTableVersion,
)

if TYPE_CHECKING:
    from markettor.models import Team
    from markettor.models import User


def create_default_modifiers_for_user(
    user: "User", team: "Team", modifiers: Optional[TorQLQueryModifiers] = None
) -> TorQLQueryModifiers:
    if modifiers is None:
        modifiers = TorQLQueryModifiers()
    else:
        modifiers = modifiers.model_copy()

    modifiers.useMaterializedViews = markettoranalytics.feature_enabled(
        "data-modeling",
        str(user.distinct_id),
        person_properties={
            "email": user.email,
        },
        only_evaluate_locally=True,
        send_feature_flag_events=False,
    )

    return create_default_modifiers_for_team(team, modifiers)


def create_default_modifiers_for_team(
    team: "Team", modifiers: Optional[TorQLQueryModifiers] = None
) -> TorQLQueryModifiers:
    if modifiers is None:
        modifiers = TorQLQueryModifiers()
    else:
        modifiers = modifiers.model_copy()

    if isinstance(team.modifiers, dict):
        for key, value in team.modifiers.items():
            if getattr(modifiers, key) is None:
                setattr(modifiers, key, value)

    set_default_modifier_values(modifiers, team)

    return modifiers


def set_default_modifier_values(modifiers: TorQLQueryModifiers, team: "Team"):
    if modifiers.personsOnEventsMode is None:
        modifiers.personsOnEventsMode = team.person_on_events_mode_flag_based_default

    if modifiers.personsArgMaxVersion is None:
        modifiers.personsArgMaxVersion = PersonsArgMaxVersion.AUTO

    if modifiers.inCohortVia is None:
        modifiers.inCohortVia = InCohortVia.AUTO

    if modifiers.materializationMode is None or modifiers.materializationMode == MaterializationMode.AUTO:
        modifiers.materializationMode = MaterializationMode.LEGACY_NULL_AS_NULL

    if modifiers.optimizeJoinedFilters is None:
        modifiers.optimizeJoinedFilters = False

    if modifiers.bounceRatePageViewMode is None:
        modifiers.bounceRatePageViewMode = BounceRatePageViewMode.COUNT_PAGEVIEWS

    if modifiers.sessionTableVersion is None:
        modifiers.sessionTableVersion = SessionTableVersion.AUTO

    if (
        modifiers.propertyGroupsMode is None
        and is_cloud()
        and markettoranalytics.feature_enabled(
            "torql-optimized-property-groups-mode-enabled",
            str(team.uuid),
            groups={"project": str(team.id)},
            group_properties={"project": {"id": str(team.id), "created_at": team.created_at, "uuid": team.uuid}},
            only_evaluate_locally=True,
            send_feature_flag_events=False,
        )
    ):
        modifiers.propertyGroupsMode = PropertyGroupsMode.OPTIMIZED


def set_default_in_cohort_via(modifiers: TorQLQueryModifiers) -> TorQLQueryModifiers:
    if modifiers.inCohortVia is None or modifiers.inCohortVia == InCohortVia.AUTO:
        modifiers.inCohortVia = InCohortVia.SUBQUERY

    return modifiers
