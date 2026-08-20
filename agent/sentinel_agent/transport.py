import random
import time
import requests

class EventTransport:
    def __init__(self, base_url, token, max_attempts=5):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.max_attempts = max_attempts

    def send(self, event):
        delay = 1.0
        headers = {"X-Sentinel-Agent-Token": self.token}
        for attempt in range(self.max_attempts):
            try:
                response = requests.post(
                    self.base_url + "/api/v1/events",
                    json=event,
                    headers=headers,
                    timeout=10,
                )
                response.raise_for_status()
                return response.json()
            except requests.RequestException:
                if attempt == self.max_attempts - 1:
                    raise
                time.sleep(min(delay + random.random(), 30))
                delay *= 2
