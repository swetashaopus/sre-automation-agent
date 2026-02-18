class GrafanaClient:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key

    def get_dashboards(self):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f'{self.url}/api/search', headers=headers)
        response.raise_for_status()
        return response.json()

    def get_dashboard(self, dashboard_uid):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f'{self.url}/api/dashboards/uid/{dashboard_uid}', headers=headers)
        response.raise_for_status()
        return response.json()

    def get_panel_data(self, dashboard_uid, panel_id, from_time, to_time):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        params = {
            'from': from_time,
            'to': to_time,
            'panelId': panel_id
        }
        response = requests.get(f'{self.url}/api/ds/query', headers=headers, params=params)
        response.raise_for_status()
        return response.json()