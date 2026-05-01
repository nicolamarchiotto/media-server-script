#!/bin/bash
echo
echo Server install script
echo

sudo ./subscripts/program_shutdown.sh
sudo ./program_shutdown_webui/install_flask_service.sh
sudo systemctl daemon-reload

echo

pip install -q PyYAML

python3 edit_homer_config.py

echo

docker compose up -d