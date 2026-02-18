class IncidentManager:
    def __init__(self):
        self.active = set()

    def create(self, anomaly):
        key = str(anomaly)
        if key in self.active:
            return None
        self.active.add(key)
        return anomaly
