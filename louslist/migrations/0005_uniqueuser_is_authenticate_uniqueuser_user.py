# Generated by Django 4.1.1 on 2022-12-06 23:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('louslist', '0004_uniqueuser_times'),
    ]

    operations = [
        migrations.AddField(
            model_name='uniqueuser',
            name='is_authenticate',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='uniqueuser',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]