from django.apps import AppConfig


class AppAmonzeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_amonze'
    def ready(self):
        import app_amonze.signals