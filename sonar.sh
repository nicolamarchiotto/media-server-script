sudo docker run -d \
  --name=sonarr \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Europe/Rome \
  -p 8989:8989 \
  -v ~/sonar:/config \
  -v ~/media/shows:/tv `#optional` \
  -v ~/media:/downloads `#optional` \
  --restart unless-stopped \
  lscr.io/linuxserver/sonarr:latest