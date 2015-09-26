# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations

def create_superadmin(apps, schema_editor):
    # at time of writing, create_superuser() fails
    # on migration's serialized user model (dj17, dj18, dj19)
    from django.contrib.auth import get_user_model
    get_user_model().objects.create_superuser(username=settings.SUPERUSER_USERNAME, email=settings.SUPERUSER_EMAIL, password=settings.SUPERUSER_PASSWORD)

class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL)
    ]
    operations = [
        migrations.RunPython(create_superadmin),
    ]
