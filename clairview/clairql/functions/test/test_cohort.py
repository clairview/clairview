import pytest
from django.test import override_settings

from clairview.clairql import ast
from clairview.clairql.errors import QueryError
from clairview.clairql.parser import parse_expr
from clairview.clairql.query import execute_clairql_query
from clairview.clairql.test.utils import pretty_print_response_in_tests
from clairview.models import Cohort
from clairview.models.cohort.util import recalculate_cohortpeople
from clairview.models.utils import UUIDT
from clairview.schema import ClairQLQueryModifiers
from clairview.test.base import (
    BaseTest,
    _create_person,
    _create_event,
    flush_persons_and_events,
)

elements_chain_match = lambda x: parse_expr("match(elements_chain, {regex})", {"regex": ast.Constant(value=str(x))})
not_call = lambda x: ast.Call(name="not", args=[x])


class TestCohort(BaseTest):
    maxDiff = None

    def _create_random_events(self) -> str:
        random_uuid = f"RANDOM_TEST_ID::{UUIDT()}"
        _create_person(
            properties={"$os": "Chrome", "random_uuid": random_uuid},
            team=self.team,
            distinct_ids=["bla"],
            is_identified=True,
        )
        _create_event(distinct_id="bla", event=random_uuid, team=self.team)
        flush_persons_and_events()
        return random_uuid

    @pytest.mark.usefixtures("unittest_snapshot")
    @override_settings(PERSON_ON_EVENTS_OVERRIDE=True, PERSON_ON_EVENTS_V2_OVERRIDE=False)
    def test_in_cohort_dynamic(self):
        random_uuid = self._create_random_events()
        cohort = Cohort.objects.create(
            team=self.team,
            groups=[{"properties": [{"key": "$os", "value": "Chrome", "type": "person"}]}],
        )
        recalculate_cohortpeople(cohort, pending_version=0, initiating_user_id=None)
        response = execute_clairql_query(
            f"SELECT event FROM events WHERE person_id IN COHORT {cohort.pk} AND event='{random_uuid}'",
            self.team,
            modifiers=ClairQLQueryModifiers(inCohortVia="subquery"),
            pretty=False,
        )
        assert pretty_print_response_in_tests(response, self.team.pk) == self.snapshot
        self.assertEqual(len(response.results), 1)
        self.assertEqual(response.results[0][0], random_uuid)

    @pytest.mark.usefixtures("unittest_snapshot")
    @override_settings(PERSON_ON_EVENTS_OVERRIDE=True, PERSON_ON_EVENTS_V2_OVERRIDE=False)
    def test_in_cohort_static(self):
        cohort = Cohort.objects.create(
            team=self.team,
            is_static=True,
        )
        response = execute_clairql_query(
            f"SELECT event FROM events WHERE person_id IN COHORT {cohort.pk}",
            self.team,
            modifiers=ClairQLQueryModifiers(inCohortVia="subquery"),
            pretty=False,
        )
        assert pretty_print_response_in_tests(response, self.team.pk) == self.snapshot

    @pytest.mark.usefixtures("unittest_snapshot")
    @override_settings(PERSON_ON_EVENTS_OVERRIDE=True, PERSON_ON_EVENTS_V2_OVERRIDE=False)
    def test_in_cohort_strings(self):
        Cohort.objects.create(
            team=self.team,
            name="my cohort",
            is_static=True,
        )
        response = execute_clairql_query(
            f"SELECT event FROM events WHERE person_id IN COHORT 'my cohort'",
            self.team,
            modifiers=ClairQLQueryModifiers(inCohortVia="subquery"),
            pretty=False,
        )
        assert pretty_print_response_in_tests(response, self.team.pk) == self.snapshot

    @override_settings(PERSON_ON_EVENTS_OVERRIDE=True, PERSON_ON_EVENTS_V2_OVERRIDE=True)
    def test_in_cohort_error(self):
        with self.assertRaises(QueryError) as e:
            execute_clairql_query(f"SELECT event FROM events WHERE person_id IN COHORT true", self.team)
        self.assertEqual(str(e.exception), "cohort() takes exactly one string or integer argument")

        with self.assertRaises(QueryError) as e:
            execute_clairql_query(
                f"SELECT event FROM events WHERE person_id IN COHORT 'blabla'",
                self.team,
            )
        self.assertEqual(str(e.exception), "Could not find a cohort with the name 'blabla'")