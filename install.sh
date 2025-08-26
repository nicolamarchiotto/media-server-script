#!/bin/bash
echo
echo Server install script
echo

./subscripts/folders.sh


sudo ./subscripts/program_shutdown.sh
sudo systemctl daemon-reload

echo

pip install -q PyYAML

python3 edit_homer_config.py

echo

docker compose up -d