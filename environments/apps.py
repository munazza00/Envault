from django.apps import AppConfig


class EnvironmentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "environments"

    def ready(self):
     import environments.signals