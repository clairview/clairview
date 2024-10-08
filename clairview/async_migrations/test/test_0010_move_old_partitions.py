import pytest

from clairview.async_migrations.runner import start_async_migration
from clairview.async_migrations.setup import (
    get_async_migration_definition,
    setup_async_migrations,
)
from clairview.async_migrations.test.util import AsyncMigrationBaseTest
from clairview.models.event.util import create_event
from clairview.models.utils import UUIDT
from clairview.test.base import FuzzyInt

pytestmark = pytest.mark.async_migrations

MIGRATION_NAME = "0010_move_old_partitions"

uuid1, uuid2, uuid3 = (UUIDT() for _ in range(3))


MIGRATION_DEFINITION = get_async_migration_definition(MIGRATION_NAME)


def run_migration():
    setup_async_migrations(ignore_clairview_version=True)
    return start_async_migration(MIGRATION_NAME, ignore_clairview_version=True)


class Test0010MoveOldPartitions(AsyncMigrationBaseTest):
    def setUp(self):
        MIGRATION_DEFINITION.parameters["OLDEST_PARTITION_TO_KEEP"] = (
            "202301",
            "",
            str,
        )
        MIGRATION_DEFINITION.parameters["NEWEST_PARTITION_TO_KEEP"] = (
            "202302",
            "",
            str,
        )
        MIGRATION_DEFINITION.parameters["OPTIMIZE_TABLE"] = (False, "", bool)

        create_event(
            event_uuid=uuid1,
            team=self.team,
            distinct_id="1",
            event="$pageview",
            timestamp="1900-01-02T00:00:00Z",
        )
        create_event(
            event_uuid=uuid2,
            team=self.team,
            distinct_id="1",
            event="$pageview",
            timestamp="2022-02-02T00:00:00Z",
        )
        create_event(
            event_uuid=uuid3,
            team=self.team,
            distinct_id="1",
            event="$pageview",
            timestamp="2045-02-02T00:00:00Z",
        )

        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_completes_successfully(self):
        self.assertTrue(run_migration())

        # this test is not very helpful, but we will at least catch if this changes
        self.assertEqual(len(MIGRATION_DEFINITION.operations), FuzzyInt(5, 6))
