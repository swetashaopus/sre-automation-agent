import time
import signal
import threading

from config.settings import Settings
from connectors.prometheus_client import PrometheusClient
from connectors.log_aggregator import LogAggregator
from connectors.slack_notifier import SlackNotifier
from analysis.anomaly_detector import AnomalyDetector
from analysis.ai_summarizer import AISummarizer
from incident.incident_manager import IncidentManager
from api.health_server import start_health_server
from utils.logger import logger

def main():
    settings = Settings()

    logger.info("🚀 AI SRE Automation Agent Starting...")

    prometheus = PrometheusClient(settings)
    logs = LogAggregator()
    detector = AnomalyDetector(settings.anomaly_threshold)
    summarizer = AISummarizer()
    incident_manager = IncidentManager()
    slack = SlackNotifier(settings)

    threading.Thread(target=start_health_server, daemon=True).start()

    running = True

    def shutdown_handler(signum, frame):
        nonlocal running
        logger.info("🛑 Graceful shutdown initiated...")
        running = False

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    cycle = 0

    while running:
        try:
            logger.info("🔎 Monitoring cycle started")

            metrics = prometheus.fetch_metrics()
            log_data = logs.collect_logs()

            if settings.demo_mode and cycle == 2:
                logger.warning("🔥 Injecting demo anomaly spike")
                metrics["cpu_usage"] = 97

            anomalies = detector.detect(metrics, log_data)

            if anomalies:
                incident = incident_manager.create(anomalies)
                if incident:
                    summary = summarizer.summarize(anomalies)
                    logger.warning(f"⚠️ Incident Detected: {summary}")
                    slack.send(summary)
                else:
                    logger.info("Duplicate incident ignored.")

            cycle += 1
            time.sleep(settings.polling_interval)

        except Exception:
            logger.exception("Unexpected failure in monitoring loop.")
            time.sleep(5)

    logger.info("✅ Agent shutdown complete.")

if __name__ == "__main__":
    main()
