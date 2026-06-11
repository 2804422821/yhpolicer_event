from django.apps import AppConfig


class AppDictConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.system.app_init'

    def ready(self):
        import apps.system.app_init.management.commands
