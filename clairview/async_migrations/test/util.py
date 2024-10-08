from unittest.mock import patch

from clairview.models.async_migration import AsyncMigration, MigrationStatus
from clairview.test.base import BaseTest


class AsyncMigrationBaseTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.patcher = patch("clairviewanalytics.capture")
        self.patcher.start()
        self.addCleanup(self.patcher.stop)


def create_async_migration(
    name="test1",
    description="my desc",
    clairview_min_version="1.0.0",
    clairview_max_version="100000.0.0",
    status=MigrationStatus.NotStarted,
):
    return AsyncMigration.objects.create(
        name=name,
        description=description,
        clairview_min_version=clairview_min_version,
        clairview_max_version=clairview_max_version,
        status=status,
    )
