sudo docker run -d \
  --name=radarr \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Europe/Rome \
  -p 7878:7878 \
  -v ~/dockers/radar:/config \
  -v ~/media/movies:/movies `#optional` \
  -v ~/media:/downloads `#optional` \
  --restart unless-stopped \
  lscr.io/linuxserver/radarr:latest
