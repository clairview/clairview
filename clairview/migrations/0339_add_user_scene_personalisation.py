# Generated by Django 3.2.19 on 2023-08-02 10:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import clairview.models.utils


class Migration(migrations.Migration):
    dependencies = [
        ("clairview", "0338_datawarehouse_saved_query"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserScenePersonalisation",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=clairview.models.utils.UUIDT,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("scene", models.CharField(max_length=200)),
                (
                    "dashboard",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="clairview.dashboard",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="clairview.team",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="scene_personalisation",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="userscenepersonalisation",
            constraint=models.UniqueConstraint(
                fields=("team", "user", "scene"),
                name="clairview_unique_scene_personalisation",
            ),
        ),
    ]