from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("clairview", "0038_migrate_actions_to_precalculate_events"),
    ]

    operations = [
        migrations.RunSQL(
            """
            UPDATE "clairview_event"
            SET properties = properties || jsonb_build_object('$ip', ip)
            WHERE ip IS NOT NULL;
            """,
            "",
            elidable=True,  # This table no longer exists
        )
    ]
