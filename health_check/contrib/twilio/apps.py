from django.apps import AppConfig

from health_check.plugins import plugin_dir


class HealthCheckConfig(AppConfig):
    name = 'health_check.contrib.twilio_storage'

    def ready(self):
        from .backends import TwilioBackend
        plugin_dir.register(TwilioBackend)
