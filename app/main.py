
import json
import time
from pathlib import Path

print("🚀 AI SRE Automation Agent (Corporate Demo Mode)")

data_file = Path(__file__).resolve().parent.parent / "demo" / "test_metrics.json"

with open(data_file) as f:
    test_data = json.load(f)

print("📊 Loaded Test Dataset")

# Process normal cycles
for entry in test_data["normal_cycle"]:
    print(f"✅ Normal Metrics | CPU: {entry['cpu_usage']}% | Memory: {entry['memory_usage']}%")
    time.sleep(1)

# Process anomaly cycle
for entry in test_data["anomaly_cycle"]:
    print(f"🔥 Anomaly Metrics | CPU: {entry['cpu_usage']}% | Memory: {entry['memory_usage']}%")
    time.sleep(1)
    
    if entry["cpu_usage"] > 80:
        print("⚠️ INCIDENT DETECTED")
        print(f"🧠 AI Summary: High CPU spike ({entry['cpu_usage']}%). Likely traffic surge or heavy workload.")
        print("📨 Slack Alert Sent (Simulated)")
        time.sleep(1)

print("✅ Demo completed successfully")
