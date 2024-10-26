# Generated by Django 4.2 on 2024-10-26 06:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('NeuroRsa', '0002_recipient_emoji'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='recipient',
            unique_together={('user', 'name')},
        ),
    ]
