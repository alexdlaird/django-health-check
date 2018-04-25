from django.db import DatabaseError, IntegrityError

from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import (
    ServiceReturnedUnexpectedResult, ServiceUnavailable
)

from .models import TestModel


class DatabaseBackend(BaseHealthCheckBackend):

    def check_status(self):
        try:
            obj = TestModel.objects.create(title="test")
            obj.title = "newtest"
            obj.save()
            obj.delete()
        except IntegrityError as e:
            self.add_error(ServiceReturnedUnexpectedResult("Integrity error"), e)
        except DatabaseError as e:
            self.add_error(ServiceUnavailable("Database error"), e)
