# Generated by Django 3.2.18 on 2023-06-21 14:40

from django.db import migrations, models

# mypy fails here because we're using such an old version
# error: Module "django.contrib.postgres.operations" has no attribute "AddIndexConcurrently"
# but that's not true
from django.contrib.postgres.operations import AddIndexConcurrently


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("clairview", "0330_add_autocapture_exceptions_events_to_ignore"),
    ]

    operations = [
        AddIndexConcurrently(
            model_name="propertydefinition",
            index=models.Index(
                fields=["team_id", "type", "is_numerical"],
                name="clairview_pro_team_id_eac36d_idx",
            ),
        ),
    ]