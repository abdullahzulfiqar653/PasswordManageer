import os

from django.apps import apps
from django.dispatch import receiver
from django.core.management import call_command
from django.db.models.signals import post_migrate


@receiver(post_migrate, sender=apps.get_app_config("NeuroMail"))
def load_data_from_fixture(sender, **kwargs):
    email_extensions = os.path.join("NeuroMail", "fixtures", "email_extensions.json")
    ai_templates = os.path.join("NeuroMail", "fixtures", "email_ai_template.json")

    call_command("loaddata", email_extensions, app_label="NeuroMail")
    call_command("loaddata", ai_templates, app_label="NeuroMail")
