# Generated by Django 3.1.12 on 2021-08-06 13:18

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("clairview", "0163_insights_favorited_updatedat_tags"),
    ]

    operations = [
        migrations.RunSQL(
            [
                "SET statement_timeout = 600000000;",
                "CREATE INDEX CONCURRENTLY IF NOT EXISTS clairview_per_team_id_bec4e5_idx ON clairview_person(team_id, id DESC);",
            ],
            reverse_sql='DROP INDEX "clairview_per_team_id_bec4e5_idx";',
        )
    ]