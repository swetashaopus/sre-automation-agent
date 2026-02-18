class HealthReporter:
    def __init__(self, metrics, logs):
        self.metrics = metrics
        self.logs = logs

    def generate_health_report(self):
        report = {
            "status": self.evaluate_system_health(),
            "metrics_summary": self.summarize_metrics(),
            "logs_summary": self.summarize_logs(),
        }
        return report

    def evaluate_system_health(self):
        # Implement logic to evaluate system health based on metrics and logs
        return "Healthy"  # Placeholder

    def summarize_metrics(self):
        # Implement logic to summarize metrics
        return {"metric_name": "value"}  # Placeholder

    def summarize_logs(self):
        # Implement logic to summarize logs
        return {"log_level": "count"}  # Placeholder

    def distribute_report(self, email_notifier):
        report = self.generate_health_report()
        email_notifier.send_health_report(report)