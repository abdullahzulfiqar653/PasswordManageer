# Generated by Django 4.2 on 2025-02-05 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_remove_userprofile_image_userprofile_image_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="address",
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
