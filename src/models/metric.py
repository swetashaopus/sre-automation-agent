class Metric:
    def __init__(self, name: str, value: float, timestamp: float):
        self.name = name
        self.value = value
        self.timestamp = timestamp

    def __repr__(self):
        return f"Metric(name={self.name}, value={self.value}, timestamp={self.timestamp})"