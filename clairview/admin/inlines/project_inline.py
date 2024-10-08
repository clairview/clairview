from django.contrib import admin
from django.utils.html import format_html

from clairview.admin.admins.project_admin import ProjectAdmin
from clairview.models import Project


class ProjectInline(admin.TabularInline):
    extra = 0
    model = Project

    fields = (
        "id",
        "displayed_name",
        "created_at",
    )
    readonly_fields = [*ProjectAdmin.readonly_fields, "displayed_name"]

    def displayed_name(self, project: Project):
        return format_html(
            '<a href="/admin/clairview/project/{}/change/">{}.&nbsp;{}</a>',
            project.pk,
            project.pk,
            project.name,
        )
