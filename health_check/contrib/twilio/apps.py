from django.apps import AppConfig
from django.conf import settings

from health_check.plugins import plugin_dir


class HealthCheckConfig(AppConfig):
    name = 'health_check.contrib.twilio'

    def ready(self):
        from .backends import TwilioBackend

        if getattr(settings, 'HEALTHCHECK_FANOUT_BACKENDS', True):
            for service in getattr(settings, 'HEALTHCHECK_TWILIO_SERVICES', ['SMS', 'Phone Numbers']):
                celery_class_name = '{}:{}'.format(TwilioBackend.__name__, service.replace(' ', ''))

                celery_class = type(celery_class_name, (TwilioBackend,), {'queues': [service]})
                plugin_dir.register(celery_class)
        else:
            plugin_dir.register(TwilioBackend)

