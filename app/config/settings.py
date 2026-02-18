import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    slack_webhook: str = os.getenv("SLACK_WEBHOOK", "")
    anomaly_threshold: int = 80
    polling_interval: int = 5
    demo_mode: bool = True
