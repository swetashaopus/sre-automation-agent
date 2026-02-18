# SRE Autonomous Agent

The SRE Autonomous Agent is designed to connect monitoring systems (Prometheus, Grafana) and log platforms to continuously detect behavioral anomalies, correlate metrics with logs, perform root cause analysis, and generate comprehensive incident and health reports. These reports are automatically distributed via email to stakeholders.

## Features

- **Behavioral Anomaly Detection**: Utilizes advanced algorithms to identify unusual patterns in metrics.
- **Metric and Log Correlation**: Correlates metrics with logs to pinpoint potential issues.
- **Root Cause Analysis**: Analyzes correlated data to determine the root cause of incidents.
- **Automated Reporting**: Generates incident and health reports and sends them via email to stakeholders.

## Project Structure

```
sre-autonomous-agent
├── src
│   ├── main.py
│   ├── config
│   ├── connectors
│   ├── analysis
│   ├── reporting
│   ├── models
│   ├── utils
│   └── templates
├── tests
├── requirements.txt
├── docker-compose.yml
└── Dockerfile
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd sre-autonomous-agent
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the integration settings in `src/config/integrations.yaml`.

## Usage

To run the SRE Autonomous Agent, execute the following command:
```
python src/main.py
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for discussion.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Running tests

To run tests locally:

```
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest -q
```

Using `tox` (if installed):

```
tox
```

CI: a GitHub Actions workflow is included at `.github/workflows/python-tests.yml` to run tests on push and pull requests.