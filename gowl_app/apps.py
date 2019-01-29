from django.apps import AppConfig


class GowlAppConfig(AppConfig):
    name = 'gowl_app'

    def ready(self):
        import gowl_app.signals
