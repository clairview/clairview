# Generated by Django 4.2.11 on 2024-05-06 09:46

from django.db import migrations, models
import django.db.models.deletion

# NOTE for future readers: This migration handles adding a constraint in a non-blocking way
# Got this by running
# DEBUG=1 python manage.py makemigrations
# then
# DEBUG=1 python manage.py sqlmigrate clairview 0415_pluginconfig_match_action
# which output:
### BEGIN;
### --
### -- Add field match_action to pluginconfig
### --
### ALTER TABLE "clairview_pluginconfig" ADD COLUMN "match_action_id" integer NULL CONSTRAINT "clairview_pluginconfig_match_action_id_1cbf8562_fk_clairview_a" REFERENCES "clairview_action"("id") DEFERRABLE INITIALLY DEFERRED; SET CONSTRAINTS "clairview_pluginconfig_match_action_id_1cbf8562_fk_clairview_a" IMMEDIATE;
### CREATE INDEX "clairview_pluginconfig_match_action_id_1cbf8562" ON "clairview_pluginconfig" ("match_action_id");
### COMMIT;
# and then modify the migration from the below commented version to a safe non-blocking version


# # ORIGINIAL migration
# class Migration(migrations.Migration):
#     dependencies = [
#         ("clairview", "0411_eventproperty_indexes"),
#     ]

#     operations = [
#         migrations.AddField(
#             model_name="pluginconfig",
#             name="match_action",
#             field=models.ForeignKey(
#                 blank=True,
#                 null=True,
#                 on_delete=django.db.models.deletion.SET_NULL,
#                 related_name="plugin_configs",
#                 to="clairview.action",
#             ),
#         ),
#     ]


class Migration(migrations.Migration):
    atomic = False  # Added to support concurrent index creation
    dependencies = [
        ("clairview", "0414_personalapikey_mask_value"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name="pluginconfig",
                    name="match_action",
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="plugin_configs",
                        to="clairview.action",
                    ),
                )
            ],
            database_operations=[
                # We add -- existing-table-constraint-ignore to ignore the constraint validation in CI.
                migrations.RunSQL(
                    """
                    ALTER TABLE "clairview_pluginconfig" ADD COLUMN "match_action_id" integer NULL CONSTRAINT "clairview_pluginconfig_match_action_id_1cbf8562_fk_clairview_a" REFERENCES "clairview_action"("id") DEFERRABLE INITIALLY DEFERRED; -- existing-table-constraint-ignore
                    SET CONSTRAINTS "clairview_pluginconfig_match_action_id_1cbf8562_fk_clairview_a" IMMEDIATE; -- existing-table-constraint-ignore
                    """,
                    reverse_sql="""
                        ALTER TABLE "clairview_pluginconfig" DROP COLUMN IF EXISTS "match_action_id";
                    """,
                ),
                # We add CONCURRENTLY to the create command
                migrations.RunSQL(
                    """
                    CREATE INDEX CONCURRENTLY "clairview_pluginconfig_match_action_id_1cbf8562" ON "clairview_pluginconfig" ("match_action_id");
                    """,
                    reverse_sql="""
                        DROP INDEX IF EXISTS "clairview_pluginconfig_match_action_id_1cbf8562";
                    """,
                ),
            ],
        ),
    ]