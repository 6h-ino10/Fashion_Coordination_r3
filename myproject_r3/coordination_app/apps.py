from django.apps import AppConfig


class Coordination_appConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coordination_app'

    def ready(self):
        import users.signals
