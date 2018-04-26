import logging
from timeit import default_timer as timer

from django.utils.translation import ugettext_lazy as _

from health_check.exceptions import HealthCheckException, ServiceUnavailable, ServiceReturnedUnexpectedResult

logger = logging.getLogger('health-check')


class BaseHealthCheckBackend:
    def __init__(self):
        self.errors = []
        self.critical = getattr(self, 'critical', True)

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

    def pretty_status(self):
        if self.errors:
            return "\n".join(str(e) for e in self.errors)
        return _('working')

    def sensitive_status(self):
        status = _('operational')
        for error in self.errors:
            if isinstance(error, ServiceUnavailable):
                status = 'major_outage'
                break
            elif isinstance(error, ServiceReturnedUnexpectedResult):
                status = 'minor_outage'
            elif status != 'minor_outage':
                status = 'degraded_performance'
        return status

    @property
    def status(self):
        return int(not self.errors)

    def identifier(self):
        return self.__class__.__name__
