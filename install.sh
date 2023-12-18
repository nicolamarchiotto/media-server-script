#!/bin/bash
echo server install script

./subscripts/ssh.sh
./subscripts/docker_engine.sh

sudo ./subscripts/program_shutdown.sh
sudo systemctl daemon-reload

pip install PyYAML
python3 edit_homer_config.py

docker compose up -d

cat ./README.md
