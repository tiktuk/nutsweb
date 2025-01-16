from django.apps import AppConfig


class NutsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nuts'

    def ready(self):
        from . import checks  # noqa
