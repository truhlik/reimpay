from django.apps import AppConfig


class CreditConfig(AppConfig):
    name = 'main.apps.credit'

    def ready(self):
        import main.apps.credit.signals.handlers  # noqa

