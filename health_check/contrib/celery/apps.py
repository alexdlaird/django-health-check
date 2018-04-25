from celery import current_app
from django.apps import AppConfig

from health_check.plugins import plugin_dir


class HealthCheckConfig(AppConfig):
    name = 'health_check.contrib.celery'

    def ready(self):
        from .backends import CeleryBackend

        for queue in current_app.amqp.queues:
            celery_class_name = '{}_{}'.format(CeleryBackend.__class__, queue.title())

            celery_class = type(celery_class_name, (CeleryBackend,), {'queue': queue})
            plugin_dir.register(celery_class)
