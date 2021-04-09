# Generated by Django 3.1.6 on 2021-04-01 09:58

from django.db import migrations

import jobserver.fields


class Migration(migrations.Migration):

    dependencies = [
        ("jobserver", "0025_add_jobrequest_project_definition"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="roles",
            field=jobserver.fields.RolesField(default=list),
        ),
    ]