# SRE Automation Agent

A Python-based Site Reliability Engineering (SRE) automation agent that monitors system health, detects issues, and generates alerts and reports.

## Features

- **System Monitoring**
  - CPU usage monitoring with configurable thresholds
  - Memory usage tracking
  - Disk space monitoring for all partitions
  - Process and service monitoring

- **Automated Alerting**
  - Threshold-based alert generation
  - Configurable severity levels
  - Alert history tracking
  - Extensible alert delivery methods

- **Reporting**
  - Real-time system status summaries
  - JSON and text report generation
  - Historical alert tracking
  - Overall system health status

- **Flexible Configuration**
  - YAML-based configuration
  - Environment variable support
  - Runtime parameter overrides
  - Easy customization of thresholds and intervals

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the agent once and display a report:

```bash
python agent.py --once
```

### Continuous Monitoring

Run the agent in continuous mode (checks every 60 seconds by default):

```bash
python agent.py
```

### Generate Reports

Run checks and save reports to files:

```bash
python agent.py --report
```

### Custom Configuration

Use a custom configuration file:

```bash
python agent.py --config /path/to/config.yaml
```

### Command-Line Options

- `-c, --config PATH` - Path to configuration file
- `-o, --once` - Run checks once and exit
- `-r, --report` - Generate and save report files

## Configuration

The agent uses a YAML configuration file (`config.yaml`) with the following structure:

```yaml
monitoring:
  interval_seconds: 60      # Check interval
  cpu_threshold: 80         # CPU alert threshold (%)
  memory_threshold: 85      # Memory alert threshold (%)
  disk_threshold: 90        # Disk alert threshold (%)

alerts:
  enabled: true
  methods:
    - log                   # Alert delivery methods

logging:
  level: INFO              # Log level
  file: sre_agent.log      # Log file path

services:                  # Optional service monitoring
  - name: nginx
  - name: python
```

### Configuration Options

#### Monitoring Settings

- `interval_seconds`: How often to run checks (default: 60)
- `cpu_threshold`: CPU usage percentage to trigger alerts (default: 80)
- `memory_threshold`: Memory usage percentage to trigger alerts (default: 85)
- `disk_threshold`: Disk usage percentage to trigger alerts (default: 90)

#### Alert Settings

- `enabled`: Enable/disable alerting (default: true)
- `methods`: List of alert delivery methods (currently supports: log)

#### Logging Settings

- `level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `file`: Path to log file

#### Service Monitoring

Add services to monitor by listing them under the `services` section:

```yaml
services:
  - name: nginx
  - name: postgresql
  - name: redis
```

## Examples

### Example 1: Quick Health Check

```bash
python agent.py --once
```

Output:
```
==================================================
SRE Automation Agent - System Report
==================================================
Timestamp: 2026-02-18T07:43:21.931Z
Overall Status: HEALTHY

CPU:
  Usage: 15.20%
  Status: healthy
  Threshold: 80%

Memory:
  Usage: 45.30%
  Status: healthy
  Threshold: 85%

Disk:
  /:
    Usage: 62.10%
    Status: healthy
    Threshold: 90%
==================================================
```

### Example 2: Continuous Monitoring

```bash
python agent.py
```

The agent will run continuously, checking system health every 60 seconds and logging alerts when thresholds are exceeded.

### Example 3: Generate Reports

```bash
python agent.py --report
```

This will generate two report files:
- `sre_report_YYYYMMDD_HHMMSS.json` - JSON format report
- `sre_report_YYYYMMDD_HHMMSS.txt` - Human-readable text report

## Architecture

The SRE Automation Agent consists of several modules:

- **agent.py** - Main agent orchestrator
- **config.py** - Configuration management
- **monitor.py** - System and service monitoring
- **alerts.py** - Alert generation and management
- **report.py** - Report generation and formatting

## Extending the Agent

### Adding New Alert Methods

To add new alert delivery methods (e.g., email, Slack), extend the `AlertManager` class in `alerts.py`:

```python
def _send_email_alert(self, alert: Dict[str, Any]):
    # Implement email sending logic
    pass
```

### Adding Custom Metrics

To add custom metrics, extend the `SystemMonitor` or create a new monitor class in `monitor.py`.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License - feel free to use this agent in your projects.

## Author

Created for SRE automation and system monitoring purposes.
