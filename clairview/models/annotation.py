from typing import Optional

from django.db import models
from django.utils import timezone


class Annotation(models.Model):
    class Scope(models.TextChoices):
        INSIGHT = "dashboard_item", "insight"
        DASHBOARD = "dashboard", "dashboard"
        PROJECT = "project", "project"
        ORGANIZATION = "organization", "organization"

    class CreationType(models.TextChoices):
        USER = "USR", "user"
        GITHUB = "GIT", "GitHub"

    content = models.CharField(max_length=400, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    dashboard_item = models.ForeignKey("clairview.Insight", on_delete=models.SET_NULL, null=True, blank=True)
    dashboard = models.ForeignKey("clairview.Dashboard", on_delete=models.SET_NULL, null=True, blank=True)
    team = models.ForeignKey("clairview.Team", on_delete=models.CASCADE)
    organization = models.ForeignKey("clairview.Organization", on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True)
    scope = models.CharField(max_length=24, choices=Scope.choices, default=Scope.INSIGHT)
    creation_type = models.CharField(max_length=3, choices=CreationType.choices, default=CreationType.USER)
    date_marker = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    # DEPRECATED: replaced by scope
    apply_all = models.BooleanField(null=True)

    @property
    def insight_short_id(self) -> Optional[str]:
        return self.dashboard_item.short_id if self.dashboard_item is not None else None

    @property
    def insight_name(self) -> Optional[str]:
        return self.dashboard_item.name if self.dashboard_item is not None else None

    @property
    def insight_derived_name(self) -> Optional[str]:
        return self.dashboard_item.derived_name if self.dashboard_item is not None else None

    @property
    def dashboard_name(self) -> Optional[str]:
        return self.dashboard.name if self.dashboard is not None else None

    def get_analytics_metadata(self):
        return {"scope": str(self.scope), "date_marker": self.date_marker}