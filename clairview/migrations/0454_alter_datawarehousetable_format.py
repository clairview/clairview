# Generated by Django 4.2.14 on 2024-08-13 10:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clairview", "0453_alter_errortrackinggroup_fingerprint_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datawarehousetable",
            name="format",
            field=models.CharField(
                choices=[
                    ("CSV", "CSV"),
                    ("CSVWithNames", "CSVWithNames"),
                    ("Parquet", "Parquet"),
                    ("JSONEachRow", "JSON"),
                    ("Delta", "Delta"),
                    ("DeltaS3Wrapper", "DeltaS3Wrapper"),
                ],
                max_length=128,
            ),
        ),
    ]