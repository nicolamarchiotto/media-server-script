import os
import re
import subprocess
from pathlib import Path
from typing import Optional

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-secret-key")

SERVICE_NAME = "mystartup.service"
SCRIPT_PATH = Path("/opt/mystartup.sh")
SERVICE_PATH = Path("/etc/systemd/system/mystartup.service")

SERVICE_UNIT_CONTENT = """[Unit]
Description=Set automatic shutdown
[Service]
Type=oneshot
ExecStart=/opt/mystartup.sh
[Install]
WantedBy=multi-user.target
"""

SHUTDOWN_COMMAND_TEMPLATE = "#!/bin/bash\nsudo shutdown {time}\n"
TIME_PATTERN = re.compile(r"^([01]?\d|2[0-3]):([0-5]\d)$")
SCRIPT_COMMAND_PATTERN = re.compile(r"^\s*sudo\s+shutdown\s+([01]?\d|2[0-3]):([0-5]\d)\s*$")


def run_command(command: list[str], use_sudo: bool = True) -> tuple[str, str, int]:
    if use_sudo and os.geteuid() != 0:
        command = ["sudo"] + command
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def write_text(path: Path, text: str) -> None:
    if os.geteuid() == 0:
        path.write_text(text, encoding="utf-8")
        return

    process = subprocess.run(["sudo", "tee", str(path)], input=text, text=True, capture_output=True)
    if process.returncode != 0:
        raise RuntimeError(process.stderr.strip() or "failed to write file")


def ensure_script_file() -> None:
    if not SCRIPT_PATH.exists():
        write_text(SCRIPT_PATH, SHUTDOWN_COMMAND_TEMPLATE.format(time="01:30"))
        if os.geteuid() == 0:
            SCRIPT_PATH.chmod(0o755)
        else:
            run_command(["chmod", "0755", str(SCRIPT_PATH)])


def ensure_service_file() -> None:
    if not SERVICE_PATH.exists():
        write_text(SERVICE_PATH, SERVICE_UNIT_CONTENT)


def ensure_service_files() -> None:
    ensure_script_file()
    ensure_service_file()


def get_scheduled_time() -> Optional[str]:
    if not SCRIPT_PATH.exists():
        return None

    try:
        content = SCRIPT_PATH.read_text(encoding="utf-8")
    except PermissionError:
        return None

    for line in content.splitlines():
        match = SCRIPT_COMMAND_PATTERN.match(line)
        if match:
            return f"{match.group(1)}:{match.group(2)}"
    return None


def validate_time(value: str) -> bool:
    return TIME_PATTERN.match(value.strip()) is not None


def get_service_status() -> dict[str, Optional[str]]:
    active_out, _, _ = run_command(["systemctl", "is-active", SERVICE_NAME])
    enabled_out, _, _ = run_command(["systemctl", "is-enabled", SERVICE_NAME])
    return {
        "active": (active_out or "inactive").capitalize(),
        "enabled": (enabled_out or "disabled").capitalize(),
    }


def get_service_script_time() -> Optional[str]:
    if not SERVICE_PATH.exists() or not SCRIPT_PATH.exists():
        return None

    return get_scheduled_time()


def get_active_shutdown_time() -> Optional[str]:
    """Get the currently active scheduled shutdown time from systemd."""
    try:
        # Use 'shutdown' command status check - check if a shutdown is scheduled
        # The /run/systemd/shutdown/scheduled file contains shutdown time info
        shutdown_file = Path("/run/systemd/shutdown/scheduled")
        if shutdown_file.exists():
            print("Found active scheduled shutdown.")
            content = shutdown_file.read_text(encoding="utf-8")
            for line in content.splitlines():
                if line.startswith("USEC="):
                    # Extract microseconds since epoch
                    import time
                    usec = int(line.split("=")[1])
                    timestamp = usec / 1_000_000
                    # Convert to HH:MM format
                    time_struct = time.localtime(timestamp)
                    return f"{time_struct.tm_hour:02d}:{time_struct.tm_min:02d}"
        return None
    except Exception:
        return None


