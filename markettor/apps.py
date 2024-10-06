import os

import markettoranalytics
import structlog
from django.apps import AppConfig
from django.conf import settings
from markettoranalytics.client import Client
from markettoranalytics.exception_capture import Integrations

from markettor.git import get_git_branch, get_git_commit_short
from markettor.settings import SELF_CAPTURE, SKIP_ASYNC_MIGRATIONS_SETUP
from markettor.tasks.tasks import sync_all_organization_available_product_features
from markettor.utils import get_machine_id, get_self_capture_api_token

logger = structlog.get_logger(__name__)


class MarketTorConfig(AppConfig):
    name = "markettor"
    verbose_name = "MarketTor"

    def ready(self):
        markettoranalytics.api_key = "sTMFPsFhdP1Ssg"
        markettoranalytics.personal_api_key = os.environ.get("MARKETTOR_PERSONAL_API_KEY")
        markettoranalytics.poll_interval = 90
        markettoranalytics.enable_exception_autocapture = True
        markettoranalytics.exception_autocapture_integrations = [Integrations.Django]

        if settings.E2E_TESTING:
            markettoranalytics.api_key = "phc_ex7Mnvi4DqeB6xSQoXU1UVPzAmUIpiciRKQQXGGTYQO"
            markettoranalytics.personal_api_key = None
        elif settings.TEST or os.environ.get("OPT_OUT_CAPTURE", False):
            markettoranalytics.disabled = True
        elif settings.DEBUG:
            # log development server launch to markettor
            if os.getenv("RUN_MAIN") == "true":
                # Sync all organization.available_product_features once on launch, in case plans changed
                sync_all_organization_available_product_features()

                # NOTE: This has to be created as a separate client so that the "capture" call doesn't lock in the properties
                phcloud_client = Client(markettoranalytics.api_key)

                phcloud_client.capture(
                    get_machine_id(),
                    "development server launched",
                    {"git_rev": get_git_commit_short(), "git_branch": get_git_branch()},
                )

            local_api_key = get_self_capture_api_token(None)
            if SELF_CAPTURE and local_api_key:
                markettoranalytics.api_key = local_api_key
                markettoranalytics.host = settings.SITE_URL
            else:
                markettoranalytics.disabled = True

        # load feature flag definitions if not already loaded
        if not markettoranalytics.disabled and markettoranalytics.feature_flag_definitions() is None:
            markettoranalytics.load_feature_flags()

        from markettor.async_migrations.setup import setup_async_migrations

        if SKIP_ASYNC_MIGRATIONS_SETUP:
            logger.warning("Skipping async migrations setup. This is unsafe in production!")
        else:
            setup_async_migrations()
