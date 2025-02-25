# Generated by Django 3.2.1 on 2021-06-03 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobserver", "0040_set_backend_memberships"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="backends",
            field=models.ManyToManyField(
                related_name="backends",
                through="jobserver.BackendMembership",
                to="jobserver.Backend",
            ),
        ),
    ]
