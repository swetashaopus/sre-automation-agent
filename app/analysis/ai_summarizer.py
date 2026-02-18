class AISummarizer:
    def summarize(self, anomaly):
        return (
            f"🚨 High CPU usage detected ({anomaly['value']}%). "
            "Possible causes: traffic surge or heavy workload."
        )
