class MetricCorrelator:
    def __init__(self, log_aggregator, anomaly_detector):
        self.log_aggregator = log_aggregator
        self.anomaly_detector = anomaly_detector

    def correlate_metrics_with_logs(self, metrics):
        logs = self.log_aggregator.collect_logs()
        correlated_data = []

        for metric in metrics:
            for log in logs:
                if self.is_related(metric, log):
                    correlated_data.append((metric, log))

        return correlated_data

    def is_related(self, metric, log):
        # Implement logic to determine if a metric and log are related
        return metric.name in log.message

    def perform_root_cause_analysis(self, correlated_data):
        root_causers = []
        for metric, log in correlated_data:
            if self.anomaly_detector.detect_anomaly(metric):
                root_causers.append((metric, log))
        
        return root_causers

    def generate_report(self, root_causers):
        report = "Root Cause Analysis Report\n"
        report += "=" * 30 + "\n"
        for metric, log in root_causers:
            report += f"Metric: {metric.name}, Log: {log.message}\n"
        
        return report