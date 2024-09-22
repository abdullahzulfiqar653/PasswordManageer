import os

from django.apps import apps
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.management import call_command
from django.db.models.signals import post_migrate, post_save

from main.models.user_profile import UserProfile


@receiver(post_migrate, sender=apps.get_app_config("main"))
def load_data_from_fixture(sender, **kwargs):
    subscription_plans_data = os.path.join(
        "main", "fixtures", "subscription_plans_data.json"
    )
    call_command("loaddata", subscription_plans_data, app_label="main")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
