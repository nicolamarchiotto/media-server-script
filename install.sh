#!/bin/bash
echo server install script

./subscripts/ssh.sh
./subscripts/docker_engine.sh

sudo ./subscripts/program_shutdown.sh
docker compose up -d

cat ./README.md
