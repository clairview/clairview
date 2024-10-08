import datetime
from typing import Optional, cast
from zoneinfo import ZoneInfo

from ee.models.license import License, LicenseManager
from clairview.test.base import APIBaseTest


class LicensedTestMixin:
    """
    Test API using Django REST Framework test suite, for licensed ClairView (mainly enterprise edition).
    """

    CONFIG_LICENSE_KEY: Optional[str] = "12345::67890"
    CONFIG_LICENSE_PLAN: Optional[str] = "enterprise"
    license: License = None

    def license_required_response(
        self,
        message: str = "This feature is part of the premium ClairView offering. Self-hosted licenses are no longer available for purchase. Please contact sales@clairview.com to discuss options.",
    ) -> dict[str, Optional[str]]:
        return {
            "type": "server_error",
            "code": "payment_required",
            "detail": message,
            "attr": None,
        }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        if cls.CONFIG_LICENSE_PLAN:
            cls.license = super(LicenseManager, cast(LicenseManager, License.objects)).create(
                key=cls.CONFIG_LICENSE_KEY,
                plan=cls.CONFIG_LICENSE_PLAN,
                valid_until=datetime.datetime(2038, 1, 19, 3, 14, 7, tzinfo=ZoneInfo("UTC")),
            )
            if hasattr(cls, "organization") and cls.organization:
                cls.organization.update_available_product_features()
                cls.organization.save()


class APILicensedTest(LicensedTestMixin, APIBaseTest):
    pass