def update_shutdown_time(new_time: str) -> None:
    if not validate_time(new_time):
        raise ValueError("Invalid time format")
    script_text = SHUTDOWN_COMMAND_TEMPLATE.format(time=new_time)
    write_text(SCRIPT_PATH, script_text)
    if os.geteuid() == 0:
        SCRIPT_PATH.chmod(0o755)
    else:
        run_command(["chmod", "0755", str(SCRIPT_PATH)])


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    if request.method == "POST":
        action = request.form.get("action", "")
        script_time = request.form.get("script_time", "").strip()
        schedule_time = request.form.get("schedule_time", "").strip()

        try:
            if action == "enable":
                ensure_service_files()
                run_command(["systemctl", "daemon-reload"])
                out, err, code = run_command(["systemctl", "enable", SERVICE_NAME])
                if code == 0:
                    flash("Service enabled successfully.", "success")
                else:
                    flash(err or out or "Failed to enable service.", "danger")
            elif action == "disable":
                out, err, code = run_command(["systemctl", "disable", SERVICE_NAME])
                if code == 0:
                    flash("Service disabled successfully.", "success")
                else:
                    flash(err or out or "Failed to disable service.", "danger")
            elif action == "start":
                ensure_service_files()
                run_command(["systemctl", "daemon-reload"])
                out, err, code = run_command(["systemctl", "start", SERVICE_NAME])
                if code == 0:
                    flash("Service started successfully.", "success")
                else:
                    flash(err or out or "Failed to start service.", "danger")
            elif action == "stop":
                out, err, code = run_command(["systemctl", "stop", SERVICE_NAME])
                if code == 0:
                    flash("Service stopped successfully.", "success")
                else:
                    flash(err or out or "Failed to stop service.", "danger")
            elif action == "cancel":
                out, err, code = run_command(["shutdown", "-c"])
                if code == 0:
                    flash("Pending shutdown canceled successfully.", "success")
                else:
                    flash(err or out or "Failed to cancel pending shutdown.", "danger")
            elif action == "shutdown_in_minute":
                out, err, code = run_command(["shutdown", "+1"])
                if code == 0:
                    flash("System will shutdown in 1 minute.", "success")
                else:
                    flash(err or out or "Failed to schedule shutdown.", "danger")
            elif action == "edit_script":
                script_time = request.form.get("script_time", "").strip()
                if not validate_time(script_time):
                    flash("Enter a valid time in HH:MM format.", "warning")
                else:
                    ensure_service_files()
                    update_shutdown_time(script_time)
                    flash(f"Service shutdown time updated to {script_time}.", "success")
            elif action == "reschedule":
                schedule_time = request.form.get("schedule_time", "").strip()
                if not validate_time(schedule_time):
                    flash("Enter a valid time in HH:MM format.", "warning")
                else:
                    # Cancel current shutdown if scheduled
                    run_command(["shutdown", "-c"])
                    # Schedule new shutdown time
                    out, err, code = run_command(["shutdown", schedule_time])
                    if code == 0:
                        flash(f"Shutdown rescheduled to {schedule_time}.", "success")
                    else:
                        flash(err or out or "Failed to reschedule shutdown.", "danger")
            else:
                flash("Unknown action.", "warning")
        except Exception as exc:
            flash(str(exc), "danger")

        return redirect(url_for("index"))

    # GET request
    status = get_service_status()
    scheduled_time = get_service_script_time() or "None"
    active_shutdown_time = get_active_shutdown_time() or ""
    if request.args.get("canceled"):
        scheduled_time = "None"
        active_shutdown_time = ""
    script_exists = SCRIPT_PATH.exists()
    service_exists = SERVICE_PATH.exists()

    return render_template(
        "index.html",
        status=status,
        scheduled_time=scheduled_time,
        active_shutdown_time=active_shutdown_time,
        script_exists=script_exists,
        service_exists=service_exists,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
