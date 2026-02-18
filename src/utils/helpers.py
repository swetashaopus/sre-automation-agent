def calculate_average(values):
    if not values:
        return 0
    return sum(values) / len(values)

def format_timestamp(timestamp):
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def extract_error_messages(log_entries):
    return [entry.message for entry in log_entries if entry.level == 'ERROR']

def is_anomaly_detected(metric_value, threshold):
    return metric_value > threshold

def generate_report_summary(incident_count, health_status):
    return {
        'incident_count': incident_count,
        'health_status': health_status
    }