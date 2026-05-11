#!/bin/bash

set -e

echo "🚀 Installing Flask systemd service..."

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SERVICE_NAME="flask-shutdown.service"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}"

VENV_DIR="$APP_DIR/venv"
PYTHON_BIN="$VENV_DIR/bin/python"

echo "📁 App directory:"
echo "   $APP_DIR"

# --------------------------------------------------
# CHECK FILES
# --------------------------------------------------
if [ ! -f "$APP_DIR/app.py" ]; then
    echo "❌ app.py not found"
    exit 1
fi

if [ ! -f "$APP_DIR/.env" ]; then
    echo "❌ .env file not found"
    exit 1
fi

if [ ! -x "$PYTHON_BIN" ]; then
    echo "❌ Virtualenv python not found:"
    echo "   $PYTHON_BIN"
    exit 1
fi

# --------------------------------------------------
# CREATE SYSTEMD SERVICE
# --------------------------------------------------
echo "⚙️ Creating systemd service..."

sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=Flask Shutdown App
After=network.target

[Service]
Type=simple
User=root

WorkingDirectory=$APP_DIR

EnvironmentFile=$APP_DIR/.env
Environment=PYTHONUNBUFFERED=1

ExecStart=$PYTHON_BIN $APP_DIR/app.py

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# --------------------------------------------------
# RELOAD SYSTEMD
# --------------------------------------------------
echo "🔄 Reloading systemd..."

sudo systemctl daemon-reload

# --------------------------------------------------
# ENABLE SERVICE
# --------------------------------------------------
echo "🚀 Enabling service..."

sudo systemctl enable "$SERVICE_NAME"

# --------------------------------------------------
# START SERVICE
# --------------------------------------------------
echo "▶️ Starting service..."

sudo systemctl restart "$SERVICE_NAME"

sleep 2

# --------------------------------------------------
# STATUS
# --------------------------------------------------
echo ""
echo "📊 Service status:"
systemctl status "$SERVICE_NAME" --no-pager