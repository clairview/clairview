# Generated by Django 4.2.14 on 2024-08-12 12:04

from django.db import connection, migrations


def insert_stripe_account_schemas(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, team_id FROM clairview_externaldatasource where source_type = 'Stripe'")
        stripe_sources = cursor.fetchall()

    ExternalDataSchema = apps.get_model("clairview", "ExternalDataSchema")
    for source in stripe_sources:
        schema = ExternalDataSchema.objects.create(
            name="Account",
            source_id=source[0],
            team_id=source[1],
            should_sync=False,
            sync_type=None,
            sync_type_config={},
        )
        schema.save()


def reverse(apps, _):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("clairview", "0464_action_pinned_at"),
    ]

    operations = [
        migrations.RunPython(insert_stripe_account_schemas, reverse),
    ]