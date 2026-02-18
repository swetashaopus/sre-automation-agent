import time
from connectors.prometheus_client import PrometheusClient
from connectors.grafana_client import GrafanaClient
from connectors.log_aggregator import LogAggregator
from analysis.anomaly_detector import AnomalyDetector
from analysis.metric_correlator import MetricCorrelator
from analysis.log_analyzer import LogAnalyzer
from analysis.root_cause_analyzer import RootCauseAnalyzer
from reporting.incident_reporter import IncidentReporter
from reporting.health_reporter import HealthReporter
from reporting.email_notifier import EmailNotifier
from config.settings import Settings

def main():
    settings = Settings()
    
    prometheus_client = PrometheusClient(settings.prometheus)
    grafana_client = GrafanaClient(settings.grafana)
    log_aggregator = LogAggregator(settings.log_sources)
    
    anomaly_detector = AnomalyDetector()
    metric_correlator = MetricCorrelator()
    log_analyzer = LogAnalyzer()
    root_cause_analyzer = RootCauseAnalyzer()
    
    incident_reporter = IncidentReporter()
    health_reporter = HealthReporter()
    email_notifier = EmailNotifier(settings.email)
    
    while True:
        metrics = prometheus_client.fetch_metrics()
        logs = log_aggregator.collect_logs()
        
        anomalies = anomaly_detector.detect(metrics)
        correlated_data = metric_correlator.correlate(metrics, logs)
        root_causes = root_cause_analyzer.analyze(correlated_data)
        
        if anomalies:
            incident_report = incident_reporter.generate(anomalies, root_causes)
            email_notifier.send(incident_report)
        
        health_report = health_reporter.generate(metrics, logs)
        email_notifier.send(health_report)
        
        time.sleep(settings.polling_interval)

if __name__ == "__main__":
    main()