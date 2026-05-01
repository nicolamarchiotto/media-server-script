#!/bin/bash

echo "Starting Flask service installation..."

set -e

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="flask-shutdown.service"
ENV_FILE="/etc/flask-shutdown.env"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}"

echo "📄 Creating environment file..."
sudo tee "$ENV_FILE" > /dev/null << 'EOF'
FLASK_SECRET_KEY=change-me-to-a-strong-secret
EOF

sudo chmod 600 "$ENV_FILE"

echo "⚙️ Creating systemd service..."
sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=Flask Shutdown App
After=network.target

[Service]
Type=simple
User=hp
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/python3 $APP_DIR/app.py
Restart=always
EnvironmentFile=$ENV_FILE
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload

echo "🚀 Enabling service..."
sudo systemctl enable "$SERVICE_NAME"

echo "▶️ Starting service..."
sudo systemctl restart "$SERVICE_NAME"

echo "✅ Done!"
echo "📊 Status:"
systemctl status "$SERVICE_NAME" --no-pager