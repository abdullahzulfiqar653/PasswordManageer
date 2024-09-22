from django.apps import AppConfig


class NeuromailConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "NeuroMail"

    def ready(self):
        # Import signals when the app is ready
        from . import signals
