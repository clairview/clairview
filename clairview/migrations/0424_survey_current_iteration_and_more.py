# Generated by Django 4.2.11 on 2024-06-06 14:54

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clairview", "0423_alter_externaldatasource_source_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="survey",
            name="current_iteration",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name="survey",
            name="current_iteration_start_date",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="survey",
            name="iteration_count",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name="survey",
            name="iteration_frequency_days",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name="survey",
            name="iteration_start_dates",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.DateTimeField(null=True), blank=True, default=None, null=True, size=None
            ),
        ),
    ]