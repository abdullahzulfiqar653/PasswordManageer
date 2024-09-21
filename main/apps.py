from django.apps import AppConfig


class MainConfig(AppConfig):
    name = "main"

    def ready(self):
        # Import signals when the app is ready
        from . import signals
