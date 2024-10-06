# Created manually on 2024-04-10 18:46

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ("markettor", "0410_action_steps_population"),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY markettor_eventproperty_team_id_and_property_r32khd9s ON markettor_eventproperty(team_id, property)",
            reverse_sql='DROP INDEX "markettor_eventproperty_team_id_and_property_r32khd9s"',
        ),
    ]
