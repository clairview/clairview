# Generated by Django 3.0.7 on 2020-08-21 09:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clairview", "0076_auto_20200819_1214"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cohortpeople",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]