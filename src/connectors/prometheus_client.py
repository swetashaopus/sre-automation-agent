from typing import Optional
import requests



class PrometheusClient:
    def __init__(
        self,
        base_url: str = "http://localhost:9090",
        session: Optional[requests.Session] = None,
        timeout: float = 10.0,
    ):
        self.base_url = base_url
        self.session = session or requests.Session()
        self.timeout = timeout


    def fetch_metrics(self, query, start_time=None, end_time=None):
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
