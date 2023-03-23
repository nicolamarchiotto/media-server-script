#!/bin/bash
echo server install script

./subscripts/folders.sh
./subscripts/ssh.sh
./subscripts/docker_engine.sh
./subscripts/jellyfin.sh
./subscripts/qbittorrent.sh
./subscripts/sonar.sh
./subscripts/radar.sh
./subscripts/jackett.sh
./subscripts/filebrowser.sh
./subscripts/photoprism.sh

sudo ./subscripts/program_shutdown.sh

cat ./README.md
