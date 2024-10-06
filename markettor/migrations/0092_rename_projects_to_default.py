from django.db import migrations


def forwards_func(apps, schema_editor):
    Team = apps.get_model("markettor", "Team")
    Team.objects.filter(organization__isnull=False).exclude(name__iexact="Hogflix Demo App").update(
        name=Team._meta.get_field("name").get_default()
    )


def reverse_func(apps, schema_editor):
    Team = apps.get_model("markettor", "Team")
    for team in (
        Team.objects.filter(organization__isnull=False)
        .exclude(name__iexact="Hogflix Demo App")
        .select_related("organization")
    ):
        team.name = team.organization.name
        team.save()


class Migration(migrations.Migration):
    dependencies = [
        ("markettor", "0091_messagingrecord"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func, elidable=True),
    ]
