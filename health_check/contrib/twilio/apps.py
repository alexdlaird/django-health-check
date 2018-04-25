from django.apps import AppConfig

from health_check.plugins import plugin_dir


class HealthCheckConfig(AppConfig):
    name = 'health_check.contrib.twilio'

    def ready(self):
        from .backends import TwilioBackend
        plugin_dir.register(TwilioBackend)
