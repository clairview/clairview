from unittest.mock import patch

from markettor.models.async_migration import AsyncMigration, MigrationStatus
from markettor.test.base import BaseTest


class AsyncMigrationBaseTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.patcher = patch("markettoranalytics.capture")
        self.patcher.start()
        self.addCleanup(self.patcher.stop)


def create_async_migration(
    name="test1",
    description="my desc",
    markettor_min_version="1.0.0",
    markettor_max_version="100000.0.0",
    status=MigrationStatus.NotStarted,
):
    return AsyncMigration.objects.create(
        name=name,
        description=description,
        markettor_min_version=markettor_min_version,
        markettor_max_version=markettor_max_version,
        status=status,
    )
