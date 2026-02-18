import requests

class SlackNotifier:
    def __init__(self, settings):
        self.webhook = settings.slack_webhook

    def send(self, message):
        if not self.webhook:
            print("Slack webhook not configured.")
            return
        payload = {"text": message}
        requests.post(self.webhook, json=payload, timeout=5)
