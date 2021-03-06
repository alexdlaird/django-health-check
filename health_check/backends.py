import logging
from timeit import default_timer as timer

from django.utils.translation import ugettext_lazy as _

from health_check.exceptions import HealthCheckException

logger = logging.getLogger('health-check')


class BaseHealthCheckBackend:
    critical = True
    description = ''

    def __init__(self):
        self._identifier = self.__class__.__name__

        self.errors = []
        self.severity = HealthCheckException.level, HealthCheckException.identifier

    def check_status(self):
        raise NotImplementedError

    def run_check(self):
        start = timer()
        self.errors = []
        try:
            self.check_status()
        except HealthCheckException as e:
            self.add_error(e, e)
        except BaseException:
            logger.exception("Unexpected Error!")
            raise
        finally:
            self.time_taken = timer() - start

    def add_error(self, error, cause=None):
        if isinstance(error, HealthCheckException):
            pass
        elif isinstance(error, str):
            msg = error
            error = HealthCheckException(msg)
        else:
            msg = _("unknown error")
            error = HealthCheckException(msg)
        if isinstance(cause, BaseException):
            logger.exception(str(error))
        else:
            logger.error(str(error))
        self.errors.append(error)

        if error.level < self.severity[0]:
            self.severity = error.level, error.identifier

    def pretty_status(self):
        if self.errors:
            return "\n".join(str(e) for e in self.errors)
        return _('working')

    @property
    def status(self):
        return int(not self.errors)

    def identifier(self):
        return self._identifier
