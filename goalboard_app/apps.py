from django.apps import AppConfig


class GoalboardAppConfig(AppConfig):
    name = 'goalboard_app'

    def ready(self):
        import goalboard_app.signals
