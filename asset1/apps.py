from django.apps import AppConfig

class Asset1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'asset1'

    def ready(self):
        import asset1.signals
