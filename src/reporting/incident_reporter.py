class IncidentReporter:
    def __init__(self, anomaly_data=None, log_data=None):
        self.anomaly_data = anomaly_data or []
        self.log_data = log_data or []

    def generate_report(self):
        report_content = self._format_report()
        return report_content

    def _format_report(self):
        report = "Incident Report\n"
        report += "=" * 50 + "\n"
        report += "Detected Anomalies:\n"
        for anomaly in self.anomaly_data:
            report += f"- {anomaly}\n"
        report += "\nCorrelated Logs:\n"
        for log in self.log_data:
            report += f"- {log}\n"
        return report

    def save_report(self, file_path):
        with open(file_path, 'w') as report_file:
            report_file.write(self.generate_report())

    def send_report(self, email_notifier):
        report_content = self.generate_report()
        email_notifier.send_email("Incident Report", report_content)