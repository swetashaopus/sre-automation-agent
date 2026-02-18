class PrometheusClient:
    def __init__(self, settings):
        self.settings = settings

    def fetch_metrics(self):
        return {"cpu_usage": 45}
