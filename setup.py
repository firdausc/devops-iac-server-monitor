import os
import subprocess
import sys
import time
import urllib.request
import webbrowser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PORT = 5000


def log(step, message):
    """Print standard formatted status message."""
    print(f"[STEP {step}] {message}")


def install_dependencies():
    """Install required packages from requirements.txt without manual clicking."""
    log(1, "Verifying and installing dependencies...")
    req_file = os.path.join(BASE_DIR, "requirements.txt")

    if not os.path.exists(req_file):
        print(f"       -> [ERROR] requirements.txt not found at: {req_file}")
        sys.exit(1)

    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", req_file]
        )
        print("       -> Dependencies verified and installed successfully.")
    except subprocess.CalledProcessError as exc:
        print(f"       -> [ERROR] Failed to install dependencies: {exc}")
        sys.exit(1)


def configure_environment():
    """Set up configuration folders, environment files, and system variables."""
    log(2, "Configuring environment, directories, and settings...")

    # 1. Idempotent directory creation
    config_dir = os.path.join(BASE_DIR, "config")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)
        print(f"       -> Created directory: {config_dir}")
    else:
        print(f"       -> Directory already exists: {config_dir} (Skipping creation)")

    # 2. Idempotent configuration file creation
    config_file = os.path.join(config_dir, "config.env")
    if not os.path.exists(config_file):
        with open(config_file, "w", encoding="utf-8") as f:
            f.write(f"PORT={DEFAULT_PORT}\nAPP_NAME=server-monitor\n")
        print(f"       -> Created configuration file: {config_file}")
    else:
        print(f"       -> Configuration file already exists: {config_file} (Preserved)")

    # 3. Set environment variable for execution
    os.environ["PORT"] = str(DEFAULT_PORT)
    print(f"       -> Set environment variable 'PORT' = '{DEFAULT_PORT}'")


def is_app_running(port=DEFAULT_PORT):
    """Check if the server monitor app is already running via its /health endpoint."""
    health_url = f"http://127.0.0.1:{port}/health"
    try:
        with urllib.request.urlopen(health_url, timeout=1.5) as response:
            return response.status == 200
    except Exception:
        return False


def start_application(port=DEFAULT_PORT):
    """Launch app.py in the background if not already running."""
    log(3, "Checking application status...")

    # Idempotency check: prevent duplicate processes
    if is_app_running(port):
        print(f"       -> [NOTICE] Server monitor is already running on port {port}.")
        print("       -> Skipping startup to prevent duplicate instances.")
        webbrowser.open(f"http://127.0.0.1:{port}")
        return

    print("       -> Application is not running. Starting app.py in background...")
    app_script = os.path.join(BASE_DIR, "app.py")
    env = os.environ.copy()
    env["PORT"] = str(port)

    # Launch detached background process on Windows
    # CREATE_NEW_PROCESS_GROUP (0x00000200) allows the app to live independently
    creation_flags = 0x00000200 if os.name == "nt" else 0

    subprocess.Popen(
        [sys.executable, app_script],
        env=env,
        creationflags=creation_flags,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Wait up to 5 seconds for the server to come alive
    print("       -> Waiting for application health check to report OK...")
    for _ in range(10):
        time.sleep(0.5)
        if is_app_running(port):
            print(f"       -> [SUCCESS] Server monitor active at http://127.0.0.1:{port}")
            webbrowser.open(f"http://127.0.0.1:{port}")
            return

    print("       -> [WARNING] App process launched, but health check did not respond yet.")


if __name__ == "__main__":
    print("=" * 65)
    print("  DEVOPS IaC ENVIRONMENT DEPLOYMENT - SERVER MONITOR")
    print("=" * 65)
    install_dependencies()
    configure_environment()
    start_application()
    print("=" * 65)
    print("  SETUP COMPLETE - ALL TASKS FINISHED AUTOMATICALLY")
    print("=" * 65)
