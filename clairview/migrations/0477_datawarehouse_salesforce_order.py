# Generated by Django 4.2.15 on 2024-09-17 21:01

from django.db import migrations, connection


def insert_salesforce_order_schemas(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, team_id FROM clairview_externaldatasource where source_type = 'Salesforce'")
        salesforce_sources = cursor.fetchall()

    ExternalDataSchema = apps.get_model("clairview", "ExternalDataSchema")
    for source in salesforce_sources:
        schema = ExternalDataSchema.objects.create(
            name="Order",
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
        ("clairview", "0476_alter_integration_sensitive_config"),
    ]

    operations = [
        migrations.RunPython(insert_salesforce_order_schemas, reverse),
    ]