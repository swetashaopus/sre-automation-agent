import unittest
from src.reporting.incident_reporter import IncidentReporter
from src.reporting.health_reporter import HealthReporter
from src.reporting.email_notifier import EmailNotifier

class TestReporting(unittest.TestCase):

    def setUp(self):
        self.incident_reporter = IncidentReporter()
        self.health_reporter = HealthReporter()
        self.email_notifier = EmailNotifier()

    def test_generate_incident_report(self):
        report = self.incident_reporter.generate_report()
        self.assertIsNotNone(report)
        self.assertIn("Incident Report", report)

    def test_generate_health_report(self):
        report = self.health_reporter.generate_report()
        self.assertIsNotNone(report)
        self.assertIn("Health Report", report)

    def test_send_email_notification(self):
        result = self.email_notifier.send_notification("test@example.com", "Test Subject", "Test Body")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()