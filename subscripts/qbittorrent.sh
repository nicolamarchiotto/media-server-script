sudo docker run -d \
  --name=qbittorrent \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Europe/Rome \
  -e WEBUI_PORT=8080 \
  -p 8080:8080 \
  -p 6881:6881 \
  -p 6881:6881/udp \
  -v ~/dockers/qbittorrent:/config \
  -v ~/media:/downloads \
  --restart unless-stopped \
  lscr.io/linuxserver/qbittorrent:latest
