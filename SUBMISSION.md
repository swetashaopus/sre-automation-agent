# SRE Autonomous Agent — Submission

## Project

The SRE Autonomous Agent connects monitoring systems and log platforms to detect anomalies, correlate metrics and logs, perform root-cause analysis, and generate incident and health reports delivered by email.

## Team / Author

- Submitter: Sweta Shalini
- Repository: sre-autonomous-agent

## Short Summary

This project implements a lightweight pipeline that ingests metrics and logs, detects behavioral anomalies, correlates signals, and produces human-readable incident reports. It includes connectors for Prometheus and Grafana, analysis modules, and reporting components.

## Key Features

- Behavioral anomaly detection
- Metric-log correlation
- Root cause analysis
- Automated incident and health reporting via email

## Architecture Overview

- `src/connectors` — integrations with Prometheus, Grafana, and log aggregation
- `src/analysis` — anomaly detection, correlation, and root-cause modules
- `src/reporting` — report rendering and notification
- `src/models` / `src/utils` — data models and helpers

## Files of Interest

- Project README: [README.md](README.md)
- Tests: `tests/` (unit tests) and pytest config: [pytest.ini](pytest.ini)
- CI workflow: [.github/workflows/python-tests.yml](.github/workflows/python-tests.yml)
- Dev dependencies: [requirements-dev.txt](requirements-dev.txt)
- Tox config: [tox.ini](tox.ini)

## Installation (local, Windows)

1. Install Python 3.9+ (or use the included Docker setup).
2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Run the Agent (quick)

```powershell
python src\main.py
```

Or use Docker (if Docker is available):

```powershell
docker-compose up --build
```

## Running Tests

Run unit tests with coverage locally:

```powershell
pytest -q
```

Run via `tox`:

```powershell
pip install tox
tox
```

CI: The repository includes a GitHub Actions workflow at [.github/workflows/python-tests.yml](.github/workflows/python-tests.yml) that runs tests on push and PRs.

## Notes & Assumptions

- Integration configuration lives in `src/config/integrations.yaml` and should be populated with valid credentials/endpoints before connecting to external services.
- Email sending is configured in `src/reporting/email_notifier.py`; provide SMTP settings in environment or config.

## How to Evaluate (suggested)

1. Populate `src/config/integrations.yaml` with a local Prometheus endpoint or mock connectors.
2. Run the agent and trigger sample anomalous metrics/logs.
3. Run unit tests with `pytest` to validate analysis components.

## Contact

For questions, contact the submitter in the repository or open an issue.

---

Generated submission document for hackathon submission.
