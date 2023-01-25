#!/bin/bash
echo creating folders "in" home
echo -e "\n"
echo creating media folders "if" it does not exist
if [ ! -d "~/media" ] 
    then mkdir ~/media 
fi
if [ ! -d "~/media/movies" ]
    then mkdir ~/media/movies
fi 
if [ ! -d "~/media/shows" ] 
    then mkdir ~/media/shows 
fi
mkdir -p ~/dockers
mkdir -p ~/dockers/jellyfin
mkdir -p ~/dockers/sonar
mkdir -p ~/dockers/radar
mkdir -p ~/dockers/qbittorrent
mkdir -p ~/dockers/filebrowser
mkdir -p ~/dockers/jackett
