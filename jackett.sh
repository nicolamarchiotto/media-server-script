sudo docker run -d \
  --name=jackett \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Europe/Rome \
  -e AUTO_UPDATE=true `#optional` \
  -e RUN_OPTS=<run options here> `#optional` \
  -p 9117:9117 \
  -v /jackett:/config \
  -v /media:/downloads \
  --restart unless-stopped \
  lscr.io/linuxserver/jackett:latest