# Generated by Django 3.2.15 on 2022-12-01 13:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clairview", "0281_create_insight_caching_state_model"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="insightcachingstate",
            name="last_refresh_queued_at",
        ),
        migrations.AddField(
            model_name="insightcachingstate",
            name="last_refresh_queued_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RemoveConstraint(
            model_name="insightcachingstate",
            name="unique_insight_for_caching_state_idx",
        ),
        migrations.AddConstraint(
            model_name="insightcachingstate",
            constraint=models.UniqueConstraint(
                condition=models.Q(("dashboard_tile__isnull", True)),
                fields=("insight",),
                name="unique_insight_for_caching_state_idx",
            ),
        ),
        migrations.AlterField(
            model_name="insightcachingstate",
            name="dashboard_tile",
            field=models.ForeignKey(
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="caching_states",
                to="clairview.dashboardtile",
            ),
        ),
        migrations.AlterField(
            model_name="insightcachingstate",
            name="insight",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="caching_states",
                to="clairview.insight",
            ),
        ),
    ]