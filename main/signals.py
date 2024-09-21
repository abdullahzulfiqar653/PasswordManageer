import os

from django.apps import apps
from django.dispatch import receiver
from django.core.management import call_command
from django.db.models.signals import post_migrate


@receiver(post_migrate, sender=apps.get_app_config("main"))
def load_data_from_fixture(sender, **kwargs):
    fixture_file = os.path.join("main", "fixtures", "subscription_plans_data.json")
    call_command("loaddata", fixture_file, app_label="main")
