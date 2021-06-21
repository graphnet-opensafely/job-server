# Generated by Django 3.2.4 on 2021-06-11 10:28

from django.db import migrations


def set_is_active(apps, schema_editor):
    Backend = apps.get_model("jobserver", "Backend")

    Backend.objects.filter(name__in=["emis", "tpp"]).update(is_active=True)


def unset_is_active(apps, schema_editor):
    Backend = apps.get_model("jobserver", "Backend")

    Backend.objects.update(is_active=True)


class Migration(migrations.Migration):

    dependencies = [
        ("jobserver", "0042_add_backend_is_active"),
    ]

    operations = [migrations.RunPython(set_is_active, reverse_code=unset_is_active)]