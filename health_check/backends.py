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

    def pretty_status(self, hide_uncritical=False):
        if not hide_uncritical and self.errors:
            return "\n".join(str(e) for e in self.errors)
        return _('working')

    def sensitive_status(self):
        status = _('operational')
        severity = 999
        for error in self.errors:
            if isinstance(error, HealthCheckException) and error.severity < severity:
                severity = error.severity
                status = error.identifier
        return status

    def highest_severity(self):
        severity = 999
        for error in self.errors:
            if isinstance(error, HealthCheckException) and error.severity < severity:
                severity = error.severity
        return severity

    @property
    def status(self):
        return int(not self.errors)

    def identifier(self):
        return self._identifier
