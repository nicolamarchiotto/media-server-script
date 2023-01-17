#!/bin/bash
echo server install script

./folders.sh
./git.sh
./ssh.sh
./docker_engine.sh
./jellyfin.sh
./qbittorrent.sh
./sonar.sh
./radar.sh
./filebrowser.sh

echo -e "\n" 
echo qbittorrent web interface  http://localhost:8080
echo default user:admin, default password:adminadmin
echo -e "\n"
echo jellyfin web interface     http://localhost:8096
echo -e "\n"
echo sonar web interface        http://localhost:8989
echo -e "\n"
echo radar web interface        http://localhost:7878
echo -e "\n"
echo filebrowser web interface  http://localhost:8081
echo default user:admin, default password:admin
echo -e "\n"
