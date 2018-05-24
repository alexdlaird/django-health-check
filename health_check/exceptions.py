from django.utils.translation import ugettext_lazy as _


class HealthCheckException(Exception):
    level = 4
    message_type = _("unknown error")
    identifier = _("unknown")

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "%s: %s" % (self.message_type, self.message)


class ServiceWarning(HealthCheckException):
    level = 3
    message_type = _("warning")
    identifier = _("degraded_performance")


class ServiceUnavailable(HealthCheckException):
    level = 1
    message_type = _("unavailable")
    identifier = _("major_outage")


class ServiceReturnedUnexpectedResult(HealthCheckException):
    level = 2
    message_type = _("unexpected result")
    identifier = _("minor_outage")
