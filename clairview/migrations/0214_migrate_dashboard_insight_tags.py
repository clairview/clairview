# Generated by Django 3.2.5 on 2022-01-28 21:40
from django.db import migrations


def forwards(apps, schema_editor):
    pass


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("clairview", "0213_deprecated_old_tags"),
    ]

    operations = [migrations.RunPython(forwards, reverse, elidable=True)]