sudo docker run -d \
  --name=jellyfin \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Europe/Rome \
  -p 8096:8096 \
  -p 8920:8920 `#optional` \
  -p 7359:7359/udp `#optional` \
  -p 1900:1900/udp `#optional` \
  -v ~/jellyfin:/config \
  -v ~/media/shows:/data/tvshows \
  -v ~/media/movies:/data/movies \
  --restart unless-stopped \
  lscr.io/linuxserver/jellyfin:latest