# Created manually on 2024-04-10 18:46

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ("clairview", "0410_action_steps_population"),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY clairview_eventproperty_team_id_and_property_r32khd9s ON clairview_eventproperty(team_id, property)",
            reverse_sql='DROP INDEX "clairview_eventproperty_team_id_and_property_r32khd9s"',
        ),
    ]
