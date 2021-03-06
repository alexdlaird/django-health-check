import json
from urllib.request import urlopen

from django.conf import settings

from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import ServiceUnavailable, ServiceWarning


class TwilioHealthCheck(BaseHealthCheckBackend):
    TWILIO_SUMMARY_URL = 'https://gpkpyklzq55q.statuspage.io/api/v2/summary.json'
    TWILIO_STATUS_URL = 'https://gpkpyklzq55q.statuspage.io/api/v2/status.json'

    def __init__(self):
        super().__init__()
        self.services = getattr(self, 'services', [])

    def check_status(self):
        timeout = getattr(settings, 'HEALTHCHECK_TWILIO_TIMEOUT', 10)

        try:
            if len(self.services) > 0:
                response = urlopen(TwilioHealthCheck.TWILIO_SUMMARY_URL, timeout=timeout)
                data = json.loads(response.read().decode('utf-8'))
                for component in data['components']:
                    if component['name'] in self.services and component['status'] != 'operational':
                        self.add_error(ServiceWarning(
                            '{} - {}'.format(component['name'], component['status'])))
            else:
                response = urlopen(TwilioHealthCheck.TWILIO_STATUS_URL, timeout=timeout)
                data = json.loads(response.read().decode('utf-8'))
                if data['status']['indicator'] != 'none':
                    self.add_error(ServiceWarning(data['status']['indicator']))
        except BaseException as e:
            self.add_error(ServiceUnavailable("Unknown error"), e)
