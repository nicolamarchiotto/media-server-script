#!/bin/bash
echo uninstalling ssh...
sudo apt-get remove openssh-server

echo uninstalling docker engine, all images and volumes...
sudo apt-get purge -y docker-engine docker docker.io docker-ce docker-ce-cli docker-compose-plugin
sudo apt-get autoremove -y --purge docker-engine docker docker.io docker-ce docker-compose-plugin
sudo rm -rf /var/lib/docker /etc/docker
sudo rm /etc/apparmor.d/docker
sudo groupdel docker
sudo rm -rf /var/run/docker.sock

echo -e "\n"
echo -e "Deleting docker folder"
echo -e "\n"

rm -rf ~/dockers_configs

sudo systemctl disable mystartup.service
