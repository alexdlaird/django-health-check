import json
import urllib.request

from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import ServiceWarning


class TwilioBackendHealthCheck(BaseHealthCheckBackend):
    def __init__(self):
        super().__init__()
        self.services = getattr(self, 'services', [])

    def check_status(self):
        if len(self.services) > 0:
            response = urllib.request.urlopen('https://gpkpyklzq55q.statuspage.io/api/v2/summary.json')
            data = json.loads(response.read().decode('utf-8'))
            for component in data['components']:
                if component['name'] in self.services and component['status'] != 'operational':
                    self.add_error(ServiceWarning(
                        'Twilio service {} returned status {}'.format(component['name'], data['status'])))
        else:
            response = urllib.request.urlopen('https://gpkpyklzq55q.statuspage.io/api/v2/status.json')
            data = json.loads(response.read().decode('utf-8'))
            if data['status']['indicator'] != 'none':
                self.add_error(ServiceWarning(data['status']['indicator']))
