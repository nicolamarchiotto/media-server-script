#!/bin/bash
echo server install script

./folders.sh
./ssh.sh
./docker_engine.sh
./jellyfin.sh
./qbittorrent.sh
./sonar.sh
./radar.sh
./jackett.sh
./filebrowser.sh

sudo ./program_shutdown.sh

echo -e "\n" 
echo qbittorrent web interface  http://localhost:8080
echo default user:admin, default password:adminadmin
echo -e "\n"
echo jellyfin web interface     http://localhost:8096
echo -e "\n"
echo sonarr web interface        http://localhost:8989
echo -e "\n"
echo radarr web interface        http://localhost:7878
echo -e "\n"
echo jackett web interface        http://localhost:9117
echo -e "\n"
echo filebrowser web interface  http://localhost:8081
echo default user:admin, default password:admin
echo -e "\n"
