from typing import NamedTuple
from unittest.mock import patch
from clairview.torql.modifiers import create_default_modifiers_for_team
from clairview.torql.query import execute_torql_query
from clairview.models import Cohort
from clairview.schema import (
    TorQLQueryModifiers,
    PersonsArgMaxVersion,
    PersonsOnEventsMode,
    MaterializationMode,
)
from clairview.test.base import BaseTest
from django.test import override_settings


class TestModifiers(BaseTest):
    @override_settings(PERSON_ON_EVENTS_OVERRIDE=False, PERSON_ON_EVENTS_V2_OVERRIDE=False)
    def test_create_default_modifiers_for_team_init(self):
        assert self.team.person_on_events_mode == PersonsOnEventsMode.PERSON_ID_OVERRIDE_PROPERTIES_JOINED
        modifiers = create_default_modifiers_for_team(self.team)
        # The default is not None! It's explicitly `PERSON_ID_OVERRIDE_PROPERTIES_JOINED`
        assert modifiers.personsOnEventsMode == PersonsOnEventsMode.PERSON_ID_OVERRIDE_PROPERTIES_JOINED
        modifiers = create_default_modifiers_for_team(
            self.team,
            TorQLQueryModifiers(personsOnEventsMode=PersonsOnEventsMode.PERSON_ID_NO_OVERRIDE_PROPERTIES_ON_EVENTS),
        )
        assert modifiers.personsOnEventsMode == PersonsOnEventsMode.PERSON_ID_NO_OVERRIDE_PROPERTIES_ON_EVENTS
        modifiers = create_default_modifiers_for_team(
            self.team,
            TorQLQueryModifiers(personsOnEventsMode=PersonsOnEventsMode.PERSON_ID_OVERRIDE_PROPERTIES_ON_EVENTS),
        )
        assert modifiers.personsOnEventsMode == PersonsOnEventsMode.PERSON_ID_OVERRIDE_PROPERTIES_ON_EVENTS

    def test_team_modifiers_override(self):
        assert self.team.modifiers is None
        modifiers = create_default_modifiers_for_team(self.team)
        assert modifiers.personsOnEventsMode == self.team.default_modifiers["personsOnEventsMode"]
        assert (
            modifiers.personsOnEventsMode
            == PersonsOnEventsMode.PERSON_ID_OVERRIDE_PROPERTIES_JOINED  # the default mode
        )

        self.team.modifiers = {"personsOnEventsMode": PersonsOnEventsMode.PERSON_ID_OVERRIDE_PROPERTIES_ON_EVENTS}
        self.team.save()
        modifiers = create_default_modifiers_for_team(self.team)
        assert modifiers.personsOnEventsMode == PersonsOnEventsMode.PERSON_ID_OVERRIDE_PROPERTIES_ON_EVENTS
        assert (
            self.team.default_modifiers["personsOnEventsMode"]
            == PersonsOnEventsMode.PERSON_ID_OVERRIDE_PROPERTIES_JOINED  # no change here
        )

        self.team.modifiers = {"personsOnEventsMode": PersonsOnEventsMode.PERSON_ID_NO_OVERRIDE_PROPERTIES_ON_EVENTS}
        self.team.save()
        modifiers = create_default_modifiers_for_team(self.team)
        assert modifiers.personsOnEventsMode == PersonsOnEventsMode.PERSON_ID_NO_OVERRIDE_PROPERTIES_ON_EVENTS

    @patch(
        # _person_on_events_person_id_override_properties_on_events is normally determined by feature flag
        "clairview.models.team.Team._person_on_events_person_id_override_properties_on_events",
        True,
    )
    def test_modifiers_persons_on_events_default_is_based_on_team_property(self):
        assert self.team.modifiers is None
        modifiers = create_default_modifiers_for_team(self.team)
        assert self.team.person_on_events_mode == PersonsOnEventsMode.PERSON_ID_OVERRIDE_PROPERTIES_ON_EVENTS
        assert modifiers.personsOnEventsMode == self.team.default_modifiers["personsOnEventsMode"]
        assert modifiers.personsOnEventsMode == PersonsOnEventsMode.PERSON_ID_OVERRIDE_PROPERTIES_ON_EVENTS

    def test_modifiers_persons_on_events_mode_person_id_override_properties_on_events(self):
        query = "SELECT event, person_id FROM events"

        # Control
        response = execute_torql_query(
            query,
            team=self.team,
            modifiers=TorQLQueryModifiers(personsOnEventsMode=PersonsOnEventsMode.DISABLED),
        )
        assert " JOIN " in response.clickhouse

        # Test
        response = execute_torql_query(
            query,
            team=self.team,
            modifiers=TorQLQueryModifiers(
                personsOnEventsMode=PersonsOnEventsMode.PERSON_ID_NO_OVERRIDE_PROPERTIES_ON_EVENTS
            ),
        )
        assert " JOIN " not in response.clickhouse

    def test_modifiers_persons_on_events_mode_mapping(self):
        query = "SELECT event, person.id, person.properties, person.created_at FROM events"

        class TestCase(NamedTuple):
            mode: PersonsOnEventsMode
            expected_columns: list[str]
            other_expected_values: list[str] = []

        test_cases: list[TestCase] = [
            TestCase(
                PersonsOnEventsMode.DISABLED,
                [
                    "events.event AS event",
                    "events__pdi__person.id AS id",
                    "events__pdi__person.properties AS properties",
                    "events__pdi__person.created_at AS created_at",
                ],
            ),
            TestCase(
                PersonsOnEventsMode.PERSON_ID_NO_OVERRIDE_PROPERTIES_ON_EVENTS,
                [
                    "events.event AS event",
                    "events.person_id AS id",
                    "events.person_properties AS properties",
                    "toTimeZone(events.person_created_at, %(torql_val_0)s) AS created_at",
                ],
            ),
            TestCase(
                PersonsOnEventsMode.PERSON_ID_OVERRIDE_PROPERTIES_ON_EVENTS,
                [
                    "events.event AS event",
                    "if(not(empty(events__override.distinct_id)), events__override.person_id, events.person_id) AS id",
                    "events.person_properties AS properties",
                    "toTimeZone(events.person_created_at, %(torql_val_0)s) AS created_at",
                ],
                [
                    "events__override ON equals(events.distinct_id, events__override.distinct_id)",
                ],
            ),
            TestCase(
                PersonsOnEventsMode.PERSON_ID_OVERRIDE_PROPERTIES_JOINED,
                [
                    "events.event AS event",
                    "events__person.id AS id",
                    "events__person.properties AS properties",
                    "events__person.created_at AS created_at",
                ],
                [
                    "events__person ON equals(if(not(empty(events__override.distinct_id)), events__override.person_id, events.person_id), events__person.id)",
                    "events__override ON equals(events.distinct_id, events__override.distinct_id)",
                ],
            ),
        ]

        for test_case in test_cases:
            clickhouse_query = execute_torql_query(
                query,
                team=self.team,
                modifiers=TorQLQueryModifiers(personsOnEventsMode=test_case.mode),
                pretty=False,
            ).clickhouse
            assert clickhouse_query is not None
            assert (
                f"SELECT {', '.join(test_case.expected_columns)} FROM" in clickhouse_query
            ), f"PoE mode: {test_case.mode}"
            for value in test_case.other_expected_values:
                assert value in clickhouse_query

    def test_modifiers_persons_argmax_version_v2(self):
        query = "SELECT * FROM persons"

        # Control (v1)
        response = execute_torql_query(
            query,
            team=self.team,
            modifiers=TorQLQueryModifiers(personsArgMaxVersion=PersonsArgMaxVersion.V1),
        )
        assert "in(tuple(person.id, person.version)" not in response.clickhouse

        # Test (v2)
        response = execute_torql_query(
            query,
            team=self.team,
            modifiers=TorQLQueryModifiers(personsArgMaxVersion=PersonsArgMaxVersion.V2),
        )
        assert "in(tuple(person.id, person.version)" in response.clickhouse

    def test_modifiers_persons_argmax_version_auto(self):
        # Use the v2 query when selecting properties.x
        response = execute_torql_query(
            "SELECT id, properties.$browser, is_identified FROM persons",
            team=self.team,
            modifiers=TorQLQueryModifiers(personsArgMaxVersion=PersonsArgMaxVersion.AUTO),
        )
        assert "in(tuple(person.id, person.version)" in response.clickhouse

        # Use the v2 query when selecting properties
        response = execute_torql_query(
            "SELECT id, properties FROM persons",
            team=self.team,
            modifiers=TorQLQueryModifiers(personsArgMaxVersion=PersonsArgMaxVersion.AUTO),
        )
        assert "in(tuple(person.id, person.version)" in response.clickhouse

        # Use the v1 query when not selecting any properties
        response = execute_torql_query(
            "SELECT id, is_identified FROM persons",
            team=self.team,
            modifiers=TorQLQueryModifiers(personsArgMaxVersion=PersonsArgMaxVersion.AUTO),
        )
        assert "in(tuple(person.id, person.version)" not in response.clickhouse

    def test_modifiers_in_cohort_join(self):
        cohort = Cohort.objects.create(team=self.team, name="test")
        response = execute_torql_query(
            f"select * from persons where id in cohort {cohort.pk}",
            team=self.team,
            modifiers=TorQLQueryModifiers(inCohortVia="subquery"),
        )
        assert "LEFT JOIN" not in response.clickhouse

        # Use the v1 query when not selecting any properties
        response = execute_torql_query(
            f"select * from persons where id in cohort {cohort.pk}",
            team=self.team,
            modifiers=TorQLQueryModifiers(inCohortVia="leftjoin"),
        )
        assert "LEFT JOIN" in response.clickhouse

    def test_modifiers_materialization_mode(self):
        try:
            from ee.clickhouse.materialized_columns.analyze import materialize
        except ModuleNotFoundError:
            # EE not available? Assume we're good
            self.assertEqual(1 + 2, 3)
            return
        materialize("events", "$browser")

        response = execute_torql_query(
            "SELECT properties.$browser FROM events",
            team=self.team,
            modifiers=TorQLQueryModifiers(materializationMode=MaterializationMode.AUTO),
            pretty=False,
        )
        assert (
            "SELECT nullIf(nullIf(events.`mat_$browser`, ''), 'null') AS `$browser` FROM events" in response.clickhouse
        )

        response = execute_torql_query(
            "SELECT properties.$browser FROM events",
            team=self.team,
            modifiers=TorQLQueryModifiers(materializationMode=MaterializationMode.LEGACY_NULL_AS_NULL),
            pretty=False,
        )
        assert (
            "SELECT nullIf(nullIf(events.`mat_$browser`, ''), 'null') AS `$browser` FROM events" in response.clickhouse
        )

        response = execute_torql_query(
            "SELECT properties.$browser FROM events",
            team=self.team,
            modifiers=TorQLQueryModifiers(materializationMode=MaterializationMode.LEGACY_NULL_AS_STRING),
            pretty=False,
        )
        assert "SELECT nullIf(events.`mat_$browser`, '') AS `$browser` FROM events" in response.clickhouse

        response = execute_torql_query(
            "SELECT properties.$browser FROM events",
            team=self.team,
            modifiers=TorQLQueryModifiers(materializationMode=MaterializationMode.DISABLED),
            pretty=False,
        )
        assert (
            "SELECT replaceRegexpAll(nullIf(nullIf(JSONExtractRaw(events.properties, %(torql_val_0)s), ''), 'null'), '^\"|\"$', '') AS `$browser` FROM events"
            in response.clickhouse
        )

    def test_optimize_joined_filters(self):
        # no optimizations
        response = execute_torql_query(
            f"select event from events where person.properties.$browser ilike '%Chrome%'",
            team=self.team,
            modifiers=TorQLQueryModifiers(optimizeJoinedFilters=False),
        )
        # "ilike" shows up once in the response
        assert response is not None
        assert response.clickhouse is not None
        assert response.clickhouse.count("ilike") == 1

        # with optimizations
        response = execute_torql_query(
            f"select event from events where person.properties.$browser ilike '%Chrome%'",
            team=self.team,
            modifiers=TorQLQueryModifiers(optimizeJoinedFilters=True),
        )
        # "ilike" shows up twice in the response
        assert response is not None
        assert response.clickhouse is not None
        assert response.clickhouse.count("ilike") == 2