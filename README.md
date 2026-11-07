# Cloud Server Monitoring Dashboard — Infrastructure as Code (IaC)

A lightweight, automated DevOps environment deployment and server resource monitoring application built with Python and Flask.

---

## 👥 Team Responsibilities

| Team Member | Role | Key Deliverables & Contributions |
| :--- | :--- | :--- |
| **Member 1** | Application & Testing Lead | • Repository setup & architecture<br>• Core monitoring application (`app.py`)<br>• Dependency specifications (`requirements.txt`)<br>• Automated test suite (`test_app.py`)<br>• Report Section 1 (IaC Theory & Overview) |
| **Member 2** | Automation & Quality Lead | • Automated deployment script (`setup.py`)<br>• Idempotency & background process management<br>• Flake8 style configuration (`.flake8`) & linting<br>• Project documentation (`README.md`)<br>• Report Section 2 (Implementation & Verification) |

---

## 💻 Prerequisites & Environment

* **Target Operating System:** Windows 10 / 11 (tested and verified)
* **Python Version:** Python 3.10 or higher
* **Internet Connection:** Required for first-time package downloads via `pip`

---

##  Quick Start (Automated One-Step Setup)

To provision the environment and launch the monitoring dashboard from a clean machine, open your command prompt/terminal inside the project directory and run:
python setup.py

## What setup.py Automates:
Dependency Resolution: Automatically validates and installs required packages (Flask, psutil, pytest, flake8) from requirements.txt.
Environment Configuration: Safely provisions the config/ directory and writes config/config.env with default runtime settings (PORT=5000).
Application Lifecycle: Launches app.py in the background as an independent detached process and automatically opens your web browser to the dashboard.

## 🔁 Idempotency & Re-running
The deployment script is fully idempotent. Running python setup.py a second time is always safe:
Directory & Config Check: If the config/ folder or config.env file already exists, creation is skipped to prevent overwriting existing settings.
Process Detection: Before attempting to start a process, setup.py queries http://127.0.0.1:5000/health. If the server monitor is already running, it skips launching a duplicate instance and re-opens the browser dashboard.

## 🌐 Application Endpoints
Once deployed, the monitoring application serves the following endpoints:
Endpoint	Method	Description
http://127.0.0.1:5000/	GET	Real-time web dashboard displaying CPU, RAM, and Disk metrics (auto-refreshes every 5s).
http://127.0.0.1:5000/health	GET	Health-check endpoint returning {"status": "ok", "application": "server-monitor"}.
http://127.0.0.1:5000/metrics	GET	Raw system resource metrics formatted as JSON.

## 🧪 Quality Assurance & Testing
1. Code Style Linting (Flake8)
Verify PEP 8 compliance and code quality:
code
Bash
python -m flake8 .
(Passing check produces zero errors/warnings based on .flake8 specifications).
2. Automated Functional Tests (Pytest)
Run the automated test suite against application routes:
code
Bash
python -m pytest

## 🛠️ Key Design Decisions
Detached Background Process: The application is started via subprocess.Popen with detached creation flags so that setup.py can finish execution cleanly and return control to the terminal without blocking.
Health-Check Gating: Instead of brittle process PID lookups, setup.py queries the live /health endpoint to accurately confirm operational readiness.
Configuration Isolation: Operational parameters (PORT) are decoupled from source code into environment variables and config/config.env.

## 🛑 How to Stop the Application
To terminate the background monitoring server on Windows:
code
Cmd
taskkill /F /IM python.exe