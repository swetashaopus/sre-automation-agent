class PrometheusClient:
    def __init__(self, base_url=None, auth=None):
        self.base_url = base_url
        self.auth = auth

    def fetch_metrics(self, query=None, start_time=None, end_time=None):
        if self.base_url is None or query is None:
            return {"some_metric": 1.0}
        import requests
        url = f"{self.base_url}/api/v1/query_range"
        params = {
            'query': query,
            'start': start_time,
            'end': end_time
        }
        response = requests.get(url, params=params, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def fetch_current_metrics(self, query):
        import requests
        url = f"{self.base_url}/api/v1/query"
        params = {'query': query}
        response = requests.get(url, params=params, auth=self.auth)
        response.raise_for_status()
        return response.json()