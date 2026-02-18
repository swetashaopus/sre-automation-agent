class AnomalyDetector:
    def __init__(self, threshold):
        self.threshold = threshold

    def detect(self, metrics, logs):
        if metrics.get("cpu_usage", 0) > self.threshold:
            return {"type": "CPU_SPIKE", "value": metrics["cpu_usage"]}
        return None
