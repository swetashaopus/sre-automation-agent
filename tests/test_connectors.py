import unittest
from src.connectors.prometheus_client import PrometheusClient
from src.connectors.grafana_client import GrafanaClient
from src.connectors.log_aggregator import LogAggregator

class TestConnectors(unittest.TestCase):

    def setUp(self):
        self.prometheus_client = PrometheusClient()
        self.grafana_client = GrafanaClient()
        self.log_aggregator = LogAggregator()

    def test_prometheus_client_fetch_metrics(self):
        metrics = self.prometheus_client.fetch_metrics()
        self.assertIsInstance(metrics, dict)
        self.assertIn('some_metric', metrics)

    def test_grafana_client_get_dashboards(self):
        dashboards = self.grafana_client.get_dashboards()
        self.assertIsInstance(dashboards, list)
        self.assertGreater(len(dashboards), 0)

    def test_log_aggregator_collect_logs(self):
        logs = self.log_aggregator.collect_logs()
        self.assertIsInstance(logs, list)
        self.assertGreater(len(logs), 0)

if __name__ == '__main__':
    unittest.main()