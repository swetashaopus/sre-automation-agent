class Incident:
    def __init__(self, timestamp, severity, description):
        self.timestamp = timestamp
        self.severity = severity
        self.description = description

    def __repr__(self):
        return f"Incident(timestamp={self.timestamp}, severity={self.severity}, description={self.description})"