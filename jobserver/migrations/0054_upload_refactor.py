# Generated by Django 3.2.4 on 2021-07-12 18:21

import uuid

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobserver", "0053_released_file"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="release",
            name="backend_user",
        ),
        migrations.RemoveField(
            model_name="release",
            name="upload_dir",
        ),
        migrations.AddField(
            model_name="release",
            name="requested_files",
            field=models.JSONField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="release",
            name="status",
            field=models.TextField(
                choices=[
                    ("REQUESTED", "Requested"),
                    ("APPROVED", "Approved"),
                    ("REJECTED", "Rejected"),
                ],
                default="REQUESTED",
            ),
        ),
        migrations.AddField(
            model_name="releasefile",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="releasefile",
            name="created_by",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="released_files",
                to="jobserver.user",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="releasefile",
            name="filehash",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="release",
            name="backend",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="releases",
                to="jobserver.backend",
            ),
        ),
        migrations.AlterField(
            model_name="release",
            name="created_by",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="releases",
                to="jobserver.user",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="release",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
