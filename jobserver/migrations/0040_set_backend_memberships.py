# Generated by Django 3.2.1 on 2021-05-24 13:25

from django.db import migrations


def add_default_memberships(apps, schema_editor):
    Backend = apps.get_model("jobserver", "Backend")
    BackendMembership = apps.get_model("jobserver", "BackendMembership")
    User = apps.get_model("jobserver", "User")

    tpp = Backend.objects.get(name="tpp")

    BackendMembership.objects.bulk_create(
        [BackendMembership(backend=tpp, user=user) for user in User.objects.all()]
    )


def delete_memberships(apps, schema_editor):
    BackendMembership = apps.get_model("jobserver", "BackendMembership")

    BackendMembership.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("jobserver", "0039_add_backend_membership_model"),
    ]

    operations = [
        migrations.RunPython(add_default_memberships, reverse_code=delete_memberships)
    ]
