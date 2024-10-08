import os

import clairviewanalytics
import structlog
from django.apps import AppConfig
from django.conf import settings
from clairviewanalytics.client import Client
from clairviewanalytics.exception_capture import Integrations

from clairview.git import get_git_branch, get_git_commit_short
from clairview.settings import SELF_CAPTURE, SKIP_ASYNC_MIGRATIONS_SETUP
from clairview.tasks.tasks import sync_all_organization_available_product_features
from clairview.utils import get_machine_id, get_self_capture_api_token

logger = structlog.get_logger(__name__)


class ClairViewConfig(AppConfig):
    name = "clairview"
    verbose_name = "ClairView"

    def ready(self):
        clairviewanalytics.api_key = "sTMFPsFhdP1Ssg"
        clairviewanalytics.personal_api_key = os.environ.get("CLAIRVIEW_PERSONAL_API_KEY")
        clairviewanalytics.poll_interval = 90
        clairviewanalytics.enable_exception_autocapture = True
        clairviewanalytics.exception_autocapture_integrations = [Integrations.Django]

        if settings.E2E_TESTING:
            clairviewanalytics.api_key = "phc_ex7Mnvi4DqeB6xSQoXU1UVPzAmUIpiciRKQQXGGTYQO"
            clairviewanalytics.personal_api_key = None
        elif settings.TEST or os.environ.get("OPT_OUT_CAPTURE", False):
            clairviewanalytics.disabled = True
        elif settings.DEBUG:
            # log development server launch to clairview
            if os.getenv("RUN_MAIN") == "true":
                # Sync all organization.available_product_features once on launch, in case plans changed
                sync_all_organization_available_product_features()

                # NOTE: This has to be created as a separate client so that the "capture" call doesn't lock in the properties
                phcloud_client = Client(clairviewanalytics.api_key)

                phcloud_client.capture(
                    get_machine_id(),
                    "development server launched",
                    {"git_rev": get_git_commit_short(), "git_branch": get_git_branch()},
                )

            local_api_key = get_self_capture_api_token(None)
            if SELF_CAPTURE and local_api_key:
                clairviewanalytics.api_key = local_api_key
                clairviewanalytics.host = settings.SITE_URL
            else:
                clairviewanalytics.disabled = True

        # load feature flag definitions if not already loaded
        if not clairviewanalytics.disabled and clairviewanalytics.feature_flag_definitions() is None:
            clairviewanalytics.load_feature_flags()

        from clairview.async_migrations.setup import setup_async_migrations

        if SKIP_ASYNC_MIGRATIONS_SETUP:
            logger.warning("Skipping async migrations setup. This is unsafe in production!")
        else:
            setup_async_migrations()
