from datetime import datetime
import os
import re
import subprocess
from functools import wraps
from pathlib import Path
from typing import Optional
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)

from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)


# Load .env file
load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Read credentials from .env

APP_USERNAME = os.environ.get("APP_USERNAME")
APP_PASSWORD = os.environ.get("APP_PASSWORD")

SERVICE_NAME = "mystartup.service"
SCRIPT_PATH = Path("/opt/mystartup.sh")

# ------------------------------------------------------------
# USER MODEL
# ------------------------------------------------------------
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    if user_id == APP_USERNAME:
        return User(user_id)
    return None

# ------------------------------------------------------------
# VALIDATION
# ------------------------------------------------------------
TIME_PATTERN = re.compile(r"^([01]?\d|2[0-3]):([0-5]\d)$")
SCRIPT_TIME_PATTERN = re.compile(r"shutdown\s+([01]?\d|2[0-3]):([0-5]\d)")

# ------------------------------------------------------------
# COMMAND RUNNER
# ------------------------------------------------------------
def run_command(command: list[str], input_text: str = None) -> tuple[str, str, int]:
    result = subprocess.run(
        command,
        input=input_text,
        text=True,
        capture_output=True
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


# ------------------------------------------------------------
# SCRIPT HANDLING (/opt/mystartup.sh)
# ------------------------------------------------------------
def get_script_shutdown_time() -> str:
    if not SCRIPT_PATH.exists():
        return ""

    content = SCRIPT_PATH.read_text()
    match = SCRIPT_TIME_PATTERN.search(content)

    if match:
        return f"{match.group(1)}:{match.group(2)}"

    return ""


def update_script_shutdown_time(time_str: str) -> None:
    if not TIME_PATTERN.match(time_str):
        raise ValueError("Invalid time format")

    SCRIPT_PATH.write_text(
        f"#!/bin/bash\nshutdown {time_str}\n"
    )
    SCRIPT_PATH.chmod(0o755)


def shutdown_in_one_minute():
    return run_command(["sudo", "shutdown", "+1"])

# ------------------------------------------------------------
# AT SCHEDULER (HH:MM)
# ------------------------------------------------------------
def schedule_shutdown_at(time_str: str) -> tuple[str, str, int]:
    cancel_all_shutdowns()
    return run_command(["sudo", "shutdown", "-h", time_str])

def cancel_all_shutdowns() -> None:
    run_command(["shutdown", "-c"])

def reboot_in_a_minute():
    cancel_all_shutdowns()
    return run_command(["sudo", "shutdown", "-r", "+1"])

# ------------------------------------------------------------
# VALIDATION
# ------------------------------------------------------------
def validate_time(value: str) -> bool:
    return TIME_PATTERN.match(value.strip()) is not None


# ------------------------------------------------------------
# SERVICE STATUS
# ------------------------------------------------------------
def get_service_status() -> dict[str, str]:
    active_out, _, _ = run_command(["systemctl", "is-active", SERVICE_NAME])
    enabled_out, _, _ = run_command(["systemctl", "is-enabled", SERVICE_NAME])

    return {
        "active": active_out or "inactive",
        "enabled": enabled_out or "disabled",
    }


# ------------------------------------------------------------
# ACTIVE SHUTDOWN
# ------------------------------------------------------------
def get_active_shutdown_time() -> Optional[str]:
    try:
        with open("/run/systemd/shutdown/scheduled", "r") as f:
            lines = f.readlines()

        usec = None

        for line in lines:
            if line.startswith("USEC="):
                usec = int(line.split("=", 1)[1].strip())
                break

        if usec is None:
            return None

        # systemd stores time in microseconds
        shutdown_dt = datetime.fromtimestamp(usec / 1_000_000)

        # return HH:MM format
        return shutdown_dt.strftime("%H:%M")

    except Exception:
        return None
    
def get_scheduled_reboot_time() -> Optional[str]:
    try:
        with open("/run/systemd/shutdown/scheduled", "r") as f:
            lines = f.readlines()

        usec = None
        mode = None

        for line in lines:
            if line.startswith("USEC="):
                usec = int(line.split("=", 1)[1].strip())
            elif line.startswith("MODE="):
                mode = line.split("=", 1)[1].strip()

        if usec is None or mode != "reboot":
            return None

        dt = datetime.fromtimestamp(usec / 1_000_000)
        return dt.strftime("%H:%M")

    except Exception:
        return None
    
def get_scheduled_reboot_time_full() -> Optional[str]:
    try:
        with open("/run/systemd/shutdown/scheduled", "r") as f:
            lines = f.readlines()

        usec = None
        mode = None

        for line in lines:
            if line.startswith("USEC="):
                usec = int(line.split("=", 1)[1].strip())
            elif line.startswith("MODE="):
                mode = line.split("=", 1)[1].strip()

        if usec is None or mode != "reboot":
            return None

        dt = datetime.fromtimestamp(usec / 1_000_000)

        # IMPORTANT: return full datetime format systemd understands better
        return dt.strftime("%H:%M")

    except Exception:
        return None

# ------------------------------------------------------------
# LOGIN
# ------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == APP_USERNAME and password == APP_PASSWORD:
            user = User(username)
            login_user(user)

            flash("Login successful", "success")
            return redirect(url_for("index"))

        flash("Invalid username or password", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "success")
    return redirect(url_for("login"))

# ------------------------------------------------------------
# FLASK ROUTES
# ------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        action = request.form.get("action", "")

        try:
            # ---------------- ENABLE ----------------
            if action == "enable":
                run_command(["systemctl", "daemon-reload"])
                out, err, code = run_command(["systemctl", "enable", SERVICE_NAME])

                flash("Service enabled" if code == 0 else err,
                      "success" if code == 0 else "danger")

            # ---------------- DISABLE ----------------
            elif action == "disable":
                out, err, code = run_command(["systemctl", "disable", SERVICE_NAME])

                flash("Service disabled" if code == 0 else err,
                      "success" if code == 0 else "danger")

            # ---------------- START ----------------
            elif action == "start":
                run_command(["systemctl", "daemon-reload"])
                out, err, code = run_command(["systemctl", "start", SERVICE_NAME])

                flash("Service started" if code == 0 else err,
                      "success" if code == 0 else "danger")

            # ---------------- STOP ----------------
            elif action == "stop":
                out, err, code = run_command(["systemctl", "stop", SERVICE_NAME])

                flash("Service stopped" if code == 0 else err,
                      "success" if code == 0 else "danger")

            # ---------------- CANCEL ALL ----------------
            elif action == "cancel":
                cancel_all_shutdowns()
                flash("All shutdowns canceled", "success")

            # ---------------- 🔥 1 MINUTE SHUTDOWN ----------------
            elif action == "shutdown_in_minute":
                out, err, code = shutdown_in_one_minute()

                flash(
                    "Shutdown in 1 minute scheduled" if code == 0 else err,
                    "success" if code == 0 else "danger"
                )

            # ---------------- RESCHEDULE (AT HH:MM) ----------------
            elif action == "reschedule":
                schedule_time = request.form.get("schedule_time", "").strip()

                if validate_time(schedule_time):
                    out, err, code = schedule_shutdown_at(schedule_time)

                    flash(
                        f"Shutdown scheduled at {schedule_time}" if code == 0 else err,
                        "success" if code == 0 else "danger"
                    )
                else:
                    flash("Invalid time format", "warning")


            # ---------------- REBOOT IN A MINUTE ----------------
            elif action == "reboot_in_a_minute":
                reboot_in_a_minute()
                flash("Reboot in a minute", "success")

            # ---------------- EDIT SCRIPT ----------------
            elif action == "edit_script":
                script_time = request.form.get("script_time", "").strip()

                if validate_time(script_time):
                    update_script_shutdown_time(script_time)
                    flash(f"Script updated to {script_time}", "success")
                else:
                    flash("Invalid time format", "warning")

        except Exception as e:
            flash(str(e), "danger")

        return redirect(url_for("index"))

    # ---------------- GET ----------------
    status = get_service_status()
    active_shutdown_time = get_active_shutdown_time()
    active_reboot_time = get_scheduled_reboot_time()
    scheduled_time = get_script_shutdown_time()

    return render_template(
        "index.html",
        status=status,
        active_shutdown_time=active_shutdown_time,
        active_reboot_time=active_reboot_time,
        scheduled_time=scheduled_time
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)