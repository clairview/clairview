# Generated by Django 3.2.14 on 2022-07-29 19:19

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clairview", "0253_add_async_migration_parameters"),
    ]

    operations = [
        migrations.CreateModel(
            name="PromptSequenceState",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("key", models.CharField(max_length=400)),
                (
                    "last_updated_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("step", models.IntegerField(default=0)),
                ("completed", models.BooleanField(default=False)),
                ("dismissed", models.BooleanField(default=False)),
                (
                    "person",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="clairview.person"),
                ),
                (
                    "team",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="clairview.team"),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="promptsequencestate",
            constraint=models.UniqueConstraint(
                fields=("team", "person", "key"),
                name="unique sequence key for person for team",
            ),
        ),
    ]