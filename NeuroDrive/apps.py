from django.apps import AppConfig


class NeurodriveConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "NeuroDrive"

    def ready(self):
        # Import signals when the app is ready
        from . import signals
