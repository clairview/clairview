import os
from pprint import pprint

import markettoranalytics
from django.conf import settings
from django.core.management.base import BaseCommand

from markettor.utils import get_helm_info_env, get_machine_id


class Command(BaseCommand):
    help = "Notify that helm install/upgrade has happened"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", type=bool, help="Print information instead of sending it")

    def handle(self, *args, **options):
        report = get_helm_info_env()
        report["deployment"] = os.getenv("DEPLOYMENT", "unknown")

        print(f"Report for {get_machine_id()}:")
        pprint(report)

        if not options["dry_run"]:
            markettoranalytics.api_key = "sTMFPsFhdP1Ssg"
            disabled = markettoranalytics.disabled
            markettoranalytics.disabled = False
            markettoranalytics.capture(
                get_machine_id(),
                "helm_install",
                report,
                groups={"instance": settings.SITE_URL},
            )
            markettoranalytics.disabled = disabled
