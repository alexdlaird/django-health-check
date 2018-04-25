from django.apps import AppConfig

from health_check.plugins import plugin_dir


class HealthCheckConfig(AppConfig):
    name = 'health_check.storage'

    def ready(self):
        from .backends import DefaultFileStorageBackend
        plugin_dir.register(DefaultFileStorageBackend)
