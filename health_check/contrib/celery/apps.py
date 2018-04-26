from celery import current_app
from django.apps import AppConfig
from django.conf import settings

from health_check.plugins import plugin_dir


class HealthCheckConfig(AppConfig):
    name = 'health_check.contrib.celery'

    def ready(self):
        from .backends import CeleryHealthCheck

        if getattr(settings, 'HEALTHCHECK_FANOUT_BACKENDS', True):
            for queue in current_app.amqp.queues:
                celery_class_name = '{}:{}'.format(CeleryHealthCheck.__name__, queue.title())

                celery_class = type(celery_class_name, (CeleryHealthCheck,), {'queues': [queue]})
                plugin_dir.register(celery_class)
        else:
            celery_class = type(CeleryHealthCheck.__name__, (CeleryHealthCheck,), {'queues': current_app.amqp.queues})
            plugin_dir.register(celery_class)
