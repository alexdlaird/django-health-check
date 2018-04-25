from health_check.backends import BaseHealthCheckBackend


class TwilioBackendHealthCheck(BaseHealthCheckBackend):
    def __init__(self):
        super().__init__()
        self.services = getattr(self, 'services', [])

    def check_status(self):
        if len(self.services) > 0:
            'https://gpkpyklzq55q.statuspage.io/api/v2/status.json'
            pass
        else:
            'https://gpkpyklzq55q.statuspage.io/api/v2/summary.json'
            pass
