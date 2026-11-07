import os
import platform
from pathlib import Path

import psutil
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <META http-equiv="refresh" content="5">
    <title>Server Monitor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 720px;
            margin: 50px auto;
            padding: 20px;
            background: #f3f6fa;
            color: #182338;
        }
        .card {
            background: white;
            padding: 24px;
            border-radius: 12px;
        }
             .metrics-grid {
         display: grid;
         grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
         gap: 16px;
         margin-top: 24px;
     }
     .metric {
         background: #f3f6fa;
         border-radius: 10px;
         padding: 16px;
     }
     .metric strong {
         display: block;
         font-size: 1.6rem;
         margin: 8px 0;
     }
     .metric progress {
         width: 100%;
         accent-color: #2563eb;
     }
    </style>
</head>
<body>
    <div class="card">
        <h1>Server Monitoring Dashboard</h1>
             <p>Monitoring this {{ metrics.operating_system }} machine.
         Refreshes every 5 seconds.</p>

     <div class="metrics-grid">
         <div class="metric">
             <label for="cpu">CPU usage</label>
             <strong>{{ metrics.cpu_percent }}%</strong>
             <progress id="cpu" value="{{ metrics.cpu_percent }}"
                 max="100"></progress>
         </div>

         <div class="metric">
             <label for="memory">RAM usage</label>
             <strong>{{ metrics.memory_percent }}%</strong>
             <progress id="memory" value="{{ metrics.memory_percent }}"
                 max="100"></progress>
         </div>

         <div class="metric">
             <label for="disk">Disk usage</label>
             <strong>{{ metrics.disk_percent }}%</strong>
             <progress id="disk" value="{{ metrics.disk_percent }}"
                 max="100"></progress>
         </div>
     </div>
    </div>
</body>
</html>
"""


def get_metrics():
    """Read resource usage from the machine running this application."""
    system_drive = Path.home().anchor
    return {
        "operating_system": platform.system(),
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage(system_drive).percent,
    }


@app.get("/")
def dashboard():
    """Display the monitoring dashboard."""
    return render_template_string(PAGE, metrics=get_metrics())


@app.get("/metrics")
def metrics():
    """Return monitoring data as JSON."""
    return jsonify(get_metrics())


@app.get("/health")
def health():
    """Provide a simple application health check."""
    return jsonify({"status": "ok", "application": "server-monitor"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=False)
